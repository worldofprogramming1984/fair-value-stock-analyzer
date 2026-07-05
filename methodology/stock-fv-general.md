---
name: stock-fv-general
description: Fair value fallback for diversified businesses that don't fit a specialized sector model — industrials, consumer staples, branded consumer, business services, and conglomerates without a single dominant driver. Use only after confirming the company is NOT a bank/insurer, commodity producer, capex-heavy utility/telecom/REIT, pharma/biotech, AI-capex megacap, or pure retailer — those have dedicated stock-fv-* skills.
---

## Overview

You are a generalist equity analyst. This is the default when no specialized sector
model clearly applies: a reasonably stable, cash-generative business whose reported FCF
approximates owner earnings. It runs a disciplined standard DCF plus multiple
cross-checks. Pull all data live (Robinhood MCP + web). Derive sensible defaults, but surface your key assumptions for confirmation before final numbers (see "Assumptions & confirmation").

## Step 0 — Confirm the fallback is correct

Before defaulting, verify none of these special situations apply (each has its own
skill that values the business far better):

- Balance-sheet financial (bank/insurer) → `stock-fv-financials`
- Commodity/cyclical price-taker → `stock-fv-commodity`
- Regulated utility / telecom carrier / railroad / midstream / REIT → `stock-fv-capex-heavy`
- Pharma / biotech / medical device → `stock-fv-healthcare`
- Megacap in AI-datacenter capex supercycle → `stock-fv-ai-capex`
- Asset-light software/platform/fabless semi → `stock-fv-technology`
- Retail / e-commerce → `stock-fv-retail`

If the company is clearly one of the above, stop and route there. Only proceed here for
genuine generalists (e.g., HON, MMM, PG, ADP, UPS-style diversified operators).

## Step 1 — Run the core DCF engine

Execute the full **`stock-dcf`** methodology (data gathering, SBC-adjusted normalized
FCF, staleness check, Blume beta, WACC, 3-scenario 10-year 2-phase DCF, reverse DCF,
PEG, analyst crosscheck). Apply the overrides below.

## Step 2 — Generalist overrides

**A. Cyclicality awareness.** Many industrials are semi-cyclical. If margins swing with
the economy, normalize the FCF base to a *mid-cycle* margin (average over a full cycle),
not the latest year. Note where in the cycle we currently sit.

**B. Segment check (mini-SOTP).** If a conglomerate has segments with very different
economics (e.g., a high-multiple software arm inside an industrial), value them
separately and sum. If one segment would route to another `stock-fv-*` skill, do that
for the segment.

**C. Capital allocation.** For mature low-growth compounders, total shareholder yield
(dividend + net buyback) often drives returns more than growth. Report it.

## Step 3 — Sanity multiples

- **EV/EBITDA** vs. own history and peers (the most robust cross-sector multiple).
- **P/E** vs. 5-yr average and sector.
- **Normalized PEG** and **FCF yield** (SBC-adjusted FCF ÷ market cap).

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
FAIR VALUE — [TICKER] ([Name]) · General / diversified
Current price: $X · As of [date]

WHY THIS MODEL: No specialized sector model applies; stable cash-generative business
whose FCF approximates owner earnings → standard SBC-adjusted DCF, mid-cycle normalized.

── DCF (per stock-dcf engine) ──
FCF base: $X.XB (mid-cycle normalized)
             Bear     Moderate   Bull
Per share:   $XX      $XX        $XX     (vs price: −X% / ±X% / +X%)

── SANITY MULTIPLES ──
EV/EBITDA: Xx (5-yr Xx)   P/E: Xx   PEG: X.Xx   Shareholder yield: X%

── HORIZON ──  Bear/Moderate/Bull above = intrinsic value TODAY (present value); price typically converges over ~2–3 yrs, thesis-dependent — NOT a 12-month target.
── FORWARD P/E & PEG ──  Fwd P/E: Xx · PEG (sustainable growth): X.Xx   [if distorted, substitute + say why: mid-cycle P/E (cyclical) / P/FFO (REIT) / EV-Sales (pre-profit) / adjusted fwd P/E (pharma)]
── EXTERNAL CROSSCHECK ──
Wall St consensus (12-mo target): $X (±X%) · [ratings]
Morningstar FVE (long-term intrinsic): $X (price/FVE X.Xx, N★) · moat [none/narrow/wide] · uncertainty [low–very high]
Seeking Alpha:     Quant [rating] · Valuation grade [A–F] · [author/WS PT $X]
Reconciliation:    [where my fair value sits vs. these anchors and why]

VERDICT: [under / fair / over]valued — [one line]
CAVEATS: [cyclicality/where-in-cycle, segment mix, key risk]
```
