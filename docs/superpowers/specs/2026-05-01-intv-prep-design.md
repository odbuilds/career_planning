# intv-prep Skill — Design Spec
**Date:** 2026-05-01

---

## Overview

A Claude Code skill that generates a comprehensive interview prep document for a given role. The user provides a job description (URL or pasted text) and the skill researches the company, analyses the JD, pauses for human-sourced LinkedIn intel, then writes a structured prep file to `intv/`.

---

## Invocation

```
/intv-prep https://jobs.lever.co/company/role-id
/intv-prep [pasted JD text]
```

If invoked with no argument, the skill prompts: *"Paste the JD or drop a link."*

---

## Profile Sources

The skill reads the following to personalise all output:

- `jobpilot/profile.yaml` — structured skills, experience, background
- Most relevant CV from `cvs/` — inferred from role type (e.g. `cv_agentic.md` for AI roles, `cv_consulting.md` for advisory roles)
- `intv/interview_strategies.md` — Oliver's named strategies and tactics

---

## Research Pipeline

Steps run in order with visible progress messages.

### Step 1 — JD Analysis
Extract from the JD:
- Role title and company name
- The **one core problem** this hire is meant to solve
- The **3 key skills** to evidence in the interview
- Whether the company is a startup (informs Step 4)
- Any named hiring manager

### Step 2 — Company Research
WebSearch + WebFetch:
- Who they are, what they sell, business model
- Ideal and current customer profile
- The core problem they solve and their differentiation

### Step 3 — Key People Research
WebSearch for CEO, CTO, and any named hiring manager:
- Background and tenure
- Recent interviews, podcasts, conference talks
- Stated company strategy, priorities, and challenges
- Anything directly relevant to the role

### Step 4 — Recent News & Company Signals
WebSearch for last 3–6 months:
- Product launches, pivots, partnerships, press
- If startup: Crunchbase funding data, round size, investors, any pivot signals or runway concerns

---

## Pause Point

After automated research completes, the skill pauses and prompts:

> *"Research done. Before I write the doc, I need a few things from you:*
> *1. Hiring manager's LinkedIn URL (required)*
> *2. Any posts, comments, or content from them you want me to factor in (optional — paste directly)*
> *3. Any feedback from a previous round with this company (optional)*
>
> *[Checking intv/ for a prior file from this company...]*
> *Found: `intv/25-04-22-cosuno.md` — should I reference it?"*

The skill then:
- Fetches the LinkedIn profile via WebFetch
- Reads any pasted posts and synthesises the hiring manager's stated priorities, language, and concerns
- Loads previous round feedback if provided
- Loads the prior interview file if the user confirms

---

## Output File

Written to `intv/YYYY-MM-DD-<company-slug>.md`

### Document Sections

#### 1. Company Snapshot
Key facts: founded, stage, size, funding, product, customers, business model. Dense reference block — the kind of thing to skim the morning of the interview.

#### 2. The One Thing
The single core problem this hire is meant to solve, stated plainly. This is the frame for the entire interview — everything else should connect back to it.

Then: the **3 key skills to evidence**, each with a one-line explanation of why it matters for this role.

#### 3. Key People
One section per person (CEO, CTO, hiring manager if distinct). For each:
- Role, background, tenure
- What they've said publicly about strategy and challenges
- What to know before you're in the room with them

#### 4. Hiring Manager Intel
Synthesised from LinkedIn profile and any provided posts:
- What they're focused on right now
- Language and framing they use
- Any stated frustrations or challenges
- How to mirror their register without losing your voice

#### 5. Interview Strategy
One recommended strategic posture drawn from `intv/interview_strategies.md`, with:
- Which strategy fits this role and why
- How to open with it
- How to sustain it across different question types
- If a previous round was referenced: whether to shift strategy or double down

#### 6. Handling Weaknesses
Cross-reference Oliver's profile against the JD requirements. For each meaningful gap:
- Name the gap plainly
- Suggest a specific framing that acknowledges it without undermining confidence
- Provide a pivot to adjacent strength

If previous round feedback is provided, address it explicitly here.

#### 7. Tell Me About Yourself
A scripted answer (2–3 minutes spoken) that:
- Opens with the outcome/identity, not the chronology
- Is anchored to the one core problem from Section 2
- References specific, credible work
- Closes with a clear "why this role, why now" that connects to company research

#### 8. Why This Company / Why Now
A scripted answer to "why us?" that:
- Is grounded in specific research (recent news, funding moment, product direction, something the CEO said)
- Avoids generic praise
- Connects the company's current moment to Oliver's specific interests and skills

#### 9. Ten Expected Questions
The 10 questions most likely to come up for this role, each with:
- Why they're asking it (the underlying concern)
- A best-practice answer customised with Oliver's specific experience and the company context
- Format guidance (STAR or PCR as appropriate, drawn from existing prep file conventions)

#### 10. Questions to Ask Them
3–5 sharp questions Oliver can ask the interviewer that:
- Signal the homework has been done
- Advance the chosen strategy
- Surface information useful for evaluating the role

Flagged as: strategic (advance the posture), diagnostic (evaluate fit), or signal (demonstrate thinking).

#### 11. 30-60-90 Day Sketch
A rough outline of what Oliver would actually do in the first three months:
- Days 1–30: orient, listen, identify the highest-leverage problems
- Days 31–60: first concrete moves, early wins
- Days 61–90: longer-horizon bets, how success is measured

Customised to the role and company context from research.

#### 12. Watch-Outs
Red flags to monitor during the interview, with suggested approaches:
- Seniority mismatch (role too junior or too senior vs. how it's being pitched)
- Role ambiguity (unclear mandate, multiple hiring managers, no clear success metric)
- Company signals (funding concerns, pivot risk, cultural friction)
- Anything specific surfaced in the research
- If referencing a prior file: unresolved concerns carried forward

---

## Skill File Location

`~/.claude/skills/intv-prep/SKILL.md`

---

## Non-Goals

- This skill does not run a mock interview or coaching session — that is a separate skill
- It does not score or rank roles — that is JobPilot's job
- It does not update the database or interact with any app
