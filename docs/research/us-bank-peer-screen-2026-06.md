# US Bank Peer Screen — Quality / Value at Any Rate

> **Purpose.** Build a comparable peer set of large and regional US banks and rank them on a
> *quality-at-a-reasonable-price* basis, so we can identify candidates likely to outperform their peers.
>
> **Thesis frame (chosen):** "Quality / value at any rate" — best franchises on ROE, profitability,
> credit, and valuation, *rate-regime agnostic*. The rising-Treasury-yield angle is kept only as a
> secondary risk overlay (§6), not the ranking driver.
>
> **Data.** Fundamentals = FY2024 annual (latest full year on the feed). Valuation = close of
> **2026-06-24**. Source: Tushare US endpoints (`us_fina_indicator`, `us_daily`). This is a screening
> tool, **not investment advice**. Several inputs need verification against primary filings — see §5 and §7.

---

## 1. TL;DR — the shortlist

A peer screen is a *funnel*, not a verdict. Read it as: "these names deserve the deep-dive first."

| Bucket | Names | One-line reason |
|---|---|---|
| **Quality leaders** (earn the premium) | **JPM**, then FITB, RF, MTB, PNC | Highest ROE / ROA; JPM is the clear franchise champion but priced for it (P/B 2.6×). |
| **Value leaders** (cheap for what you get) | **ZION**, TFC, USB, RF, HBAN | Lowest P/E and highest ROE-per-unit-of-P/B; ZION screens cheapest on both. |
| **Best blend (quality × value)** | **ZION, RF, WFC, HBAN, MTB** | Score well on profitability *and* valuation simultaneously — the core watchlist. |
| **Special situations (handle separately)** | KEY, COF, FITB | One-off loss / different model / pending M&A — not apples-to-apples (§5). |
| **Removed from peer set** | CMA | Acquired by Fifth Third; delisted ~Jan 2026 (§5). |

**If you want one name per camp to start the deep-dive:**
- *Quality you overpay for:* **JPM** — best-in-class returns, but the market knows it.
- *Quality at a fair price:* **WFC** or **RF** — double-digit ROE / ~1%+ ROA at ~13× P/E and ~1.5× book.
- *Deep value:* **ZION** — cheapest P/E (10.6×) with a 12.8% ROE, but smallest and historically the most rate/AOCI-sensitive (verify before acting).

---

## 2. Methodology

**Universe (16 → 15 active).** Money-center + super-regionals (JPM, BAC, WFC, C, USB, PNC, TFC, COF)
plus regionals (RF, FITB, MTB, CFG, KEY, ZION, HBAN). CMA dropped (acquired).

**Metrics.**
- *Quality:* ROE, ROA, net margin (net income / total revenue), credit cost (loan-loss provision / revenue).
- *Value:* P/E, P/B, and **ROE ÷ P/B** — a quick "quality-for-price" ratio (how much return-on-equity you
  buy per turn of book value). Higher is better; it stops you from calling a cheap low-ROE bank "value."

**Composite.** Average percentile rank across ROE (×2), ROA, net margin, earnings yield (1/PE), and
ROE/PB (×1.5). Lower composite = better. KEY is intentionally pushed down because its FY2024 ROE is
negative from a one-off (see §5) — do not read KEY's rank literally.

**Known limitation:** P/B here is **reported book**, not tangible book. Acquisitive banks carrying goodwill
(TFC, USB, PNC, BAC) look optically cheaper on P/B than on P/TBV. Re-run on tangible book before final calls.

---

## 3. The scorecard (sorted best → worst composite)

FY2024 fundamentals · valuation as of 2026-06-24 · ranked for *quality at a reasonable price*.

| Rank | Ticker | Bank | Tier | ROE % | ROA % | Net margin % | Credit cost % | P/B | P/E | ROE/PB | Mkt cap ($B) |
|---:|---|---|:--:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | **ZION** | Zions Bancorp | R | 12.8 | 0.88 | 25.0 | 2.3 | 1.39 | 10.6 | **9.21** | 10.0 |
| 2 | **JPM** | JPMorgan | L | **17.0** | **1.46** | **32.9** | 6.0 | 2.60 | 16.0 | 6.52 | 893.5 |
| 2 | **RF** | Regions Financial | R | 10.6 | 1.20 | 26.7 | 6.9 | 1.45 | 12.2 | 7.30 | 25.2 |
| 4 | FITB | Fifth Third | R | 11.8 | 1.09 | 27.3 | 6.3 | 1.56 | 18.4 | 7.55 | 49.8 |
| 5 | WFC | Wells Fargo | L | 11.0 | 1.02 | 24.3 | 5.3 | 1.59 | 13.0 | 6.92 | 258.0 |
| 6 | HBAN | Huntington | R | 9.8 | 0.95 | 26.5 | 5.7 | 1.20 | 13.5 | 8.19 | 35.6 |
| 7 | PNC | PNC Financial | L | 10.8 | 1.05 | 27.6 | **3.7** | 1.67 | 13.9 | 6.48 | 96.3 |
| 8 | MTB | M&T Bank | R | 8.9 | **1.24** | 27.9 | 6.6 | 1.34 | 13.1 | 6.65 | 34.2 |
| 9 | TFC | Truist Financial | L | 7.6 | 0.91 | 36.5 | 14.1† | **1.05** | 12.3 | 7.21 | 62.0 |
| 10 | USB | U.S. Bancorp | L | 10.8 | 0.93 | 23.2 | 8.2 | 1.59 | 12.6 | 6.76 | 93.3 |
| 11 | COF | Capital One | L | 7.8 | 0.97 | 12.1 | 30.0‡ | 1.16 | n/a | 6.74 | 123.5 |
| 12 | BAC | Bank of America | L | 9.2 | 0.83 | 25.5 | 5.5 | 1.49 | 14.5 | 6.16 | 409.7 |
| 13 | CFG | Citizens Financial | R | 6.2 | 0.69 | 19.3 | 8.8 | 1.23 | 16.4 | 5.06 | 29.4 |
| 14 | C | Citigroup | L | 6.1 | 0.54 | 15.9 | 12.5 | **1.28** | 17.9 | 4.75 | 244.9 |
| — | KEY‡ | KeyCorp | R | −0.9 | −0.09 | −3.5 | 7.3 | 1.44 | 14.2 | n/m | 25.1 |

`†` TFC credit-cost ratio is inflated by a depressed 2024 revenue base (post-2023 restructuring). `‡` See §5.

---

## 4. How to read the ranking

- **JPM is the quality benchmark, not a value play.** 17% ROE, 1.46% ROA, 33% net margin — top of every
  profitability column. You pay for it: 2.6× book and 16× earnings, the richest multiples in the group.
  It outperforms peers *operationally*; whether the *stock* outperforms depends on whether that premium can expand.
- **The "blend" names (ZION, RF, WFC, HBAN, MTB)** are where quality and price overlap. Each pairs a
  ~10–13% ROE / ~1%+ ROA with a low-teens-or-better P/E and ~1.2–1.6× book. This is the literal answer to
  "quality at a reasonable price."
- **ZION screens #1 but earns an asterisk.** Cheapest P/E (10.6×) and best ROE/PB, real 12.8% ROE. But it
  is the *smallest* ($10B cap), and Zions historically carries above-average securities/AOCI and CRE
  sensitivity. The cheap multiple may be the market pricing that risk, not a free lunch. Verify §6/§7 first.
- **Laggards (C, CFG) are cheap for a reason** — single-digit ROE and sub-0.7% ROA. Citi is a structural
  turnaround/re-rating story (cheap P/B 1.3×, but you're betting on management hitting return targets), not
  a quality compounder. Don't confuse "low P/B" with "value" when ROE doesn't support it.
- **PNC and MTB** stand out on *credit discipline* (lowest provision/revenue among the spread lenders) and
  best ROA (MTB 1.24%) — quality that the composite slightly under-rewards because their multiples are fair.

---

## 5. Data caveats & exclusions (read before trusting any single row)

- **CMA (Comerica) — removed.** Price feed stops 2026-01-30; consistent with the **Fifth Third → Comerica
  acquisition** closing in Q1 2026. No longer an independent peer; its franchise now sits inside FITB.
- **KEY (KeyCorp) — FY2024 not representative.** Reported a net **loss** (ROE −0.9%) driven by a one-off
  securities-repositioning/AOCI charge, not operating distress. Its *normalized* run-rate ROE is positive
  (mid-to-high single digits). Re-screen KEY on a clean trailing-twelve-month or forward basis before judging.
- **COF (Capital One) — not apples-to-apples.** A **credit-card-centric** lender, so a ~30% provision/revenue
  ratio is *structural*, not a sign of stress. Its loan/deposit ratios from the feed look corrupted
  (implausibly low) and P/E returned null. It also closed the **Discover acquisition (2025)**, which
  reshapes the balance sheet. Treat COF separately from traditional spread banks.
- **TFC (Truist)** — the 562% net-income YoY and 36.5% net margin are optics off a 2023 base distorted by a
  goodwill impairment; the elevated credit-cost ratio reflects depressed 2024 revenue, not a credit event.
- **P/B = reported book, not tangible.** Goodwill-heavy banks (TFC, USB, PNC, BAC) are cheaper on P/B than
  on P/TBV. The single most important refinement before acting.
- **FY2024 fundamentals vs. 2026-06 prices.** There is a ~18-month gap between the financial year and the
  valuation snapshot. Refresh with FY2025 / latest TTM figures when available for a like-for-like read.

---

## 6. Secondary overlay — rate sensitivity (qualitative, verify against filings)

Not used in the ranking, but decisive if your view shifts from "any rate" toward a directional rate call.
**None of the three drivers below are in standard financial feeds — they live in 10-Q narrative disclosures.**
Treat this section as a hypothesis checklist, not data (author knowledge cutoff Jan 2026):

- **Asset sensitivity (NII per +100bp):** every bank's 10-Q has a table — "+100bp parallel shock → ±X% NII."
  Historically BAC and the large deposit-funded banks screen most *asset-sensitive*; verify current positioning.
- **Deposit beta:** how fast a bank passes rate rises to depositors. Heavy retail/low-cost-deposit franchises
  (USB, WFC, PNC) tend to have lower betas = better in a higher-for-longer world.
- **AOCI / unrealized securities losses:** the 2023 regional-bank lesson. Higher rates *help* NII but *hit*
  the bond book — same event, opposite signs on earnings vs. capital. Disproportionately matters for the
  smaller regionals (ZION, KEY, CFG). Check AOCI as a % of tangible equity for each.
- **Curve shape, not just level:** banks earn the *slope*. A steepening (un-inversion) helps spread lenders
  more than a high-but-flat curve. If your real thesis is steepening, re-rank toward the most asset-sensitive,
  cleanest-AOCI names rather than the cheapest-P/E ones.

---

## 7. Recommended next steps (to turn this screen into a decision)

1. **Refresh to latest financials.** Pull FY2025 / latest-TTM `us_fina_indicator` so fundamentals and the
   2026-06 price are on the same clock.
2. **Switch to tangible book.** Recompute P/TBV and ROTCE — the metrics bank investors actually underwrite.
3. **Deep-dive the blend shortlist (ZION, RF, WFC, HBAN, MTB)** plus the quality anchor (JPM):
   read each 10-Q's interest-rate-sensitivity table, AOCI / tangible-equity ratio, NIM trend, deposit beta,
   and CRE concentration (regionals).
4. **Add price momentum / relative strength** (1Y and 6M total return vs. the KRE / KBW index) — quality+value
   that is *already working* is a stronger signal than quality+value that the market keeps ignoring.
5. **Normalize the special situations** (KEY ex-charge, COF as a card lender, FITB pro-forma for Comerica)
   before including or excluding them from the final basket.

---

*Generated as a screening aid. Not investment advice. Verify all figures against primary filings (SEC EDGAR
10-K/10-Q, FDIC call reports) before acting. 中国境内用户如涉及境外投资,请注意合规与风险揭示。*
