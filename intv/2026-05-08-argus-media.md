# Argus Media — Senior AI Automation Engineer
**Date:** 2026-05-08
**Stage:** First interview

---

## Section 1: Company Snapshot

**Founded:** 1970 | **HQ:** London, UK | **Private** (employee shareholders + General Atlantic majority; Hg exited 2024)
**Size:** ~2,000 employees | **Offices:** 31 globally
**Revenue:** ~$320M (2026) | **Revenue growth:** 17% YoY (FY2023); energy transition products +46%

**What they do:** Independent provider of price assessments, market intelligence, news, and analytics for global energy and commodity markets. Publishes 40,000+ commodity prices used as reference benchmarks in physical contracts, derivatives, swaps clearing, royalties, and project finance. Coverage spans oil, gas, power, petrochemicals, metals, and rapidly expanding energy transition commodities (SAF, lithium, hydrogen).

**Business model:** Subscription data and intelligence (B2B SaaS-style), consulting services, and industry conferences. Customers are trading firms, energy companies, governments, and financial institutions in 160 countries.

**Customers:** Trading desks, energy procurement teams, risk managers, and policy bodies that need trusted price benchmarks and market context for high-stakes financial and operational decisions.

**Ownership moment (2024):** In January 2024, Hg (PE firm) exited its stake. CEO Adrian Binks (who has led the company since 1984) became majority owner, with General Atlantic retaining a large minority. This signals Argus is positioned for continued long-term independent growth — not an exit-driven company, not a fast-pivot startup.

**AI direction:** January 2026 — Argus partnered with Snowflake to deliver "AI-ready data" to energy companies, signalling the company is actively making its data infrastructure machine-readable and analyst-grade AI tooling a product direction.

**The role:** Internal-facing Senior AI Automation Engineer building Copilot Studio / Power Automate workflows that boost team productivity across Argus's ~2,000-person organisation. One direct report to mentor.

---

## Section 2: The One Thing

**The core problem this hire solves:** Argus's journalists, analysts, and operations staff are generating and processing 40,000+ data points daily across 31 offices using workflows that still rely heavily on manual effort — and without someone who can translate those messy processes into reliable, owned AI automation, productivity gains from the AI wave stay theoretical.

**Three key skills to evidence:**

1. **Production AI assistants/agents that have been built and maintained** — The JD explicitly says "used in production," not just prototyped. This is the primary filter. Your LinkedIn pipeline and insurance eval framework are the evidence.

2. **Microsoft stack fluency (Power Automate, Copilot Studio, APIs)** — The tools are named and required. Your stack is different. This is the critical gap to address directly and confidently without being defensive.

3. **Owning solutions post-launch** — "Own solutions after launch improving reliability, usability and performance" is rare language for a JD. They've been burned by people who build and move on. Your prompt-first methodology and monitoring-by-design approach are the direct answer here.

---

## Section 3: Key People

### Adrian Binks — Chairman and CEO

Took management control of Argus in 1984 and built it from a small publication into a $320M global data business. Won EY International Entrepreneur of the Year 2017. Still majority owner post-2024 ownership consolidation. Not an investor-driven CEO — he's a founder-operator who's been running this company for 40 years.

**Public framing (Dec 2025):** On 2026 commodity market outlook: *"The world has grown used to the remarkable resilience of commodities markets over the past three years. But the challenges of 2026 look set to shake things up in a way not seen since Russia went into Ukraine."* Also: *"Our mission to bring transparency to these markets remains unchanged"* — mission-first language, not growth-at-all-costs.

**What to know:** Adrian won't be in your interview, but his framing matters. Argus is not a company trying to sell itself. It is a company trying to serve its customers better for the next 40 years. Internal AI automation is in service of that: better analyst productivity means better coverage, faster insights, more comprehensive data. Frame any automation conversation in terms of analyst/journalist quality of output, not headcount efficiency.

### CTO / Engineering Leadership

*[No specific public information found for Argus Media's CTO or Head of Engineering after two search attempts. Their engineering team operates relatively quietly given the company's B2B data focus. Research on LinkedIn before the interview — look for "Head of Technology" or "VP Engineering" at Argus Media to understand whether the interview panel will be product/engineering-led or ops/IT-led.]*

---

## Section 4: Hiring Manager Intel

*[No LinkedIn data provided — research manually before the interview. Key things to find: is the hiring manager from an engineering/IT background or from the commodity markets business side? That distinction changes the interview tone significantly. If they're from IT/engineering, lean technical. If they're from the business side, lead with outcomes and reliability. Look for their current focus — are they building out a new function, or expanding an existing one? Is this the first AI automation hire or part of a growing team?]*

---

## Section 5: Interview Strategy

**Recommended strategy: Solution Provider**

Why it fits: Argus is hiring someone to own solutions — the word "own" appears explicitly in the JD. They're not hiring a contractor who builds and moves on. Walking in with a clear methodology for how you approach automation problems, take them to production, and keep them reliable over time directly addresses the hiring concern. You should be able to describe your approach to AI automation work before they ask you to.

**How to open:** In the first two minutes, after the initial pleasantries, say something like: *"Before we get into questions I want to say — I've spent time thinking about what this role actually involves, and I have a specific view on where AI automation tends to succeed in an organisation like Argus and where it tends to stall. I'd love to test that against what you've seen internally."* This signals preparation, positions you as someone with genuine opinions, and invites them to share the real problem.

**How to sustain it across question types:**

- For experience questions: connect your evidence directly to Argus's operational reality. Not "I built a pipeline" but "I built a pipeline for a team whose entire job was analysing large volumes of structured data — the same challenge your analysts have with commodity price and news workflows."
- For tooling questions (Power Automate / Copilot Studio gap): lead with your position on the underlying problem before you address the specific tool. "My view on automation tooling is that the choice should follow the complexity of the workflow — simpler tools for linear processes, more powerful orchestration for stateful multi-step work. I've operated at both ends of that. The specific tools here are learnable quickly; the judgment about which approach to use is what takes time to develop."
- For "why Argus" questions: the Snowflake AI-ready data partnership, the mission-first culture, and the internal productivity mandate all provide genuine hooks.

---

## Section 6: Handling Weaknesses

**Gap 1: Microsoft stack (Copilot Studio, Power Automate, Microsoft Graph)**

This is the most significant gap. The JD lists these as essential requirements, and your production stack is LangGraph, n8n, Claude/OpenAI APIs, LangSmith. You have not built in Copilot Studio or Power Automate.

*Framing:* "I want to be direct about this. My production automation stack has been LangGraph and n8n rather than the Microsoft Power Platform. The underlying engineering patterns — agent orchestration, API integration, output validation, post-launch monitoring — are the same problems; the tools are different. I've learned new automation frameworks quickly before — I moved from sequential prompt chains to LangGraph's stateful graph architecture in under a week because I approached it by mapping the design first and then learning the primitives. I'd apply the same approach to Copilot Studio and Power Automate. The Microsoft tooling is learnable fast; the judgment about how to design reliable automations is what I've spent two years building."

*Pivot:* Your n8n work is the closest analogue — workflow automation with API integrations, conditional routing, and external service connections. Position n8n as the tool you use where Microsoft would use Power Automate. The architectural thinking transfers directly.

**Gap 2: OAuth / Microsoft Graph / permissions management**

Listed as a hard requirement. Your experience with permissions and auth is more generic (API key management, rate limiting, deduplication) than Microsoft-stack-specific.

*Framing:* "My auth experience is API-level rather than Microsoft Graph specifically — I've handled OAuth flows in the context of API integrations in my pipelines, but not specifically within the Microsoft 365 permission model. That's a specific gap. What I'm confident in is understanding why permissions management matters in enterprise automation — you don't want an agent accessing data the invoking user can't see, and you don't want automation silently failing because a credential expired. The Microsoft Graph layer is learnable; the underlying reason it matters is something I already know."

**Gap 3: CI/CD and version control as engineering fundamentals**

The JD asks for "engineering fundamentals: version control, CI/CD, automated testing." Your work has been more in the prompt engineering and pipeline architecture space than traditional software engineering. You use git and Claude Code to manage your work, but you're not a CI/CD practitioner.

*Framing:* "My version control practice is solid — I work with git and manage pipeline code properly. My CI/CD experience is lightweight: I've not been running deployment pipelines in the way a backend engineer would. For internal automation tools, the deployment cycle is typically more manual than a customer-facing product. What I've built instead is a testing and eval layer for AI outputs that catches quality regressions before they reach users — which I'd argue is the more valuable practice for AI automation work specifically, because the failure modes aren't compilation errors, they're silent quality degradation."

**Gap 4: Mentoring experience**

JD mentions "mentor one engineer." You haven't had direct reports, but you've led programmes and influenced technical practice.

*Framing:* "I haven't managed direct reports, but I've led technical programmes for teams — a 40-person AI enablement programme, cross-functional client workstreams where I was the technical lead. The skill of getting someone up to speed on a new technical approach, building their confidence on real outputs, and raising the quality of what they produce — that's something I've done repeatedly even if not in a formal line-management structure."

---

## Section 7: Tell Me About Yourself

*"My background is building AI systems that hold up in production — specifically the layer between a working prototype and something that a team can depend on day to day. I've spent the last two and a half years at HumanFirst working across enterprise clients where the problem isn't usually the AI model, it's whether the pipeline around it is reliable enough to trust.*

*The most directly relevant piece of work for this role is probably the analytics pipeline I built for a global insurance firm. They had 50,000+ customer-broker conversations flowing through their system each year, and a manual review process that was too slow and inconsistent. My job was to automate the classification at scale — but the real engineering challenge was building something the ops team would trust. That meant designing an evaluation framework from their own expert judgment, building quality gates that caught edge cases before they reached anyone, and setting up monitoring so we could see when the system was drifting before users noticed. That system is still running in production.*

*On the agentic side — I built a full outreach automation pipeline that processed 15,000+ profiles, ran qualification prompts, generated personalised content, handled rate limits and deduplication, and logged everything to a database for audit. Same fundamental architecture as the kind of internal workflows I'd be building at Argus: structured input, conditional processing, reliable output, owned and monitored over time.*

*The reason I'm interested in this specific role: Argus is a company that runs on precision data and trusted analysis. Internal AI workflows that help analysts produce better, faster outputs have to meet the same quality bar as the data itself. That's exactly the kind of AI automation I find most interesting to build — where the failure mode isn't 'the thing didn't run' but 'the thing ran quietly and produced something the user trusted but shouldn't have.' That's the harder problem, and it's the one I've spent my time on."*

---

## Section 8: Why This Company / Why Now

*"Argus just partnered with Snowflake to make its data AI-ready for energy companies — which tells me the organisation is thinking seriously about how AI tooling interacts with the data layer, not just about surface-level productivity. That's the kind of environment where internal AI automation work matters: there's institutional awareness of what it takes to make AI outputs trustworthy, not just functional.*

*The other thing I find compelling is the stability of the mandate. Argus has been independently run for 40 years, and Adrian Binks just consolidated majority ownership — this isn't a company that's about to pivot or get acquired. Building internal automation infrastructure that actually gets maintained and improved over time requires a stable platform. I've seen automation work stall when the company context shifts; the ownership structure here suggests that's not the risk.*

*And the problem — helping a team of journalists and analysts who work with high-precision data use AI without compromising the quality bar they've built careers around — that's exactly the kind of challenge where getting the trust layer right is as important as the engineering."*

---

## Section 9: Ten Expected Questions

---

**Q1: "Walk us through an AI automation you've built end to end."**
*Why they're asking:* The JD requires production experience. They want to verify it's real, not described.
*Format:* STAR

*Answer:*
"The most directly relevant is the outreach automation pipeline I built at HumanFirst. The business situation was that we'd lost our sales function and needed to rebuild pipeline without a team behind it.

The pipeline ran in n8n and LangGraph. It started with scraping LinkedIn for posts matching specific keywords relevant to our product, filtered to profiles matching target roles and company sizes. A generative AI step then qualified those profiles further — not everyone who posted about NLP was a genuine prospect, so the prompt was designed to distinguish people actively building with the technology versus people commenting on it generally. Once qualified, personalised outreach messages were drafted using Claude, with two content variants running in parallel for A/B comparison. Every result went into a Supabase database with deduplication logic to prevent repeat outreach to the same person.

The engineering challenges were mostly operational rather than model-related: rate limit handling across the scraping layer, quota management across API calls, and making sure the deduplication logic held under concurrent writes. The qualification prompt was where I spent the most time — getting it to reliably make the right distinction required a proper labelled test set and several rounds of iteration before I trusted it enough to run at scale.

Results: 70% connection rate, 40% response rate, 7% demo attendance — significantly better than what we'd been achieving manually. And the monitoring setup meant I could see when output quality drifted and adjust the prompts without touching the pipeline architecture.

For an Argus context — the same pattern applies to any internal workflow that involves taking structured data inputs, applying a classification or generation step, and routing the output reliably. The architecture transfers directly."

---

**Q2: "How do you approach converting a messy business workflow into a clean automation?"**
*Why they're asking:* The JD uses this exact phrase — it's a core job description. They want your methodology.
*Format:* PCR

*Answer:*
"My starting point is always the humans who do the work, not the workflow documentation — because what's written down is rarely what actually happens. I ask two questions: first, 'what's the most repetitive decision you make where the answer is almost always the same?' — that's the automation candidate. Second, 'what's the messiest case you regularly see, and what makes it hard?' — that tells me where the automation will fail and whether that failure is acceptable.

From there I apply three filters before I design anything. Decision consistency: would two experienced people almost always make the same call? If they frequently disagree, the task isn't ready to automate — or you need an escalation layer rather than full automation. Input structure: does the automation get everything it needs from the data available, or does it require implicit context, verbal context, or information outside the system? Unstructured required context is the thing that kills automation projects. And failure cost: what happens when the automation gets it wrong? High-cost failures need a human review gate; low-cost failures can run autonomously and be caught in batch audit.

The 'clean technical solution' part comes from being honest about scope. Messy workflows have exceptions that don't deserve automating — the 5% of cases that require real judgment should escalate to a human, not get forced through an automation that will fail on them. The value is in the 95% that are genuinely consistent. I'd rather ship a reliable automation that handles 90% of volume and escalates the rest than a comprehensive one that fails silently on 10%."

---

**Q3: "What's your experience with the Microsoft Power Platform and Copilot Studio?"**
*Why they're asking:* It's listed as essential. They need to know your real level.
*Format:* PCR

*Answer:*
"I want to be accurate about this rather than overstate it. My production automation stack has been LangGraph and n8n — I haven't built in Copilot Studio or Power Automate directly. That's a genuine gap on the tooling side.

What I can say is that the engineering problems are architecturally the same. N8n — where I've built multiple production pipelines — is a direct workflow automation equivalent to Power Automate. Both handle API integrations, conditional routing, and multi-step workflows with external service connections. Copilot Studio is Microsoft's take on the same agent orchestration problem I've handled in LangGraph. The underlying design decisions — when to route, how to handle failures, how to validate outputs before they reach users — those are what I've spent two years developing judgment on.

My experience learning new automation frameworks suggests I can be productive in the Microsoft stack quickly. When I moved from sequential prompt chains to LangGraph's stateful graph model, I gave myself a week, mapped the design on paper first, built the simplest possible working graph, and added complexity incrementally. I'd apply exactly the same approach to Copilot Studio and Power Automate.

The thing I'd want to be honest about: I'd arrive needing to build the Microsoft stack knowledge, not arriving with it. If there are Copilot Studio or Power Automate problems that need solving from day one without a ramp period, that's a conversation we should have. If there's a few weeks of learning while delivering in parallel, that's where I'd expect to operate."

---

**Q4: "How do you make sure an automation keeps working reliably after launch?"**
*Why they're asking:* "Own solutions after launch improving reliability, usability and performance" is explicit in the JD. They've had people who build and disappear.
*Format:* PCR

*Answer:*
"My principle is that monitoring goes on before the first real run, not after something breaks. For any automation in production, that means: structured logging on every significant step so you can trace what happened on a specific input, a quality metric that you can trend over time rather than check reactively, and an alerting mechanism for anomaly patterns — quality score distribution shifts, error rate spikes, latency outliers.

The monitoring approach I've developed specifically for AI automation is different from traditional software monitoring because the failures are often silent. A traditional software system crashes visibly. An LLM-based automation can run, complete, and return plausible-looking output that's quietly wrong. The only defence against that is score distribution monitoring — tracking the distribution of output quality over time so you see it drift before a user does.

The improvement loop I run: I treat production failures as test set additions. Every time an output is flagged as wrong — by a user, by monitoring, or by a random audit — that case goes into the labelled dataset. Over time, that dataset becomes the most valuable asset in the system: every edge case the real world produced that wasn't anticipated during build. I run the current prompt or workflow configuration against that growing dataset periodically; if performance on the new cases is lower than on the original set, something needs updating.

For Argus specifically, I'd want to understand how 'reliable' is defined for each workflow — is it 99% accuracy on output classification, is it latency, is it uptime? The monitoring strategy follows from what failure looks like, not from a generic template."

---

**Q5: "Tell me about a time you had to get a sceptical team to adopt a new AI tool or workflow."**
*Why they're asking:* Internal adoption is the real delivery challenge. They want to know you can bring people along.
*Format:* STAR

*Answer:*
"The clearest example is the AI enablement programme I ran for 40 non-technical staff at a Canadian engineering firm. The challenge wasn't hostility — it was informed scepticism. These were senior technical staff who knew their domain deeply, immediately spotted when an AI output was wrong in that domain, and had seen enough impressive demos that fell apart on their actual work to be appropriately cautious.

What worked: I started from their outputs, not my tooling. I asked each participant to bring two pieces of their own work — one they were proud of, one they thought was substandard. Those became the reference set for evaluating anything AI-generated. That immediately grounds the trust conversation in their judgment rather than in metrics they don't own or understand.

The second thing that worked was radical transparency about failure. Before anyone found a case where the AI was wrong, I showed them cases where it was wrong myself. If you surface the failure modes before the sceptic finds them, they stop looking for reasons to distrust the tool and start treating it as a known system with known limits. That's a fundamentally different and more productive relationship.

The result was that 40 people moved from sceptical to active users over the course of the programme — not because I convinced them, but because I earned their trust by treating their judgment as the standard the tool had to meet.

For an Argus context, journalists and analysts are the same dynamic at a higher level of intellectual sophistication. The approach is identical: start from their work, not your demo. Show failure modes before they find them. Build the quality bar around their judgment."

---

**Q6: "How do you handle it when a business stakeholder asks you to build something that you know will fail?"**
*Why they're asking:* Internal automation roles require technical judgment that pushes back on unrealistic briefs.
*Format:* STAR

*Answer:*
"The key distinction I've learned to make is between 'this is technically difficult' and 'this won't work for the reason you think it will.' Those are different conversations.

The most direct example is when a client wanted to automate a review process where experienced reviewers frequently disagreed with each other. Their assumption was that AI could resolve the disagreement — produce a consistent answer where humans were inconsistent. My assessment was that the inconsistency wasn't a process failure; it was a genuine signal that the cases were hard. An automation that produced a consistent answer on hard cases would just be consistently wrong some of the time, in a way that was invisible.

Rather than arguing the point, I ran the measurement. I had three reviewers independently classify the same 200-case sample and measured agreement. Agreement on the easy cases was above 90% — those were automatable. Agreement on the hard cases was 60% — that's coin-flip territory, not something to automate. I presented that data and proposed automating the easy cases (the majority of volume) and escalating the hard cases to human review. The stakeholder got the efficiency gain they needed; the hard cases got the attention they deserved.

The lesson I've applied since: 'this won't work' is much more persuasive when it comes with data rather than an opinion. Build the smallest possible measurement, run it on a real sample, and let the numbers make the argument."

---

**Q7: "Describe your approach to testing and monitoring AI features."**
*Why they're asking:* "Pragmatic testing and monitoring approach for AI features" is listed as a requirement.
*Format:* PCR

*Answer:*
"Prompt-first is the principle I operate by. Before I wire any pipeline together, every prompt in it has been validated independently against a representative input set. That means: define what a good output looks like, build a labelled test set of at least 50–100 real inputs, run every prompt against that set in isolation, and only assemble the chain once each step passes independently. The cost of finding a failure at assembly is much higher than finding it at prompt level.

For AI-specific testing, there's an additional challenge that doesn't exist in standard software: the failure modes are often silent. A well-designed test suite for an LLM pipeline checks not just that the system runs, but that the output quality distribution is where you expect it. That means having a quality metric — which might be a human agreement rate, an LLM-judge score, or a rule-based validator for structured outputs — and running your test set against it as a regression check before any deployment.

In production, I use LangSmith-style per-node tracing on LLM calls so I can trace exactly what input a step received and what output it produced. That makes debugging a specific failure tractable rather than requiring you to reproduce the whole pipeline from scratch.

The pragmatic part: I calibrate the depth of testing to the failure cost. An automation that generates a first-draft summary for an analyst to review gets lighter testing than an automation that routes a compliance decision. The testing overhead should reflect the consequence of getting it wrong."

---

**Q8: "How do you prioritise which internal workflows to automate first?"**
*Why they're asking:* For a team-wide mandate, they need someone with a principled approach to roadmap decisions.
*Format:* PCR

*Answer:*
"Three criteria in order of priority. First, decision consistency — is this a workflow where experienced people would almost always do the same thing given the same inputs? If yes, it's automatable in principle. If the answer varies significantly between people or depends on implicit context outside the data, it probably isn't ready for automation yet, regardless of how much time it takes.

Second, input structure — does the automation have everything it needs from the available data, or does it require context that's implicit, verbal, or stored in someone's head? Unstructured required context is the thing that kills automation projects in practice. A workflow that looks simple but requires 'knowing what the analyst usually does with these types of sources' is not ready to automate; one that has clean structured inputs is.

Third, failure cost and recovery — what happens when the automation is wrong? If a wrong output gets caught by a human before it causes a problem, that's a recoverable failure mode; you can build with a lighter human review gate. If a wrong output gets acted on directly without review, the failure cost is higher and you need more rigorous validation before going live.

I'd start with the highest decision-consistency, most structured-input, lowest-failure-cost workflow — not the highest-volume one. The first automation needs to work visibly and build confidence across the team. A high-profile failure on the first deployment sets back everything that comes after it."

---

**Q9: "How do you integrate AI with internal systems securely and sustainably?"**
*Why they're asking:* "Integrate AI with internal systems securely and sustainably" is verbatim in the JD.
*Format:* PCR

*Answer:*
"There are three layers I think about. The data access layer, the execution layer, and the audit layer.

On data access: the automation should only be able to see what the user who invoked it can see. That's the principle. If an AI workflow is accessing internal systems — databases, document stores, communications — it should inherit the invoking user's permissions rather than running with a service account that has broader access. In a Microsoft 365 context, Microsoft Graph handles this naturally when you use delegated authentication rather than application-level permissions. In my own pipelines I've handled this by ensuring API credentials are scoped to the minimum required rather than org-wide. The problem you're preventing is an automation that inadvertently surfaces data one user can access to another.

On the execution layer: automations that take actions — send messages, update records, make API calls — should have explicit confirmation steps before they act, especially early in their life. An automation that drafts and holds for review is safer than one that drafts and sends. You can always reduce the friction once you have a track record. 'Sustainable' to me means the automation degrades gracefully — if a third-party API fails, it escalates to a human rather than failing silently or erroring out without leaving a trace.

On the audit layer: every significant action should be logged. Who triggered it, what input it received, what it did, what the output was. This isn't optional in an enterprise context — it's the mechanism for investigating problems when something goes wrong and for demonstrating compliance if anyone asks."

---

**Q10: "Where do you see AI automation going in a company like Argus over the next two years?"**
*Why they're asking:* Senior role — they want strategic thinking, not just execution capability.
*Format:* PCR

*Answer:*
"Argus's recent Snowflake partnership to make data AI-ready is a signal worth paying attention to — it suggests the organisation is thinking about AI tooling at the infrastructure level, not just the surface. That's the right direction, and it has implications for what internal automation looks like in two years.

My view on where this goes: the first wave of internal automation is about reducing friction in existing workflows — drafting, summarising, routing, classifying. That's what this role is building now. The second wave, which I'd expect to start becoming relevant in 12–18 months, is about connecting those automations into coherent pipelines where outputs from one workflow feed inputs to another. A journalist's research workflow feeding into a first-draft synthesis, feeding into a compliance and fact-check step. That's not much more complex in principle; it requires the first wave to be reliable enough to trust as upstream inputs.

The risk I'd watch for: automation sprawl. Teams start building their own Copilot plugins and Power Automate flows independently, none of them are monitored properly, and six months later you have 40 automations across the organisation with no-one who knows what's in production. The value of this role, built right, is that it establishes the governance and quality bar before that happens — not just builds things, but creates the standard that future automation has to meet."

---

## Section 10: Questions to Ask Them

**1. "How do you currently decide which internal workflows are worth automating — is there a process for that, or does it come from teams raising requests?" [Diagnostic]**
*Why:* Reveals whether you'd be hunting for opportunities systematically or responding to whoever shouts loudest. Very different roles.

**2. "The JD mentions 'own solutions after launch' — what has that looked like in practice? Have there been automations that launched and then needed significant maintenance?" [Signal]**
*Why:* Shows you took the ownership language seriously, and surfaces the real reliability history. Their answer tells you what kind of technical debt exists.

**3. "How does the AI automation function sit relative to the broader engineering team — do you have dedicated engineers to collaborate with, or is the expectation to build mostly independently?" [Diagnostic]**
*Why:* Directly affects how much Python/backend depth matters and whether you'd have support on the Microsoft stack ramp.

**4. "What's the Copilot Studio and Power Automate maturity level right now — is this function starting from scratch, or are there existing automations you'd be inheriting?" [Diagnostic]**
*Why:* Tells you whether day one is greenfield build or maintenance and extension — significantly different jobs.

**5. "Argus just partnered with Snowflake to deliver AI-ready data externally — does that shape what you're thinking about for internal tooling, or is the internal automation function relatively separate from the product data infrastructure?" [Strategic]**
*Why:* Shows you've done the research. Surfaces whether internal automation is connected to the broader AI direction or is a parallel track. Also signals you're thinking at infrastructure level, not just task level.

---

## Section 11: 30-60-90 Day Sketch

**Days 1–30: Map and listen.**
Don't build anything for the first month. The goal is to understand which teams have the most repetitive analytical and operational workflows, what Microsoft stack is already in place, and what's been tried before that didn't stick. Shadow analysts covering a few different commodity segments — oil, gas, energy transition — because the nature of the repetitive work likely varies by desk. Also: understand the data environment. Argus runs on proprietary price assessments and editorial processes; knowing what data is accessible via API versus what lives in legacy systems is essential before any design decision.

**Days 31–60: First automation, owned end to end.**
Identify one high-confidence candidate — the workflow with the most consistent decisions, the most structured inputs, and the most recoverable failure mode. Build it in Copilot Studio or Power Automate to get operational on the core stack. Deploy initially in assist mode where the automation surfaces its output alongside the analyst rather than replacing their step, and measure how often the analyst accepts versus overrides the output. That agreement rate is your first quality baseline. Also: start the monitoring setup from day one, not after you've proven the concept.

**Days 61–90: First quality case and roadmap foundation.**
Use the agreement rate data from the first deployment to make a quantified case for moving from assist to autonomous on that workflow. Identify the next two or three candidates from the mapping work, prioritised by the decision-consistency and input-structure framework. The output of the first 90 days should be: one automation in production with a measured quality baseline, a decision on expanded autonomy backed by data, and a prioritised backlog of next workflows with the quality bar and monitoring approach established as a standard for everything that follows.

---

## Section 12: Watch-Outs

**Seniority mismatch**
The role is "Senior" but mentions mentoring only one engineer — suggesting a small team or near-solo function. The salary and scope imply this is a senior IC role, not a team lead or manager. Probe: *"Can you tell me more about the team structure — is this primarily an individual contributor build role, or is there a management dimension that grows over time?"* If the answer suggests the scope is narrower than "Senior" implies (i.e. building a handful of Copilot Studio workflows rather than building a function), worth understanding whether there's a growth path.

**Role ambiguity**
"Build and run AI-powered internal workflows" is broad. It could mean anything from managing a library of Copilot plugins to building complex multi-step automations. The phrase "convert messy business workflows into clean technical solutions" suggests real engineering complexity, but Copilot Studio / Power Automate as the primary tooling suggests it may also be more IT-adjacent than engineering-adjacent. The questions in Section 10 are designed to surface this. Watch for answers that suggest low engineering ambition — if the real job is maintaining pre-built Power Automate templates, that's not the role the JD describes.

**Company signals**
No significant red flags. Argus is profitable, long-tenured, mission-stable, and recently consolidated ownership for long-term independent operation. The one thing to watch: Argus's commercial product is AI-ready commodity data delivered externally (the Snowflake partnership). If the internal engineering priorities shift toward product infrastructure, internal automation could become a secondary mandate. Ask: *"How is the internal automation function resourced relative to the product engineering team — is this function growing, stable, or being evaluated?"*

**Microsoft stack gap (your own watch-out)**
The Power Automate / Copilot Studio gap is real and will likely come up. Do not wait for them to raise it — bring it up yourself, with the framing from Section 6. An interviewer who discovers a gap they didn't expect is more unsettled than one who hears you name it first with a credible explanation. The proactive framing also signals the self-awareness they'd need in someone owning production systems.
