# US Bank Peer Screen — Quality / Value at Any Rate

> **Purpose.** Build a comparable peer set of large and regional US banks and rank them on a
> *quality-at-a-reasonable-price* basis, so we can identify candidates likely to outperform their peers.
>
> **Thesis frame (chosen):** "Quality / value at any rate" — best franchises on ROE, profitability,
> credit, and valuation, *rate-regime agnostic*. The rising-Treasury-yield angle is kept only as a
> secondary risk overlay (§6), not the ranking driver.
>
> **Data — current as of 2026-06-25.** Fundamentals = **FY2025 annual** (latest full year, reported
> Feb 2026). Valuation (P/E, P/B, market cap) = close of **2026-06-24**. Source: Tushare US endpoints
> (`us_fina_indicator`, `us_daily`). Fundamentals and prices are now on the same clock. This is a
> screening tool, **not investment advice**. Several inputs need verification against primary filings — see §5 and §7.

---

## 1. TL;DR — the shortlist

A peer screen is a *funnel*, not a verdict. Read it as: "these names deserve the deep-dive first."

| Bucket | Names | One-line reason |
|---|---|---|
| **Quality leaders** (earn the premium) | **JPM**, then RF, FITB, USB, WFC, PNC | Highest ROE / ROA; JPM is the clear franchise champion but priced for it (P/B 2.6×). |
| **Value leaders** (cheap for what you get) | **ZION**, USB, TFC, RF, WFC | Lowest P/E and highest ROE-per-unit-of-P/B; ZION screens cheapest on both. |
| **Best blend (quality × value)** | **ZION, RF, USB, WFC, MTB** | Score well on profitability *and* valuation simultaneously — the core watchlist. |
| **Special situation (handle separately)** | COF | FY2025 ROE crushed to 2.2% by the Discover day-2 reserve build (§5). |
| **Removed from peer set** | CMA | Acquired by Fifth Third; delisted ~Jan 2026 (§5). |

**If you want one name per camp to start the deep-dive:**
- *Quality you overpay for:* **JPM** — best-in-class returns (15.7% ROE), but the market knows it (2.6× book).
- *Quality at a fair price:* **RF** or **USB** — ~11–12% ROE / ~1.1–1.4% ROA at ~12.5× P/E and ~1.5× book.
- *Deep value:* **ZION** — cheapest P/E (10.6×) with a 12.5% ROE, but smallest and historically the most
  rate/AOCI-sensitive (verify §6 before acting).

---

## 2. Methodology

**Universe (16 → 15 active).** Money-center + super-regionals (JPM, BAC, WFC, C, USB, PNC, TFC, COF)
plus regionals (RF, FITB, MTB, CFG, KEY, ZION, HBAN). CMA dropped (acquired).

**Metrics.**
- *Quality:* ROE, ROA, net margin (net income / total revenue), credit cost (loan-loss provision / revenue).
- *Value:* P/E, P/B, and **ROE ÷ P/B** — a quick "quality-for-price" ratio (how much return-on-equity you
  buy per turn of book value). Higher is better; it stops you from calling a cheap low-ROE bank "value."

**Composite.** Average rank across ROE (×2), ROA, net margin, earnings yield (1/PE), and ROE/PB (×1.5).
Lower composite = better.

**Known limitation:** P/B here is **reported book**, not tangible book. Acquisitive banks carrying goodwill
(TFC, USB, PNC, BAC) look optically cheaper on P/B than on P/TBV. Re-run on tangible book before final calls.

---

## 3. The scorecard (sorted best → worst composite)

FY2025 fundamentals · valuation as of 2026-06-24 · ranked for *quality at a reasonable price*.

| Rank | Ticker | Bank | Tier | ROE % | ROA % | Net margin % | Credit cost % | P/B | P/E | ROE/PB | Mkt cap ($B) |
|---:|---|---|:--:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | **ZION** | Zions Bancorp | R | 12.5 | 1.01 | 26.6 | **2.1** | 1.39 | **10.6** | **9.01** | 10.0 |
| 2 | **RF** | Regions Financial | R | 11.3 | **1.36** | 28.6 | 6.2 | 1.45 | 12.2 | 7.81 | 25.2 |
| 3 | **JPM** | JPMorgan | L | **15.7** | 1.29 | **31.3** | 7.8 | 2.60 | 16.0 | 6.05 | 893.5 |
| 4 | USB | U.S. Bancorp | L | 11.6 | 1.09 | 26.6 | 7.7 | 1.59 | 12.6 | 7.30 | 93.3 |
| 5 | WFC | Wells Fargo | L | 11.8 | 0.99 | 25.5 | 4.4 | 1.59 | 13.0 | 7.41 | 258.0 |
| 6 | PNC | PNC Financial | L | 11.4 | 1.21 | 30.3 | **3.4** | 1.67 | 13.9 | 6.86 | 96.3 |
| 7 | MTB | M&T Bank | R | 9.8 | 1.34 | 29.4 | 5.2 | 1.34 | 13.1 | 7.29 | 34.2 |
| 8 | FITB | Fifth Third | R | 11.6 | 1.18 | 28.0 | 7.3 | 1.56 | 18.4 | 7.44 | 49.8 |
| 9 | HBAN | Huntington | R | 9.1 | 0.98 | 27.3 | 5.7 | **1.20** | 13.5 | 7.57 | 35.6 |
| 10 | TFC | Truist Financial | L | 8.1 | 0.97 | 26.1 | 9.3 | **1.05** | 12.3 | 7.75 | 62.0 |
| 11 | BAC | Bank of America | L | 10.1 | 0.89 | 27.0 | 5.0 | 1.49 | 14.5 | 6.75 | 409.7 |
| 12 | KEY | KeyCorp | R | 9.0 | 0.99 | 24.5 | 6.3 | 1.44 | 14.2 | 6.23 | 25.1 |
| 13 | CFG | Citizens Financial | R | 7.0 | 0.81 | 22.2 | 7.4 | 1.23 | 16.4 | 5.66 | 29.4 |
| 14 | C | Citigroup | L | 6.7 | 0.54 | 17.0 | 12.0 | **1.28** | 17.9 | 5.26 | 244.9 |
| 15 | COF‡ | Capital One | L | 2.2 | 0.37 | 4.6 | 38.7‡ | 1.16 | n/a | 1.86 | 123.5 |

`‡` COF FY2025 distorted by the Discover acquisition — see §5. Do not read its rank literally.

---

## 4. How to read the ranking

- **JPM is the quality benchmark, not a value play.** 15.7% ROE, 1.29% ROA, 31% net margin — top of the
  profitability columns. You pay for it: 2.6× book and 16× earnings, the richest multiples in the group.
  It outperforms peers *operationally*; whether the *stock* outperforms depends on that premium holding.
- **The "blend" names (ZION, RF, USB, WFC, MTB)** are where quality and price overlap. Each pairs a
  ~10–13% ROE / ~1%+ ROA with a low-teens-or-better P/E and ~1.3–1.6× book. This is the literal answer to
  "quality at a reasonable price."
- **RF is the cleanest mid-cap story this year.** Highest ROA in the group (1.36%), an 11.3% ROE, and still
  cheap at 12.2× / 1.45× book — it climbs to #2 on FY2025 numbers.
- **ZION screens #1 but earns an asterisk.** Cheapest P/E (10.6×) and best ROE/PB, real 12.5% ROE, lowest
  credit cost. But it is the *smallest* ($10B cap) and historically carries above-average securities/AOCI
  and CRE sensitivity. The cheap multiple may be the market pricing that risk, not a free lunch (see §6).
- **PNC and MTB stand out on quality of earnings** — best credit discipline (PNC 3.4% provision/revenue)
  and best regional ROA (MTB 1.34%). The composite slightly under-rewards them because their multiples are fair.
- **Laggards (C, CFG) are cheap for a reason** — single-digit ROE and (for C) sub-0.6% ROA. Citi is a
  structural turnaround/re-rating story (cheap at 1.28× book, but you're betting on management hitting return
  targets), not a quality compounder. Don't confuse "low P/B" with "value" when ROE doesn't support it.

---

## 5. Data caveats & exclusions (read before trusting any single row)

- **CMA (Comerica) — removed.** Price feed stops 2026-01-30; consistent with the **Fifth Third → Comerica
  acquisition** closing in Q1 2026. No longer an independent peer; its franchise now sits inside FITB.
- **COF (Capital One) — special situation, FY2025.** Net income fell ~48% YoY to $2.45B and ROE collapsed to
  2.2% because closing the **Discover acquisition (2025)** forced a one-time ~$20.7B "day-2" CECL reserve on
  the acquired loan book. Underlying earnings power is far higher; the headline ratios are not comparable.
  Also a **credit-card-centric** lender, so a high structural provision rate is normal, and its loan/deposit
  ratios from the feed look corrupted. Screen COF separately, on a normalized basis.
- **KEY (KeyCorp) — now normalized.** FY2024 was a one-off net *loss* (securities-repositioning/AOCI charge);
  FY2025 ROE has recovered to a clean **9.0%**, so KEY is ranked as a normal regional here (no asterisk).
- **YoY optics to ignore:** KEY's +1236% and TFC's +53% revenue growth are recoveries off depressed 2024
  bases (KEY's charge; Truist's 2023 restructuring), not organic surges. The *level* ratios are what matter.
- **P/B = reported book, not tangible.** Goodwill-heavy banks (TFC, USB, PNC, BAC) are cheaper on P/B than
  on P/TBV. The single most important refinement before acting.

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

1. **Switch to tangible book.** Recompute P/TBV and ROTCE — the metrics bank investors actually underwrite.
2. **Deep-dive the blend shortlist (ZION, RF, USB, WFC, MTB)** plus the quality anchor (JPM):
   read each 10-Q's interest-rate-sensitivity table, AOCI / tangible-equity ratio, NIM trend, deposit beta,
   and CRE concentration (regionals).
3. **Add price momentum / relative strength** (1Y and 6M total return vs. the KRE / KBW index) — quality+value
   that is *already working* is a stronger signal than quality+value the market keeps ignoring.
4. **Layer in Q1-2026** results (already on the feed) to confirm the FY2025 trend is intact, not rolling over.
5. **Normalize the special situation** (COF ex-Discover-reserve) before including or excluding it from the basket.

---

*Generated as a screening aid. Not investment advice. Verify all figures against primary filings (SEC EDGAR
10-K/10-Q, FDIC call reports) before acting. 中国境内用户如涉及境外投资,请注意合规与风险揭示。*
