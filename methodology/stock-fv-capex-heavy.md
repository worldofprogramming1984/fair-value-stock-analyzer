---
name: stock-fv-capex-heavy
description: Fair value for structurally capital-intensive businesses whose reported free cash flow is permanently depressed by heavy ongoing capex — regulated electric/gas/water utilities, railroads, midstream/pipeline (MLPs), and REITs. Use when large recurring capital investment is intrinsic to operations. Distinguishes maintenance capex from growth capex and uses rate-base, distributable-cash-flow, or FFO/NAV models as appropriate. NOT for temporary AI-datacenter capex (use stock-fv-ai-capex).
---

## Overview

You are an infrastructure/utilities analyst. These businesses spend heavily on capex
*every year, forever* — so reported FCF understates their economics, and the key move is
separating **maintenance capex** (recurring, deduct it) from **growth capex**
(discretionary investment that expands the asset base). Each sub-type has a purpose-built
model. These are largely income/dividend vehicles with real debt — discount at
enterprise WACC and use low, inflation-like terminal growth.

Pull all data live (Robinhood MCP + web). Derive sensible defaults, but surface your key assumptions for confirmation before final numbers (see "Assumptions & confirmation").

## Step 1 — Identify the sub-type, then use its model

### A. Regulated utility (electric/gas/water — NEE, DUK, SO)
Earnings are set by regulators: `allowed ROE × rate base`. Value is driven by **rate-base
growth**.
- Gather: rate base, allowed ROE, approved rate-base CAGR, dividend + growth rate, payout.
- **Primary: Dividend Discount Model** (2-stage) — utilities are bond-proxies; the
  dividend and its growth (≈ rate-base growth) drive return.
- **Cross-check:** `Justified P/B = (allowed ROE − g)/(CoE − g) × book`; and P/E vs. peers.
- Discount at cost of equity for the DDM; note interest-rate sensitivity (utilities fall
  when long rates rise).

### B. Railroad / capital-intensive industrial (UNP, CSX)
Durable pricing power despite heavy capex.
- **Primary:** run the **`stock-dcf`** engine on FCF = OCF − *maintenance* capex (not
  total), growing the maintenance-adjusted FCF. Enterprise WACC.
- **Key diagnostic: ROIC vs. WACC** — the whole thesis is compounding at returns above
  cost of capital. Report operating ratio (rail efficiency).
- Cross-check EV/EBITDA.

### C. REIT (O, PLD, AMT)
Never use EPS or FCF — depreciation is a huge non-cash charge that understates earnings.
- **Primary: FFO and AFFO** (Funds From Operations = net income + real-estate depreciation
  − gains on sales; AFFO subtracts recurring maintenance capex). Value on **P/FFO** and
  **P/AFFO** vs. peers, and a **dividend discount / AFFO-yield** model.
- **NAV cross-check:** `NAV = (stabilized NOI ÷ market cap rate) − net debt`. Report
  premium/discount to NAV.
- Watch: debt maturities, occupancy, cap-rate sensitivity.

### D. Midstream / pipeline / MLP (ET, EPD, KMI)
Toll-road cash flows, distribution-focused.
- **Primary:** DCF of **distributable cash flow (DCF/unit)**; value on distribution yield
  + coverage ratio and EV/EBITDA.
- Watch distribution coverage (>1.2× healthy) and leverage (net debt/EBITDA).

## Step 2 — Universal overrides for the sector

- **Maintenance vs. growth capex split is mandatory** — owner earnings deduct only
  maintenance capex; growth capex is investment to be judged on its return.
- **Terminal growth ≈ inflation (2%)** — these grow with GDP/rate base, not faster.
- **Debt is real and large** — use enterprise-level analysis; report net debt/EBITDA.

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
FAIR VALUE — [TICKER] ([Name]) · Capex-heavy [utility / railroad / REIT / midstream]
Current price: $X · As of [date]

WHY THIS MODEL: Heavy permanent capex depresses reported FCF → [rate-base / maintenance-
capex FCF / FFO-AFFO / distributable-cash] model used. Maintenance vs growth capex split.

── INPUTS ──  [rate base & allowed ROE | FFO/AFFO per share | DCF/unit & coverage] · net debt/EBITDA Xx

── VALUATION ──
Primary model per share:  Bear $XX · Moderate $XX · Bull $XX   (vs price: −X% / ±X% / +X%)
Cross-check: [P/FFO Xx | NAV $XX, P/NAV X.Xx | justified P/B X.Xx | EV/EBITDA Xx]

── SANITY ──  Dividend yield X% (payout/coverage X) · [operating ratio / occupancy / MLR]

── HORIZON ──  Bear/Moderate/Bull above = intrinsic value TODAY (present value); price typically converges over ~2–3 yrs, thesis-dependent — NOT a 12-month target.
── FORWARD P/E & PEG ──  Fwd P/E: Xx · PEG (sustainable growth): X.Xx   [if distorted, substitute + say why: mid-cycle P/E (cyclical) / P/FFO (REIT) / EV-Sales (pre-profit) / adjusted fwd P/E (pharma)]
── EXTERNAL CROSSCHECK ──
Wall St consensus (12-mo target): $X (±X%) · [ratings]
Morningstar FVE (long-term intrinsic): $X (price/FVE X.Xx, N★) · moat [none/narrow/wide] · uncertainty [low–very high]
Seeking Alpha:     Quant [rating] · Valuation grade [A–F] · [author/WS PT $X]
Reconciliation:    [where my fair value sits vs. these anchors and why]

VERDICT: [under / fair / over]valued — [one line]
CAVEATS: [interest-rate sensitivity; regulatory/rate-case risk; leverage; distribution safety]
```
