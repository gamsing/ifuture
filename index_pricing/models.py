from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class IndexSpec:
    product: str
    spot_code: str
    weight_code: str
    multiplier: float


@dataclass(frozen=True)
class ContractSpec:
    """
    Contract identified by year-month.

    Supports:
    - "2609" (YYMM)
    - "202609" (YYYYMM)
    """

    product: str
    year_month: str  # YYMM
    expiry_date: date

    @property
    def yymm(self) -> str:
        ym = self.year_month.strip()
        if len(ym) == 4 and ym.isdigit():
            return ym
        if len(ym) == 6 and ym.isdigit():
            # YYYYMM -> YYMM
            return ym[2:]
        raise ValueError(f"Unsupported year_month: {self.year_month!r} (expected YYMM or YYYYMM)")

    @property
    def year(self) -> int:
        ym = self.year_month.strip()
        if len(ym) == 6 and ym.isdigit():
            return int(ym[:4])
        if len(ym) == 4 and ym.isdigit():
            # Interpret as 20YYMM
            return 2000 + int(ym[:2])
        raise ValueError(f"Unsupported year_month: {self.year_month!r}")

    @property
    def month(self) -> int:
        ym = self.year_month.strip()
        if len(ym) == 6 and ym.isdigit():
            return int(ym[4:6])
        if len(ym) == 4 and ym.isdigit():
            return int(ym[2:4])
        raise ValueError(f"Unsupported year_month: {self.year_month!r}")


@dataclass(frozen=True)
class PricingInputs:
    asof_date: date
    S: float
    F: float
    r: float
    q: float
    T: float


@dataclass(frozen=True)
class PricingResult:
    FV: float
    deviation: float
    signal: int  # 1 long, -1 short, 0 neutral
    inputs: PricingInputs
    implied_q: float
    implied_r: float
