"""Prompt assembly + routing tests (no API key, no network)."""
from engine import prompts


def test_all_skills_registered():
    assert len(prompts.SKILLS) == 11
    assert "stock-fv-financials" in prompts.SKILLS
    assert "stock-fv-ai-capex" in prompts.SKILLS
    assert "stock-fv-unprofitable-growth" in prompts.SKILLS


def test_methodology_files_load_and_strip_frontmatter():
    for name in prompts.SKILLS + ["stock-dcf", "_dispatcher"]:
        body = prompts._load(name)
        assert not body.startswith("---"), f"{name}: frontmatter not stripped"
        assert len(body) > 200, f"{name}: body too short"


def test_classify_prompt_has_json_contract():
    cp = prompts.classify_system_prompt()
    assert '"skill"' in cp
    assert '"sotp"' in cp
    assert "stock-fv-financials" in cp  # allowed list present


def test_value_prompt_appends_engine_only_when_referenced():
    tech = prompts.value_system_prompt("stock-fv-technology")   # references stock-dcf
    fin = prompts.value_system_prompt("stock-fv-financials")    # does not
    assert "SHARED DCF ENGINE" in tech
    assert "SHARED DCF ENGINE" not in fin


def test_value_prompt_includes_app_context_and_web_search_rule():
    p = prompts.value_system_prompt("stock-fv-general")
    assert "APP EXECUTION CONTEXT" in p
    assert "web_search" in p
    assert "NEVER" in p  # no-fabrication rule


def test_unknown_skill_falls_back_to_general():
    p = prompts.value_system_prompt("does-not-exist")
    # general skill body mentions the fallback framing
    assert "general" in p.lower()


def test_assumptions_prompt_requests_json_array():
    p = prompts.assumptions_system_prompt("stock-fv-technology")
    assert "DERIVE ASSUMPTIONS ONLY" in p
    assert "JSON array" in p
    # unknown skill falls back to general, still builds
    assert "DERIVE ASSUMPTIONS" in prompts.assumptions_system_prompt("bogus")


def test_confirmed_assumptions_injected_into_value_prompt():
    without = prompts.value_user_prompt("MSFT", "DATA", False, [])
    assert "CONFIRMED ASSUMPTIONS" not in without
    withb = prompts.value_user_prompt("MSFT", "DATA", False, [],
                                      assumptions_block="- WACC: 8%")
    assert "CONFIRMED ASSUMPTIONS" in withb and "WACC: 8%" in withb


def test_value_system_prompt_tells_model_not_to_reask():
    p = prompts.value_system_prompt("stock-fv-general")
    assert "do NOT ask the user" in p or "do not re-derive" in p.lower()


def test_user_prompt_sotp_toggle():
    plain = prompts.value_user_prompt("KO", "DATA", False, [])
    assert "SUM-OF-THE-PARTS" not in plain
    assert "KO" in plain and "DATA" in plain

    sotp = prompts.value_user_prompt("AMZN", "DATA", True, ["AWS -> stock-fv-ai-capex"])
    assert "SUM-OF-THE-PARTS" in sotp
    assert "AWS" in sotp
