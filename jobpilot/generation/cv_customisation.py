from openai import OpenAI

from core.config import Config
from generation.cv_recommendation import get_cv_content


def customise(
    jd_text: str,
    cv_slug: str,
    config: Config,
    archetype: str = "",
) -> str:
    """
    Tailor a CV variant to a specific job description.
    Returns the tailored CV as markdown.
    Raises on API error.
    """
    cv_markdown = get_cv_content(cv_slug, config)
    archetype_line = f"\n**Detected Archetype:** {archetype}" if archetype else ""

    prompt = f"""You are tailoring a CV for a specific job application.

# Job Description
{jd_text}
{archetype_line}

# Original CV
{cv_markdown}

# Instructions

Produce a tailored version of this CV optimised for the job description above. Follow all rules exactly.

## What you MAY do
- Reorder bullet points within a role so the most JD-relevant achievements appear first
- Rewrite up to 4 existing bullet points to use vocabulary from the JD (e.g. if JD says "agentic workflows" and the CV says "multi-agent systems", use the JD's phrasing where it accurately describes the same thing)
- Revise the Professional Summary / intro to match the role archetype and JD priorities
- Integrate JD keywords naturally into existing bullets, only where they accurately describe the existing work

## What you MUST NOT do
- Add any skill, tool, technology, language, or framework not already present in the original CV
- Change employer names, job titles, dates, or company names
- Remove entire roles or significantly shorten the document
- Fabricate or inflate metrics, results, or outcomes not in the original
- Add entirely new bullet points describing work not in the original

## Output
Return the complete CV in the same markdown format as the input. No preamble, explanation, or commentary — just the CV.
"""

    client = OpenAI(api_key=config.openrouter_api_key, base_url="https://openrouter.ai/api/v1")
    message = client.chat.completions.create(
        model=config.generation_model,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.choices[0].message.content.strip()
