# Projects

## Personal & Internal Projects

### Research Agent with Lovable Frontend
Built for a client whose account executives needed to track clients and prospects in the news and draft outreach emails in the AE's tone of voice when news articles identified an opportunity.

Built as a proof of concept integrating HumanFirst with Lovable — HumanFirst as the environment for writing, iterating, and testing prompts; Lovable handling the frontend and workflow. Pipeline: OpenAI with web search first finds URLs of relevant news articles → per-URL search to summarise relevant info → third prompt creates a final report → additional prompts identify outreach opportunities and draft outreach emails → iterated over a list of companies, outputting a summary report and relevant outreach email per company where opportunities were apparent. Backend connection via Supabase; main engineering challenge was timeout handling across chained prompts. Further improved with a reflection loop — review the report, identify gaps, generate new search queries, and rewrite.

Stack: Lovable, Supabase, OpenAI (web search), HumanFirst.

Skills evidenced: multi-step LLM pipeline design, reflection loop architecture, prompt iteration in HumanFirst, Lovable + HumanFirst integration, timeout/async handling in chained workflows.

---

### Internal LinkedIn Outreach Automation
Following a company restructure that reduced the team from 22 to 8 and removed the sales function, built an automated LinkedIn outreach process used for both pipeline development and product interviews/demos.

Built in n8n: scraped LinkedIn for posts matching keywords related to strategic needs → 500+ profiles filtered by location and role → generative AI filtered by post content for high-specificity targeting → outreach messages drafted with gen AI with A/B testing over content. Results exported to a database with deduplication checks to prevent repeat outreach. Managed API rate limits and scrape quotas with complex handling logic. Reached over 15,000 profiles.

Results: 70% connection rate, 40% response rate, 20% free access signup, 10% demo booked, 7% demo attended.

Stack: n8n, LinkedIn scraping (external tool), generative AI (message drafting), database deduplication layer.

Skills evidenced: workflow automation, lead enrichment pipeline, A/B testing of AI-generated content, rate limit and quota management, conversion funnel instrumentation.

---



### vid2doc
POC to convert screen-recording videos (product walkthroughs, demo recordings) into professional "how to" documentation automatically — timestamped screenshots included, output as styled HTML/PDF.

Pipeline: video upload → Whisper transcription with timestamps → LLM extracts key concepts → LLM drafts markdown doc with screenshot placeholders → LLM selects optimal frame timestamps (reasoning about stable UI states, avoiding motion blur) → Canvas-based browser frame extraction (chosen over FFmpeg due to Supabase function size limits) → LLM quality review scores 1–10, triggers one conditional regeneration pass if below threshold → human review in split-screen markdown editor → styled HTML/PDF output.

Grew from 5 to 7 prompts during development — consistency problems found during parallel testing in HumanFirst drove the additions. All prompts designed and chain-tested in HumanFirst before building the Lovable app, using 5 real transcripts in parallel. This caught flow problems at prompt level rather than after the full app was built. Prompts live in HumanFirst rather than buried in Lovable code, so they can be iterated without touching the frontend.

Stack: Lovable (React/TypeScript), Supabase, OpenAI Whisper, Claude via HumanFirst, Canvas API for frame extraction, weasyprint for PDF.

Skills evidenced: multi-step LLM pipeline design, structured JSON prompt chaining, iterative prompt development with parallel input testing, human-in-the-loop workflow design, constraint-driven technical decisions (browser-native extraction over server-side processing), HumanFirst + Lovable integration.

---





---

## Client Work

### AI Training and Enablement Program — Canadian Engineering Firm
*HumanFirst*

Designed and delivered a comprehensive generative AI training program transforming 40 non-technical business users into proficient AI practitioners over 2 months. Over 60% of participants implemented unique AI use cases and maintained weekly usage patterns. Mentored individuals through the full project lifecycle from use case discovery to implementation, resulting in diverse applications including: marketing content repurposing, automated vendor documentation analysis, internal training material generation, Jira ticket trend analysis, code assistance for non-developers, and automated audio transcription with templated data extraction.

---

### Dialogflow Platform Migration and Optimisation — Enterprise Voice AI
*HumanFirst*

Led the migration of a high-volume voice bot (100,000+ monthly contacts) from Dialogflow ES to CX over 6 months. Reduced intents from 950 to under 200 through analysis of 2 million customer utterances using HumanFirst clustering and universal sentence embedding. Increased F1 score from below 50% to 96%, expanding model coverage to over 65% of intents at 70% confidence. Transformed architecture to entity-based recognition, enabling future generative AI features.

---

### FAQ Generation and Knowledge Base Development — European CPaaS Provider
*HumanFirst*

Processed 50,000+ customer conversations using generative AI to create a comprehensive, action-oriented FAQ database. Engineered a structured knowledge base pairing problem descriptions with step-by-step resolution guides, optimised for RAG implementation.

---

### Marketing Intelligence Analysis — European CPaaS Provider
*HumanFirst*

Led sentiment analysis by scraping and analysing product reviews using GPT-4/GPT-4-mini to extract feature-specific satisfaction levels. Constructed a hierarchical taxonomy of customer feedback themes to inform data-driven product and marketing strategy decisions.

---

### Microsoft Copilot Chatbot POC — Leading Canadian Parcel Delivery Service
*HumanFirst*

Led POC exploring Microsoft Copilot integrated with Azure CLU, analysing 10,000 customer service conversations to identify intents and auto-generate conversation flow designs. Conducted evaluation revealing RAG hallucination risks and demonstrated CLU advantages over Copilot's native NLU. Delivered findings within 4 weeks.

---

### Prompt Engineering for Insurance Industry Analytics
*HumanFirst*

Designed prompts for analysing customer-broker conversations using Speechmatics, Anthropic, and HumanFirst. Built evaluation framework comparing AI classifications against human baselines. Contributed to analysis of 50,000+ conversations for reporting via BigQuery and Looker.

---

### Prompt Engineering for Mortgage Broker Quality Assurance
*HumanFirst*

Designed prompts for AI-powered analysis of sales follow-up calls, enabling automated assessment of process adherence across 20 agents. Built evaluation framework for objective measurement of agent compliance with sales protocols.

---

### RAG System Evaluation — Canadian Telecommunications Company
*HumanFirst*

Evaluated RAG solutions (LangChain, Dialogflow CX, Stack AI, OpenAI GPTs) for contact centre agent support. Developed evaluation framework measuring accuracy, hallucination rates, implementation complexity, and cost. Delivered strategic recommendations and implementation roadmap.

---

### Sales Objection Analysis — Latin American Call Centre
*HumanFirst*

Analysed 20,000+ conversations to identify and classify sales objections using generative AI. Delivered classification model and prompt engineering methodology within one week.

---

### Strategic Competitor Analysis — Online Marketplace
*HumanFirst*

Analysed 20,000+ customer reviews across 4 competitors over 12 months using GPT-4-mini. Constructed hierarchical taxonomy; developed interactive Plotly visualisations to identify strategic opportunities.

---

### Low-Code AI Integration and Automation
*HumanFirst*

Leveraged Zapier, Make.com, Power Platform, and n8n to build AI-powered business process automations. Delivered: content repurposing pipeline (video → blog/social), intelligent email triage, and automated action item extraction from meeting transcripts.
