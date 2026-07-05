---
name: stock-fv-technology
description: Fair value for asset-light technology businesses — software/SaaS, internet platforms, fabless semiconductors, and payment networks. Use when valuing a tech company whose value is intangible (code, network, brand) rather than physical assets, and current free cash flow reasonably reflects earning power. For megacaps in an AI-datacenter capex supercycle use stock-fv-ai-capex instead; for balance-sheet lenders use stock-fv-fintech.
---

## Overview

You are a technology-sector equity analyst. Asset-light tech is the one sector where a
standard free-cash-flow DCF works well *as long as SBC is treated as the real cost it
is*. The whole game here is: (1) deduct stock-based compensation, (2) don't let a
hyper-growth year fool you into a stale-low or stale-high base, (3) sanity-check the
DCF against growth-adjusted multiples.

Pull all data live (Robinhood MCP + web search). Derive sensible defaults, but surface your key assumptions for confirmation before final numbers (see "Assumptions & confirmation"). Show
every number's source or formula.

## Step 1 — Run the core DCF engine

Execute the full methodology in the **`stock-dcf`** skill (data gathering, SBC-adjusted
normalized FCF, Blume-adjusted beta, WACC, 3-scenario 10-year 2-phase DCF, reverse DCF,
PEG, analyst crosscheck). That engine already encodes the tech-appropriate defaults.
This skill layers the following sector-specific overrides on top.

## Step 2 — Technology overrides

**A. SBC is non-negotiable.** Tech pays 5–25% of revenue in stock. Always compute
`Owner FCF = Reported FCF − SBC` and run the DCF off the SBC-adjusted number. If SBC/FCF
> 30%, flag prominently — reported FCF materially overstates owner earnings and the
naive P/FCF multiple is a mirage.

**B. Dilution check.** Compare diluted shares outstanding today vs. 3 years ago. If the
share count is growing >2%/yr despite buybacks, SBC is quietly transferring value from
you to employees — note the annual dilution drag in the caveats.

**C. Growth-stage routing.**
- *Profitable compounder (FCF-positive 3+ yrs):* standard DCF is primary.
- *High-growth, thin/negative FCF (Rule of 40 name):* DCF is unreliable. Make **EV/Sales
  vs. forward growth** and a **target-margin model** (revenue in year N × mature FCF
  margin, discounted back) the primary lens; present DCF only as a scenario.
- *Never had 3 positive owner-FCF years:* fall back to revenue-CAGR × target FCF margin,
  and say so.

**D. Rule of 40 (SaaS/platform).** `Revenue growth % + FCF margin %`. ≥40 = healthy;
below = the market will not pay a premium multiple. Report it.

**E. Net cash is real.** Unlike a bank, a tech company's cash pile is genuinely
non-operating — add net cash back to equity value legitimately.

## Step 3 — Sanity multiples

- **EV/FCF** (SBC-adjusted) vs. the company's own 5-yr history and 2–3 peers.
- **Normalized PEG** = forward P/E ÷ *sustainable* long-run EPS growth (not a one-time
  surge year). 1.0–1.5 = fair for a quality compounder; >2 needs high conviction.
- **EV/Sales vs. growth** for pre-profit names.

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
FAIR VALUE — [TICKER] ([Name]) · Technology (asset-light)
Current price: $X · As of [date]

WHY THIS MODEL: Value is intangible and current FCF reflects earning power → SBC-adjusted
FCF-DCF is appropriate. [If growth-stage/pre-profit, state the substitution.]

── DCF (per stock-dcf engine, SBC-adjusted) ──
Owner FCF base: $X.XB (Reported $X.XB − SBC $X.XB)   SBC/FCF: X%
             Bear     Moderate   Bull
Per share:   $XX      $XX        $XX     (vs price: −X% / ±X% / +X%)

── SANITY MULTIPLES ──
EV/FCF: Xx (5-yr avg Xx)   Rule of 40: XX   Normalized PEG: X.Xx

── HORIZON ──  Bear/Moderate/Bull above = intrinsic value TODAY (present value); price typically converges over ~2–3 yrs, thesis-dependent — NOT a 12-month target.
── FORWARD P/E & PEG ──  Fwd P/E: Xx · PEG (sustainable growth): X.Xx   [if distorted, substitute + say why: mid-cycle P/E (cyclical) / P/FFO (REIT) / EV-Sales (pre-profit) / adjusted fwd P/E (pharma)]
── EXTERNAL CROSSCHECK ──
Wall St consensus (12-mo target): $X (±X%) · [ratings]
Morningstar FVE (long-term intrinsic): $X (price/FVE X.Xx, N★) · moat [none/narrow/wide] · uncertainty [low–very high]
Seeking Alpha:     Quant [rating] · Valuation grade [A–F] · [author/WS PT $X]
Reconciliation:    [where my fair value sits vs. these anchors and why]

VERDICT: [under / fair / over]valued — [one line]
CAVEATS: [SBC/dilution drag, growth-stage reliability, key risk]
```
