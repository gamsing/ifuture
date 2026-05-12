# Index Futures Pricing (IH / IF / IC / IM)

This folder contains a small reusable pricing module extracted from your notebooks.

## What it does

- Fetches spot index close `S` and futures close `F` via Tushare
- Builds `r` from SHIBOR (linear interpolation to maturity in days)
- Estimates dividend yield `q` via:
  - `index` mode: `index_dailybasic` dividend yield (fast, if available)
  - `constituent` mode: constituent-weighted `dv_ttm` (bottom-up, slower)
- Computes cost-of-carry fair value: `FV = S * exp((r - q) * T)`
- Reports deviation `(F - FV) / FV` and a simple signal vs a threshold

## Quick usage

CLI (prints a compact table):

```bash
python3 -m index_pricing.cli --contract 2609 --products IH,IF,IM --dividend constituent
```

Script (prints a full dataframe, optional Excel export):

```bash
python3 price_indices.py --contract 2609 --products IH,IF,IM --out ih_if_im_2609.xlsx
```

## Token setup

Tushare needs a token. Either:

- Set `TUSHARE_TOKEN` in your environment, or
- Set `TS_TOKEN` in your environment.
