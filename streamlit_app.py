"""Fair Value Stock Analyzer — Streamlit front end.

Type a ticker → sector-aware fair-value analysis. Bring your own Anthropic API key.
Runs the same sector-skill methodology built in Claude Code, via the Anthropic API.
"""
from __future__ import annotations

import streamlit as st

from engine import data as datamod
from engine import llm

st.set_page_config(page_title="Fair Value Stock Analyzer", page_icon="📈", layout="centered")


@st.cache_data(ttl=900, show_spinner=False)
def _fetch(ticker: str) -> dict:
    return datamod.fetch(ticker)


# ---------------- Sidebar: key + settings ----------------
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input(
        "Anthropic API key",
        type="password",
        help="Your key is used only for this session and never stored. "
        "Get one at console.anthropic.com → API Keys.",
        placeholder="sk-ant-...",
    )
    model_label = st.selectbox("Model", list(llm.MODEL_CHOICES.keys()), index=0)
    model = llm.MODEL_CHOICES[model_label]
    use_web = st.toggle(
        "Enable web search",
        value=True,
        help="Lets the model pull analyst consensus, Morningstar, Seeking Alpha, "
        "segments, and patent dates. Adds a few cents per run. If your key can't "
        "use web search, turn this off and the model works from market data alone.",
    )
    st.caption("Cost is on your own key — typically a few cents to ~$0.15 per ticker.")
    st.divider()
    st.caption(
        "⚠️ Educational tool, **not financial advice**. Figures are model estimates "
        "from public data and may be wrong or stale. Do your own research."
    )

# ---------------- Main ----------------
st.title("📈 Fair Value Stock Analyzer")
st.write(
    "Sector-aware intrinsic value — the app first classifies the business "
    "(bank, commodity, AI-capex megacap, pharma, REIT, …) and then applies the "
    "valuation model that actually fits it, instead of one DCF for everything."
)

col1, col2 = st.columns([3, 1])
with col1:
    ticker = st.text_input("Ticker", placeholder="e.g. MSFT, JPM, XOM, ABBV, AMZN").strip().upper()
with col2:
    st.write("")
    st.write("")
    run = st.button("Analyze", type="primary", use_container_width=True)

if run:
    if not api_key:
        st.warning("Add your Anthropic API key in the sidebar to run an analysis.")
        st.stop()
    if not ticker:
        st.warning("Enter a ticker symbol.")
        st.stop()

    try:
        with st.spinner(f"Fetching market data for {ticker}…"):
            d = _fetch(ticker)
            block = datamod.format_data_block(d)
    except datamod.DataError as e:
        st.error(str(e))
        st.stop()
    except Exception as e:  # yfinance can raise assorted network errors
        st.error(f"Could not fetch data for {ticker}: {e}")
        st.stop()

    # Header
    price = f"${d['price']:,.2f}" if d.get("price") else "n/a"
    st.subheader(f"{d['long_name']} ({ticker})")
    hc1, hc2, hc3 = st.columns(3)
    hc1.metric("Price", price)
    hc2.metric("Sector", d.get("sector") or "n/a")
    if d.get("target_mean"):
        hc3.metric("Wall St target", f"${d['target_mean']:,.2f}")

    try:
        with st.spinner("Classifying the business…"):
            cls = llm.classify(api_key, block, model=llm.HAIKU)
        badge = cls.get("archetype", cls["skill"].replace("stock-fv-", ""))
        st.info(f"**Classified as:** {badge}  ·  {cls.get('rationale', '')}"
                + ("  ·  _sum-of-the-parts_" if cls.get("sotp") else ""))

        with st.spinner(f"Valuing with {model_label} ({cls['skill']})…"):
            analysis = llm.value(api_key, ticker, block, cls, model=model, use_web_search=use_web)
    except llm.LLMError as e:
        st.error(str(e))
        st.stop()

    st.markdown(analysis)
    st.divider()
    st.caption(
        f"Model: {model_label} · data: yfinance · web search: "
        f"{'on' if use_web else 'off'} · not financial advice."
    )
else:
    st.caption("Enter a ticker and click Analyze. You'll need your own Anthropic API key (sidebar).")
