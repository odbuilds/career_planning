# Senior AI Engineer — Quadrivia

---

## Overview

| Field | Detail |
|---|---|
| Company | Quadrivia |
| Role | Senior AI Engineer |
| Salary | €150k |
| Location | Europe / Remote |
| Status | Recruiter Call |
| Interest level | 3 |
| Date of first contact | 2026-03-31 |
| Recruiter call | 2026-04-01 |

---

## Source

- **Channel:** LinkedIn — inbound message
- **Type:** Recruiter outreach (not direct application)
- **Recruiter:** Joshua Taylor, Executive Consultant — Software Engineering, Impala Search
- **Notes:** Josh reached out directly. Company not named in initial message.

---

## The Role

### What they are building
AI agents and AI systems for clinics and the NHS (UK). AI assistant designed by clinicians to automate routine workflows and improve patient care at scale. Enabling healthcare teams to manage large volumes of patient interactions while maintaining clinical quality, safety, and compliance.

### What the role involves
From recruiter call (2026-04-01):
- Improving voice latency
- Managing turn-taking and barge-in
- OCEL-first tracing
- Managing a RAG pipeline
- Context engineering
- EHR (Electronic Health Record) integration into LLM tools
- Multi-agent orchestration and shared memory

From original outreach:
- Designing and deploying agentic AI systems in production environments
- Building and iterating on LLM-driven workflows, prompts, and evaluation frameworks
- Integrating AI systems into real-world healthcare workflows and data pipelines
- Collaborating with product, clinical, and engineering teams to ensure reliability, safety, and compliance

### What they are looking for
- Strong experience in LLMs, Python, and production-grade AI systems
- Enjoys complex, high-stakes problems and shipping impactful products
- Multi-agent projects (impressive)
- Healthtech experience (impressive)
- Low latency video/voice AI streaming (impressive)

### Full message received

> Hi Oliver,
>
> I hope this message finds you well!
>
> I'm reaching out about an exciting AI Engineer opportunity with my client, a fast-growing healthtech company building an AI assistant designed by clinicians to automate routine workflows and improve patient care at scale.
>
> They're tackling a genuinely complex problem - enabling healthcare teams to manage large volumes of patient interactions while maintaining clinical quality, safety, and compliance - using conversational AI and intelligent automation.
>
> In this role, you'd be working on:
> Designing and deploying agentic AI systems in production environments;
> Building and iterating on LLM-driven workflows, prompts, and evaluation frameworks;
> Integrating AI systems into real-world healthcare workflows and data pipelines;
> Collaborating closely with product, clinical, and engineering teams to ensure reliability, safety, and performance
>
> It's a particularly interesting environment as it combines cutting-edge AI development with real-world impact, where systems need to be both technically robust and clinically safe.
>
> They're looking for someone with strong experience in LLMs, Python, and production-grade AI systems, who enjoys working on complex, high-stakes problems and shipping impactful products. Experience with multi-agent projects, health-tech or low latency video / voice AI streaming would also be really impressive.
>
> If this sounds like it could be relevant, I'd love to share more about the team, product, and vision - would you be open to a quick conversation later this week or early next?
>
> Best,
> Josh
>
> Joshua Taylor
> Executive Consultant | Software Engineering at Impala Search

---

## Fit Assessment

### Strengths against this role
- LLM-driven workflows and evaluation — LLM-as-judge pipeline for insurance firm, agentic trace evaluation research
- Conversational AI at scale — full arc from NLU through to agentic systems
- High-volume interaction management — analogous contact centre background
- Evaluation and quality frameworks — directly relevant to clinical safety requirements
- Multi-step LLM pipeline design — LangGraph, n8n, HumanFirst
- Enterprise client delivery — working with product and operational teams

### Gaps to address
- Python — functional but not strong; would need to address directly
- Production-grade AI systems — limited large-scale production track record
- Healthtech / EHR — no direct domain experience; FHIR, HL7, NHS data models are new territory
- Voice AI (latency, barge-in, turn-taking) — distinct engineering discipline; no hands-on experience
- OCEL tracing — specific standard not yet explored (existing observability knowledge transfers)
- NHS compliance — DSP Toolkit, DSPT, clinical data classification unfamiliar
- Multi-agent at scale — personal projects only, not enterprise production

### Honest assessment
Stretch role at €150k. Shared this honestly with recruiter on call — recruiter likely to put forward anyway. Context engineering and multi-agent architecture are genuine strengths. Voice AI is the biggest real gap. Worth pursuing but go in clear-eyed. See `skills_gap_tracker.md` for detailed prep priorities if interview confirmed.

---

## CV Sent

*Version: Healthtech-tailored (cv_healthtech.md)*
*Date sent: —*

---

### CV Text

# OLIVER DAY
oliver.p.day@gmail.com | +381 603388856 | linkedin.com/in/dayoliver
Belgrade, Serbia (open to remote)

## Profile

AI engineer with 10+ years building and evaluating conversational AI systems at enterprise scale. Background spans the full arc from high-volume customer interaction management through NLU model development to LLM-powered agentic workflows. Particular focus on evaluation frameworks, production reliability, and quality assurance for systems that need to perform consistently under real-world conditions — including safety-critical contexts where output quality has direct operational consequences. Work sits at the intersection of technical implementation and quality engineering: building systems that are measurable, observable, and improvable in production.

## Experience

### Conversational AI Developer — HumanFirst
*November 2023 – Present*

- Designed and deployed an LLM-as-judge evaluation pipeline for a global insurance firm — automated analysis of customer service conversations to monitor agent adherence to clinical-style guidelines at scale, flagging quality and compliance issues without manual review
- Built a multi-step prompt orchestration and evaluation framework for an international mortgage brokerage, integrating with BigQuery/Looker to surface performance insights and drive iterative quality improvement
- Designed and built a production agentic workflow using LangGraph and n8n — multi-stage LLM pipeline processing 15,000+ profiles with automated qualification, personalised content generation, and A/B testing across messaging variants; achieved 70% engagement rate
- Designed and built multiple conversational AI solutions across Dialogflow, Kore.AI, and Microsoft Copilot for enterprise clients, covering solution architecture, conversation design, NLU model development, and integration with existing data pipelines and operational workflows
- Led NLU model optimisation programmes for HumanFirst enterprise clients — systematic analysis of production conversation data to identify intent classification failures, coverage gaps, and training data weaknesses, driving iterative model improvement
- Researched and built tooling for agentic trace evaluation — manual annotation workflows combined with HumanFirst clustering and semantic search to identify similar failure patterns across large trace sets and estimate issue frequency
- Delivered enterprise AI training programmes enabling clinical and operational teams to adopt and evaluate AI tools effectively

### Conversation Engineer — Conversation Design Institute Services
*October 2021 – October 2023*

- Led NLU model improvement programmes for enterprise clients in financial services and pharmaceutical sectors — systematic conversation data analysis to identify failure patterns and drive measurable quality improvements
- Consulted on conversational AI strategy and platform implementation for enterprises managing high-volume, quality-critical interaction workflows
- Led R&D for CDI's LLM consulting offering — evaluating emerging capabilities and translating into structured implementation methodologies
- Designed and delivered workshops on NLU model evaluation, conversation flow design, and building conversational AI solutions on low-code platforms for enterprise teams

### Conversation Designer — Travtus
*July 2021 – April 2023*

- Designed conversational AI experiences and built NLU models for a property management platform, handling high-volume tenant and landlord interactions across complex multi-step workflows

## Projects

**Eval Tool** *(Personal/research)*
Research project exploring agentic trace evaluation. Built a browser-based annotation interface using Claude Code for manual review of OpenTelemetry agent traces. Used HumanFirst clustering and semantic search to surface similar spans for further annotation and estimate the frequency of identified failure patterns across the dataset. Stack: Python, HumanFirst, Claude Code.

**LinkedIn Outreach Automation** *(Production)*
End-to-end agentic pipeline: LLM-powered qualification across 15,000+ profiles, personalised content generation, A/B testing, database deduplication, and complex rate-limit handling. 70% connection rate, 40% response rate, 7% demo attendance. Stack: n8n, LangGraph, Claude, Supabase.

**LinkedIn Post Agent** *(Personal)*
Nine-node LangGraph pipeline with conditional routing, Pydantic output validation, LangSmith observability, and GEPA evaluation integration for automated prompt optimisation. Stack: LangGraph, HumanFirst, LangSmith, Python.

## Capabilities

- Agentic AI system design and deployment (LangGraph, n8n, multi-step LLM pipelines, GEPA)
- LLM evaluation — LLM-as-judge design, agentic trace analysis, NLU failure pattern identification, semantic clustering for issue frequency estimation
- Prompt engineering and pipeline design (HumanFirst, Claude, OpenAI)
- Conversational AI design and NLU model development (Dialogflow, Kore.AI, Microsoft Copilot)
- Production observability — LangSmith tracing, failure pattern detection, quality monitoring
- RAG solution design and retrieval evaluation
- Python (pipeline development, data processing, API integration)
- Enterprise AI training and clinical/operational team enablement

## Education

**Knox College**, Galesburg, Illinois
Bachelor of Arts — Political Science and Biology, 2005

**London School of Commerce**, Belgrade, Serbia
MBA with Distinction, 2013

---

## Status Log

| Date | Status | Notes |
|---|---|---|
| 2026-03-31 | CV Prepared | Inbound recruiter message received via LinkedIn. CV tailored and prepared. |
| 2026-04-01 | Recruiter Call | Call with Josh Taylor. Company confirmed as Quadrivia. Full role spec discussed. Shared honest assessment that role feels like a stretch. Recruiter likely to put name forward regardless. Waiting to hear if interview is confirmed. Josh travelling to Japan — director/colleague will keep in contact in the meantime. Next expected contact from Josh: midday 20 April. |

---

## Contacts

| Name | Role | Company | Notes |
|---|---|---|---|
| Joshua Taylor | Executive Consultant | Impala Search | Initial contact. Travelling to Japan after call — next contact likely midday 20 April. Director or colleague will keep in touch in the meantime. |

---

## Interview Notes

*Nothing yet.*

---

## Decision Notes

*Nothing yet.*
