Here is a list of things that I've built

- check whether the method used could be improved using the same tools and resources
- check what an optimal method would now be with the latest techniques and tools/platforms
- look for any additional information that could make this richer example
- list the skills it required and evidences 

research agent with lovable front end
built for a client who wanted a tool for account executives to keep track of clients and prospects in the news and draft outreach emails in the AE's tone of voice if news articles identify an opportunity
built as a proof of concept of using humanfirst with lovable - humanfirst as the point for writing, iterating and testing prompts while lovable handles the front end and manages the workflow
built to poc level with minimal evals 
used humanfirst api endpoints and specific prompt to connect them 
used openai with websearch to first find urls of relevant news articles, for each url do a separate websearch to summarise any relevant info and then a third prompt to create a final report, additional prompts to id outreach opportunities and draft outreach letter iterated over a list of companies and then output a summary report for each company and a relevant outreach email where opportunities were apparent
connection handled by supabase - main challenge was timeouts as there were several prompts chained 
Further improved with reflection loop - review the report look for gaps, generate new search queries and rewriting
chosen as a poc by client as they identified it as a value add rather than a cost saving
we did do some brief discussion of their needs and interests
check with lauren to add detail

internal linkedin outreach flow
following company restructure we removed the sales team and cut the team from 22 to 8
built an automated linkedin outreach process that was key to product development used for both finding sales opps and for prod dev interviews and demos
built in n8n and scraped linkedin for posts matching keywords related to strategic needs, those 500+ profiles were filtered by location and role and then used gen ai to filter based on post content to get super specific targets, then drafted outreach messages with gen ai with a/b testing over content 
achieved 70% connection rate, 40% response to messages, 20% signup for free access, 10% book a demo and 7% attend
the flow used an external tool to scrape linkedin and had limits so added complex handling to manage 
results were exported to a database and also checked against to ensure no repeat outreach
over 15k profiles reached out to 


Winnow (task prioritisation agent)
Personal project to explore LangGraph agent development. Core problem: too many tasks, side interests, and articles competing for attention — needed something that decides what's actually worth doing relative to current goals, not a form to fill in.

Tasks added as natural language. A 4-step LangGraph pipeline handles the rest: (1) structured data extraction from free-text input, (2) URL research — if a link is present, retrieves and summarises the content before prioritisation, (3) prioritisation against goals, deadlines, and dependencies, (4) decomposition of complex tasks into smaller steps. Low-priority reading items are batched into a weekly digest rather than cluttering the task list.

LangGraph requires defining the state schema and graph structure upfront — every input/output format, every handoff between steps — before writing any prompt logic. This forced a key design decision: prompts had to be designed and validated in HumanFirst first, so the data structures and handoffs were known before touching code. Each prompt was tested against multiple inputs in parallel, outputs from step one dropped into step two as test input, chain validated step by step. By the time implementation started, the hard design work was done — Claude Code built the state file and graph structure from already-tested prompts and known handoffs. UI and database work was all that remained.

Stack: LangGraph, Claude via HumanFirst, Claude Code for implementation.

Skills evidenced: LangGraph agent architecture (state schema design, graph definition, multi-step chaining), prompt-first development methodology, URL content retrieval and summarisation, goal-aware prioritisation logic, Claude Code for agentic code generation from validated design.


vid2doc
POC to convert screen-recording videos (product walkthroughs, demo recordings) into professional "how to" documentation automatically — timestamped screenshots included, output as styled HTML/PDF.

Pipeline: video upload → Whisper transcription with timestamps → LLM extracts key concepts → LLM drafts markdown doc with screenshot placeholders → LLM selects optimal frame timestamps (reasoning about stable UI states, avoiding motion blur) → Canvas-based browser frame extraction (chosen over FFmpeg due to Supabase function size limits) → LLM quality review scores 1-10, triggers one conditional regeneration pass if below threshold → human review in split-screen markdown editor → styled HTML/PDF output.

Grew from 5 to 7 prompts during development — consistency problems found during parallel testing in HumanFirst drove the additions. Key decision: all prompts designed and chain-tested in HumanFirst before building the Lovable app, using 5 real transcripts in parallel. This caught flow problems at prompt level rather than after the full app was built. Prompts live in HumanFirst rather than buried in Lovable code, so they can be iterated without touching the frontend.

Stack: Lovable (React/TypeScript), Supabase, OpenAI Whisper, Claude via HumanFirst, Canvas API for frame extraction, weasyprint for PDF.

Skills evidenced: multi-step LLM pipeline design, structured JSON prompt chaining, iterative prompt development with parallel input testing, human-in-the-loop workflow design, constraint-driven technical decisions (browser-native extraction over server-side processing), HumanFirst + Lovable integration.






LinkedIn post agent
Takes a rough idea or URL-with-take and produces a LinkedIn post in the user's voice. LangGraph pipeline: idea refinement → optional research → draft writing → tone adjustment → review → conditional rewrite (max 2x) → finalisation.

All LLM calls route through HumanFirst — the code handles routing and Pydantic validation only; model choice, temperature, system prompts, and variable injection are managed in HumanFirst. Prompts were built and tested in HumanFirst before any pipeline code was written: mention syntax failures, inconsistent JSON output from the idea refiner, and over-permissive review calibration were all caught at prompt level against 20 samples in minutes rather than in a running pipeline. Claude Code built the workspace, collections, intents, and all prompts via the HumanFirst MCP skill, then built the full LangGraph agent once prompts were validated. Iteration pattern: prompt changes made in HumanFirst UI, schema changes propagated back through code by Claude Code.

Traces go to LangSmith for per-node observability. GEPA (Generative Evaluation and Prompt Adjustment) integration is built and waiting on a labelled dataset. A dedicated judge optimiser (`gepa-llm-judge/`) is configured for LinkedIn post quality — binary good/bad classification with reasoning, using GPT-4o-mini for evaluation and GPT-4o for reflection. Once a labelled CSV exists, GEPA analyses failure cases, generates candidate prompt revisions, and evaluates them; the winning prompt gets promoted back into HumanFirst without touching pipeline code. A general-purpose GEPA classifier template (`gepa_classify.py`) and Jupyter notebook are also complete for other optimisation tasks.

Stack: LangGraph, HumanFirst (prompts, variable injection, model routing), LangSmith (tracing), Pydantic, Claude Code + HumanFirst MCP for build.

Skills evidenced: LangGraph pipeline design with conditional routing, prompt-first development methodology, HumanFirst MCP-driven workspace setup, Pydantic validation for LLM output schemas, LangSmith observability, separation of prompt logic from routing logic.

canam projects

call to transcript to custom format output for lean meetings