# 📈 Fair Value Stock Analyzer

A sector-aware stock fair-value tool. Type a ticker and it first **classifies the
business** — bank, commodity producer, AI-capex megacap, pharma, REIT, fintech,
retailer, … — then applies the valuation model that actually fits it, instead of
forcing one DCF onto every company.

Why that matters: a standard free-cash-flow DCF quietly breaks for whole sectors —
banks (deposits aren't debt), commodity producers (point-in-time earnings mislead),
AI-capex megacaps (current FCF is temporarily depressed), pharma (patent cliffs +
GAAP distortion). This tool routes each ticker to the right method.

It also has a **Portfolio analysis** mode (see below).

> ⚠️ **Educational tool — not financial advice.** Estimates come from public data
> and an LLM and may be wrong or stale. Always do your own research.

For architecture, methodology, and design decisions, see **[DESIGN.md](DESIGN.md)**.

## How it works

- **Data:** [yfinance](https://github.com/ranaroussi/yfinance) (free, no key) for price
  and fundamentals.
- **Brain:** the app sends that data plus a library of sector valuation methodologies
  (in [`methodology/`](methodology/)) to the **Anthropic API**, which classifies the
  business and produces a Bear / Moderate / Bull fair value with sanity multiples and an
  external crosscheck (analyst consensus; Morningstar / Seeking Alpha via web search).
- **Bring your own key:** you paste your own Anthropic API key in the sidebar. It's used
  only for your session, never stored or committed. Cost is on your key — typically a few
  cents to ~$0.15 per ticker.

## Run it locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Then open the local URL, paste your Anthropic API key (from
[console.anthropic.com](https://console.anthropic.com) → API Keys) in the sidebar, and
enter a ticker.

> Python 3.12 is recommended (`.python-version`); some data dependencies may not yet ship
> wheels for very new Python versions.

## Portfolio analysis mode

Switch to **Portfolio analysis** in the sidebar to get a portfolio's strengths and
weaknesses — concentration, diversification, hidden correlation (e.g. several holdings
riding one theme), and bear-market durability.

- **Input:** upload a **screenshot** of your holdings (Claude vision reads them) or **enter
  them manually** in the table. Review/edit the parsed rows before analyzing. (A live
  Robinhood connection isn't offered here — it's tied to a single account and can't
  securely serve other users in a shared app.)
- **Guardrail:** the analyst is **not a certified financial advisor** and says so. By
  default it gives **analysis only — no buy/sell/allocation suggestions.**
- **Owner mode (optional):** you can unlock suggestions for yourself with a passphrase.
  Generate its hash and set it as a secret — nothing sensitive lives in the repo:

  ```bash
  python scripts/make_owner_hash.py "your secret passphrase"
  ```

  Put the printed `OWNER_PASSPHRASE_HASH = "…"` in Streamlit Cloud → app → Settings →
  Secrets (or export it as an env var locally). Enter the passphrase in the sidebar to
  switch on owner mode. If no hash is configured, everyone is a guest (analysis only).

## Run the tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -q
```

The suite (prompt routing, data formatting, LLM guards) runs without an API key or network.

## Deploy free & share a link (Streamlit Community Cloud)

1. Push this repo to GitHub (already done if you used `gh`).
2. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub.
3. **Create app → From existing repo** → pick `fair-value-stock-analyzer`, branch `main`,
   main file `streamlit_app.py` → **Deploy**.
4. You get a public `https://<name>.streamlit.app` URL. Share it — each visitor uses
   **their own** Anthropic key, so it costs you nothing to run.

No secrets need to be configured in the Streamlit dashboard: the app holds no keys.

## What it can and can't do

**Can:** classify into the right sector model; Bear/Moderate/Bull fair value; sector
sanity multiples; Wall-Street consensus; sum-of-the-parts for multi-segment names
(e.g. AMZN); Morningstar / Seeking Alpha crosschecks when web search is enabled.

**Can't (honestly):** guarantee data completeness — yfinance is best-effort and missing
fields show as "n/a"; provide paywalled figures if web search is off (they're marked
"not available", never faked).

## Project layout

```
streamlit_app.py     UI + orchestration
engine/data.py       yfinance fetch → normalized data
engine/prompts.py    assemble classify + valuation prompts from methodology/
engine/llm.py        Anthropic API calls (classify, value)
methodology/         the sector valuation skills (the app's "brain")
```

## License

MIT — see [LICENSE](LICENSE).
