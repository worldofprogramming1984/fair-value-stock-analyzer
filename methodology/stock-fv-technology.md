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

Pull all data live (Robinhood MCP + web search). Never ask the user for inputs. Show
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

── EXTERNAL CROSSCHECK ──
Wall St consensus: $X (±X%) · [ratings]
Morningstar FVE:   $X (price/FVE X.Xx, N★) · moat [none/narrow/wide] · uncertainty [low–very high]
Seeking Alpha:     Quant [rating] · Valuation grade [A–F] · [author/WS PT $X]
Reconciliation:    [where my fair value sits vs. these anchors and why]

VERDICT: [under / fair / over]valued — [one line]
CAVEATS: [SBC/dilution drag, growth-stage reliability, key risk]
```
