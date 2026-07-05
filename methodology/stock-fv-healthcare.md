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

Pull all data live (Robinhood MCP + web). Derive sensible defaults, but surface your key assumptions for confirmation before final numbers (see "Assumptions & confirmation").

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

## Assumptions & confirmation

Before presenting final valuation numbers, surface the assumptions you will use and let
the user override them:
1. Derive default assumptions from the data — the base (FCF / earnings / book / FFO as
   appropriate), Phase-1 growth, discount rate (WACC or cost of equity), terminal growth,
   and any sector-specific margins or multiples used above.
2. Print a clear **ASSUMPTIONS** block: label each value and note where it came from.
3. Ask: *"Would you like to enter your own values for any of these, or should I proceed
   with these assumptions?"* — then wait for the reply.
4. If the user provides overrides, recompute with them; otherwise proceed. Always echo the
   final assumptions used in the output.

Non-interactive contexts (a one-shot call that cannot collect a reply — e.g. the web app's
single-shot mode, or when the caller has already supplied confirmed assumptions) skip the
question: print the ASSUMPTIONS block and proceed with the given/default values.

## Forward P/E & PEG (always report when recommending)

Alongside the sector sanity multiples, always surface **forward P/E** and **PEG** so the
recommendation carries a growth-adjusted valuation check:
- **Forward P/E** = price / next-FY consensus EPS.
- **PEG** = forward P/E / sustainable long-run EPS growth % (use the durable multi-year
  growth rate, NOT a one-time surge year). PEG <1 = cheap for the growth; 1-1.5 = fair for
  a quality compounder; >2 = priced for high conviction.

Use the RIGHT denominator — these two MISLEAD for some businesses, so flag and substitute
rather than printing a garbage number:
- **Cyclical / commodity:** forward P/E on peak-or-trough earnings misleads — use a
  MID-CYCLE-normalized P/E and say so; PEG is not meaningful (price-taker).
- **REITs:** use forward **P/FFO** (and FFO-growth PEG), not P/E.
- **Pre-profit / unprofitable growth:** P/E and PEG are undefined — use EV/Sales vs growth.
- **Banks / insurers:** P/E is fine; PEG is secondary to P/B-vs-ROE.
- **Distorted GAAP earnings** (acquired-IPR&D / intangible amortization — e.g. some pharma):
  use ADJUSTED forward EPS and state that GAAP is distorted.

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

── FORWARD P/E & PEG ──  Fwd P/E: Xx · PEG (sustainable growth): X.Xx   [if distorted, substitute + say why: mid-cycle P/E (cyclical) / P/FFO (REIT) / EV-Sales (pre-profit) / adjusted fwd P/E (pharma)]
── EXTERNAL CROSSCHECK ──
Wall St consensus: $X (±X%) · [ratings]
Morningstar FVE:   $X (price/FVE X.Xx, N★) · moat [none/narrow/wide] · uncertainty [low–very high]
Seeking Alpha:     Quant [rating] · Valuation grade [A–F] · [author/WS PT $X]
Reconciliation:    [where my fair value sits vs. these anchors and why]

VERDICT: [under / fair / over]valued — [one line]
CAVEATS: [patent cliff timing; pipeline/trial risk; IRA drug-price negotiation; M&A/IPR&D noise]
```
