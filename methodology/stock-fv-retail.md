---
name: stock-fv-retail
description: Fair value for retailers — warehouse/big-box compounders (Costco, Walmart, Target), e-commerce and marketplaces (Amazon retail, MercadoLibre), and specialty/discretionary chains (TJX, Home Depot). Use for businesses that sell physical goods through stores or online. Capitalizes operating leases into enterprise value, values on unit economics and same-store sales, and runs sum-of-the-parts for mixed retail+cloud+ads companies like Amazon.
---

## Overview

You are a retail/consumer analyst. Retail is a thin-margin, high-volume business, so
small margin changes swing valuation hard and **operating leases must be capitalized into
enterprise value** (a retailer's store leases are debt in all but name). The value driver
is unit economics: new-store returns, same-store (comparable) sales growth, and — for
warehouse clubs — membership fees. For mixed companies (Amazon), the consolidated numbers
hide everything; use sum-of-the-parts.

Pull all data live (Robinhood MCP + web). Derive sensible defaults, but surface your key assumptions for confirmation before final numbers (see "Assumptions & confirmation").

## Step 1 — Identify the sub-type

- **Quality compounder / warehouse / big-box** (COST, WMT, TJX, HD): stable, unit-economics
  driven → Step 2.
- **E-commerce / marketplace, mixed model** (AMZN, MELI): consolidated FCF is misleading →
  Step 3 (SOTP).
- **Specialty / discretionary / turnaround** (cyclical, fashion-risk): → Step 2 with a
  cyclical-margin caveat and lower multiple.

## Step 2 — Compounder: unit-economics DCF, lease-adjusted

- **Capitalize operating leases** into EV and net debt (present value of lease
  obligations). A lease-unadjusted EV/EBIT understates leverage.
- **Unit economics:** new-store ROIC, store count growth runway, **same-store sales (comps)**
  and **sales per square foot**. For **Costco**, model **membership fee income**
  separately — it's high-margin, recurring, and a huge share of operating profit; the
  retail margin is thin by design.
- **Primary:** run the **`stock-dcf`** engine on SBC-adjusted FCF, growth anchored to
  (unit growth + comps + modest margin change). WACC (lease-adjusted).
- Sanity: **EV/EBIT** and **EV/EBITDAR** (lease-adjusted), P/E vs. own history, comps trend.
  Low-margin retail is very EV/EBIT-sensitive — a small margin miss is a big value hit.

## Step 3 — E-commerce / mixed: sum-of-the-parts

Consolidated FCF blends a low-margin retail engine with high-value segments. Value each:
- **Retail/marketplace segment:** value on a normalized retail operating margin, or
  EV/GMV vs. peers.
- **Cloud segment (AWS):** the real profit engine — value via `stock-fv-ai-capex` or a
  high-margin DCF/EV-EBITDA. Often most of the equity value.
- **Advertising segment:** high-margin, tech-like multiple.
- Sum segment values + net cash → equity value → per share. State each segment's share of
  total value (this is the whole point — e.g., AWS+ads often > the entire retail business).

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

## Output format

```
FAIR VALUE — [TICKER] ([Name]) · Retail [compounder | e-commerce SOTP | specialty]
Current price: $X · As of [date]

WHY THIS MODEL: Thin-margin physical-goods business; leases capitalized into EV; valued
on unit economics [+ membership] OR sum-of-the-parts for mixed retail/cloud/ads.

── COMPOUNDER: comps X% · unit growth X% · [membership income $X.XB] · lease-adj EV $XB
── SOTP: Retail $XX + Cloud $XX + Ads $XX + net cash $X  (segment % of value: R X% / C X% / A X%)

── VALUATION ──
Per share:  Bear $XX · Moderate $XX · Bull $XX   (vs price: −X% / ±X% / +X%)

── SANITY ──  EV/EBIT(lease-adj) Xx · EV/EBITDAR Xx · P/E Xx · comps X%

── EXTERNAL CROSSCHECK ──
Wall St consensus: $X (±X%) · [ratings]
Morningstar FVE:   $X (price/FVE X.Xx, N★) · moat [none/narrow/wide] · uncertainty [low–very high]
Seeking Alpha:     Quant [rating] · Valuation grade [A–F] · [author/WS PT $X]
Reconciliation:    [where my fair value sits vs. these anchors and why]

VERDICT: [under / fair / over]valued — [one line]
CAVEATS: [margin sensitivity; lease leverage; e-commerce competition; consumer cyclicality; SOTP segment assumptions]
```
