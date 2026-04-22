# OLIVER DAY
oliver.p.day@gmail.com | +381 603388856 | linkedin.com/in/dayoliver

---

## Profile

AI engineer focused on evaluation infrastructure, production reliability, and quality systems for LLM-powered applications. Work sits at the point where systems are deployed but not yet observable or systematically improvable — building the frameworks, tooling, and processes that make AI behaviour measurable at scale. Background spans LLM-as-judge pipeline design, agentic trace analysis, NLU failure pattern identification, and prompt optimisation infrastructure. Particular interest in the intersection of evaluation methodology and production feedback loops: not just detecting failures, but building systems that improve from them.

---

## Experience

### Conversational AI Developer — HumanFirst
*November 2023 – Present*

- Designed and deployed an LLM-as-judge evaluation pipeline for a global insurance firm — automated analysis of production customer service conversations to monitor agent adherence to guidelines at scale, with structured output validation and quality flagging replacing manual review
- Built a prompt orchestration and evaluation framework for an international mortgage brokerage — multi-prompt pipeline integrated with BigQuery/Looker to surface performance metrics and drive iterative quality improvement across deployed models
- Researched and built tooling for agentic trace evaluation — LLM prompts extract semantic dimensions (Action, Reasoning, Plan, Tool Call, Decision Point) from OpenTelemetry spans; HumanFirst clustering and PQL queries surface similar failure patterns across large trace sets and estimate issue frequency at scale
- Designed and built a production agentic pipeline using LangGraph and n8n — multi-stage LLM workflow with automated qualification logic, quality gates, A/B testing framework, and deduplication; 70% engagement rate across 15,000+ processed profiles
- Led the migration of a high-volume voice bot (100,000+ monthly contacts) from Dialogflow ES to CX — rebuilt NLU architecture using HumanFirst clustering on 2 million customer utterances, reducing intents from 950 to under 200 and improving F1 from below 50% to 96%; the migration also required designing a structured evaluation framework to validate model performance at each stage
- Evaluated RAG solutions for a Canadian telecommunications company — benchmarked LangChain, Dialogflow CX, Stack AI, and OpenAI GPTs against output accuracy, hallucination rate, implementation complexity, and operational cost; delivered platform-specific implementation guides and a strategic recommendation
- Led NLU model improvement programmes for enterprise clients — systematic analysis of production conversation data to identify intent classification failures, coverage gaps, and training data weaknesses driving measurable quality improvements
- Prototype and evaluate agentic AI workflows using LangGraph and HumanFirst — applying a prompt-first development methodology that validates pipeline logic and output schemas before implementation

### Conversation Engineer — Conversation Design Institute Services
*October 2021 – October 2023*

- Led NLU model improvement programmes for enterprise clients in financial services and pharmaceutical sectors — systematic conversation data analysis identifying failure patterns and driving measurable quality improvements
- Led R&D for CDI's LLM consulting offering — evaluating emerging evaluation and quality assurance methodologies and translating into structured implementation frameworks for enterprise clients
- Designed and delivered evaluation-focused training for enterprise teams on NLU model assessment, LLM output quality, and systematic model improvement processes

### Conversation Designer — Travtus
*July 2021 – April 2023*

- Designed conversational AI experiences and built NLU models for a property management platform, with ongoing quality monitoring and iterative improvement across high-volume interaction workflows

---

## Projects

**RAG and Conversational AI Platform Evaluation** *(Client Project — Canadian Telecommunications Company)*
Systematic comparative evaluation of RAG solutions and conversational AI platforms for large-scale contact centre agent support. Benchmarked LangChain, Dialogflow CX, Stack AI, and OpenAI GPTs against output accuracy, hallucination rate, implementation complexity, and operational cost. Additionally evaluated Microsoft Copilot + Azure CLU against native Copilot NLU — CLU demonstrated measurable accuracy advantages for intent handling, while RAG limitations and hallucination risks were documented with mitigation strategies. Delivered platform-specific best practice guides, a strategic recommendation, and an implementation roadmap enabling stakeholders to make an informed deployment decision. Stack: Dialogflow CX, Microsoft Copilot Studio, Azure CLU, LangChain, Stack AI, OpenAI GPTs.

**LinkedIn Post Agent** *(Personal)*
Nine-node LangGraph pipeline with GEPA (Generative Evaluation and Prompt Adjustment) integration — binary good/bad quality judge using GPT-4o-mini for evaluation and GPT-4o for reflection. Once a labelled dataset is available, GEPA analyses failure cases, generates candidate prompt revisions, and evaluates them; winning prompt promoted back to HumanFirst without touching pipeline code. LangSmith per-node observability throughout. Stack: LangGraph, HumanFirst, LangSmith, Python.

**LinkedIn Outreach Automation** *(Production)*
Production pipeline with LLM-powered qualification, A/B testing across messaging variants, and deduplication against an existing database — quality gates preventing repeat outreach and ensuring targeting precision. 70% connection rate, 40% response rate across 15,000+ profiles. Stack: n8n, LangGraph, Claude, Supabase.

---

## Capabilities

- LLM evaluation design — LLM-as-judge pipeline architecture, output schema validation, quality gate design
- Agentic trace analysis — OpenTelemetry span tree parsing, semantic dimension extraction, failure pattern clustering
- Production observability — LangSmith tracing, HumanFirst PQL queries, performance metric surfacing
- Prompt optimisation infrastructure — GEPA integration, automated prompt revision evaluation, HumanFirst prompt management
- NLU quality systems — intent classification failure analysis, coverage gap identification, training data improvement
- Python — evaluation pipeline development, data processing, annotation tooling
- LangGraph — pipeline design with conditional routing, Pydantic output validation

---

## Education

**Knox College**, Galesburg, Illinois
Bachelor of Arts — Political Science and Biology, 2005

**London School of Commerce**, Belgrade, Serbia
MBA with Distinction, 2013
