# Career Notes

---

## What Not to Build a Career Around

Standalone "prompt engineering," generic chatbot implementation, or commodity RAG setup. These capabilities still matter, but mostly as components inside broader, outcome-owning roles. Vendors are increasingly productizing the easy layer, and the durable value is shifting upward into workflow design, evaluation, domain specificity, and governance.

---

## Three Candidate Positions

### 1. Enterprise AI Workflow / Agentic Operations Architecture

**Why it stands out:** Sits at the centre of where spending is moving and where execution is weakest. Gives the broadest monetization surface: senior employee roles, consulting engagements, and eventual vertical product opportunities. Confidence: high.

**Why now:** Enterprises are increasing budgets fast, but most have not actually redesigned operating models or workflows. That gap will not be closed by generic prompting or one-off pilots.

**Why it is better than nearby alternatives:** Stronger than a generic "AI strategist" role because it owns implementation logic and business outcomes. Stronger than a pure product role because it can travel across functions and consulting contexts.

**What to avoid:** Vague AI strategy positioning, prompt-only consulting, or tool-first demo work with no workflow ownership.

**Best first move (next 6–12 months):** Build a portfolio around 2 concrete workflows (e.g. support operations and internal knowledge work). Show current-state process maps, target-state agent architecture, handoffs, eval design, governance, and an ROI model.

---

### 2. AI Evaluation, Reliability, and Assurance

**Why it stands out:** One of the most defensible spaces in the LLM stack, and one of the least crowded relative to its importance. Plays directly to conversational analysis and problem framing. Confidence: high.

**Why now:** More systems are reaching production, and buyers are realizing that generic benchmarks do not protect them in business-specific contexts. Observability, testing, and AI assurance are maturing into paid categories.

**Why it is better than nearby alternatives:** More durable than "prompt engineering" because it owns quality over time. More specialized and harder to outsource than generic QA.

**What to avoid:** Tool-only observability work that is detached from business KPIs or domain-specific evaluation criteria.

**Best first move (next 6–12 months):** Create a repeatable evaluation package: failure taxonomy, gold-set method, red-team checklist, regression dashboard logic, and a sample workflow audit.

---

### 3. Customer Service / Contact Center / Voice AI Transformation

**Why it stands out:** Cleanest direct extension of the target profile and one of the clearest live budget areas in AI. Combines strong demand with measurable outcomes and strong consulting monetization. Confidence: high.

**Why now:** AI in service is moving from FAQ bots to containment, agent assist, workflow automation, and voice systems tied to operations. Vendors, buyers, and startups are all converging on this space at once.

**Why it is better than nearby alternatives:** Stronger than generic "chatbot builder" work because the KPI model is clearer and the operational stakes are higher.

**What to avoid:** Low-end bot setup services or shallow prompt tuning without integration, QA, or escalation design.

**Best first move (next 6–12 months):** Specialise around one measurable outcome — containment + escalation quality, agent-assist productivity, or voice self-service for one workflow.

---

## Market Analysis

### The Most Common Professional Weakness

"Pilot competence" without "production competence." Shows up as: weak evaluation (no regression tests, no acceptance thresholds), weak observability (can't diagnose failures), and weak governance (no evidence trail). The market is reacting: AWS and Microsoft are explicitly packaging evaluation and guardrails as first-class platform features.

### Underdeveloped Capabilities Across the Industry

AI safety/security engineering for tool-using systems, AI incident response, and operational governance. OWASP's LLM risk taxonomy and NIST secure development guidance indicate that AI engineering is converging with security engineering, but most organisations still lack mature practices.

### Emerging Cross-Domain Areas

Strong potential, limited competition — at the "interfaces" between domains:
- Evaluation × product analytics
- Security × agents/tool permissions
- Governance × DevOps evidence automation
- RAG × enterprise IAM and data governance
- Inference optimisation × FinOps

These are under-served precisely because they require experience across multiple functions.

### Overhyped Areas

**Standalone GenAI job titles** remain a small share of postings. Indeed shows GenAI-term postings at 0.21% of US postings by Nov 2024 (growing quickly, but still rare), while AI-term postings more broadly were below the 2022 peak — consistent with a market where GenAI is being absorbed into existing roles rather than spawning endless new titles.

**"Agent everywhere" narratives** outpace most organisations' ability to scale. McKinsey shows substantial agent experimentation, but broad scaling is still not the norm, and Gartner stresses that autonomy introduces new risks requiring oversight.

### Core Market Pull

Three hard constraints organisations are already paying to solve: **quality/measurement**, **security of tool-using systems**, and **inference economics**.

---

## Skill Profiles

### Continuous LLM Evaluation Engineering

#### Definition

The ability to design and operate an evaluation and monitoring system that keeps an LLM application reliable as prompts, models, retrieval, and data change — so organisations can ship updates without quality regressions and can prove safety/quality to risk owners.

Buyers include enterprise platform teams scaling copilots, product companies monetising GenAI features, and consultancies paid to move clients from POC to production.

*Demand signal:* AWS has made RAG/model evaluation features generally available (including "bring your own inference"), and Microsoft is shipping an Azure AI Evaluation SDK.

#### Evidence Employers Will Accept

- A production-style evaluation harness with dataset versioning, evaluator definitions, score aggregation, and release gates. Include a sample report from at least two model/prompt variants.
- A RAG evaluation report with citation quality metrics (precision/coverage), showing measurement of "groundedness" with a before/after narrative tied to user impact.
- An online monitoring dashboard + incident analysis: top failure modes, drift signals, and at least one post-incident evaluation update that prevented recurrence.
- A/B test or canary results connecting evaluation metrics to a business KPI (containment/deflection, time-to-resolution, conversion, CSAT).
- A "model upgrade readiness" packet: evaluation comparison across candidate models (quality + safety + cost/latency) with a go/no-go recommendation and explicit risk trade-offs.
- A custom evaluator contribution (open source or internal) for a domain-specific constraint.
- A governance-ready audit trail: a lightweight "evaluation evidence register" mapping the evaluation regime to risk requirements (EU AI Act, NIST guidance).

#### Learning Path

1. Build a real RAG system with citation output using a managed knowledge base/retrieval stack.
2. Create an evaluation dataset: 200–500 queries representing real workflows, including messy and adversarial cases. Label a subset manually for calibration.
3. Operationalise offline evaluation using a production-oriented toolchain: AWS Bedrock Evaluations or Azure AI Evaluation SDK.
4. Add continuous release gating: wire evaluation into CI/CD so every prompt/retrieval/model change must pass defined thresholds.
5. Deploy minimal observability: log prompts, retrieval context IDs, model version, and evaluation sampling. Produce one monthly "quality & risk report."

#### Primary Employers and Titles

Enterprise GenAI platform teams; SaaS companies productising copilots; consultancies implementing production GenAI; cloud vendors and AI tooling companies.

Titles: LLMOps/GenAIOps Engineer; AI Quality Engineer; LLM Evaluation Specialist; ML Engineer (GenAI) — Reliability; AI Product Engineer; Applied Scientist (Evaluation/Measurement).

#### Why It's Defensible

Hard to automate because the premium work is choosing what to measure, designing rubrics that reflect business risk, diagnosing failures across retrieval + prompts + user intent, and negotiating trade-offs with stakeholders.

Compounds because evaluation becomes the "control plane" for everything else: once you can measure system quality, you can safely adopt new models, new retrieval approaches, and agentic workflows with less risk.

#### First-Year Outcomes

- Reduce severe quality regressions by 30–60% vs baseline releases via release gates.
- Improve grounded answer rate in a RAG assistant by +15–30 percentage points, with a reproducible evaluation report used by product/risk stakeholders.
- Reduce model/prompt change cycle time by 25–40% by replacing ad-hoc manual testing with repeatable evaluation runs.

---

### LLM Inference Cost Engineering

#### Definition

The ability to serve LLMs (and GenAI workloads such as RAG and agent calls) with predictable latency and throughput at sustainable unit economics, using batching, caching, quantisation, routing, and disciplined cost measurement — so GenAI roll-outs don't collapse under GPU costs.

Buyers include product companies with high request volumes, enterprise platform teams rolling out copilots broadly, and cloud/infra vendors supporting customers' production deployments.

*Demand signal:* GenAI spend is large and rising (Gartner 2025 forecast) and FinOps bodies are explicitly publishing "FinOps for AI" guidance, indicating recurring organisational need to plan, allocate, forecast, and optimise AI spend.

#### Evidence Employers Will Accept

- A reproducible inference benchmark report (tokens/sec, p50/p95 latency, error rate, GPU utilisation) before and after optimisation using a credible serving engine (e.g., vLLM).
- A production-ish model server deployment using NVIDIA Triton Inference Server.
- Quantisation and batching impact evidence using TensorRT-LLM, with an "accuracy vs cost" chart and a go/no-go threshold tied to product needs.
- A multi-model routing policy that chooses models based on SLA/cost with measured savings and no material quality regression.
- An "AI unit economics" dashboard: cost per conversation, cost per resolved ticket, cost per document processed; with budget alerting and forecasting.
- A token waste reduction programme showing reductions in unnecessary tool calls/long prompts/retry loops with measured impact on success rate.
- Meaningful open-source contributions to inference tooling (vLLM/Triton/TensorRT-LLM).

#### Learning Path

1. Build and measure a baseline serving stack using vLLM with a clear benchmark harness.
2. Add a production-grade serving layer via Triton Inference Server.
3. Optimise for cost/performance: implement continuous batching, caching, and quantisation. Record before/after.
4. Wrap in FinOps discipline: define AI cost units, build allocation and forecasting using FinOps for AI guidance.
5. Close the loop with quality gates: connect cost optimisations to evaluation results.

#### Primary Employers and Titles

High-volume AI product companies; enterprise AI platform teams; cloud/infra vendors; consultancies delivering cost and performance turnarounds.

Titles: Inference Engineer; AI Infrastructure Engineer; ML Platform Engineer; Performance Engineer (LLM Serving); AI SRE; FinOps for AI / AI Cost Engineer.

#### Why It's Defensible

Depends on real workloads, messy constraints (SLAs, burstiness, compliance boundaries), hardware realities, and organisational trade-offs. Tooling can assist but cannot replace an engineer who can diagnose bottlenecks end-to-end.

Compounds because cost optimisation becomes more important at scale: every additional user, workflow, and agent action multiplies spend.

#### First-Year Outcomes

- Reduce inference cost per successful task by 20–50% through batching, caching, routing, and prompt/tool efficiency.
- Improve p95 latency by 20–40% and throughput by 1.5–3× for a defined workload after serving optimisations.
- Establish an AI cost governance baseline with allocation, budget alerting, and forecasting for one GenAI product line.

---

## Opportunity Space Strategies

*Detailed strategy breakdowns — see also career-other-notes.md*

### AI Evaluation Strategies

#### Release Gatekeeping System

Turn evaluation into a release governance mechanism that decides what ships. The moat: becoming the organisation's risk-reducing accelerator by embedding evaluation into CI/CD.

**Proof employers accept:**
- CI pipeline running evaluation on every prompt/model/retrieval change with hard go/no-go thresholds
- Quarterly "model upgrade readiness" pack: evaluation deltas, risk notes, rollout plan
- Audit trail of evaluation datasets and evaluator versions
- Evidence that regressions per release dropped materially after gates were added
- Documented escalation/override procedure for urgent releases

**Build steps:**
1. Use AWS Bedrock RAG Evaluation GA or Azure Evaluation SDK to establish baseline metrics and weekly runs
2. Add citation metrics and grounding checks for RAG outputs
3. Wire into CI/CD and define "release stop" thresholds aligned to customer impact

**Buyers/titles:** Product engineering and platform leadership; regulated operations. Titles: AI Quality Lead, LLMOps Engineer (evaluation), Applied Scientist (measurement).

**Risks:**
- Gate metrics become "gameable" → mitigate with periodic human review panels + adversarial sets
- Evaluation slows shipping → mitigate with fast "smoke eval" + deeper nightly runs

**First-year outcomes:**
- Reduce customer-visible severe regressions by 30–60%
- Reduce time-to-deploy model/prompt changes by 20–35%

---

#### KPI-Linked Evaluation

Build evaluation that predicts business outcomes (conversion, containment, cycle time), segmented by user cohort and workflow.

**Proof employers accept:**
- Mapping of evaluation metrics to business KPIs with a dashboard
- A/B test results where evaluation predicted a KPI change with rollout recommendation
- Cohort analysis: which user segments benefit/hurt, and mitigation plan
- "Value per £ token" report linking to cost engineering and budget allocation
- One documented case where evaluation blocked expansion due to predicted KPI harm

**Build steps:**
1. Choose one workflow where AI impacts measurable KPI
2. Build an evaluation dataset mirroring production distribution
3. Run controlled A/B tests and build a KPI predictive model/heuristic

**Buyers/titles:** Product managers, ops leaders, analytics leaders. Titles: AI Product Analyst (GenAI), Evaluation Lead, LLM Product Engineer.

**Risks:**
- Proxy metrics mislead → mitigate by continually validating against real outcome metrics
- Data privacy limits measurement → mitigate with aggregate metrics and privacy-preserving logging

**First-year outcomes:**
- Improve a target KPI by 10–20% while maintaining risk thresholds
- Reduce spend wasted on low-impact use cases by 15–25%

---

#### Adversarial Drift Lab

Build a continuous lab that stress-tests models/agents against evolving failure modes (prompt attacks, drift, retrieval poisoning).

**Proof employers accept:**
- Red-team/adversarial dataset with monthly updates and tracked pass rates
- Drift detection dashboard (quality, safety, and tool-use error signals by version/cohort)
- Documented process connecting new incidents → new tests → new gates
- Integration of guardrails into evaluation runs
- Quarterly "risk burn-down" report for leadership

**Build steps:**
1. Stand up baseline evaluation using AWS RAG Eval GA or Azure Evaluation SDK
2. Add adversarial prompts and tool-misuse simulations; run nightly
3. Connect to runtime guardrails and measure catch rates vs false positives

**Buyers/titles:** Platform reliability teams, security/risk teams, regulated product lines. Titles: AI Reliability Engineer, AI Safety/Evaluation Lead, Applied Scientist (robustness).

**Risks:**
- Red-team becomes theatre → mitigate with operational metrics (incidents prevented, regressions caught)
- Overblocking harms user experience → mitigate by tracking false positives and adjusting thresholds

**First-year outcomes:**
- Decrease high-severity AI incidents by 25–50%
- Cut time to root-cause model regressions by 30–40%

---

### Agentic Automation Strategies

#### Agent Operating System

Build reusable "agent OS" primitives — tool contracts, memory policies, permissioning, evaluation hooks — so the organisation can launch many agents safely.

**Proof employers accept:**
- Standard tool schema and permission model used across at least two agent workflows
- "Agent templates" repo: orchestration, retries, idempotency, safety checks, logging
- Integrated evaluation pipeline for agent workflows
- Playbook for deploying agents into IT/service ops
- Evidence of reduced build time for new agent workflows

**Build steps:**
1. Choose a platform context (ServiceNow AI Platform or Salesforce agent ecosystem) and implement two distinct workflows
2. Standardise tool APIs and permissions; add human approval for high-impact actions
3. Integrate evaluation and guardrails; require passing tests before expanding scope

**Buyers/titles:** CIO/COO transformation leaders, enterprise platforms, product orgs. Titles: AI Workflow Architect, Agent Platform Engineer, Automation Lead.

**Risks:**
- Overbuilding a platform before proving value → mitigate by shipping 2 workflows that share 70–80% primitives
- Tool sprawl and permission creep → mitigate with autonomy tiering and least privilege

**First-year outcomes:**
- Reduce time to launch a new agent workflow by 30–50%
- Improve agent task success rate by 10–20 points

---

#### Human Control Tower

Build a "control tower" for monitoring, escalation, and human oversight across many agents.

**Proof employers accept:**
- Central dashboard: agent success rate, tool errors, escalations, and policy violations per workflow
- Escalation playbook (when the agent must hand off; how humans correct and feed back)
- Incident response process for agent failures
- Evidence of reduced human workload variance
- One quarterly governance review showing decisions based on control tower data

**Build steps:**
1. Instrument agent workflows with standard telemetry and evaluation sampling
2. Define escalation rules and build UX for human approval/override
3. Run "agent incident drills" and update the playbook monthly

**Buyers/titles:** Service operations leaders, platform reliability teams, risk/compliance. Titles: Agent Ops Lead, AI Operations Manager, AI SRE.

**Risks:**
- Over-alerting creates fatigue → mitigate with tiered alerts and SLO-based paging
- Insufficient human capacity for escalations → mitigate with autonomy tiers and improving agent reliability

**First-year outcomes:**
- Reduce escalations requiring engineer intervention by 25–40%
- Increase safe agent containment by 10–20 points in one function

---

#### Autonomy Tiering

Define and implement a tiered autonomy model ("copilot", "delegate", "autopilot") with explicit approval gates, cost budgets, and risk controls.

**Proof employers accept:**
- Published autonomy policy with tool permissions, approval requirements, and audit logs per tier
- Evidence that higher tiers have stricter evaluation gates and monitoring
- Cost budgets per tier enforced by FinOps controls
- Case study expanding one workflow from copilot → delegate with measured incident rates and ROI
- Procurement-friendly documentation of autonomy boundaries

**Build steps:**
1. Draft tier definitions aligned to risk and reversibility of actions
2. Implement tier-based access controls and human approval
3. Add tier-based budgets and throttles using FinOps for AI guidance

**Buyers/titles:** Enterprise transformation, risk/compliance, IT/service ops. Titles: AI Workflow Architect, Governance Engineer, Agent Platform PM.

**Risks:**
- Autonomy tiers too rigid, blocking value → mitigate with pilot waivers and time-boxed exceptions
- Approval friction overwhelms users → mitigate with tier selection and progressive automation only after KPI gains

**First-year outcomes:**
- Expand one agent workflow to a higher autonomy tier while keeping incident rate under threshold
- Reduce average human time per task by 15–25% in a targeted workflow

---

### Forward-Deployed Engineering Strategies

#### Implementation Kit Productisation

Turn implementation lessons into repeatable assets: templates, reference architectures, and automated checks that reduce delivery cost and increase reliability.

**Proof employers accept:**
- Reusable "go-live kit": architecture template, security checklist, evaluation harness, runbooks
- Deployment acceleration metric (time-to-first-value reduced across projects)
- Customer-facing case study with production KPIs
- Open-source or internal tooling automating integration steps
- Post-implementation adoption playbook

**Build steps:**
1. Pick one vertical workflow (IT service desk, sales ops, contact centre) and deliver a reference build
2. Standardise evaluation and guardrails
3. Convert implementation steps into a kit with checklists and automation; iterate on next deployment

**Buyers/titles:** AI vendors, consultancies, integrators, large enterprises. Titles: Forward-Deployed Engineer, Solutions Engineer (AI), Customer Success Engineer (GenAI), Implementation Consultant.

**Risks:**
- Assets become tool-specific → mitigate with "BYO inference" evaluation harnesses and vendor-agnostic control patterns
- Customers resist standardisation → mitigate by making kits configurable with risk tiers and governance hooks

**First-year outcomes:**
- Reduce "time to production" on similar deployments by 30–50%
- Improve first-90-days stability: 20–40% fewer high-severity incidents

---

#### Procurement-to-Production Bridge

Treat procurement, contracting, and governance as part of delivery — reducing friction between legal/procurement and engineering.

**Proof employers accept:**
- Pre-built "procurement evidence pack" (security, evaluation, data handling, change management)
- Contract clause templates for model updates, logging, and incident response
- Governance + evaluation checklist used to unblock at least one production approval
- AI literacy rollout plan for the customer organisation
- "Vendor due diligence scorecard" reusable across accounts

**Build steps:**
1. Build a standard evidence pack aligned to EU AI Act timeline milestones and NIST guidance
2. Integrate evaluation tooling outputs into the pack
3. Run a joint workshop with legal/procurement + engineering on one deployment

**Buyers/titles:** AI vendors selling to enterprises; consultancies; internal enterprise AI enablement. Titles: Forward-Deployed Engineer, Solutions Architect, AI Delivery Lead, Technical Programme Manager (AI).

**Risks:**
- Becomes paperwork-heavy → mitigate by automating evidence capture
- Misalignment with local regulation interpretations → mitigate by separating "required" vs "recommended" controls

**First-year outcomes:**
- Reduce procurement/security review cycle time by 20–35%
- Increase POC → production conversion rate by 10–20 points

---

#### Vertical Outcome Moat

Own a vertical workflow and KPI plus repeatable delivery assets, becoming the default expert for a revenue-bearing outcome.

**Proof employers accept:**
- Vertical playbook with metrics, failure modes, and evaluation datasets tailored to that workflow
- Two case studies in the same vertical showing comparable KPI improvements
- Reusable integration blueprint (systems, data sources, tool actions)
- Training package (AI literacy + operator SOPs) specific to that workflow
- Benchmark pack demonstrating why the chosen workflow is suited for agents

**Build steps:**
1. Choose one vertical workflow where agents are already appearing (service ops/IT, knowledge management)
2. Build a reference implementation on one major platform
3. Standardise evaluation + cost + governance artefacts and reuse across a second project

**Buyers/titles:** Vertical SaaS vendors, consultancies, enterprise centres of excellence. Titles: Forward-Deployed Engineer (Vertical), AI Workflow Architect, Solutions Consultant.

**Risks:**
- Vertical selection fails (low data quality, low ROI) → mitigate by choosing workflows with clear KPIs and proving pilots fast
- Platform dependency → mitigate by documenting portable patterns and evaluation datasets

**First-year outcomes:**
- Deliver 1–2 repeatable deployments with measurable KPI gains (+10–20% containment or −15–25% cycle time)
- Improve delivery margin/time-to-value (20–30% fewer delivery hours on second deployment)

---

### AI Governance & Model Risk Architecture

#### What This Actually Is

Designing and operationalizing governance systems for LLMs and generative AI inside regulated or high-risk environments (finance, healthcare, insurance, government). Not AI ethics philosophy — but:
- Model risk classification frameworks
- AI audit trails and traceability
- Human-in-the-loop review workflows
- Bias and fairness monitoring systems
- AI policy enforcement mechanisms
- Compliance mapping (EU AI Act, NIST AI RMF, ISO 42001)

#### The Core Business Problem

Executives want AI deployed. Legal and risk teams are blocking it. Enterprises cannot scale AI without auditability, risk controls, documentation, monitoring systems, and clear accountability structures. Without governance architecture, AI stays stuck in pilot mode.

#### Why Demand Will Grow

- EU AI Act enforcement timeline
- US financial regulators increasing AI scrutiny
- Board-level accountability for AI risk
- Insurance carriers asking AI governance questions
- Public incidents (hallucinations, bias, compliance failures)

Every enterprise AI deployment now triggers governance review.

#### Why Talent Is Scarce

Most AI professionals don't understand regulatory environments or enterprise compliance workflows, and can't translate model behaviour into legal risk frameworks. Most compliance professionals don't understand LLM systems. This is a rare bridge skill.

#### Who Pays

Banks, insurance companies, healthcare systems, government contractors, Fortune 500 compliance-driven enterprises. Large budgets, low risk tolerance.

---

### Enterprise AI Workflow Orchestration & Integration Architecture

#### What This Actually Is

Designing and implementing production AI workflows that integrate LLMs, internal databases, APIs, CRM systems, ERP systems, document stores, and automation tools. Not building demos — designing end-to-end AI-enabled business processes.

#### The Core Business Problem

Most companies have 200+ SaaS tools, fragmented data, manual workflows, and no unified automation layer. LLMs alone don't create ROI. Integrated AI workflows do.

#### Real Demand Signals

- Massive hiring for AI integration engineers
- Growth of orchestration platforms (LangChain, LlamaIndex, Airflow + LLM layers)
- Consulting demand for "AI transformation" projects
- RPA vendors embedding LLM layers
- Enterprise AI budget shifting from experimentation to deployment

#### Why Talent Is Scarce

Most AI engineers focus on model performance and don't understand enterprise systems. Most IT integration professionals don't understand LLM constraints or prompt engineering. Bridging AI and enterprise systems is rare.

#### Why It's Defensible

- Requires deep institutional knowledge
- Requires understanding messy internal systems
- Involves stakeholder coordination
- Accumulates contextual leverage over time

#### Who Pays

Mid-market and enterprise companies, operations-heavy businesses, consulting firms implementing AI transformation. Revenue-linked work — budgets are real.
