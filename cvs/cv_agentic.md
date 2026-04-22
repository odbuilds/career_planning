# OLIVER DAY
oliver.p.day@gmail.com | +381 603388856 | linkedin.com/in/dayoliver

---

## Profile

AI engineer with 10+ years building conversational AI and LLM systems at enterprise scale. Background spans the full arc from managing high-volume contact centre operations through NLU model development to designing and deploying production agentic pipelines. Particular focus on the engineering challenges that appear after the proof of concept — state management across multi-step chains, reliable output validation, quality gates that hold under real-world conditions, and observability that makes failures diagnosable. Work sits at the intersection of pipeline architecture and production reliability: building systems that process real data at scale, behave predictably, and improve over time.

---

## Experience

### Conversational AI Developer — HumanFirst
*November 2023 – Present*

- Designed and built a production agentic workflow using LangGraph and n8n — multi-stage pipeline processing 15,000+ profiles with automated qualification logic, personalised content generation at scale, A/B testing across messaging variants, and rate-limit and deduplication handling; achieved 70% engagement rate and 20+ weekly qualified outcomes
- Designed and deployed an AI analytics and evaluation framework for a global insurance firm — automated pipeline analysing 50,000+ customer-broker conversations to classify and report escalation and contact reasons at scale; built the prompt design, output validation, and human-baseline evaluation process from scratch, with results surfaced through BigQuery and Looker dashboards
- Built a prompt orchestration and evaluation framework for an international mortgage brokerage — multi-prompt pipeline integrated with BigQuery/Looker for performance monitoring and iterative quality improvement across 20 agents
- Led the migration of a high-volume voice bot (100,000+ monthly contacts) from Dialogflow ES to CX — rebuilt the NLU architecture using HumanFirst clustering on 2 million customer utterances, reducing intents from 950 to under 200 and improving F1 score from below 50% to 96%
- Designed and deployed conversational AI solutions across Dialogflow, Kore.AI, and Microsoft Copilot for enterprise clients, covering solution architecture, NLU model development, and integration with operational data pipelines

### Conversation Engineer — Conversation Design Institute Services
*October 2021 – October 2023*

- Led R&D for CDI's LLM consulting offering — evaluating emerging LLM capabilities, building proof-of-concept pipelines, and translating findings into structured implementation methodologies for enterprise clients
- Led NLU model improvement programmes for enterprise clients in financial services and pharmaceutical sectors — systematic pipeline analysis to identify failure patterns and drive measurable quality improvements
- Designed and delivered training programmes on LLM pipelines, prompt engineering, and conversational AI implementation for enterprise engineering and operational teams

### Conversation Designer — Travtus
*July 2021 – April 2023*

- Built NLU models and conversational AI workflows for a property management platform, handling high-volume multi-step interactions across tenant and landlord workflows

---

## Projects

**LinkedIn Post Agent** *(Personal)*
Six-node LangGraph pipeline: Idea refinement → optional research → draft → review → conditional rewrite (max 2x) → finalisation. All LLM calls route through HumanFirst — code handles routing and Pydantic validation only; prompts, model selection, and variable injection managed externally. LangSmith tracing per node. GEPA integration built for automated prompt optimisation once labelled dataset is available. Stack: LangGraph, HumanFirst, LangSmith, Python.

**Research Agent with Lovable Frontend** *(Client POC)*
Multi-step agentic pipeline for account executive intelligence — monitors company and prospect news, identifies outreach opportunities, and drafts personalised emails in the AE's tone of voice. Pipeline: web search → per-URL retrieval and summarisation → opportunity identification → personalised email drafting, iterated over a client list with a structured report and outreach email per company. Improved with a reflection loop: reviews the initial report, identifies gaps, generates new search queries, and rewrites. Main engineering challenge: chained prompts routed through Supabase required careful timeout and error handling. Chosen by the client as a revenue-generating value-add rather than a cost saving. Stack: HumanFirst, Lovable, OpenAI (web search), Supabase.

**LinkedIn Outreach Automation** *(Production)*
End-to-end pipeline: LLM-powered profile qualification across 15,000+ records, personalised message generation, A/B testing framework, database deduplication, rate-limit handling. 70% connection rate, 40% response rate, 7% demo attendance. Stack: n8n, LangGraph, Claude, Supabase.

---

## Capabilities

- Agentic system architecture — LangGraph state schema design, multi-step graph definition, conditional routing, Pydantic output validation
- Multi-agent pipeline development — n8n, LangGraph, prompt orchestration, data contract design
- Production observability — LangSmith per-node tracing, failure pattern detection, GEPA prompt optimisation integration
- LLM evaluation design — LLM-as-judge, quality gates, human-baseline validation
- NLU model development and optimisation — intent architecture, clustering-based model simplification, F1 improvement
- Python — pipeline development, API integration, data processing
- RAG solution design and retrieval evaluation

---

## Education

**Knox College**, Galesburg, Illinois
Bachelor of Arts — Political Science and Biology, 2005

**London School of Commerce**, Belgrade, Serbia
MBA with Distinction, 2013
