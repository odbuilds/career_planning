"""
Cascade pipeline scorer — three-stage filter producing a letter tier (A/B/C/D) or DQ.

Stage 1: regex pre-filter (language, US-only, short contracts)
Stage 2: Gemma binary classifier (research / swe-heavy / ds-heavy / sales)
Stage 3: Gemma tier scorer (A/B/C/D against Oliver's profile)
"""

import asyncio
import json
import re

import openai
from openai import AsyncOpenAI, OpenAI


def _extract_json(raw: str) -> dict:
    """Extract the first valid JSON object from raw text, tolerating nested braces."""
    # Strip markdown fences
    if raw.startswith("```"):
        lines = raw.splitlines()[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw = "\n".join(lines).strip()
    # Try direct parse first
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    # Fall back: first { to last }
    start = raw.find('{')
    end = raw.rfind('}')
    if start != -1 and end != -1 and end > start:
        return json.loads(raw[start:end + 1])
    raise ValueError(f"No JSON object found in response: {raw[:200]}")

try:
    from langdetect import detect, LangDetectException
    _LANGDETECT_AVAILABLE = True
except ImportError:
    _LANGDETECT_AVAILABLE = False


# ── Stage 1: Regex pre-filter ─────────────────────────────────────────────────

_GBP_MIN = 70_000
_EUR_MIN = 55_000

_US_ONLY_PHRASES = [
    'must be authorized to work in the us',
    'must be authorized to work in the united states',
    'us citizens only',
    'must be a us citizen',
    'green card required',
    'us work authorization required',
    'authorized to work in the united states without sponsorship',
]


def _extract_salary_amounts(text: str) -> tuple[list[float], list[float]]:
    """Return (gbp_amounts, eur_amounts) >= 10,000 found in text."""
    gbp, eur = [], []

    def _parse(num_str: str, k_flag: str | None) -> float:
        return float(num_str.replace(',', '')) * (1000 if k_flag else 1)

    for m in re.finditer(r'£\s*([\d,]+)\s*(k)?', text, re.IGNORECASE):
        v = _parse(m.group(1), m.group(2))
        if v >= 10_000:
            gbp.append(v)

    for m in re.finditer(r'\b([\d,]+)\s*(k)?\s*gbp\b', text, re.IGNORECASE):
        v = _parse(m.group(1), m.group(2))
        if v >= 10_000:
            gbp.append(v)

    for m in re.finditer(r'€\s*([\d,]+)\s*(k)?', text, re.IGNORECASE):
        v = _parse(m.group(1), m.group(2))
        if v >= 10_000:
            eur.append(v)

    for m in re.finditer(r'\b([\d,]+)\s*(k)?\s*eur\b', text, re.IGNORECASE):
        v = _parse(m.group(1), m.group(2))
        if v >= 10_000:
            eur.append(v)

    return gbp, eur


def _regex_prefilter(jd_text: str) -> tuple[str, str | None]:
    """Returns ('continue', None) or ('reject', reason)."""
    text_lower = jd_text.lower()

    if _LANGDETECT_AVAILABLE:
        try:
            if detect(jd_text[:1000]) != 'en':
                return ('reject', 'non-english')
        except LangDetectException:
            pass

    if any(p in text_lower for p in _US_ONLY_PHRASES):
        return ('reject', 'us-only')

    # Short contract — forward pattern: "6 months contract/engagement/assignment"
    m = re.search(
        r'\b(\d{1,2})[\s-]?months?\s+(contract|ftc|fixed[\s-]term|engagement|assignment|role|position)\b',
        text_lower,
    )
    if m and int(m.group(1)) <= 12:
        return ('reject', 'short-contract')
    # Short contract — reverse pattern: "contract of 6 months", "duration: 6 months"
    m = re.search(
        r'\b(?:contract|engagement|assignment|duration)[^.\n]{0,40}\b(\d{1,2})\s*months?\b',
        text_lower,
    )
    if m and int(m.group(1)) <= 12:
        return ('reject', 'short-contract')

    # Daily rate = contracting signal
    if re.search(r'\b(?:day\s+rate|daily\s+rate|rate\s+per\s+day)\b', text_lower):
        return ('reject', 'contract-day-rate')
    if re.search(
        r'£\s*\d[\d,]*\s*[-–]\s*£?\s*\d[\d,]*\s*(?:per\s+day|/\s*day)',
        text_lower,
    ):
        return ('reject', 'contract-day-rate')
    if re.search(r'\b\d[\d,]+\s*[-–]\s*\d[\d,]+\s*(?:per\s+day|/\s*day)\b', text_lower):
        return ('reject', 'contract-day-rate')

    # IR35 / umbrella company = UK contracting signals
    if 'ir35' in text_lower:
        return ('reject', 'contract-ir35')
    if re.search(r'\bumbrella\s+company\b', text_lower):
        return ('reject', 'contract-umbrella')

    gbp_amounts, eur_amounts = _extract_salary_amounts(jd_text)
    if gbp_amounts and max(gbp_amounts) < _GBP_MIN:
        return ('reject', f'salary-too-low (max £{int(max(gbp_amounts)):,} < £{_GBP_MIN:,})')
    if eur_amounts and max(eur_amounts) < _EUR_MIN:
        return ('reject', f'salary-too-low (max €{int(max(eur_amounts)):,} < €{_EUR_MIN:,})')

    return ('continue', None)


# ── Stage 2: Gemma binary classifier ─────────────────────────────────────────

_GEMMA_FILTER_PROMPT = """Read the job description and answer four yes/no questions. Reply ONLY with JSON: {{"research": true/false, "swe_heavy": true/false, "ds_heavy": true/false, "sales_performance": true/false}}

QUESTIONS:
1. "research": Is this primarily a research role? Signs: paper publication expected, novel algorithm development, research lab, "publish at NeurIPS/ICML", PhD strongly preferred for the science itself rather than as credential inflation. Applied LLM/agentic work using existing models is NOT research.

2. "swe_heavy": Is the day-to-day work primarily software engineering (backend services, distributed systems, infra, DevOps, full-stack web) with AI/LLM as a minor or secondary component? If AI is in the title but the actual responsibilities are 60%+ generic engineering, answer true. If the role is genuinely about building LLM pipelines, agents, or AI products, answer false even if it mentions Python/APIs/cloud.

3. "ds_heavy": Is this primarily data science or classical ML — training models, feature engineering, statistical modelling, experimentation platforms, MLOps, fine-tuning, RLHF — rather than applied LLM/agent work using pre-trained models?

4. "sales_performance": Is this role focused on selling — carrying a quota, closing deals, generating pipeline, hitting revenue targets, or being measured on sales performance? Signs: "quota", "ARR target", "close deals", "drive revenue", "pipeline generation", "Account Executive", "BDR", "SDR", "Sales Representative", commission-heavy compensation.
IMPORTANT: pre-sales engineering, solutions engineering, sales engineering, forward deployed engineering, and technical roles that SUPPORT sales teams (demos, technical scoping, client workshops, RFP responses) are NOT sales performance roles — answer false for those.

JD:
{jd_text}"""


def _gemma_filter(jd_text: str, client: OpenAI, model: str) -> tuple[str, str | None, dict | None]:
    """Returns (decision, reason, flags). Fail-open on parse error."""
    prompt = _GEMMA_FILTER_PROMPT.format(jd_text=jd_text[:4000])
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=100,
        )
        raw = response.choices[0].message.content or ""
        flags = _extract_json(raw)
        for key in ("research", "swe_heavy", "ds_heavy", "sales_performance"):
            if key not in flags:
                return ('continue', None, {'parse_error': f'missing key {key}', 'raw': raw})
    except (json.JSONDecodeError, KeyError, ValueError, openai.APIError) as e:
        return ('continue', None, {'parse_error': str(e)})

    if flags.get("research"):
        return ('reject', 'research-role', flags)
    if flags.get("swe_heavy"):
        return ('reject', 'swe-heavy', flags)
    if flags.get("ds_heavy"):
        return ('reject', 'ds-heavy', flags)
    if flags.get("sales_performance"):
        return ('reject', 'sales-performance-role', flags)

    return ('continue', None, flags)


# ── Stage 3: Gemma tier scorer ────────────────────────────────────────────────

_TIER_PROMPT = """You are tiering a job for Oliver Day. Read the JD and assign a tier based on whether the day-to-day work described matches what Oliver actually does.

OLIVER'S ACTUAL WORK:
- Conversational AI design and deployment across enterprise platforms: Dialogflow (ES and CX), Kore.AI, Microsoft Copilot. End-to-end delivery covering solution architecture, conversation design, and integration
- Production chatbot deployment and operation. This is where his understanding of LLM production challenges comes from: iteration loops, failure analysis, the necessity of evals, the gap between demo and reality
- Building applications with LLM services via API: extensive experience consuming LLM APIs to build production features and pipelines
- AI automation and enablement: building LLM-powered automations in his current role, helping organisations adopt AI through workflow automation, internal tooling, and process redesign
- LLM evaluation and conversation analysis at scale: LLM-as-judge for QA and adherence, automated analysis of large conversation datasets, prompt orchestration with reporting layers
- Solutions engineering and AI consulting: led R&D for an LLM consulting offering, designed methodology for matching clients to platforms, delivered enterprise training and client workshops, scoped and shipped client engagements end-to-end

OLIVER'S WORKING STYLE:
- No/low-code focused. Builds with platforms like HumanFirst, n8n, Lovable, Supabase, plus low-code conversational AI platforms. NOT a software engineer or coder. Python is used for orchestration and glue, not for building services or production code at depth
- Strong on understanding LLMs and how to apply them through APIs and platforms. Weaker on writing software systems

OLIVER'S TRAJECTORY:
- Agentic systems is an area he's actively building expertise in: personal projects with LangGraph, one production deployment. Not yet his core day-to-day — treat agentic-heavy roles as growth opportunities (B), not perfect matches (A), unless the role explicitly accepts a conversational AI / LLM applications background as the foundation

OLIVER IS NOT:
- A software engineer or coder
- A model trainer or researcher
- A backend/platform/infra engineer
- A data scientist

SENIORITY: Individual contributor and lead-level roles are the target. Director, Head of, VP, or above are not ideal — tier those down. Senior IC, Staff, Principal, Lead, or Manager-of-a-small-team roles are fine.

GEOGRAPHY: Belgrade-based. Accepts any remote (UK/EU/global), UK on-site/hybrid, or EU on-site/hybrid.
- Roles explicitly offering global remote or EU remote get a tier bump (e.g. B→A, C→B) — location flexibility is a significant positive signal.
- Roles that are fully on-site outside the UK/EU, or that state a country requirement Oliver can't meet, tier down one step.

COMPANY DOMAIN RULE — apply this before assigning any tier:
Solutions engineer, pre-sales engineer, forward deployed engineer, customer success, and implementation roles ONLY qualify for A or B if the company is clearly an AI, LLM, conversational AI, agentic AI, or no-code/low-code AI platform vendor. Evidence: the JD or company description explicitly mentions LLMs, AI agents, conversational AI, NLP, or the product itself is an AI tool. If the company is a generic SaaS vendor, consultancy, or non-AI tech firm, these titles are C at best — the work is relationship management or generic technical onboarding, not AI deployment. Title alone is not evidence; the product must be AI.

TIER on the JD's actual responsibilities, not the title:

A — Strong fit. JD describes work Oliver has done before AND can be done with no/low-code or LLM-API-focused tooling. Strongest matches: solutions engineer / forward deployed engineer / AI consultant roles at AI/LLM/conversational AI vendors, AI automation and enablement roles, conversational AI roles, contact centre AI roles, AI advisory roles, LLM evaluation roles, AI roles at no-code/low-code platform vendors.

B — Possible fit. Includes:
    - Director-level or above roles, even where the work itself would otherwise be A-tier
    - Roles requiring strong Python skills as a meaningful part of the job (not deep software engineering, but expecting fluent Python authoring)
    - Agentic engineering roles (growth area, not core)
    - Applied LLM/conversational work with stack mismatch or seniority gap
    - Roles that are AI-applied but in a domain where he has no edge
    - Roles mixing no/low-code work with more code-writing than he typically does
    - Solutions engineer / customer success at an AI-adjacent company where AI is a feature, not the core product

C — Tangential. Roles that require writing real software (production services, backend systems, full-stack apps) even if AI is the domain. Heavy Python engineering with LLM features. AI product management with light hands-on. VP/Head-of roles where the work itself is also a poor fit. Solutions engineer / customer success / implementation roles at non-AI companies.

D — Not a fit. Geography wrong, or fundamentally about work Oliver doesn't do: model training, pure infra, data science, sales quota, pure research. Also: roles requiring strong software engineering skills as a hard prerequisite.

Don't tier up because the title sounds good. Don't tier down because the title is unfamiliar — read what the work actually is. The no/low-code lens matters: a role described as "build LLM features" might be a great fit if it's API-and-platform work, but a poor fit if it requires authoring production software.

Reply ONLY with JSON:
{{"tier": "A"|"B"|"C"|"D", "reason": "<one sentence>"}}

JD:
{jd_text}"""


def _gemma_tier_scorer(jd_text: str, client: OpenAI, model: str) -> tuple[str, str]:
    """Returns (tier, reason). Defaults to ('C', error) on parse failure."""
    prompt = _TIER_PROMPT.format(jd_text=jd_text[:5000])
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=200,
        )
        raw = (response.choices[0].message.content or "").strip()
        data = _extract_json(raw)
        tier = str(data.get("tier", "C")).upper()
        if tier not in ("A", "B", "C", "D"):
            tier = "C"
        reason = str(data.get("reason", ""))
        return (tier, reason)
    except (json.JSONDecodeError, KeyError, ValueError, openai.APIError) as e:
        return ("C", f"parse-error: {str(e)[:100]}")


# ── Orchestrator ──────────────────────────────────────────────────────────────

def pipeline_score(jd_text: str, config) -> tuple[str | None, str]:
    """
    Run the three-stage cascade for a single JD.
    Returns (tier_or_dq, reason) or (None, error_msg).
    """
    if not config.openrouter_api_key:
        return None, "No OPENROUTER_API_KEY set"
    if not jd_text or not jd_text.strip():
        return None, "No JD text"

    decision, reason = _regex_prefilter(jd_text)
    if decision == 'reject':
        return ('DQ', f"Stage 1: {reason}")

    client = OpenAI(api_key=config.openrouter_api_key, base_url="https://openrouter.ai/api/v1")
    model = config.pipeline_scoring_model

    decision, reason, _flags = _gemma_filter(jd_text, client, model)
    if decision == 'reject':
        return ('DQ', f"Stage 2: {reason}")

    tier, reason = _gemma_tier_scorer(jd_text, client, model)
    return (tier, reason)


# ── Async batch variant ───────────────────────────────────────────────────────

async def _score_one_async(
    idx: int,
    jd_text: str,
    config,
    client: AsyncOpenAI,
    semaphore: asyncio.Semaphore,
) -> tuple[int, str | None, str]:
    async with semaphore:
        if not jd_text or not jd_text.strip():
            return (idx, None, "No JD text")

        # Stage 1 is synchronous / cheap — run inline
        decision, reason = _regex_prefilter(jd_text)
        if decision == 'reject':
            return (idx, 'DQ', f"Stage 1: {reason}")

        model = config.pipeline_scoring_model

        # Stage 2
        try:
            prompt2 = _GEMMA_FILTER_PROMPT.format(jd_text=jd_text[:4000])
            resp2 = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt2}],
                temperature=0,
                max_tokens=100,
            )
            raw2 = (resp2.choices[0].message.content or "").strip()
            flags = _extract_json(raw2)
            if flags.get("research"):
                return (idx, 'DQ', "Stage 2: research-role")
            if flags.get("swe_heavy"):
                return (idx, 'DQ', "Stage 2: swe-heavy")
            if flags.get("ds_heavy"):
                return (idx, 'DQ', "Stage 2: ds-heavy")
            if flags.get("sales_performance"):
                return (idx, 'DQ', "Stage 2: sales-performance-role")
        except (json.JSONDecodeError, KeyError, ValueError, openai.APIError):
            pass  # fail-open to Stage 3

        # Stage 3
        try:
            prompt3 = _TIER_PROMPT.format(jd_text=jd_text[:5000])
            resp3 = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt3}],
                temperature=0,
                max_tokens=200,
            )
            raw3 = (resp3.choices[0].message.content or "").strip()
            data3 = _extract_json(raw3)
            tier = str(data3.get("tier", "C")).upper()
            if tier not in ("A", "B", "C", "D"):
                tier = "C"
            reason = str(data3.get("reason", ""))
            return (idx, tier, reason)
        except (json.JSONDecodeError, KeyError, ValueError, openai.APIError) as e:
            return (idx, "C", f"parse-error: {str(e)[:100]}")


def pipeline_score_batch(
    jobs: list[dict],
    config,
    concurrency: int = 10,
) -> list[tuple[int, str | None, str]]:
    """
    Score a batch of jobs concurrently.
    jobs: list of dicts with keys 'id' and 'jd_text'
    Returns list of (id, tier_or_dq_or_none, reason).
    """
    if not config.openrouter_api_key:
        return [(j["id"], None, "No OPENROUTER_API_KEY set") for j in jobs]

    async def _run():
        client = AsyncOpenAI(
            api_key=config.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
        )
        semaphore = asyncio.Semaphore(concurrency)
        tasks = [
            _score_one_async(j["id"], j.get("jd_text", ""), config, client, semaphore)
            for j in jobs
        ]
        return await asyncio.gather(*tasks)

    import concurrent.futures

    def _run_in_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(_run())
        finally:
            loop.close()

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        return ex.submit(_run_in_thread).result()
