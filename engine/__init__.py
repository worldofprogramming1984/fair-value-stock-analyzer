"""Fair Value Stock Analyzer — engine package.

Thin orchestration around the Anthropic API that reuses the sector-aware
valuation methodology (see ../methodology). Nothing here stores an API key;
the key is supplied per call by the Streamlit UI (bring-your-own-key).
"""
