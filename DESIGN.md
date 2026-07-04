# Design Document — Fair Value Stock Analyzer

Status: living document · Last updated: July 2026

## 1. Purpose

A sector-aware stock valuation and portfolio-analysis tool. It answers two questions:

1. **What is a stock worth?** — classify the business, then apply the intrinsic-value
   model that actually fits its economics (not one DCF for everything).
2. **How healthy is a portfolio?** — surface a portfolio's strengths and weaknesses
   (concentration, diversification, hidden correlation, bear-market durability), with a
   strict "not a certified financial advisor" guardrail.

It ships in two forms that share the same methodology: a set of **Claude Code skills +
subagents** (for the author, with richer tools) and a **standalone Streamlit web app**
(free, shareable, bring-your-own-key).

## 2. Problem statement

A single free-cash-flow DCF quietly produces wrong answers across whole sectors:

| Sector | Why a naive FCF-DCF breaks |
|---|---|
| Banks / insurers | "FCF" swings hundreds of billions on balance-sheet mechanics; deposits aren't debt; cash isn't idle. |
| Commodity / cyclical | Point-in-time earnings mislead — peak looks cheap right before a fall, trough looks dear right before recovery. |
| AI-capex megacaps | Current FCF is *temporarily depressed* by a datacenter build → DCF *understates* value. |
| Pharma | GAAP earnings are distorted by acquired-IPR&D / intangible amortization; patents expire (cliffs). |
| REITs / utilities | Depreciation and permanent capex make EPS/FCF meaningless; FFO / rate-base models are correct. |
| Pre-profit growth | No positive earnings or FCF → P/E and standard DCF are undefined. |

The core design idea: **route each company to a purpose-built model.**

## 3. Architecture

```
                         ┌────────────────────────── CLAUDE CODE (author) ──────────────────────────┐
                         │  Skills (LLM instruction files)          Subagents                        │
                         │  ├ stock-dcf            (shared engine)  ├ fair-value-analyst  (dispatcher)│
                         │  ├ stock-fv-* × 11      (sector models)  └ portfolio-analyst   (RH-MCP)    │
                         │  └ stock-analyze        (10-framework)                                     │
                         │  Tools: Robinhood MCP, web search, Skill/Agent system                      │
                         └───────────────────────────────────────────────────────────────────────────┘
                                   │  (methodology copied verbatim, not moved)
                                   ▼
┌──────────────────────────────── STREAMLIT WEB APP (shareable, BYO-key) ───────────────────────────────┐
│  streamlit_app.py  ── Mode: [Single-stock fair value] | [Portfolio analysis]                          │
│                                                                                                        │
│  engine/data.py       yfinance → normalized fundamentals + data block                                  │
│  engine/prompts.py    load methodology/*.md → classify + value system prompts                          │
│  engine/llm.py        Anthropic API: classify (Haiku) → value (Sonnet/Opus) + web_search tool          │
│  engine/portfolio.py  screenshot (vision) / manual → holdings → yfinance sector breakdown              │
│  engine/analyst.py    owner/guest gate + portfolio-analysis call                                       │
│  methodology/*.md     the skills + dispatcher + portfolio framework (the "brain")                      │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Why two surfaces.** The skills are LLM-instruction files — they only "run" when a model
reads them as prompts with data and tools. Claude Code executes them natively (with the
Robinhood MCP and Skill/Agent system). The web app re-hosts the *same* methodology by
sending it to the Anthropic API, so friends get the same intelligence without Claude Code.

**Why the app is LLM-backed (not pure Python).** The valuation reasoning — classification,
sum-of-the-parts, patent-cliff modeling, reading Morningstar/Seeking-Alpha — needs an LLM;
a deterministic reimplementation would lose most of it. The app therefore calls the
Anthropic API. To keep it free to host and share, it is **bring-your-own-key**: each user
supplies their own Anthropic key, so usage cost never lands on the owner.

## 4. Components

### 4.1 Sector skills (the valuation models)
Eleven `stock-fv-*` skills, each self-contained, plus `stock-dcf` as the shared DCF engine
that the DCF-based skills reference:

| Skill | Primary model |
|---|---|
| `technology` | SBC-adjusted 2-phase FCF-DCF; Rule of 40; normalized PEG |
| `financials` | Justified P/B = (ROE−g)/(CoE−g) + residual income; **cost of equity only** |
| `commodity` | Mid-cycle normalized DCF + NAV / reserves; terminal g ≈ 0 |
| `ai-capex` | Normalized-capex DCF + SOTP (mature core + AI optionality); ROIC-vs-WACC on the build |
| `capex-heavy` | Utility → rate base × allowed ROE / DDM; REIT → FFO/AFFO + NAV; MLP → distributable cash |
| `fintech` | Network → tech-style DCF; balance-sheet lender → financials-style P/B-ROE |
| `communication` | Telecom → infra/DDM; media → subscriber economics, content-as-capex |
| `retail` | Lease-adjusted DCF + unit economics; SOTP for e-commerce (AMZN) |
| `healthcare` | Pharma → adjusted-FCF DCF + patent-cliff steps; biotech → rNPV; device → compounder DCF |
| `unprofitable-growth` | Revenue-to-maturity target-margin DCF + reverse DCF; runway & dilution |
| `general` | Fallback disciplined DCF for diversified names |

Every skill ends with an **external crosscheck** (Wall-St consensus + Morningstar Fair
Value Estimate + Seeking Alpha Quant/Valuation) and a not-fabricated "n/a" rule.

### 4.2 Dispatcher — `fair-value-analyst`
Classifies a ticker top-down into one archetype (first match wins, stated with a
rationale), invokes the matching skill, and runs **sum-of-the-parts** for multi-segment
names (e.g. AMZN = retail + AWS + advertising). Profitability gate routes unprofitable
growth companies to `unprofitable-growth` before the technology/general fallback.

### 4.3 Portfolio analyst
- **Claude Code `portfolio-analyst`** (owner-side): pulls holdings from the Robinhood MCP
  or a pasted screenshot; may offer suggestions (it's the owner); always discloses it is
  not a certified financial advisor.
- **Web app Portfolio mode**: holdings via screenshot (Claude vision) or manual entry;
  deterministic sector/concentration breakdown; **analysis-only for guests**, suggestions
  only in owner mode.

### 4.4 App engine modules
- `data.py` — yfinance fetch → normalized dict + compact "data block" that grounds the LLM.
- `prompts.py` — loads `methodology/*.md`, strips frontmatter, builds the classify and
  value system prompts; appends the DCF engine only when a skill references it.
- `llm.py` — Anthropic client; two calls: cheap **classify** (Haiku) → **value**
  (Sonnet default / Opus) with the `web_search` server tool; typed error handling.
- `portfolio.py` — vision extraction, manual normalization, yfinance sector breakdown.
- `analyst.py` — owner/guest gate (`is_owner`) + the portfolio-analysis call.

## 5. Data flow

### Single-stock
```
ticker → yfinance fundamentals → classify (Haiku) → value (Sonnet/Opus + web search) → Markdown
```

### Portfolio
```
screenshot ──vision──┐
                     ├→ holdings table (user confirms/edits) → yfinance sector breakdown
manual entry ────────┘        → analyst call (owner|guest) → Markdown
```

### Screenshot storage / privacy
- The uploaded image lives **only in server RAM** for the duration of processing — the app
  writes it to **no disk, database, log, or repo**.
- It is transmitted **once** to the Anthropic API (under the user's own key) for the vision
  step, then discarded. Only the *derived holdings* persist, in session memory, cleared on
  session end.
- Anthropic's commercial API terms: inputs are **not used to train models**, retained
  briefly for trust-and-safety only.

## 6. Security & compliance

- **Bring-your-own-key.** The Anthropic key is entered at runtime, held in session state,
  never stored, logged, or committed. The repo contains **no secrets** and is safe public.
- **Owner gate.** Portfolio suggestions are gated by an owner passphrase whose **SHA-256
  hash** is set as `OWNER_PASSPHRASE_HASH` (Streamlit secret / env var — never plaintext,
  never in the repo). Comparison is constant-time (`engine/analyst.py`). No hash configured
  ⇒ everyone is a guest.
- **Not a certified financial advisor.** Always disclosed. **Guest mode is analysis-only** —
  the system prompt hard-forbids any buy/sell/allocation/"you should" output.
- **Prompt-injection resistance.** Extracted holdings and screenshot text are treated as
  **data, not instructions**; the no-advice rule overrides anything embedded in them.
- **No fabrication.** When a figure (Morningstar FVE, Seeking Alpha grade, a missing
  fundamental) can't be retrieved, the output says "not available" rather than guessing.

## 7. Deployment

- Code lives on **GitHub** (`worldofprogramming1984/fair-value-stock-analyzer`).
- The live app runs free on **Streamlit Community Cloud**, deployed from `main` /
  `streamlit_app.py`; it yields a public `*.streamlit.app` URL to share.
- Only secret (optional): `OWNER_PASSPHRASE_HASH`, set in the Streamlit dashboard. Users
  supply their own Anthropic key in-app.
- Python pinned to 3.12 (`.python-version`) for dependency-wheel compatibility.

## 8. Known limitations & decisions

- **Robinhood MCP is owner-only.** It authenticates to a single account, so it cannot
  securely serve friends in a public app — the app uses screenshot/manual for everyone;
  Robinhood stays in Claude Code (or local) for the owner.
- **Data completeness.** yfinance is best-effort; missing fields render as "n/a". Segment
  data, drug-level patent dates, and Morningstar/SA are filled via web search or marked
  unavailable.
- **LLM variance.** Estimates are model output on public data — approximate, occasionally
  wrong or stale; explicitly **not financial advice**.
- **Cost/fidelity trade.** LLM-backed for fidelity ⇒ needs an API key (BYO). A free
  deterministic engine was considered and rejected as too lossy.

## 9. Testing

`pytest tests/` (20 tests, no key/network required): prompt routing (skill registry,
frontmatter stripping, engine-append logic, SOTP toggle), data formatting, LLM guards,
portfolio normalization + sector math, owner-hash true/false, and the guest-forbids-advice
/ owner-allows-advice policy. The live LLM path is verified manually with a key.

## 10. Future work

- Multi-screenshot consolidation (brokerage + 401k + Roth) in owner mode.
- Combine Robinhood MCP + pasted screenshots in the Claude Code `portfolio-analyst`.
- Optional caching / rate-limit resilience for yfinance on shared cloud IPs.
- Charts (sector pie, Bear/Mod/Bull bars) in the app output.
