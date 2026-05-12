from __future__ import annotations

import calendar
import math
from dataclasses import dataclass
from datetime import date

from .models import PricingInputs, PricingResult


class ExpiryCalendar:
    @staticmethod
    def get_cffex_expiry(year_month: str) -> date:
        """CFFEX index futures: the third Friday of the contract month."""
        ym = year_month.strip()
        if len(ym) != 4 or not ym.isdigit():
            raise ValueError(f"Unsupported year_month: {year_month!r} (expected YYMM like '2609')")
        year = 2000 + int(ym[:2])
        month = int(ym[2:])
        c = calendar.monthcalendar(year, month)
        fridays = [week[4] for week in c if week[4] != 0]
        return date(year, month, fridays[2])


class TimeToMaturity:
    @staticmethod
    def compute_T(asof_date: date, expiry_date: date) -> tuple[int, float]:
        """Returns (calendar_days, annualized_T)."""
        days = (expiry_date - asof_date).days
        days = max(days, 0)
        return days, days / 365.0


@dataclass(frozen=True)
class CostOfCarryPricer:
    def price(self, inputs: PricingInputs, threshold: float = 0.005) -> PricingResult:
        S, F, r, q, T = inputs.S, inputs.F, inputs.r, inputs.q, inputs.T

        if T <= 0:
            return PricingResult(FV=S, deviation=0.0, signal=0, inputs=inputs, implied_q=q, implied_r=r)

        FV = S * math.exp((r - q) * T)
        dev = (F - FV) / FV if FV != 0 else 0.0

        signal = 0
        if dev > threshold:
            signal = -1
        elif dev < -threshold:
            signal = 1

        implied_q = r - math.log(F / S) / T if (F > 0 and S > 0) else 0.0
        implied_r = q + math.log(F / S) / T if (F > 0 and S > 0) else 0.0

        return PricingResult(
            FV=float(FV),
            deviation=float(dev),
            signal=int(signal),
            inputs=inputs,
            implied_q=float(implied_q),
            implied_r=float(implied_r),
        )
