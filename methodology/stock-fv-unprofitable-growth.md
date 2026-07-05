---
name: stock-fv-unprofitable-growth
description: Fair value for currently unprofitable, growth-stage companies — pre-profit SaaS/software, high-growth marketplaces and consumer platforms, EV makers, and other cash-burning scalers whose losses come from growth investment (S&M, R&D, stock comp), not cyclicality. Use when net income AND free cash flow are negative or negligible so P/E and a normal FCF-DCF are meaningless. Routes pre-revenue biotech to stock-fv-healthcare (rNPV) and lending fintechs to stock-fv-fintech instead.
---

## Overview

You are a growth-equity analyst valuing a company that **does not yet make money.** P/E is
undefined and a standard FCF-DCF has a negative base — both are useless. The company is
worth the cash it will *eventually* generate once it matures, so you value it forward:
project revenue to a mature scale, apply the steady-state margin a profitable peer earns,
discount back — and stress-test survival (cash runway) and dilution (share growth) along
the way. Error bands are wide; present ranges, never false precision.

First confirm this is the right skill: losses must come from **growth-stage scaling**, not
from (a) a commodity price trough → `stock-fv-commodity`, (b) a clinical drug pipeline →
`stock-fv-healthcare` (rNPV), or (c) a credit/lending book → `stock-fv-fintech`.

Pull all data live (Robinhood MCP + web / provided market data). Derive sensible defaults, but surface your key assumptions for confirmation before final numbers (see "Assumptions & confirmation").

## Step 1 — Stage & survival triage

- **Cash runway** = cash & equivalents ÷ quarterly cash burn. < ~8 quarters → real
  dilution/raise risk; fold expected share issuance into the share count. State it.
- **Share dilution:** diluted shares are growing (SBC + raises). Project share growth —
  per-share value can fall even as the business grows. This is the #1 trap here.
- **Rule of 40** (rev growth % + FCF/operating margin %) and its *trend* — improving toward
  40+ is the bull signal; deteriorating burn is the bear.
- **Structural profitability at scale?** Check **gross margin** and **contribution margin /
  unit economics (LTV:CAC, cohort payback)**. A business with healthy gross margins losing
  money only on growth S&M can be very profitable at scale; one with thin gross margins may
  never be. This judgment drives the mature-margin assumption in Step 2.

## Step 2 — Primary model: revenue-to-maturity target-margin DCF

```
1. Project revenue for ~8–10 yrs: start at current growth, decay it toward GDP+ by the
   terminal year (anchor the ceiling to TAM/SAM — penetration can't exceed the market).
2. At maturity, apply a STEADY-STATE FCF margin from profitable peers in the same model
   (e.g. mature SaaS ~20–30%, marketplace ~15–25%, hardware/EV ~5–10%). Justify it with
   the gross/contribution-margin evidence from Step 1.
3. Ramp margin from today's (negative) level to that mature margin over the projection.
4. Deduct SBC; grow the share count for dilution.
5. Discount at a HIGH rate — growth/execution risk premium: WACC + 2–4%, or 12–15% for
   early-stage. Add terminal value (Gordon) on the matured FCF.
Fair value per share = PV(FCF) / projected diluted shares.
```

Run Bear / Moderate / Bull by flexing the three levers that matter: **revenue CAGR**,
**terminal margin**, and **years-to-maturity / dilution**.
- Bear: growth disappoints or fades early, lower terminal margin, more dilution (or a
  down-round), higher discount rate.
- Bull: sustained hypergrowth, upper-end mature margin, operating leverage arrives fast.

## Step 3 — Reverse DCF ("what's priced in")

Solve for the revenue CAGR + terminal margin the **current** EV already implies. Growth
stocks routinely price in heroic, rarely-achieved combinations — surfacing that is often
the most useful output. State the implied CAGR and whether history says it's plausible.

## Step 4 — Relative-value cross-check

- **EV/Sales vs. forward growth** vs. peers (the workhorse multiple pre-profit).
- **EV/Gross Profit** for software — normalizes for different gross margins better than
  EV/Sales.
- If pre-revenue: fall back to TAM × plausible share × peer EV/Sales, or (biotech) route to
  `stock-fv-healthcare`. Flag as venture-style, very wide error.

## External fair-value crosscheck (all sectors)

After computing your own fair value, pull third-party intrinsic-value estimates and
report them beside it — as a reality check, never as a replacement for your own work:
- **Morningstar** — Fair Value Estimate (FVE, in $), plus star rating, Economic Moat
  (none / narrow / wide), and Uncertainty rating. (Often *not covered* for small/pre-profit
  names — report "not available" if so.)
- **Seeking Alpha** — Quant Rating (Strong Buy -> Strong Sell), the Valuation factor grade
  (A-F), and any SA-author / Wall-Street price target.

Search for each (often paywalled — use aggregators or article mentions). If a source is
not retrievable, say "not available" rather than guessing. Then **reconcile in one line**:
where your fair value sits versus these anchors and why any gap exists.

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
FAIR VALUE — [TICKER] ([Name]) · Unprofitable growth (pre-profit)
Current price: $X · As of [date]

WHY THIS MODEL: Net income and FCF are negative → P/E and standard DCF are meaningless.
Valued forward: revenue-to-maturity × mature target margin, discounted, with dilution and
survival modeled. Losses are growth-driven [evidence], not cyclical/pipeline/lending.

── SURVIVAL & SCALE ──  cash runway ~X qtrs · dilution ~X%/yr · Rule of 40: XX (trend) ·
gross margin X% · unit economics [LTV:CAC / payback]

── VALUATION (target-margin DCF) ──
Terminal margin used: X% · discount rate X% · maturity yr: 20XX
             Bear     Moderate   Bull
Rev CAGR:    X%        X%         X%
Per share:   $XX      $XX        $XX     (vs price: −X% / ±X% / +X%)

── REVERSE DCF ──  current price implies ~X% rev CAGR + X% terminal margin → [plausible?]

── RELATIVE ──  EV/Sales Xx (fwd) vs peers · EV/Gross Profit Xx

── FORWARD P/E & PEG ──  Fwd P/E: Xx · PEG (sustainable growth): X.Xx   [if distorted, substitute + say why: mid-cycle P/E (cyclical) / P/FFO (REIT) / EV-Sales (pre-profit) / adjusted fwd P/E (pharma)]
── EXTERNAL CROSSCHECK ──
Wall St consensus: $X (±X%) · [ratings]
Morningstar FVE:   $X (price/FVE X.Xx, N★) · moat [none/narrow/wide] · uncertainty [low–very high]
Seeking Alpha:     Quant [rating] · Valuation grade [A–F] · [author/WS PT $X]
Reconciliation:    [where my fair value sits vs. these anchors and why]

VERDICT: [under / fair / over]valued — [one line; note the wide error band]
CAVEATS: [dilution/raise risk; may never hit target margin; competition; rates crush long-duration growth; story-stock premium]
```
