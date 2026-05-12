from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
import threading
import time
from typing import Callable, Dict, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import tushare as ts

from .cache import CachePolicy, DiskCache
from .calendars import TradeCalendar
from .interfaces import DividendYieldProvider, MarketDataProvider, RateProvider
from .models import IndexSpec
from .retry import with_retry


def _ymd(d: date | str) -> str:
    if isinstance(d, str):
        return d
    return d.strftime("%Y%m%d")


@dataclass(frozen=True)
class TushareConfig:
    token: Optional[str] = None
    cache_dir: Optional[Path] = None
    cache_policy: CachePolicy = CachePolicy(enabled=True, ttl_seconds=24 * 3600)


class TushareProvider:
    def __init__(self, cfg: TushareConfig | None = None) -> None:
        cfg = cfg or TushareConfig()
        token = cfg.token or os.environ.get("TUSHARE_TOKEN") or os.environ.get("TS_TOKEN")
        # Avoid ts.set_token(), which writes ~/tk.csv (may be blocked in sandboxed environments).
        pro_kwargs = {"token": token} if token else {}
        self.pro = ts.pro_api(**pro_kwargs)
        self.cache = None
        if cfg.cache_dir is not None:
            self.cache = DiskCache(cfg.cache_dir, policy=cfg.cache_policy)

    def _cached(self, key: str, fn):
        if self.cache is None:
            return fn()
        return self.cache.get_or_set(key, fn)

    @with_retry()
    def trade_calendar(self, exchange: str, start_date: str, end_date: str) -> TradeCalendar:
        key = f"trade_cal:{exchange}:{start_date}:{end_date}"
        df = self._cached(key, lambda: self.pro.trade_cal(exchange=exchange, start_date=start_date, end_date=end_date))
        if "cal_date" not in df.columns or "is_open" not in df.columns:
            raise ValueError("Unexpected trade_cal schema from Tushare")
        return TradeCalendar(exchange=exchange, df=df[["cal_date", "is_open"]].copy())

    @with_retry()
    def latest_trade_date(self, exchange: str = "SSE", lookback_days: int = 30) -> str:
        end = date.today()
        start = end - timedelta(days=lookback_days)
        cal = self.trade_calendar(exchange=exchange, start_date=_ymd(start), end_date=_ymd(end))
        open_days = cal.df[cal.df["is_open"].astype(str).isin(["1", "True", "true"])]
        if open_days.empty:
            raise ValueError("No open days found in lookback window")
        today = _ymd(end)
        latest = str(open_days["cal_date"].max())
        # Daily bars may not be available for the current trading day yet; prefer the last completed day.
        if latest == today:
            prev = open_days[open_days["cal_date"] < today]
            if prev.empty:
                raise ValueError("No previous open day found in lookback window")
            latest = str(prev["cal_date"].max())
        return latest

    @with_retry()
    def index_close(self, ts_code: str, trade_date: str) -> float:
        key = f"index_daily:{ts_code}:{trade_date}"
        df = self._cached(key, lambda: self.pro.index_daily(ts_code=ts_code, start_date=trade_date, end_date=trade_date))
        if df.empty:
            raise ValueError(f"No index_daily for {ts_code} at {trade_date}")
        return float(df["close"].iloc[0])

    @with_retry()
    def fut_close(self, ts_code: str, trade_date: str) -> float:
        key = f"fut_daily:{ts_code}:{trade_date}"
        df = self._cached(key, lambda: self.pro.fut_daily(ts_code=ts_code, start_date=trade_date, end_date=trade_date))
        if df.empty:
            raise ValueError(f"No fut_daily for {ts_code} at {trade_date}")
        return float(df["close"].iloc[0])

    @with_retry()
    def shibor_rate(self, trade_date: str, days: int) -> float:
        """
        Interpolate SHIBOR nodes to a target maturity in days.
        Uses linear interpolation and extrapolates for long maturities.
        """
        key = f"shibor:{trade_date}"
        df = self._cached(key, lambda: self.pro.shibor(start_date=trade_date, end_date=trade_date))
        if df.empty:
            raise ValueError(f"No shibor data at {trade_date}")
        row = df.iloc[0]
        nodes = np.array([1, 7, 14, 30, 90, 180, 270, 360], dtype=float)
        rates = np.array(
            [row["on"], row["1w"], row["2w"], row["1m"], row["3m"], row["6m"], row["9m"], row["1y"]],
            dtype=float,
        )
        rates = rates / 100.0
        days_f = float(max(1, int(days)))
        return float(interp1d(nodes, rates, kind="linear", fill_value="extrapolate")(days_f))

    @with_retry()
    def shibor_nodes(self, trade_date: str) -> dict[str, float]:
        key = f"shibor:{trade_date}"
        df = self._cached(key, lambda: self.pro.shibor(start_date=trade_date, end_date=trade_date))
        if df.empty:
            raise ValueError(f"No shibor data at {trade_date}")
        row = df.iloc[0]
        return {
            "on": float(row["on"]) / 100.0,
            "1w": float(row["1w"]) / 100.0,
            "2w": float(row["2w"]) / 100.0,
            "1m": float(row["1m"]) / 100.0,
            "3m": float(row["3m"]) / 100.0,
            "6m": float(row["6m"]) / 100.0,
            "9m": float(row["9m"]) / 100.0,
            "1y": float(row["1y"]) / 100.0,
        }

    @with_retry()
    def index_dividend_yield(self, ts_code: str, trade_date: str) -> Optional[float]:
        """
        Try to read dividend yield directly from index_dailybasic if available.
        Returns a decimal (e.g. 0.02), or None if not available.
        """
        key = f"index_dailybasic:{ts_code}:{trade_date}"
        df = self._cached(
            key,
            lambda: self.pro.index_dailybasic(ts_code=ts_code, start_date=trade_date, end_date=trade_date),
        )
        if df.empty:
            return None
        for col in ("dividend_yield", "dividend_yield_ttm"):
            if col in df.columns and not pd.isna(df[col].iloc[0]):
                return float(df[col].iloc[0]) / 100.0
        return None

    @with_retry()
    def index_weights(self, index_code: str, start_date: str, end_date: str) -> pd.DataFrame:
        key = f"index_weight:{index_code}:{start_date}:{end_date}"
        df = self._cached(key, lambda: self.pro.index_weight(index_code=index_code, start_date=start_date, end_date=end_date))
        return df.copy()

    @with_retry()
    def daily_basic_dv_ttm(self, trade_date: str) -> pd.DataFrame:
        key = f"daily_basic:{trade_date}:dv_ttm"
        df = self._cached(key, lambda: self.pro.daily_basic(trade_date=trade_date, fields="ts_code,dv_ttm"))
        return df.copy()

    @with_retry()
    def stock_basic(self) -> pd.DataFrame:
        key = "stock_basic:ts_code,symbol,name,industry"
        df = self._cached(key, lambda: self.pro.stock_basic(fields="ts_code,symbol,name,industry"))
        return df.copy()


class TushareMarketData(MarketDataProvider):
    def __init__(self, provider: TushareProvider) -> None:
        self.provider = provider

    def get_spot_close(self, asof: date, spot_code: str) -> float:
        return self.provider.index_close(ts_code=spot_code, trade_date=_ymd(asof))

    def get_fut_close(self, asof: date, fut_code: str) -> float:
        return self.provider.fut_close(ts_code=fut_code, trade_date=_ymd(asof))


class TushareRateData(RateProvider):
    def __init__(self, provider: TushareProvider) -> None:
        self.provider = provider

    def get_shibor_rate(self, asof: date, days_to_expiry: int) -> float:
        return self.provider.shibor_rate(trade_date=_ymd(asof), days=days_to_expiry)


@dataclass(frozen=True)
class IndexDailyBasicDyProvider(DividendYieldProvider):
    provider: TushareProvider
    fallback_q: float = 0.02

    def get_dividend_yield(self, asof: date, index: IndexSpec, expiry_date: date) -> float:
        q = self.provider.index_dividend_yield(ts_code=index.spot_code, trade_date=_ymd(asof))
        if q is None or q <= 0:
            return float(self.fallback_q)
        return float(q)


@dataclass(frozen=True)
class ConstituentWeightedDvProvider(DividendYieldProvider):
    provider: TushareProvider
    fallback_q: float = 0.02
    dv_ttm_cap_pct: float = 15.0
    weight_lookback_days: int = 365

    def get_dividend_yield(self, asof: date, index: IndexSpec, expiry_date: date) -> float:
        # expiry_date is accepted for API compatibility; this implementation uses dv_ttm (annualized).
        end = asof
        start = end - timedelta(days=self.weight_lookback_days)
        w_df = self.provider.index_weights(index_code=index.weight_code, start_date=_ymd(start), end_date=_ymd(end))
        if w_df.empty:
            return float(self.fallback_q)
        latest = str(w_df["trade_date"].max())
        w_df = w_df[w_df["trade_date"] == latest].copy()
        if "con_code" in w_df.columns:
            w_df = w_df.rename(columns={"con_code": "ts_code"})

        b_df = self.provider.daily_basic_dv_ttm(trade_date=_ymd(asof))
        if b_df.empty:
            return float(self.fallback_q)

        merged = pd.merge(w_df, b_df, on="ts_code", how="inner")
        if merged.empty:
            return float(self.fallback_q)

        merged["w_norm"] = merged["weight"] / merged["weight"].sum()
        merged["dv_clean"] = merged["dv_ttm"].fillna(0).clip(upper=self.dv_ttm_cap_pct) / 100.0
        q = float((merged["dv_clean"] * merged["w_norm"]).sum())
        return q if q > 0 else float(self.fallback_q)


class RealTimeProvider(MarketDataProvider, RateProvider):
    """
    Real-time adapter for spot/futures/rate data.

    Inject your feed callbacks so this provider can be used by PricingEngine
    without changing pricing logic.
    """

    def __init__(
        self,
        spot_last_fetcher: Callable[[str], float],
        fut_last_fetcher: Callable[[str], float],
        rate_fetcher: Optional[Callable[[date, int], float]] = None,
        active_contracts_fetcher: Optional[Callable[[str, date], Sequence[str]]] = None,
        fallback_rate: float = 0.015,
    ) -> None:
        self._spot_last_fetcher = spot_last_fetcher
        self._fut_last_fetcher = fut_last_fetcher
        self._rate_fetcher = rate_fetcher
        self._active_contracts_fetcher = active_contracts_fetcher
        self._fallback_rate = fallback_rate

    def get_spot_last(self, spot_code: str) -> float:
        return float(self._spot_last_fetcher(spot_code))

    def get_fut_last(self, fut_code: str) -> float:
        return float(self._fut_last_fetcher(fut_code))

    def get_spot_close(self, asof: date, spot_code: str) -> float:
        return self.get_spot_last(spot_code)

    def get_fut_close(self, asof: date, fut_code: str) -> float:
        return self.get_fut_last(fut_code)

    def get_shibor_rate(self, asof: date, days_to_expiry: int) -> float:
        if self._rate_fetcher is None:
            return float(self._fallback_rate)
        return float(self._rate_fetcher(asof, days_to_expiry))

    def get_active_contract_months(self, product: str, asof: date) -> Sequence[str]:
        if self._active_contracts_fetcher is None:
            return []
        return list(self._active_contracts_fetcher(product, asof))


class RealTimeConstituentWeightedDvProvider(DividendYieldProvider):
    """
    Live q estimator:
    - index weights are cached and refreshed periodically
    - DV_TTM snapshot is refreshed every request
    """

    def __init__(
        self,
        weight_fetcher: Callable[[str, date], pd.DataFrame],
        realtime_dv_ttm_fetcher: Callable[[date], pd.DataFrame],
        fallback_q: float = 0.02,
        dv_ttm_cap_pct: float = 15.0,
        weight_cache_ttl_seconds: int = 30 * 60,
        dv_cache_ttl_seconds: int = 5,
    ) -> None:
        self.weight_fetcher = weight_fetcher
        self.realtime_dv_ttm_fetcher = realtime_dv_ttm_fetcher
        self.fallback_q = fallback_q
        self.dv_ttm_cap_pct = dv_ttm_cap_pct
        self.weight_cache_ttl_seconds = weight_cache_ttl_seconds
        self.dv_cache_ttl_seconds = dv_cache_ttl_seconds
        self._lock = threading.Lock()
        self._weight_cache: Dict[str, Tuple[float, pd.DataFrame]] = {}
        self._dv_cache: Dict[str, Tuple[float, pd.DataFrame]] = {}

    @staticmethod
    def _normalize_weights(weight_df: pd.DataFrame) -> pd.DataFrame:
        df = weight_df.copy()
        if "con_code" in df.columns and "ts_code" not in df.columns:
            df = df.rename(columns={"con_code": "ts_code"})
        if "trade_date" in df.columns:
            latest = str(df["trade_date"].max())
            df = df[df["trade_date"] == latest].copy()
        return df

    def _get_weights(self, index_code: str, asof: date) -> pd.DataFrame:
        now = time.time()
        with self._lock:
            if index_code in self._weight_cache:
                ts_cached, cached_df = self._weight_cache[index_code]
                if now - ts_cached < self.weight_cache_ttl_seconds:
                    return cached_df.copy()

        try:
            fresh = self.weight_fetcher(index_code, asof)
            if not fresh.empty:
                fresh = self._normalize_weights(fresh)
        except Exception:
            # Cache an empty frame briefly to avoid repeated slow failures.
            fresh = pd.DataFrame()
        with self._lock:
            self._weight_cache[index_code] = (now, fresh.copy())
        return fresh

    def _get_dv_ttm(self, asof: date) -> pd.DataFrame:
        key = asof.strftime("%Y%m%d")
        now = time.time()
        with self._lock:
            cached = self._dv_cache.get(key)
            if cached is not None:
                ts_cached, cached_df = cached
                if now - ts_cached < self.dv_cache_ttl_seconds:
                    return cached_df.copy()
        try:
            fresh = self.realtime_dv_ttm_fetcher(asof)
            if fresh is None:
                fresh = pd.DataFrame()
        except Exception:
            fresh = pd.DataFrame()
        with self._lock:
            self._dv_cache[key] = (now, fresh.copy())
        return fresh

    def get_dividend_yield(self, asof: date, index: IndexSpec, expiry_date: date) -> float:
        _ = expiry_date  # reserved for future period-specific dividend modeling
        try:
            weight_df = self._get_weights(index.weight_code, asof)
        except Exception:
            return float(self.fallback_q)
        if weight_df.empty:
            return float(self.fallback_q)

        dv_df = self._get_dv_ttm(asof)
        if dv_df.empty:
            return float(self.fallback_q)
        if "ts_code" not in dv_df.columns or "dv_ttm" not in dv_df.columns:
            return float(self.fallback_q)

        merged = pd.merge(weight_df, dv_df[["ts_code", "dv_ttm"]], on="ts_code", how="inner")
        if merged.empty:
            return float(self.fallback_q)

        merged["w_norm"] = merged["weight"] / merged["weight"].sum()
        merged["dv_clean"] = merged["dv_ttm"].fillna(0).clip(upper=self.dv_ttm_cap_pct) / 100.0
        q = float((merged["dv_clean"] * merged["w_norm"]).sum())
        return q if q > 0 else float(self.fallback_q)
