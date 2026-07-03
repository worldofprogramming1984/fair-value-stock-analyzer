---
name: stock-dcf
description: Calculate the intrinsic value of a stock using a 3-scenario DCF (Discounted Cash Flow) model — Bear, Moderate, and Bull cases. Use this skill when the user asks for intrinsic value, DCF valuation, fair value estimate, or "what is this stock worth". Works for any public company ticker. Always pulls live data automatically; no manual inputs required.
---

## Overview

You are a quantitative equity analyst. When asked for a DCF valuation of any stock, execute the following steps exactly in order. Pull all data automatically — never ask the user for inputs. Always state your assumptions explicitly so the user understands the basis for each number.

---

## Step 1: Gather Data

Collect the following data points using Robinhood MCP and web search. Search for each item specifically; do not guess.

### From Robinhood MCP
- `get_equity_quotes`: Current stock price, market cap
- `get_equity_fundamentals`: Beta (raw), shares outstanding, PE ratio, dividend yield

### From Web Search (search "[TICKER] free cash flow history site:macrotrends.net" or similar)
Collect for the last 5 fiscal years (or as many as available):
- **Free Cash Flow** (Operating Cash Flow − CapEx) for each year
- **Stock-Based Compensation (SBC)** for each year — search "[TICKER] stock based compensation annual"
- **Total Revenue** for each year
- **Total Debt** (most recent, long-term)
- **Operating Lease Liabilities** (most recent) — if material (>5% of market cap), include in total debt
- **Cash & Cash Equivalents + Short-Term Investments** — use the **most recently reported quarter**, not the annual figure
- **Interest Expense** (TTM, for cost of debt)
- **Effective Tax Rate** (TTM) — normalize if an obvious one-time item distorts it
- **Shares Outstanding** (diluted, most recent)
- **Most recent quarterly FCF** — needed for the staleness check in Step 2B
- **Analyst consensus FCF for the current fiscal year** (if available — search "[TICKER] free cash flow estimate consensus [year]")
- **Company guidance** — search "[TICKER] revenue guidance [year] [year+1]" to capture any forward outlook

### From Web Search (search "10 year treasury yield today")
- **Risk-free rate**: Current 10-year US Treasury yield (as a decimal, e.g., 0.0439)

---

## Step 2: Compute Normalized FCF and Growth Rate

This step replaces raw TTM FCF with an economically defensible base. TTM FCF is a poor starting point whenever a company is in a capex cycle, restructuring, acquisition integration, or AI-era inflection — which can make the historical base severely stale.

### 2A — Compute SBC-Adjusted FCF (True Owner Earnings)

```
SBC-Adjusted FCF = Reported FCF − SBC
```

SBC is a real economic cost (shareholder dilution) that FCF calculations add back as a non-cash item. Always deduct it to get true owner earnings. Report both numbers.

Compute SBC-Adjusted FCF for each of the last 5 years.

> **One-time SBC distortion:** If SBC spikes dramatically in a single year (e.g., due to acquisition RSU vesting), note it explicitly. The spike suppresses that year's SBC-adjusted FCF below normal earning power. Flag it and consider whether to include it in the normalization or exclude it.

### 2B — Normalize the FCF Base

**Step 1:** Identify the last 3 years where SBC-Adjusted FCF was positive (call them the "normal years").

**Step 2:** Calculate the FCF margin for each normal year:
```
FCF Margin (yr) = SBC-Adjusted FCF (yr) / Total Revenue (yr)
```

**Step 3:** Average those margins:
```
Normalized FCF Margin = avg(FCF Margin over normal years)
```

**Step 4:** Apply to current trailing revenue:
```
Historical Normalized FCF Base = Normalized FCF Margin × Trailing 12-Month Revenue
```

**Step 5 — Staleness Check (Critical for high-growth or inflection companies):**

Before using the historical normalized base, check whether it is stale:

```
Annualized Recent Quarterly FCF = Most Recent Quarter FCF × 4
Staleness Ratio = Annualized Recent Quarterly FCF / Historical Normalized FCF Base
```

- If Staleness Ratio > 1.5 (i.e., current run-rate is >50% above historical base), the base is stale.
- If analyst consensus FCF for the current fiscal year is available and >30% above the historical base, the base is stale.

**When the base is stale — use the Forward FCF Base instead:**
```
Forward FCF Base = analyst consensus FCF for current fiscal year
                   (or annualized recent quarterly FCF if consensus unavailable)
```

State clearly which base was used and why. The Forward FCF Base captures the current business reality; the historical base captures the pre-inflection business. For AI-era companies, hypergrowth periods, or post-acquisition integrations, the forward base is almost always more appropriate.

> **Example from practice (AVGO 2026):** Historical normalized base = $21.8B. Analyst FY2026 consensus FCF = $49.9B. Staleness ratio = 2.29x. Forward base used. Growth rates applied from $49.9B forward, not $21.8B.

> **When to flag a normalization caveat:** If TTM FCF deviates more than 50% below the Normalized FCF Base (in the other direction — current earnings are depressed), state explicitly: "TTM FCF is depressed by [X] — likely [capex surge / restructuring]. The normalized base of $X.XB reflects the business's earning power under normal investment conditions."

> **Exception:** If the company has never had 3 positive SBC-Adjusted FCF years (early-stage, deep loss), fall back to revenue-based projection: use revenue CAGR as the growth rate and apply a target FCF margin (analyst consensus or industry average). State this clearly.

### 2C — Calculate Growth Rate

**Step 1 — Historical FCF CAGR (baseline calculation):**

Use 3-year averages at both endpoints to reduce endpoint sensitivity:
```
Recent Avg FCF   = avg(SBC-Adjusted FCF for the 3 most recent positive years)
Oldest Avg FCF   = avg(SBC-Adjusted FCF for the 3 oldest available positive years)
Years Between    = midpoint of recent years − midpoint of oldest years
FCF CAGR         = (Recent Avg FCF / Oldest Avg FCF)^(1 / Years Between) − 1
```

**Step 2 — Revenue CAGR (always calculate as a cross-check):**
```
Recent Avg Revenue = avg(Revenue, last 3 years)
Oldest Avg Revenue = avg(Revenue, oldest 3 available years)
Revenue CAGR       = (Recent Avg Revenue / Oldest Avg Revenue)^(1 / years) − 1
```

**Step 3 — Forward Growth Check (new — critical for inflection companies):**

Search for:
- Company guidance: "[TICKER] revenue guidance fiscal [year] [year+1]"
- Analyst consensus revenue growth for next 2–3 years

If company guidance or analyst consensus implies growth materially above historical CAGR (>1.5× difference), flag the inflection explicitly:

> "Historical FCF CAGR of X% is backward-looking and predates the [AI / cloud / restructuring] inflection. Management guidance implies Y% growth. Consider using forward-looking rates anchored to guidance."

**Step 4 — Which growth rate to use:**

| Situation | Growth Rate to Use |
|---|---|
| Historical CAGR available, no major inflection | FCF CAGR (if < 2× revenue CAGR) else Revenue CAGR |
| FCF CAGR unavailable, negative, or > 2× revenue CAGR | Revenue CAGR |
| Forward FCF Base used (staleness ratio > 1.5x) | Forward-looking rates anchored to guidance/consensus |
| Company in AI supercycle, management gives explicit guidance | Guidance-anchored rates (Bear = low end, Moderate = midpoint, Bull = above guidance) |

Always state which was used and why.

---

## Step 3: Calculate Base WACC

### Beta: Apply Blume Mean-Reversion Adjustment

Raw trailing beta overstates risk for long-horizon valuation because betas empirically mean-revert toward 1.0 over time. Apply the Blume adjustment:

```
Adjusted Beta = 0.67 × Raw Beta + 0.33 × 1.0
```

Use Adjusted Beta in all WACC calculations. Report both the raw and adjusted beta.

### Cost of Equity (CAPM):
```
Market Risk Premium = 5.5% (Damodaran long-run average — fixed)
Cost of Equity = Risk-free Rate + Adjusted Beta × Market Risk Premium
```

### Cost of Debt:
```
Cost of Debt (pre-tax) = Interest Expense / Total Debt
If Interest Expense unavailable or Total Debt ≈ 0: use Cost of Debt = Risk-free Rate + 1%
Clamp to [1%, 20%] as a sanity check
```

### Effective Tax Rate:
```
Use the normalized effective tax rate (3-year average or stated normalized rate).
Do not use a single anomalous year — deferred tax provisions from acquisitions can
temporarily spike the rate (e.g., VMware integration pushed AVGO's FY2024 rate to 37.8%
vs a normalized 5–8%). Explain any normalization applied.
```

### Capital Structure:
```
Equity Value  = Current Market Cap
Debt Value    = Total Long-Term Debt + Operating Lease Liabilities (if material)
Total Capital = Equity Value + Debt Value
E/V = Equity Value / Total Capital
D/V = Debt Value  / Total Capital
```

### WACC:
```
WACC = (E/V × Cost of Equity) + (D/V × Cost of Debt × (1 − Effective Tax Rate))
```

---

## Step 4: Define the 3 Scenarios

### Growth Rates

**If using historical FCF CAGR as the base:**

| Scenario | Phase 1 Growth (Yr 1–5) | Phase 2 Growth (Yr 6–10) |
|---|---|---|
| Bear | 50% of base CAGR (floor: 0%) | Linear fade from Phase 1 → Terminal Growth |
| Moderate | Base CAGR (cap: 30%) | Linear fade from Phase 1 → Terminal Growth |
| Bull | 150% of base CAGR (cap: 35%) | Linear fade from Phase 1 → Terminal Growth |

**If using forward-looking rates (guidance/consensus anchored):**

Anchor to company guidance range. Set:
- Bear = below guidance low end (skeptical execution)
- Moderate = midpoint of guidance range
- Bull = above guidance high end (beats + margin expansion)

Example (AVGO FY2026 — guidance 20–25% AI FCF growth):
- Bear: 15% | Moderate: 22% | Bull: 30%

**Special case — high-growth companies (base CAGR > 30%):**
- Bear: 10%
- Moderate: 25% (regression to mean)
- Bull: 35%

**Special case — declining or insufficient FCF CAGR:**
- Bear: 0% (flat)
- Moderate: Revenue CAGR / 2
- Bull: Revenue CAGR
- Flag explicitly as limited-visibility situation

**Phase 2 — Linear Fade:**

In years 6–10, growth declines linearly each year from the Phase 1 rate down to the scenario's terminal growth rate:
```
Growth(yr t) = Phase1_Rate + (Terminal_Rate − Phase1_Rate) × (t − 5) / 5
  where t ∈ {6, 7, 8, 9, 10}
```

This produces a smooth deceleration instead of a step-function cliff at year 5.

### WACC Adjustments

| Scenario | WACC |
|---|---|
| Bear | Base WACC + 2.0% |
| Moderate | Base WACC |
| Bull | Base WACC − 1.0% |

### Terminal Growth Rate

Terminal growth must not exceed long-run nominal GDP and must stay at least 150 bps below the risk-free rate:

```
Max Terminal Growth = min(2.5%, Risk-free Rate − 1.5%)
```

| Scenario | Terminal Growth Rate |
|---|---|
| Bear | 1.5% |
| Moderate | min(2.0%, Max Terminal Growth) |
| Bull | min(2.5%, Max Terminal Growth) |

---

## Step 5: Run the DCF for Each Scenario

### Project FCF over 10 Years

Start from the FCF Base determined in Step 2B (historical normalized or forward):

```
FCF_yr1 = FCF Base × (1 + Phase1_Growth)
FCF_yr2 = FCF_yr1 × (1 + Phase1_Growth)
...
FCF_yr5 = FCF_yr4 × (1 + Phase1_Growth)

# Phase 2: linear fade
FCF_yr6  = FCF_yr5  × (1 + Phase1_Growth + (TGR − Phase1_Growth) × 1/5)
FCF_yr7  = FCF_yr6  × (1 + Phase1_Growth + (TGR − Phase1_Growth) × 2/5)
FCF_yr8  = FCF_yr7  × (1 + Phase1_Growth + (TGR − Phase1_Growth) × 3/5)
FCF_yr9  = FCF_yr8  × (1 + Phase1_Growth + (TGR − Phase1_Growth) × 4/5)
FCF_yr10 = FCF_yr9  × (1 + TGR)
```

### Discount Each Year to Present Value:
```
PV(FCF_t) = FCF_t / (1 + WACC)^t
```

### Terminal Value (Gordon Growth Model):
```
Terminal Value     = FCF_yr10 × (1 + Terminal_Growth) / (WACC − Terminal_Growth)
PV(Terminal Value) = Terminal Value / (1 + WACC)^10
```

### Enterprise Value → Equity Value → Per Share:
```
Enterprise Value = Σ PV(FCF yr 1–10) + PV(Terminal Value)
Equity Value     = Enterprise Value + Total Cash − Total Debt
Intrinsic Value Per Share = Equity Value / Diluted Shares Outstanding
```

Use the **most recently reported quarter** cash figure — not the annual report figure. Cash changes quickly in FCF-heavy companies.

### Margin of Safety:
```
Margin of Safety = (Intrinsic Value Per Share − Current Price) / Current Price × 100%
Positive → stock trades below intrinsic value (undervalued)
Negative → stock trades above intrinsic value (overvalued)
```

---

## Step 6: Identify Key Value Driver

After running all 3 scenarios, perform a sensitivity on each of the three main levers:

- **FCF growth rate**: How much does intrinsic value change if Phase 1 growth is ±1%?
- **WACC**: How much does intrinsic value change if WACC is ±1%?
- **Terminal growth rate**: How much does intrinsic value change if TGR is ±0.5%?

The lever with the largest per-share impact is the key value driver. State it and give the $/share sensitivity.

> **From practice:** For large-cap tech with high market caps, WACC is almost always the dominant driver (~$50+/share per 1% change), often 3× more impactful than the FCF growth rate. This is because a 1% WACC change affects the discount on every future year and the terminal value. Always highlight this — investors often obsess over growth rate but WACC sensitivity is what moves the needle most.

---

## Step 7: PEG Ratio (New — Derived Alongside DCF)

After completing the DCF, always compute the PEG ratio as a complementary sanity check.

```
Trailing EPS      = Current Price / Trailing P/E
Forward P/E       = Current Price / Next-Year Consensus EPS
FY+1 EPS Growth   = (Next-Year EPS / Trailing EPS) − 1

Trailing PEG      = Trailing P/E / FY+1 EPS Growth Rate (as %)
Forward PEG       = Forward P/E / FY+1 EPS Growth Rate (as %)
Normalized PEG    = Forward P/E / Sustainable Long-Run EPS Growth Rate (as %)
```

**Which PEG to emphasize:**
- Trailing PEG: Often misleading for companies mid-inflection (pre-AI-surge P/E is too high)
- Forward PEG: Distorted if the FY+1 growth rate is a one-time step-change (e.g., 94% post-AI inflection year)
- **Normalized PEG**: Most honest — use sustainable long-run growth rate (analyst 3–5 year CAGR consensus), not the surge year

**Interpretation:**
- PEG < 1.0: Potentially undervalued (Lynch rule)
- PEG 1.0–1.5: Fairly valued for high-quality compounder
- PEG > 2.0: Premium — requires high conviction in sustained growth
- Blue-chip compounders (MSFT, GOOGL) have historically traded at 1.5–2.5× PEG

---

## Step 8: Analyst Consensus Crosscheck (New)

Always pull 12-month analyst consensus as a crosscheck. Search "[TICKER] analyst price target consensus 12 month [year]".

Collect:
- Consensus price target (mean)
- High / Low target
- Buy / Hold / Sell breakdown
- Number of analysts

Then explain the gap between DCF intrinsic value and analyst targets:

**DCF vs. Analyst Targets — always explain this:**

| | DCF | Analyst Target |
|---|---|---|
| **Answers** | What is this business worth? | Where will this stock trade in 12 months? |
| **Method** | Discounted cash flows | Forward P/E × next-year earnings |
| **Captures** | Fundamental intrinsic value | Sentiment + multiple expansion |
| **Limitation** | Undervalues hypergrowth; terminal growth caps at 2.5% | Can be consensus-chasing; no margin of safety |

Key framing: **DCF gives the floor** (intrinsic value if growth disappoints). **Analyst targets give the ceiling** (where sentiment takes it if growth delivers). The current price sits between these two — and that gap defines the risk/reward.

If analyst targets are significantly above DCF intrinsic value (common for AI/hypergrowth names), explain that analysts are typically doing: `Forward P/E × FY+2 EPS = price target`. Show the implied multiple math.

---

## Output Format

```
═══════════════════════════════════════════════════════════
  DCF INTRINSIC VALUE — [TICKER] ([Company Name])
  As of [Date] | Current Price: $XX.XX
═══════════════════════════════════════════════════════════

── INPUT DATA ──────────────────────────────────────────────
  TTM Reported FCF:            $X.XB
  TTM SBC:                    −$X.XB
  TTM SBC-Adjusted FCF:        $X.XB
  Normalized FCF Margin:       X.X%  (avg of [yr], [yr], [yr])
  Historical Normalized Base:  $XX.XB
  Most Recent Quarterly FCF:   $X.XB  (annualized: ~$XX.XB)
  Analyst FY Consensus FCF:    $XX.XB
  Staleness Ratio:             X.Xx  → [stale / current]
  FCF BASE USED:               $XX.XB  ([historical / forward] — reason: [X])

  FCF CAGR ([yr]–[yr]):        X.X%   (or "N/A — revenue CAGR used")
  Revenue CAGR ([yr]–[yr]):    X.X%
  Company Guidance:            [X]
  Growth Proxy Used:           [FCF CAGR / Revenue CAGR / Forward-looking] — reason: [X]

  Raw Beta:                    X.XX
  Adjusted Beta (Blume):       X.XX  (0.67 × X.XX + 0.33)
  Total Debt:                  $XX.XB
  Total Cash (latest qtr):     $XX.XB
  Net Debt:                    $XX.XB
  Shares Outstanding:          X.XXB
  Risk-Free Rate:              X.X% (10-yr Treasury, as of [date])

── WACC CALCULATION ────────────────────────────────────────
  Cost of Equity:    X.X%  (CAPM: X.X% + X.XX × 5.5%)
  Cost of Debt:      X.X%  (pre-tax) → X.X% after-tax (tax: X.X%)
  Capital Structure: XX% equity / XX% debt
  Base WACC:         X.X%

── SCENARIO ASSUMPTIONS ────────────────────────────────────
                       BEAR       MODERATE     BULL
  FCF Base:           $XX.XB     $XX.XB       $XX.XB  (same)
  Growth Basis:       [historical CAGR / forward guidance — explain]
  Phase 1 Growth:      X.X%       X.X%         X.X%
  Phase 2:            Fade to     Fade to      Fade to
                       1.5%        2.0%         2.5%
  WACC Used:           X.X%       X.X%         X.X%
  Terminal Growth:     1.5%        2.0%         2.5%

── INTRINSIC VALUE RESULTS ─────────────────────────────────
                       BEAR       MODERATE     BULL
  Enterprise Value:   $XXB        $XXB         $XXB
  Equity Value:       $XXB        $XXB         $XXB
  Per Share:          $XX.XX      $XX.XX       $XX.XX
  vs. Current Price:  −XX%        −XX%/+XX%    +XX%

── KEY VALUE DRIVER ────────────────────────────────────────
  Most sensitive to: [FCF growth / WACC / terminal growth]
  +1% in WACC → intrinsic value changes by ~$X.XX/share
  +1% in growth → intrinsic value changes by ~$X.XX/share

── PEG RATIO ───────────────────────────────────────────────
  Trailing EPS:       $X.XX  (price / trailing P/E)
  Forward P/E:        X.Xx   (price / next-yr consensus EPS)
  Next-Yr EPS Growth: X.X%
  Trailing PEG:       X.Xx
  Forward PEG:        X.Xx
  Normalized PEG:     X.Xx   (forward P/E / sustainable X.X% growth)
  Interpretation:     [undervalued / fairly valued / premium — context]

── REVERSE DCF ─────────────────────────────────────────────
  To justify today's price of $XX.XX at base WACC (X.X%)
  and 2.0% terminal growth, the market implies:
    Steady-state FCF required: ~$XXB
    vs. FCF Base today:        ~$XXB
    Implied FCF multiple:       X.Xx
    Implied annual growth:      ~X.X% per year for 10 years

── ANALYST CROSSCHECK ──────────────────────────────────────
  Consensus target:   $XXX  (+XX% upside)
  High / Low:         $XXX / $XXX
  Ratings:            XX Buy / XX Hold / XX Sell
  How analysts get there: [X]x FY[Y] EPS × $X.XX = ~$XXX
  DCF floor vs analyst ceiling: [explain the gap clearly]

── ASSUMPTIONS & CAVEATS ───────────────────────────────────
  • [FCF base note — historical or forward, and why]
  • [SBC deduction note]
  • [Beta/Blume note]
  • [Tax rate normalization if applied]
  • [Terminal growth cap note]
  • [Company-specific risks: customer concentration, AI capex dependency,
     debt load, competitive threats, regulatory, etc.]
  • [Why DCF may undervalue: if hypergrowth stock, explain DCF floor vs
     market ceiling dynamic]
```

---

## Important Rules

1. **Always run the staleness check.** The #1 DCF error is using a stale historical base when a company has undergone a step-change in earnings power. Check quarterly run-rate and analyst consensus before locking in the base.
2. **Normalized FCF Base over TTM FCF.** TTM FCF is a point-in-time number. The normalized base reflects sustainable earning power. Show TTM FCF as context only.
3. **Always deduct SBC.** If SBC data is unavailable, state so explicitly and note intrinsic value is likely overstated.
4. **Always apply Blume beta.** Report raw beta for reference, use adjusted beta in all calculations.
5. **Terminal growth must respect the rate floor.** Never use terminal growth above `min(2.5%, rf − 1.5%)`.
6. **Phase 2 must fade linearly, not step.** Year 6–10 growth linearly interpolates between Phase 1 and terminal rate.
7. **Use most recent quarterly cash.** Annual cash figures can be 6–12 months stale. Cash changes fast in FCF-heavy companies.
8. **Normalize the tax rate.** One-time deferred tax provisions (acquisitions, restructuring) can spike or collapse the effective rate. Use a 3-year average or stated normalized rate.
9. **Always compute PEG.** It takes 30 seconds and gives the user an immediately intuitive valuation sanity check alongside the DCF.
10. **Always pull analyst targets and explain the DCF-vs-target gap.** Users are confused when DCF says $78 and analysts say $520. Explaining this is as important as the DCF itself.
11. **Always show your math.** Every number must be traceable to a source or formula.
12. **Always cite data sources and dates.**
13. **Do not anchor to the current price during the DCF.** Current price appears only in margin of safety, PEG, and reverse DCF sections.
14. **Flag data quality issues prominently.** Sparse FCF history (<3 years), persistent losses, or extreme SBC ratios reduce reliability.
15. **Round sensibly.** Per-share values to 2 decimal places. Billions to 1 decimal place.
