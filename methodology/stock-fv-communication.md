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

Pull all data live (Robinhood MCP + web). Never ask the user for inputs.

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

── EXTERNAL CROSSCHECK ──
Wall St consensus: $X (±X%) · [ratings]
Morningstar FVE:   $X (price/FVE X.Xx, N★) · moat [none/narrow/wide] · uncertainty [low–very high]
Seeking Alpha:     Quant [rating] · Valuation grade [A–F] · [author/WS PT $X]
Reconciliation:    [where my fair value sits vs. these anchors and why]

VERDICT: [under / fair / over]valued — [one line]
CAVEATS: [telecom: leverage, price war, dividend safety | media: content spend sustainability, churn, cord-cutting]
```
