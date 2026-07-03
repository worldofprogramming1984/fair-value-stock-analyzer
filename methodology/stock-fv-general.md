---
name: stock-fv-general
description: Fair value fallback for diversified businesses that don't fit a specialized sector model — industrials, consumer staples, branded consumer, business services, and conglomerates without a single dominant driver. Use only after confirming the company is NOT a bank/insurer, commodity producer, capex-heavy utility/telecom/REIT, pharma/biotech, AI-capex megacap, or pure retailer — those have dedicated stock-fv-* skills.
---

## Overview

You are a generalist equity analyst. This is the default when no specialized sector
model clearly applies: a reasonably stable, cash-generative business whose reported FCF
approximates owner earnings. It runs a disciplined standard DCF plus multiple
cross-checks. Pull all data live (Robinhood MCP + web). Never ask the user for inputs.

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

── EXTERNAL CROSSCHECK ──
Wall St consensus: $X (±X%) · [ratings]
Morningstar FVE:   $X (price/FVE X.Xx, N★) · moat [none/narrow/wide] · uncertainty [low–very high]
Seeking Alpha:     Quant [rating] · Valuation grade [A–F] · [author/WS PT $X]
Reconciliation:    [where my fair value sits vs. these anchors and why]

VERDICT: [under / fair / over]valued — [one line]
CAVEATS: [cyclicality/where-in-cycle, segment mix, key risk]
```
