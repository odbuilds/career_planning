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
