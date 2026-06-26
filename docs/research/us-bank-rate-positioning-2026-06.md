# US Bank Rate-Positioning Study — Who Outperforms on the Rate Thesis

> **Thesis.** US Treasury yields higher-for-longer, curve dis-inverting. Banks that win are
> **asset-sensitive** (NII rises with rates), with **low deposit beta**, **clean AOCI / small HTM holes**,
> and **manageable CRE** — the dual-edged risks that blew up the 2023 regionals. This study ranks 15 large +
> regional US banks on that framework, not on generic quality/value.
>
> **As of 2026-06-25.** Structured layer = Tushare (Q1-2026 balance sheet `20260331` + FY2025 indicators +
> 2026-06-24 valuation). Filing layer = SEC 10-Q/10-K + Q1-2026 earnings calls.
>
> **⚠️ Source-confidence caveat (updated 2026-06-26).** The **5 priority banks (BAC, ZION, USB, KEY, WFC)** have
> now been **finalized from the primary Q1-2026 10-Q** — asset-sensitivity/EVE tables, HTM/AFS gross unrealized
> losses, and average deposit cost are read directly from SEC EDGAR (see **§2.1**); those cells are marked **✓**
> and are high-confidence. (The original session's HTTP 403s were a missing-User-Agent egress quirk, not a real
> block; direct EDGAR fetch works.) The **remaining 10 names'** filing-layer figures (asset-sensitivity, HTM/AFS
> marks, CET1, CRE, NII guidance) are **still web-sourced** — single-source, verify against the 10-Q before
> trading. The structured layer (AOCI, AFS/HTM balances, TCE, P/TBV, ROA) is computed directly from the Tushare
> feed and is high-confidence. Per-field confidence is flagged throughout. Not investment advice.

---

## 1. Macro backdrop — the curve (your framework item ③)

Treasury par yields, 2026-06-25 (Tushare `us_tycr`):

| 3M | 2Y | 5Y | 10Y | 30Y | **2s10s** | **3M-10Y** |
|---:|---:|---:|---:|---:|---:|---:|
| 3.84 | 4.09 | 4.15 | 4.40 | 4.86 | **+31 bp** | **+56 bp** |

**The curve is positively sloped again — dis-inverted, modestly steepening.** This is the constructive regime
for spread lenders: banks earn the slope, and the 2022–24 inversion that compressed NIMs has unwound. A
steepening bias *favors asset-sensitive, clean-AOCI names* over the cheapest-multiple names — so rate
positioning, not just valuation, should drive selection here.

---

## 2. The rate-positioning scorecard (all 15)

Sorted by rate-positioning tier. **Sens** = asset (A) / neutral (N) / liability (L) sensitive.
**AOCI/TCE** and **P/TBV** are hard structured figures. Cells marked **✓** are now read directly from the
bank's **Q1-2026 10-Q** (primary source — full figures, incl. EVE and AFS losses, in **§2.1**); unmarked
filing cells remain web-sourced pending the same treatment.

| Ticker | Sens | ΔNII +100bp | AOCI/TCE | HTM unrl. loss | CET1 | CRE % (office) | NIM | NCO % | FY26 NII guide (Δ) | P/TBV | ROA |
|---|:--:|---|---:|---|---:|---|---:|---:|---|---:|---:|
| **BAC** | **A** (asym) | +$0.4B ✓ | −5.3% | **$81.2B** ✓ | 11.2 | 5.7% (low) | 2.07↑ | 0.48 | +6–8% **RAISED** | 1.98 | 0.89 |
| **USB** | **A** (mod) | +200bp:+0.48% ✓ | −15.6% | **$9.4B** ✓ | 10.8 | n/f | 2.77 | 0.56 | +6–7% maintained | 2.01 | 1.09 |
| **KEY** | N→A | +200bp:+0.38% ✓ | −15.1% | **$0.4B** ✓ (bal $8.7B) | 11.4* | n/f | 2.87↑ | 0.38 | +9–10% **RAISED** | 1.70 | 0.99 |
| **ZION** | **A** (high) | **+3.7%** ✓ | **−31.5%** | **$0.07B** △ ✓ | 11.5 | **22%** ($1.6B off.) | 3.27 | 0.03 | +7–8% **RAISED** | 1.64 | 1.01 |
| **WFC** | A (mod, asym) | +$1.7B ✓ | −5.7% | **$32.9B** ✓ | 10.3 | 13% (office focus) | 2.47 | 0.45 | ~$50B maintained | 1.87 | 0.99 |
| **CFG** | A (slight) | +1.3% | −13.2% | n/f | 10.5 | 17% (office ~2%) | 3.14↑ | 0.39 | +10–12% maintained | 1.85 | 0.81 |
| **FITB** | A→N | +0.1 to +0.9% | −14.7% | ~$0.1B | 10.0 | ~13–15% | 3.30↑ | 0.37 | $8.7–8.8B **RAISED** | 2.27 | 1.18 |
| **PNC** | A (sec.) | n/f | −8.7% | n/f | 10.1 | n/f | 2.95↑ | n/f | +14.5%† maintained | 2.21 | 1.21 |
| **JPM** | A (EaR) | n/f | **−1.5%** | $22.9B | 14.3 | ~9.8% | 2.99 | 0.61 | ~$103B **CUT** | 3.21 | 1.29 |
| **MTB** | **N** (hedged) | n/f | **+0.4%** | $0.74B | 10.3 | 16.8% (office stress) | 3.71 | 0.31 | $7.2–7.35B maintained | 2.00 | 1.34 |
| **RF** | A→**N** (hedged) | n/f | −14.7% | n/f | 10.7‡ | 16.8% (**office 0.9%**) | 3.67 | 0.54 | +2.5–4% maintained | 2.16 | 1.36 |
| **HBAN** | A (mod) | −100bp:−0.5% | −10.2% | n/f | 10.2 | 13% (office 1.6%) | 3.24 | 0.26 | +39–43%§ low-end | 1.77 | 0.98 |
| **C** | A (reduced) | −100bp:−$2.0B | −23.6%¶ | n/f | 12.7 | n/f | n/f | ~1.16 | +5–6% maintained | 1.42 | 0.54 |
| **TFC** | **L** (short end) | n/f | −15.0% | n/f | 10.8 | 7.4% | 3.02 | 0.61 | +2–3% **LOWERED** | 1.47 | 0.97 |
| **COF** | N (card) | n/f | −7.0% | N/A (all-AFS) | 14.4 | small | 7.87# | 3.45# | none | 1.47 | 0.37# |

\* KEY marked CET1 (incl. AOCI) ≈10.0%. † PNC incl. FirstBank; legacy ~+7.5–8%. ‡ RF 9.4% incl. AOCI.
§ HBAN distorted by Cadence/Veritex M&A. ¶ Citi AOCI is **mostly FX translation, not securities marks** —
do not read it like a regional's bond hole. # COF card-model / Discover-distorted — not comparable.
**✓ = filing-verified** against the Q1-2026 10-Q (BAC/ZION/USB/KEY/WFC done — see §2.1). △ ZION's *current*
HTM mark is only **$0.07B**; the often-cited "$1.5B" is the pre-tax unrealized loss on securities **transferred
from AFS to HTM**, frozen in AOCI ($1.2B after-tax) and amortizing — it will **not** hit earnings absent a sale,
and is **not** a current HTM fair-value hole (ZION 10-Q, Investment Securities footnote / MD&A).

---

## 2.1 Primary-source detail — the 5 priority banks (Q1-2026 10-Q, read directly)

These five are now finalized from the **actual filings** (SEC EDGAR, accessed 2026-06-26). The original
session's 403s were an egress quirk (missing declared User-Agent), not a content gap; with that fixed every
figure below is read from the primary 10-Q — Item 3 *Quantitative and Qualitative Disclosures About Market
Risk* and the *Investment Securities* footnote.

**A. Interest-rate sensitivity — 12-month NII and EVE (as disclosed; signs are the bank's own):**

| Bank | NII +100bp | +200bp | −100bp | −200bp | EVE +100 / +200bp | Disclosure (10-Q) |
|---|---|---|---|---|---|---|
| **BAC** | **+$0.4B** | +$0.6B | **−$2.0B** | −$4.9B | *qualitative only* | Table 40, banking-book NII to curve, instantaneous |
| **WFC** | **+$1.7B** | *n/d* | −$2.3B | −$5.4B | *not disclosed* | Table 22, 12-mo NII, instantaneous parallel |
| **ZION** | **+3.7%** | **+7.4%** | −3.7% | −7.2% | **−0.1% / −0.8%** | EaR + EVE table, immediate parallel |
| **USB** | *n/d* | **+0.48%** | *n/d* | −0.34% | *MVE method, no figure* | Table 9, ±50 / ±200bp immediate |
| **KEY** | *n/d* | **+0.38%** | *n/d* | +0.12% | *not disclosed* | Figure 22, ±200bp gradual, 12-mo NII-at-risk (tol. ±5%) |

*Units:* BAC and WFC report the NII change in **$B**; ZION, USB, KEY report it as **% of NII**. *n/d* = the bank
does not disclose that shock (USB publishes ±50/±200 only; KEY ±200 gradual only; WFC has no +200 parallel).

**B. Securities unrealized losses (gross, Mar 31 2026) and deposit cost / rough deposit beta:**

| Bank | HTM gross unrl. loss | AFS gross unrl. loss | IB-deposit cost Q1'26 (Q1'25) | Δ YoY | rough down-beta |
|---|---|---|---|---|---|
| **BAC** | **$81.2B** | $3.0B | 1.99% (2.42%) | −43bp | ~0.67 |
| **WFC** | **$32.9B** *(net $32.8B)* | $4.5B | 1.90% (2.17%) | −27bp | ~0.42 |
| **USB** | **$9.4B** | $4.8B | 2.13% (2.39%) | −26bp | ~0.40 |
| **KEY** | **$0.4B** | $2.6B | 2.01% (2.53%) | −52bp | ~0.81 |
| **ZION** | **$0.07B** △ | $1.2B | 2.26% (2.61%) | −35bp | ~0.54 |

**What the primary text settles:**
- **EVE is barely disclosed.** Of the five, **only ZION publishes a quantitative ±bp EVE** — and it is hedged to
  **near-neutral (−0.1% at +100bp, −0.8% at +200bp)** even though its *income* is the most asset-sensitive in the
  group (**EaR +3.7%/+100bp, +7.4%/+200bp**). That split is the whole ZION thesis in two numbers: earnings geared
  to higher rates, economic value hedged flat. **BAC** discusses EVE only qualitatively (managed to internal
  limits, no number); **USB** runs "market value of equity" modeling but discloses no figure; **WFC** and **KEY**
  publish no EVE sensitivity at all. So an EVE-vs-NII contrast can only be drawn cleanly for ZION.
- **HTM marks: two confirmed, two filled, one corrected.** BAC **$81.2B** and WFC **$32.9B** gross confirm the
  web-sourced marks to the dollar. USB **$9.4B** and KEY **$0.4B** fill prior `n/f`s. **ZION is the correction
  (△):** its *current* HTM fair-value gap is only **$0.07B** — the HTM book is mostly agency MBS sitting near par.
  ZION's securities pain is in **AFS (−$1.2B)** plus a **$1.5B pre-tax ($1.2B after-tax) loss on AFS→HTM-transferred
  securities frozen in AOCI** that amortizes and will not hit earnings absent a sale. That ties out with the
  −31.5% AOCI/TCE and means ZION's bond risk is **fully visible on the balance sheet, not hidden in HTM** — the
  opposite of the BAC/WFC pattern. The earlier "$1.5B transfer" cell conflated that AOCI item with an HTM mark.
- **BAC's asymmetry is real and confirmed.** Up moves help little (+$0.4B/+100, +$0.6B/+200); down moves hurt a lot
  (−$2.0B/−100, −$4.9B/−200). The "−$2.0B per −100bp" used in §5's BAC underwrite is the filing figure.
- **The filings flip the BAC-vs-WFC asset-sensitivity ranking.** On the *disclosed instantaneous +100bp parallel*
  shock, **WFC (+$1.7B, ≈+3% of NII) screens as more asset-sensitive than BAC (+$0.4B, ≈+0.6%)**. BAC's
  "most asset-sensitive mega" reputation rests on short-end gearing and on the *level* of rates staying high
  (its huge non-/low-rate deposit base), not on a marginal parallel shock — and its profile is the more asymmetric
  (far more downside to cuts). Net: BAC's tier-1 case rests on **cheapest funding + the only *raised* guidance +
  low CRE**, more than on out-and-out parallel-shock sensitivity, where WFC actually ranks higher.
- **Deposit beta** = Δ(avg cost of *total interest-bearing deposits*, Q1'25→Q1'26, from each 10-Q average-balance
  table) ÷ the **−65bp** move in the quarterly-average **3-month UST** (4.34%→3.69%, a clean Fed-path proxy). This
  is a **cutting-cycle *down*-beta** (pass-through of *falling* rates), not the 2022–24 hiking-cycle up-beta, which
  a single 10-Q can't yield. Read it carefully: a **low** down-beta (USB 0.40, WFC 0.42) means deposits are
  **sticky on the way down** — least margin *relief* if the Fed keeps cutting, but these two already fund cheapest
  (1.90–2.13%). **KEY 0.81** and **BAC 0.67** reprice deposits down fastest. For a *higher-for-longer* world
  (rates roughly flat) the operative edge is the **low absolute funding cost** of WFC/BAC, not the beta sign.

---

## 3. The headline finding — earnings-end vs capital-end (your framework items ① + ②)

The whole point of this framework is that **higher rates help the income statement but hurt the balance
sheet — and the two don't show up in the same place.** Three patterns fall out of the data:

**A. The big banks look clean on AOCI but hide the largest HTM holes.**
AOCI/TCE only captures *available-for-sale* marks. The held-to-maturity mark sits off that line (opt-out
banks), footnote-only — the exact SVB blind spot. So:
- **BAC**: AOCI/TCE a benign −5.3%, but a **$81.2B gross HTM unrealized loss** — by far the largest hidden hole.
  It just **raised** NII guidance (the only mega to). Textbook tension: best earnings leverage to *high rates
  staying high*, worst latent securities scar if it were ever forced to realize it. (On a marginal +100bp parallel
  shock the disclosed NII lift is modest, **+$0.4B** — its asset-sensitivity is short-end/level-driven, not
  parallel-shock-driven; see §2.1.)
- **WFC**: similar shape — clean −5.7% AOCI, but **$32.9B HTM** loss; NIM low (2.47%) but the franchise is sticky.
  Its disclosed +100bp NII lift (**+$1.7B**) is the **largest of the megas** shown here.
- **JPM**: cleanest of the megas (AOCI/TCE −1.5%, HTM loss "only" $23B on a far bigger book), but it **cut**
  NII guidance and trades at **3.2× tangible book** — priced for its quality.

**B. The regionals wear the damage on AOCI, in plain sight.**
- **ZION** is the sharp end: **AOCI/TCE −31.5%** (worst in the group) *and* **22% CRE**, yet it is the **most
  asset-sensitive** regional (+3.7% NII per +100bp) and **raised** guidance. It has hedged EVE to near-neutral
  (+200bp EVE −0.8%), but it is the highest risk/reward name — the cleanest embodiment of "rates up = income
  good, capital bad."
- **USB, KEY, TFC, FITB, RF, CFG** all cluster at −13% to −16% AOCI/TCE — meaningful but not existential, and
  none is forced to sell.

**C. Two names are genuinely clean on capital — for opposite reasons.**
- **MTB**: AOCI/TCE **+0.4%** (a small *gain*) and a tiny $0.7B HTM loss — the least rate-scarred balance sheet
  in the group, the payoff for running hedged-neutral. Offset: it carries the most-watched **office-CRE** book.
- **JPM**: clean by sheer scale and hedging.

> **Citi caveat:** Citi's −23.6% AOCI/TCE looks alarming but is dominated by **foreign-currency translation
> (CTA)**, not bond marks — a different (and less rate-driven) risk than a regional's securities hole. Don't
> rank it alongside ZION.

---

## 4. Deposit franchise, NIM and guidance (items ④ + ⑤)

- **NII guidance direction is the cleanest forward tell** (item ⑤). **Raised:** BAC, KEY, ZION, FITB. **Cut /
  lowered:** JPM, TFC, HBAN(low-end). **Maintained:** WFC, USB, C, PNC, RF, MTB, CFG. The **BAC-raises /
  JPM-cuts** split is the signal of the quarter: BAC's asset sensitivity is paying off into the held-up rate
  curve while JPM laps tough comps.
- **NIM level & direction:** regionals run structurally higher NIM (MTB 3.71, RF 3.67, ZION 3.27, HBAN 3.24,
  CFG 3.14, TFC 3.02) vs the megas (BAC 2.07, WFC 2.47, USB 2.77, PNC 2.95). Several are **expanding** (BAC,
  KEY, CFG, FITB, PNC ↑). Low absolute NIM at BAC/WFC = more room to re-price up; high NIM at the regionals =
  more to defend.
- **Deposit beta** (item ④): now sourced from each 10-Q's average-balance table (see §2.1B). Avg cost of total
  interest-bearing deposits, **Q1'26 (Q1'25)**: WFC **1.90% (2.17%)**, BAC **1.99% (2.42%)**, KEY **2.01% (2.53%)**,
  USB **2.13% (2.39%)**, ZION **2.26% (2.61%)**. All fell YoY as the Fed eased (3-month UST −65bp). The implied
  **cutting-cycle down-beta** runs **USB 0.40 ≈ WFC 0.42 < ZION 0.54 < BAC 0.67 < KEY 0.81** — i.e. WFC/USB hold
  the **cheapest and stickiest** deposit funding (the low-beta franchise edge that pays off in higher-for-longer),
  while KEY/BAC pass falling rates through fastest. Caveat: this is a *down*-cycle beta; the 2022–24 *up*-beta isn't
  recoverable from one quarter's filing.
- **CRE / office** (the regional landmine): **lowest office** = RF (office just **0.9%** of loans) and ZION
  ($1.6B, mostly suburban); **highest watch** = MTB (office-CRE the named stress point), CFG, M-cap-light
  regionals. Total CRE: ZION 22% > CFG 17% > RF/MTB 16.8% > HBAN/WFC/FITB ~13% > JPM ~10% > TFC 7% > BAC 6%.

---

## 5. Verdict — who should outperform peers on this thesis

Framed on the actual thesis (higher-for-longer + dis-inverting curve), not generic value:

**Tier 1 — best rate-positioned (asset-sensitive + guidance up/held + survivable risk):**
- **BAC** — the cleanest-funded mega (lowest deposit cost ex-WFC) and the only one **raising** NII guidance; low
  CRE, rising NIM off a low base. (Note: on a marginal +100bp parallel shock WFC's disclosed NII lift is larger —
  §2.1 — so BAC's edge here is funding + guidance direction, not raw parallel sensitivity.) **The catch you must
  underwrite:** the $81.2B HTM mark. If your thesis is
  rates *stay high or rise*, that mark just sits there and NII compounds — BAC wins. If you think rates get
  *cut*, BAC has the most NII to give back (−$2.0B per −100bp) **and** the hole stays. High-conviction *only*
  under a higher-for-longer view.
- **USB** — asset-sensitive, **best-in-class ROA among the supers (1.09)**, NIM 2.77 and rising, guidance
  maintained +6–7%, reasonable P/TBV 2.0. The lower-drama way to own the thesis; AOCI/TCE −15.6% is the watch.
- **KEY** — guidance **raised** +9–10% as the 2024 securities repositioning flips to a tailwind; ~neutral
  sensitivity means *less downside* if rates fall; cheapest tangible multiple in the tier (1.70×).

**Tier 2 — high-beta / situational:**
- **ZION** — most asset-sensitive regional and **raised** guidance, but **−31.5% AOCI/TCE and 22% CRE**. Highest
  upside to the thesis, highest blow-up risk if credit or deposits wobble. Size it small; it's the lever, not the core.
- **CFG, FITB** — asset-sensitive, CFG cheap with rising NIM (office-CRE watch); FITB **raised** guidance but
  results are pro-forma for the Comerica close (integration + AOCI noise).

**Tier 3 — quality, but rate-neutral (own for the franchise, not the rate beta):**
- **MTB** (cleanest balance sheet, highest NIM, but office CRE) and **RF** (top ROA 1.36, lowest office 0.9%,
  but hedged to neutral so little rate upside). Great banks; muted leverage to *this* thesis.

**Avoid / fade on this thesis:**
- **TFC** — explicitly **liability-sensitive on the short end** and **lowered** NII guidance: it benefits from
  *cuts*, not from higher-for-longer. Wrong side of the trade.
- **JPM** — operationally the best bank here (ROA 1.29, cleanest AOCI), but **cut** guidance and trades at
  3.2× tangible book: you're paying a premium for quality while its NII momentum lags. Own it for safety, not
  for rate upside.
- **COF, C** — special situations: COF is card-model/Discover-distorted (not comparable); Citi is a cheap
  (1.42× TBV) re-rating story whose AOCI optics are FX, not bonds — a different bet entirely.

**One-line answer:** for a *higher-for-longer* Treasury thesis, the peer-outperformer shortlist is
**BAC, USB, KEY** (with **ZION** as the high-beta kicker); **avoid TFC**; treat **JPM** as quality-ballast
rather than a rate play.

---

## 6. Confidence & verification checklist (do before trading)

| Field | Confidence | Note |
|---|---|---|
| AOCI/TCE, AFS/HTM balances, P/TBV, TCE, ROA, NIM-proxy | **High** | Computed from Tushare Q1-2026 balance sheet / FY2025 indicators directly. |
| Curve / 2s10s | **High** | Tushare `us_tycr`, 2026-06-25. |
| CET1, reported NIM, NCO, NPL, NII guidance & direction | **Medium** | Web-sourced from earnings releases/calls; mostly multi-corroborated. |
| **ΔNII ±bp / EVE / HTM·AFS losses / deposit cost — BAC, ZION, USB, KEY, WFC** | **High** | ✅ **Finalized 2026-06-26 from the primary Q1-2026 10-Q** (Item 3 market-risk table + Investment Securities footnote + average-balance deposit cost). See §2.1. |
| **ΔNII ±100bp / EVE table, HTM/AFS unrealized-loss $ — other 10 names** | **Low / partial** | Still web-sourced; live in each 10-Q Item 3 / securities footnote. Same EDGAR full-text method now works (the 403s were a missing User-Agent) — extend when needed. |

**Status:** the 5 priority names (BAC, ZION, USB, KEY, WFC) are **done** from the primary 10-Q (§2.1). **Still
outstanding** — the other 10 (C, PNC, TFC, COF, RF, FITB, MTB, CFG, HBAN; JPM partial): pull each Q1-2026 10-Q
→ *Quantitative and Qualitative Disclosures About Market Risk* (±100/200bp NII + EVE) and *Investment Securities*
footnote (HTM vs AFS unrealized loss) + average-cost-of-deposits, via EDGAR full-text search
(`efts.sec.gov/LATEST/search-index?q=...` or the UI at `https://efts.sec.gov/LATEST/search-index`).

---

## 7. Changelog — primary-source finalization (2026-06-26)

Read directly from each Q1-2026 10-Q (SEC EDGAR). **Net: the thesis holds; three substantive corrections.**

1. **BAC ΔNII +100bp: "+~$0.45B (≈+0.7%)" → +$0.4B.** The old figure conflated the Dec-2025 column (+$0.7B) with
   the current quarter. Full BAC curve (Table 40, $B): +100 **+0.4**, +200 +0.6, −100 −2.0, −200 −4.9. EVE is
   *qualitative only* in BAC's 10-Q.
2. **ZION HTM "$1.5B transfer" → $0.07B current mark (corrected & relabeled).** ZION's *current* HTM gross
   unrealized loss is just **$65M**; the "$1.5B" is the pre-tax loss on **AFS→HTM-transferred** securities frozen
   in **AOCI** ($1.2B after-tax), amortizing, won't hit earnings absent a sale. ZION's bond risk is AFS/AOCI-visible
   (AFS −$1.2B), not a hidden HTM hole. ZION EaR **+3.7%/+100, +7.4%/+200** and **EVE −0.1%/+100, −0.8%/+200**
   both **confirmed** to the filing.
3. **Asset-sensitivity ranking refined.** On the disclosed +100bp parallel shock, **WFC (+$1.7B, ≈+3%) > BAC
   (+$0.4B, ≈+0.6%)** — so BAC's "purest asset-sensitivity mega" framing was softened to *cheapest funding + only
   raised guidance*; §3A/§5 adjusted.

**Filled prior `n/f`s:** USB HTM **$9.4B** / AFS $4.8B / +200bp NII **+0.48%** (confirmed); KEY HTM **$0.4B**
(bal $8.7B) / AFS $2.6B / +200bp NII-at-risk **+0.38%** (gradual). **Confirmed to the dollar:** BAC HTM **$81.2B**,
WFC HTM **$32.9B** gross ($32.8B net), WFC +100bp **+$1.7B**, BAC −100bp **−$2.0B**.

**Deposit beta (new):** avg cost of total interest-bearing deposits, Q1'26 vs Q1'25, from each 10-Q average-balance
table, ÷ the −65bp move in the quarterly-avg 3-month UST → cutting-cycle **down-betas: USB 0.40, WFC 0.42, ZION
0.54, BAC 0.67, KEY 0.81**. WFC/USB fund cheapest and stickiest (1.90%/2.13%).

---

*Screening aid, not investment advice. The 5 priority names are primary-sourced (§2.1, §7); the other 10's
filing-layer figures remain web-sourced pending the same treatment. 中国境内用户如涉及境外投资,请注意合规与风险揭示。*
