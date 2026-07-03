"""LLM module tests that don't hit the API."""
import pytest

from engine import llm


def test_model_choices_map_to_ids():
    ids = set(llm.MODEL_CHOICES.values())
    assert llm.SONNET in ids and llm.OPUS in ids and llm.HAIKU in ids


def test_web_search_tool_shape():
    assert llm.WEB_SEARCH_TOOL["type"].startswith("web_search")
    assert llm.WEB_SEARCH_TOOL["name"] == "web_search"


def test_missing_key_raises_friendly_error():
    with pytest.raises(llm.LLMError):
        llm.classify("", "some data block")
