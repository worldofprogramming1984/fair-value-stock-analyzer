"""Portfolio ingestion + owner-gate tests (no API key, no network)."""
import hashlib

from engine import analyst
from engine import portfolio as pf
from engine import prompts


def test_normalize_cleans_tickers_and_numbers():
    rows = [
        {"ticker": " aapl ", "value": "$1,000", "percent": "10%"},
        {"ticker": "msft", "value": "2000", "percent": None},
        {"ticker": "", "value": "5"},          # dropped (no ticker)
    ]
    out = pf.normalize_manual(rows)
    assert [h["ticker"] for h in out] == ["AAPL", "MSFT"]
    assert out[0]["value"] == 1000.0
    assert out[0]["percent"] == 10.0


def test_percents_derived_from_values_when_absent():
    rows = [{"ticker": "A", "value": 300}, {"ticker": "B", "value": 100}]
    out = pf.normalize_manual(rows)  # no percents given
    pcts = {h["ticker"]: h["percent"] for h in out}
    assert pcts["A"] == 75.0 and pcts["B"] == 25.0


def test_breakdown_math(monkeypatch):
    monkeypatch.setattr(pf, "_sector", lambda t: {"AAPL": "Tech", "XOM": "Energy"}.get(t, "Unknown"))
    holdings = [
        {"ticker": "AAPL", "name": None, "value": None, "percent": 60.0},
        {"ticker": "XOM", "name": None, "value": None, "percent": 40.0},
    ]
    b = pf.enrich_and_breakdown(holdings)
    assert b["n_holdings"] == 2
    assert b["top_name"] == "AAPL" and b["top_weight"] == 60.0
    assert b["top5_weight"] == 100.0
    assert b["sectors"] == {"Tech": 60.0, "Energy": 40.0}


def test_format_block_runs(monkeypatch):
    monkeypatch.setattr(pf, "_sector", lambda t: "Tech")
    holdings = pf.normalize_manual([{"ticker": "A", "percent": 100}])
    block = pf.format_holdings_block(holdings, pf.enrich_and_breakdown(holdings))
    assert "Holdings" in block and "Sector mix" in block


def test_is_owner_true_false():
    phrase = "correct horse battery"
    h = hashlib.sha256(phrase.encode()).hexdigest()
    assert analyst.is_owner(phrase, h) is True
    assert analyst.is_owner("wrong", h) is False
    assert analyst.is_owner(phrase, None) is False   # not configured
    assert analyst.is_owner("", h) is False


def test_guest_policy_forbids_advice_owner_allows():
    assert "may NOT give any recommendation" in analyst.GUEST_POLICY
    assert "Options to consider" in analyst.OWNER_POLICY
    # methodology prompt loads and carries the disclaimer requirement
    body = prompts._load("portfolio-analyst")
    assert "not a certified financial advisor" in body.lower()
