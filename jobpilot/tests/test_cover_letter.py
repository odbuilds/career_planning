import sys
import json
from pathlib import Path
from unittest.mock import MagicMock, patch
sys.path.insert(0, str(Path(__file__).parent.parent))

from generation.cover_letter import classify, _load_example, VALID_ROLE_TYPES


def test_valid_role_types_contains_all_five():
    assert VALID_ROLE_TYPES == {
        "builder", "solutions_engineer", "enablement", "ai_engineer", "strategic_pm"
    }


def test_classify_parses_valid_json():
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices[0].message.content = (
        '{"role_type": "builder", "reasoning": "Hands-on delivery role."}'
    )
    role_type, reasoning, _ = classify(mock_client, "google/gemma-4-26b-a4b-it", "Build fast AI tools")
    assert role_type == "builder"
    assert reasoning == "Hands-on delivery role."


def test_classify_falls_back_on_invalid_json():
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices[0].message.content = (
        "I think this is a builder role."
    )
    role_type, reasoning, _ = classify(mock_client, "google/gemma-4-26b-a4b-it", "Build fast AI tools")
    assert role_type == "builder"
    assert "Classification failed" in reasoning


def test_classify_falls_back_on_unknown_role_type():
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices[0].message.content = (
        '{"role_type": "wizard", "reasoning": "Magic role."}'
    )
    role_type, reasoning, _ = classify(mock_client, "google/gemma-4-26b-a4b-it", "Do magic")
    assert role_type == "builder"
    assert "Classification failed" in reasoning


def test_classify_falls_back_on_api_exception():
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("API timeout")
    role_type, reasoning, t_classify = classify(mock_client, "google/gemma-4-26b-a4b-it", "Build things")
    assert role_type == "builder"
    assert "Classification failed" in reasoning
    assert t_classify == 0.0


def test_load_example_returns_content_for_known_type(tmp_path, monkeypatch):
    examples_dir = tmp_path / "examples"
    examples_dir.mkdir()
    (examples_dir / "builder.md").write_text("Builder example letter", encoding="utf-8")
    monkeypatch.setattr("generation.cover_letter._EXAMPLES_DIR", examples_dir)
    result = _load_example("builder")
    assert result == "Builder example letter"


def test_load_example_falls_back_to_builder_for_missing_type(tmp_path, monkeypatch):
    examples_dir = tmp_path / "examples"
    examples_dir.mkdir()
    (examples_dir / "builder.md").write_text("Builder fallback", encoding="utf-8")
    monkeypatch.setattr("generation.cover_letter._EXAMPLES_DIR", examples_dir)
    result = _load_example("solutions_engineer")
    assert result == "Builder fallback"


def test_load_example_returns_empty_string_if_all_missing(tmp_path, monkeypatch):
    examples_dir = tmp_path / "examples"
    examples_dir.mkdir()
    monkeypatch.setattr("generation.cover_letter._EXAMPLES_DIR", examples_dir)
    result = _load_example("builder")
    assert result == ""
