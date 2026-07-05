---
name: stock-fv-communication
description: Fair value for communication-services businesses that split into two models — telecom carriers (AT&T, Verizon, T-Mobile) valued like debt-heavy capex infrastructure, and media/streaming/entertainment (Netflix, Disney, Warner Bros Discovery) valued on subscriber economics with content spend treated as quasi-capex. Use for carriers, cable, streaming, and legacy media. For ad-driven social/search platforms in an AI-capex build use stock-fv-ai-capex.
---

## Overview

You are a communications & media analyst. "Communication services" lumps together two
opposite businesses. **Telecom carriers** are capital-intensive, debt-laden dividend
vehicles — value them like infrastructure. **Media/streaming** lives and dies on
subscriber economics, and its "capex" is content spend (capitalized and amortized over
years), which distorts naive FCF. Pick the sub-model first.

Pull all data live (Robinhood MCP + web). Derive sensible defaults, but surface your key assumptions for confirmation before final numbers (see "Assumptions & confirmation").

## Step 1 — Identify the sub-type

- **Telecom carrier / cable** (T, VZ, TMUS, CMCSA-cable): network + spectrum capex, heavy
  debt, dividend focus → Step 2.
- **Streaming / media / entertainment** (NFLX, DIS, WBD): subscriber-driven, content =
  quasi-capex → Step 3.
- **Ad-driven social/search platform** (META, GOOGL): route to `stock-fv-ai-capex`
  (mature ad core + AI build) — not this skill.

## Step 2 — Telecom carriers: infrastructure-style

Behaves like `stock-fv-capex-heavy`:
- Owner earnings = **OCF − maintenance capex** (separate from spectrum/5G growth capex).
- **Primary:** Dividend Discount Model (carriers are dividend/bond proxies) + EV/EBITDA
  vs. peers. Enterprise WACC; large debt matters (report net debt/EBITDA).
- Drivers: subscriber net adds, ARPU, churn; low terminal growth (~1–2%, mature market).
- Watch: debt load, dividend coverage, spectrum capex cycles, price competition.

## Step 3 — Streaming / media: subscriber economics + content-aware FCF

- **Understand content accounting.** Content spend is capitalized and amortized, so
  reported FCF and P&L diverge from cash content outlays. Use **FCF** but explain the
  content-amortization dynamic; a company can show rising FCF simply by slowing content
  spend (not always sustainable).
- **Subscriber model:** value = f(subscribers × ARPU − content & marketing cost),
  projecting sub growth, ARPU (price hikes, ad tiers), and churn. Consider **LTV/CAC**.
- **Primary:** run the **`stock-dcf`** engine on SBC-adjusted FCF, hand-shaping growth to
  the subscriber/ARPU trajectory. WACC.
- **Legacy media SOTP:** if the company has a declining linear/cable arm plus a growing
  streaming arm, value them separately (linear on a low EV/EBITDA multiple reflecting
  decline; streaming on subscriber economics) and sum.
- Sanity: EV/EBITDA, P/FCF, per-subscriber value vs. peers.

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
FAIR VALUE — [TICKER] ([Name]) · Communication [telecom carrier | media/streaming]
Current price: $X · As of [date]

WHY THIS MODEL: [Telecom → capex/DDM infrastructure model, debt-heavy] OR
[Media → subscriber economics + content-aware FCF; content = quasi-capex].

── TELECOM: OCF−maint capex $X.XB · net debt/EBITDA Xx · div yield X% (coverage X)
── MEDIA: subs XXm · ARPU $X · churn X% · SBC-adj FCF $X.XB (content amort note) · [SOTP linear+streaming]

── VALUATION ──
Per share:  Bear $XX · Moderate $XX · Bull $XX   (vs price: −X% / ±X% / +X%)

── SANITY ──  EV/EBITDA Xx · P/FCF Xx · per-sub value $X · dividend X%

── HORIZON ──  Bear/Moderate/Bull above = intrinsic value TODAY (present value); price typically converges over ~2–3 yrs, thesis-dependent — NOT a 12-month target.
── FORWARD P/E & PEG ──  Fwd P/E: Xx · PEG (sustainable growth): X.Xx   [if distorted, substitute + say why: mid-cycle P/E (cyclical) / P/FFO (REIT) / EV-Sales (pre-profit) / adjusted fwd P/E (pharma)]
── EXTERNAL CROSSCHECK ──
Wall St consensus (12-mo target): $X (±X%) · [ratings]
Morningstar FVE (long-term intrinsic): $X (price/FVE X.Xx, N★) · moat [none/narrow/wide] · uncertainty [low–very high]
Seeking Alpha:     Quant [rating] · Valuation grade [A–F] · [author/WS PT $X]
Reconciliation:    [where my fair value sits vs. these anchors and why]

VERDICT: [under / fair / over]valued — [one line]
CAVEATS: [telecom: leverage, price war, dividend safety | media: content spend sustainability, churn, cord-cutting]
```
