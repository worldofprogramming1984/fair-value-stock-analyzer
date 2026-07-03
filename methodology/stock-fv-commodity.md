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

Pull all data live (Robinhood MCP + web). Never ask the user for inputs.

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

── EXTERNAL CROSSCHECK ──
Wall St consensus: $X (±X%) · [ratings]
Morningstar FVE:   $X (price/FVE X.Xx, N★) · moat [none/narrow/wide] · uncertainty [low–very high]
Seeking Alpha:     Quant [rating] · Valuation grade [A–F] · [author/WS PT $X]
Reconciliation:    [where my fair value sits vs. these anchors and why]

VERDICT: [under / fair / over]valued — [one line, note cycle timing risk]
CAVEATS: [commodity price is the swing factor; reserve depletion; capital discipline; ESG/regulatory]
```
