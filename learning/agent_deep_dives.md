# Agent Architecture: Deep Dives
*Three areas to understand at interview depth*

---

## 1. Tool Design

### Why it matters
The model decides when and how to use a tool based entirely on the tool's description and the current context. Poor tool design produces unpredictable behaviour that looks like a model problem but is actually a design problem.

### The tool description is the interface
Every tool has a description the model reads at each decision step. It needs to answer four questions:
- **What does this tool do?** (specific, not vague)
- **When should I use it?** (the trigger condition)
- **When should I NOT use it?** (explicit exclusions prevent misuse)
- **What will I get back?** (so the model can reason about the output)

Bad description: `"search_web: Searches the web"`  
Good description: `"search_web: Retrieves current information from the web for factual questions, recent events, or data not likely to be in training data. Do not use for information already available in the provided context."`

### Granularity
- **Too coarse:** one tool that does many things → model can't predict output, prompt injection risk
- **Too fine:** dozens of narrow tools → model doesn't know which to combine, decision overhead
- **Right level:** one tool per discrete action type. If you find yourself writing `mode` or `type` parameters to switch a tool's behaviour, split it into two tools.

### Input schema design
Each field in the tool's input schema needs:
- A clear, unambiguous name (not `query`, but `search_query` or `customer_id`)
- A description explaining what the field means and any constraints
- Appropriate typing (string, int, enum) — enums are powerful because they constrain the model's choices

### Output design
What the tool returns shapes what the model can reason about next:
- Structured output (JSON) is better than free text — the model parses it more reliably
- Error returns must be informative: `{"error": "customer not found", "searched_id": "123"}` not just `{"error": true}`
- Don't return raw large objects — summarise or select the relevant fields before returning to the model

### Tool count
Model performance on tool selection degrades significantly above ~10-15 tools. Strategies for large toolsets:
- **Tool routing:** a meta-tool that selects a category, then a second call picks the specific tool
- **Tool filtering by context:** only present relevant tools based on current agent state
- **Subagents:** route to a specialised agent that has a smaller, focused toolset

### Side effects and idempotency
Any tool that writes, sends, or deletes something is a side-effect tool. Rules:
- Make side-effect tools idempotent where possible (calling twice has the same result as calling once)
- Name them explicitly: `send_email` not `email` — the verb signals to the model (and to you) that this has consequences
- Add confirmation steps before irreversible actions in high-stakes agents
- Log every side-effect tool call with inputs — you need this for debugging

### Further reading
- [Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents) — Anthropic engineering blog, the definitive reference on tool design principles
- [Building Effective AI Agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic research, covers the full agent design picture including tool philosophy
- [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) — OpenAI, production-focused with tool design and orchestration guidance

### Recommended course
[AI Agents: LLMs, Tool Calling, and Human-in-the-Loop](https://frontendmasters.com/courses/ai-agents-v2/) — Frontend Masters. Builds agents from scratch with a strong focus on tool calling mechanics, framework comparison (OpenAI Agents SDK, Mastra), and guardrail design. Practical over theoretical.

---

## 2. State and Memory Design

### The four types of memory in agents

**1. In-context (working memory)**  
What's in the current context window right now. Ephemeral — gone at the end of the run unless persisted. This is the agent's scratchpad: the task, the conversation so far, intermediate results, tool outputs. Limited by token budget — you must manage what stays and what gets dropped.

**2. Short-term external (episodic)**  
Memories from the current session, stored outside the context window and retrieved selectively. Typically: conversation history, intermediate results from earlier in a long task. Stored in a database or cache, retrieved by recency or relevance.

**3. Long-term external (semantic)**  
Persistent knowledge that survives across sessions. User preferences, accumulated facts, learned patterns. Usually stored in a vector database (for semantic retrieval) or a structured database (for exact lookup). Needs explicit write decisions — agents don't learn by default.

**4. Tool/system state**  
State held by external systems the agent interacts with — a database it writes to, a document it's editing. Not "owned" by the agent but affects its behaviour. Important to model explicitly: the agent needs to know what state the external system is in.

### State schema design (LangGraph / pipeline context)
In a node-based agent framework, each node reads from and writes to a shared state object. Design decisions:

- **What fields does the state object carry?** Be explicit — don't use a generic dict. Typed schemas catch bugs early.
- **What gets updated at each node?** Document which fields each node reads and writes. Nodes that write to fields other nodes depend on create coupling.
- **Accumulation vs. replacement:** Does a node add to a list (e.g. messages history) or replace a value (e.g. current_plan)? Different behaviour, different risks.
- **Visibility:** In multi-agent systems, which agents can see which parts of state? Subagents often need isolated state to avoid polluting the supervisor's context.

### Preventing context bloat
The longer an agent runs, the more the context fills up. Strategies:
- **Summarisation:** periodically compress conversation history into a summary, drop raw messages
- **Selective retrieval:** don't load all long-term memory upfront — retrieve only what's relevant to the current step
- **State pruning:** explicitly drop intermediate results from state once they're no longer needed
- **Structured extraction:** instead of passing raw tool output to the next step, extract only the relevant fields

### Checkpointing and persistence
Some frameworks (LangGraph) support checkpointing — saving the full agent state at each node so a run can be resumed after failure or interruption. When to use:
- Long-running agents where restarts are expensive
- Human-in-the-loop workflows where the agent pauses for approval
- Agents that interact with external systems with costs per call

### The key design question
For every piece of information in your agent: *What scope does it need to survive?*
- This step only → in-context, don't persist
- This run → short-term state, clear on completion
- Across runs → long-term memory, explicit write decision
- Across all users / global → careful — you're building a knowledge base, not just agent memory

### Further reading
- [The Architecture of Agent Memory: How LangGraph Really Works](https://dev.to/sreeni5018/the-architecture-of-agent-memory-how-langgraph-really-works-59ne) — DEV Community, detailed walkthrough of LangGraph's memory architecture with the four memory types explained concretely
- [LangChain Memory documentation](https://docs.langchain.com/oss/python/langgraph/memory) — official LangChain/LangGraph docs, authoritative reference for memory patterns and the checkpointing API
- [Long-Term Agentic Memory With LangGraph](https://medium.com/@anil.jain.baba/long-term-agentic-memory-with-langgraph-824050b09852) — Medium, practical implementation guide for persistent memory across sessions

### Recommended course
[Long-Term Agentic Memory with LangGraph](https://www.deeplearning.ai/short-courses/long-term-agentic-memory-with-langgraph/) — DeepLearning.AI (free). Taught by Harrison Chase (LangChain co-founder). Covers semantic, episodic, and procedural memory types; builds an email agent with routing, tools, and persistent memory. The most direct course for this topic.

---

## 3. Orchestration Pattern Selection

### The main patterns

**Single agent with tools (ReAct)**  
One LLM in a loop: reason → select tool → call tool → observe result → reason again. The most common pattern.  
*Use when:* bounded task, clear toolset, moderate complexity  
*Breaks down when:* task is too complex to plan end-to-end in one model, toolset is too large, loops become uncontrolled

**Sequential pipeline**  
Fixed sequence of steps, each a node/LLM call. No branching based on content — the flow is always the same.  
*Use when:* well-defined transformation tasks, the sequence is always known (e.g. extract → format → validate → output)  
*Breaks down when:* you need conditional logic, different inputs need different paths

**Conditional pipeline (router)**  
Sequential pipeline with routing nodes that inspect output and choose a branch. Still deterministic in structure, but the path varies by content.  
*Use when:* a small number of known cases that need different handling  
*Breaks down when:* the branching logic becomes too complex or the cases aren't known upfront

**Planner + executor**  
Two-stage: a planner LLM generates a step-by-step plan from the task, then an executor works through the plan. The plan is explicit and inspectable.  
*Use when:* complex multi-step tasks, you want human review of the plan before execution, the task benefits from upfront decomposition  
*Breaks down when:* the planner makes wrong assumptions early (errors propagate), tasks require real-time adaptation that the plan didn't anticipate

**Supervisor + subagents**  
A supervisor agent receives a task, decomposes it, and routes subtasks to specialised subagents. Subagents report back; supervisor synthesises.  
*Use when:* tasks span multiple domains that benefit from specialisation, tasks that are too long/complex for a single context window  
*Breaks down when:* coordination overhead exceeds the value of specialisation, subagents need to share state

**Parallel subagents**  
Multiple agents work on independent subtasks simultaneously, results combined.  
*Use when:* subtasks are genuinely independent (researching multiple sources, analysing multiple documents), latency matters  
*Breaks down when:* subtasks have dependencies, combining results is itself complex

**Reflection / critic loop**  
Agent generates output, a second LLM call critiques it, the agent revises. Can be a separate model or the same model with a different prompt.  
*Use when:* output quality is critical, the task benefits from a second perspective  
*Breaks down when:* reflection adds latency without improving quality (the critic doesn't have enough context to critique well)

### Decision framework
Ask these questions in order:

1. **Is the sequence fixed or content-dependent?**  
   Fixed → pipeline. Content-dependent → ReAct or planner.

2. **How complex is the task?**  
   Bounded, single domain → single agent. Multi-domain or too long for one context → multi-agent.

3. **Are the subtasks independent?**  
   Yes → parallel. No → sequential or supervisor.

4. **How important is output quality vs. latency?**  
   Quality critical → add reflection. Latency critical → avoid extra passes.

5. **Does the agent take irreversible actions?**  
   Yes → planner pattern (review before execution) or human-in-the-loop checkpoints.

6. **What's your error tolerance?**  
   Low → simpler, more predictable patterns. Higher → ReAct/planner can handle more complexity but are harder to debug.

### Pattern combinations
Real agents often combine patterns:
- A **supervisor** routes to **specialised sequential pipelines** for well-defined subtasks
- A **planner** creates a plan, then **parallel subagents** execute independent steps, then a **reflection** pass reviews the synthesis
- A **ReAct agent** with a **reflection loop** for quality-sensitive tool-use tasks

The key question when combining: where does state live, and how does it flow between patterns? This is where multi-agent systems get complicated.

### Further reading
- [AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) — Microsoft Azure Architecture Center, production-grade pattern catalogue with decision guidance for each
- [Choosing the right orchestration pattern for multi-agent systems](https://www.kore.ai/blog/choosing-the-right-orchestration-pattern-for-multi-agent-systems) — Kore.ai, practical comparison of supervisor, pipeline, and adaptive network patterns with real use cases
- [Supervisor Agent Architecture: Orchestrating Enterprise AI at Scale](https://www.databricks.com/blog/multi-agent-supervisor-architecture-orchestrating-enterprise-ai-scale) — Databricks, in-depth treatment of the supervisor/subagent pattern in production environments

### Recommended course
[Agentic AI](https://learn.deeplearning.ai/courses/agentic-ai/information) — DeepLearning.AI (Andrew Ng). Covers the four core design patterns (Reflection, Tool Use, Planning, Multi-Agent) with hands-on implementation. The most efficient single course for understanding orchestration patterns and when to apply them.

---

*Last updated: 2026-04-28*
