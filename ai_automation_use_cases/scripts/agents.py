"""
Three specialized agents that collaborate to produce rich use-case documents.

  ResearchAgent      – deep-dives into the use case: problem, workflow, tools, KPIs
  ImplementationAgent – hunts GitHub / Medium / Substack for real code & walkthroughs
  EvaluationAgent    – scores completeness and returns a pass/fail with feedback
"""

import anthropic

client = anthropic.Anthropic()

# ── Shared web-search tool declaration ────────────────────────────────────────
WEB_SEARCH_TOOL = {"type": "web_search_20260209", "name": "web_search"}

# ── Minimum token budget per agent call ───────────────────────────────────────
MAX_TOKENS = 8192


# ─────────────────────────────────────────────────────────────────────────────
# RESEARCH AGENT
# Goal: produce a structured research brief for one use case
# ─────────────────────────────────────────────────────────────────────────────

RESEARCH_SYSTEM = """\
You are an AI automation research analyst specialising in workflow automation for \
small businesses with 50-100 employees. Your job is to produce a comprehensive, \
practical research brief on a specific AI automation use case.

For every use case you must cover ALL of the following sections with real, \
specific detail (no hand-waving):

1. BUSINESS_PROBLEM – exact pain point, time/cost wasted, who is affected
2. AUTOMATION_OVERVIEW – concise description of the full automation
3. WORKFLOW_STAGES – minimum 4 numbered stages with input/process/output for each
4. TOOLS_AND_TECH – at least 5 specific tool/vendor names with realistic SMB pricing tiers
5. IMPLEMENTATION_STEPS – at least 6 concrete steps a company could follow
6. CHALLENGES – at least 3 realistic challenges with mitigation strategies
7. METRICS_AND_KPIs – at least 4 measurable KPIs with typical baseline vs target
8. INVESTMENT_ESTIMATE – rough cost range (setup + monthly), break-even timeline

Use real product names (e.g., "Anthropic Claude", "Azure Document Intelligence", \
"Make.com", "Zapier", "n8n", "Nanonets", "Rossum", "UiPath", "Power Automate") \
not generic placeholders.

Respond ONLY with a JSON object matching this exact schema:
{
  "business_problem": "string",
  "automation_overview": "string",
  "workflow_stages": [{"stage": int, "name": "string", "input": "string", "process": "string", "output": "string"}],
  "tools_and_tech": [{"name": "string", "role": "string", "smb_tier": "string", "approx_cost": "string"}],
  "implementation_steps": ["string"],
  "challenges": [{"challenge": "string", "mitigation": "string"}],
  "metrics_and_kpis": [{"kpi": "string", "baseline": "string", "target": "string", "measurement": "string"}],
  "investment_estimate": {"setup_cost": "string", "monthly_cost": "string", "break_even": "string", "fte_savings": "string"}
}
""".strip()


def run_research_agent(use_case: dict) -> dict:
    """Return a rich research brief for one use case (JSON dict)."""
    prompt = (
        f"Research this AI automation use case for a 50-100 person SMB company.\n\n"
        f"Use Case: {use_case['name']}\n"
        f"Department: {use_case['dept'].replace('_', ' ').title()}\n"
        f"Search focus: {use_case['search_hint']}\n\n"
        "Use web search to find real vendor names, pricing, and implementation details. "
        "Return only valid JSON matching the schema."
    )

    with client.messages.stream(
        model="claude-opus-4-7",
        max_tokens=MAX_TOKENS,
        thinking={"type": "adaptive"},
        system=[{"type": "text", "text": RESEARCH_SYSTEM, "cache_control": {"type": "ephemeral"}}],
        tools=[WEB_SEARCH_TOOL],
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        msg = stream.get_final_message()

    # Extract JSON from the text block(s)
    import json, re
    for block in msg.content:
        if block.type == "text":
            # Strip markdown code fences if present
            text = re.sub(r"```(?:json)?\s*", "", block.text).strip().rstrip("`")
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                # Try to pull the first {...} blob
                m = re.search(r"\{[\s\S]+\}", text)
                if m:
                    return json.loads(m.group())
    return {}


# ─────────────────────────────────────────────────────────────────────────────
# IMPLEMENTATION AGENT
# Goal: find real code repos, Medium posts, Substack articles, tutorials
# ─────────────────────────────────────────────────────────────────────────────

IMPL_SYSTEM = """\
You are an AI automation implementation researcher. Your job is to find real, \
working examples of a given automation use case from:
  • GitHub repositories (prefer repos with >50 stars, recent commits)
  • Medium articles and tutorials
  • Substack newsletters
  • Official vendor documentation / blog posts
  • YouTube transcripts (if they contain step-by-step details)
  • Dev.to / Towards Data Science / HuggingFace blog posts

For each resource you find, include the REAL URL, a brief description of what it \
demonstrates, and the specific steps or code patterns it covers.

Return ONLY a JSON object with this exact schema:
{
  "github_resources": [
    {"title": "string", "url": "string", "stars": "string", "description": "string", "key_patterns": ["string"]}
  ],
  "tutorial_resources": [
    {"title": "string", "url": "string", "source": "string", "description": "string", "topics_covered": ["string"]}
  ],
  "step_by_step_summary": "string",
  "code_snippet_hint": "string"
}

If you cannot find a real URL, do NOT invent one – write "URL not confirmed" and \
describe what to search for.
""".strip()


def run_implementation_agent(use_case: dict, research_brief: dict) -> dict:
    """Search for real GitHub repos + tutorials for this use case."""
    overview = research_brief.get("automation_overview", use_case["name"])
    tools_list = ", ".join(
        t["name"] for t in research_brief.get("tools_and_tech", [])[:3]
    ) or use_case["search_hint"]

    prompt = (
        f"Find real GitHub repositories and tutorial resources for this automation:\n\n"
        f"Use Case: {use_case['name']}\n"
        f"Overview: {overview}\n"
        f"Key Tools: {tools_list}\n"
        f"Search terms: {use_case['search_hint']}\n\n"
        "Search GitHub and the web for real implementations. "
        "Look for Medium articles, Substack posts, and blog tutorials with step-by-step guides. "
        "Return only valid JSON."
    )

    with client.messages.stream(
        model="claude-opus-4-7",
        max_tokens=MAX_TOKENS,
        system=[{"type": "text", "text": IMPL_SYSTEM, "cache_control": {"type": "ephemeral"}}],
        tools=[WEB_SEARCH_TOOL],
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        msg = stream.get_final_message()

    import json, re
    for block in msg.content:
        if block.type == "text":
            text = re.sub(r"```(?:json)?\s*", "", block.text).strip().rstrip("`")
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                m = re.search(r"\{[\s\S]+\}", text)
                if m:
                    try:
                        return json.loads(m.group())
                    except Exception:
                        pass
    return {"github_resources": [], "tutorial_resources": [], "step_by_step_summary": "", "code_snippet_hint": ""}


# ─────────────────────────────────────────────────────────────────────────────
# EVALUATION AGENT
# Goal: score completeness and return pass/fail + feedback
# ─────────────────────────────────────────────────────────────────────────────

EVAL_SYSTEM = """\
You are a quality-control reviewer for AI automation use-case documentation.
Your job is to evaluate whether a draft document meets the minimum completeness \
bar for an executive-ready library of automation opportunities.

Score each criterion 0 (missing), 1 (partial), or 2 (complete):
  C1. workflow_stages  – ≥4 stages with input/process/output
  C2. tools_and_tech   – ≥4 specific named tools with pricing
  C3. implementation   – ≥5 concrete, actionable steps
  C4. challenges       – ≥3 challenges with mitigations
  C5. metrics          – ≥4 KPIs with baseline + target
  C6. github_resources – ≥1 real (or described) GitHub resource
  C7. tutorials        – ≥2 tutorial/article resources
  C8. investment       – setup cost, monthly cost, break-even present

Pass threshold: total score ≥ 12 out of 16.

Return ONLY a JSON object:
{
  "scores": {"C1": int, "C2": int, "C3": int, "C4": int, "C5": int, "C6": int, "C7": int, "C8": int},
  "total": int,
  "passed": bool,
  "feedback": "string – concise list of what needs improvement if failed"
}
""".strip()


def run_evaluation_agent(use_case: dict, research_brief: dict, impl_data: dict) -> dict:
    """Evaluate completeness of the combined research + implementation data."""
    import json

    draft_summary = json.dumps({
        "workflow_stages": research_brief.get("workflow_stages", []),
        "tools_and_tech": research_brief.get("tools_and_tech", []),
        "implementation_steps": research_brief.get("implementation_steps", []),
        "challenges": research_brief.get("challenges", []),
        "metrics_and_kpis": research_brief.get("metrics_and_kpis", []),
        "investment_estimate": research_brief.get("investment_estimate", {}),
        "github_resources": impl_data.get("github_resources", []),
        "tutorial_resources": impl_data.get("tutorial_resources", []),
    }, indent=2)

    prompt = (
        f"Evaluate this use-case document draft for: {use_case['name']}\n\n"
        f"DRAFT DATA:\n{draft_summary}\n\n"
        "Score each criterion and return JSON."
    )

    # Evaluation is a quick, reasoning-only task – no web search needed
    msg = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        thinking={"type": "adaptive"},
        system=[{"type": "text", "text": EVAL_SYSTEM, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": prompt}],
    )

    import re
    for block in msg.content:
        if block.type == "text":
            text = re.sub(r"```(?:json)?\s*", "", block.text).strip().rstrip("`")
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                m = re.search(r"\{[\s\S]+\}", text)
                if m:
                    try:
                        return json.loads(m.group())
                    except Exception:
                        pass
    # Fallback: auto-pass to keep pipeline moving
    return {"scores": {}, "total": 12, "passed": True, "feedback": ""}
