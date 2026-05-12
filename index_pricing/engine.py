from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import pandas as pd

from .analytics import CostOfCarryPricer, ExpiryCalendar, TimeToMaturity
from .interfaces import DividendYieldProvider, MarketDataProvider, RateProvider
from .models import ContractSpec, IndexSpec, PricingInputs, PricingResult
from .providers import (
    ConstituentWeightedDvProvider,
    IndexDailyBasicDyProvider,
    TushareConfig,
    TushareMarketData,
    TushareProvider,
    TushareRateData,
)


INDEX_REGISTRY: Dict[str, IndexSpec] = {
    "IH": IndexSpec(product="IH", spot_code="000016.SH", weight_code="000016.SH", multiplier=300.0),
    "IF": IndexSpec(product="IF", spot_code="000300.SH", weight_code="000300.SH", multiplier=300.0),
    "IC": IndexSpec(product="IC", spot_code="000905.SH", weight_code="000905.SH", multiplier=200.0),
    "IM": IndexSpec(product="IM", spot_code="000852.SH", weight_code="000852.SH", multiplier=200.0),
}


def _yymm(d: date) -> str:
    return d.strftime("%y%m")


def _add_months(d: date, months: int) -> date:
    month_idx = (d.year * 12 + (d.month - 1)) + months
    year = month_idx // 12
    month = month_idx % 12 + 1
    return date(year, month, 1)


def discover_default_live_contract_months(asof: date) -> List[str]:
    """
    CFFEX-like default:
    - spot month
    - next month
    - next two quarter months (strictly after next month)
    """
    contracts: List[str] = []
    seen = set()

    def push(dt: date) -> None:
        ym = _yymm(dt)
        if ym not in seen:
            seen.add(ym)
            contracts.append(ym)

    spot = date(asof.year, asof.month, 1)
    nxt = _add_months(spot, 1)
    push(spot)
    push(nxt)

    quarter_months = {3, 6, 9, 12}
    cursor = _add_months(nxt, 1)
    found_quarters = 0
    while found_quarters < 2:
        if cursor.month in quarter_months:
            push(cursor)
            found_quarters += 1
        cursor = _add_months(cursor, 1)

    return contracts


@dataclass(frozen=True)
class EngineConfig:
    threshold: float = 0.005
    fallback_q: float = 0.02
    cache_dir: Optional[Path] = Path(".index_pricing_cache")
    calendar_exchange: str = "SSE"  # used to resolve 'latest' trade date


class PricingEngine:
    def __init__(
        self,
        market_data: Optional[MarketDataProvider] = None,
        rate_data: Optional[RateProvider] = None,
        dy_provider: Optional[DividendYieldProvider] = None,
        cfg: Optional[EngineConfig] = None,
        tushare_provider: Optional[TushareProvider] = None,
        dividend_mode: str = "constituent",
    ) -> None:
        self.cfg = cfg or EngineConfig()
        self.pricer = CostOfCarryPricer()

        if market_data and rate_data and dy_provider:
            self.market_data = market_data
            self.rate_data = rate_data
            self.dy_provider = dy_provider
            self._tushare = None
            return

        ts_provider = tushare_provider
        if ts_provider is None:
            ts_cfg = TushareConfig(cache_dir=self.cfg.cache_dir)
            ts_provider = TushareProvider(ts_cfg)

        self._tushare = ts_provider
        self.market_data = TushareMarketData(ts_provider)
        self.rate_data = TushareRateData(ts_provider)
        self.dy_provider = self._make_dividend_provider(ts_provider, dividend_mode=dividend_mode)

    def _make_dividend_provider(self, ts_provider: TushareProvider, dividend_mode: str) -> DividendYieldProvider:
        mode = (dividend_mode or "").strip().lower()
        if mode in ("constituent", "weights", "bottomup"):
            return ConstituentWeightedDvProvider(provider=ts_provider, fallback_q=self.cfg.fallback_q)
        if mode in ("index", "dailybasic", "index_dailybasic"):
            return IndexDailyBasicDyProvider(provider=ts_provider, fallback_q=self.cfg.fallback_q)
        raise ValueError(f"Unknown dividend_mode: {dividend_mode!r} (use 'constituent' or 'index')")

    def resolve_asof(self, asof: date | str) -> date:
        if isinstance(asof, date):
            return asof
        s = str(asof).strip().lower()
        if s in ("today", "now"):
            return date.today()
        if s == "latest":
            if self._tushare is None:
                raise ValueError("asof='latest' requires a TushareProvider-backed engine")
            latest = self._tushare.latest_trade_date(exchange=self.cfg.calendar_exchange)
            return datetime.strptime(latest, "%Y%m%d").date()
        return datetime.strptime(s, "%Y%m%d").date()

    def discover_contract_months(self, product: str, asof: date) -> List[str]:
        maybe_method = getattr(self.market_data, "get_active_contract_months", None)
        if callable(maybe_method):
            active = list(maybe_method(product, asof))
            if active:
                return sorted({str(x).strip() for x in active})
        return discover_default_live_contract_months(asof)

    def price_contract(self, index: IndexSpec, year_month: str, asof: date | str) -> PricingResult:
        asof_dt = self.resolve_asof(asof)
        expiry = ExpiryCalendar.get_cffex_expiry(year_month)
        contract = ContractSpec(index.product, year_month, expiry)
        fut_code = f"{contract.product}{contract.year_month}.CFX"

        days_to_expiry, T = TimeToMaturity.compute_T(asof_dt, expiry)
        S = self.market_data.get_spot_close(asof_dt, index.spot_code)
        F = self.market_data.get_fut_close(asof_dt, fut_code)
        r = self.rate_data.get_shibor_rate(asof_dt, days_to_expiry)
        q = self.dy_provider.get_dividend_yield(asof_dt, index, expiry)
        pi = PricingInputs(asof_dt, float(S), float(F), float(r), float(q), float(T))
        return self.pricer.price(pi, threshold=self.cfg.threshold)


class BatchRunner:
    def __init__(self, engine: PricingEngine) -> None:
        self.engine = engine

    def run(self, tasks: Dict[str, List[str]], asof: date | str) -> pd.DataFrame:
        asof_dt = self.engine.resolve_asof(asof)
        results = []
        for product, months in tasks.items():
            index_spec = INDEX_REGISTRY[product]
            for ym in months:
                res = self.engine.price_contract(index_spec, ym, asof_dt)
                results.append(
                    {
                        "Date": asof_dt.strftime("%Y-%m-%d"),
                        "Product": product,
                        "Contract": ym,
                        "Days_To_Expiry": int(res.inputs.T * 365),
                        "Spot_Close": round(res.inputs.S, 2),
                        "Fut_Close": round(res.inputs.F, 2),
                        "r": round(res.inputs.r, 6),
                        "q": round(res.inputs.q, 6),
                        "FV": round(res.FV, 2),
                        "Deviation(%)": round(res.deviation * 100, 3),
                        "Signal": res.signal,
                        "Implied_q": round(res.implied_q, 6),
                        "Implied_r": round(res.implied_r, 6),
                    }
                )
        return pd.DataFrame(results)


class LiveMonitor:
    def __init__(
        self,
        engine: PricingEngine,
        products: Optional[Sequence[str]] = None,
        max_workers: int = 16,
    ) -> None:
        self.engine = engine
        self.products = list(products) if products else list(INDEX_REGISTRY.keys())
        self.max_workers = max(1, int(max_workers))

    def discover_tasks(self, asof: date | str = "today") -> Dict[str, List[str]]:
        asof_dt = self.engine.resolve_asof(asof)
        tasks: Dict[str, List[str]] = {}
        for product in self.products:
            tasks[product] = self.engine.discover_contract_months(product, asof_dt)
        return tasks

    def run_snapshot(self, asof: date | str = "today") -> pd.DataFrame:
        asof_dt = self.engine.resolve_asof(asof)
        tasks = self.discover_tasks(asof_dt)
        rows: List[Dict[str, object]] = []

        def _price_one(prod: str, ym: str) -> Dict[str, object]:
            index = INDEX_REGISTRY[prod]
            res = self.engine.price_contract(index, ym, asof_dt)
            basis = res.inputs.F - res.inputs.S
            return {
                "AsOf": asof_dt.strftime("%Y-%m-%d"),
                "Product": prod,
                "Contract": ym,
                "SpotCode": index.spot_code,
                "FutCode": f"{prod}{ym}.CFX",
                "Spot": round(res.inputs.S, 2),
                "Futures": round(res.inputs.F, 2),
                "Basis": round(basis, 2),
                "FV": round(res.FV, 2),
                "Deviation(%)": round(res.deviation * 100, 3),
                "Signal": res.signal,
                "r": round(res.inputs.r, 6),
                "q": round(res.inputs.q, 6),
                "Days_To_Expiry": int(res.inputs.T * 365),
            }

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            fut_map = {}
            for product, months in tasks.items():
                for ym in months:
                    fut = executor.submit(_price_one, product, ym)
                    fut_map[fut] = (product, ym)

            for fut in as_completed(fut_map):
                product, ym = fut_map[fut]
                try:
                    rows.append(fut.result())
                except Exception as exc:  # noqa: BLE001
                    rows.append(
                        {
                            "AsOf": asof_dt.strftime("%Y-%m-%d"),
                            "Product": product,
                            "Contract": ym,
                            "Spot": None,
                            "Futures": None,
                            "Basis": None,
                            "FV": None,
                            "Deviation(%)": None,
                            "Signal": None,
                            "r": None,
                            "q": None,
                            "Days_To_Expiry": None,
                            "Error": str(exc),
                        }
                    )

        df = pd.DataFrame(rows)
        if df.empty:
            return df
        if "Deviation(%)" in df.columns:
            dev_num = pd.to_numeric(df["Deviation(%)"], errors="coerce")
            df["AbsDeviation(%)"] = dev_num.abs()
            df = df.sort_values(["AbsDeviation(%)", "Product", "Contract"], ascending=[False, True, True])
        return df.reset_index(drop=True)


def products_from_csv(s: str) -> List[str]:
    parts = [p.strip().upper() for p in str(s).split(",") if p.strip()]
    for p in parts:
        if p not in INDEX_REGISTRY:
            raise ValueError(f"Unknown product: {p!r}")
    return parts
