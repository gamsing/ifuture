# US Bank Rate-Positioning Study — Who Outperforms on the Rate Thesis

> **Thesis.** US Treasury yields higher-for-longer, curve dis-inverting. Banks that win are
> **asset-sensitive** (NII rises with rates), with **low deposit beta**, **clean AOCI / small HTM holes**,
> and **manageable CRE** — the dual-edged risks that blew up the 2023 regionals. This study ranks 15 large +
> regional US banks on that framework, not on generic quality/value.
>
> **As of 2026-06-25.** Structured layer = Tushare (Q1-2026 balance sheet `20260331` + FY2025 indicators +
> 2026-06-24 valuation). Filing layer = SEC 10-Q/10-K + Q1-2026 earnings calls.
>
> **⚠️ Source-confidence caveat (important).** This environment's egress policy **hard-blocks direct fetch of
> SEC EDGAR and company IR sites** (HTTP 403). The filing-layer figures (asset-sensitivity tables, HTM/AFS
> marks, CET1, CRE, NII guidance) were therefore recovered via **web search of those same filings/transcripts**,
> not by reading primary documents — they are **single-source and should be verified against the actual 10-Q
> before trading**. The structured layer (AOCI, AFS/HTM balances, TCE, P/TBV, ROA) is computed directly from
> the Tushare feed and is high-confidence. Per-field confidence is flagged throughout. Not investment advice.

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
**AOCI/TCE** and **P/TBV** are hard structured figures; filing-layer columns are web-sourced (verify).

| Ticker | Sens | ΔNII +100bp | AOCI/TCE | HTM unrl. loss | CET1 | CRE % (office) | NIM | NCO % | FY26 NII guide (Δ) | P/TBV | ROA |
|---|:--:|---|---:|---|---:|---|---:|---:|---|---:|---:|
| **BAC** | **A** (asym) | +~$0.45B (≈+0.7%) | −5.3% | **$81.2B** | 11.2 | 5.7% (low) | 2.07↑ | 0.48 | +6–8% **RAISED** | 1.98 | 0.89 |
| **USB** | **A** (mod) | +200bp:+0.48% | −15.6% | n/f | 10.8 | n/f | 2.77 | 0.56 | +6–7% maintained | 2.01 | 1.09 |
| **KEY** | N→A | n/f | −15.1% | n/f (HTM~$8.6B) | 11.4* | n/f | 2.87↑ | 0.38 | +9–10% **RAISED** | 1.70 | 0.99 |
| **ZION** | **A** (high) | **+3.7%** | **−31.5%** | $1.5B transfer | 11.5 | **22%** ($1.6B off.) | 3.27 | 0.03 | +7–8% **RAISED** | 1.64 | 1.01 |
| **WFC** | A (mod, asym) | +$1.7B (≈+3.4%) | −5.7% | **$32.8B** | 10.3 | 13% (office focus) | 2.47 | 0.45 | ~$50B maintained | 1.87 | 0.99 |
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

---

## 3. The headline finding — earnings-end vs capital-end (your framework items ① + ②)

The whole point of this framework is that **higher rates help the income statement but hurt the balance
sheet — and the two don't show up in the same place.** Three patterns fall out of the data:

**A. The big banks look clean on AOCI but hide the largest HTM holes.**
AOCI/TCE only captures *available-for-sale* marks. The held-to-maturity mark sits off that line (opt-out
banks), footnote-only — the exact SVB blind spot. So:
- **BAC**: AOCI/TCE a benign −5.3%, but a **$81B gross HTM unrealized loss** — by far the largest hidden hole.
  It is also the *most asset-sensitive* big bank and just **raised** NII guidance. Textbook tension: best
  earnings leverage to higher rates, worst latent securities scar if it were ever forced to realize it.
- **WFC**: similar shape — clean −5.7% AOCI, but **$33B HTM** loss; NIM low (2.47%) but the franchise is sticky.
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
- **Deposit beta** (item ④): not cleanly in any feed; directionally, the low-cost-deposit megas (BAC, WFC, USB)
  carry the lowest betas = better in higher-for-longer. *Verify against each 10-Q's average-cost-of-deposits
  trend — this is the one item I could not source consistently.*
- **CRE / office** (the regional landmine): **lowest office** = RF (office just **0.9%** of loans) and ZION
  ($1.6B, mostly suburban); **highest watch** = MTB (office-CRE the named stress point), CFG, M-cap-light
  regionals. Total CRE: ZION 22% > CFG 17% > RF/MTB 16.8% > HBAN/WFC/FITB ~13% > JPM ~10% > TFC 7% > BAC 6%.

---

## 5. Verdict — who should outperform peers on this thesis

Framed on the actual thesis (higher-for-longer + dis-inverting curve), not generic value:

**Tier 1 — best rate-positioned (asset-sensitive + guidance up/held + survivable risk):**
- **BAC** — the purest asset-sensitivity play among the megas and the only one **raising** NII guidance; low
  CRE, rising NIM off a low base. **The catch you must underwrite:** the $81B HTM mark. If your thesis is
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
| **ΔNII ±100bp / EVE table, HTM/AFS unrealized-loss $** | **Low / partial** | The single highest-value items — live in 10-Q Item 3 / securities footnote, which were **egress-blocked**. Several are NOT FOUND or single-source. **Pull these directly from EDGAR to finalize.** |

**To complete the study from an unblocked network:** open each bank's **Q1-2026 10-Q → "Quantitative and
Qualitative Disclosures About Market Risk"** (the ±100/200bp NII and EVE table) and **securities footnote**
(HTM vs AFS unrealized loss), plus the **average-cost-of-deposits** trend for a clean deposit-beta. Priority
order: BAC, ZION, USB, KEY, WFC (the names whose verdict most hinges on the missing sensitivity/HTM cells).

---

*Screening aid, not investment advice. Filing-layer figures are web-sourced pending primary-document
verification. 中国境内用户如涉及境外投资,请注意合规与风险揭示。*
