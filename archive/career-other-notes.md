# Advanced Strategies by Opportunity Space

---

## AI Cost Engineering

**Demand anchor:** GenAI spend is forecast to surge and 80% of 2025 GenAI spend is expected to go to hardware, making inference economics a board-level constraint rather than a technical optimisation project. FinOps bodies have explicitly created "FinOps for AI" guidance, signalling institutionalisation of AI cost management.

---

### Strategy: Unit Economics Ownership

**Description:** Move beyond "reduce GPU cost" into owning the full unit economics of AI features (cost-to-serve, margin, and pricing levers), turning cost engineering into product strategy. The moat: you become the person who can convert hardware-heavy spend into profitable packaging decisions — two steps beyond current infra roles.

**Proof employers accept:**
- A production "AI cost per successful outcome" dashboard (e.g., £/resolved ticket, £/qualified lead, £/completed workflow), with attribution to model, prompt, retrieval, and tool calls
- A pricing/packaging memo linking cost curves to tiering (free vs paid, limits, throttles) and showing simulated margin impact
- A cost–quality trade study showing "cheaper model + guardrails + evaluation gates" achieves target KPI at lower cost
- Chargeback/showback policy applied to at least one business unit, including budgeting alerts and consumption thresholds
- Post-mortem of one cost incident (runaway retries/tool loops) with remediation and measured drop in token waste

**Build steps:**
1. Instrument cost drivers (tokens, tool calls, retrieval calls, GPU hours) and connect to a FinOps reporting baseline
2. Create a unit metric for one workflow (e.g., cost per resolved IT ticket) and validate against business reporting
3. Introduce controlled experiments (model routing, caching, prompt changes) with evaluation gates
4. Propose packaging levers (rate limits, premium model tier) and measure impact over 4–8 weeks

**Buyers/titles:** CFO/FinOps leads, platform product managers, AI platform heads. Titles: AI Cost Engineer, Inference/Platform Engineer, FinOps for AI Lead, AI Product Ops (unit economics).

**Risks:**
- Becoming "finance-only" and losing technical credibility → keep a reproducible benchmark + optimisation pipeline attached to every pricing decision
- Perverse incentives (teams reduce cost by hurting outcomes) → mitigate via KPIs that are outcome-linked and gated by evaluation

**First-year outcomes:**
- Reduce cost per successful workflow by 20–40% while holding quality above defined release gates
- Launch one AI feature tier/pricing policy with measured margin improvement (e.g., +5–15% contribution margin on AI add-on)

---

### Strategy: Portfolio Routing Layer

**Description:** Build a reusable model/hardware routing layer (multi-model, multi-region, fallback) that turns cost engineering into a platform capability shared across products. The structural advantage is "portfolio optionality": reduce vendor lock-in and adopt better models/hardware without breaking workflows.

**Proof employers accept:**
- A router service with documented policies (complexity-based model choice, latency SLOs, cost ceilings) and audit logs
- Benchmark report showing throughput/latency improvements under load plus stable success rates under evaluation
- A failover playbook (model/provider outage → safe degrade) tested via simulations
- A migration case study: "model A → B" completed with <X% KPI regression due to routing + evaluation gates
- Evidence of reduced P0 incidents caused by provider limits/timeouts

**Build steps:**
1. Define routing inputs: request type, risk tier, latency budget, maximum cost per request
2. Implement canary routing and integrate evaluation into rollout
3. Add observability: per-route cost, error rates, user outcomes; build automated rollbacks on quality regressions
4. Build provider portability in contracts and operational docs

**Buyers/titles:** AI platform teams, infra teams, product orgs with multiple GenAI features. Titles: Inference Engineer, Platform Engineer, AI SRE, LLMOps Engineer.

**Risks:**
- Router becomes a bottleneck/service reliability issue → mitigate with SRE-grade engineering and staged rollout
- "Optimising for cost" triggers quality complaints → mitigate with hard evaluation gates and user-segmented KPIs

**First-year outcomes:**
- Cut p95 latency by 20–35% and/or reduce cost per 1k tasks by 15–30% via routing and caching
- Reduce provider-related incidents (timeouts/rate limits) by 30–50% through failover and throttling controls

---

### Strategy: Policy-as-Code FinOps

**Description:** Go beyond dashboards to implement enforceable cost controls: quotas, budget guardrails, automated approvals for high-autonomy agents, and policy-as-code for model usage. The moat is organisational leverage — your controls allow the business to scale AI without runaway spend or chaotic exceptions.

**Proof employers accept:**
- A policy repository (quotas, rate limits, model allowlists by risk tier) with automated enforcement
- Budget alerts + automated throttling for over-budget workloads with documented business exception process
- "AI spend governance" playbook aligned to FinOps for AI scope (allocation, forecasting, optimisation)
- One quarter of showback reporting and outcomes (teams reduced token waste by X%)
- Integration with evaluation: policies reference minimum quality thresholds

**Build steps:**
1. Adopt FinOps for AI terminology and scopes; define cost ownership and chargeback model
2. Implement automated constraints based on model, tool permission, and autonomy tier
3. Create an exception workflow tied to business approvals and time-bounded overrides

**Buyers/titles:** FinOps leadership, platform leadership, governance councils. Titles: FinOps for AI Lead, AI Platform Governance Lead, AI Infrastructure Engineer with governance remit.

**Risks:**
- Controls block innovation → mitigate with sandbox environments + fast exception paths
- Policy drift (rules not updated as models change) → mitigate with quarterly policy review tied to spend and incident metrics

**First-year outcomes:**
- Reduce unallocated AI spend to <5–10% of total AI spend
- Prevent at least one major cost incident via automated throttles

---

## AI Evaluation

**Demand anchor:** AWS is productising RAG evaluation GA (BYO inference + citation metrics), and Microsoft is shipping an Azure AI Evaluation SDK, signalling that enterprises want measurable, repeatable evaluation — especially as most organisations are still not scaled and agents are rising.

---

### Strategy: Release Gatekeeping System

**Description:** Turn evaluation into a release governance mechanism that decides what ships, not a "nice-to-have report." The moat: becoming the organisation's risk-reducing accelerator by embedding evaluation into CI/CD and change approval.

**Proof employers accept:**
- CI pipeline that runs evaluation on every prompt/model/retrieval change with hard go/no-go thresholds
- A quarterly "model upgrade readiness" pack: evaluation deltas, risk notes, rollout plan
- Audit trail of evaluation datasets and evaluator versions
- Evidence that regressions per release dropped materially after gates were added
- Documented escalation/override procedure for urgent releases

**Build steps:**
1. Use AWS Bedrock RAG Evaluation GA or Azure Evaluation SDK to establish baseline metrics and weekly runs
2. Add citation metrics and grounding checks for RAG outputs (precision/coverage)
3. Wire into CI/CD and define "release stop" thresholds aligned to customer impact

**Buyers/titles:** Product engineering and platform leadership; regulated operations. Titles: AI Quality Lead, LLMOps Engineer (evaluation), Applied Scientist (measurement).

**Risks:**
- Gate metrics become "gameable" → mitigate with periodic human review panels + adversarial sets
- Evaluation slows shipping → mitigate with fast "smoke eval" + deeper nightly runs

**First-year outcomes:**
- Reduce customer-visible severe regressions by 30–60%
- Reduce time-to-deploy model/prompt changes by 20–35%

---

### Strategy: KPI-Linked Evaluation

**Description:** Go beyond "helpfulness scores" to build evaluation that predicts business outcomes (conversion, containment, cycle time), segmented by user cohort and workflow. The moat: you become the bridge between AI engineering and executive decision-making.

**Proof employers accept:**
- A mapping of evaluation metrics to business KPIs (correlation or causal testing) with a dashboard
- A/B test results where evaluation predicted a KPI change with rollout recommendation
- Cohort analysis: which user segments benefit/hurt, and mitigation plan
- A "value per £ token" report linking to cost engineering and budget allocation decisions
- One documented case where evaluation blocked expansion due to predicted KPI harm

**Build steps:**
1. Choose one workflow where AI impacts measurable KPI
2. Build an evaluation dataset that mirrors production distribution (including long-tail queries)
3. Run controlled A/B tests and build a KPI predictive model/heuristic

**Buyers/titles:** Product managers, ops leaders, analytics leaders. Titles: AI Product Analyst (GenAI), Evaluation Lead, LLM Product Engineer.

**Risks:**
- Proxy metrics mislead → mitigate by continually validating against real outcome metrics and revising rubrics
- Data privacy limits measurement → mitigate with aggregate metrics and privacy-preserving logging

**First-year outcomes:**
- Improve a target KPI (e.g., containment or analyst cycle time) by 10–20% while maintaining risk thresholds
- Reduce spend wasted on low-impact use cases by 15–25%

---

### Strategy: Adversarial Drift Lab

**Description:** Build a continuous lab that stress-tests models/agents against evolving failure modes (prompt attacks, drift, retrieval poisoning). Anticipates the second-order consequences of agents: as autonomy rises, failure impact rises, so resilience becomes a competitive moat.

**Proof employers accept:**
- A red-team/adversarial dataset with monthly updates and tracked pass rates
- Drift detection dashboard (quality, safety, and tool-use error signals by version/cohort)
- A documented process connecting new incidents → new tests → new gates (closed-loop)
- Integration of guardrails into evaluation runs
- Quarterly "risk burn-down" report for leadership

**Build steps:**
1. Stand up baseline evaluation using AWS RAG Eval GA or Azure Evaluation SDK
2. Add adversarial prompts and tool-misuse simulations; run nightly
3. Connect to runtime guardrails (AWS Guardrails or Azure Prompt Shields) and measure catch rates vs false positives

**Buyers/titles:** Platform reliability teams, security/risk teams, regulated product lines. Titles: AI Reliability Engineer, AI Safety/Evaluation Lead, Applied Scientist (robustness).

**Risks:**
- Red-team becomes theatre → mitigate with operational metrics (incidents prevented, regressions caught)
- Overblocking harms user experience → mitigate by tracking false positives and adjusting thresholds

**First-year outcomes:**
- Decrease high-severity AI incidents by 25–50%
- Cut "time to root-cause" for model regressions by 30–40%

---

## AI Governance

**Demand anchor:** The EU AI Act applies progressively with major obligations from 2025 onward. Deloitte finds leaders expect rapid GenAI transformation, yet only ~a quarter feel highly prepared on governance/risk — creating a multi-year capability build gap.

---

### Strategy: Evidence Factory

**Description:** Move beyond policy documents to build an "evidence factory": automated, continuously updated governance artefacts (risk registers, eval logs, access controls, incident logs) that make audits and procurement faster.

**Proof employers accept:**
- A governance evidence register that auto-populates from telemetry: model versions, datasets, evaluations, incidents
- EU AI Act readiness file: mapping obligations to controls and evidence sources, updated monthly
- ISMS/AIMS integration: documented alignment to ISO/IEC 42001 management system model
- Automated documentation generation (model cards/system cards) from CI/CD and logs
- "Audit dry run" report showing time saved vs prior manual approach

**Build steps:**
1. Pick one AI system and create a minimum evidence schema aligned to NIST AI 600-1 categories + EU AI Act milestones
2. Instrument pipelines so evaluation results and versioning automatically write to the evidence store
3. Build dashboards and monthly sign-off workflow (compliance + product)

**Buyers/titles:** Risk/compliance functions, internal audit, platform governance councils. Titles: AI Governance Lead, Model Risk Manager, Responsible AI Engineer, Compliance Automation Lead.

**Risks:**
- Evidence without real controls → mitigate by tying every document to an enforced control (access, guardrails, evaluation gates)
- Scope creep → mitigate by starting with one "high exposure" workflow and expanding by templates

**First-year outcomes:**
- Cut time to produce audit/procurement evidence by 40–60%
- Reduce governance-related deployment delays by 25–40%

---

### Strategy: GPAI Vendor Due Diligence

**Description:** Anticipate that governance will increasingly be about vendor ecosystems (GPAI providers, model brokers, evaluation tools, safety layers), not just internal models. The moat is procurement leverage: standardise contracts, SLAs, evidence requirements, and exit options.

**Proof employers accept:**
- A "GPAI vendor scorecard" template: security, evaluation transparency, data handling, monitoring, incident response
- Contract clauses library for GenAI (audit rights, logging, data retention, model change notifications)
- A vendor onboarding playbook tying evaluation requirements to integration steps
- A de-risked migration plan (multi-model strategy) with exit routes
- One executed vendor selection/renewal decision with documented decision trail

**Build steps:**
1. Map NIST AI 600-1 risk categories to vendor questions and evidence requests
2. Create a pilot vendor evaluation harness (quality + safety + cost)
3. Build a standard "model change management" process

**Buyers/titles:** Procurement, legal, enterprise architecture, risk owners. Titles: AI Vendor Manager, AI Procurement Lead, Model Risk Officer, AI Governance PM.

**Risks:**
- Over-engineering slows adoption → mitigate with tiered due diligence by risk level
- Procurement lacks technical buy-in → mitigate by pairing scorecard with evaluation runs and crisp executive summaries

**First-year outcomes:**
- Reduce time to approve a new model/vendor by 20–35% via standardised due diligence
- Reduce concentration risk: ensure top workflows can switch providers within X weeks

---

### Strategy: AI Literacy Operating Model

**Description:** Treat AI literacy as an operating model: role-based training + controls + oversight processes, not generic education. Goes beyond current hiring by creating scalable human governance — especially as AI literacy is already required under Article 4 and as agents spread across functions.

**Proof employers accept:**
- Role-based AI literacy curriculum mapped to provider vs deployer responsibilities and risk tiers
- Training completion metrics + proficiency checks tied to job roles
- A "human oversight playbook" (when to escalate to humans, approval gates for irreversible actions)
- Reduced incident rate correlated with training rollout (pre/post)
- Evidence of compliance alignment using the Commission FAQ guidance points

**Build steps:**
1. Use the EC AI literacy FAQ to define minimum expectations and tailor by role and risk
2. Implement training + access controls: only trained users can operate high-risk tools/agents
3. Run quarterly tabletop exercises (prompt attacks, hallucination incidents, agent mis-actions) and update procedures

**Buyers/titles:** HR/L&D, compliance, operational leaders, platform governance. Titles: AI Governance Lead, Responsible AI Programme Manager, AI Enablement Lead.

**Risks:**
- Training becomes checkbox compliance → mitigate with scenario-based assessments and incident drills
- High staff turnover → mitigate by integrating literacy into onboarding and access provisioning

**First-year outcomes:**
- Achieve ≥85–95% role-based AI literacy coverage for in-scope staff; reduce policy violations/incidents by 20–40%
- Reduce time for safe rollout of new AI tools by 15–30%

---

## Agentic Automation

**Demand anchor:** Gartner predicts that by 2028, one-third of GenAI interactions will use action models/autonomous agents, and McKinsey reports 23% scaling agentic AI somewhere — yet scaling within any single function remains limited, highlighting a "hard work to do it well" gap. Vendor launches (Salesforce Agentforce, ServiceNow AI Platform) validate that agents are becoming a mainstream product category.

---

### Strategy: Agent Operating System

**Description:** Build reusable "agent OS" primitives — tool contracts, memory policies, permissioning, evaluation hooks — so the organisation can launch many agents safely rather than building one-off bots. The moat is platform externalities: every new agent inherits reliability and governance.

**Proof employers accept:**
- A standard tool schema and permission model used across at least two agent workflows
- "Agent templates" repo: orchestration, retries, idempotency, safety checks, logging
- Integrated evaluation pipeline for agent workflows (success rate, tool-call accuracy, citation grounding)
- A playbook for deploying agents into IT/service ops
- Evidence of reduced build time for new agent workflows

**Build steps:**
1. Choose a platform context (ServiceNow AI Platform or Salesforce agent ecosystem) and implement two distinct workflows
2. Standardise tool APIs and permissions; add human approval for high-impact actions
3. Integrate evaluation and guardrails; require passing tests before expanding scope

**Buyers/titles:** CIO/COO transformation leaders, enterprise platforms, product orgs. Titles: AI Workflow Architect, Agent Platform Engineer, Automation Lead.

**Risks:**
- Overbuilding a platform before proving value → ship 2 workflows that share 70–80% primitives
- Tool sprawl and permission creep → mitigate with autonomy tiering and least privilege

**First-year outcomes:**
- Reduce time to launch a new agent workflow by 30–50%
- Improve agent task success rate by 10–20 points via standardised workflows + evaluation gates

---

### Strategy: Human Control Tower

**Description:** Build a "control tower" for monitoring, escalation, and human oversight across many agents. The moat is organisational safety at scale — deeply coupled to internal workflows and risk tolerance.

**Proof employers accept:**
- A central dashboard: agent success rate, tool errors, escalations, and policy violations per workflow
- An escalation playbook (when the agent must hand off; how humans correct and feed back)
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

### Strategy: Autonomy Tiering

**Description:** Define and implement a tiered autonomy model ("copilot", "delegate", "autopilot") with explicit approval gates, cost budgets, and risk controls. Enables safe expansion of autonomy without rewriting governance each time.

**Proof employers accept:**
- A published autonomy policy with tool permissions, approval requirements, and audit logs per tier
- Evidence that higher tiers have stricter evaluation gates and monitoring
- Cost budgets per tier enforced by FinOps controls
- A case study expanding one workflow from copilot → delegate with measured incident rates and ROI
- Procurement-friendly documentation of autonomy boundaries

**Build steps:**
1. Draft tier definitions aligned to risk and reversibility of actions
2. Implement tier-based access controls and human approval
3. Add tier-based budgets and throttles using FinOps for AI guidance

**Buyers/titles:** Enterprise transformation, risk/compliance, IT/service ops. Titles: AI Workflow Architect, Governance Engineer, Agent Platform PM.

**Risks:**
- Autonomy tiers too rigid, blocking value → mitigate with pilot waivers and time-boxed exceptions
- Approval friction overwhelms users → mitigate with progressive automation only after KPI gains

**First-year outcomes:**
- Expand one agent workflow to a higher autonomy tier while keeping incident rate under threshold
- Reduce average human time per task by 15–25% in a targeted workflow

---

## Forward-Deployed Engineering

**Demand anchor:** Gartner notes CIOs shifting toward commercial off-the-shelf solutions, increasing demand for integration and "last mile" implementation. Accenture reported $3B GenAI new bookings in FY2024. Sharp growth in forward-deployed engineer postings as customers need customisation of complex AI tools.

---

### Strategy: Implementation Kit Productisation

**Description:** Go beyond "solve the customer problem once" and turn lessons into repeatable assets: templates, reference architectures, and automated checks. The moat: a compounding library — each deployment makes you faster and harder to replace.

**Proof employers accept:**
- A reusable "go-live kit": architecture template, security checklist, evaluation harness, runbooks
- A deployment acceleration metric (time-to-first-value reduced across projects)
- A customer-facing case study with production KPIs (cost, accuracy, incident rate)
- Open-source or internal tooling automating integration steps
- Post-implementation adoption playbook (training + workflow redesign)

**Build steps:**
1. Pick one vertical workflow (IT service desk, sales ops, contact centre) and deliver a reference build
2. Standardise evaluation and guardrails
3. Convert implementation steps into a kit with checklists and automation; iterate on the next deployment

**Buyers/titles:** AI vendors, consultancies, integrators, large enterprises. Titles: Forward-Deployed Engineer, Solutions Engineer (AI), Customer Success Engineer (GenAI), Implementation Consultant.

**Risks:**
- Assets become tool-specific → mitigate with vendor-agnostic control patterns
- Customers resist standardisation → mitigate by making kits configurable with risk tiers and governance hooks

**First-year outcomes:**
- Reduce "time to production" on similar deployments by 30–50%
- Improve first-90-days stability: 20–40% fewer high-severity incidents

---

### Strategy: Procurement-to-Production Bridge

**Description:** Treat procurement, contracting, and governance as part of delivery — anticipating that EU AI Act timelines and governance readiness gaps will block rollouts unless addressed early. The moat is deal acceleration.

**Proof employers accept:**
- A pre-built "procurement evidence pack" (security, evaluation, data handling, change management)
- Contract clause templates for model updates, logging, and incident response expectations
- A governance + evaluation checklist used to unblock at least one production approval
- AI literacy rollout plan aligned to EC guidance for the customer organisation
- A "vendor due diligence scorecard" reusable across accounts

**Build steps:**
1. Build a standard evidence pack aligned to EU AI Act timeline milestones and NIST guidance
2. Integrate evaluation tooling outputs into the pack
3. Run a joint workshop with legal/procurement + engineering on one deployment

**Buyers/titles:** AI vendors selling to enterprises; consultancies; internal enterprise AI enablement. Titles: Forward-Deployed Engineer, Solutions Architect, AI Delivery Lead, Technical Programme Manager (AI).

**Risks:**
- Becomes paperwork-heavy → mitigate by automating evidence capture
- Misalignment with local regulation interpretations → separate "required" vs "recommended" controls

**First-year outcomes:**
- Reduce procurement/security review cycle time by 20–35%
- Increase POC → production conversion rate by 10–20 points

---

### Strategy: Vertical Outcome Moat

**Description:** Anticipate that generic "LLM implementation" will commoditise. The durable moat is owning a vertical workflow and KPI plus repeatable delivery assets — becoming the default expert for a revenue-bearing outcome.

**Proof employers accept:**
- A vertical playbook with metrics, failure modes, and evaluation datasets tailored to that workflow
- Two case studies in the same vertical showing comparable KPI improvements and stable risk controls
- A reusable integration blueprint (systems, data sources, tool actions)
- A training package (AI literacy + operator SOPs) specific to that workflow
- A benchmark pack demonstrating why the chosen workflow is suited for agents

**Build steps:**
1. Choose one vertical workflow where agents are already appearing (service ops/IT, knowledge management)
2. Build a reference implementation on one major platform (Salesforce Agentforce or ServiceNow)
3. Standardise evaluation + cost + governance artefacts and reuse across a second project

**Buyers/titles:** Vertical SaaS vendors, consultancies, enterprise centres of excellence. Titles: Forward-Deployed Engineer (Vertical), AI Workflow Architect, Solutions Consultant.

**Risks:**
- Vertical selection fails → choose workflows with clear KPIs and data availability, prove pilots fast
- Platform dependency → document portable patterns and evaluation datasets

**First-year outcomes:**
- Deliver 1–2 repeatable deployments with measurable KPI gains (+10–20% containment or −15–25% cycle time)
- Improve delivery margin/time-to-value (20–30% fewer delivery hours on second deployment)
