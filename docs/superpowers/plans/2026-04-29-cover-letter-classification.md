# Cover Letter Classification Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Gemma-powered JD classification step that routes cover letter generation to one of 5 role-type branches, each using a branch-specific example letter, with all prompts extracted to a dedicated `prompts.py` file.

**Architecture:** A new `classify()` call runs at the start of `generate()`, producing a `(role_type, reasoning)` tuple. A `role_context` string assembled from that tuple is prepended to all three prompt templates (draft, critic, rewrite) via a `{role_context}` placeholder. The branch-specific example letter is loaded from `generation/examples/{role_type}.md` and injected via `{example_letter}` in the draft template. All prompt templates live in `generation/prompts.py`; `cover_letter.py` becomes a pure orchestrator.

**Tech Stack:** Python, OpenRouter API (via openai SDK), `google/gemma-4-26b-a4b-it` for classification, pytest for tests.

---

### Task 1: Create example letter files

**Files:**
- Create: `jobpilot/generation/examples/builder.md`
- Create: `jobpilot/generation/examples/strategic_pm.md`
- Create: `jobpilot/generation/examples/enablement.md`
- Create: `jobpilot/generation/examples/solutions_engineer.md`
- Create: `jobpilot/generation/examples/ai_engineer.md`

- [ ] **Step 1: Create builder.md** (IFS letter from cover_ex.md, letter only — no annotations)

`jobpilot/generation/examples/builder.md`:
```
Dear Hiring Team,

I am writing to apply for the Forward Deployed AI Engineer role at IFS. The position sits squarely at what I have spent the last several years building toward: working directly with enterprise customers to design and deploy production AI that solves real operational problems.

My background covers the full delivery arc the role demands. At HumanFirst, I have deployed conversational AI and LLM-powered systems for enterprise clients across insurance, financial services, and telecommunications, from scoping and architecture through integration, evaluation, and handoff. Recent work includes LangGraph-based agentic pipelines, LLM-as-judge quality monitoring integrated with BigQuery and Looker, and a voice bot migration that rebuilt the NLU architecture from the ground up and took F1 from below 50% to 96% in production across 100,000 monthly contacts.

The enterprise integration dimension of this role is familiar ground. I regularly work across API-based integrations with platforms such as Salesforce, ServiceNow, and CRM middleware, and I understand the operational constraints that shape what good AI deployment looks like in mission-critical environments. I am equally comfortable in a technical architecture discussion and in a client discovery session, and much of my work involves translating ambiguous business problems into defined technical approaches and delivering them quickly. A recent POC for a Latin American call centre, analysing 20,000 conversations and building a generative AI classification model for sales objections with a reusable methodology, was completed in one week.

I also understand that deployment is not the finish line. I have designed and delivered enterprise AI training programmes, including one for 40 non-technical staff at a Canadian engineering firm, with the explicit goal of enabling client teams to maintain and improve deployed systems independently. Getting to a stable handoff that the customer can own is something I plan for from the start of any engagement.

I would welcome the opportunity to discuss how my experience maps to what IFS is building.

Yours sincerely,

Oliver Day
```

- [ ] **Step 2: Create strategic_pm.md** (Miller letter)

`jobpilot/generation/examples/strategic_pm.md`:
```
Dear Hiring Team,

The goal Miller has set for this role, doubling revenue without doubling headcount, is the right frame for thinking about AI in an organisation. Not what AI can do in theory, but what it takes to make it stick at scale. That question is what draws me to this role.

From five years of deploying AI across enterprise clients, I have developed a clear view of what failure looks like: an AI team that becomes the bottleneck, initiatives that do not connect to measurable outcomes, and adoption that stops at the enthusiasts. What success requires is systematic experimentation with real governance behind it and front line teams equipped to run their own workflows. Building that infrastructure inside a specialist broker is exactly the problem I want to work on.

I have worked across financial services and insurance clients on prompt orchestration, conversation analysis, and production quality monitoring, enough exposure to regulated, client-facing environments to understand the constraints without overstating my insurance domain depth.

I combine that delivery experience with the strategic and stakeholder dimensions the role requires. I have run hands-on AI enablement programmes for non-technical teams, translated ambiguous business problems into scoped technical solutions, and operated across the full lifecycle from business case through to handoff and adoption measurement. The blend of hands-on delivery and strategic leadership the JD describes is how I already work.

I would welcome the opportunity to discuss how my experience maps to what Miller is building.

Yours sincerely,

Oliver Day
```

- [ ] **Step 3: Create enablement.md** (Everfield letter)

`jobpilot/generation/examples/enablement.md`:
```
Dear Hiring Team,

The Everfield AI enablement role is one of the most directly aligned opportunities I have seen to what I actually do: go into organisations, show people what is possible with AI, build working things alongside them, and stay until it sticks. That description maps closely to the last three years of my work, and it is why I am applying.

My background sits at the intersection of technical AI delivery and enablement. At HumanFirst I have designed and deployed LLM-powered systems for enterprise clients across insurance, financial services, and telecommunications, and delivered hands-on AI training programmes to technical and non-technical teams alike. A programme for 40 non-technical staff at a Canadian engineering firm moved participants from zero to building and maintaining their own AI workflows in two months, with over 60% sustaining weekly usage.

On the technical side, I work across the full stack of tools the role requires. I build agentic pipelines in LangGraph and n8n, design prompt evaluation frameworks, work with RAG systems, and have hands-on experience with Claude Code and AI-augmented development workflows.

I am aware that my experience sits above the stated range for this role. I would rather be transparent about that than pretend otherwise. What it means in practice is that Everfield gets someone who can operate independently from day one and compress the ramp across portfolio companies. What I am genuinely looking for is the Everfield enablement model itself: working across an entire portfolio, learning how AI adoption gets driven at scale across diverse organisations, and developing that craft under someone who has already built it. That is not something I can get anywhere else.

I am excited about the Everfield model and would welcome the opportunity to talk about how I can contribute.

Yours sincerely,

Oliver Day
```

- [ ] **Step 4: Create stub files for solutions_engineer.md and ai_engineer.md**

Both are copies of `builder.md` for now, to be replaced when real example letters exist.

`jobpilot/generation/examples/solutions_engineer.md` — copy of builder.md content (same text as Step 1).

`jobpilot/generation/examples/ai_engineer.md` — copy of builder.md content (same text as Step 1).

- [ ] **Step 5: Commit**

```bash
git add jobpilot/generation/examples/
git commit -m "Add branch example cover letters (stubs for solutions_engineer, ai_engineer)"
```

---

### Task 2: Create generation/prompts.py

**Files:**
- Create: `jobpilot/generation/prompts.py`

All four templates use `.format()` substitution. Any `{` or `}` that is NOT a template variable is written as `{{` or `}}`.

- [ ] **Step 1: Write failing test for CLASSIFY_PROMPT**

Create `jobpilot/tests/test_prompts.py`:

```python
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
```

- [ ] **Step 2: Run test to confirm it fails**

```bash
cd /home/ubuntu/source/career_planning/jobpilot && python -m pytest tests/test_prompts.py -v 2>&1 | head -30
```

Expected: ImportError or ModuleNotFoundError for `generation.prompts`.

- [ ] **Step 3: Create jobpilot/generation/prompts.py**

```python
CLASSIFY_PROMPT = """You are classifying a job description to determine the primary role type.

Read the job description below and identify which of the following role types it most closely represents:

- builder: Hands-on delivery, shipping automations, fast iteration, minimal process, forward deployed engineering
- solutions_engineer: Customer-facing technical work, scoping, POCs, translating problems into solutions
- enablement: Embedding AI adoption across teams, training, coaching, change management
- ai_engineer: Technical depth, production systems, architecture, evaluation frameworks
- strategic_pm: Programme leadership, prioritisation, stakeholder management, governance, business outcomes

Job Description:
{jd_text}

Respond with JSON only. No other text, no markdown, no code fences:
{{"role_type": "<one of the five keys above>", "reasoning": "<one sentence explaining why>"}}"""


DRAFT_PROMPT = """You are a professional cover letter writer. Produce a single cover letter and nothing else.

## Role Context
{role_context}

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
   - State what {candidate_name} brings to the specific problem this company is solving — in plain, concrete language. No stacking of abstract noun phrases ("production-grade agentic architecture, rigorous evaluation methodology, and…"). One clear claim.
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

The example below shows the tone, structure, and level of specificity to aim for. Do not copy it — use it to calibrate voice and argument density.

{example_letter}

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


CRITIC_PROMPT = """You are a sharp, experienced editor — the kind who has read thousands of cover letters and has zero patience for wasted words, false modesty, or empty enthusiasm. Your job is not to be cruel, but to be honest in a way that actually helps.

You will be given a job description and a cover letter. Read both carefully. Then edit the letter like a real editor would: with a red pen, strong opinions, and the candidate's best interests at heart.

Your critique should feel like notes from a trusted mentor who wants the candidate to get the job. Be direct. Be specific. Quote the letter back to the candidate when something isn't working.

## Role Context
{role_context}

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
OVERALL: [Pass | Minor revisions | Major revisions]"""


REWRITE_PROMPT = """An editor has reviewed a cover letter draft and produced the feedback and rewrite brief below. Your job is to write the final version using that brief as your guide.

## Role Context
{role_context}

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
```

- [ ] **Step 4: Run tests to confirm they pass**

```bash
cd /home/ubuntu/source/career_planning/jobpilot && python -m pytest tests/test_prompts.py -v
```

Expected: 5 tests pass.

- [ ] **Step 5: Commit**

```bash
git add jobpilot/generation/prompts.py jobpilot/tests/test_prompts.py
git commit -m "Add prompts.py with classify/draft/critic/rewrite templates and tests"
```

---

### Task 3: Update cover_letter.py

**Files:**
- Modify: `jobpilot/generation/cover_letter.py`

- [ ] **Step 1: Write failing tests for classify() and _load_example()**

Add to `jobpilot/tests/test_cover_letter.py` (create new file):

```python
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
    role_type, reasoning = classify(mock_client, "google/gemma-4-26b-a4b-it", "Build fast AI tools")
    assert role_type == "builder"
    assert reasoning == "Hands-on delivery role."


def test_classify_falls_back_on_invalid_json():
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices[0].message.content = (
        "I think this is a builder role."
    )
    role_type, reasoning = classify(mock_client, "google/gemma-4-26b-a4b-it", "Build fast AI tools")
    assert role_type == "builder"
    assert "Classification failed" in reasoning


def test_classify_falls_back_on_unknown_role_type():
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices[0].message.content = (
        '{"role_type": "wizard", "reasoning": "Magic role."}'
    )
    role_type, reasoning = classify(mock_client, "google/gemma-4-26b-a4b-it", "Do magic")
    assert role_type == "builder"


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
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
cd /home/ubuntu/source/career_planning/jobpilot && python -m pytest tests/test_cover_letter.py -v 2>&1 | head -30
```

Expected: ImportError — `classify`, `_load_example`, `VALID_ROLE_TYPES` not yet defined.

- [ ] **Step 3: Add imports, constants, classify(), and _load_example() to cover_letter.py**

At the top of `cover_letter.py`, add the import:
```python
import re
from generation import prompts
```

After the existing imports (before `_UK_INDICATORS`), add:
```python
VALID_ROLE_TYPES = {"builder", "solutions_engineer", "enablement", "ai_engineer", "strategic_pm"}

_EXAMPLES_DIR = Path(__file__).parent / "examples"
```

After `_strip_planning()`, add these two new functions:
```python
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
```

**Note:** `_call_model` is defined later in the file. Move `classify` and `_load_example` to after `_call_model`, or forward-reference is fine in Python since they're not called at module load time. Place them after `_call_model` to be safe.

- [ ] **Step 4: Run tests to confirm they pass**

```bash
cd /home/ubuntu/source/career_planning/jobpilot && python -m pytest tests/test_cover_letter.py -v
```

Expected: all 7 tests pass.

- [ ] **Step 5: Update _build_prompt() to use prompts.DRAFT_PROMPT**

Replace the existing `_build_prompt` function body with:

```python
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
```

- [ ] **Step 6: Update _build_critic_prompt() to use prompts.CRITIC_PROMPT**

Replace the existing `_build_critic_prompt` function body with:

```python
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
```

- [ ] **Step 7: Update _build_rewrite_prompt() to use prompts.REWRITE_PROMPT**

Replace the existing `_build_rewrite_prompt` function body with:

```python
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
```

- [ ] **Step 8: Update generate() to classify and load example before building prompts**

In `generate()`, after the existing setup (after `is_uk = _is_uk_role(...)` and before `draft_prompt = _build_prompt(...)`), insert:

```python
    # Classify JD and load branch example
    classify_model = config.pipeline_scoring_model
    role_type, reasoning = classify(client, classify_model, jd_text)
    role_context = f"Role classification: {role_type} — {reasoning}"
    example_letter = _load_example(role_type)
    print(f"  classified as: {role_type} — {reasoning}", flush=True)
```

Then update the three `_build_*` calls to pass `role_context` and (for draft) `example_letter`:

```python
    draft_prompt = _build_prompt(
        company, role, jd_text, cv_content,
        projects_content, snippets_content, config, is_uk,
        role_context=role_context,
        example_letter=example_letter,
    )
```

```python
    critic_prompt = _build_critic_prompt(draft, jd_text, role, company, role_context=role_context)
```

```python
    rewrite_prompt = _build_rewrite_prompt(
        draft, critique, draft_prompt,
        cv_content, projects_content, snippets_content,
        role_context=role_context,
    )
```

Also move the `client = OpenAI(...)` line to before the classify call (it's currently after `is_uk`). The client is needed by `classify()`.

The full updated section of `generate()` from `is_uk` to the first model call should read:

```python
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
```

- [ ] **Step 9: Run all tests**

```bash
cd /home/ubuntu/source/career_planning/jobpilot && python -m pytest tests/ -v
```

Expected: all tests pass.

- [ ] **Step 10: Commit**

```bash
git add jobpilot/generation/cover_letter.py jobpilot/tests/test_cover_letter.py
git commit -m "Add classify() and _load_example() to cover_letter.py, wire into generate()"
```

---

### Task 4: Smoke test end-to-end

**Files:** none new

- [ ] **Step 1: Run the existing __main__ block**

```bash
cd /home/ubuntu/source/career_planning/jobpilot && python -m generation.cover_letter 2>&1
```

Expected output includes a line like:
```
  classified as: ai_engineer — The role requires production system architecture and evaluation frameworks.
  [0/classify] google/gemma-4-26b-a4b-it: 2.3s
  [1/draft] moonshotai/kimi-k2.5: 8.1s
  [2/critic] moonshotai/kimi-k2.5: 12.4s
  [3/rewrite] moonshotai/kimi-k2.5: 9.7s
```

Followed by the generated cover letter.

- [ ] **Step 2: Verify no regressions in the Streamlit UI**

```bash
cd /home/ubuntu/source/career_planning/jobpilot && nohup streamlit run app.py --server.port 8501 > /tmp/jobpilot.log 2>&1 &
```

Open browser to `http://localhost:8501`, navigate to cover letter generation, generate one letter end-to-end, confirm it completes without error.

- [ ] **Step 3: Final commit**

```bash
git add -A
git commit -m "Cover letter classification pipeline — complete"
```
