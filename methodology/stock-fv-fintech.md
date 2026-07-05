---
name: stock-fv-fintech
description: Fair value for fintech businesses, which split into two very different models. Payment networks and processors (Visa, Mastercard, Fiserv, PayPal) are asset-light toll-booths valued like technology. Balance-sheet lenders and BNPL (SoFi, Affirm, Ally) carry credit risk on their own book and are valued like financials. Use for any payments, digital-banking, or lending-technology company; this skill picks the right sub-model.
---

## Overview

You are a fintech analyst. The single most important question is: **does this company
lend its own money (credit risk on balance sheet) or just move other people's money
(fee/take-rate)?** The answer flips the entire valuation approach. Networks are among the
best businesses in the world (toll-booth economics, tiny capex); lenders are banks
wearing a tech logo and must be valued on book value and credit.

Pull all data live (Robinhood MCP + web). Derive sensible defaults, but surface your key assumptions for confirmation before final numbers (see "Assumptions & confirmation").

## Step 1 — Classify the fintech sub-type

- **Payment network / processor** (V, MA, FISV, GPN, PYPL, ADYEN): revenue = take-rate ×
  payment volume; negligible credit risk; asset-light → Step 2.
- **Balance-sheet lender / BNPL / neobank** (SOFI, AFRM, ALLY, LC): originates loans, holds
  credit risk, reserves for losses → Step 3.
- *Hybrid* (e.g., a payments company with a growing lending book): value the segments
  separately and sum.

## Step 2 — Networks/processors: technology-style DCF

Value like an asset-light compounder driven by volume:
- **Revenue driver:** take-rate × total payment volume (TPV/GDV) growth. Project TPV
  growth (secular cash→digital shift) and any take-rate change.
- Run the **`stock-dcf`** engine on **SBC-adjusted FCF** (fintech pays heavy stock comp —
  always deduct; check dilution). WACC discount rate; add back net cash.
- Sanity: **EV/FCF**, **normalized PEG**, EV/Sales, and operating margin (networks run
  50%+ margins; processors lower).
- Watch: disintermediation risk (real-time payments, stablecoins, regulation of
  interchange).

## Step 3 — Balance-sheet lenders: financials-style

Treat like a bank/specialty-finance (see `stock-fv-financials` mechanics):
- **Cost of equity, not WACC.** Deposits/funding are operating inputs.
- **Primary:** once profitable, **Justified P/B = (ROE − g)/(CoE − g) × book**, and/or P/E.
  Watch **book value growth**, **net charge-offs**, **loan-loss reserve adequacy**, and
  funding mix (deposits vs. warehouse lines).
- If pre-profit/hyper-growth: value on revenue × target mature margin discounted back, or
  P/B with a path-to-normalized-ROE narrative. Heavy SBC → model dilution explicitly.
- Sanity: **P/B vs. ROE**, P/E when profitable, tangible book.
- Credit risk is the swing factor — stress the charge-off rate in the bear case.

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

## Output format

```
FAIR VALUE — [TICKER] ([Name]) · Fintech [network/processor | balance-sheet lender]
Current price: $X · As of [date]

WHY THIS MODEL: [Take-rate × volume, asset-light → tech-style SBC-adjusted DCF] OR
[carries credit risk on balance sheet → financials-style P/B-ROE, cost of equity].

── NETWORK: TPV $XT growing X% · take-rate X% · SBC-adj FCF $X.XB · op margin X%
── LENDER: BVPS $X · ROE X% · net charge-offs X% · reserve coverage Xx · CoE X%

── VALUATION ──
Per share:  Bear $XX · Moderate $XX · Bull $XX   (vs price: −X% / ±X% / +X%)

── SANITY ──  [EV/FCF Xx · PEG X.Xx] OR [P/B X.Xx vs ROE X% · P/E Xx]

── FORWARD P/E & PEG ──  Fwd P/E: Xx · PEG (sustainable growth): X.Xx   [if distorted, substitute + say why: mid-cycle P/E (cyclical) / P/FFO (REIT) / EV-Sales (pre-profit) / adjusted fwd P/E (pharma)]
── EXTERNAL CROSSCHECK ──
Wall St consensus: $X (±X%) · [ratings]
Morningstar FVE:   $X (price/FVE X.Xx, N★) · moat [none/narrow/wide] · uncertainty [low–very high]
Seeking Alpha:     Quant [rating] · Valuation grade [A–F] · [author/WS PT $X]
Reconciliation:    [where my fair value sits vs. these anchors and why]

VERDICT: [under / fair / over]valued — [one line]
CAVEATS: [networks: disintermediation/interchange regulation, SBC dilution | lenders: credit cycle, funding, dilution]
```
