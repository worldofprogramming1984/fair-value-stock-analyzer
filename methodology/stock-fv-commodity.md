---
name: stock-fv-commodity
description: Fair value for commodity and cyclical price-taker businesses — oil & gas E&P, integrated energy, metals & mining, materials, chemicals, steel, and paper. Use when earnings are driven by a commodity price the company does not control, so point-in-time FCF (peak or trough of the cycle) is misleading. This skill normalizes to mid-cycle economics and cross-checks against asset/reserve value (NAV).
---

## Overview

You are a natural-resources equity analyst. The defining error in this sector is valuing
a cyclical off a single year: at the top of the cycle trailing FCF looks huge and the
stock looks cheap right before earnings collapse; at the bottom it looks expensive right
before they recover. **Normalize to mid-cycle** and anchor on **asset value (NAV)**,
because at cycle lows these stocks trade on book/replacement value, not earnings.

Pull all data live (Robinhood MCP + web). Derive sensible defaults, but surface your key assumptions for confirmation before final numbers (see "Assumptions & confirmation").

## Step 1 — Gather data

- Robinhood: price, shares, market cap, beta, P/B, dividend.
- Web, last 5–7 yrs (a full cycle): revenue, operating margin, FCF, the relevant
  **commodity price** history. Production volumes. **Reserves** (proven/2P for E&P;
  mineral reserves & mine life for miners). **All-in sustaining cost (AISC)** for miners
  or breakeven for E&P. Net debt. Decommissioning/reclamation liabilities.
- Web: a normalized/mid-cycle commodity price deck (analyst long-run assumption). 10-yr Treasury.

## Step 2 — Normalize to mid-cycle

```
Mid-cycle margin = average operating/FCF margin across the full cycle (5–7 yrs)
Normalized FCF = Mid-cycle margin × current-production revenue at a NORMALIZED price deck
```
Never extrapolate the latest year. State explicitly where in the cycle we are now
(price vs. 5-yr range) and what normalized price you used.

## Step 3 — Primary model: mid-cycle DCF (low terminal growth)

Run the **`stock-dcf`** engine off the *normalized* FCF base, with two commodity overrides:
- **Terminal growth ≈ 0–1%.** A price-taker has no pricing power; long-run real growth
  is volume-limited and often flat-to-declining (depleting reserves).
- **Higher discount rate** — add a cyclicality/commodity-risk premium to WACC.
Run Bear/Moderate/Bull by flexing the **normalized commodity price**, not just growth.

## Step 4 — Cross-check: Net Asset Value (NAV)

For E&P and miners this is often the primary anchor:
```
NAV = PV of production from proven+probable reserves at the normalized price deck
      − development capex − decommissioning − net debt
NAV per share = NAV / shares
```
Report P/NAV. Historically these trade 0.8–1.2× NAV; below ~0.8× is a value signal, above
~1.2× prices in exploration upside or higher prices.

## Step 5 — Sector sanity multiples

- **P/B vs. mid-cycle ROE** (at cycle lows the floor is book/replacement value).
- **EV/EBITDA at mid-cycle prices** (not trailing).
- **Dividend + buyback yield** and payout sustainability at the normalized price.
- Miners: **AISC vs. spot** (margin per unit) and **reserve life** (years).

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
- **Pre-profit / unprofitable growth:** P/E and PEG are undefined — use **P/S** (and EV/Sales) + **P/S-to-growth** (the PEG analog); route to `stock-fv-unprofitable-growth`.
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
FAIR VALUE — [TICKER] ([Name]) · Commodity / cyclical price-taker
Current price: $X · As of [date]

WHY THIS MODEL: Earnings driven by an uncontrolled commodity price → point-in-time FCF
misleads. Normalized to mid-cycle + anchored on NAV. Cycle position: [price vs range].

── NORMALIZATION ──  Mid-cycle margin X% · normalized price $X · normalized FCF $X.XB

── VALUATION ──
Mid-cycle DCF per share (flex on price):  Bear $XX · Mod $XX · Bull $XX
NAV per share: $XX   → P/NAV X.Xx
             (vs price: −X% / ±X% / +X%)

── SANITY ──  P/B X.Xx vs mid-cycle ROE X% · EV/EBITDA(mid) Xx · yield X% · [AISC/reserve life]

── HORIZON ──  Bear/Moderate/Bull above = intrinsic value TODAY (present value); price typically converges over ~2–3 yrs, thesis-dependent — NOT a 12-month target.
── FORWARD P/E & PEG ──  Fwd P/E: Xx · PEG (sustainable growth): X.Xx   [if distorted, substitute + say why: mid-cycle P/E (cyclical) / P/FFO (REIT) / EV-Sales (pre-profit) / adjusted fwd P/E (pharma)]
── EXTERNAL CROSSCHECK ──
Wall St consensus (12-mo target): $X (±X%) · [ratings]
Morningstar FVE (long-term intrinsic): $X (price/FVE X.Xx, N★) · moat [none/narrow/wide] · uncertainty [low–very high]
Seeking Alpha:     Quant [rating] · Valuation grade [A–F] · [author/WS PT $X]
Reconciliation:    [where my fair value sits vs. these anchors and why]

VERDICT: [under / fair / over]valued — [one line, note cycle timing risk]
CAVEATS: [commodity price is the swing factor; reserve depletion; capital discipline; ESG/regulatory]
```
