from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta

import pandas as pd


def third_friday(year: int, month: int) -> date:
    """CFFEX index futures last trading day is typically the 3rd Friday of the delivery month."""
    first = date(year, month, 1)
    # Monday=0 ... Sunday=6
    first_friday_offset = (4 - first.weekday()) % 7
    first_friday = first + timedelta(days=first_friday_offset)
    return first_friday + timedelta(days=14)  # third Friday


@dataclass(frozen=True)
class TradeCalendar:
    exchange: str
    df: pd.DataFrame  # expects columns: cal_date, is_open

    def is_open(self, d: date) -> bool:
        s = d.strftime("%Y%m%d")
        row = self.df[self.df["cal_date"] == s]
        if row.empty:
            return False
        return str(row["is_open"].iloc[0]) in ("1", "True", "true")

    def previous_open(self, d: date) -> date:
        # Find the nearest open day on or before d within the calendar frame.
        s = d.strftime("%Y%m%d")
        df = self.df[self.df["cal_date"] <= s].copy()
        if df.empty:
            raise ValueError("Trade calendar window too small to resolve previous open day")
        df = df[df["is_open"].astype(str).isin(["1", "True", "true"])]
        if df.empty:
            raise ValueError("No open days in trade calendar window")
        cal_date = str(df["cal_date"].max())
        return datetime.strptime(cal_date, "%Y%m%d").date()


def resolve_cffex_index_future_expiry(year: int, month: int, cal: TradeCalendar) -> date:
    """
    Base rule: 3rd Friday.
    Adjustment: if holiday/non-trading day, use the previous open day.
    """
    target = third_friday(year, month)
    if cal.is_open(target):
        return target
    return cal.previous_open(target)
