from __future__ import annotations

import argparse

from index_pricing.engine import BatchRunner, EngineConfig, PricingEngine, products_from_csv


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Batch price IH/IF/IC/IM and optionally export to Excel.")
    ap.add_argument("--contracts", "--contract", dest="contracts", required=True, help="Comma-separated YYMM, e.g. 2603,2604,2606,2609")
    ap.add_argument("--asof", default="latest", help="YYYYMMDD or 'latest'")
    ap.add_argument("--products", default="IH,IF,IM", help="Comma-separated, default IH,IF,IM")
    ap.add_argument("--dividend", default="constituent", help="Dividend model: 'constituent' or 'index'")
    ap.add_argument("--threshold", type=float, default=0.005, help="Deviation threshold (decimal)")
    ap.add_argument("--fallback-q", type=float, default=0.02, help="Fallback dividend yield (decimal)")
    ap.add_argument("--out", default="", help="Excel output path (optional)")
    args = ap.parse_args(argv)

    cfg = EngineConfig(threshold=args.threshold, fallback_q=args.fallback_q)
    engine = PricingEngine(cfg=cfg, dividend_mode=args.dividend)
    runner = BatchRunner(engine)
    products = products_from_csv(args.products)
    contracts = [c.strip() for c in str(args.contracts).split(",") if c.strip()]
    tasks = {p: contracts for p in products}
    df = runner.run(tasks, asof=args.asof)
    print(df.to_string(index=False))
    if args.out:
        df.to_excel(args.out, index=False)
        print(f"\nExported: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
