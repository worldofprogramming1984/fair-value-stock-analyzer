"""Portfolio ingestion: screenshot (vision) OR manual entry -> normalized holdings,
plus a deterministic sector/concentration breakdown (yfinance).

Holdings schema: list of {"ticker": str, "name": str|None, "value": float|None,
"percent": float|None}.
"""
from __future__ import annotations

import base64
import json
import re
from functools import lru_cache

import anthropic
import yfinance as yf

from .llm import LLMError, _client, _text, _wrap_api_errors

_VISION_PROMPT = (
    "This image is a screenshot of an investment portfolio / holdings list. "
    "Extract every holding you can read. Respond with ONLY a JSON array, no prose, "
    'of objects: {"ticker": "AAPL", "name": "Apple Inc", "value": 1234.56, '
    '"percent": 9.5}. Use null for any field you cannot read. value = dollar market '
    "value; percent = portfolio weight if shown. Include cash if listed (ticker "
    '"CASH"). Do not invent holdings that are not visible.'
)


def extract_from_image(api_key: str, image_bytes: bytes, media_type: str,
                       model: str = "claude-sonnet-5") -> list[dict]:
    """Use Claude vision to read holdings from a portfolio screenshot."""
    client = _client(api_key)
    b64 = base64.standard_b64encode(image_bytes).decode("ascii")
    if media_type not in ("image/png", "image/jpeg", "image/gif", "image/webp"):
        media_type = "image/png"

    def call():
        return client.messages.create(
            model=model,
            max_tokens=1500,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64",
                                                 "media_type": media_type, "data": b64}},
                    {"type": "text", "text": _VISION_PROMPT},
                ],
            }],
        )

    resp = _wrap_api_errors(call)
    raw = _text(resp)
    match = re.search(r"\[.*\]", raw, re.DOTALL)
    if not match:
        raise LLMError("Couldn't read holdings from that image — try a clearer screenshot "
                       "or use manual entry.")
    try:
        items = json.loads(match.group(0))
    except json.JSONDecodeError:
        raise LLMError("Couldn't parse the holdings from that image — use manual entry.")
    return normalize_manual(items)


def normalize_manual(rows) -> list[dict]:
    """Clean a list of {ticker, value, percent[, name]} rows (from vision or a table)."""
    out = []
    for r in rows or []:
        tkr = str(r.get("ticker") or "").strip().upper()
        if not tkr:
            continue
        out.append({
            "ticker": tkr,
            "name": (r.get("name") or None),
            "value": _num(r.get("value")),
            "percent": _num(r.get("percent")),
        })
    return _fill_percents(out)


def _num(x):
    if x is None or x == "":
        return None
    try:
        return float(str(x).replace("$", "").replace(",", "").replace("%", "").strip())
    except (TypeError, ValueError):
        return None


def _fill_percents(holdings: list[dict]) -> list[dict]:
    """If weights are missing but values exist, derive percents from values."""
    have_pct = any(h["percent"] is not None for h in holdings)
    total_val = sum(h["value"] for h in holdings if h["value"] is not None)
    if not have_pct and total_val > 0:
        for h in holdings:
            if h["value"] is not None:
                h["percent"] = round(100 * h["value"] / total_val, 2)
    return holdings


@lru_cache(maxsize=256)
def _sector(ticker: str) -> str:
    if ticker in ("CASH", "USD"):
        return "Cash"
    try:
        return yf.Ticker(ticker).info.get("sector") or "Unknown"
    except Exception:
        return "Unknown"


def enrich_and_breakdown(holdings: list[dict]) -> dict:
    """Compute sector mix + concentration from holdings (weights preferred)."""
    weighted = [h for h in holdings if h["percent"] is not None]
    total_pct = sum(h["percent"] for h in weighted) or 0.0

    sectors: dict[str, float] = {}
    for h in holdings:
        w = h["percent"]
        if w is None:
            continue
        sec = _sector(h["ticker"])
        sectors[sec] = sectors.get(sec, 0.0) + w

    ordered = sorted(weighted, key=lambda h: h["percent"], reverse=True)
    top = ordered[0] if ordered else None
    top5 = sum(h["percent"] for h in ordered[:5])

    return {
        "n_holdings": len(holdings),
        "total_percent": round(total_pct, 1),
        "top_name": (top["ticker"] if top else None),
        "top_weight": (round(top["percent"], 1) if top else None),
        "top5_weight": round(top5, 1),
        "sectors": {k: round(v, 1) for k, v in sorted(sectors.items(), key=lambda kv: -kv[1])},
    }


def format_holdings_block(holdings: list[dict], breakdown: dict) -> str:
    lines = ["Holdings (ticker · weight · value):"]
    for h in sorted(holdings, key=lambda x: (x["percent"] is None, -(x["percent"] or 0))):
        pct = f"{h['percent']:.1f}%" if h["percent"] is not None else "n/a"
        val = f"${h['value']:,.0f}" if h["value"] is not None else "n/a"
        nm = f" ({h['name']})" if h.get("name") else ""
        lines.append(f"  {h['ticker']}{nm}: {pct} · {val}")
    b = breakdown
    lines += [
        "",
        f"Breakdown: {b['n_holdings']} holdings; top position "
        f"{b['top_name']} at {b['top_weight']}%; top-5 = {b['top5_weight']}%.",
        "Sector mix: " + ", ".join(f"{k} {v}%" for k, v in b["sectors"].items()),
    ]
    return "\n".join(lines)
