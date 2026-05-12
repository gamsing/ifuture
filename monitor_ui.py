from __future__ import annotations

import importlib
import math
import os
import time
from datetime import date, datetime
from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st

from index_pricing.engine import (
    INDEX_REGISTRY,
    EngineConfig,
    LiveMonitor,
    PricingEngine,
    discover_default_live_contract_months,
)
from index_pricing.local_store import (
    LocalDailyDividendProvider,
    LocalDailyRateProvider,
    LocalMarketStore,
    LocalStoreConfig,
)
from index_pricing.providers import (
    ConstituentWeightedDvProvider,
    RealTimeProvider,
    TushareConfig,
    TushareProvider,
)

try:
    from streamlit_autorefresh import st_autorefresh  # type: ignore
except Exception:  # noqa: BLE001
    st_autorefresh = None


def _load_realtime_adapter(module_name: str):
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        return None


def _has_tushare_token(token_override: str = "") -> bool:
    return bool(
        token_override.strip()
        or os.environ.get("TUSHARE_RT_TOKEN")
        or os.environ.get("TUSHARE_TOKEN")
        or os.environ.get("TS_TOKEN")
    )


def _demo_spot_last(spot_code: str) -> float:
    demo_spots = {
        "000016.SH": 2860.0,
        "000300.SH": 4025.0,
        "000905.SH": 6120.0,
        "000852.SH": 6280.0,
    }
    return demo_spots.get(str(spot_code).strip().upper(), 4000.0)


def _demo_fut_last(fut_code: str) -> float:
    code = str(fut_code).strip().upper()
    product = code[:2]
    ym = code[2:6]
    index = INDEX_REGISTRY.get(product)
    if index is None:
        return 4000.0

    spot = _demo_spot_last(index.spot_code)
    default_months = discover_default_live_contract_months(date.today())
    try:
        month_rank = default_months.index(ym)
    except ValueError:
        month_rank = 0

    demo_basis_by_product = {
        "IH": 0.006,
        "IF": -0.012,
        "IC": -0.032,
        "IM": -0.045,
    }
    basis_rate = demo_basis_by_product.get(product, -0.01) - month_rank * 0.004
    return spot * (1.0 + basis_rate)


@st.cache_resource(show_spinner=False)
def _get_tushare_provider(cache_dir: str, token_override: str) -> TushareProvider:
    token = token_override.strip() if token_override else None
    return TushareProvider(TushareConfig(token=token, cache_dir=Path(cache_dir)))


@st.cache_resource(show_spinner=False)
def _get_local_store(db_path: str) -> LocalMarketStore:
    return LocalMarketStore(LocalStoreConfig(db_path=Path(db_path)))


def _refresh_daily_factors_if_due(
    store: LocalMarketStore,
    ts_provider: TushareProvider,
    products: list[str],
    fallback_q: float,
) -> tuple[int, str]:
    """
    Refreshes q + SHIBOR once factors are due.
    Priority:
    - after 17:00 local time: try today's date first
    - always ensure latest completed trading day exists
    """
    now = datetime.now()
    q_provider = ConstituentWeightedDvProvider(provider=ts_provider, fallback_q=fallback_q)

    target_dates: list[str] = []
    if now.hour >= 17:
        target_dates.append(now.strftime("%Y%m%d"))
    latest_trade_date = ts_provider.latest_trade_date(exchange="SSE")
    if latest_trade_date not in target_dates:
        target_dates.append(latest_trade_date)

    updates = 0
    msg = "up-to-date"
    for trade_date in target_dates:
        try:
            asof_dt = datetime.strptime(trade_date, "%Y%m%d").date()
        except ValueError:
            continue
        try:
            shibor_nodes = ts_provider.shibor_nodes(trade_date)
        except Exception:
            continue

        for product in products:
            if store.has_daily_factor(trade_date, product):
                continue
            index = INDEX_REGISTRY[product]
            try:
                q = q_provider.get_dividend_yield(asof_dt, index, asof_dt)
            except Exception:
                q = fallback_q
            store.upsert_daily_factor(
                trade_date=trade_date,
                product=product,
                q=float(q),
                shibor_nodes=shibor_nodes,
                source="daily_after_1700",
            )
            updates += 1
            msg = f"refreshed for {trade_date}"
    return updates, msg


def _build_monitor(
    threshold: float,
    fallback_q: float,
    products: list[str],
    adapter_module_name: str,
    ts_provider: TushareProvider,
    store: LocalMarketStore,
) -> tuple[LiveMonitor, bool, str]:
    cfg = EngineConfig(threshold=threshold, fallback_q=fallback_q, cache_dir=Path(".index_pricing_cache"))
    if not _has_tushare_token():
        market_provider = RealTimeProvider(
            spot_last_fetcher=_demo_spot_last,
            fut_last_fetcher=_demo_fut_last,
            rate_fetcher=None,
            active_contracts_fetcher=lambda _product, asof: discover_default_live_contract_months(asof),
            fallback_rate=0.015,
        )
        rate_provider = LocalDailyRateProvider(store=store, fallback_rate=0.015)
        dividend_provider = LocalDailyDividendProvider(store=store, fallback_q=fallback_q)
        engine = PricingEngine(
            market_data=market_provider,
            rate_data=rate_provider,
            dy_provider=dividend_provider,
            cfg=cfg,
        )
        return LiveMonitor(engine=engine, products=products), False, "Demo Mode (synthetic quotes)"

    adapter = _load_realtime_adapter(adapter_module_name)
    source_name = "Tushare EOD"
    realtime_enabled = False

    if adapter is not None and callable(getattr(adapter, "get_spot_last", None)) and callable(
        getattr(adapter, "get_fut_last", None)
    ):
        source_name = f"Realtime Adapter: {adapter_module_name}"
        realtime_enabled = True
        market_provider = RealTimeProvider(
            spot_last_fetcher=getattr(adapter, "get_spot_last"),
            fut_last_fetcher=getattr(adapter, "get_fut_last"),
            rate_fetcher=None,
            active_contracts_fetcher=getattr(adapter, "get_active_contract_months", None),
            fallback_rate=0.015,
        )
        rate_provider = LocalDailyRateProvider(store=store, fallback_rate=0.015)
        dividend_provider = LocalDailyDividendProvider(store=store, fallback_q=fallback_q)
        engine = PricingEngine(
            market_data=market_provider,
            rate_data=rate_provider,
            dy_provider=dividend_provider,
            cfg=cfg,
        )
        return LiveMonitor(engine=engine, products=products), realtime_enabled, source_name

    # Fallback mode keeps historical behavior if realtime adapter is unavailable.
    engine = PricingEngine(cfg=cfg, tushare_provider=ts_provider, dividend_mode="constituent")
    return LiveMonitor(engine=engine, products=products), realtime_enabled, source_name


def _deviation_style(v):
    if pd.isna(v):
        return ""
    x = float(v)
    if x >= 0.5:
        return "background-color: rgba(200,0,0,0.30)"
    if x <= -0.5:
        return "background-color: rgba(0,120,0,0.30)"
    return "background-color: rgba(150,150,150,0.12)"


def _persist_minute_quotes(store: LocalMarketStore, df: pd.DataFrame) -> None:
    if df.empty or "AsOf" not in df.columns:
        return
    asof_value = str(df["AsOf"].dropna().iloc[0]) if not df["AsOf"].dropna().empty else ""
    if not asof_value:
        return
    try:
        asof_dt = datetime.strptime(asof_value, "%Y-%m-%d").date()
    except ValueError:
        return

    rows = []
    for _, row in df.iterrows():
        prod = str(row.get("Product", ""))
        ctt = str(row.get("Contract", ""))
        if prod not in INDEX_REGISTRY or not ctt:
            continue
        spot_code = INDEX_REGISTRY[prod].spot_code
        rows.append(
            {
                "Product": prod,
                "Contract": ctt,
                "SpotCode": spot_code,
                "FutCode": f"{prod}{ctt}.CFX",
                "Spot": row.get("Spot"),
                "Futures": row.get("Futures"),
            }
        )
    store.upsert_minute_quotes(asof_date=asof_dt, rows=rows)


def main() -> None:
    st.set_page_config(page_title="CFFEX Real-Time Basis Monitor", layout="wide")
    st.title("CFFEX Index Futures Monitor")

    st.sidebar.header("Settings")
    products = st.sidebar.multiselect(
        "Products",
        options=list(INDEX_REGISTRY.keys()),
        default=list(INDEX_REGISTRY.keys()),
    )
    threshold = st.sidebar.number_input("Deviation Threshold", value=0.005, step=0.001, format="%.4f")
    fallback_q = st.sidebar.number_input("Fallback q", value=0.02, step=0.001, format="%.4f")
    refresh_sec = int(st.sidebar.slider("Refresh (seconds)", min_value=2, max_value=30, value=5))
    adapter_module = st.sidebar.text_input(
        "Realtime adapter module",
        value=os.environ.get("REALTIME_ADAPTER_MODULE", "realtime_adapter"),
    )
    rt_token_input = st.sidebar.text_input(
        "Realtime Token (optional override)",
        value=os.environ.get("TUSHARE_RT_TOKEN", ""),
        type="password",
        help="If provided, monitor uses this token for rt_idx_min/rt_fut_min/fut_mapping checks.",
    )
    db_path = st.sidebar.text_input("Local DB Path", value=".index_pricing_local/market_cache.db")

    if rt_token_input.strip():
        os.environ["TUSHARE_RT_TOKEN"] = rt_token_input.strip()

    has_token = _has_tushare_token(rt_token_input)
    if not has_token:
        st.info("演示模式 · 未检测到 Tushare token, 当前使用合成行情用于界面预览。")

    if st_autorefresh is not None:
        st_autorefresh(interval=refresh_sec * 1000, key="refresh_timer")
    else:
        st.sidebar.info("Install streamlit-autorefresh for auto-refresh. Use manual refresh otherwise.")
        st.sidebar.button("Refresh now")

    ts_provider = _get_tushare_provider(".index_pricing_cache", rt_token_input)
    store = _get_local_store(db_path)

    # Refresh q + SHIBOR at most once every 10 minutes per app session.
    now_ts = time.time()
    last_factor_sync = float(st.session_state.get("last_factor_sync_ts", 0.0))
    if has_token and now_ts - last_factor_sync > 600:
        with st.spinner("Refreshing daily q/SHIBOR cache if due..."):
            updates, sync_msg = _refresh_daily_factors_if_due(
                store=store,
                ts_provider=ts_provider,
                products=products,
                fallback_q=fallback_q,
            )
        st.session_state.last_factor_sync_ts = now_ts
        st.caption(f"Daily factor sync: {sync_msg} (updates={updates})")
    elif not has_token:
        st.caption("Daily factor sync: skipped in demo mode")

    monitor, realtime_enabled, source_name = _build_monitor(
        threshold=threshold,
        fallback_q=fallback_q,
        products=products,
        adapter_module_name=adapter_module,
        ts_provider=ts_provider,
        store=store,
    )
    asof = "today" if realtime_enabled else "latest"
    st.caption(f"Data Source: {source_name} | AsOf Mode: {asof}")
    adapter_for_health = _load_realtime_adapter(adapter_module)
    if adapter_for_health is not None and callable(getattr(adapter_for_health, "get_realtime_health", None)):
        health = adapter_for_health.get_realtime_health()
        st.caption(
            "RT Health | "
            f"token={health.get('token_loaded')} | "
            f"rt_idx_min={health.get('rt_idx_min')} | "
            f"fut_mapping={health.get('fut_mapping')} | "
            f"rt_fut_min={health.get('rt_fut_min')}"
        )
        note = str(health.get("note", "")).strip()
        if note:
            st.warning(note)

    if "last_snapshot_df" not in st.session_state:
        st.session_state.last_snapshot_df = pd.DataFrame()
    if "last_snapshot_time" not in st.session_state:
        st.session_state.last_snapshot_time = ""

    status_placeholder = st.empty()
    with status_placeholder.container():
        st.info("Fetching latest snapshot...")

    df = pd.DataFrame()
    fetch_error: Optional[str] = None
    try:
        with st.spinner("Loading minute prices and pricing all contracts..."):
            df = monitor.run_snapshot(asof=asof)
    except Exception as exc:  # noqa: BLE001
        fetch_error = str(exc)

    status_placeholder.empty()

    if fetch_error:
        st.warning(f"Live refresh failed: {fetch_error}")

    if not df.empty:
        _persist_minute_quotes(store, df)

        # ── Annotate rows with quote source (RT / STALE) + timestamp ─────
        if realtime_enabled and adapter_for_health is not None and callable(
            getattr(adapter_for_health, "get_last_quote_meta", None)
        ):
            sources, qtimes = [], []
            for _, row in df.iterrows():
                prod = str(row.get("Product", ""))
                ym = str(row.get("Contract", ""))
                fut_code = f"{prod}{ym}.CFX"
                meta = adapter_for_health.get_last_quote_meta(fut_code, "FT")
                src = meta.get("source", "unknown")
                age = meta.get("age_seconds")
                label = f"{src} ({age:.0f}s)" if age is not None else src
                sources.append(label)
                qtimes.append(meta.get("quote_time", ""))
            df["DataSource"] = sources
            df["QuoteTime"] = qtimes
        else:
            df["DataSource"] = "N/A"
            df["QuoteTime"] = ""

        st.session_state.last_snapshot_df = df.copy()
        st.session_state.last_snapshot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elif not st.session_state.last_snapshot_df.empty:
        df = st.session_state.last_snapshot_df.copy()
        st.info(f"Showing last successful snapshot from {st.session_state.last_snapshot_time}")
    else:
        st.warning("No rows returned yet.")
        return

    # ── Data source summary badges ────────────────────────────────────────
    if "DataSource" in df.columns:
        rt_mask = df["DataSource"].str.startswith("RT")
        stale_mask = df["DataSource"].str.startswith("STALE")
        mb1, mb2, mb3 = st.columns(3)
        mb1.metric("Realtime rows", int(rt_mask.sum()))
        mb2.metric("Stale rows", int(stale_mask.sum()))
        mb3.metric("Last refresh", st.session_state.get("last_snapshot_time", "—"))

    top = df[df["Deviation(%)"].notna()].head(1)
    if not top.empty:
        row = top.iloc[0]
        st.metric("Top |Deviation|", f"{abs(float(row['Deviation(%)'])):.3f}%", f"{row['Product']}{row['Contract']}")

    if "Error" in df.columns and df["Error"].notna().any():
        st.error("Some rows failed to price. Scroll table for details.")

    show = df.copy()
    show["ArbSignal"] = show["Signal"].map({1: "Long Basis", -1: "Short Basis", 0: "Neutral"})
    cols = [
        "AsOf",
        "Product",
        "Contract",
        "DataSource",
        "Spot",
        "Futures",
        "Basis",
        "FV",
        "Deviation(%)",
        "ArbSignal",
        "r",
        "q",
        "Days_To_Expiry",
        "QuoteTime",
    ]
    if "Error" in show.columns:
        cols.append("Error")
    # Guard: only keep cols that actually exist
    show = show[[c for c in cols if c in show.columns]]

    fmt = {}
    for col, fmt_str in [
        ("Spot", "{:.2f}"), ("Futures", "{:.2f}"), ("Basis", "{:.2f}"),
        ("FV", "{:.2f}"), ("Deviation(%)", "{:.3f}"), ("r", "{:.4f}"), ("q", "{:.4f}"),
    ]:
        if col in show.columns:
            fmt[col] = fmt_str

    try:
        dev_subset = ["Deviation(%)"] if "Deviation(%)" in show.columns else []
        styler = show.style
        if dev_subset:
            styler = styler.map(_deviation_style, subset=dev_subset)
        styled = styler.format(fmt, na_rep="—")
        st.dataframe(styled, width="stretch", height=560)
    except AttributeError:
        st.dataframe(show, width="stretch", height=560)

    heat = df.pivot(index="Product", columns="Contract", values="Deviation(%)")
    if not heat.empty:
        st.subheader("Deviation Heatmap (%)")
        try:
            heat_view = heat.style.background_gradient(cmap="RdYlGn_r", axis=None).format("{:.3f}", na_rep="—")
        except AttributeError:
            heat_view = heat
        st.dataframe(heat_view, width="stretch")

    # ── Intraday Deviation Trend Chart ───────────────────────────────────────
    if realtime_enabled and adapter_for_health is not None and callable(
        getattr(adapter_for_health, "get_intraday_minute_bars", None)
    ):
        st.subheader("Intraday Deviation Trend")

        # Build contract option list from current snapshot
        contract_options: list[str] = []
        for _, snap_row in df.iterrows():
            if pd.notna(snap_row.get("Product")) and pd.notna(snap_row.get("Contract")):
                contract_options.append(f"{snap_row['Product']}{snap_row['Contract']}")

        selected_contract = st.selectbox(
            "Select a contract to view today's intraday deviation chart",
            options=["— select —"] + contract_options,
            key="intraday_contract_select",
        )

        if selected_contract and selected_contract != "— select —":
            # Parse product and year_month from selection (e.g. "IM2609")
            sel_product = selected_contract[:2]
            sel_ym = selected_contract[2:]
            fut_code = f"{selected_contract}.CFX"

            match_rows = df[(df["Product"] == sel_product) & (df["Contract"] == sel_ym)]
            if match_rows.empty:
                st.warning(f"No snapshot row found for {selected_contract}.")
            else:
                snap = match_rows.iloc[0]
                S = float(snap["Spot"]) if pd.notna(snap.get("Spot")) else None
                r = float(snap["r"]) if pd.notna(snap.get("r")) else 0.015
                q = float(snap["q"]) if pd.notna(snap.get("q")) else 0.02
                days_to_exp = float(snap["Days_To_Expiry"]) if pd.notna(snap.get("Days_To_Expiry")) else 1.0
                T = max(days_to_exp, 0.0) / 365.0

                if S is None or S <= 0:
                    st.warning("Cannot compute intraday deviation: spot price unavailable.")
                else:
                    with st.spinner(f"Loading intraday minute bars for {fut_code}…"):
                        bars = adapter_for_health.get_intraday_minute_bars(fut_code)

                    if bars.empty or "close" not in bars.columns:
                        st.info(f"No intraday minute data available for {fut_code} today.")
                    else:
                        FV = S * math.exp((r - q) * T)
                        bars = bars.copy()
                        bars["Deviation(%)"] = (bars["close"].astype(float) - FV) / FV * 100.0

                        time_col = "trade_time" if "trade_time" in bars.columns else None
                        if time_col:
                            bars = bars.set_index(time_col)

                        st.caption(
                            f"{fut_code} | Spot={S:.2f}  FV={FV:.2f}  r={r:.4f}  q={q:.4f}  T={days_to_exp:.0f}d"
                        )
                        st.line_chart(bars["Deviation(%)"], width="stretch")

                        # Summary stats
                        dev_series = bars["Deviation(%)"].dropna()
                        if not dev_series.empty:
                            col1, col2, col3, col4 = st.columns(4)
                            col1.metric("Current", f"{dev_series.iloc[-1]:.3f}%")
                            col2.metric("Max", f"{dev_series.max():.3f}%")
                            col3.metric("Min", f"{dev_series.min():.3f}%")
                            col4.metric("Bars", str(len(dev_series)))


if __name__ == "__main__":
    main()
