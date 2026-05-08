"""
LLM scorer — uses an OpenRouter model to score a job description against Oliver's profile.
Called by the discovery runner for jobs that pass the keyword threshold.
Returns a score 0.0–10.0 and a one-line reason.
"""

import asyncio
import json
import re

import openai
from openai import AsyncOpenAI, OpenAI


_SYSTEM = """You are a job relevance scorer. Score how well a job matches the candidate using the rules below.
Output a score 0.0–10.0. Start at 5.0 and apply the rules.

━━ CANDIDATE SUMMARY ━━
10+ years in enterprise AI — conversational AI, LLM pipelines, agentic systems, evaluation frameworks, 
Currently building production-grade AI at HumanFirst. Strong on no code building and evaluations, not on research or model training.
Open to roles in AI engineering or AI consulting/solutions. Based in Belgrade, works remotely, open to UK relocation.

━━ ROLE TYPES — candidate is open to all ━━
TYPE A — AI Engineering: building agentic systems, LLM pipelines, evaluation frameworks, multi-agent workflows, RAG, prompt engineering, conversational AI
TYPE B — AI Consulting / Solutions: solutions engineer, forward deployed engineer, AI enablement, AI adoption, AI advisory, AI strategy, fractional AI, customer success (technical), pre-sales, GTM engineer, technical account management — any role where deep AI expertise is applied in a client-facing or go-to-market context
TYPE C - Conversational AI and conversation design

━━ BOOST (add to score) ━━
+0.5  Core stack match at least 2 of the following -  LangGraph, LangChain, LangSmith, n8n, agentic, evaluation framework, LLM-as-judge
+3.5  Strong domain fit: conversational AI, NLU, contact centre AI, voice AI, , prompt optimisation
+2.5  Consulting/solutions fit (Type B): solutions engineer, forward deployed engineer, AI enablement, AI adoption lead, AI consultant, AI advisor, fractional CTO/AI, pre-sales with AI domain depth — candidate's consulting background is directly transferable
+3.0  AI automation or enablement
+4.0  Remote role without stating a specific country
+1.0  UK-based role (London, Edinburgh, Cambridge, Norwich)
+0.5  Spain or Europe-based role
+0.5  Mentions Claude, Anthropic, or OpenAI as primary stack

━━ PENALISE (subtract from score) ━━
-3.5  Role is primarily software engineering — system design, backend, full-stack, microservices, distributed systems — with AI as secondary or incidental. "AI Engineer" in title but JD is really SWE.
-1.0  Heavy focus on production experience
-2.0  Requires PhD or pure research background
-3.0  Primary stack is Java, C++, Rust, or Scala with no Python/LLM overlap
-2.0  Requires hands-on ML experience (model training, fine-tuning, RLHF, MLOps, model architecture) as a core requirement
-4.0  Requires 5+ years of software engineering as an explicit prerequisite, independent of AI skills
-2.5  Requires 5+ years in a specific narrow domain the candidate doesn't have (e.g. finance quant, drug discovery, legal)
-2.0  Role is primarily data engineering, data pipelines, or data warehousing with AI as a side mention
-2.0  Role is heavily focused on sales 

━━ DISQUALIFY — score exactly 1.0 ━━
Any of: pure research lab role, requires PhD as a hard requirement, no AI/LLM component at all, junior/graduate level, retail/operations/non-tech
Role is >60% software engineering (backend, full-stack, infra, DevOps) with AI as a minor addition — even if titled "AI Engineer"
Role is >60% data science or ML research — building or training models, not deploying or applying LLM systems
Job is a contract role or fixed term contract role for 12 months or under
Job description is not written in English
Requires fluency in a language other than English or in addition to English
Role is US-only: located in the United States with no remote or relocation option outside the US (signals: US city/state with no mention of remote or international, explicit "must be authorised to work in the US", US-only salary in USD with no remote option)
NOTE: do NOT disqualify "Solutions Engineer" or "AI Enablement" roles on the basis of being client-facing — these are a good fit for this candidate.

━━ CALIBRATION ━━
9–10: Candidate could apply today with high confidence — stack, seniority, and domain all align
7–8:  Strong fit, worth applying, minor gaps
5–6:  Relevant but notable mismatch in stack, seniority, or domain
3–4:  Tangential — AI mentioned but not the core of the role
1–2:  Wrong domain, wrong level, or disqualifying requirement

Respond ONLY with valid JSON in this exact format:
{"score": 7.5, "reason": "One sentence citing the specific rule(s) that most affected the score"}"""



def _build_user_message(jd_text: str) -> str:
    return f"""JOB DESCRIPTION:
{jd_text[:5000]}"""


def _parse_response(raw: str) -> tuple[float, str]:
    if raw.startswith("```"):
        lines = raw.splitlines()
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw = "\n".join(lines).strip()
    # Extract first JSON object only, ignoring any trailing text
    match = re.search(r'\{[^{}]*\}', raw, re.DOTALL)
    if match:
        raw = match.group(0)
    data = json.loads(raw)
    score = float(data["score"])
    reason = str(data.get("reason", ""))
    return round(max(0.0, min(10.0, score)), 1), reason


def llm_score(jd_text: str, config) -> tuple[float | None, str]:
    """
    Score a single JD synchronously. Returns (score, reason) or (None, error).
    """
    if not config.openrouter_api_key:
        return None, "No OPENROUTER_API_KEY set"
    if not jd_text or not jd_text.strip():
        return None, "No JD text to score"

    client = OpenAI(api_key=config.openrouter_api_key, base_url="https://openrouter.ai/api/v1")

    try:
        response = client.chat.completions.create(
            model=config.llm_scoring_model,
            max_tokens=200,
            messages=[
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": _build_user_message(jd_text)},
            ],
        )
        return _parse_response(response.choices[0].message.content.strip())
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        return None, f"Parse error: {e}"
    except openai.APIError as e:
        return None, f"API error: {e}"


async def _score_one_async(
    job_id: int,
    jd_text: str,
    config,
    client: AsyncOpenAI,
    semaphore: asyncio.Semaphore,
) -> tuple[int, float | None, str]:
    async with semaphore:
        try:
            response = await client.chat.completions.create(
                model=config.llm_scoring_model,
                max_tokens=200,
                messages=[
                    {"role": "system", "content": _SYSTEM},
                    {"role": "user", "content": _build_user_message(jd_text)},
                ],
            )
            content = response.choices[0].message.content
            if content is None:
                return job_id, None, "Empty response from model"
            score, reason = _parse_response(content.strip())
            return job_id, score, reason
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            return job_id, None, f"Parse error: {e}"
        except openai.APIError as e:
            return job_id, None, f"API error: {e}"
        except TypeError as e:
            return job_id, None, f"Type error: {e}"


def llm_score_batch(jobs: list[dict], config, concurrency: int = 20) -> list[tuple[int, float | None, str]]:
    """
    Score a batch of jobs concurrently.
    jobs: list of dicts with keys 'id' and 'jd_text'
    Returns list of (job_id, score, reason) in completion order.
    """
    if not config.openrouter_api_key:
        return [(j["id"], None, "No OPENROUTER_API_KEY set") for j in jobs]

    async def _run():
        client = AsyncOpenAI(api_key=config.openrouter_api_key, base_url="https://openrouter.ai/api/v1")
        semaphore = asyncio.Semaphore(concurrency)
        tasks = [
            _score_one_async(j["id"], j["jd_text"], config, client, semaphore)
            for j in jobs
            if j.get("jd_text", "").strip()
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
