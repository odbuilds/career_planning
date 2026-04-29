import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from generation import prompts


def test_classify_prompt_contains_jd():
    result = prompts.CLASSIFY_PROMPT.format(jd_text="Build AI systems for NHS")
    assert "Build AI systems for NHS" in result


def test_classify_prompt_lists_all_role_types():
    result = prompts.CLASSIFY_PROMPT.format(jd_text="test")
    for key in ["builder", "solutions_engineer", "enablement", "ai_engineer", "strategic_pm"]:
        assert key in result


def test_draft_prompt_contains_role_context():
    result = prompts.DRAFT_PROMPT.format(
        role_context="Role classification: builder — hands-on delivery role",
        role="Engineer",
        company="Acme",
        jd_text="Build things",
        cv_content="CV here",
        snippets_content="Snippets here",
        projects_content="Projects here",
        candidate_name="Oliver Day",
        relocation_note="",
        example_letter="Dear Hiring Team,\n\nExample letter.\n\nOliver Day",
    )
    assert "Role classification: builder" in result
    assert "Dear Hiring Team," in result


def test_critic_prompt_contains_role_context():
    result = prompts.CRITIC_PROMPT.format(
        role_context="Role classification: enablement — training focus",
        role="Consultant",
        company="Corp",
        jd_text="Train teams",
        draft="Dear Hiring Team,\n\nDraft.\n\nOliver Day",
    )
    assert "Role classification: enablement" in result


def test_rewrite_prompt_contains_role_context():
    result = prompts.REWRITE_PROMPT.format(
        role_context="Role classification: ai_engineer — technical depth",
        draft="Draft text",
        critique="Critique text",
        original_prompt="Original prompt",
        cv_content="CV",
        projects_content="Projects",
        snippets_content="Snippets",
    )
    assert "Role classification: ai_engineer" in result
