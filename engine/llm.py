"""Anthropic API calls: (1) classify the ticker, (2) run the sector valuation.

Bring-your-own-key: the API key is passed in per call from the Streamlit UI and
is never stored or logged here.
"""
from __future__ import annotations

import json
import re
from typing import Optional

import anthropic

from . import prompts

# Model ids (see the app sidebar for the user-facing choice).
HAIKU = "claude-haiku-4-5-20251001"   # cheap — classification
SONNET = "claude-sonnet-5"            # default — valuation
OPUS = "claude-opus-4-8"              # best — valuation

MODEL_CHOICES = {
    "Sonnet 5 (recommended)": SONNET,
    "Opus 4.8 (best, pricier)": OPUS,
    "Haiku 4.5 (cheapest)": HAIKU,
}

WEB_SEARCH_TOOL = {"type": "web_search_20250305", "name": "web_search", "max_uses": 6}


class LLMError(Exception):
    pass


def _client(api_key: str) -> anthropic.Anthropic:
    if not api_key or not api_key.strip():
        raise LLMError("No Anthropic API key provided. Add yours in the sidebar.")
    return anthropic.Anthropic(api_key=api_key.strip())


def _text(resp) -> str:
    return "".join(b.text for b in resp.content if getattr(b, "type", None) == "text").strip()


def _wrap_api_errors(fn):
    try:
        return fn()
    except anthropic.AuthenticationError:
        raise LLMError("Invalid Anthropic API key. Check the key in the sidebar.")
    except anthropic.RateLimitError:
        raise LLMError("Anthropic rate limit hit — wait a moment and try again.")
    except anthropic.APIStatusError as e:
        raise LLMError(f"Anthropic API error ({e.status_code}). Try again shortly.")
    except anthropic.APIError as e:
        raise LLMError(f"Anthropic API error: {e}")


def classify(api_key: str, data_block: str, model: str = HAIKU) -> dict:
    """Return {skill, archetype, rationale, sotp, segments}."""
    client = _client(api_key)

    def call():
        return client.messages.create(
            model=model,
            max_tokens=400,
            system=prompts.classify_system_prompt(),
            messages=[{"role": "user", "content": f"MARKET DATA:\n{data_block}"}],
        )

    resp = _wrap_api_errors(call)
    raw = _text(resp)
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        # Fall back to the safe default rather than erroring the whole run.
        return {"skill": "stock-fv-general", "archetype": "general",
                "rationale": "classification response unparseable; used fallback",
                "sotp": False, "segments": []}
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError:
        return {"skill": "stock-fv-general", "archetype": "general",
                "rationale": "classification JSON invalid; used fallback",
                "sotp": False, "segments": []}
    if data.get("skill") not in prompts.SKILLS:
        data["skill"] = "stock-fv-general"
    data.setdefault("archetype", data["skill"].replace("stock-fv-", ""))
    data.setdefault("rationale", "")
    data.setdefault("sotp", False)
    data.setdefault("segments", [])
    return data


def derive_assumptions(api_key: str, data_block: str, classification: dict,
                       model: str = SONNET) -> list[dict]:
    """Ask the model for the key assumptions it would use, for the user to review/edit.
    Returns a list of {key, label, value, note}; [] if it can't be parsed."""
    client = _client(api_key)

    def call():
        return client.messages.create(
            model=model,
            max_tokens=700,
            system=prompts.assumptions_system_prompt(classification["skill"]),
            messages=[{"role": "user", "content": f"MARKET DATA:\n{data_block}"}],
        )

    resp = _wrap_api_errors(call)
    match = re.search(r"\[.*\]", _text(resp), re.DOTALL)
    if not match:
        return []
    try:
        items = json.loads(match.group(0))
    except json.JSONDecodeError:
        return []
    out = []
    for it in items:
        if isinstance(it, dict) and it.get("label"):
            out.append({"label": str(it.get("label")),
                        "value": str(it.get("value", "")),
                        "note": str(it.get("note", ""))})
    return out


def value(
    api_key: str,
    ticker: str,
    data_block: str,
    classification: dict,
    model: str = SONNET,
    use_web_search: bool = True,
    assumptions_block: str | None = None,
) -> str:
    """Run the sector valuation skill; return formatted Markdown."""
    client = _client(api_key)
    system = prompts.value_system_prompt(classification["skill"])
    user = prompts.value_user_prompt(
        ticker, data_block, classification.get("sotp", False),
        classification.get("segments", []), assumptions_block=assumptions_block,
    )
    tools = [WEB_SEARCH_TOOL] if use_web_search else []

    def call():
        return client.messages.create(
            model=model,
            max_tokens=4000,
            system=system,
            tools=tools,
            messages=[{"role": "user", "content": user}],
        )

    resp = _wrap_api_errors(call)
    out = _text(resp)
    if not out:
        raise LLMError("The model returned an empty response — try again.")
    return out
