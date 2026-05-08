# Behavioural Interview Question Bank
*Calibrated for: Economist (Round 2), Wise (Round 1), Accenture / Baringa / Argus / SuperAwesome (screening)*

---

## 1. Building an Agent End-to-End

**"Walk me through an agent you built — from the initial problem to production."**

- Name the business problem first (not the tech stack) — what was failing or missing without automation?
- Describe one real design decision you made and the alternative you rejected (e.g. agent vs chain, n8n vs LangGraph)
- Name a specific failure mode you encountered during build and how you handled it
- State what "production" looked like — scale, reliability, observability, not just "it worked"
- Connect the engineering pattern to something the interviewer's company would recognise

---

**"What were the hardest engineering decisions you made in [pipeline / agent]?"**

- Lead with the decision, not the context — "I chose X over Y because…"
- Name the tradeoff explicitly: what you gained and what you gave up
- Show you'd make the same call again (or explain why you'd do it differently)
- Reference at least one failure mode you were designing against
- Don't use jargon — explain it in terms of what went wrong or right in practice

---

**"How do you decide what should be an agent vs a simple prompt vs a chain?"**

- State your default: simplest structure that solves the problem
- Give a clear criterion for upgrading from prompt → chain (genuinely separable stages)
- Give a clear criterion for upgrading from chain → agent (routing unknown in advance)
- Reference the LinkedIn Post Agent as the "looks like an agent but isn't" example — deterministic routing
- Mention why you're conservative about agents: non-determinism, harder to test, harder to audit

---

**"How do you instrument and monitor an LLM pipeline after deployment?"**

- LangSmith (or equivalent) per-node tracing goes on before first live run, not after
- Name the specific metrics you track: score distribution, latency per node, error rate by node, input distribution drift
- Explain how you detect silent failures (plausible-but-wrong outputs that don't raise errors)
- Describe the feedback loop: how production failures feed back into the test set
- Make clear monitoring is a design decision made before build, not bolted on after

---

## 2. Evaluation Frameworks

**"How do you build an eval framework when there's no clear ground truth?"**

- Replace ground truth with expert consensus — find 3–5 domain experts, measure where they agree
- The agreement cases become your labelled dataset; the disagreement cases get escalated, not automated
- Describe how you used inter-annotator agreement as your benchmark (insurance work: 84% agreement)
- Distinguish pointwise vs pairwise: pairwise for prompt iteration, pointwise for ongoing monitoring
- Emphasise: eval is never finished — production failures extend the dataset

---

**"What makes a good LLM judge prompt?"**

- Criteria decomposition first: don't ask "is this good", ask one specific thing at a time
- Chain-of-thought before verdict: ask for evidence before score so you can audit the reasoning
- Calibration against human baseline — the prompt isn't done until you've measured agreement rate
- Name the known failure modes: verbosity bias, position bias, self-preference, calibration drift after model upgrades
- For editorial/voice quality: use exemplars in the rubric (show, don't describe)

---

**"How do you validate an AI system before shipping it to real users?"**

- Gate 1: passes eval suite against labelled test set including edge cases — if no suite, it's still a prototype
- Gate 2: 30–50 real-world inputs not in the test set; failures from this phase get added to the dataset
- Gate 3: observability live before first user — traces, logs, score distribution monitoring
- Gate 4 (for sensitive use cases): human review phase on first 50–100 outputs post-launch
- Underlying principle: pre-launch validation hours are worth more than post-launch incident response days

---

## 3. Stakeholder Management and Alignment

**"Tell me about a time you had to get a sceptical team to trust an AI system."**

- Start from their output, not your tooling — ask them to bring work they're proud of and work they think is poor
- Surface failure modes before they find them; show where the system gets it wrong proactively
- Build the eval framework around their judgment, not an external metric they didn't define
- Reference the 40-person engineering firm enablement programme — specific, credible, transferable
- Show how trust was earned over time, not assumed from the start

---

**"How do you keep stakeholders aligned when requirements change mid-project?"**

- Distinguish between requirements changing and goals shifting — different responses
- Describe how you document a specific success criterion before any build starts
- Give an example of surfacing a misalignment early enough to avoid rework (not after the demo fails)
- Mention that frequent small check-ins with a shared working document beats a big reveal
- For AI work specifically: show how you use the eval framework as a shared alignment artifact

---

**"How do you work with domain experts who can't articulate the rules they're applying?"**

- The rule is implicit — treat their decisions as ground truth, not their stated criteria
- Run structured labelling sessions: give them inputs, observe their classifications, measure agreement
- Ask "what makes this case hard?" to surface the edge case logic they never had to articulate before
- Never try to extract the rubric directly — build it inductively from labelled examples
- Reference the insurance analyst work and the connection to editorial judgment at The Economist

---

**"Describe a time you influenced a technical direction without formal authority."**

- Name the specific thing you disagreed with and why (not just "I had a different view")
- Describe the approach you took: evidence before argument, not argument alone
- Show you did something visible rather than wrote a memo — ran one project differently and let the outcome argue
- The influence came from the track record, not the position
- Reference the prompt-first methodology emerging from practice at HumanFirst

---

## 4. Handling Ambiguity

**"Tell me about a time you had to drive a project with no clear direction."**

- Start with how you made the implicit goal explicit — from "build X" to a specific measurable statement
- Name the thing you decided not to solve — scope management under ambiguity is as important as what you built
- Describe the smallest-first approach: the two-day prototype that gave signal before committing to the full build
- Explain how you defined success before you built anything, even when no one asked you to
- Reference the LinkedIn outreach pipeline as the clearest example of solo-defined problem → solo-built solution → measurable outcome

---

**"How do you decide what to do first when a new role or project has no defined roadmap?"**

- Listen and map first — don't build anything in the first weeks until you understand the existing processes
- Identify the highest-confidence candidate: most consistent decisions, most structured inputs, most recoverable failures
- Name a principle for prioritisation (e.g. decision consistency + input structure + failure cost)
- Show you can produce a prioritised list from first principles, not wait for a brief
- Reference the Wise 30/60/90 approach: first 30 days you're not building anything

---

**"How do you handle it when the scope keeps expanding?"**

- Name the mechanism you use to hold scope: a written success criterion agreed before build starts
- Distinguish "nice to have" additions from things that change what success looks like
- Give a specific example where you pushed back on scope and explained why
- Show you understand scope creep in AI work specifically: "and then evaluate it" is always more work than estimated
- Mention the cost of scope creep in agentic pipelines — more steps = more failure modes = exponentially harder to test

---

## 5. Feasibility and Scoping

**"How do you assess whether something is a good candidate for AI automation?"**

- Three filters: decision consistency, input structure, failure cost — apply them in order
- Decision consistency: would two experienced people usually agree? If not, the task isn't ready to automate
- Input structure: does the agent have all the information it needs, or is important context implicit or verbal?
- Failure cost: is the failure mode recoverable? If not, keep humans in the loop for that step
- Mention the KYC/financial crime example as a case study: binary decisions, structured inputs, recoverable routing failures

---

**"How do you explain to a non-technical stakeholder why something they want to automate is harder than it looks?"**

- Start with what they can observe: "this decision looks simple from the outside because you've internalised all the context"
- Name the three things that make automation hard: implicit rules, unstructured inputs, high-cost failures
- Give a concrete example of a case where the edge case isn't rare — it's 20% of the volume
- Don't promise to automate — promise to define what "automatable" means for their process and measure it
- Offer the assist-mode approach: show the agent's classification alongside the human decision for 4 weeks before removing the human

---

**"How do you decide when to use an existing tool vs build something custom?"**

- Simplest tool first: use the lowest-complexity option that solves the problem reliably
- Name the cost of custom: maintenance, debugging surface area, onboarding friction for the next person
- Name the cost of an off-the-shelf tool: vendor lock-in, limited observability, slower iteration
- Give a real example of where you used the simpler tool (n8n vs LangGraph for linear workflows)
- Mention the Google Agentspace/Credal discussion as an example of how infrastructure context changes the answer

---

## 6. Failure and Recovery

**"Tell me about an AI system you built that failed in production."**

- Name the failure specifically — not "it didn't work" but the exact mechanism (cumulative latency, silent tool call error, etc.)
- Describe the detection story: how did you find out? (shows whether you had observability or found out from a user)
- Walk through the fix: what changed architecturally, not just what you patched
- State the lesson: what would you build differently from the start next time?
- Reference the Supabase timeout failure — chained LLM calls at production scale, latency is multiplicative not additive

---

**"What do you do when an eval shows your pipeline is failing on a class of inputs you didn't anticipate?"**

- Treat it as information, not a crisis — these are the most valuable cases you'll add to your dataset
- Categorise the failures before fixing: are they a prompt issue, a data issue, or an architecture issue?
- Don't fix the prompt to pass the failing cases — fix it to pass the failing cases without degrading the cases it was already passing
- Run the updated prompt against the full labelled set before deploying, not just the new failures
- Tell the relevant stakeholder immediately: they trust a team that surfaces failures, not one that hides them

---

## 7. Career Narrative and Motivation

**"Why are you moving from consulting/client work to an internal role?"**

- First reason (real): client work means handing over and losing visibility — the most interesting part (what breaks at scale over time) is invisible to you
- Second reason (real): the compounding is different — internal infrastructure keeps improving; client work knowledge scatters across engagements
- Connect to the specific role: name why this company's problem is the one you want to own long-term
- Don't over-explain — two genuine reasons are stronger than four engineered ones
- Demonstrate you understand the transition: internal roles have different stakeholders, longer timelines, less defined briefs

---

**"Why do you want to work here specifically?"**

- Open with something specific from the research — a product decision, a funding milestone, something someone said publicly
- Avoid generic mission-alignment language — connect their current moment to your specific experience
- Name the problem they're trying to solve and why your background maps onto it
- Make it directional: "this is the problem I want to work on for the next three years" rather than "I admire your work"
- Close with a question that signals you've done more than surface research

---

**"What kind of work do you do best?"**

- Name the specific layer: the gap between "working prototype" and "production-reliable system"
- Describe the conditions: small team, open mandate, direct access to domain experts, real data
- Give evidence that this positioning is based on track record, not preference (the pipeline work, the eval frameworks)
- Be honest about what you don't do best (dense Python from scratch, pure research) — it increases the credibility of what you do claim
- Connect to the role: "which is why this role fits — the [specific mandate] is exactly that layer"

---

**"Where do you want to be in three years?"**

- Don't answer with a job title — answer with a type of problem or a type of capability
- Connect it to a genuine trend you believe in (the gap between demo and production-grade AI at scale)
- Show it's directional, not a step up from your current role — "I want to be the person who has shipped X at Y scale"
- For engineering roles: mention wanting to own the full lifecycle of a deployed system over time
- For strategy/consulting roles: mention wanting to build a methodology that survives beyond individual client engagements

---

## 8. The AI-Specific Questions (Now Standard)

**"How do you make sure an AI system behaves consistently in production?"**

- Consistent behaviour requires narrow action spaces — more tools and more general instructions = more variance
- Validation gates between pipeline steps prevent error compounding
- Prompt versioning and logging: the current prompt must be traceable to any output, not just the code
- Score distribution monitoring: if average output quality starts drifting, something upstream changed
- Regular sample audits: randomly pull N outputs per week for human review; this catches silent failures that metrics miss

---

**"What's the hardest part of getting an AI pilot to become a production system?"**

- It's not the model — it's the trust infrastructure around it
- Governance: who owns the agent's decisions? What's the audit trail? Who reviews edge cases?
- Ops team adoption: the team whose workflow changes is the critical path, not the engineering team
- Failure handling: what does the system do when it's uncertain? A pilot that fails silently is worse than no automation
- Eval infrastructure: without a labelled dataset and a quality gate, there's no mechanism to improve it over time
- Reference the ~25% of orgs stat: most pilots don't make production, and the reason is almost never the model

---

**"How do you think about when to keep a human in the loop?"**

- Default: keep humans in the loop until you have measured confidence data that justifies removing them
- Threshold logic: above-confidence-threshold decisions run autonomously; below-threshold go to a human with the agent's reasoning surfaced
- Non-negotiable escalation: high-cost failures (compliance violations, irreversible actions) always have a human gate regardless of confidence
- Assist mode first: deploy the agent alongside the human, measure agreement for 4–6 weeks, then make the case for removing the loop
- Regulators and auditors: in regulated contexts, the audit trail and escalation logic need to be there from day one, not added after

---

*Last updated: 2026-05-07*
