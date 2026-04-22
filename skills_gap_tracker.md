# Skills Gap Tracker
*Running record of skills asked for across all applications, vs Oliver's current level*

---

## How to read this

Each application adds its required skills to the table below. Skills asked for multiple times are consolidated — frequency is tracked. Gap rating is honest self-assessment: **Low / Moderate / High**.

---

## Skills Demand vs Current Level

| Skill | Times Asked | Oliver's Level | Gap | Notes |
|---|---|---|---|---|
| **RAG pipeline (design + management)** | 1 | Intermediate — has built pipelines, understands chunking and retrieval | Moderate | Lacks domain-specific context (e.g., healthcare data formats, EHR) |
| **Multi-agent orchestration** | 1 | Intermediate — LangGraph state schema, multi-node pipelines | Moderate | Architecture knowledge present; no production-at-scale evidence yet |
| **Context engineering** | 1 | Strong — active area of study and practice | Low | Real strength; lead with this |
| **Agent observability / tracing** | 1 | Intermediate — LangSmith, eval tooling, trace analysis | Moderate | OCEL is a specific standard not yet explored |
| **OCEL-first tracing** | 1 | None | High | Object-Centric Event Log — specific to agent workflow tracing; learnable |
| **EHR integration into LLM tools** | 1 | None | High | FHIR, HL7, NHS data models — domain-specific; new territory |
| **Voice latency engineering** | 1 | None | High | STT/TTS pipeline optimisation, streaming; distinct engineering discipline |
| **Turn-taking and barge-in (voice)** | 1 | Conceptual only (conversational AI background) | High | Implementation-level voice UX engineering; hands-on experience lacking |
| **Health/NHS compliance** | 1 | Aware of GDPR; no NHS-specific experience | High | DSP Toolkit, DSPT, clinical data classification |

---

## Application Log

### 1. Quadrivia — Senior AI Engineer
*Health tech — agents/AI systems for clinics and NHS UK*
*Recruiter call: 2026-04-01*
*Source: LinkedIn inbound recruiter*

**Skills required by this role:**
- Voice latency improvement
- Turn-taking and barge-in management
- OCEL-first tracing
- RAG pipeline management
- Context engineering
- EHR integration into LLM tools
- Multi-agent orchestration and shared memory

**Self-assessment:** Role is stretching beyond current comfort zone — honest position shared with recruiter. Interview not yet confirmed; recruiter likely to put forward anyway.

**If interview confirmed — prep priorities:**
1. OCEL tracing — read spec, find practical agent tracing examples
2. FHIR basics and EHR API patterns
3. NHS data governance fundamentals (DSP Toolkit, IG requirements)
4. Voice pipeline architecture: STT → LLM → TTS, latency sources at each stage
5. Barge-in detection techniques (VAD, energy-based, model-based)
6. Voice agent frameworks to understand (LiveKit, Pipecat, Vapi)

**Positioning note:** Lead with context engineering and multi-agent as genuine strengths. Be honest about voice being new — frame it as "I understand the conversational design layer; the real-time audio engineering is where I'd need to build quickly." The NLU/conversational AI and evaluation background is directly relevant to clinical dialogue quality.

---

## Recurring Gaps (asked for 2+ times)

*None yet — will populate as more applications are added.*

---

## Skills to Build Proactively

Skills that have appeared even once but represent genuine gaps worth closing regardless of which role lands:

| Skill | Why Worth Closing | How to Start |
|---|---|---|
| **OCEL tracing** | Emerging standard for agent observability; will appear in more roles | Read OCEL spec; find open-source examples |
| **Voice pipeline basics** | Voice AI is growing fast in CX and health tech | Study LiveKit / Pipecat architecture; understand VAD and latency sources |
| **EHR/FHIR basics** | Health tech is a strong vertical for Oliver's background | FHIR quick start; NHS API docs |
| **NHS compliance fundamentals** | Credibility for any UK health-tech role | DSP Toolkit overview; IG training modules |
