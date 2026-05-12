from __future__ import annotations

import sqlite3
import threading
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Optional

import numpy as np
from scipy.interpolate import interp1d

from .interfaces import DividendYieldProvider, RateProvider
from .models import IndexSpec


SHIBOR_NODE_COLS = ["on", "1w", "2w", "1m", "3m", "6m", "9m", "1y"]
SHIBOR_NODES = np.array([1, 7, 14, 30, 90, 180, 270, 360], dtype=float)


def _ymd(d: date | str) -> str:
    if isinstance(d, str):
        return d
    return d.strftime("%Y%m%d")


@dataclass(frozen=True)
class LocalStoreConfig:
    db_path: Path = Path(".index_pricing_local/market_cache.db")


class LocalMarketStore:
    def __init__(self, cfg: LocalStoreConfig | None = None) -> None:
        self.cfg = cfg or LocalStoreConfig()
        self.cfg.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.cfg.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS daily_factors (
                    trade_date TEXT NOT NULL,
                    product TEXT NOT NULL,
                    q REAL NOT NULL,
                    sh_on REAL,
                    sh_1w REAL,
                    sh_2w REAL,
                    sh_1m REAL,
                    sh_3m REAL,
                    sh_6m REAL,
                    sh_9m REAL,
                    sh_1y REAL,
                    source TEXT,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (trade_date, product)
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS minute_quotes (
                    ts_minute TEXT NOT NULL,
                    asof_date TEXT NOT NULL,
                    product TEXT NOT NULL,
                    contract TEXT NOT NULL,
                    spot_code TEXT NOT NULL,
                    fut_code TEXT NOT NULL,
                    spot REAL,
                    futures REAL,
                    basis REAL,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (ts_minute, product, contract)
                )
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_daily_factors_prod_date ON daily_factors(product, trade_date)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_minute_quotes_date ON minute_quotes(asof_date, product)")

    def upsert_daily_factor(
        self,
        trade_date: str,
        product: str,
        q: float,
        shibor_nodes: Dict[str, float],
        source: str = "daily_refresh",
    ) -> None:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO daily_factors (
                    trade_date, product, q,
                    sh_on, sh_1w, sh_2w, sh_1m, sh_3m, sh_6m, sh_9m, sh_1y,
                    source, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(trade_date, product) DO UPDATE SET
                    q=excluded.q,
                    sh_on=excluded.sh_on,
                    sh_1w=excluded.sh_1w,
                    sh_2w=excluded.sh_2w,
                    sh_1m=excluded.sh_1m,
                    sh_3m=excluded.sh_3m,
                    sh_6m=excluded.sh_6m,
                    sh_9m=excluded.sh_9m,
                    sh_1y=excluded.sh_1y,
                    source=excluded.source,
                    updated_at=excluded.updated_at
                """,
                (
                    trade_date,
                    product,
                    float(q),
                    float(shibor_nodes.get("on", 0.0)),
                    float(shibor_nodes.get("1w", 0.0)),
                    float(shibor_nodes.get("2w", 0.0)),
                    float(shibor_nodes.get("1m", 0.0)),
                    float(shibor_nodes.get("3m", 0.0)),
                    float(shibor_nodes.get("6m", 0.0)),
                    float(shibor_nodes.get("9m", 0.0)),
                    float(shibor_nodes.get("1y", 0.0)),
                    source,
                    now,
                ),
            )

    def has_daily_factor(self, trade_date: str, product: str) -> bool:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT 1 FROM daily_factors WHERE trade_date=? AND product=? LIMIT 1",
                (trade_date, product),
            ).fetchone()
        return row is not None

    def get_latest_daily_factor(self, asof: date, product: str) -> Optional[sqlite3.Row]:
        asof_s = _ymd(asof)
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT *
                FROM daily_factors
                WHERE product=? AND trade_date<=?
                ORDER BY trade_date DESC
                LIMIT 1
                """,
                (product, asof_s),
            ).fetchone()
        return row

    def get_latest_shibor_row(self, asof: date) -> Optional[sqlite3.Row]:
        asof_s = _ymd(asof)
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT *
                FROM daily_factors
                WHERE trade_date<=?
                ORDER BY trade_date DESC
                LIMIT 1
                """,
                (asof_s,),
            ).fetchone()
        return row

    def upsert_minute_quotes(self, asof_date: date, rows: list[dict]) -> None:
        if not rows:
            return
        ts_minute = datetime.now().strftime("%Y-%m-%d %H:%M:00")
        asof_s = _ymd(asof_date)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payload = []
        for row in rows:
            product = str(row["Product"])
            contract = str(row["Contract"])
            spot = row.get("Spot")
            fut = row.get("Futures")
            if spot is None or fut is None:
                continue
            spot_code = row.get("SpotCode", "")
            fut_code = row.get("FutCode", "")
            basis = float(fut) - float(spot)
            payload.append((ts_minute, asof_s, product, contract, spot_code, fut_code, float(spot), float(fut), basis, now))
        if not payload:
            return
        with self._lock, self._connect() as conn:
            conn.executemany(
                """
                INSERT INTO minute_quotes (
                    ts_minute, asof_date, product, contract, spot_code, fut_code,
                    spot, futures, basis, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(ts_minute, product, contract) DO UPDATE SET
                    asof_date=excluded.asof_date,
                    spot_code=excluded.spot_code,
                    fut_code=excluded.fut_code,
                    spot=excluded.spot,
                    futures=excluded.futures,
                    basis=excluded.basis,
                    updated_at=excluded.updated_at
                """,
                payload,
            )


class LocalDailyRateProvider(RateProvider):
    def __init__(self, store: LocalMarketStore, fallback_rate: float = 0.015) -> None:
        self.store = store
        self.fallback_rate = fallback_rate

    def get_shibor_rate(self, asof: date, days_to_expiry: int) -> float:
        row = self.store.get_latest_shibor_row(asof)
        if row is None:
            return float(self.fallback_rate)
        rates = np.array(
            [
                row["sh_on"],
                row["sh_1w"],
                row["sh_2w"],
                row["sh_1m"],
                row["sh_3m"],
                row["sh_6m"],
                row["sh_9m"],
                row["sh_1y"],
            ],
            dtype=float,
        )
        if np.isnan(rates).any() or np.all(rates == 0):
            return float(self.fallback_rate)
        days_f = float(max(1, int(days_to_expiry)))
        return float(interp1d(SHIBOR_NODES, rates, kind="linear", fill_value="extrapolate")(days_f))


class LocalDailyDividendProvider(DividendYieldProvider):
    def __init__(self, store: LocalMarketStore, fallback_q: float = 0.02) -> None:
        self.store = store
        self.fallback_q = fallback_q

    def get_dividend_yield(self, asof: date, index: IndexSpec, expiry_date: date) -> float:
        _ = expiry_date
        row = self.store.get_latest_daily_factor(asof, product=index.product)
        if row is None:
            return float(self.fallback_q)
        q = row["q"]
        if q is None:
            return float(self.fallback_q)
        return float(q)
