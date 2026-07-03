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

Pull all data live (Robinhood MCP + web). Never ask the user for inputs.

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

── EXTERNAL CROSSCHECK ──
Wall St consensus: $X (±X%) · [ratings]
Morningstar FVE:   $X (price/FVE X.Xx, N★) · moat [none/narrow/wide] · uncertainty [low–very high]
Seeking Alpha:     Quant [rating] · Valuation grade [A–F] · [author/WS PT $X]
Reconciliation:    [where my fair value sits vs. these anchors and why]

VERDICT: [under / fair / over]valued — [one line]
CAVEATS: [interest-rate sensitivity; regulatory/rate-case risk; leverage; distribution safety]
```
