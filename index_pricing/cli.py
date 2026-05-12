from __future__ import annotations

import argparse

import pandas as pd

from .engine import BatchRunner, EngineConfig, INDEX_REGISTRY, PricingEngine, products_from_csv


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Batch price CFFEX index futures (IH/IF/IC/IM) via cost-of-carry.")
    ap.add_argument("--contracts", "--contract", dest="contracts", required=True, help="Comma-separated YYMM, e.g. 2603,2604,2606,2609")
    ap.add_argument("--asof", default="latest", help="YYYYMMDD or 'latest'")
    ap.add_argument("--products", default="IH,IF,IC,IM", help="Comma-separated: IH,IF,IC,IM")
    ap.add_argument("--dividend", default="constituent", help="Dividend model: 'constituent' or 'index'")
    ap.add_argument("--threshold", type=float, default=0.005, help="Deviation threshold (e.g. 0.005 = 50bp)")
    ap.add_argument("--fallback-q", type=float, default=0.02, help="Fallback dividend yield if data missing (decimal)")
    ap.add_argument("--sort", default="", help="Optional sort: 'absdev' or 'dev'")
    args = ap.parse_args(argv)

    cfg = EngineConfig(threshold=args.threshold, fallback_q=args.fallback_q)
    engine = PricingEngine(cfg=cfg, dividend_mode=args.dividend)
    runner = BatchRunner(engine)

    products = products_from_csv(args.products)
    contracts = [c.strip() for c in str(args.contracts).split(",") if c.strip()]
    tasks = {p: contracts for p in products}
    df = runner.run(tasks, asof=args.asof)

    if str(args.sort).strip().lower() == "absdev":
        df = df.assign(**{"AbsDeviation(%)": df["Deviation(%)"].abs()}).sort_values("AbsDeviation(%)", ascending=False)
    elif str(args.sort).strip().lower() == "dev":
        df = df.sort_values("Deviation(%)", ascending=False)

    with pd.option_context("display.max_columns", None, "display.width", 200):
        print(df.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
