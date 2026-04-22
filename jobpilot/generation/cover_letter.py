import json
import time
from pathlib import Path

from openai import OpenAI

from core.config import Config
from generation.cv_recommendation import get_cv_content

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
) -> str:
    relocation_note = ""
    if is_uk:
        relocation_note = (
            "\n**Relocation:** This is a UK-based role. "
            f"{config.name} is currently based in Belgrade, Serbia and is actively seeking to relocate back to the UK. "
            "Include one clear, matter-of-fact sentence stating this — specifically that they are relocating to the UK "
            "and are available to do so. Do not make it sound uncertain or apologetic. Place it in the closing paragraph."
        )

    return f"""You are a professional cover letter writer. Produce a single cover letter and nothing else.

# INPUTS

**Target Role:** {role} at {company}

**Job Description:**
{jd_text}

**Candidate CV:**
{cv_content}

**Cover Letter Snippets (HIGHEST PRIORITY — reuse phrasing verbatim or near-verbatim):**
{snippets_content}

**Project Evidence (personal projects and client work — use for concrete examples):**
{projects_content}

# RULES


## Structure & Length

Total: 300–450 words. Every sentence must earn its place.

You are writing a full cover letter, start with Dear Hiring Manager

1. **Opening (2–3 sentences):**
   - Start with a specific result achieved or insight from the provided facts that connects directly to the company's core problem.
   - Name the role and company.
   - Do not be salesy 
   - Do NOT open with the candidate's title or years of experience. Do NOT open with "I am excited/writing/pleased to…"

2. **Body — Argument, not inventory (2 paragraphs, ~200 words total):**
   - Think about the skills that most align with with the job description in general. If the job description is for a conversational AI related role focus on conversational AI related examples and snippets, if it is focused on agentic focus on agentic related examples
   - Choose a MAXIMUM of 2 projects. Pick the two most relevant to what the job description actually asks for. Discard the rest — more projects are not more persuasive.
   - For each project: one sentence of context, one sentence of method/tools, one sentence of measurable outcome.
   - This is not a regurgitation of the CV but an explanation of what makes the candidate relevant. 

3. **Motivation (3–4 sentences, one short paragraph):**
   - Possible options include:
    - Genuine fascination with how humans interact with AI and solving challenges with AI as a puzzle.
    - Desire to keep learning
   - Make it CONCRETE: tie it to a specific design decision, a failure mode discovered, or a moment of insight from the projects above. Abstract philosophy ("at the architectural level") is not motivation — a specific story is.
   - Connect this curiosity to something the company is building or a challenge implied by the JD.

4. **Closing (1–2 sentences):**
   - State what {config.name} brings to the specific problem this company is solving — in plain, concrete language. No stacking of abstract noun phrases ("production-grade agentic architecture, rigorous evaluation methodology, and…"). One clear claim.
   - Add a why-this-company line ONLY if the JD provides a genuine, specific hook. Do not fabricate.
   - Close with the Candidates name Oliver Day
   {relocation_note}



## Voice & Style

- Conversational and direct — write the way a thoughtful person talks, not the way a press release reads.
- Confident but not bombastic. One clear claim, stated plainly, is more persuasive than three stacked superlatives.
- Vary sentence length. A short sentence after a technical one lands harder than another long one.
- No hedging, no filler, no throat-clearing.
- Write in first person ("I built…", "I bring…"). Never refer to the candidate in third person.
- BANNED PHRASES (never use):
  "passionate about", "excited to", "love the opportunity", "would be a great fit",
  "team player", "results-driven", "hard worker", "go-getter", "synergy",
  "fast-paced environment", "dynamic team", "at the intersection of"
- BANNED REGISTER: do not write marketing copy. Phrases like "I bring X, Y, and Z" stacked with abstract nouns, or openers that read like a LinkedIn summary, are the wrong register. Write to a person, not at an audience.

## Anti-Patterns to Avoid

These are specific failure modes from previous generations. Do NOT repeat them:
- ❌ Opening with "[Name] is a [title] with [N] years…" — this is a CV line, not a hook.
- ❌ Listing 3+ projects sequentially — this reads as inventory, not argument.
- ❌ A paragraph that is just a tools/stack list ("LangGraph for X, Python for Y, BigQuery for Z…").
- ❌ Abstract motivation ("how context is passed between agents, how failures surface…") without a concrete anchor.
- ❌ A closing sentence that stacks 3+ abstract noun phrases with commas.
- ❌ Paragraphs longer than 5 sentences.
- ❌ Trying to force the experience to meet the requirements, dont invent or exagerrate experience. If its not there move on to something that is.
- ❌ "It's not X, it's Y" contrasts as an opening device — e.g. "The hard part isn't the engineering, it's the trust-building." This pattern reads as rehearsed and has become a cliché in AI cover letters. Open with a specific fact, result, or observation instead.
- ❌ Meta-commentary about which experience is more relevant — e.g. "The training programme is the more directly relevant of the two." The letter is not a narration of your selection process. Use the experience directly without explaining why you chose it over another.

## Writing Standards

- Action verb + metric: "Cut latency from 2.1s to 380ms" not "improved performance". Specifics beat abstractions.
- Ethical keyword rule: you may reframe real experience using the JD's exact vocabulary, but NEVER add tools or skills not already in the CV. Reformulate what is real — do not fabricate.
- Exact project names: use the name from source materials verbatim (e.g. "Winnow", "vid2doc", "TRAIL"). Do not paraphrase or genericise.
- One clear closing claim: replace stacked noun phrases ("production-grade architecture, rigorous evaluation, and deep expertise") with a single, concrete statement.
- If the source materials contain no strong match for a JD requirement, leave it out. A shorter honest letter beats a padded one. Do not stretch, extrapolate, or invent to fill a gap.

## Format

- Plain text. No markdown, no bullets, no subject line.
- No salutation unless the JD names a specific contact.

# WORKED EXAMPLE

The example below shows the tone, structure, and level of specificity to aim for on a Conversational AI role. Do not copy it — use it to calibrate voice and argument density.

**Example JD archetype:** Conversational AI & Prompt Engineer (ZenBusiness / Velo)

**Example letter:**
Dear Hiring Team,

The Conversational AI & Prompt Engineer role at ZenBusiness caught my attention immediately. I've been working in this space through its entire progression — from intent-driven systems in Dialogflow and IBM Watson to modern LLM pipelines and LangGraph agents — and the challenges you've described around Velo are exactly where my experience sits.

At enterprise scale, I've led the migration of a voice bot handling 100,000+ monthly contacts, reducing its intent set from 950 to under 200 through analysis of 2 million customer utterances and lifting its F1 score from below 50% to 96%. I've built evaluation frameworks comparing AI classifications against human baselines across 50,000+ conversations in insurance and mortgage QA, assessed RAG solutions for a telecommunications contact centre, and processed 50,000+ customer conversations to build a knowledge base optimised for retrieval. A large part of that work has come from reading real interaction data — diagnosing where systems break in production and why — which shapes how I design and constrain LLM behaviour from the outset.

More recently I've been building agentic systems: multi-step pipelines with reflection loops and structured JSON chaining, LangGraph agents with automated prompt optimisation, and full evaluation frameworks with LLM-as-judge scoring. I treat these systems as non-deterministic components that require deliberate shaping and ongoing iteration — not something you deploy and expect to stabilise on their own.

Thank you for your time.

Oliver Day

**What makes this example work:**
- Opens with a span-of-experience claim that directly mirrors the JD's progression of technologies
- Body paragraph 1 leads with the highest-credibility metric (100k contacts, F1 50%→96%) then stacks supporting evidence without listing tools
- Body paragraph 2 shifts to recent agentic work and frames the candidate's mental model ("non-deterministic components"), not just a project list
- No banned phrases, no exaggerated or fabricated examples or claims, no stacked abstractions in the closing

---

**Example JD archetype:** Senior Lead Applied AI Engineer / LLMOps/Platform (Simon-Kucher)

**Example letter:**
Dear Hiring Team,

Claude's Managed Agents announcement made something concrete: connecting pipelines is becoming a commodity. What isn't commoditised is the work of designing workflows with real teams and defining what a good output looks like across domains with genuine edge cases.

That's where my background sits. I've worked through the entire progression of human-computer interaction, from intent-driven chatbots in Dialogflow and Watson to modern LLM pipelines, and a large part of that experience came from reading real interaction data: understanding where systems break in production and why, and negotiating with stakeholders about what matters and what doesn't.

At HumanFirst I've worked across multiple LLM projects including data analysis, deep research agents, and GTM workflows. In particular, enabling 40 non-technical practitioners at a Canadian engineering firm to build and ship their own AI use cases required the same skill as designing a good conversational system: understanding what teams actually need, not just what they ask for.

The limiting factor in agentic systems is never the graph structure. It's constraint, evaluation, and iteration based on real behaviour. Simon-Kucher's focus on measurable outcomes over capability for its own sake is the environment where that approach matters most, and it's the layer my experience directly addresses.

Thank you for your time.

Oliver Day

**What makes this example work:**
- Opens with a market observation anchored to a specific event (Claude's Managed Agents) — frames Oliver as someone thinking at the strategic level without using a contrast device
- No project-by-project inventory; instead ties the through-line of the experience (reading real interaction data, negotiating with stakeholders) directly to what the JD values
- The HumanFirst paragraph uses a concrete scenario (40 non-technical practitioners) to show stakeholder translation skills without listing tools
- Closing lands on a single concrete claim tied to a specific company value ("measurable outcomes over capability for its own sake")

---

**Example JD archetype:** Agentic AI Engineer / Enterprise Consulting (Cognizant-style)

**Example letter:**
Dear Hiring Team,

Running a four-week POC for a major parcel delivery service — evaluating Microsoft Copilot against Azure CLU — the finding that changed their roadmap wasn't a model performance metric. It was identifying where RAG hallucinations would surface in their specific workflows before anything hit production. That kind of discovery only happens when the consultative and engineering work are running in parallel, and it's where I've spent most of my career.

At HumanFirst I've worked embedded in enterprise client teams across regulated industries — insurance, mortgage QA, telecommunications, and a 40-person AI enablement programme at a Canadian engineering firm. That work involved running workshops to surface high-value use cases, helping non-technical stakeholders understand what these systems are actually doing, and translating business requirements into AI architectures that people could trust and maintain. I've led POCs under real time pressure, including a Microsoft Copilot and Azure CLU evaluation for a major parcel delivery service where I identified RAG hallucination risks and demonstrated CLU advantages within four weeks. Findings like that only emerge if you understand both the technology and the business context well enough to ask the right questions.

The technical depth backs the consulting. I've built multi-step agentic pipelines in LangGraph with Pydantic validation and LangSmith observability, evaluated RAG solutions across LangChain, Dialogflow CX, Stack AI, and OpenAI GPTs with frameworks measuring accuracy, hallucination rates, and implementation complexity, and built knowledge bases from 50,000+ conversations structured for retrieval. I've also built evaluation frameworks measuring AI output against human baselines across 50,000+ conversations in regulated industries, and managed prompts in HumanFirst so they're versioned and iterable without touching application code. The design principle underneath all of it is the same one that shapes how I approach client work: separate what can be evaluated and iterated from what defines the structure, so the system can improve continuously without constant intervention.

Cognizant's Agent Foundry framing of Discover, Design, Build, Scale maps closely to how I think about this work. The consulting and the engineering are not separate tracks. The reason the build succeeds is the quality of the discovery.

Thank you for your time.

Oliver Day

**What makes this example work:**
- Opens with a specific POC scenario and an unexpected finding — the insight lands before the candidate is introduced, which mirrors what this JD values without using a contrast device
- Body paragraph 1 leads with the embedded client work and uses a concrete POC (parcel delivery service, four-week evaluation) to demonstrate the consulting-plus-technical combination
- Body paragraph 2 provides technical credibility without being a stack list — each item is paired with a specific outcome or design principle
- Closing ties back to the company's own framing (Agent Foundry) as a genuine specific hook, not a generic compliment

---

First output a planning block (it will be stripped before delivery), then the letter:
Slow down, think, breathe and then create, be decisive.
<planning>
archetype: [one of: LLMOps/Platform | Agentic/Automation | Agentic/Enterprise Consulting | Technical PM | Solutions Architect | Forward Deployed | AI Transformation]
project_1: [project name] — [one sentence: why this is the strongest fit for this specific JD]
project_2: [project name] — [one sentence: why this is the second strongest fit]
hook: [draft of the opening 2 sentences — specific to this company's problem, not generic]
angle: [one sentence: how to frame Oliver's background for this role and archetype]
</planning>

Then the letter with no additional preamble or commentary."""


def _build_critic_prompt(draft: str, jd_text: str, role: str, company: str) -> str:
    return f"""You are a sharp, experienced editor — the kind who has read thousands of cover letters and has zero patience for wasted words, false modesty, or empty enthusiasm. Your job is not to be cruel, but to be honest in a way that actually helps.

You will be given a job description and a cover letter. Read both carefully. Then edit the letter like a real editor would: with a red pen, strong opinions, and the candidate's best interests at heart.

Your critique should feel like notes from a trusted mentor who wants the candidate to get the job. Be direct. Be specific. Quote the letter back to the candidate when something isn't working.

# INPUTS

**Target Role:** {role} at {company}

**Job Description:**
{jd_text}

**Draft Cover Letter:**
{draft}

# WHAT TO ASSESS


Assess the draft on exactly these seven dimensions. For each, give a verdict (Pass / Needs Work / Fail) followed by 1–3 editorial notes. If a dimension is fine, write "Pass — no changes needed."

1. **Opening line** — Does it make you want to keep reading? If it leads with "I am writing to apply for..." or equivalent, say so directly and explain why it fails.

2. **The pitch** — Can you tell in 30 seconds why this person, for this job? If not, say so plainly. What is missing?

3. **The case for hiring them** — Can you state in one sentence why this candidate over anyone else? If yes, quote it. If no, say so. Is the differentiator leading or buried? Do not suggest what the value proposition should be — only assess whether one is present and where it lands.

4. **Relevance of examples** — Does each example explicitly address a specific requirement named in the JD? Quote the JD requirement alongside the example and state whether the connection is made or left for the reader to infer. If the connection is implicit, say so. If the JD requires something the letter does not address at all, name the gap — do not instruct the writer to add something. A shorter honest letter beats a padded one.

5. **Proof points** — Where do they make claims without evidence? Quote the weak line. What number, result, or specific moment would make it believable? If a claim cannot be substantiated, say so — do not suggest invented detail.

6. **Voice** — Does this sound like a person or a LinkedIn profile? Quote specific offending phrases. Flag anything stiff, clichéd, or performative — e.g. "I am passionate about...", "I thrive in fast-paced environments". Also flag any meta-commentary where the writer narrates their own selection process rather than writing the letter — e.g. "The training programme is the more directly relevant of the two", "Of my two experiences here, X is the stronger fit." The letter is not a narration of how it was written. If present, quote it and call it out explicitly.

7. **Closing** — Does it land or fizzle? A weak closing is a missed final impression.


# FORMAT
Plain text under seven numbered headings. No preamble, no praise, no suggested rewrites or example content.

After your critique, produce a rewrite brief using exactly these fields:

Value proposition: [one sentence — who this person is and why they are the hire]
Tone: [2–3 words]
Proof points to use: [quote or paraphrase only specific examples, numbers, or moments that already appear verbatim in the draft above — do NOT invent new metrics, percentages, or results]
Things to cut: [phrases, claims, or sections that should go]
JD gaps to address: [requirements from the JD the letter ignored or underserved — list the gap only, do NOT suggest what evidence to use or invent]
One non-negotiable: [the single most important structural or framing change the rewrite must make]

CRITICAL: The rewrite brief must contain zero fabricated data. Every number, percentage, result, and project name in "Proof points to use" must be directly quoted from the draft. If the draft lacks a metric for something, leave that gap — do not invent a plausible-sounding one.

End with:
OVERALL: [Pass | Minor revisions | Major revisions]]"""


def _build_rewrite_prompt(
    draft: str,
    critique: str,
    original_prompt: str,
    cv_content: str,
    projects_content: str,
    snippets_content: str,
) -> str:
    return f"""An editor has reviewed a cover letter draft and produced the feedback and rewrite brief below. Your job is to write the final version using that brief as your guide.

# EDITOR'S FEEDBACK AND REWRITE BRIEF
{critique}

# DRAFT FOR REFERENCE
{draft}

# SOURCE MATERIALS — the only permitted source of facts, metrics, and examples

**CV:**
{cv_content}

**Project Evidence:**
{projects_content}

**Cover Letter Snippets:**
{snippets_content}

# BEFORE YOU WRITE

Read the source materials and produce an internal inventory:
- List every fact, metric, project name, and example available in the source materials.
- Cross-check against the brief's "Proof points to use" — mark each as FOUND or NOT FOUND.
- For any NOT FOUND item, do not use it in the letter.

Do not output this inventory. Use it only to constrain what goes in the letter.

# RULES — read before writing a single word

**On evidence:**
- Every fact, metric, example, and project name must come directly from the source materials above. If it is not in those materials, it does not go in the letter. No exceptions.
- Do not invent, infer, or round up. Quote numbers as they appear in the source materials. If a metric does not exist for a project, omit it — do not substitute a plausible-sounding one.
- If you catch yourself writing a number, a project name, or a result that you cannot point to verbatim in the source materials — stop and delete it. Confident-sounding specificity that isn't sourced is worse than vagueness.
- The JD describes the employer's world. It is not evidence about the candidate. Do not reflect JD language back as if it describes the candidate's experience.

**On gaps:**
- The editor's rewrite brief lists JD gaps. Before addressing any gap, check whether the source materials contain genuine, high-confidence evidence for it. If they do not, leave the gap unaddressed. A shorter honest letter is always better than a padded one.
- "JD gaps to address" in the brief is a prompt to look, not an instruction to fill regardless. If you look and find nothing solid, move on.

**On the brief:**
- Use the Value proposition, Tone, and One non-negotiable fields as the spine of the rewrite.
- Use Proof points to use to select which evidence from the source materials to carry forward.
- Apply Things to cut — remove those phrases or sections entirely.

**On structure and voice:**
- Follow all formatting and structural rules in the original brief below.
- Direct and clear. Not conversational to the point of being casual, not formal to the point of being stiff. Write like someone confident enough not to perform confidence.

# ORIGINAL BRIEF (structural and formatting rules)
{original_prompt}

Output only the final cover letter. No preamble, no planning block, no commentary."""


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
    draft_prompt = _build_prompt(
        company, role, jd_text, cv_content,
        projects_content, snippets_content, config, is_uk,
    )

    client = OpenAI(api_key=config.openrouter_api_key, base_url="https://openrouter.ai/api/v1")
    fast_model = config.llm_scoring_model
    critic_model = config.critic_model
    rewrite_model = config.rewrite_model

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
    critic_prompt = _build_critic_prompt(draft, jd_text, role, company)
    critique, t_critic = _call_model(client, critic_model, critic_prompt, max_tokens=8000, stage="2/critic", debug_dir=debug_dir)

    # Stage 3: rewrite (main model) — same source materials as the drafter
    rewrite_prompt = _build_rewrite_prompt(
        draft, critique, draft_prompt,
        cv_content, projects_content, snippets_content,
    )
    rewritten, t_rewrite = _call_model(client, rewrite_model, rewrite_prompt, stage="3/rewrite", debug_dir=debug_dir)
    rewritten = _strip_planning(rewritten)

    t_total_elapsed = time.perf_counter() - t_total
    print(f"  total: {t_total_elapsed:.1f}s", flush=True)

    _write_timing_log(company, role, fast_model, critic_model, rewrite_model, t_draft, t_critic, t_rewrite, t_total_elapsed)

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
