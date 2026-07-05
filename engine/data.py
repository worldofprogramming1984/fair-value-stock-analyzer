"""Market-data fetch via yfinance (free, no API key).

Produces a normalized dict of the fields the valuation prompts need, plus a
compact human-readable "financial data block" used to ground the LLM so it
does not have to look up basic figures (reduces hallucination + web-search cost).

Every field is best-effort: yfinance is scraping-based and flaky, so missing
values come back as None and are rendered as "n/a" rather than guessed.
"""
from __future__ import annotations

from typing import Any, Optional

import yfinance as yf


class DataError(Exception):
    """Raised when a ticker cannot be resolved at all."""


def _get(d: dict, *keys: str) -> Optional[Any]:
    for k in keys:
        v = d.get(k)
        if v not in (None, "", "Infinity", float("inf")):
            return v
    return None


def _row(df, *candidates: str, n: int = 5) -> Optional[list[float]]:
    """First matching statement row as a most-recent-first list of floats."""
    if df is None or getattr(df, "empty", True):
        return None
    for label in candidates:
        if label in df.index:
            series = df.loc[label]
            vals = [float(x) for x in series.tolist() if x == x]  # drop NaN
            if vals:
                return vals[:n]
    return None


def _b(x: Optional[float]) -> str:
    """Format a dollar amount in billions."""
    if x is None:
        return "n/a"
    return f"${x / 1e9:,.2f}B"


def _pct(x: Optional[float]) -> str:
    if x is None:
        return "n/a"
    return f"{x * 100:,.1f}%"


def fetch(ticker: str) -> dict:
    """Fetch and normalize fundamentals for a ticker. Raises DataError if unresolvable."""
    ticker = ticker.strip().upper()
    if not ticker:
        raise DataError("Please enter a ticker symbol.")

    t = yf.Ticker(ticker)
    try:
        info = t.info or {}
    except Exception:
        info = {}

    # Price / size — prefer fast_info, fall back to info
    price = market_cap = shares = None
    try:
        fi = t.fast_info
        price = getattr(fi, "last_price", None)
        market_cap = getattr(fi, "market_cap", None)
        shares = getattr(fi, "shares", None)
    except Exception:
        pass
    price = price or _get(info, "currentPrice", "regularMarketPrice", "previousClose")
    market_cap = market_cap or _get(info, "marketCap")
    shares = shares or _get(info, "sharesOutstanding")

    if price is None and not info:
        raise DataError(
            f"Could not find data for '{ticker}'. Check the symbol "
            "(US-listed equities work best)."
        )

    # Statements (annual)
    try:
        cf, ist, bs = t.cashflow, t.income_stmt, t.balance_sheet
    except Exception:
        cf = ist = bs = None

    d = {
        "ticker": ticker,
        "long_name": _get(info, "longName", "shortName") or ticker,
        "sector": _get(info, "sector"),
        "industry": _get(info, "industry"),
        "summary": _get(info, "longBusinessSummary"),
        "price": price,
        "market_cap": market_cap,
        "shares_outstanding": shares,
        "beta": _get(info, "beta"),
        "trailing_pe": _get(info, "trailingPE"),
        "forward_pe": _get(info, "forwardPE"),
        "peg": _get(info, "trailingPegRatio", "pegRatio"),
        "price_to_sales": _get(info, "priceToSalesTrailing12Months"),
        "price_to_book": _get(info, "priceToBook"),
        "roe": _get(info, "returnOnEquity"),
        "book_value_per_share": _get(info, "bookValue"),
        "dividend_yield": _get(info, "dividendYield"),
        "total_debt": _get(info, "totalDebt"),
        "total_cash": _get(info, "totalCash"),
        "free_cashflow": _get(info, "freeCashflow"),
        # analyst consensus
        "target_mean": _get(info, "targetMeanPrice"),
        "target_high": _get(info, "targetHighPrice"),
        "target_low": _get(info, "targetLowPrice"),
        "num_analysts": _get(info, "numberOfAnalystOpinions"),
        "recommendation": _get(info, "recommendationKey"),
        # multi-year statement series (most recent first)
        "revenue": _row(ist, "Total Revenue", "Operating Revenue"),
        "net_income": _row(ist, "Net Income", "Net Income Common Stockholders"),
        "operating_cash_flow": _row(cf, "Operating Cash Flow", "Cash Flow From Continuing Operating Activities"),
        "capex": _row(cf, "Capital Expenditure", "Capital Expenditures"),
        "sbc": _row(cf, "Stock Based Compensation"),
        "dep_amort": _row(cf, "Depreciation And Amortization", "Depreciation Amortization Depletion"),
        "free_cashflow_series": _row(cf, "Free Cash Flow"),
    }
    return d


def format_data_block(d: dict) -> str:
    """Compact text block handed to the LLM to ground its numbers."""
    def series(key: str, transform=_b) -> str:
        vals = d.get(key)
        if not vals:
            return "n/a"
        return ", ".join(transform(v) for v in vals) + "  (most recent first)"

    price = f"${d['price']:,.2f}" if d.get("price") else "n/a"
    tgt = "n/a"
    if d.get("target_mean"):
        tgt = f"mean ${d['target_mean']:,.2f}"
        if d.get("target_low") and d.get("target_high"):
            tgt += f" (range ${d['target_low']:,.2f}–${d['target_high']:,.2f})"
        if d.get("num_analysts"):
            tgt += f", {int(d['num_analysts'])} analysts"
        if d.get("recommendation"):
            tgt += f", rec: {d['recommendation']}"

    lines = [
        f"Ticker: {d['ticker']}  ({d['long_name']})",
        f"Sector / Industry: {d.get('sector') or 'n/a'} / {d.get('industry') or 'n/a'}",
        f"Current price: {price}",
        f"Market cap: {_b(d.get('market_cap'))}   Shares out: "
        + (f"{d['shares_outstanding']/1e9:,.2f}B" if d.get('shares_outstanding') else 'n/a'),
        f"Beta (raw): {d.get('beta') if d.get('beta') is not None else 'n/a'}",
        f"Trailing P/E: {d.get('trailing_pe') or 'n/a'}   Forward P/E: {d.get('forward_pe') or 'n/a'}"
        f"   PEG: {d.get('peg') or 'n/a'}   P/S: {d.get('price_to_sales') or 'n/a'}",
        f"Price/Book: {d.get('price_to_book') or 'n/a'}   ROE: {_pct(d.get('roe'))}   "
        f"Book value/share: {('$'+format(d['book_value_per_share'],',.2f')) if d.get('book_value_per_share') else 'n/a'}",
        f"Dividend yield: {_pct(d.get('dividend_yield')) if d.get('dividend_yield') else 'n/a'}",
        f"Total debt: {_b(d.get('total_debt'))}   Total cash: {_b(d.get('total_cash'))}   "
        f"TTM FCF (info): {_b(d.get('free_cashflow'))}",
        f"Wall St price target: {tgt}",
        "",
        "Multi-year statement history (annual, most recent first):",
        f"  Revenue:            {series('revenue')}",
        f"  Net income:         {series('net_income')}",
        f"  Operating cash flow:{series('operating_cash_flow')}",
        f"  Capital expenditure:{series('capex')}",
        f"  Stock-based comp:   {series('sbc')}",
        f"  Depreciation & amort:{series('dep_amort')}",
        f"  Free cash flow:     {series('free_cashflow_series')}",
    ]
    summary = d.get("summary")
    if summary:
        lines += ["", f"Business summary: {summary[:900]}"]
    return "\n".join(lines)
