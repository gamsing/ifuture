from __future__ import annotations

from datetime import date
from typing import Protocol

from .models import IndexSpec


class MarketDataProvider(Protocol):
    def get_spot_close(self, asof: date, spot_code: str) -> float: ...
    def get_fut_close(self, asof: date, fut_code: str) -> float: ...


class RateProvider(Protocol):
    def get_shibor_rate(self, asof: date, days_to_expiry: int) -> float: ...


class DividendYieldProvider(Protocol):
    def get_dividend_yield(self, asof: date, index: IndexSpec, expiry_date: date) -> float: ...
