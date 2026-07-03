"""Assemble the classify + value prompts from the copied methodology files.

The methodology/*.md files are the exact skills built in Claude Code, reused
verbatim as prompts. `_dispatcher.md` is the fair-value-analyst agent (the
classification tree); `stock-fv-*.md` are the sector skills; `stock-dcf.md` is
the shared DCF engine that several skills reference.
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

METHODOLOGY_DIR = Path(__file__).resolve().parent.parent / "methodology"

# Valid skill names the classifier is allowed to choose (must match files).
SKILLS = [
    "stock-fv-technology",
    "stock-fv-commodity",
    "stock-fv-financials",
    "stock-fv-fintech",
    "stock-fv-capex-heavy",
    "stock-fv-ai-capex",
    "stock-fv-communication",
    "stock-fv-retail",
    "stock-fv-healthcare",
    "stock-fv-unprofitable-growth",
    "stock-fv-general",
]

_FRONTMATTER = re.compile(r"^---\n.*?\n---\n", re.DOTALL)


@lru_cache(maxsize=None)
def _load(name: str) -> str:
    """Read a methodology file, stripping YAML frontmatter."""
    path = METHODOLOGY_DIR / f"{name}.md"
    text = path.read_text(encoding="utf-8")
    return _FRONTMATTER.sub("", text).strip()


APP_CONTEXT = """
--- APP EXECUTION CONTEXT (read carefully) ---
You are running inside a web app, NOT Claude Code. You do NOT have the Robinhood
MCP or the Skill/subagent system. The market data you need has already been
fetched (via yfinance) and is provided in the user message under "MARKET DATA".
Ground every hard number in that block. For anything not in it — analyst
consensus detail, Morningstar Fair Value Estimate, Seeking Alpha grades, business
segments, patent/LOE dates — use the web_search tool if it is available. If web
search is not available, mark those items "not available" and say so; NEVER
fabricate a number or a third-party estimate.

Output the final result as clean GitHub-flavored Markdown (headings, a
Bear / Moderate / Bull table, bold labels) suitable for rendering in a web page.
Do NOT wrap the whole thing in a code fence. Keep the sector's required sections:
classification + why-this-model, valuation table, sanity multiples, external
crosscheck, verdict, and caveats.
""".strip()


def classify_system_prompt() -> str:
    """System prompt for the cheap classification call."""
    tree = _load("_dispatcher")
    allowed = ", ".join(SKILLS)
    return (
        tree
        + "\n\n--- YOUR TASK IN THIS APP ---\n"
        "You are only doing STEP 2 (classification) here, from the market data "
        "provided in the user message. Do not value the company yet.\n"
        f"Choose exactly one skill from: {allowed}\n"
        "Respond with ONLY a JSON object, no prose, of the form:\n"
        '{"skill": "stock-fv-...", "archetype": "<short label>", '
        '"rationale": "<one sentence>", "sotp": true|false, '
        '"segments": ["<segment> -> <skill>", ...]}\n'
        'Set "sotp" true only for genuine multi-segment names (e.g. AMZN = '
        "retail + AWS + ads); otherwise false with an empty segments list."
    )


def value_system_prompt(skill: str) -> str:
    """System prompt for the main valuation call: the chosen skill + engine + app note."""
    if skill not in SKILLS:
        skill = "stock-fv-general"
    body = _load(skill)
    parts = [body]
    # Append the shared DCF engine when the skill references it.
    if "stock-dcf" in body:
        parts.append("\n\n=== SHARED DCF ENGINE (referenced above) ===\n" + _load("stock-dcf"))
    parts.append("\n\n" + APP_CONTEXT)
    return "\n".join(parts)


def value_user_prompt(ticker: str, data_block: str, sotp: bool, segments: list[str]) -> str:
    sotp_note = ""
    if sotp:
        seg = "; ".join(segments) if segments else "value each major segment separately and sum"
        sotp_note = (
            "\n\nThis is a SUM-OF-THE-PARTS case: "
            f"{seg}. Value each segment with the appropriate method and sum to an "
            "equity value per share."
        )
    return (
        f"Compute the fair value of {ticker}.{sotp_note}\n\n"
        f"MARKET DATA (from yfinance):\n{data_block}"
    )
