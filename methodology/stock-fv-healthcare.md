---
name: stock-fv-healthcare
description: Fair value for healthcare businesses — large-cap pharma, clinical-stage biotech, and medical devices/tools/diagnostics. Use for drug and device makers whose value hinges on patents, pipelines, and regulated approvals. Handles GAAP distortion from acquired-IPR&D and intangible amortization, explicit patent-cliff (loss-of-exclusivity) modeling for pharma, and risk-adjusted NPV for pipeline biotech. Route managed-care/health insurers to stock-fv-financials instead.
---

## Overview

You are a healthcare equity analyst. This sector has three very different animals, so
first identify which one you're valuing, then use its model. The two recurring traps:
(1) GAAP earnings are meaningless for acquisitive pharma (acquired-IPR&D charges and
amortization of acquired intangibles crush reported net income — ABBV showed a 128x GAAP
P/E that was pure noise); use **adjusted (non-GAAP) earnings**. (2) Patents expire — a
drug can lose most of its revenue overnight at **loss of exclusivity (LOE)**; you must
model the cliff, not extrapolate.

Pull all data live (Robinhood MCP + web). Never ask the user for inputs.

## Step 1 — Identify the sub-type

- **Large-cap pharma** (ABBV, PFE, MRK, LLY): commercial drugs + pipeline → Step 2.
- **Clinical-stage biotech** (little/no product revenue, burning cash): pipeline is
  everything → Step 3 (rNPV).
- **Medical device / tools / diagnostics** (ISRG, MDT, TMO): steady compounder, razor-
  and-blade, high switching costs → Step 4.
- **Managed care / health insurer** (UNH, ELV, CI): STOP — this is a balance-sheet
  financial; use `stock-fv-financials` (P/B-ROE, medical loss ratio).

## Step 2 — Large-cap pharma: adjusted-FCF DCF with explicit patent cliffs

- **Use adjusted earnings/FCF.** Strip acquired-IPR&D and amortization of acquired
  intangibles. State GAAP vs. adjusted and why adjusted is the right base.
- **Model the cliff.** List top drugs, their share of revenue, and **LOE dates**. In the
  projection, step down each drug's revenue at its LOE (typically −50% to −80% within
  1–2 years as generics/biosimilars enter). Do NOT apply a smooth single growth rate over
  a cliff.
- **Add the pipeline.** Credit late-stage assets (probability-weighted peak sales) that
  offset the cliff. Growth engines (e.g., a company's post-Humira Skyrizi/Rinvoq) are the
  bull case.
- Run the **`stock-dcf`** engine on adjusted FCF, but hand-shape Phase-1 growth around the
  cliff/pipeline schedule rather than using a mechanical CAGR. WACC discount rate.
- Sanity: **adjusted P/E**, **PEG on normalized (post-cliff) growth**, EV/EBITDA, dividend.

## Step 3 — Clinical-stage biotech: risk-adjusted NPV (rNPV)

Current earnings are negative and irrelevant. Value the pipeline asset-by-asset:
```
rNPV = Σ_assets [ peak sales × probability of approval (PoA) × PV of cash-flow profile ]
       − PV of R&D + SG&A burn until launch
       + net cash
```
- PoA by phase (rough industry priors): Phase 1 ~10%, Phase 2 ~20–30%, Phase 3 ~50–65%,
  filed ~85%. State the priors used.
- Add **cash runway** (quarters of burn left) — dilution risk if they must raise.
- This is inherently wide-error; present a range, not a point.

## Step 4 — Medical device / tools: compounder DCF

- Run the **`stock-dcf`** engine on SBC-adjusted FCF (behaves like a quality tech
  compounder: durable growth, high switching costs, recurring consumables/service).
- Sanity: EV/EBITDA, P/E vs. history, organic growth rate.

## External fair-value crosscheck (all sectors)

After computing your own fair value, pull third-party intrinsic-value estimates and
report them beside it — as a reality check, never as a replacement for your own work:
- **Morningstar** — Fair Value Estimate (FVE, in $), plus star rating, Economic Moat
  (none / narrow / wide), and Uncertainty rating. This is a genuine intrinsic-value anchor.
- **Seeking Alpha** — Quant Rating (Strong Buy -> Strong Sell), the Valuation factor grade
  (A-F), and any SA-author / Wall-Street price target. (SA usually has no single "fair
  value" number — report the Quant rating + Valuation grade instead.)

Search for each (often paywalled — use aggregators or article mentions). If a source is
not retrievable, say "not available" rather than guessing. Then **reconcile in one line**:
where your fair value sits versus Morningstar's FVE and the Street, and why any gap exists
(typically different growth or discount-rate assumptions).

## Output format

```
FAIR VALUE — [TICKER] ([Name]) · Healthcare [pharma / biotech / device]
Current price: $X · As of [date]

WHY THIS MODEL: [Adjusted-FCF DCF with patent-cliff modeling | rNPV pipeline sum |
compounder DCF]. GAAP earnings [adjusted because …].

── PHARMA: adjusted FCF $X.XB (GAAP net income $X.XB) · key LOEs: [drug @ year, …] · pipeline offset [assets]
── BIOTECH: rNPV by asset [Asset A $X (PhaseN, PoA X%) …] · cash runway X qtrs
── DEVICE: SBC-adj FCF $X.XB · organic growth X%

── VALUATION ──
Per share:  Bear $XX · Moderate $XX · Bull $XX   (vs price: −X% / ±X% / +X%)

── SANITY ──  Adjusted P/E Xx · PEG(normalized) X.Xx · EV/EBITDA Xx · dividend X%

── EXTERNAL CROSSCHECK ──
Wall St consensus: $X (±X%) · [ratings]
Morningstar FVE:   $X (price/FVE X.Xx, N★) · moat [none/narrow/wide] · uncertainty [low–very high]
Seeking Alpha:     Quant [rating] · Valuation grade [A–F] · [author/WS PT $X]
Reconciliation:    [where my fair value sits vs. these anchors and why]

VERDICT: [under / fair / over]valued — [one line]
CAVEATS: [patent cliff timing; pipeline/trial risk; IRA drug-price negotiation; M&A/IPR&D noise]
```
