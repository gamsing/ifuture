from __future__ import annotations

import contextlib
import io
import os
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple

import pandas as pd
import tushare as ts

from index_pricing.analytics import ExpiryCalendar
from index_pricing.engine import discover_default_live_contract_months
from index_pricing.providers import TushareConfig, TushareProvider


_LOCK = threading.Lock()

# ── Price cache: key -> (cached_ts, price) ───────────────────────────────
_LAST_CACHE: Dict[str, Tuple[float, float]] = {}

# ── Quote metadata: key -> (cached_ts, source, quote_time) ───────────────
# source: "RT" (realtime) | "STALE" (historical pro_bar fallback)
_QUOTE_META: Dict[str, Tuple[float, str, str]] = {}

_ACTIVE_CONTRACTS_CACHE: Dict[str, Tuple[float, List[str]]] = {}
_MAIN_MAPPING_CACHE: Dict[str, Tuple[float, str]] = {}
_HEALTH_CACHE: Dict[str, Tuple[float, Dict[str, str]]] = {}
_PROVIDER_CACHE: Dict[str, TushareProvider] = {}

# ── TTL constants ─────────────────────────────────────────────────────────
_LAST_TTL_SECONDS = 50
_ACTIVE_CONTRACTS_TTL_SECONDS = 300
_MAPPING_TTL_SECONDS = 60
_HEALTH_TTL_SECONDS = 30
_GLOBAL_BATCH_TTL_SECONDS = 15   # how often the big batch prefetch runs
_DEFAULT_RATE = 0.015

# ── Spot / product constants ──────────────────────────────────────────────
_ALL_SPOT_CODES = "000016.SH,000300.SH,000905.SH,000852.SH"

# Main-contract tushare codes (used for fut_mapping)
_PRODUCT_MAIN_MAP: Dict[str, str] = {
    "IH": "IH.CFX",
    "IF": "IF.CFX",
    "IC": "IC.CFX",
    "IM": "IM.CFX",
}

# ── Global batch state ────────────────────────────────────────────────────
_GLOBAL_BATCH_TS: float = 0.0
_GLOBAL_BATCH_LOCK = threading.Lock()

# ── Circuit breakers: endpoint -> (disabled_until_ts, last_error) ────────
# When an endpoint returns a token error we back off for _CB_COOLDOWN_SECONDS
# to avoid flooding stdout with Tushare's "您的token不对" prints.
_CB_COOLDOWN_SECONDS = 600   # 10 minutes
_CIRCUIT_BREAKERS: Dict[str, Tuple[float, str]] = {}
_CB_LOCK = threading.Lock()


def _cb_is_open(endpoint: str) -> bool:
    """Return True if the circuit breaker allows calls to this endpoint."""
    with _CB_LOCK:
        entry = _CIRCUIT_BREAKERS.get(endpoint)
    if entry is None:
        return True
    disabled_until, _ = entry
    return time.time() >= disabled_until


def _cb_trip(endpoint: str, reason: str) -> None:
    """Trip the circuit breaker for an endpoint."""
    with _CB_LOCK:
        _CIRCUIT_BREAKERS[endpoint] = (time.time() + _CB_COOLDOWN_SECONDS, reason)


def _cb_reason(endpoint: str) -> str:
    with _CB_LOCK:
        entry = _CIRCUIT_BREAKERS.get(endpoint)
    return entry[1] if entry else ""


@contextlib.contextmanager
def _quiet_tushare():
    """Suppress Tushare SDK prints to stdout (it prints error messages before raising)."""
    trap = io.StringIO()
    with contextlib.redirect_stdout(trap):
        yield trap


# ─────────────────────────────────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────────────────────────────────

def _now_ts() -> float:
    return time.time()


def _resolve_token() -> str:
    return (
        os.environ.get("TUSHARE_RT_TOKEN")
        or os.environ.get("TUSHARE_TOKEN")
        or os.environ.get("TS_TOKEN")
        or ""
    )


def _get_provider() -> TushareProvider:
    token = _resolve_token()
    with _LOCK:
        p = _PROVIDER_CACHE.get(token)
        if p is not None:
            return p
    p = TushareProvider(TushareConfig(token=token if token else None))
    with _LOCK:
        _PROVIDER_CACHE[token] = p
    return p


def _get_pro():
    return _get_provider().pro


def _cached_last_get(key: str) -> Optional[float]:
    now = _now_ts()
    with _LOCK:
        v = _LAST_CACHE.get(key)
    if v is None:
        return None
    ts_cached, value = v
    if now - ts_cached > _LAST_TTL_SECONDS:
        return None
    return float(value)


def _cached_last_set(key: str, value: float, source: str = "RT", quote_time: str = "") -> None:
    now = _now_ts()
    with _LOCK:
        _LAST_CACHE[key] = (now, float(value))
        _QUOTE_META[key] = (now, source, quote_time)


def _extract_product_prefix(ts_code: str) -> str:
    m = re.match(r"^([A-Z]{2})", ts_code.strip().upper())
    if not m:
        return ""
    return m.group(1)


def _get_time_col(df: pd.DataFrame) -> Optional[str]:
    """Return the first available time column name (rt_idx_min uses 'time'; rt_fut_min uses 'trade_time')."""
    for c in ("time", "trade_time"):
        if c in df.columns:
            return c
    return None


def _normalize_rt_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalise realtime endpoint output to always have 'ts_code' and 'close' columns.
    Tushare rt_idx_min / rt_fut_min use 'code' (not 'ts_code') as the identifier column.
    """
    out = df.copy()
    if out.empty:
        return out
    cols_lower = {c.lower(): c for c in out.columns}

    # ts_code: accept 'ts_code' or 'code'
    code_col = cols_lower.get("ts_code") or cols_lower.get("code")
    if code_col is None:
        raise ValueError("rt endpoint output missing ts_code/code column")
    if code_col != "ts_code":
        out = out.rename(columns={code_col: "ts_code"})

    # close: straightforward
    close_col = cols_lower.get("close")
    if close_col is None:
        raise ValueError("rt endpoint output missing close column")
    if close_col != "close":
        out = out.rename(columns={close_col: "close"})

    return out


def _cache_rt_df_rows(df: pd.DataFrame, asset_tag: str, source: str = "RT") -> None:
    """Write each row of a normalised rt dataframe into the price + meta caches."""
    if df.empty or "ts_code" not in df.columns or "close" not in df.columns:
        return
    time_col = _get_time_col(df)
    for _, row in df.iterrows():
        try:
            code = str(row["ts_code"]).strip().upper()
            value = float(row["close"])
            qt = str(row[time_col]) if (time_col and pd.notna(row.get(time_col))) else ""
            _cached_last_set(f"last:{asset_tag}:{code}", value, source=source, quote_time=qt)
        except Exception:
            continue


def _rt_fut_min_batch(ts_codes: List[str], freq: str = "1MIN") -> pd.DataFrame:
    """
    Call rt_fut_min with a comma-separated list of contract codes.
    Returns a deduplicated DataFrame (one row per ts_code, latest bar).
    Returns empty DataFrame on any error.
    """
    cleaned = [x.strip().upper() for x in ts_codes if str(x).strip()]
    if not cleaned:
        return pd.DataFrame()
    joined = ",".join(cleaned)
    try:
        df = _get_pro().rt_fut_min(ts_code=joined, freq=freq)
    except Exception:
        return pd.DataFrame()
    if df is None or df.empty:
        return pd.DataFrame()
    try:
        out = _normalize_rt_df(df)
    except Exception:
        return pd.DataFrame()
    time_col = _get_time_col(out)
    if time_col:
        out = out.sort_values(time_col, ascending=False).drop_duplicates(subset=["ts_code"], keep="first")
    else:
        out = out.drop_duplicates(subset=["ts_code"], keep="first")
    return out.reset_index(drop=True)


def _fetch_last_minute_close_probar(ts_code: str, asset: str) -> float:
    """
    Historical fallback via ts.pro_bar.
    Returns the most recent minute-bar close from the last ~24 hours.
    Marks the result as STALE in the metadata cache.
    """
    cache_key = f"last:{asset}:{ts_code}"
    # Use stale cache to avoid hammering the API
    with _LOCK:
        v = _LAST_CACHE.get(cache_key)
    if v is not None:
        return float(v[1])

    end = datetime.now()
    start = end - timedelta(days=1)
    df = None
    try:
        df = ts.pro_bar(
            ts_code=ts_code,
            asset=asset,
            freq="1min",
            start_date=start.strftime("%Y-%m-%d %H:%M:%S"),
            end_date=end.strftime("%Y-%m-%d %H:%M:%S"),
            api=_get_pro(),
        )
    except Exception:
        pass

    if df is None or df.empty:
        raise ValueError(f"No minute bars for {ts_code}")
    if "trade_time" in df.columns:
        latest = df.sort_values("trade_time", ascending=False).iloc[0]
    else:
        latest = df.iloc[0]
    if "close" not in latest:
        raise ValueError(f"Minute bar schema missing 'close' for {ts_code}")
    value = float(latest["close"])
    _cached_last_set(cache_key, value, source="STALE", quote_time="")
    return value


def _get_or_fetch_mapping(main_code: str) -> str:
    """
    Returns the current active contract code for a main contract (e.g. 'IM.CFX' -> 'IM2603.CFX').
    Uses fut_mapping; column is 'mapping_ts_code' (Tushare naming).
    Result is cached for _MAPPING_TTL_SECONDS.
    """
    now = _now_ts()
    with _LOCK:
        c = _MAIN_MAPPING_CACHE.get(main_code)
    if c is not None and (now - c[0] < _MAPPING_TTL_SECONDS):
        return c[1]
    df_map = _get_pro().fut_mapping(ts_code=main_code)
    if df_map is None or df_map.empty:
        raise ValueError(f"fut_mapping returned empty for {main_code}")
    # Column is 'mapping_ts_code' in Tushare API
    col = "mapping_ts_code" if "mapping_ts_code" in df_map.columns else (
        "mapping_code" if "mapping_code" in df_map.columns else None
    )
    if col is None:
        raise ValueError(f"fut_mapping missing mapping column; got: {df_map.columns.tolist()}")
    # Sort descending by trade_date to get latest mapping
    if "trade_date" in df_map.columns:
        df_map = df_map.sort_values("trade_date", ascending=False)
    mapping_code = str(df_map.iloc[0][col]).strip().upper()
    if not mapping_code:
        raise ValueError(f"Empty mapping_code for {main_code}")
    with _LOCK:
        _MAIN_MAPPING_CACHE[main_code] = (now, mapping_code)
    return mapping_code


# ─────────────────────────────────────────────────────────────────────────
# Batch prefetch  (primary realtime path)
# ─────────────────────────────────────────────────────────────────────────

def _batch_fetch_spots() -> None:
    """
    Primary spot path: single rt_idx_min call with all 4 index codes.
    Uses circuit breaker to avoid repeated calls after a token rejection.
    """
    if not _cb_is_open("rt_idx_min"):
        return
    try:
        with _quiet_tushare() as trapped:
            df = _get_pro().rt_idx_min(ts_code=_ALL_SPOT_CODES, freq="1MIN")
        printed = trapped.getvalue()
        if "token" in printed.lower() or "不对" in printed:
            _cb_trip("rt_idx_min", printed.strip().splitlines()[0] if printed.strip() else "token_error")
            return
        if df is None or df.empty:
            return
        out = _normalize_rt_df(df)
        time_col = _get_time_col(out)
        if time_col:
            out = out.sort_values(time_col, ascending=False).drop_duplicates(subset=["ts_code"], keep="first")
        _cache_rt_df_rows(out, asset_tag="I", source="RT")
    except Exception:
        pass


def _batch_fetch_futures(asof: date) -> None:
    """
    Primary futures path:
    1. fut_mapping for each product concurrently  -> 4 mapping codes
    2. rt_fut_min with batch of mapping codes + all active contracts
    All results are written to cache with source="RT".
    """
    now = _now_ts()

    # Step 1 – get mapping codes for all 4 products concurrently
    def _map_one(main_code: str) -> Optional[str]:
        with _LOCK:
            c = _MAIN_MAPPING_CACHE.get(main_code)
        if c is not None and (now - c[0] < _MAPPING_TTL_SECONDS):
            return c[1]
        try:
            df_map = _get_pro().fut_mapping(ts_code=main_code)
            if df_map is None or df_map.empty:
                return None
            col = "mapping_ts_code" if "mapping_ts_code" in df_map.columns else (
                "mapping_code" if "mapping_code" in df_map.columns else None
            )
            if col is None:
                return None
            if "trade_date" in df_map.columns:
                df_map = df_map.sort_values("trade_date", ascending=False)
            code = str(df_map.iloc[0][col]).strip().upper()
            if not code:
                return None
            with _LOCK:
                _MAIN_MAPPING_CACHE[main_code] = (now, code)
            return code
        except Exception:
            return None

    mapping_codes: List[str] = []
    with ThreadPoolExecutor(max_workers=4) as ex:
        fmap = {ex.submit(_map_one, main): main for main in _PRODUCT_MAIN_MAP.values()}
        for f in as_completed(fmap):
            try:
                code = f.result()
                if code:
                    mapping_codes.append(code)
            except Exception:
                pass

    # Step 2 – build full list of active contracts (calendar-based)
    active_contracts: List[str] = []
    months = discover_default_live_contract_months(asof)
    for product in _PRODUCT_MAIN_MAP:
        for ym in months:
            active_contracts.append(f"{product}{ym}.CFX")

    # Mapping codes go first so they get priority in dedup
    all_codes = list(dict.fromkeys(mapping_codes + active_contracts))
    if not all_codes:
        return

    # Step 3 – single batch rt_fut_min call
    df = _rt_fut_min_batch(all_codes, freq="1MIN")
    if not df.empty:
        _cache_rt_df_rows(df, asset_tag="FT", source="RT")


def _do_global_batch_prefetch(asof: date) -> None:
    """
    Trigger a full spot + futures batch prefetch when the last one is stale.
    Non-blocking: if another thread is already fetching, skip (they'll update the cache).
    """
    global _GLOBAL_BATCH_TS
    now = _now_ts()
    # Fast path without lock
    if now - _GLOBAL_BATCH_TS < _GLOBAL_BATCH_TTL_SECONDS:
        return
    # One thread does the actual work; others skip
    acquired = _GLOBAL_BATCH_LOCK.acquire(blocking=False)
    if not acquired:
        return
    try:
        # Double-check inside lock
        if now - _GLOBAL_BATCH_TS < _GLOBAL_BATCH_TTL_SECONDS:
            return
        _GLOBAL_BATCH_TS = now  # mark immediately to prevent pile-up
        _batch_fetch_spots()
        _batch_fetch_futures(asof)
    finally:
        _GLOBAL_BATCH_LOCK.release()


# ─────────────────────────────────────────────────────────────────────────
# Public API – price fetchers
# ─────────────────────────────────────────────────────────────────────────

def get_spot_last(ts_code: str) -> float:
    """
    Realtime spot index price.
    Primary:  batch rt_idx_min (via _do_global_batch_prefetch)
    Fallback: single rt_idx_min call
    Final:    pro_bar historical (STALE)
    """
    code = str(ts_code).strip().upper()
    cache_key = f"last:I:{code}"

    _do_global_batch_prefetch(date.today())

    cached = _cached_last_get(cache_key)
    if cached is not None:
        return cached

    # Single-code direct fallback (skip if circuit breaker is tripped)
    if _cb_is_open("rt_idx_min"):
        try:
            with _quiet_tushare() as trapped:
                df = _get_pro().rt_idx_min(ts_code=code, freq="1MIN")
            printed = trapped.getvalue()
            if "token" in printed.lower() or "不对" in printed:
                _cb_trip("rt_idx_min", printed.strip().splitlines()[0] if printed.strip() else "token_error")
            elif df is not None and not df.empty and "close" in df.columns:
                time_col = _get_time_col(df)
                if time_col:
                    df = df.sort_values(time_col, ascending=False)
                value = float(df.iloc[0]["close"])
                qt = str(df.iloc[0][time_col]) if time_col else ""
                _cached_last_set(cache_key, value, source="RT", quote_time=qt)
                return value
        except Exception:
            pass

    # Stale historical fallback
    return _fetch_last_minute_close_probar(code, asset="I")


def get_fut_last(ts_code: str) -> float:
    """
    Realtime futures price.
    Primary:  batch fut_mapping + rt_fut_min (via _do_global_batch_prefetch)
    Fallback: targeted fut_mapping(product.CFX) -> rt_fut_min([mapping_code, ts_code])
    Final:    pro_bar historical (STALE)
    """
    code = str(ts_code).strip().upper()
    cache_key = f"last:FT:{code}"

    _do_global_batch_prefetch(date.today())

    cached = _cached_last_get(cache_key)
    if cached is not None:
        return cached

    # Targeted fallback using correct mapping flow
    product = _extract_product_prefix(code)
    if product in _PRODUCT_MAIN_MAP:
        try:
            main_code = _PRODUCT_MAIN_MAP[product]
            mapping_code = _get_or_fetch_mapping(main_code)
            # Request both the active main contract AND the specific contract
            codes_to_fetch = list(dict.fromkeys([mapping_code, code]))
            df = _rt_fut_min_batch(codes_to_fetch, freq="1MIN")
            if not df.empty:
                _cache_rt_df_rows(df, asset_tag="FT", source="RT")
            cached = _cached_last_get(cache_key)
            if cached is not None:
                return cached
        except Exception:
            pass

    # Stale historical fallback (marks source="STALE")
    return _fetch_last_minute_close_probar(code, asset="FT")


def get_last_quote_meta(ts_code: str, asset_tag: str = "FT") -> Dict[str, object]:
    """
    Return source / quote_time / age metadata for a given code.
    Used by monitor_ui to display RT vs STALE badge per contract row.

    Returns dict with keys:
      source      – "RT", "STALE", or "unknown"
      quote_time  – timestamp string from the API (may be empty)
      price       – last cached price (float or None)
      age_seconds – seconds since last cache update (float or None)
    """
    key = f"last:{asset_tag}:{ts_code}"
    with _LOCK:
        meta = _QUOTE_META.get(key)
        last = _LAST_CACHE.get(key)
    if meta is None:
        return {"source": "unknown", "quote_time": "", "price": None, "age_seconds": None}
    now = _now_ts()
    cached_ts, source, quote_time = meta
    price = last[1] if last else None
    return {
        "source": source,
        "quote_time": quote_time,
        "price": price,
        "age_seconds": round(now - cached_ts, 1),
    }


# ─────────────────────────────────────────────────────────────────────────
# Public API – convenience / intraday helpers
# ─────────────────────────────────────────────────────────────────────────

def get_main_contract_rt_min(main_code: str, frequency: str = "1MIN") -> pd.DataFrame:
    """
    Step 1: fut_mapping(main_code) -> mapping_code
    Step 2: rt_fut_min(mapping_code, freq)
    """
    main = str(main_code).strip().upper()
    mapping_code = _get_or_fetch_mapping(main)
    try:
        df_rt = _get_pro().rt_fut_min(ts_code=mapping_code, freq=frequency)
    except Exception as exc:
        raise ValueError(f"rt_fut_min failed for {mapping_code}: {exc}") from exc
    if df_rt is None or df_rt.empty:
        raise ValueError(f"rt_fut_min returned empty for {mapping_code}")
    out = _normalize_rt_df(df_rt)
    _cache_rt_df_rows(out, asset_tag="FT", source="RT")
    return out


def get_main_contracts_rt_min(main_codes: List[str], frequency: str = "1MIN") -> pd.DataFrame:
    """Fetch realtime minute data for multiple main-contract codes via mapping."""
    mapped: List[str] = []
    for raw in main_codes:
        main = str(raw).strip().upper()
        if not main:
            continue
        try:
            mapped.append(_get_or_fetch_mapping(main))
        except Exception:
            continue
    if not mapped:
        return pd.DataFrame()
    out = _rt_fut_min_batch(mapped, freq=frequency)
    _cache_rt_df_rows(out, asset_tag="FT", source="RT")
    return out


def get_intraday_minute_bars(ts_code: str, freq: str = "1MIN") -> pd.DataFrame:
    """
    Fetch today's full intraday minute bars for a futures contract via rt_fut_min_daily.
    Returns a DataFrame sorted ascending by time with at minimum ts_code and close columns.
    """
    code = str(ts_code).strip().upper()
    try:
        df = _get_pro().rt_fut_min_daily(ts_code=code, freq=freq)
        if df is None or df.empty:
            return pd.DataFrame()
        out = _normalize_rt_df(df)
        time_col = _get_time_col(out)
        if time_col:
            out = out.sort_values(time_col, ascending=True)
        return out.reset_index(drop=True)
    except Exception:
        return pd.DataFrame()


def get_rate(asof: date, days_to_expiry: int) -> float:
    try:
        provider = _get_provider()
        latest = provider.latest_trade_date(exchange="SSE")
        return float(provider.shibor_rate(trade_date=latest, days=days_to_expiry))
    except Exception:
        return float(_DEFAULT_RATE)


def _expiry_not_passed(ym: str, asof: date) -> bool:
    try:
        return asof <= ExpiryCalendar.get_cffex_expiry(ym)
    except Exception:
        return True


def get_active_contract_months(product: str, asof: date) -> List[str]:
    product = str(product).upper()
    now = _now_ts()
    with _LOCK:
        cached = _ACTIVE_CONTRACTS_CACHE.get(product)
    if cached is not None and (now - cached[0] < _ACTIVE_CONTRACTS_TTL_SECONDS):
        return list(cached[1])

    base = discover_default_live_contract_months(asof)
    discovered: List[str] = [ym for ym in base if _expiry_not_passed(ym, asof)]
    if not discovered:
        discovered = list(base)

    with _LOCK:
        _ACTIVE_CONTRACTS_CACHE[product] = (now, list(discovered))
    return discovered


def get_index_weights(index_code: str, asof: date) -> pd.DataFrame:
    end = asof.strftime("%Y%m%d")
    start = (asof - timedelta(days=365)).strftime("%Y%m%d")
    try:
        return _get_provider().index_weights(index_code=index_code, start_date=start, end_date=end)
    except Exception:
        return pd.DataFrame()


def get_realtime_dv_ttm(asof: date) -> pd.DataFrame:
    try:
        return _get_provider().daily_basic_dv_ttm(trade_date=asof.strftime("%Y%m%d"))
    except Exception:
        try:
            provider = _get_provider()
            latest = provider.latest_trade_date(exchange="SSE")
            return provider.daily_basic_dv_ttm(trade_date=latest)
        except Exception:
            return pd.DataFrame()


def get_realtime_health() -> Dict[str, str]:
    """
    Probe all required realtime endpoints and return a status dict.
    Cached for _HEALTH_TTL_SECONDS to avoid hammering the API on every render.
    """
    token = _resolve_token()
    key = token or "__empty__"
    now = _now_ts()
    with _LOCK:
        cached = _HEALTH_CACHE.get(key)
    if cached is not None and (now - cached[0] < _HEALTH_TTL_SECONDS):
        return dict(cached[1])

    result: Dict[str, str] = {
        "token_loaded": "yes" if bool(token) else "no",
        "rt_idx_min": "unknown",
        "fut_mapping": "unknown",
        "rt_fut_min": "unknown",
        "note": "",
    }

    if not token:
        result["note"] = "No token in TUSHARE_RT_TOKEN/TUSHARE_TOKEN/TS_TOKEN."
        with _LOCK:
            _HEALTH_CACHE[key] = (now, dict(result))
        return result

    pro = _get_pro()

    # Check rt_idx_min (suppress Tushare stdout prints during probe)
    if not _cb_is_open("rt_idx_min"):
        result["rt_idx_min"] = f"cb_tripped:{_cb_reason('rt_idx_min')}"
    else:
        try:
            with _quiet_tushare() as trapped:
                df = pro.rt_idx_min(ts_code="000852.SH", freq="1MIN")
            printed = trapped.getvalue()
            if "token" in printed.lower() or "不对" in printed:
                err_msg = printed.strip().splitlines()[0] if printed.strip() else "token_error"
                _cb_trip("rt_idx_min", err_msg)
                result["rt_idx_min"] = f"err:{err_msg}"
            else:
                result["rt_idx_min"] = "ok" if (df is not None and not df.empty) else "empty"
        except Exception as exc:
            result["rt_idx_min"] = f"err:{exc}"

    # Check fut_mapping -> rt_fut_min (chained, as per required flow)
    try:
        df_map = pro.fut_mapping(ts_code="IM.CFX")
        col = "mapping_ts_code" if (df_map is not None and "mapping_ts_code" in df_map.columns) else (
            "mapping_code" if (df_map is not None and "mapping_code" in df_map.columns) else None
        )
        if df_map is None or df_map.empty or col is None:
            result["fut_mapping"] = "empty"
        else:
            if "trade_date" in df_map.columns:
                df_map = df_map.sort_values("trade_date", ascending=False)
            mapping_code = str(df_map.iloc[0][col]).strip().upper()
            result["fut_mapping"] = f"ok ({mapping_code})"
            # Cache the mapping code while we have it
            with _LOCK:
                _MAIN_MAPPING_CACHE["IM.CFX"] = (now, mapping_code)
            # Now test rt_fut_min with the mapping code
            try:
                df2 = pro.rt_fut_min(ts_code=mapping_code, freq="1MIN")
                result["rt_fut_min"] = "ok" if (df2 is not None and not df2.empty) else "empty"
            except Exception as exc2:
                result["rt_fut_min"] = f"err:{exc2}"
    except Exception as exc:
        result["fut_mapping"] = f"err:{exc}"
        result["rt_fut_min"] = "skipped (mapping failed)"

    if result["fut_mapping"].startswith("err:") or result["rt_fut_min"].startswith("err:"):
        result["note"] = "Futures realtime endpoints unavailable; adapter will fallback to stale source."
    elif result["rt_idx_min"].startswith("err:"):
        result["note"] = "Index realtime endpoint unavailable."

    with _LOCK:
        _HEALTH_CACHE[key] = (now, dict(result))
    return result
