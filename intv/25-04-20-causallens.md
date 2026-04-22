# CausalLens — Artificial Intelligence Engineer
**Date:** Monday 20 April 2025

## Role Summary
Forward-deployed AI engineering role. Build and deliver agentic workflows for enterprise clients. Client-facing, solution architecture, LLMs/RAG/MCPs in production. Process: screening → "Day 0" (~3hr in-person challenge + presentation + interviews).

## The JD in Brief
- Build production-grade agentic workflows for enterprise clients (J&J, Cisco, Syneos Health)
- Direct client engagement with both technical and business stakeholders
- Design scalable AI architectures using latest AI tech
- Lead delivery from concept to deployment
- Backed by $50M+; "Digital Workers" as their core narrative

## Key Themes to Prep
- [ ] Forward-deployed / client-facing AI engineering experience stories
- [ ] Production LLM/agentic deployment examples
- [ ] Architecture decisions under real constraints
- [ ] Translating business problems into AI solutions
- [ ] Questions about "Day 0" structure and what they're evaluating

---

## Background Research

### What They Actually Do
- Builds **Digital Workers** — autonomous multi-agent AI systems that automate complex enterprise workflows end-to-end, not isolated tasks
- Three-layer product stack:
  - **Blueprints** — ~24 pre-built workflow templates, "80% ready out of the box," industry-specific
  - **Digital Worker Factory** — the assembly and deployment platform
  - **System of Work** — the governance OS: monitoring, audit trails, human-in-the-loop controls, ROI dashboards
- Core manifesto: **"Human-only companies are obsolete"** — deliberate, not hyperbole
- Technical moat: **causal reasoning layered on top of LLMs** via their Causality MCP
- Benchmark claim (Jan 2026): **20× higher reliability than OpenAI** on complex knowledge tasks; 3× on operational tasks
- Deployments go into existing enterprise stacks without migration: Veeva, SAP, Oracle Argus, Medidata, Salesforce, Databricks, Snowflake

---

### Digital Worker Blueprints — How They Work

**What a Blueprint is:**
A pre-built, pre-validated multi-agent workflow for a specific business process. It contains the agent orchestration logic, sequence of steps, tools invoked (data connectors, LLM calls, causal reasoning modules, validation agents), decision checkpoints, compliance guardrails, and Judge Agent scaffolding — already assembled and tested.

**The 80/20 split in practice:**
- **80% (pre-built):** Agent workflow logic, pre-configured integrations for the vertical, business rules and exception handling, compliance guardrails (GxP, SOC 2, HIPAA), audit trail wiring, Judge Agent evaluation framework
- **20% (your job as AI Engineer):** Connect to the client's specific system instances (their Veeva vault, their Oracle Argus config), tailor guardrails to client SOPs, configure escalation/approval thresholds, provide domain data for causal model calibration, customise output formats and downstream write-backs

**Stated deployment time:** 24 hours from Blueprint to live worker (vs. weeks/months for bespoke builds)

**Pharma Blueprints (9 available):**
- MLR Review Worker — pre-screens marketing assets against drug labels (USPI/SmPC) before formal review; integrates with Veeva PromoMats
- Medical Info & Safety Intake / PV Routing — NLP intake of adverse events and product complaints, real-time coding and routing into pharmacovigilance systems (Oracle Argus); case processing from ~1 week to 24 hours
- RFP Responder — reads proposals, surfaces prior content, drafts submissions
- Sales Territory Alignment — re-evaluates territories from scratch using physician opportunity, affiliations, travel constraints, rep capacity; Veeva/Salesforce CRM integration; $500K/yr savings cited
- Investigator Grant Variance — real-time monitoring across CTMS, EDC, ERP
- Scope of Work Digital Worker — contract drift tracking, billing automation
- Medical Writing — drafts regulatory documents and clinical summaries

**Finance/Ops Blueprints:**
- Financial Reconciliation — matches data across banks, ERPs, CRMs, and ledgers
- Accounts Payable — full invoice-to-payment cycle
- Payroll Automation
- Employee Onboarding

**Technical structure of each Blueprint:**
1. Planning Agent — decomposes the workflow, routes tasks to specialist agents
2. Specialist Agents — data ingestion, analysis, decision, write-back
3. Causality MCP — gives agents access to causal graphs for cause-effect reasoning
4. Judge Agent — executes code and inspects outputs against pre-defined criteria before any result is finalised or written to a system of record
5. Governor Agents — enforce policy guardrails; never let workers act outside defined bounds
6. System of Work hooks — pre-wired monitoring, audit logging, escalation triggers
7. Docker packaging — every completed worker ships as a Docker image, deployable on AWS/Azure/GCP or on-premise

---

### Digital Worker Factory — How It Works

**What it is:** The assembly platform — takes a Blueprint and a client specification and produces a deployed, running Digital Worker.

**Engineering interface:** Hybrid — not purely no-code, not purely code-first:
- Describe process requirements in natural language → system begins assembling agent workflows
- Visual adjustment of workflow steps, routing logic, and connections
- Single SDK call for programmatic integration by engineers
- Business users can configure data sources, approval thresholds, and reporting without engineering involvement

**Assembly flow:**
1. Blueprint selection — choose the closest pre-built worker
2. Specification input — describe the specific process, systems to connect, SOPs and guardrails to embed
3. Factory assembly — applies spec to Blueprint, adjusts agent logic, connects integrations, tunes causal models to client data
4. Forward-deployed engineering — the AI Engineer (this role) handles the 20% customisation on-site or remotely
5. Deployment — Docker image produced, deployed on client infra, System of Work activated

**Confirmed integrations:** Veeva Vault, Veeva PromoMats, Veeva CRM, Oracle Argus (pharmacovigilance), Medidata, Salesforce, Databricks, Snowflake (Snowflake Marketplace native app), SAP, Jira, GitHub, Confluence, IBM watsonx Orchestrate (launch partner), Google Cloud/Gemini

---

### How Causal Reasoning Works — The Core Technical Moat

**Why standard ML fails at causal questions:**
A standard ML model learns P(Y|X) — the probability of an outcome given inputs. It's a pattern-matching machine. The critical failure: it only models what was observed, not what would happen if you actively changed something. CausalLens demonstrated this with a medical dataset: an XGBoost model achieved 1.2 MAE on held-out test data but 41.8 MAE on counterfactual queries — a 35× degradation — because its learned distribution broke down when treatments were actively changed. This is why correlation-based models fail in production for intervention and RCA tasks.

**Judea Pearl's Causal Hierarchy — their theoretical grounding:**
- **Level 1 — Association:** "What does X correlate with?" → standard ML and LLMs
- **Level 2 — Intervention:** "What happens if I *do* X?" → requires a causal model and the do-operator
- **Level 3 — Counterfactual:** "What *would have* happened if X had been different?" → requires structural causal models

CausalLens agents operate at Levels 2 and 3. Standard LLM agents operate at Level 1.

---

**CausalNet — how it actually works:**

A Structural Causal Model (SCM) encodes the mechanism by which the world operates, not just the pattern. Every variable is represented as a function of its direct causes plus noise: `X_i = f_i(parents(X_i), noise_i)`. The set of these equations combined with a Directed Acyclic Graph (DAG) of cause-effect relationships is the SCM. The edges in the DAG represent mechanisms, not correlations.

Building a CausalNet is a two-phase process:

**Phase 1 — Causal Discovery (building the graph):**
CausalLens uses multiple algorithm families to infer the graph structure from data:
- **Constraint-based algorithms (e.g., PC, FCI):** Run conditional independence tests — if X and Y become independent when you condition on Z, then Z is on the path between them. FCI handles potential unmeasured confounders; their "FCI Tiers" variant respects domain-defined variable ordering (e.g., upstream process variables can only cause downstream ones)
- **PCMCI** for time series: handles autocorrelation and lagged causal effects
- **NOTEARS explicitly rejected:** CausalLens published research showing NOTEARS is scale-invariant — a simple rescaling of variables produces a completely different graph. They don't use it

Domain expert input is central, not optional. Experts lock known edges, block impossible ones, specify variable ordering, and review the graph visually before committing. An LLM also suggests directional causality as a starting point for expert review. The output is a confirmed DAG.

**Phase 2 — Training the structural equations (CausalNet proper):**
With the graph fixed, CausalNet fits `f_i` for each node — learning how each node's parents produce its value. Training backends: PyTorch (nonlinear), CVXPY (convex/linear), DoubleML (unbiased causal effects), Pyro (Bayesian/uncertainty). The objective is not prediction accuracy on observational data — it's accuracy of causal effect estimates under distribution shift.

**DoubleML — why it's needed:**
Standard training conflates the causal effect of a treatment with the spurious correlation between treatment and confounders. DoubleML fixes this:
1. Train model M1 to predict treatment T from confounders X → compute residual `~T = T - M1(X)`
2. Train model M2 to predict outcome Y from confounders X → compute residual `~Y = Y - M2(X)`
3. Regress `~Y` on `~T` — now free of confounding because both residuals are orthogonal to X

CausalLens built a proprietary extension ("Full Graph DoubleML") that does this for arbitrary DAGs with multiple nodes simultaneously, not just single treatment-outcome pairs. Result on the medical example: DoubleML SCM achieved 0.35 MAE on counterfactual queries vs. 41.8 for standard ML.

**How an agent uses CausalNet at inference time:**
- **Intervention query:** `cnet.interventions.do(variable="discount", value=0.2)` — fixes the variable, severs its incoming edges (removes confounding), propagates forward through structural equations, returns the distribution of all downstream variables. Answers "what happens if we change X?"
- **Root cause analysis:** Walks backward through the graph finding which upstream variable's deviation best explains an anomalous outcome
- **Counterfactual query:** For a specific observed case, infers the noise values that explain what happened, then re-runs with the treatment changed — answers "what would have happened to this specific patient/batch/customer if we had done differently?"
- **Algorithmic recourse:** Optimises over actionable variables constrained by a cost function to find the minimal intervention that changes an outcome — used for "what does this customer need to do to qualify for credit?"

**Causality MCP:**
An MCP-protocol-compatible module exposing CausalNet's query API to agents at inference time. This is the specific differentiator in the 20× benchmark: augmented agents received all baseline inputs *plus* access to the Causality MCP; baseline agents had data only. With MCP access, agents correctly navigate confounding and distinguish direct from indirect causal effects. Without it, they can't.

---

**cLAIRE — what it is and what's actually known:**

cLAIRE = **Causal Logic in AI Reasoning models**. It is CausalLens's proprietary LLM — the language and reasoning layer that powers Digital Workers. It works alongside CausalNet (the causal engine), not instead of it.

**The architecture — two separate systems working together:**
```
User query (natural language)
        ↓
cLAIRE — decomposes the question, plans reasoning steps, generates language
        ↓ ↑ (tool calls)
CausalNet — answers causal queries: do(), counterfactuals, RCA
        ↓
cLAIRE — synthesises causal results + business context → final response
        ↓
Judge Agent — validates output against causal model and safety guardrails
        ↓
Final answer
```

cLAIRE handles language and decomposition. CausalNet handles the causal arithmetic. The key constraint: cLAIRE's generation is blocked from making recommendations that contradict what CausalNet computes. If the causal model says intervention X has no effect on Y, cLAIRE cannot recommend X to improve Y.

**The "10–100% stepwise reasoning gains" claim:**
Refers to accuracy on individual reasoning steps in multi-step causal problems — not final answer accuracy. When an LLM without causal structure reasons through root cause analysis, it makes errors at individual steps (attributes effect to wrong cause, ignores confounding, reverses direction). cLAIRE's causal guardrails constrain these steps. The benchmark and methodology are not publicly specified — treat as directional, not precise.

**What is not publicly documented about cLAIRE:**
- What base model it was fine-tuned from (almost certainly fine-tuned from an existing foundation model, not built from scratch)
- The training data and fine-tuning method (RLHF, DPO, SFT?)
- Whether "proprietary LLM" means a genuinely custom model or a heavily adapted commercial one

Do not claim to know how cLAIRE was built. The honest answer: proprietary LLM with Judge Agents providing causal validation guardrails; technical details not public.

---

**Known limitations of the causal model approach:**
- **Unmeasured confounders:** PC-based discovery assumes no hidden confounders — almost always violated in real data. FCI partially handles this but produces less informative graphs
- **Graph mis-specification propagates:** A missing or reversed edge corrupts all downstream queries. The causal graph must be right for the model to be useful — garbage graph → garbage interventions
- **Causal discovery doesn't scale without pruning:** Complexity grows super-exponentially with variable count; domain expert guidance on variable ordering is required at enterprise scale
- **Counterfactual non-identifiability:** Even with a correct graph, individual-level counterfactuals require strong distributional assumptions about noise terms that can't always be validated
- **Structural equations can go stale:** If the underlying mechanism changes (new manufacturing process, policy shift), the trained functions become wrong and the model doesn't know it

**vs. other approaches:**

| Approach | Limitation |
|---|---|
| Chain-of-thought | Still operates over correlational priors from training data; doesn't query a causal model of the specific environment |
| RAG | Retrieves correct facts but hallucinated causal explanations can still occur even with correct retrieved context |
| Standard tool use | Can call APIs and execute code, but without a causal graph, tool selection and result interpretation remains correlational |
| CausalLens | Agent has CausalNet access — can ask "what caused this?" and "what happens if I intervene?" with structural, client-specific backing |

**Benchmark evidence:**
- 20× on causality-heavy tasks (RCA, causal effect estimation); 3× on operational workloads
- One RCA scenario: OpenAI baseline scored **0%**; CausalLens succeeded
- DoubleML SCM: 0.35 MAE on counterfactual queries vs. 41.8 for standard ML (medical dataset)
- Gartner Hype Cycle for AI 2024: named sample vendor for Causal AI

---

### Agent Challenges in Their Two Primary Verticals

**Pharma / Life Sciences:**
- **Regulatory compliance is multi-layered and non-negotiable** — GxP, FDA/EMA promotional rules, HIPAA, MLR review. Every agent action touching clinical or promotional content must trace to a validated, documented decision path
- **MLR review is a systemic bottleneck** — fragmented briefs, inconsistent claims sourcing, channel-specific format requirements, fair balance placement, cross-market adaptation all slow campaigns by weeks per cycle. The MLR Review Worker pre-screens against USPI/SmPC labels *inside Veeva PromoMats* before formal review, removing the most time-consuming rework cycles
- **50–200 disconnected systems** — Veeva Vault, Veeva PromoMats, Veeva CRM, CTMS, EDC, ERP, Oracle Argus are all separate. Data never migrates — workers connect to all of them in place
- **Clinical trial delays cost ~$600K/day** — undetected grant variance and contract drift compound to million-dollar overruns. Monitored continuously by GrantGuard and SOW Digital Workers
- **Adverse event routing** is a regulatory obligation — misclassified or delayed reports create enforcement risk. PV Routing Worker compresses AE case processing from ~1 week to 24 hours
- **Workforce burnout** — 61% of clinical researchers report burnout; 12+ weeks/year lost to admin. Digital Workers recover 30–40% of this time

**Financial Services:**
- **Explainability requirements are regulatory** — KYC/AML, Basel III, SEC rules, MAS FEAT framework all require AI decisions to be explained and auditable. 84% of financial institutions report inadequate AI transparency blocking deployment (World Economic Forum)
- **Counterfactual fairness** — regulators require that AI-driven decisions (credit refusals, fraud flags) can be challenged. Causal models enable this; correlation models cannot
- **Performance degradation during market shifts** — models trained on historical data break during regime changes (COVID cited by MAS). Causal models encoding structural mechanisms are more robust than pattern-matching models
- **Reconciliation complexity** — financial reconciliation requires matching data across multiple banks, ERPs, CRMs, and ledgers simultaneously; month-end close extends for weeks with analysts spending 70–80% of time on data cleaning rather than analysis

**DANA Indonesia case (fintech at scale):**
- 200M+ customers, 40M transactions/day, analytics backlog approaching one year
- causaLens agents across fraud detection, onboarding, sentiment analysis, content generation
- Outcome: 90% of customer support queries handled by AI agents; experimentation velocity from 3 test scenarios/week to 2,000+; backlog eliminated

---

### Core Beliefs — Clearly Stated

**1. "Reliability is engineered, not emergent"**
Their near-motto. The six failure modes they design against: non-determinism, error cascading, hallucinations, poor task decomposition, tool misuse, absent self-verification. Every architectural decision is pointed at these. They publish benchmarks to prove it rather than claim it.

**2. "LLMs are copilots; Digital Workers are colleagues"**
LLMs are probabilistic. For regulated enterprise workflows this means inconsistent outputs, ungovernable behaviour, no audit trail. A Digital Worker adds deterministic business logic + causal reasoning + governance on top of the model. The LLM is the language layer, not the decision layer.

**3. "The Death of AI PoCs"**
95% of generative AI pilots fail to reach production. Not because the technology fails in testing — because sandboxed PoCs don't validate real integration complexity. The "true magic" is in final-mile integration into existing workflows, systems, and data. They replace 3-month PoCs with 30-day in-production deployments using pre-built blueprints.

**4. "Enterprise means governance by default"**
Audit trails, human-in-the-loop, kill switches, SOC 2/HIPAA/GxP — these are not add-ons, they are embedded in every Blueprint. Selling into pharma and finance means accountability is load-bearing.

**5. "Outcomes over complexity"**
*"No extra tools. No extra headcount. Just outcomes."* 5× average ROI. Every engagement is measured in cycle time saved, cost eliminated, or revenue recovered. Impressive architecture is irrelevant if the outcome isn't quantified.

**6. "Causal reasoning is the only path to explainability that holds at Level 2 and 3"**
Stakeholders — compliance officers, regulators, executives — need to know *why* a decision was made, not just *what* it was. Causal graphs provide structural explanations that trace through cause-effect paths. SHAP/LIME post-hoc explanations on correlation models cannot provide this. This is why causal reasoning is the moat, not just a feature.

---

### System of Work — Governance Layer

- **Real-time monitoring** — every workflow observed, performance/accuracy/compliance metrics logged; performance drift triggers real-time alerts
- **Human-in-the-loop** — approval gates embedded to match the client's SOPs; placement is configurable, not fixed; alerts distinguish "human approval needed" from "performance drift detected"
- **Autonomous Auditor Agents** — run alongside operational workers, validating every step in real time; flag anomalies and enforce compliance rules without waiting for human review
- **Judge Agents** — Agent-as-a-Judge evaluates outputs (reports, graphs, datasets) against pre-defined criteria; checks accuracy thresholds and data integrity before any output is finalised or written to a system of record; "glass box" replacement for black-box AI
- **Governor Agents** — built-in regulators ensuring Digital Workers never operate outside defined guardrails; enforce policies automatically at workflow level
- **Full audit trails** — every action logged, structured for regulator inspection (not just internal logging); specifically designed for GxP and financial compliance
- **Certifications:** SOC 2, HIPAA, ISO 27001

---

### Leadership
- **Darko Matovski, PhD — CEO & Co-Founder.** The intellectual voice. Core belief: AI needs to reason causally, not just correlate. Quote (TechCrunch 2022): *"AI should start to understand the world as humans understand it."* Has 25 direct reports at ~66 people — very flat, hands-on
- **Maksim Sipos — CTO.** Co-leads technical product
- **Michael Madding — COO** (recently appointed, ex-Lucra) — signals professionalisation, possible Series B prep
- **Tom Kennedy** — primary content/GTM voice, authors most blog posts on reliability benchmarks and enterprise AI buying
- **Felix Mottram** — senior AI/engineering contributor (co-authored Jan 2026 reliability benchmarks)
- **Elias Limouni** — recently hired Lead AI Engineer with GenAI/NLP background — building out the agentic delivery team

### Funding & Scale
- $44.9M Series A (Feb 2022), led by Dorilton Ventures and Molten Ventures; IQ Capital, Generation Ventures, GP Bullhound; valuation ~$250M; revenue grew 500% in the year prior
- No public Series B; COO hire + aggressive enterprise push suggests it's coming
- IBM partnership (launch partner in AI Agent Catalog); Google Cloud/Gemini partnership for grounding LLM quantitative reasoning

### Key Clients & Outcomes
| Client | What was built | Outcome |
|---|---|---|
| **J&J** | Causal agents for drug manufacturing root cause analysis | Months → days; *"We can do this in a day, not a month"* |
| **Cisco** | Agents across 10,000+ products for demand forecasting | *"Acts as a PhD-level Economist"* (Dir. Data Science) |
| **McCann Worldgroup** | Brand analytics agents replacing manual statistical modelling | *"Reproducible. Repeatable. Democratised."* |
| **Syneos Health** | HCP targeting, causal engagement strategy | Insights 10× faster at 1/10th cost; $200K MLR delays eliminated |
| **Croud** | Data cleaning automation | Eliminated 70–80% of data scientist time on cleaning |
| **DANA Indonesia** | Fraud detection, analytics, onboarding agents | Analytics backlog eliminated; 90% customer support queries handled by AI |

Pattern: **deployment-led, not SaaS.** They build and install working Digital Workers into the client's existing stack. The AI Engineer is the person executing this.

---

### Culture Signals
- **Flat and output-oriented.** CEO with 25 direct reports at 66 people. No room for people who need managing
- **Benchmarking culture.** They publish 20× reliability claims, 5× ROI, $500K savings numbers. Be quantitative about your own impact
- **Pharma is the fastest-growing vertical.** 9 blueprints, multiple named clients, Copenhagen roundtable with 30 pharma/tech execs in 2025
- **No Glassdoor data, no Reddit threads found.** Low public profile — don't expect polished onboarding; expect startup-pace delivery inside enterprise client constraints
- **Content tone:** confident, comparative (vs. OpenAI), outcome-obsessed. Strong opinions. Match that energy

---

### Expected Day-to-Day for This Role

Based on how CausalLens deploys (deployment-led, forward-deployed engineering, 20% client customisation):

**Week 1–2 of a new engagement:**
- Client discovery — map the target workflow, identify the systems involved (Veeva, SAP, Oracle), understand the SOPs and compliance requirements, document the 20% of customisation needed
- Assess which Blueprint is the closest match; document the gap between the Blueprint's default behaviour and what the client actually needs
- Stakeholder alignment with both technical (data science, IT) and business (operations, compliance) leads

**Week 2–4 (build and configure):**
- Connect Blueprint to client system instances — API credentials, integration testing, data mapping
- Tune causal models to client-specific data (provide domain data for CausalNet calibration)
- Configure approval thresholds, escalation rules, and human-in-the-loop gates to match the client's internal SOPs
- Customise output formats and downstream write-backs

**Ongoing (post-deployment):**
- Monitor performance through the System of Work; investigate and resolve production failures
- Act as the primary technical contact for the client — field questions from compliance teams, data science leads, operations VPs
- Feed failure patterns back to the Blueprint/product team
- Identify expansion opportunities (additional workflows, additional departments)
- Simultaneously juggling multiple client engagements (similar to the V7 FDE role — up to 10 concurrent)

**Internal:**
- Contribute to Blueprint development — document what the 20% commonly involves in each vertical so it can be systematised
- Work with the product team on integration gaps (systems CausalLens can't yet connect to)
- Potentially contribute to benchmark and evaluation frameworks

---

### Questions to Ask Them
*(Based on Oliver's background in agentic pipelines, HumanFirst prompt orchestration, production LLM evaluation, and enterprise delivery)*

**On the role and day-to-day:**
- When you say "forward-deployed" — what does the typical client engagement rhythm look like? Are you on-site with clients regularly, or is most of the work remote?
- How many active client engagements would I typically be running in parallel? What does context-switching look like across regulated pharma vs. other verticals?
- The JD talks about "leading delivery from concept to deployment" — where does the AI Engineer's responsibility end and the client's internal team take over?

**On the product and technical environment:**
- The Causality MCP is clearly the technical differentiator. In practice, how much time does an AI Engineer spend on the causal model calibration versus the integration and orchestration work? What's the skill split?
- How mature are the Blueprints at this point — is the 20% customisation genuinely that small in practice, or is that the aspiration and the reality is more variable?
- I work heavily with prompt orchestration through HumanFirst and use LangGraph for state management. How does the Factory's toolchain relate to those approaches — are engineers working in familiar Python/LangGraph patterns, or is it a proprietary abstraction?
- How do you handle cases where a client's regulatory requirements push outside what the Blueprint's guardrails currently support? Does the AI Engineer flag and escalate, or solve it in the field?

**On evaluation and reliability (Oliver's strongest area):**
- Your benchmark methodology against OpenAI is clearly rigorous — how does that evaluation culture translate into the field? Are AI Engineers running their own evaluation passes before a worker goes live, or is there a separate QA function?
- I've been building LLM evaluation frameworks (LLM-as-judge, quality gates, human-baseline validation). How does the Judge Agent within a Blueprint get configured for a specific client's quality bar — is that part of the 20%, or is it standardised per Blueprint?

**On growth and culture:**
- With a new COO and what looks like a professionalisation phase, how is the team structure evolving? Is there a path from AI Engineer toward Blueprint architect or product-side as the platform matures?
- What does "Day 0" actually evaluate — is it primarily technical problem-solving, client-facing communication, or both?

---

### Likely Interview Questions
- Walk me through an agentic workflow you've built — what broke, how did you make it reliable?
- How do you handle error propagation across a multi-step agent chain?
- What's the difference between correlation-based and causal reasoning in production? *(Founding thesis — they will probe this)*
- How would you customise a pre-built blueprint for a regulated pharma client with Veeva integrations?
- What does "production-ready" mean to you in an agentic system?
- Describe working directly with a non-technical enterprise client to deliver an AI system
- How do you explain a complex AI system to a compliance officer?
- Tell me about a time you turned a prototype into something genuinely reliable in production

### Phrases That Will Land Well
- Reliability as an *engineering discipline*, not a model property
- Human-in-the-loop as a *design requirement*, not an afterthought
- *"The problem with PoCs isn't the demo — it's the gap between demo and production"*
- Causal reasoning as a trust mechanism: stakeholders need "why," not just "what"
- Specific outcome metrics — cycle time, cost savings, headcount displacement
- Evaluation framework as a first-class part of the architecture, not a bolt-on

### Things to Avoid
- Framing experience as "I built impressive demos" — they are explicitly anti-PoC
- Positioning LLMs as the whole solution — their moat is what they add on top
- Vague language about "AI potential" — they ship quantified outcomes to named clients

### Competitive Positioning to Know
They benchmark against: OpenAI Agents, Microsoft Copilot/Copilot Studio, Salesforce Agentforce, legacy RPA (UiPath, Automation Anywhere)
- vs. RPA: brittle, script-based, can't handle unstructured inputs
- vs. generic LLM agents: unreliable, no governance, can't serve regulated industries
- vs. consulting-led AI: months to deploy, not production-ready, doesn't scale past the engagement

---

### Last 10 Blog Posts

---

**1. Reliability at Scale: The Hard Problem of Multi-Agent Systems** | Feb 2026 | Felix Mottram

*Core problem:* Multi-agent systems are genuinely powerful, but they don't become reliable automatically — reliability has to be deliberately engineered out of six structural failure modes that appear at scale.

*Key insight:* The six failure modes are non-determinism (same input, different output), error cascading (small mistakes compound through steps), hallucination (agents fabricate facts and act on them confidently), poor task decomposition (can't break complex goals into coherent sub-steps), tool misuse (calling APIs incorrectly or destructively), and absent self-verification (no internal quality gate before proceeding). These aren't random LLM quirks — they're systematic architectural weaknesses requiring systematic engineering responses, not prompt tuning.

*Why they wrote it:* To establish the intellectual framework before presenting their benchmark numbers. Primes buyers to think about agent failure structurally, so "20× reliability gains" lands with meaning rather than as a bare claim.

*Evidence:* J&J using agents for drug manufacturing; financial advisor agent giving contradictory risk advice to identical client profiles; procurement agent misidentifying components and halting a production line; healthcare agent hallucinating insurance pre-authorisation codes.

> *"Reliability does not emerge by chance in agentic architectures; it must be deliberately designed and continuously validated."*

---

**2. causaLens Benchmarks 20× Higher Reliability Than OpenAI on Complex Knowledge Tasks** | Jan 2026 | Tom Kennedy

*Core problem:* Standard AI agents — including OpenAI's — don't just underperform on causal reasoning tasks. They can be categorically wrong in ways that have serious consequences in pharma, manufacturing, and finance.

*Key insight:* The benchmark reveals a categorical gap, not a marginal one. On one RCA scenario, OpenAI's baseline scored 0% accuracy while CausalLens succeeded. The Causality MCP is the specific differentiator: agents given causal graphs and MCP access navigated confounding correctly; agents given only data could not. This is the technical argument that "which LLM" is the wrong question — architecture is the question.

*Why they wrote it:* Direct competitive positioning against OpenAI. The synthetic dataset methodology with known ground truths makes the comparison hard to dismiss. Forces the enterprise AI conversation from model selection to architectural decisions.

*Evidence:* 10–16 variables, 10,000 samples per dataset; 3 problem instances × 10 iterations; execution time 1.25–3.5× faster; scenarios based on pharma manufacturing, quality control, marketing attribution.

> *"Traditional AI agents simply aren't built for the kind of high-value, white-collar knowledge work that powers modern enterprises."*

---

**3. causaLens' Digital Workers Outperform OpenAI's Agents by up to 3×** | Jan 2026 | Tom Kennedy

*Core problem:* General-purpose single-agent AI systems are architecturally unsuited to complex enterprise tasks — not just less accurate but far less consistent. In production, inconsistency is itself a form of failure.

*Key insight:* The most underappreciated finding is about variance, not mean accuracy. Digital Workers showed 17–75% lower execution variance than OpenAI agents. A system that produces the right answer 78% of the time but wildly different outputs on identical inputs cannot be trusted in production. Specialised architecture constrains the solution space in ways that brute-force general models cannot — this is why they outperform even on adversarial tests (injected noise, rephrased questions).

*Why they wrote it:* Companion piece to article 2 — targeting a different buyer concern. Article 2 covers causal knowledge work; this one covers operational reliability for everyday workflows. Together they close off "OpenAI is good enough" for both high-stakes and routine tasks.

*Evidence:* Success rates — modelling: 78% vs. 50%; weather analysis: 78% vs. 50%; finance prediction: 89% vs. 70%; compliance audit: 12% vs. 0% (OpenAI failed entirely). Three evaluation methods: trace analysis, artifact analysis (Agent-as-a-Judge), adversarial robustness testing.

---

**4. Beyond Services & Scripts: Why Enterprises Need Reliable Digital Workers** | Nov 2025 | George Burton-Fletcher

*Core problem:* Every existing category of enterprise AI fails for a different but predictable reason — and none were designed to deliver operational outcomes.

*Key insight:* The article's structural argument is that the landscape has the wrong incentives baked in. Consulting firms profit from extended engagements that automation would eliminate. Lightweight agentic tools are designed for low-stakes consumer tasks, not regulated workflows. Developer frameworks require internal engineering capacity most enterprises don't have. Services-led platforms lock customers into dependency. No existing category was built for an operational leader who needs an autonomous, compliant system running mission-critical workflows. CausalLens is claiming to be a new category, not a better version of any existing one.

*Why they wrote it:* Category creation. This framing makes it harder to compare CausalLens on price or feature lists — it establishes separate evaluation criteria (outcome-focused, end-to-end, high-stakes compliant) that only they currently meet.

*Evidence:* Fortune 100 eliminated six-month processing backlog in under four weeks; global supply chain group cut manual interventions 60% in two months; Digital Workers run "thousands of workflow hours weekly" for enterprise clients.

> *"Inaction isn't just a delay; it's a direct threat to your competitive position."*

---

**5. The True Cost of Operational Inefficiency in Pharma & CROs** | Oct 2025 | Tom Kennedy

*Core problem:* The pharma industry spends $50B annually on compliance yet still accumulates $1.1B+ in penalties. The problem isn't effort — it's that 50–200 disconnected systems make full operational visibility impossible, so decisions carry more risk and every process involves more rework than it should.

*Key insight:* Operational inefficiency in pharma isn't a collection of isolated problems — it's a system failure caused by data fragmentation. No single team has full visibility across ERPs, CRMs, CTMS, and safety databases, so every decision carries compounding risk. Automating individual tasks doesn't fix this; what's needed is an intelligent operations layer that spans the fragmentation. The cost isn't just financial — it's measured in delayed therapies and compounding regulatory risk.

*Why they wrote it:* Establishes pharma and CROs as primary vertical with owned pain-point language, and pre-empts the "we already have RPA" objection by explicitly critiquing both RPA (brittle) and LLM copilots (hallucination risk) before positioning Digital Workers.

*Evidence:* $50B compliance spend; $1.1B+ penalties; 61% of clinical researchers reporting burnout; scientists losing ~12 weeks/year to admin; clinical trial delays ~$600K/day; 30–40% operational time recovery; 5× average ROI; one CRO: >10% weekly prescription uplift at no additional cost; $500K/yr from territory alignment; $200K eliminated in MLR review delays.

> *"The most effective use of an AI budget is not to fund more data silos, but to build an intelligent operations layer."*

---

**6. The Death of AI PoCs: A New Model for Buying AI in the Enterprise** | Oct 2025 | Tom Kennedy

*Core problem:* AI PoCs systematically fail not because the technology fails in testing — because sandboxed evaluation never tests the thing that actually determines production success: integration with real workflows, live data, and edge cases.

*Key insight:* The conceptual shift is treating AI deployment like a probationary hire rather than a software evaluation. An employee on trial performs real work in the actual environment against business metrics — not a lab test. Applied to AI: the evaluation question isn't "does the model work?" but "does this system improve our operations?" The final-mile integration — connecting AI to live systems and real user behaviour — is where almost all value is created or destroyed, and PoCs never reach it.

*Why they wrote it:* To dismantle the most common procurement barrier to their deals. By proposing a 30-day production probation model that CausalLens can deliver on (deploy in days, not months), they reframe buying in a way that favours their speed advantage over consulting-led competitors.

*Evidence:* MIT study — 95% of generative AI pilots fail to reach production; 78% of organisations now use AI in at least one function (up from 55%), suggesting companies are bypassing traditional PoC processes; 5× ROI target for Digital Workers.

> *"The true 'magic' of AI happens in the final mile: the deep integration into your existing workflows."*

---

**7. The Future of Pharma Operations: Why Digital Workers are the Next Competitive Advantage** | Oct 2025 | Tom Kennedy

*Core problem:* Pharma's traditional operational tools — outsourcing, SaaS, basic automation — have hit diminishing returns against rising R&D costs, growing regulatory burden, and shrinking margins.

*Key insight:* The article draws a three-way distinction that often gets collapsed: RPA (rigid scripts that break with any UI change), LLM copilots (probabilistic assistants with no governance model), and Digital Workers (multi-agent systems with deterministic business logic, causal reasoning, and built-in auditability). The first two categories cannot operate in regulated environments without unacceptable human oversight costs. Digital Workers can — because every action is monitored, logged, and auditable by design. This is the only AI class suitable for GxP workflows.

*Why they wrote it:* A comprehensive vertical playbook designed to be shared internally by a pharma champion building the business case. Covers six specific use cases with ROI estimates, names J&J and Syneos Health, and lays out deployment timelines in enough detail to take to a budget approval meeting.

*Evidence:* AI in pharma/biotech forecast to $13.1B by 2034; PV case processing week → 24 hours; CAPA closure 30–40% faster; 29% bioprocessing throughput increase; 5× ROI; payback under three months; 24-hour Blueprint deployment; "$5 digital labor value per $1 invested."

---

**8. Fixing Sales Territory Alignment Bottlenecks** | Oct 2025 | Tom Kennedy

*Core problem:* Pharma commercial teams run territory realignment via spreadsheets that take months to complete — during which market opportunities erode, top reps burn out, and compliance exposures multiply.

*Key insight:* The real argument isn't just speed — it's that annual, static territory plans are structurally incapable of reflecting dynamic market conditions. A territory designed in January based on Q3 prior-year prescribing data is already wrong by March. Territory alignment should be a continuous, data-driven process rather than a periodic project. That requires a system that ingests live data (prescribing trends, HCP affiliations, travel constraints, rep capacity) and reoptimises dynamically — which a spreadsheet-based process can never be.

*Why they wrote it:* Targeted lead-generation piece for pharma commercial leaders who recognise "territory alignment takes three months and everyone hates it" as their specific pain. Converts readers with that exact problem into demo requests.

*Evidence:* Planning cycles: months → days; deployment: 24 hours; $500K/yr savings cited; integrates directly with Veeva and Salesforce CRM via existing APIs; measurable lift in quota attainment and reduction in rep turnover.

> *"During that time, market opportunities dry up, top reps burn out from unsustainable workloads, and compliance risks spread like wildfire."*

---

**9. Streamlining Campaign Creative & QA for Faster Launches** | Oct 2025 | Tom Kennedy

*Core problem:* Healthcare marketing is bottlenecked by MLR review cycles that treat compliance as a final gate — which means errors are caught after expensive content has already been produced, triggering rework cycles that can delay campaign launches by weeks.

*Key insight:* Most MLR review delays aren't caused by the review itself being slow — they're caused by content arriving at MLR already non-compliant. Back-and-forth revision cycles compound the delay. Moving compliance from gate to guardrail — pre-screening assets against drug labels before submission and suggesting compliant alternatives rather than just flagging errors — eliminates the rework loops entirely. The solution isn't faster reviewers; it's removing the reason for re-review.

*Why they wrote it:* Vertical use-case play for pharma marketing operations and CRO/agency leaders who have personally lived through launch delays caused by compliance failures. Addresses a very specific audience with a very acute pain point.

*Evidence:* Review cycles compress from weeks to days; integrates with Veeva PromoMats and Adobe Experience Manager in place; handles six recurring bottleneck types; generates audit-ready evidence dossiers; monitors for post-launch label/policy changes; deployment in "a few weeks."

---

**10. Why LLMs Aren't Enough: Building Digital Workers for Enterprise Automation** | Oct 2025 | Tom Kennedy

*Core problem:* LLMs are architecturally unsuited to enterprise automation — not because they're unintelligent but because they're probabilistic. They predict the next plausible word, which means they cannot guarantee consistent outputs, embed stable business logic, or produce auditable decisions.

*Key insight:* The distinction between automation that *assists* and automation that *completes*. LLMs create the illusion of automation — they draft content, answer questions, summarise documents — but they require humans to validate every output before acting on it. That human validation is itself expensive; it's just less visible than the old manual process it replaced. Digital Workers close the loop: they execute end-to-end, integrate with live systems, and verify their own outputs through Judge Agents. Copilots don't reduce headcount or compress cycle times — they shift where humans spend attention without eliminating the human dependency.

*Why they wrote it:* The foundational thought leadership piece underpinning all use-case content. Establishes the company's core worldview — LLMs ≠ automation — and the vocabulary (Digital Workers, deterministic logic, Judge Agents) that every other article builds on.

*Evidence:* HBR: 95% of LLM copilots fail to improve productivity; cost enterprises up to $9M/year in lost time; ChatGPT legal case (2023): fabricated six case citations, lawyer sanctioned; 88% of AI pilots never reach production; Syneos Health: 500% ROI; $5 digital labor value per $1 invested.

> *"Where LLMs tease you with glimpses of automation, Digital Workers actually deliver it — executing workflows end-to-end with reliability."*

---

*Thematic pattern across all 10:* Every article argues the same thing from a different angle — the difference between AI that assists and AI that completes. The central thesis is consistent: LLMs alone are probabilistic and ungovernable; Digital Workers add deterministic logic, causal reasoning, and governance to produce something enterprises can actually rely on. Pharma is the dominant vertical (5 of 10 articles target it directly). The two January 2026 benchmark pieces are the most technically substantive; the October 2025 cluster reads as coordinated launch content for a pharma go-to-market push.

---

## Ideal Answers to Likely Interview Questions

---

### Q1: Walk me through an agentic workflow you've built — what broke, how did you make it reliable?

**Use: LinkedIn Outreach Automation (production) + LinkedIn Post Agent (architecture story)**

"The clearest example is an end-to-end LinkedIn outreach pipeline I built at HumanFirst following a company restructure — we'd gone from 22 to 8 people and removed the sales function, so I built the replacement. The pipeline scraped LinkedIn for posts matching strategic keywords, ran 500+ profiles through generative AI to filter by post content for high-specificity targeting, generated personalised outreach messages with A/B testing, and managed deduplication against a database of everyone we'd already contacted. Over 15,000 profiles processed; 70% connection rate, 40% response rate, 7% demo attendance.

What broke: The LinkedIn scraping tool had strict rate limits and unpredictable quota behaviour. Messages would start generating against profiles that hadn't fully resolved — so I built complex rate-limit handling and a staging layer that verified each profile before downstream steps fired. Deduplication was another failure mode — early on we'd occasionally reach the same person twice because the database check wasn't running at the right point in the chain. I moved it to a gate before any message generation rather than after.

The broader pattern I use: I design the state schema and data contracts between each step before writing any prompt logic. On the LinkedIn Post Agent I built later, I took this further — all seven prompts were built and chain-tested in HumanFirst against 20 sample inputs before I touched a running pipeline. That caught a JSON output inconsistency from the idea refiner and an over-permissive review calibration at the prompt level, not in production. By the time Claude Code built the LangGraph graph, the hard design work was done. For me, reliability engineering starts at the design stage — not after deployment."

---

### Q2: How do you handle error propagation across a multi-step agent chain?

**Use: Insurance analytics pipeline + Research Agent timeout story**

"My main approach is that errors should fail loudly, at the right point, with enough context to diagnose — not silently corrupt downstream steps.

In the insurance analytics pipeline — we were processing 50,000+ customer-broker conversations — the biggest propagation risk was a classification prompt returning malformed output that would silently pass through to BigQuery and produce incorrect dashboards. I built a Pydantic validation layer at each step output: if the schema didn't match, the pipeline stopped and logged which prompt, which input, and what it returned. That made failures diagnosable in LangSmith rather than invisible in downstream data.

The other pattern I use is gate-before-generate: on the Research Agent I built for a client, the pipeline chained web search → per-URL summarisation → outreach drafting through Supabase. The main challenge was timeouts on chained async calls. The fix was validating that each upstream output met a minimum content threshold before triggering the next prompt — rather than letting an empty or partial summary propagate into an outreach draft.

The principle across all of this: error propagation in a multi-step chain is a state management problem. If you're explicit about what a valid state looks like at each transition, you catch failures at the boundary where they occur rather than in some downstream output that's hard to trace back."

---

### Q3: What's the difference between correlation-based and causal reasoning in production?

> ⚠️ **Gap note:** No direct causal AI implementation experience — this answer demonstrates genuine conceptual understanding without overclaiming.

"The practical difference shows up most clearly when you need to answer 'if I change X, what happens to Y?' — or when a stakeholder asks 'why did this happen?' and they actually mean it.

A correlation-based model can tell you that X and Y tend to move together. That's useful for prediction, but it breaks down the moment conditions shift, and it can't tell you whether acting on X will change Y. In the evaluation work I've done building LLM-as-judge frameworks, this shows up as a specific failure mode: a model produces a confident, well-articulated explanation for why something happened, but it's identified a feature associated with the outcome rather than the mechanism that produced it. The answer sounds right and points to the wrong fix.

In a regulated enterprise context — pharma manufacturing, financial compliance — this distinction is load-bearing, not academic. A deviation investigation in a drug manufacturing process can't conclude 'process variable X was associated with this batch failure.' It needs to establish whether X caused it, whether changing X will prevent recurrence, and whether that reasoning will survive a regulatory audit. A correlation-based model can't provide that. A causal model — one that encodes the actual mechanisms and can reason about interventions — can.

What I find compelling about your approach is that it answers a fundamentally different question. 'What will happen if I do X?' is not a harder version of 'what pattern does X appear in?' It requires a different kind of reasoning entirely — and the Causality MCP giving agents access to structural causal models at inference time is what changes the category of question the agent can answer reliably, not just the accuracy on the same task."

---

### Q4: How would you customise a pre-built blueprint for a regulated pharma client with Veeva integrations?

**Use: General delivery methodology + known Blueprint/Veeva detail from research**

"My starting point would be understanding the gap between the Blueprint's default behaviour and the client's actual SOPs — specifically which steps in their workflow don't map cleanly to the Blueprint's pre-built logic. That's usually where the interesting customisation lives.

For a Veeva integration specifically, the practical work is: connect to their specific Vault or PromoMats instance, verify the authentication and permission model, map the Blueprint's data connectors to their actual vault structure and document types. The technical integration is usually straightforward; the harder part is understanding their content governance model — which document states trigger which actions, who has approval authority at each gate, and what the audit trail needs to look like for their regulatory context.

The compliance-specific configuration is the part I'd invest the most discovery time in upfront. In regulated environments, the human-in-the-loop gates and escalation thresholds aren't implementation details — they're the thing that determines whether the worker is deployable. Getting those wrong late in the customisation means rework against a compliance constraint, which is expensive.

The output validation piece — which in your architecture is the Judge Agent — is where I'd also want to get involved early. Setting the accuracy thresholds and data integrity checks to match the client's quality bar is something that needs to be done against real client data, not defaults, and it benefits from being done before the worker goes live rather than after the first production run."

---

### Q5: What does "production-ready" mean to you in an agentic system?

**Use: Own methodology across multiple projects**

"It means the system behaves predictably under conditions it wasn't explicitly designed for, and when it doesn't, you know about it before a stakeholder does.

Concretely, I think about four things:

First, **validated data contracts at every step** — not just happy-path testing. Every output schema is explicit, every handoff is validated. If an upstream step returns something malformed, it fails loudly at the boundary.

Second, **observability that makes failures diagnosable**. I use LangSmith for per-node tracing on all my LangGraph pipelines. Not because I expect failures, but because when something breaks in production, I need to know which node, which input, and what it returned — not just that something downstream was wrong.

Third, **quality gates before outputs reach systems of record**. In the insurance analytics pipeline feeding BigQuery and Looker dashboards, I built an evaluation layer comparing AI classifications against human baselines before any output was written. Once something's in a dashboard a stakeholder has already looked at, the bar to fix it is much higher.

Fourth, **the system must degrade gracefully**. Rate limits, timeouts, upstream API failures — these will happen. The question is whether the system queues, retries with context, and logs, or whether it silently produces partial results.

The thing I'd add specifically for a regulated environment: production-ready also means the audit trail is a first-class output, not an afterthought. Every decision needs to be traceable. That's a design requirement you have to bake in from the start."

---

### Q6: Describe working directly with a non-technical enterprise client to deliver an AI system

**Use: Insurance analytics pipeline + Canadian engineering firm enablement + Microsoft Copilot POC**

"The most substantive example is the analytics pipeline I built for a global insurance firm. The client was a compliance and operations team — not data scientists. They needed to understand what was happening in 50,000+ customer-broker conversations: why customers were escalating, what brokers were doing differently in high-performing interactions. The AI system I built classified conversations at scale and surfaced results through BigQuery and Looker dashboards.

The delivery had two distinct parts: the technical build, and translating what the system was doing into something the client could trust and act on. The second part was harder. They needed to understand not just that the classification was accurate, but how we knew it was accurate — which meant walking them through the evaluation framework, showing them the comparison against human baselines, and being explicit about where the model had uncertainty.

What I've found across several enterprise engagements is that the adoption barrier is almost never technical capability. It's trust. Non-technical stakeholders need to understand the failure modes before they'll rely on the output. So I've learned to lead with the evaluation story — here's what we tested, here's where it works reliably, here's what it doesn't do — before talking about the capabilities.

The Canadian engineering firm engagement was a different shape — I trained 40 non-technical business users to become AI practitioners over two months, and the measure of success wasn't whether I built something impressive, it was whether over 60% of them had implemented their own use cases within the programme. That required meeting people where they were technically, not where I was."

---

### Q7: How do you explain a complex AI system to a compliance officer?

**Use: Insurance pipeline + general principle from client delivery**

"The first thing I do is not explain the AI system at all — I explain what decisions it makes and what happens when it gets it wrong.

Compliance officers don't need to understand LangGraph or causal reasoning. They need to know: what is this system deciding, what data does it use, what are the consequences of an error, and how will we know if it starts making more of them?

In the insurance analytics pipeline, the conversation with the compliance team wasn't about the prompt architecture. It was: 'Here are the categories we're classifying. Here's the human baseline we benchmarked against. Here's the error rate, here's how we catch drift, here's what triggers a human review.' Once they could see the evaluation process was structured and the output was auditable, the conversation moved to how it integrated with their existing governance workflow rather than whether they trusted it.

The second thing I've found useful is showing the failure mode explicitly before they ask for it. Most people building AI systems present the upside and leave compliance to find the risks themselves. If you walk in and say 'here are the three conditions under which this system produces unreliable output, and here's how we handle each of them,' you shift from being a risk to being a risk manager. That's a very different conversation."

---

### Q8: Tell me about a time you turned a prototype into something genuinely reliable in production

**Use: Dialogflow migration — the clearest PoC-to-production transformation story**

"The most direct example is the Dialogflow migration I led — a high-volume voice bot handling 100,000+ monthly contacts for an enterprise client. When I came onto it, the model was in Dialogflow ES, it had 950 intents, and the F1 score was below 50%. It had grown by accretion — every new use case was a new intent, there was no underlying architecture, and coverage was poor.

What I actually did was throw away the PoC thinking and treat it as a production system design problem from scratch. I used HumanFirst to cluster 2 million customer utterances — the actual language customers were using — and rebuilt the intent architecture around what the data showed, not what someone had originally designed. That got the intent count from 950 to under 200 and the F1 score from below 50% to 96%. Coverage expanded to over 65% of intents at 70% confidence.

The reliability came from treating the model as a thing that needed to be continuously monitored and improved, not a thing that was built and shipped. The architecture we moved to was entity-based recognition, which meant it could handle variation in customer language rather than requiring exact-match training examples. And the evaluation framework — regular systematic analysis against the actual utterance distribution — meant degradation was detectable before it hit customers.

The thing I took from that engagement is that the gap between a working prototype and reliable production isn't primarily a technical gap. It's an architectural and evaluation discipline gap. The prototype worked in controlled testing. It failed in production because no one had designed for the full distribution of real customer language."

---

### Q9: What do you think is wrong with how most enterprises buy and deploy AI today?

**Use: Own delivery experience + align directly with CausalLens's "Death of AI PoCs" thesis**

"The main problem is that the evaluation model is completely disconnected from the deployment model. Enterprises run a PoC in a sandbox, it performs well against a curated dataset under controlled conditions, they approve it — and then it hits real integration complexity and breaks. 95% of generative AI pilots fail to reach production, and it's not because the demos were bad. It's because sandboxed testing doesn't surface the actual hard problems: messy upstream data, legacy system integration, edge cases in real user behaviour, latency under load, and the compliance questions that only appear when a real lawyer looks at the output.

I've seen this from the delivery side. The Microsoft Copilot evaluation I ran for a Canadian parcel delivery company was a four-week engagement that specifically set out to stress-test what the vendor's demo hadn't shown — RAG hallucination rates under real customer query distributions, NLU performance on their actual utterances rather than benchmark data. The findings were significantly different from what the vendor's PoC had implied. That's the gap enterprises consistently fall into: they evaluate the product the vendor wants to show them rather than the system they'll actually be running.

The second problem is that enterprises treat AI buying like software licensing — evaluate, sign, deploy, done. But an agentic system deployed into a regulated workflow is more like hiring a senior person into a compliance function. You'd never hire someone without a probation period and structured review. The equivalent for AI is a 30-day in-production deployment with defined success criteria before you commit. That's a completely different buying conversation to a PoC, and almost nobody structures it that way."

---

> ### ⚠️ Things I Need More Detail On
>
> Before the interview, it would help to sharpen these answers:
>
> 1. **Pharma/life sciences depth** — The Veeva customisation answer is built on research, not lived experience. If you have any client stories from HumanFirst that touched regulated industries (pharma, finance, insurance with compliance constraints), a specific anecdote would be more credible than a methodological answer.
>
> 2. **"What broke" in the insurance pipeline** — Do you have a specific failure story from that engagement? The answer above is solid but generic on the failure details. A concrete "this is the specific thing that went wrong and this is what I changed" would sharpen Q1 and Q8 significantly.
>
> 3. **The causal reasoning answer** — This is the one question where you're bridging from genuine adjacent experience (LLM evaluation, error pattern analysis) to their core thesis. It's honest and grounded, but they may probe further. Worth thinking through whether there's a cleaner example from your evaluation work where the distinction between "X was associated with failures" vs "X caused failures" was visible.
>
> 4. **Day 0 format** — The JD mentions a ~3-hour in-person challenge followed by a presentation and interviews. If you can find out what format the challenge takes before the interview (technical case study? live build? architecture whiteboard?), the answers above can be tuned accordingly. Worth asking in advance if you have a contact.

---

## Interview Strategy — Pre-Screening (15 Minutes)

### The Situation

A 15-minute pre-screening is almost certainly with a recruiter or hiring manager doing basic fit qualification, not a deep technical eval. The screener needs to answer: "Is this person worth putting in front of Day 0?" The goal is not to prove everything — it's to advance with enough signal that they're certain the answer is yes.

---

### Primary Strategy: Solution Provider

Walk in with a point of view, not a pitch. You've done the research. You understand what they're building. You have opinions about the hard problems in the space. The screener should feel like they're talking to someone who already thinks about forward-deployed AI delivery the same way CausalLens does — not someone who's excited to learn.

The anchor: **"Reliability is engineered, not emergent"** — this is their near-motto and it maps directly to how you actually work. Say it with ownership, not recognition.

---

### How to Open (if given a "tell me about yourself")

Lead with the outcome, then the frame:

> "I build production agentic pipelines — the kind that have to actually work when messy real-world data hits them, not just in demos. I've been doing this at HumanFirst across enterprise clients: a 50,000-conversation insurance analytics pipeline, a voice bot migration for 100,000 monthly contacts, a LinkedIn automation that processed 15,000 profiles in production. The common thread in everything I do is treating reliability as an engineering problem — state contracts at every step, validation before downstream steps fire, observability so failures are diagnosable rather than mysterious. That's the same framing I see in how CausalLens talks about agent architecture, which is part of why this role is interesting."

This does three things: anchors in production outcomes (not demos), uses their own language without sounding like you memorised their website, and signals you've read them seriously.

---

### Key Moves

**1. Use their vocabulary naturally, not performatively**
The phrases that land: "reliability is engineered not emergent," "the gap between the demo and production," "final-mile integration," "governance by default." Don't recite them — work them into answers where they genuinely fit.

**2. Position your evaluation/quality work as the differentiator**
Most AI engineers build things. Fewer build things with rigorous quality gates, human-baseline validation, and observable failure modes. That's your edge. Name it specifically when it comes up.

**3. Reference the client delivery pattern early**
This is a forward-deployed role. The screener needs confidence you can operate in a client environment autonomously. Reference the insurance firm engagement and the Canadian engineering firm enablement — these are your clearest evidence of client-facing delivery.

**4. Ask one diagnostic question**
At the first opportunity to flip the conversation:
> "The JD talks about leading delivery from concept to deployment — I'm curious what the typical split looks like between blueprint customisation work and client discovery/relationship time in practice?"

This signals you understand the role's shape, and it gives you information you actually need.

---

### Proactive Redirection — The Causal AI Gap

You have no direct causal AI implementation experience. They will notice eventually. Get there first if the conversation heads that way:

> "I should say clearly — I haven't implemented causal models directly. What I have is the adjacent experience: I've built the evaluation frameworks that surface the difference between 'this feature correlates with failures' and 'this is the mechanism that produces failures.' In my insurance pipeline work, that distinction was live — a model would confidently attribute escalations to the wrong cause. I've experienced what the lack of causal reasoning costs in practice, which is part of why the architecture makes sense to me. The learning curve is on the causal model calibration side — the delivery, reliability engineering, and client work is directly transferable."

Don't over-explain. One clean acknowledgement, pivot to what's real.

---

### Tactics

| Moment | Tactic |
|---|---|
| "Tell me about yourself" | Evidence-First Storytelling — outcome first, then mechanism |
| Any question about client delivery | Trojan Horse — embed client seniority inside the stories rather than claiming it |
| Any probe on causal AI | Proactive Redirection — surface and reframe before they form the doubt |
| Technical questions from a non-technical screener | Mirroring — translate to outcomes and business impact, not architecture |
| Any "why CausalLens?" question | Peer Framing — because the thesis is right, not because the opportunity is attractive |

---

### What to Avoid

- **Don't lead with HumanFirst as a company** — it won't be recognised. Lead with client outcomes and let them ask about the context.
- **Don't explain what LangGraph is** — if the screener is non-technical, it's noise; if they're technical, they know. Neither benefits from a definition.
- **Don't signal that you're excited to learn causal AI** — that frames you as a student. You're a practitioner with a gap, not a newcomer.
- **Don't fill silences with qualifications** — short answers invite follow-up. Long unprompted answers sound defensive.
- **Don't ask about salary or benefits in a pre-screening** — wait until they raise it or it's later in the process.
- **Don't mention Belgrade unless asked** — if asked about location, acknowledge it directly: you're based in Belgrade, open to relocation to London, and have been working fully remotely for [X years].

---

### Challenge and Critique

**Where this strategy could fail:**

1. **The screener goes technical immediately.** If it's actually an engineer running the pre-screening, the Solution Provider framing still works but the diagnostic question changes. Ask about the Factory toolchain and how much of the work is Python/LangGraph versus the proprietary abstraction.

2. **The causal AI gap lands harder than expected.** This is a causal AI company. If the screener is Darko or a senior engineer, "I haven't implemented causal models" might be a blocker regardless of how well it's reframed. The honest counter is that the role is delivery engineering, not causal model research — the JD doesn't list causal AI implementation as a requirement. Hold that ground if pushed.

3. **The opening sounds rehearsed.** The three-project opener is strong but can feel like a memorised pitch if delivered at speed. Slow it down. Let the outcomes land individually.

4. **Belgrade surfaces as a concern.** It might. Have a clean, confident answer ready: "I've been working remotely across enterprise clients for three years, and I'm open to relocating to London for the right role." Don't apologise for it.

5. **"Why are you leaving HumanFirst?"** This will come. Prepare something honest and brief: the role scope at CausalLens — forward-deployed, multi-client, production agentic systems at scale — is further along the trajectory you're on than what's available inside HumanFirst at this stage.

**The real risk with this strategy:** Coming across as over-prepared in a way that reads as artificial. The fix is to anchor every statement to a specific project or client outcome. Specificity reads as experience; polish without specificity reads as coaching.

---
