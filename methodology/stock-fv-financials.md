---
name: stock-fv-financials
description: Fair value for balance-sheet financial institutions — banks, thrifts, P&C and life insurers, capital-markets firms, and managed-care health insurers. Use whenever deposits, loans, reserves, float, or an investment portfolio ARE the business. A standard FCF-DCF is invalid here (deposits aren't debt, cash isn't idle, operating cash flow swings wildly on balance-sheet mechanics) — this skill uses P/B-vs-ROE, residual income, and dividend-discount instead.
---

## Overview

You are a financials-sector equity analyst. **Do not run an FCF-DCF on a bank or
insurer.** Their "free cash flow" is dominated by changes in trading assets, loans, and
deposits — it can swing hundreds of billions while net income is stable (JPM's FCF swung
−$147B↔+$107B on flat ~$50B net income). Deposits/float are the raw material of the
business, not financing layered on top, so WACC understates the discount rate, and the
"add cash back" DCF step is nonsense because reserves fund the deposit base.

Banks and insurers are valued on **book value, returns on that book, and distributions.**
Pull all data live (Robinhood MCP + web). Derive sensible defaults, but surface your key assumptions for confirmation before final numbers (see "Assumptions & confirmation").

## Step 1 — Gather data

- Robinhood `get_equity_quotes` / `get_equity_fundamentals`: price, shares, P/B, P/E,
  dividend, beta.
- Web: **book value per share (BVPS)** and **tangible BVPS**, **ROE** (and ROTCE),
  dividend payout + buyback pace, 5-yr book-value-per-share growth. Bank: **CET1 ratio**,
  net interest margin, provision for credit losses, efficiency ratio. Insurer:
  **combined ratio** (P&C), embedded value (life), investment yield. Managed care:
  **medical loss ratio (MLR)**, membership growth.
- Web: 10-yr Treasury (risk-free rate).

## Step 2 — Cost of equity (NOT WACC)

```
Adjusted Beta = 0.67 × Raw Beta + 0.33
Cost of Equity (CoE) = Risk-free Rate + Adjusted Beta × 5.5%
```
Use CoE as the discount rate throughout. Never build a WACC — bank "debt" is operating
funding, not a capital-structure choice.

## Step 3 — Primary model: Justified P/B from ROE

The cleanest bank/insurer valuation. Sustainable growth `g` should be conservative for a
mature institution (GDP-plus, ~4–6%), and must be below CoE.

```
Justified P/B = (ROE − g) / (CoE − g)
Fair Value per share = Justified P/B × BVPS
```

Run 3 scenarios by flexing ROE (through-cycle low / normalized / high) and g:
- **Bear:** trough-ish ROE, g = 3%, CoE + 1%
- **Moderate:** normalized ROE, g = 4–5%, base CoE
- **Bull:** peak ROE, g = 5–6%, CoE − 0.5%

Sanity: if `ROE × (1 − payout) > CoE`, the naive g is unsustainable — the firm can't
retain-and-grow at a return above its cost of equity forever; cap g and note it (this is
why high-ROE banks still trade at ~2–3× book, not 5×).

## Step 4 — Cross-check: Residual Income (Excess Returns) model

```
Value per share = BVPS + Σ PV[ (ROE_t − CoE) × BVPS_t ]  (10 yrs, then terminal)
```
Book grows at `BVPS_t × (1 − payout ratio)`. Discount the excess-return stream at CoE.
This should broadly agree with the justified-P/B answer; explain any gap.

## Step 5 — Cross-check: Dividend Discount Model

For dividend-heavy names, a two-stage DDM on the payout stream. Useful for insurers and
mature megabanks; less so for buyback-heavy names (capture buybacks via total payout).

## Step 6 — Sector sanity multiples

- **P/B vs. ROE** (the master chart — high-ROE deserves high P/B).
- **P/TBV** (tangible book — strips goodwill from acquisitive banks).
- **P/E** vs. peers; **dividend + buyback yield**.
- Bank health: CET1 vs. requirement. Insurer: combined ratio (<100 = underwriting
  profit). Managed care: MLR trend.

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
FAIR VALUE — [TICKER] ([Name]) · Financials (balance-sheet)
Current price: $X · As of [date]

WHY THIS MODEL: Deposits/float ARE the business and FCF is meaningless here → valued on
book value, ROE, and distributions. FCF-DCF deliberately NOT used (explain the swing).

── INPUTS ──  BVPS $X · TBVPS $X · ROE X% · CoE X% · payout X% · [CET1/combined/MLR]

── JUSTIFIED P/B ──
             Bear     Moderate   Bull
ROE / g:     X%/X%    X%/X%      X%/X%
Justified PB: X.Xx    X.Xx       X.Xx
Per share:   $XX      $XX        $XX     (vs price: −X% / ±X% / +X%)

── CROSSCHECKS ──  Residual income $XX · DDM $XX · current P/B X.Xx vs justified X.Xx

── EXTERNAL CROSSCHECK ──
Wall St consensus: $X (±X%) · [ratings]
Morningstar FVE:   $X (price/FVE X.Xx, N★) · moat [none/narrow/wide] · uncertainty [low–very high]
Seeking Alpha:     Quant [rating] · Valuation grade [A–F] · [author/WS PT $X]
Reconciliation:    [where my fair value sits vs. these anchors and why]

VERDICT: [under / fair / over]valued — [one line]
CAVEATS: [credit cycle / rate sensitivity / reserve adequacy / regulatory capital]
```
