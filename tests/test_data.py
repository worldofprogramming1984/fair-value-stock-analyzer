"""Data formatting tests (no network). fetch() itself needs yfinance/network
and is exercised manually, not here."""
import pandas as pd

from engine import data as d


def test_billions_and_pct_helpers():
    assert d._b(5e9) == "$5.00B"
    assert d._b(None) == "n/a"
    assert d._pct(0.353) == "35.3%"
    assert d._pct(None) == "n/a"


def test_row_picks_first_matching_label_and_drops_nan():
    df = pd.DataFrame(
        {"2025": [100.0, float("nan")], "2024": [90.0, 5.0]},
        index=["Total Revenue", "Stock Based Compensation"],
    )
    rev = d._row(df, "Revenue", "Total Revenue")   # second candidate matches
    assert rev == [100.0, 90.0]
    sbc = d._row(df, "Stock Based Compensation")    # NaN dropped
    assert sbc == [5.0]
    assert d._row(df, "Nonexistent Line") is None
    assert d._row(None, "anything") is None


MOCK = {
    "ticker": "TEST", "long_name": "Test Co", "sector": "Technology",
    "industry": "Software", "summary": "A test company. " * 3, "price": 123.45,
    "market_cap": 5e11, "shares_outstanding": 4.05e9, "beta": 1.1,
    "trailing_pe": 30.0, "forward_pe": 25.0, "price_to_book": 8.0, "roe": 0.35,
    "book_value_per_share": 15.2, "dividend_yield": 0.008, "total_debt": 2e10,
    "total_cash": 6e10, "free_cashflow": 7e10, "target_mean": 150.0,
    "target_high": 180.0, "target_low": 120.0, "num_analysts": 40,
    "recommendation": "buy", "revenue": [6e11, 5.5e11], "net_income": [7e10],
    "operating_cash_flow": [9e10], "capex": [-8e10], "sbc": [1e10],
    "dep_amort": [3e10], "free_cashflow_series": [7e10],
}


def test_format_data_block_full():
    block = d.format_data_block(MOCK)
    assert "Test Co" in block
    assert "$123.45" in block
    assert "mean $150.00" in block
    assert "40 analysts" in block
    assert "$500.00B" in block  # market cap


def test_format_data_block_handles_missing_fields():
    block = d.format_data_block({"ticker": "X", "long_name": "X", "price": None})
    assert "n/a" in block
    assert "X" in block
