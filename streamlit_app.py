"""Fair Value Stock Analyzer — Streamlit front end.

Two modes:
  • Single-stock fair value — sector-aware intrinsic value for a ticker.
  • Portfolio analysis — strengths/weaknesses of a portfolio (screenshot or manual),
    analysis-only for guests, suggestions only for the owner (passphrase-gated).

Bring your own Anthropic API key.
"""
from __future__ import annotations

import os

import pandas as pd
import streamlit as st

from engine import analyst
from engine import data as datamod
from engine import llm
from engine import portfolio as pf

st.set_page_config(page_title="Fair Value Stock Analyzer", page_icon="📈", layout="centered")


@st.cache_data(ttl=900, show_spinner=False)
def _fetch(ticker: str) -> dict:
    return datamod.fetch(ticker)


def _owner_hash() -> str | None:
    try:
        h = st.secrets.get("OWNER_PASSPHRASE_HASH")  # type: ignore[attr-defined]
        if h:
            return str(h)
    except Exception:
        pass
    return os.environ.get("OWNER_PASSPHRASE_HASH")


DISCLAIMER = (
    "⚠️ Educational tool, **not financial advice**, and **not a certified financial "
    "advisor**. Estimates come from public data and an LLM and may be wrong or stale. "
    "Consult a licensed professional before acting."
)

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input(
        "Anthropic API key", type="password", placeholder="sk-ant-...",
        help="Used only for this session, never stored. Get one at console.anthropic.com.",
    )
    model_label = st.selectbox("Model", list(llm.MODEL_CHOICES.keys()), index=0)
    model = llm.MODEL_CHOICES[model_label]
    mode = st.radio("Mode", ["Single-stock fair value", "Portfolio analysis"])
    st.caption("Cost is on your own key — a few cents to ~$0.15 per run.")
    st.divider()
    st.caption(DISCLAIMER)

st.title("📈 Fair Value Stock Analyzer")

# =================================================================== FAIR VALUE
if mode == "Single-stock fair value":
    st.write(
        "Sector-aware intrinsic value — the app classifies the business (bank, commodity, "
        "AI-capex megacap, pharma, REIT, …) then applies the model that fits it."
    )
    with st.sidebar:
        use_web = st.toggle("Enable web search", value=True,
                            help="Lets the model pull consensus, Morningstar, Seeking Alpha, "
                            "segments, and patent dates. Adds a few cents per run.")

    def _reset_fv():
        for k in ("fv_stage", "fv_ticker", "fv_data", "fv_block", "fv_cls", "fv_assump", "fv_result"):
            st.session_state.pop(k, None)

    stage = st.session_state.get("fv_stage")

    # ---- Stage 0: ticker entry ----
    if not stage:
        c1, c2 = st.columns([3, 1])
        ticker = c1.text_input("Ticker", placeholder="e.g. MSFT, JPM, XOM, ABBV, AMZN").strip().upper()
        c2.write(" "); c2.write(" ")
        if c2.button("Analyze", type="primary", use_container_width=True):
            if not api_key:
                st.warning("Add your Anthropic API key in the sidebar."); st.stop()
            if not ticker:
                st.warning("Enter a ticker symbol."); st.stop()
            try:
                with st.spinner(f"Fetching market data for {ticker}…"):
                    d = _fetch(ticker); block = datamod.format_data_block(d)
            except datamod.DataError as e:
                st.error(str(e)); st.stop()
            except Exception as e:
                st.error(f"Could not fetch data for {ticker}: {e}"); st.stop()
            try:
                with st.spinner("Classifying the business…"):
                    cls = llm.classify(api_key, block, model=llm.HAIKU)
                with st.spinner("Deriving assumptions for your review…"):
                    assumptions = llm.derive_assumptions(api_key, block, cls, model=model)
            except llm.LLMError as e:
                st.error(str(e)); st.stop()
            st.session_state.update(fv_stage="assume", fv_ticker=ticker, fv_data=d,
                                    fv_block=block, fv_cls=cls, fv_assump=assumptions)
            st.rerun()
        else:
            st.caption("Enter a ticker and click Analyze. You'll need your own Anthropic API key.")

    # ---- Stages 1–2: header + assumptions / result ----
    else:
        d = st.session_state.fv_data
        cls = st.session_state.fv_cls
        ticker = st.session_state.fv_ticker
        st.subheader(f"{d['long_name']} ({ticker})")
        hc1, hc2, hc3 = st.columns(3)
        hc1.metric("Price", f"${d['price']:,.2f}" if d.get("price") else "n/a")
        hc2.metric("Sector", d.get("sector") or "n/a")
        if d.get("target_mean"):
            hc3.metric("Wall St target", f"${d['target_mean']:,.2f}")
        st.info(f"**Classified as:** {cls.get('archetype', cls['skill'])}  ·  "
                f"{cls.get('rationale', '')}"
                + ("  ·  _sum-of-the-parts_" if cls.get("sotp") else ""))

        if stage == "assume":
            st.markdown("#### Review assumptions")
            st.caption("These are my default assumptions. Edit any **value** to use your own, "
                       "then run — or just proceed with mine.")
            rows = st.session_state.fv_assump or [{"label": "", "value": "", "note": ""}]
            df = pd.DataFrame(rows)[["label", "value", "note"]] if rows else pd.DataFrame(
                columns=["label", "value", "note"])
            edited = st.data_editor(
                df, num_rows="dynamic", use_container_width=True, key="fv_assump_editor",
                column_config={
                    "label": st.column_config.TextColumn("Assumption"),
                    "value": st.column_config.TextColumn("Value"),
                    "note": st.column_config.TextColumn("Basis / note"),
                })
            b1, b2 = st.columns(2)
            go = b1.button("Run valuation with these assumptions", type="primary", use_container_width=True)
            if b2.button("↺ Start over", use_container_width=True):
                _reset_fv(); st.rerun()
            if go:
                recs = edited.to_dict("records")
                lines = [f"- {r['label']}: {r['value']}"
                         + (f"  ({r['note']})" if str(r.get('note') or '').strip() else "")
                         for r in recs if str(r.get('label') or '').strip()]
                block_txt = "\n".join(lines) if lines else None
                try:
                    with st.spinner(f"Valuing with {model_label} ({cls['skill']})…"):
                        result = llm.value(api_key, ticker, st.session_state.fv_block, cls,
                                           model=model, use_web_search=use_web,
                                           assumptions_block=block_txt)
                except llm.LLMError as e:
                    st.error(str(e)); st.stop()
                st.session_state.update(fv_result=result, fv_stage="done")
                st.rerun()

        elif stage == "done":
            st.markdown(st.session_state.fv_result)
            st.divider()
            st.caption(f"Model: {model_label} · data: yfinance · not financial advice.")
            cc1, cc2 = st.columns(2)
            if cc1.button("↩ Adjust assumptions", use_container_width=True):
                st.session_state.fv_stage = "assume"
                st.session_state.pop("fv_result", None); st.rerun()
            if cc2.button("＋ Analyze another", use_container_width=True):
                _reset_fv(); st.rerun()

# =============================================================== PORTFOLIO ANALYSIS
else:
    st.write("Analyze a portfolio's **strengths and weaknesses** — concentration, "
             "diversification, hidden correlation, and bear-market durability.")
    st.warning(DISCLAIMER)

    # Owner gate
    owner = False
    owner_hash = _owner_hash()
    with st.sidebar:
        if owner_hash:
            passphrase = st.text_input("Owner passphrase (optional)", type="password",
                                       help="Unlocks suggestions for the owner. Guests get "
                                       "analysis only.")
            owner = analyst.is_owner(passphrase, owner_hash)
            if passphrase:
                st.caption("🔓 Owner mode — suggestions on" if owner
                           else "🔒 Guest mode — passphrase not recognized")
        else:
            st.caption("Guest mode (analysis only). Owner mode not configured.")

    if "holdings_df" not in st.session_state:
        st.session_state.holdings_df = pd.DataFrame(
            [{"ticker": "", "name": "", "value": None, "percent": None}]
        )

    method = st.radio("How would you like to enter your holdings?",
                      ["Upload a screenshot", "Enter manually"], horizontal=True)

    if method == "Upload a screenshot":
        up = st.file_uploader("Portfolio screenshot (PNG/JPG)", type=["png", "jpg", "jpeg"])
        if st.button("Extract holdings from screenshot"):
            if not api_key:
                st.warning("Add your Anthropic API key in the sidebar."); st.stop()
            if not up:
                st.warning("Upload a screenshot first."); st.stop()
            try:
                with st.spinner("Reading holdings from the image…"):
                    holdings = pf.extract_from_image(api_key, up.getvalue(),
                                                     up.type or "image/png", model=model)
                st.session_state.holdings_df = pd.DataFrame(holdings)
                st.success("Extracted — review and edit below, then Analyze.")
            except llm.LLMError as e:
                st.error(str(e))

    st.caption("Review / edit holdings (ticker required; value or percent recommended):")
    edited = st.data_editor(st.session_state.holdings_df, num_rows="dynamic",
                            use_container_width=True, key="holdings_editor")

    if st.button("Analyze portfolio", type="primary"):
        if not api_key:
            st.warning("Add your Anthropic API key in the sidebar."); st.stop()
        rows = edited.to_dict("records")
        holdings = pf.normalize_manual(rows)
        if not holdings:
            st.warning("Add at least one holding with a ticker."); st.stop()
        with st.spinner("Building sector/concentration breakdown…"):
            breakdown = pf.enrich_and_breakdown(holdings)
            block = pf.format_holdings_block(holdings, breakdown)

        m1, m2, m3 = st.columns(3)
        m1.metric("Holdings", breakdown["n_holdings"])
        if breakdown["top_name"]:
            m1.caption(f"Top: {breakdown['top_name']}")
        m2.metric("Top position", f"{breakdown['top_weight']}%" if breakdown["top_weight"] else "n/a")
        m3.metric("Top-5 weight", f"{breakdown['top5_weight']}%")
        if breakdown["sectors"]:
            st.caption("**Sector mix:** " + " · ".join(f"{k} {v}%" for k, v in breakdown["sectors"].items()))

        try:
            with st.spinner(f"Analyzing with {model_label}…"):
                report = analyst.analyze(api_key, block, owner=owner, model=model)
        except llm.LLMError as e:
            st.error(str(e)); st.stop()

        st.markdown(report)
        st.divider()
        st.caption(("Owner mode" if owner else "Guest mode (analysis only)")
                   + f" · model: {model_label} · not financial advice.")
