---
name: stock-fv-ai-capex
description: Fair value for megacap platforms whose free cash flow is TEMPORARILY depressed by an AI-datacenter capex supercycle — Microsoft, Alphabet, Meta, Amazon (AWS), Oracle and similar hyperscalers building GPU capacity. Use when a highly profitable cash-cow core is spending abnormally elevated (and rising) capex on AI infrastructure, so naive current-FCF understates intrinsic value. The core question is whether that capex earns above the cost of capital.
---

## Overview

You are a technology-sector analyst handling the hardest valuation problem of this era:
a company whose *current* FCF is artificially low because it is plowing cash into AI
datacenters. A naive DCF on depressed trailing FCF **understates** these businesses — the
mirror image of the usual staleness problem. But you must NOT simply assume the capex
vanishes and FCF snaps back; the honest question is **whether the incremental AI capex
earns a return above the cost of capital.** Value the mature core as a compounder, then
treat the AI build as a separately-scenariod investment.

Pull all data live (Robinhood MCP + web). Derive sensible defaults, but surface your key assumptions for confirmation before final numbers (see "Assumptions & confirmation").

## Step 1 — Gather data

- Robinhood: price, shares, market cap, beta, P/E.
- Web, last 5 yrs: revenue, operating income by segment (isolate the mature core:
  Search/Ads, Windows+Office, AWS run-rate, Instagram/FB ads), **capex** and
  **capex/revenue** trend, D&A, SBC, operating cash flow, net cash.
- Web: management capex guidance for next 1–2 years; consensus revenue growth; 10-yr Treasury.

## Step 2 — Diagnose the capex distortion

```
Capex/Revenue now vs. 5-yr-ago            → how elevated is the build?
Maintenance capex ≈ D&A (steady-state proxy)
Excess (growth/AI) capex = Total capex − maintenance capex
Normalized FCF = Operating cash flow − maintenance capex   (the "if it stopped building" number)
```
Report **both** reported FCF and normalized FCF. The gap is the AI investment you must
value explicitly rather than penalize by default.

## Step 3 — Two valuations, run both

**(A) Normalized-capex DCF.** Run the **`stock-dcf`** engine but replace elevated capex
with mid-cycle capex/revenue (or maintenance ≈ D&A) to get normalized FCF, then grow it.
This answers "what is the business worth if the build proves to be ordinary reinvestment
that sustains growth?" Use SBC-adjusted numbers. WACC discount rate.

**(B) Sum-of-the-parts.**
- **Mature core** = value the cash-cow segments as a stable compounder (their own
  operating income × appropriate multiple, or a mini-DCF). This is the floor.
- **AI investment** = value the incremental invested capital by the return it earns.
  Compute (or scenario) **ROIC on incremental AI capex vs. WACC**:
  - *Bear — capex is largely wasted:* AI ROIC < WACC → value the build at (or below) cost;
    the market is right to discount depressed FCF.
  - *Moderate — earns its cost of capital:* AI ROIC ≈ WACC → NPV-neutral; worth ~invested capital.
  - *Bull — supernormal returns:* AI ROIC > WACC (cloud/AI demand compounds) → the build
    creates large NPV; normalized FCF understates by a lot.

Combine: `Fair value = mature-core value + AI-investment value + net cash`.

## Step 4 — Sanity multiples

- **EV/EBITDA** — far less capex-distorted than P/FCF while the build runs (but note D&A
  will *rise* as the capex depreciates, pressuring future EPS — flag this).
- **Mature-core P/E** — strip the AI drag and value the core on its own earnings.
- **Reported P/FCF** — show it, then explain why it overstates cheapness/expensiveness.

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

## Time horizons (label every target)

State the horizon of each figure so they are comparable — a multi-year intrinsic value and
a 12-month price target are NOT the same number, and confusing them creates fake
"disagreement":
- **Your Bear / Moderate / Bull fair value** = **intrinsic value TODAY** (present value of
  the DCF / normalized-earnings model) — what the business is worth now. The market price
  typically converges toward it over **~2–3 years** (wide, thesis-dependent). It is NOT a
  12-month price target.
- **Wall Street consensus** = a **12-month** price target (sentiment + near-term multiple).
- **Morningstar FVE** = a **long-term intrinsic** value (present value, like your own).

If your Moderate sits above the 12-month Street target, say so explicitly and attribute the
gap to horizon, not to a valuation disagreement.

## Output format

```
FAIR VALUE — [TICKER] ([Name]) · AI-capex megacap
Current price: $X · As of [date]

WHY THIS MODEL: Current FCF is temporarily depressed by AI-datacenter capex → naive DCF
understates. Value = mature core (compounder) + AI build (scenario'd on ROIC vs WACC).

── CAPEX DISTORTION ──
Capex/rev: X% (vs X% 5yr ago)   Maintenance≈D&A: $X.XB   Excess AI capex: $X.XB
Reported FCF: $X.XB   Normalized FCF: $X.XB   (gap = the AI bet)

── VALUATION ──
(A) Normalized-capex DCF per share:  Bear $XX · Mod $XX · Bull $XX
(B) SOTP:  Mature core $XX + AI investment [Bear $X / Mod $X / Bull $X] + net cash $X
    → Bear $XX · Moderate $XX · Bull $XX     (vs price: −X% / ±X% / +X%)
AI incremental ROIC vs WACC: X% vs X% → [value-accretive / neutral / destructive]

── SANITY ──  EV/EBITDA Xx (note rising D&A) · mature-core P/E Xx · reported P/FCF Xx

── HORIZON ──  Bear/Moderate/Bull above = intrinsic value TODAY (present value); price typically converges over ~2–3 yrs, thesis-dependent — NOT a 12-month target.
── FORWARD P/E & PEG ──  Fwd P/E: Xx · PEG (sustainable growth): X.Xx   [if distorted, substitute + say why: mid-cycle P/E (cyclical) / P/FFO (REIT) / EV-Sales (pre-profit) / adjusted fwd P/E (pharma)]
── EXTERNAL CROSSCHECK ──
Wall St consensus (12-mo target): $X (±X%) · [ratings]
Morningstar FVE (long-term intrinsic): $X (price/FVE X.Xx, N★) · moat [none/narrow/wide] · uncertainty [low–very high]
Seeking Alpha:     Quant [rating] · Valuation grade [A–F] · [author/WS PT $X]
Reconciliation:    [where my fair value sits vs. these anchors and why]

VERDICT: [under / fair / over]valued — [one line, hinge on whether capex earns its cost]
CAVEATS: [rising D&A → EPS pressure; capex could prove value-destructive; SBC; regulatory]
```
