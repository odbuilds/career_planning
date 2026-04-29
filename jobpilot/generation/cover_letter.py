import json
import re
import time
from pathlib import Path

from openai import OpenAI

from core.config import Config
from generation import prompts
from generation.cv_recommendation import get_cv_content

VALID_ROLE_TYPES = {"builder", "solutions_engineer", "enablement", "ai_engineer", "strategic_pm"}

_EXAMPLES_DIR = Path(__file__).parent / "examples"

_UK_INDICATORS = {
    "uk", "united kingdom",
    "london", "cambridge", "norwich", "edinburgh",
}


def _is_uk_role(location: str, jd_text: str) -> bool:
    loc_lower = location.lower()
    if any(ind in loc_lower for ind in _UK_INDICATORS):
        return True
    # Fall back to scanning JD for strong UK signals
    jd_lower = jd_text.lower()
    return "united kingdom" in jd_lower or " uk " in jd_lower or jd_lower.startswith("uk ")


def _strip_planning(text: str) -> str:
    """Strip the <planning>...</planning> block from model output if present."""
    if "</planning>" in text:
        return text[text.index("</planning>") + len("</planning>"):].strip()
    return text.strip()


def _build_prompt(
    company: str,
    role: str,
    jd_text: str,
    cv_content: str,
    projects_content: str,
    snippets_content: str,
    config: Config,
    is_uk: bool,
    role_context: str = "",
    example_letter: str = "",
) -> str:
    relocation_note = ""
    if is_uk:
        relocation_note = (
            "\n**Relocation:** This is a UK-based role. "
            f"{config.name} is currently based in Belgrade, Serbia and is actively seeking to relocate back to the UK. "
            "Include one clear, matter-of-fact sentence stating this — specifically that they are relocating to the UK "
            "and are available to do so. Do not make it sound uncertain or apologetic. Place it in the closing paragraph."
        )

    return prompts.DRAFT_PROMPT.format(
        role_context=role_context,
        role=role,
        company=company,
        jd_text=jd_text,
        cv_content=cv_content,
        snippets_content=snippets_content,
        projects_content=projects_content,
        candidate_name=config.name,
        relocation_note=relocation_note,
        example_letter=example_letter,
    )


def _build_critic_prompt(
    draft: str,
    jd_text: str,
    role: str,
    company: str,
    role_context: str = "",
) -> str:
    return prompts.CRITIC_PROMPT.format(
        role_context=role_context,
        role=role,
        company=company,
        jd_text=jd_text,
        draft=draft,
    )


def _build_rewrite_prompt(
    draft: str,
    critique: str,
    original_prompt: str,
    cv_content: str,
    projects_content: str,
    snippets_content: str,
    role_context: str = "",
) -> str:
    return prompts.REWRITE_PROMPT.format(
        role_context=role_context,
        draft=draft,
        critique=critique,
        original_prompt=original_prompt,
        cv_content=cv_content,
        projects_content=projects_content,
        snippets_content=snippets_content,
    )


def _build_verify_prompt(letter: str, cv_content: str, projects_content: str, snippets_content: str) -> str:
    return f"""You are a fact-checker for a cover letter. Your only job is to find claims in the letter that cannot be verified in the source materials below.

# SOURCE MATERIALS

**CV:**
{cv_content}

**Project Evidence:**
{projects_content}

**Cover Letter Snippets:**
{snippets_content}

# COVER LETTER TO CHECK

{letter}

# TASK

Go through the letter sentence by sentence. For every specific claim — a number, metric, technology, project name, company name, result, or role description — find where it appears in the source materials.

Output a list of flags in this exact format, one per line:

UNSOURCED: "<exact quote from letter>" — not found in source materials
SOURCED: "<exact quote from letter>" — found in [CV / Project Evidence / Snippets]

Only flag specific factual claims (numbers, names, results, technologies). Do not flag general statements of intent or opinion.
If everything checks out, output: ALL SOURCED"""


def _build_strip_prompt(letter: str, flags: str) -> str:
    return f"""A fact-checker has reviewed a cover letter and flagged claims that could not be verified in the candidate's source materials.

# FACT-CHECKER FLAGS
{flags}

# COVER LETTER
{letter}

# TASK

Produce a clean version of the letter with every UNSOURCED claim removed or neutralised.

Rules:
- Remove or generalise any flagged claim. If a sentence loses all meaning without the unsourced claim, remove the whole sentence.
- Do not replace removed content with anything new. Do not invent alternative claims.
- Keep all SOURCED content exactly as written.
- The letter must still read as a coherent whole. Adjust surrounding sentences minimally for flow only — no new substance.
- If removing claims leaves a paragraph too thin, cut the paragraph rather than pad it.

Output only the cleaned letter. No commentary, no flags, no preamble."""


def _call_model(
    client: OpenAI,
    model: str,
    prompt: str,
    max_tokens: int = 8000,
    stage: str = "",
    debug_dir: Path | None = None,
) -> tuple[str, float]:
    t0 = time.perf_counter()
    message = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    elapsed = time.perf_counter() - t0
    label = f"[{stage}] " if stage else ""
    print(f"  {label}{model}: {elapsed:.1f}s", flush=True)
    content = message.choices[0].message.content
    if not content:
        raise ValueError(f"Model returned empty response (finish_reason: {message.choices[0].finish_reason})")
    if debug_dir and stage:
        slug = stage.replace("/", "_")
        (debug_dir / f"{slug}_prompt.txt").write_text(prompt, encoding="utf-8")
        (debug_dir / f"{slug}_output.txt").write_text(content, encoding="utf-8")
    return content, elapsed


def classify(client: OpenAI, model: str, jd_text: str) -> tuple[str, str]:
    prompt = prompts.CLASSIFY_PROMPT.format(jd_text=jd_text)
    try:
        response, _ = _call_model(client, model, prompt, max_tokens=200, stage="0/classify")
        match = re.search(r'\{[^}]+\}', response, re.DOTALL)
        if match:
            data = json.loads(match.group())
            role_type = data.get("role_type", "builder")
            reasoning = data.get("reasoning", "")
            if role_type in VALID_ROLE_TYPES:
                return role_type, reasoning
    except Exception:
        pass
    return "builder", "Classification failed — defaulting to builder"


def _load_example(role_type: str) -> str:
    path = _EXAMPLES_DIR / f"{role_type}.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    fallback = _EXAMPLES_DIR / "builder.md"
    if fallback.exists():
        return fallback.read_text(encoding="utf-8")
    return ""


_LOG_FILE = Path(__file__).parent.parent / "logs" / "cover_letter_timing.jsonl"


def _write_timing_log(
    company: str,
    role: str,
    draft_model: str,
    critic_model: str,
    rewrite_model: str,
    t_draft: float,
    t_critic: float,
    t_rewrite: float,
    t_total: float,
    critique: str = "",
) -> None:
    _LOG_FILE.parent.mkdir(exist_ok=True)
    entry = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "company": company,
        "role": role,
        "draft_model": draft_model,
        "critic_model": critic_model,
        "rewrite_model": rewrite_model,
        "t_draft": round(t_draft, 2),
        "t_critic": round(t_critic, 2),
        "t_rewrite": round(t_rewrite, 2),
        "t_total": round(t_total, 2),
        "critique": critique,
    }
    with _LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def generate(
    company: str,
    role: str,
    jd_text: str,
    cv_slug: str,
    config: Config,
    location: str = "",
    debug: bool = False,
) -> str:
    """
    Generate a cover letter for the given job via a draft → critic → rewrite pipeline.
    Returns the final letter text as a plain string.
    Raises on API error.
    """
    cv_content = get_cv_content(cv_slug, config)

    try:
        projects_content = Path(config.projects_md_path).read_text(encoding="utf-8")
    except FileNotFoundError:
        projects_content = "[Projects file not found]"

    try:
        snippets_content = Path(config.coverletter_snippets_md_path).read_text(encoding="utf-8")
    except FileNotFoundError:
        snippets_content = "[Cover letter snippets file not found]"

    is_uk = _is_uk_role(location, jd_text)

    client = OpenAI(api_key=config.openrouter_api_key, base_url="https://openrouter.ai/api/v1")
    fast_model = config.llm_scoring_model
    critic_model = config.critic_model
    rewrite_model = config.rewrite_model

    # Classify JD and load branch example
    classify_model = config.pipeline_scoring_model
    role_type, reasoning = classify(client, classify_model, jd_text)
    role_context = f"Role classification: {role_type} — {reasoning}"
    example_letter = _load_example(role_type)
    print(f"  classified as: {role_type} — {reasoning}", flush=True)

    draft_prompt = _build_prompt(
        company, role, jd_text, cv_content,
        projects_content, snippets_content, config, is_uk,
        role_context=role_context,
        example_letter=example_letter,
    )

    debug_dir: Path | None = None
    if debug:
        ts = time.strftime("%Y%m%d_%H%M%S")
        safe = company.replace(" ", "_").replace(".", "")[:30]
        debug_dir = Path(__file__).parent.parent / "debug" / f"{ts}_{safe}"
        debug_dir.mkdir(parents=True, exist_ok=True)
        print(f"  debug output → {debug_dir}", flush=True)

    print(f"Generating cover letter for {role} at {company}:", flush=True)
    t_total = time.perf_counter()

    # Stage 1: draft (fast model)
    draft_raw, t_draft = _call_model(client, fast_model, draft_prompt, stage="1/draft", debug_dir=debug_dir)
    draft = _strip_planning(draft_raw)

    # Stage 2: critic (main model)
    critic_prompt = _build_critic_prompt(draft, jd_text, role, company, role_context=role_context)
    critique, t_critic = _call_model(client, critic_model, critic_prompt, max_tokens=8000, stage="2/critic", debug_dir=debug_dir)

    # Stage 3: rewrite (main model) — same source materials as the drafter
    rewrite_prompt = _build_rewrite_prompt(
        draft, critique, draft_prompt,
        cv_content, projects_content, snippets_content,
        role_context=role_context,
    )
    rewritten, t_rewrite = _call_model(client, rewrite_model, rewrite_prompt, stage="3/rewrite", debug_dir=debug_dir)
    rewritten = _strip_planning(rewritten)

    t_total_elapsed = time.perf_counter() - t_total
    print(f"  total: {t_total_elapsed:.1f}s", flush=True)

    _write_timing_log(company, role, fast_model, critic_model, rewrite_model, t_draft, t_critic, t_rewrite, t_total_elapsed, critique=critique)

    return rewritten


if __name__ == "__main__":
    # Quick test — uses Quadrivia JD
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))

    from core.config import load_config

    cfg = load_config()
    jd = """
    Quadrivia is building AI systems for NHS trusts. We need a Senior AI Engineer
    to lead our multi-agent orchestration layer, integrate with EHR systems, and
    build evaluation pipelines that meet clinical safety standards. You will work
    closely with clinical and engineering teams to ship production-grade systems.
    Stack: Python, LangGraph, OpenAI, OCEL tracing. Voice AI experience a plus.
    """

    print("Generating cover letter for Quadrivia (London, UK)...")
    print()
    letter = generate("Quadrivia", "Senior AI Engineer", jd, "cv_healthtech", cfg, location="London, UK")
    print(letter)
    print()
    print(f"Word count: {len(letter.split())}")
