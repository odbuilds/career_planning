# The Economist — Round 2 Interview Prep
**Role:** Senior AI Engineer, AI Lab
**Stage:** Round 2 — Tech Lead interview
**Date:** 6 May 2026

---

## Why You Can Get This Job

This is not a pep talk. These are specific, logical reasons — grounded in what the role actually requires and what you've actually done.

---

**1. Your eval experience is exactly what they need most — and it's rare.**

The Economist's hardest engineering problem isn't building a RAG pipeline. It's measuring whether what the pipeline produces is any good. That's an eval problem, and eval is where most AI engineers are weakest. You've built production eval frameworks from scratch at a scale most candidates haven't touched — 50,000+ conversations, human baseline methodology, inter-annotator agreement, LLM-as-judge calibrated against expert reviewers. You didn't read about this approach; you built it for a paying client in a regulated industry. That specific experience is not common. It's the rarest thing on your CV and it happens to be the rarest thing the role needs.

**2. You've already solved the exact editorial quality problem — in a different domain.**

The Economist's challenge is: how do you evaluate quality when the ground truth is implicit, held in experienced humans' heads, and can't be written into a rubric? You solved this for insurance analysts. You didn't ask them to articulate the rules — you treated their agreement as the ground truth, built a baseline dataset from their judgments, and designed the eval framework around the cases where they agreed. The mechanism transfers directly to editors. The fact that you've done it in a different domain is a strength, not a weakness — it means you have a proven method rather than a theory.

**3. The lab is three engineers building from scratch. That's the environment where you work best.**

This isn't a role inside a large engineering org following established patterns. It's an exploratory lab with a small team and an open mandate. You've built meaningful systems as a solo or near-solo builder — the outreach pipeline, the LinkedIn post agent, the insurance evaluation framework. You know how to take a vague goal, define what success looks like, build the infrastructure, and ship something that holds up. That's harder to find than someone who can implement well inside an existing system.

**4. The "working with non-technical domain experts" requirement is genuinely unusual — and you have direct evidence.**

Most AI engineers have never had to translate between domain expertise and technical design. You ran an enablement programme for 40 non-technical staff at an engineering firm and have spent two years working with contact centre operations teams, insurance analysts, and mortgage brokers — people with strong domain instincts and zero patience for jargon. Journalists and editors are the same dynamic at a higher level of intellectual sophistication. The skill of starting from their output, not your tooling, and building their judgment into the eval framework — that's documented in your work history, not just claimed.

**5. You passed round 1 for a reason.**

The tech lead already met you and moved you forward. They're not running round 2 to be polite — they're running it because round 1 gave them a reason to. The question in front of you is not whether you belong in the room. You've already answered that. Round 2 is about depth.

**6. Your gaps are real but they're not disqualifying — and the honest framing of them is itself a signal.**

Fine-tuning is the clearest gap. But the lab described itself as exploratory, and you asked in round 1 where fine-tuning sits in priority. If the answer was "it's the immediate focus," you'd know. The role is three engineers across senior AI, AI lead, and AI infra — fine-tuning may well sit primarily with one of the other hires. Your gaps are the same gaps you'd have at any lab hiring for this profile: deep eval and pipeline strength, growing into weight-level training. That's a known, manageable gap in a strong profile. A candidate who can't speak to evals at all but has fine-tuned some models is a weaker fit for this specific lab than you are.

**7. The Economist hired internally to build a lab, not to deploy a product.**

They're not looking for someone to implement a spec. They're looking for someone who can figure out what to build, build it carefully, and work with editors to validate it. The exploratory framing of the role — three people, internal startup, still mapping the territory — is exactly where your combination of eval methodology, pipeline architecture, and domain expert collaboration is most valuable. In a mature engineering org with defined requirements, the Python fluency gap matters more. In a lab that's still asking the questions, judgment and methodology matter more.

---

The case for you getting this job is not "you're good enough despite your gaps." It's that your specific combination of skills — production eval frameworks, pipeline architecture with real failure mode knowledge, and documented ability to work with non-technical domain experts — maps directly onto the hardest parts of this role. Most candidates will be stronger on the pure engineering axis. Very few will be stronger on the axis that matters most here.

---

## Context for This Round

Round 1 was a screening. Round 2 is with the tech lead — expect a materially more technical conversation. The shift in tone: round 1 rewarded narrative and self-awareness; round 2 rewards technical judgment, specificity about options and tradeoffs, and demonstrated depth on evals and RAG. Lead more with position and less with background. Say what you think first, then back it up.

The full process ahead:
1. **Tech lead interview** ← you are here
2. Take-home test
3. Head of Data Engineering interview
4. VP of AI interview

This round sets your credibility. If you leave this interview and the tech lead doesn't believe you know evals and RAG in depth, the take-home test won't rescue you.

---

## Key Themes to Emphasise in Round 2

- **Technical judgment over experience narrative.** The tech lead wants to know how you think about hard problems, not just what you've done. Lead with your position, then your evidence.
- **Eval depth.** This is the core differentiator. Go deeper than you did in round 1. Know the failure modes of LLM judges, the difference between pointwise and pairwise, what to do when there's no ground truth.
- **RAG architecture tradeoffs.** Don't just describe RAG — show you can reason about which approach to use and why, with specific pros and cons.
- **Honest about Python.** The tech lead may probe code fluency. The framing from round 1 still stands — but in a technical interview, the emphasis shifts to "I understand the design and can catch failures" rather than "I delegate the typing."

---

## Section 1 — Questions to Ask the Tech Lead

These are calibrated for a tech lead conversation — genuinely technical, signal depth, and reveal how the lab actually operates.

**[Technical — architecture]**
1. "What does the current AI infrastructure look like — are you building on top of commercial LLM APIs, fine-tuned models, or a mix? And how much of that is in flux?"

   *Why:* Shows you understand infrastructure choices aren't neutral and signals you'd engage with them seriously.

2. "How are you handling prompt and model versioning? Is there a system for tracking which prompt was in production at a given time, or is that still evolving?"

   *Why:* Most labs at this stage haven't solved this properly. Asking it signals you know it matters.

3. "What does your current eval setup look like — is there a continuous eval loop in place, or is it still more ad hoc review?"

   *Why:* Reveals whether there's infrastructure to inherit or a blank slate to build, and positions eval as your territory.

4. "For RAG specifically — are you building on top of an existing vector store or have you evaluated options? What drove the choice?"

   *Why:* Gets into real decisions, not hypotheticals.

5. "How do you currently handle the ground truth problem for editorial content — how do you know when a RAG result or generated output is actually good?"

   *Why:* This is the hardest problem in the lab. Asking it first shows you've thought past the easy version.

**[Technical — failure modes and production]**
6. "What's broken in production that you most want to fix in the next six months?"

   *Why:* Nothing signals seriousness about reliability like asking about what's currently failing.

7. "How do you handle model output variation — if a prompt that worked last week starts behaving differently, what's your detection and response mechanism?"

   *Why:* Probes whether they have observability in place or are flying blind.

**[Ways of working]**
8. "How do editorial requests get prioritised against engineering work? Is there a product manager in the loop, or does the tech lead handle that interface?"

   *Why:* Understanding the editorial-engineering interface is critical; the answer affects everything about how you'd operate.

9. "What does the relationship with editorial look like in practice — is there a set of journalists or editors you work with regularly, or is it more project-based?"

   *Why:* Surfaces whether this is embedded collaboration or arm's-length delivery.

10. "What would the take-home test involve — are you able to share the format or scope?"

    *Why:* Legitimate and practical question. A good tech lead will respect that you're thinking about the process.

**[Broader technical direction]**
11. "Where do you think fine-tuning fits in the roadmap — is it a near-term priority or something you're waiting to have better eval infrastructure before you attempt?"

    *Why:* Your fine-tuning gap is real. Asking this positions the gap as a sequencing question rather than a skills deficiency.

12. "How do you think about the build vs buy decision for things like the vector store, re-ranking, and orchestration? Is there a principle that guides it, or is it case by case?"

    *Why:* Forces a real opinion and shows you know the landscape of tools well enough to ask the right question.

---

## Section 2 — Expected Technical Questions

### EVALS

---

**Q1: "How do you build an eval framework from scratch?"**

*What they're really asking:* Do you start with metrics or with the problem? Do you have a systematic approach or do you improvise?

*Format:* PCR

*Answer:*

"I start from the same place every time: what would an expert disagree about? That's where the eval needs to live — not the easy cases that any prompt gets right, but the edge cases and judgment calls where even good practitioners don't always agree. If you can't define that disagreement surface, you can't build a meaningful eval.

In practice the sequence is: build a human baseline first. For the insurance evaluation work I ran, that meant having experienced reviewers classify 500 conversations manually, then measuring where they disagreed with each other. Inter-annotator agreement on that set became my benchmark — if an LLM judge can match human-human agreement rates, it's doing as well as you could ask. If it can't, you have a calibration problem before you have an automation problem.

From there, eval design splits into a few choices. For automated eval at scale, I build LLM-as-judge pipelines — a prompt that takes a model output and a rubric and returns a score with reasoning. For editorial content specifically, I'd decompose that into multiple criteria evaluated separately: factual accuracy, voice consistency, structural integrity, and relevance to the query are four different things, and collapsing them into a single score loses signal. Pointwise scoring — assess each output independently against a rubric — is lower cost and faster to set up. Pairwise comparison — show the judge two outputs and ask which is better — is more expensive but more sensitive to fine-grained differences. For iterative prompt improvement, I use pairwise. For ongoing monitoring at scale, pointwise.

The other thing I'd say: eval is never finished. The dataset needs to expand as the pipeline encounters new failure modes in production. I treat the first 30–50 real-world outputs from any new pipeline as a second evaluation phase, not as production, specifically so I can add the failures I didn't anticipate into the test set."

**Tradeoffs to know if they probe:**

| Approach | Pros | Cons | Best for |
|---|---|---|---|
| LLM-as-judge (pointwise) | Fast, cheap, scalable | Position bias, verbosity bias, calibration drift | Monitoring at scale |
| LLM-as-judge (pairwise) | More sensitive to quality differences | 2× cost, harder to aggregate | Prompt iteration, A/B testing |
| Human review | Ground truth, catches subtle failures | Slow, expensive, doesn't scale | Building the baseline dataset |
| Reference-based (BLEU/ROUGE) | Cheap, deterministic | Only catches surface similarity, misses tone/quality | Sanity checking, not quality measurement |
| Embedding similarity | Captures semantic proximity | Doesn't catch factual errors or voice | Retrieval relevance checks |

---

**Q2: "What makes a good LLM judge prompt?"**

*What they're really asking:* Have you actually built one and discovered its failure modes, or are you describing the concept?

*Format:* PCR

*Answer:*

"The most important thing is criteria decomposition. A prompt that asks 'is this output good?' will produce unreliable scores because 'good' means different things and the model will weight them differently each time. A prompt that asks 'does this output accurately reflect the source material — yes or no, with reasoning' will produce consistent, auditable scores. You separate factual accuracy, tone, structure, and relevance into distinct evaluation passes. Aggregate later.

The second thing is chain-of-thought before verdict. A judge prompt that asks for a score directly produces scores that are hard to audit. A judge prompt that says 'first, list specific evidence for and against the following criteria, then give a score' produces reasoning you can read, which lets you catch when the judge is scoring for the wrong reason — verbose outputs rated higher because they seem more complete, for instance. That's position bias, or verbosity bias — both well-documented failure modes.

The third thing is calibration against your human baseline. The judge prompt isn't done until you've run it against your labelled dataset and measured agreement with human reviewers. Agreement rate is the KPI, not whether the prompt sounds right. I've thrown away judge prompts that I thought were well-constructed because they showed 65% human agreement on my test set — that's coin-flip territory on the cases that matter.

For editorial content specifically, you have an additional challenge: the judge prompt needs to capture voice in a way that the model can evaluate consistently. That means giving it exemplars — three passages that sound like The Economist and three that don't — rather than describing voice in the abstract. Concretely, the rubric should show, not tell."

**Key failure modes to know:**
- **Verbosity bias:** LLM judges tend to prefer longer, more detailed outputs even when they're worse
- **Position bias:** In pairwise evaluation, models prefer whichever output appears first ~55–60% of the time — fix by scoring both orderings and averaging
- **Self-preference:** Some models slightly prefer outputs that resemble their own generation style
- **Calibration drift:** Judge behaviour can shift across model versions even with an identical prompt — revalidate against your baseline after any model upgrade

---

**Q3: "How do you handle eval when there's no ground truth?"**

*What they're really asking:* This is the specific problem for editorial content — no single right answer. Do you know how to work in that space?

*Format:* PCR

*Answer:*

"The absence of a single ground truth is actually the normal state for most interesting evaluation problems. The insurance conversation work I did had no ground truth in the traditional sense — an experienced analyst knew a bad interaction when they saw it, but couldn't write a rule that captured it. Editorial quality is the same problem at a higher level of abstraction.

My approach is to replace ground truth with expert consensus. You identify three to five domain experts whose judgment you trust, have them independently rate a sample of outputs, and use their agreement as the benchmark. Where they agree strongly, that's your easy cases — the eval should get those right. Where they disagree, that's where the problem is genuinely hard, and you need to decide: is the eval job to replicate the average, or to surface the disagreement and let a human decide?

For The Economist specifically, I'd be very wary of treating editors as a homogeneous group. Different editors have different aesthetics. The right framing might be: define the eval in terms of 'would this pass editorial review' — a binary — rather than 'is this excellent Economist writing.' That's a lower bar but it's a bar you can measure reliably.

The other option when ground truth doesn't exist is preference-based eval without reference. Show two versions of the same piece to the same editor, ask which they'd publish. No rubric required, just a binary choice. Accumulate enough of those paired comparisons and you have a ranking. It's slow, but it creates labelled data that can train a more automated judge over time."

---

### RAG

---

**Q4: "Walk me through the RAG architecture decisions you'd make for a journalism use case."**

*What they're really asking:* Technical depth, and whether you can reason about tradeoffs — not just describe what RAG is.

*Format:* PCR

*Answer:*

"The first decision I'd make before touching any architecture is what a good retrieval looks like. For journalism, that means asking editors to show me 10 cases where they'd want retrieval to find something non-obvious — a thematic parallel from three years ago, a counterpoint from a different geography, a data point that changes the framing. If the architecture can't find those, it doesn't matter how elegant the rest is.

Then chunking. Most RAG implementations fail on journalism content because they get chunking wrong. Sentence-level chunks destroy coherence. Full-article retrieval loses specificity and makes re-ranking harder. For journalism I'd chunk at the paragraph level — that's the natural unit of argument in a broadsheet — and preserve article-level metadata with each chunk: date, section, author, topic taxonomy, and a generated summary of the article. You retrieve chunks but you surface article context.

On retrieval: hybrid retrieval — BM25 for keyword precision plus dense embeddings for semantic similarity, with a cross-encoder re-ranker to score the combined result set — typically outperforms either method alone on quality-sensitive tasks. For The Economist's archive, where terminology is specific and technical vocabulary matters, BM25 adds real value that pure semantic retrieval misses. You wouldn't want to retrieve only on embedding similarity and miss an exact match on 'Balassa-Samuelson effect.'

Then a post-retrieval quality gate — an LLM judge that assesses relevance before surfacing results to the journalist. This cuts noise substantially. The failure mode I saw most in the telecom RAG evaluation I ran was 'plausible but wrong' — chunks that sounded relevant and scored well on embedding similarity but were about a different context. That failure mode is more dangerous than 'found nothing' because the journalist doesn't know to distrust it."

**Chunking options with tradeoffs:**

| Strategy | Pros | Cons | When to use |
|---|---|---|---|
| Fixed-size (e.g. 512 tokens) | Simple, fast to implement | Breaks mid-sentence, loses coherence | Baseline only |
| Sentence-level | Fine-grained retrieval | Loses context, noisy re-ranking | Short-form content |
| Paragraph-level | Preserves argument unit, good for journalism | Paragraphs vary in length | Journalism, essays, reports |
| Semantic (by topic shift) | Preserves semantic coherence | Harder to implement, requires embedding clustering | Long-form technical docs |
| Hierarchical (chunk + parent article) | Best of both — precise retrieval, full context available | More complex indexing | Production, quality-critical retrieval |

**Retrieval options with tradeoffs:**

| Method | Pros | Cons | When to use |
|---|---|---|---|
| Dense (vector/embedding) | Captures semantic similarity, handles paraphrase | Misses exact keyword matches, expensive to index | General semantic search |
| Sparse (BM25/TF-IDF) | Fast, exact keyword matching, interpretable | Misses synonyms and paraphrase | Technical vocabulary, proper nouns |
| Hybrid (dense + sparse) | Best recall across both dimensions | More complex pipeline, re-ranker required | Quality-critical tasks — use this for Economist |
| Re-ranking (cross-encoder) | Most accurate relevance scoring | Slow — runs on retrieved set, not full index | Applied after initial retrieval |

---

**Q5: "How do you evaluate a RAG pipeline?"**

*What they're really asking:* Do you know the specific metrics for RAG, or do you only know general eval concepts?

*Format:* PCR

*Answer:*

"RAG evaluation has two independent failure modes that require separate measurement: retrieval quality and generation quality. If you evaluate only the final answer, you can't tell whether a failure was a retrieval failure or a generation failure — and they have different fixes.

On the retrieval side, the metrics I use are context precision — of the chunks retrieved, what fraction are actually relevant? — and context recall — of the relevant chunks that exist in the index, what fraction did retrieval find? Precision matters more for latency and noise; recall matters more for coverage. RAGAS is a useful framework here; it provides implementations of both with an LLM judge doing the relevance scoring. For a journalism use case, I'd also add a manual retrieval audit on a sample of real queries — running 20–30 journalist-style queries and reviewing what comes back is more informative than any automated metric in the early stages.

On the generation side: faithfulness — does the answer contain only claims supported by the retrieved context? — and answer relevance — does the answer actually address the query? Faithfulness is the hallucination check; it's the one you can't afford to skip for journalism.

The metric that doesn't exist but that matters most for editorial: does the retrieved passage actually help the journalist? That's not measurable automatically. You need the journalist in the loop. I'd design a lightweight feedback mechanism — a binary thumbs up/down on retrieved results that accumulates into a quality signal over time. That's also your eval dataset for future automated measurement."

---

**Q6: "What are the failure modes of RAG you've seen in practice?"**

*What they're really asking:* Real production experience, not textbook knowledge.

*Format:* STAR

*Answer:*

"The most instructive failure I've seen directly was in the telecom RAG evaluation work — we were assessing four different RAG solutions across a set of quality criteria including accuracy and hallucination rate. The finding that shifted the client's roadmap was that hallucination risk was highest not when retrieval found nothing, but when it found something plausible-but-wrong. A chunk that sounded relevant, matched on semantic similarity, but was from a different tariff context produced confident, well-formatted answers that were factually incorrect. That failure mode is more dangerous than 'no result found' because the user doesn't know to distrust it.

The practical lesson: build detection for plausible-but-wrong retrieval as a first-class concern, not an afterthought. The fix was to add a post-retrieval relevance check — a lightweight LLM judge that assessed whether each retrieved chunk was genuinely appropriate for the specific query before it was used in generation.

Other failure modes I'd highlight from that work:

**Chunk boundary failures** — where the relevant information spans two chunks and neither contains the full context. This shows up as partial answers that sound complete. Fix: overlap between chunks, or hierarchical chunking that can fall back to article-level context.

**Temporal decay** — old content retrieved without surfacing the date. For a news organisation with a multi-decade archive, a 2015 article about a country's economy retrieved without attribution could be worse than no answer. Metadata surfacing is a design problem as much as a retrieval problem.

**Query-document vocabulary mismatch** — journalists use natural language, the archive uses editorial style. Dense embedding handles most of this, but for specialised terminology where exact match matters, pure semantic retrieval drops relevant results. That's where hybrid retrieval pays off."

---

### ARCHITECTURE AND SYSTEM DESIGN

---

**Q7: "How would you architect an AI pipeline for a newsroom?"**

*What they're really asking:* Open-ended design question — they want to see how you structure a solution to an ambiguous problem.

*Format:* PCR

*Answer:*

"The first thing I'd do is resist the urge to design anything before understanding what the pipeline is for. 'A pipeline for a newsroom' could mean research retrieval, audio transcription, style-adaptive drafting, fact-check flagging, or headline generation — these have very different architectures. So step one is: what does a journalist actually do in a session that AI could make faster or more reliable, without compromising the editorial decisions that define the work?

Assuming the primary use case is research and drafting assistance, the architecture I'd reach for has four layers. First, a retrieval layer — hybrid retrieval over the archive with metadata filtering by date, section, and topic; a re-ranker to score relevance; and a post-retrieval gate that checks whether what came back is actually useful for the query. Second, an analysis layer — if the journalist has a draft in progress, a context injection step that makes the retrieval aware of what they're already writing. Third, a generation layer — a prompt chain that takes retrieved passages plus the working draft and produces a suggestion: a data point to include, a counterpoint to consider, an angle they haven't covered. Fourth, an evaluation layer — a lightweight quality gate that checks whether the generated suggestion is factually grounded in the retrieved passages before it reaches the journalist.

What I'd be careful about: latency. A journalist in flow doesn't want to wait for a 4-step pipeline to return. That means caching retrieval results for common query patterns, running retrieval and generation in parallel where possible, and being willing to surface a fast partial result rather than a slow complete one.

The other design principle: every part of the pipeline should be independently testable and independently observable. LangSmith-style tracing on every node. If the journalist gets a bad suggestion, you need to know whether it was a retrieval failure or a generation failure — they have different fixes."

---

**Q8: "When would you use an agent vs a chain vs a single prompt?"**

*What they're really asking:* Do you have a principled view, or do you reach for agents by default because they sound impressive?

*Format:* PCR

*Answer:*

"My default is: use the simplest structure that can solve the problem. A single prompt first. A chain if the task has genuinely separable stages. An agent only when the number of steps or the routing logic is unknown in advance.

The test for whether a chain is warranted: can I write out the full sequence of steps before building anything? If yes — step one does X, step two takes that output and does Y, step three does Z — it's a chain. That means I can test every step independently before wiring it together, and the failure modes are predictable. My LinkedIn Post Agent is a six-node chain that looks like an agent: idea refinement → research → draft → review → conditional rewrite → finalisation. But it's not an agent — the routing is deterministic. The conditional rewrite loops a maximum of twice. I can predict every possible execution path.

An agent is warranted when the model needs to decide at runtime how many steps to take, which tool to call, and in what order — usually because the task requires exploration rather than execution. Web research is a good example: you don't know in advance how many searches you'll need or what follow-up queries will emerge from the first result.

For a journalism pipeline specifically, I'd start with chains for everything that has a clear sequence — retrieve, analyse, draft — and only reach for an agent if the research step requires open-ended tool use. The reason I'm conservative about agents: they're harder to test, harder to observe, and harder to explain when they fail. For editorial content where trust is critical, predictable execution paths matter."

---

**Q9: "How do you decide when something is ready for production?"**

*What they're really asking:* Do you have a quality gate, or do you ship when it 'seems to work'?

*Format:* PCR

*Answer:*

"Three gates, in order. First, the pipeline has to pass its eval suite — meaning it meets or exceeds human agreement rates on the labelled test set, including a representative sample of edge cases. If you don't have an eval suite, you're not ready for production, you're just done with prototyping.

Second, I run the pipeline against 30–50 real-world inputs that weren't in the test set. This is the second eval phase. Failures here add directly to the test set — they're the inputs I didn't anticipate. If the failure rate on real inputs is dramatically higher than on the test set, the test set isn't representative and the pipeline isn't ready.

Third, observability has to be on before the first live user. LangSmith traces on every node. Structured logging on inputs, outputs, and scores. Alerting on anomaly patterns — score distribution shifts, latency spikes, error rates. Without this, production is a black box.

For editorial content specifically, I'd add a fourth gate: a manual review phase with real editors on the first 50 outputs after launch. Not because the pipeline is probably wrong, but because editors are faster at identifying failure modes than any automated metric. You want to understand how it fails on your content before you scale the number of users."

---

**Q10: "How do you instrument and monitor an LLM pipeline in production?"**

*What they're really asking:* Production experience. Do you know what breaks and how to see it coming?

*Format:* PCR

*Answer:*

"LangSmith is my default for LLM-specific tracing — per-node traces that show exactly what input each step received and what output it produced. That's the minimum. Without it, when something fails intermittently on a specific input shape, you're debugging blind.

Beyond tracing, the metrics I track: score distribution over time — if average output quality scores start drifting, something upstream changed. Latency per node — usually the first signal of a model API issue. Error rate by node — where in the chain failures cluster. Input distribution — if the types of queries the pipeline receives shift significantly, the pipeline may degrade even though nothing about the pipeline changed.

For editorial content, I'd add one more layer: feedback capture. A lightweight mechanism — even just a binary rating from the journalist — that creates a stream of labelled production data. Over time, that's your eval dataset update mechanism. The inputs that get low ratings become the next batch of test cases to add to the suite.

One thing I'd say: most LLM pipeline failures in production are silent. The pipeline returns an output, the output looks plausible, and no error is raised — but the output is wrong in a way that a journalist would notice. That's harder to detect than a crash. Score distribution monitoring is the main defence: if the distribution of quality scores starts skewing, you need to know before a journalist does."

---

### PYTHON / TECHNICAL DEPTH

---

**Q11: "Can you walk me through how you'd write [X] in Python?"**

*What they're really asking:* How fluent are you with code? Are you a real engineer or someone who talks about engineering?

*How to handle it honestly:*

"I want to be straightforward about how I work. I build Python pipelines — the architecture, the component design, the data contracts, the evaluation logic — but I do it with heavy tooling assistance from Claude Code. I direct the build, I review the output, and I catch the failure modes. I don't write dense Python from scratch in real-time without tooling the way someone who's been writing Python daily for five years would.

What I can do in the room: reason through the architecture, explain how I'd structure the state schema, describe how I'd handle the edge cases, walk through where the failures would likely come from. What I can't do: write fluent production Python from a whiteboard prompt as a demonstration.

I'd push back gently on one thing: the pipelines I've shipped to production — processing 50,000+ conversations, running 15,000+ profile automations at scale — have been production-quality not because every line was written by hand, but because the architecture was right and the failure modes were understood and handled. If the role requires someone who can write dense Python independently in a pair-programming session, I want to know that — because I'm not the right answer for that specific scenario. If it's about building reliable systems that hold up under real data, that's where I operate."

---

## Section 2 — Stakeholder Management at The Economist

The AI Lab at The Economist isn't embedded in a typical engineering org. It sits inside a newsroom. That makes stakeholder management one of the most distinctive challenges of the role — and one the tech lead will probe, because it's probably been the hardest part of running the lab so far.

There are three distinct stakeholder types you'll need to manage, and they have almost nothing in common.

---

### Stakeholder 1: Journalists and Editors

**Who they are:** Domain experts with high standards, strong aesthetic opinions, and zero obligation to trust an AI system. They have more to lose from bad AI output (reputational damage, factual errors) than anyone else in the building.

**What they want:** Tools that make their work faster without undermining the quality they've built a career around. They're not hostile to AI — they're hostile to AI that wastes their time or embarrasses them.

**What makes this hard:** They can't articulate their quality bar in a rubric. They know bad output when they see it, but they can't tell you the rules. Building evals from that is an engineering problem disguised as a communication problem.

**How to manage them effectively:**
- Start from their output, not your tooling. Ask to see work they're proud of and work they consider poor — those become your reference set.
- Surface failure modes before they find them. If you show them where the system gets it wrong before they discover it themselves, they shift from sceptics looking for problems to collaborators helping you fix known ones.
- Never defend a bad output. If an editor says a generated passage sounds wrong, it sounds wrong. Their instinct is the ground truth you're building toward, not an opinion to negotiate with.
- Give them control over the eval. When they label outputs good or bad, they're not doing busywork — they're building the dataset that makes the system better. Frame it that way.

**The thing that kills this relationship:** Shipping something that reaches a journalist and embarrasses them. One bad output in production does more damage to trust than ten good ones repair. Human review gates on early outputs aren't optional.

**Likely question form:** "How would you work with editors who are sceptical about AI?"

*Use:* The Canadian engineering firm example (40 non-technical staff, started from their outputs not your tooling, showed failure modes proactively). Adapt it to editorial context — the principle is identical.

---

### Stakeholder 2: The Tech Lead and Engineering Peers

**Who they are:** The people in round 2. They care about whether your systems are well-designed and maintainable, not just whether they produce plausible output. They'll push back on architecture choices and want to know your reasoning.

**What they want:** A peer who brings genuine technical judgment and doesn't need babysitting. Someone who can own a component of the system, make defensible decisions, and flag problems early.

**What makes this hard:** You have real gaps (Python fluency, fine-tuning experience) that a peer-level conversation makes more visible than a hiring manager conversation. The gap can't be hidden — it needs to be positioned.

**How to manage them effectively:**
- Lead with position. In peer technical conversations, "here's what I'd do and why" earns more credibility than "here are the options." You can always qualify the position — but start from one.
- Name the failure modes. Nothing signals real experience like knowing where a system breaks. Include failure modes unprompted in any technical answer.
- Be precise about your gaps. "I haven't run SFT directly but I've built the eval infrastructure around it and understand the data curation requirements" is a stronger framing than "I'm still learning fine-tuning." The former is a specific, bounded gap. The latter sounds like you don't know what you don't know.
- Engage genuinely with their problems. The questions in Section 1 are designed to do this — asking about prompt versioning, model drift, what's currently broken in production. A tech lead who sees that you're thinking about the operational problems, not just the build, treats you differently.

---

### Stakeholder 3: Editorial Leadership and Senior Management

**Who they are:** The Head of Data Engineering (round 4 in your process), the VP of AI (round 4), and the editorial leadership who've given the lab its mandate. They care about outcomes and risks, not implementation details.

**What they want:** Confidence that the lab is building things that will actually work in the newsroom, that the risks are understood and managed, and that the investment is going to pay off. They need to be able to answer questions from the Editor-in-Chief about what AI is doing in the building.

**What makes this hard:** These stakeholders have the least technical context and the most power to kill the project. A single high-profile failure — a factual error surfaced to an editor, a pipeline producing content that runs — would put the whole lab's mandate at risk. They're managing reputational risk at institutional scale.

**How to manage them effectively:**
- Frame everything in terms of editorial quality and risk, not technical capability. "This eval framework measures whether outputs would pass editorial review" lands better than "this eval pipeline has 87% agreement with human labels."
- Be the person who surfaces risks before they surface themselves. Senior stakeholders trust people who bring them bad news early. The alternative — discovering a problem after it's gone to print — is what they're most afraid of.
- Be honest about what AI can and cannot do for The Economist specifically. The voice drift argument (from round 1 prep) is the right frame: the lab's job is to handle tasks where the quality bar is clear and the failure mode is recoverable, and protect editorial judgment on everything else.

---

### The Cross-Cutting Principle

The common thread across all three groups is: **earn trust before asking for autonomy.**

Every AI deployment in a newsroom starts with more human oversight than it eventually needs. The editorial team reviews every output in the first cohort. The tech lead reviews your architectural decisions early on. Senior management reviews the lab's output against editorial standards. Over time, as the track record builds, the oversight reduces.

If you try to move to autonomous deployment before the trust is established — even if the system is technically ready — you'll lose the stakeholders and the mandate. If you build trust systematically and let performance data do the arguing for expanded autonomy, the system earns its own room to run.

This framing is also useful as a question: *"How does the lab currently think about the transition from human-reviewed outputs to more autonomous deployment — is there a process for earning that autonomy, or is it more informal?"* It signals that you understand the stakes and have a view on how to manage them.

---

## Section 3 — Behavioural Questions for a Tech Lead Interview

A tech lead interview mixes technical depth with behavioural probing — they want to know how you work as much as what you know. Based on the 8 core behavioural themes, the ones most likely to surface in round 2 are: **failure/recovery**, **problem-solving under ambiguity**, **learning a new skill quickly**, **functional leadership and influence**, and the AI-specific questions that are now becoming standard. Customer/user focus is covered in the stakeholder management section above. Time management and pure success stories are less likely from a tech lead.

---

**BQ1: "Tell me about a time an AI system you built failed in production and what you did."**
*Theme: Failure — they want to know you debug systematically and learn, not that you've never shipped anything imperfect.*
*Format:* STAR

*Answer:*
"The most instructive production failure I've dealt with was in the research agent I built for a client — a pipeline for account executives that monitored company and prospect news, identified outreach opportunities, and drafted personalised emails in the AE's voice. The pipeline ran five chained prompts in sequence: web search to find relevant URLs, a per-URL summarisation pass, a final report compilation, an opportunity identification step, and email drafting — all routed through Supabase as the backend. In testing against small samples it worked reliably. When it ran against the client's full company list in production, it started failing mid-execution — some companies got partial output, others got nothing.

The root cause was cumulative latency in the chained prompts. Each step was individually fast enough, but five sequential LLM calls per company, iterated across a full client list, pushed the total execution time past Supabase's function timeout limits. It wasn't a model failure or a prompt failure — it was an architecture that worked at test scale and didn't hold at production scale.

The fix required restructuring how the pipeline handled execution time. I added explicit timeout handling at each step, broke the company list processing into smaller batches so no single function invocation accumulated the full chain cost, and added retry logic for steps that failed mid-run. I also added state checkpointing — writing intermediate results to the database as each step completed rather than holding them in memory — so a timeout didn't lose the work that had already succeeded.

The lesson: the test set tells you whether the logic is right; it doesn't tell you whether the architecture holds at scale. Latency in chained LLM pipelines is multiplicative, not additive — and that only becomes visible when the input volume is production-sized. I now build explicit latency budgets into any multi-step pipeline design before I start building, and test against the upper bound of the expected input volume before I call it done."

*Notes:* If they probe for detail — the key architectural change was moving from in-memory state across the full chain to database-checkpointed intermediate results. That's the thing that made the pipeline resilient rather than just faster.

---

**BQ2: "Describe a time you had to solve a problem with incomplete information and make a judgment call."**
*Theme: Problem-solving under ambiguity — relevant to the lab context, where editorial quality is hard to define and requirements are often implicit.*
*Format:* STAR

*Answer:*
"The insurance evaluation work was the clearest version of this. The client needed a pipeline to classify 50,000+ customer-broker conversations — but the quality bar was implicit. There was no written rubric. The experienced analysts knew a problematic interaction when they saw it, but couldn't give me a rule set. I had to make a judgment call about how to capture that without a defined ground truth.

The call I made was to treat the analysts themselves as the ground truth rather than trying to extract the rules from them. I asked three analysts to independently classify a sample of 500 conversations, then measured where they agreed and where they disagreed. The agreement cases became my labelled dataset. The disagreement cases — about 15% of the sample — became the 'hard cases' category, which the pipeline escalated to human review rather than trying to classify automatically.

The incomplete-information element was that I didn't know how high the agreement rate would be until I ran the exercise. If it had come back at 60%, the whole approach would have been in trouble — you can't build a reliable classifier on a ground truth that humans only agree on 60% of the time. It came back at 84%, which was high enough to build on. But I'd committed to the approach before I knew that number, which required making a judgment that the analysts would agree more often than not on the core cases.

The pipeline ended up running reliably across the full dataset. The escalation bucket — the hard cases — turned out to be about 12% of the volume, which matched the client's expectation of how much manual review they'd need to keep."

---

**BQ3: "Tell me about a time you had to learn something new quickly because a project required it."**
*Theme: Learning/growth mindset — signals adaptability, which matters in a fast-moving lab.*
*Format:* STAR

*Answer:*
"When I started building the LinkedIn Post Agent, I hadn't used LangGraph before. I'd built multi-step pipelines but they were mostly linear chains in n8n or sequential prompt calls — not proper stateful graphs with conditional routing and typed state schemas. The pipeline I needed required conditional loops, parallel branches, and a human-in-the-loop review gate that could short-circuit the standard flow. That required LangGraph.

I gave myself a week to get to a working implementation. The way I approached it: I started by mapping the full pipeline on paper first — every node, every edge, every state variable the graph needed to track. That meant the learning problem got split in two: understanding the domain logic of what the agent needed to do, and then translating that into LangGraph primitives. Keeping them separate meant I wasn't learning the tool and designing the system simultaneously.

The thing that accelerated it most was building the simplest possible working graph first — a three-node graph with no conditional logic, just to prove the state schema was correct and that LangSmith tracing was working end-to-end. Then I added complexity incrementally. Each addition had a clear test. By the time I added the conditional rewrite loop, the rest of the graph was already validated.

The full six-node pipeline was working within the week. What I'd say about the learning: the paper design upfront was what made it tractable. I've found that most technical learning accelerates when the conceptual design is done first and the technology question reduces to 'how do I express this design in these primitives' rather than trying to learn and design simultaneously."

---

**BQ4: "Give an example of a time you influenced a technical direction without having direct authority."**
*Theme: Leadership through influence — directly relevant in a small lab where you're not managing anyone but need to shape how things are built.*
*Format:* STAR

*Answer:*
"At HumanFirst, after the company restructure reduced the team significantly, there was no formal decision-making structure for how we approached client AI work — it defaulted to whatever seemed fastest to ship. I had a view that the approach was accumulating risk: we were wiring pipelines together before the prompts had been validated independently, which meant failures showed up in integration rather than at prompt level where they're cheap to fix.

I didn't have authority to change the process — I was one of eight remaining team members, not a lead. What I did instead: I ran one project visibly differently, documented the approach, and showed the comparison. I mapped the pipeline on paper before building anything, tested every prompt against a real input set in HumanFirst before wiring them together, and shared the testing notes in a shared doc as I went. The project delivered faster than the equivalent previous projects and had fewer issues in client review.

The influence came from the evidence, not from the argument. When the next project started, the lead asked me to run the same way. That became the de facto methodology without a formal process change being declared.

The thing I learned from it: in small teams, the most durable way to shift technical practice is to do it visibly and let the outcome do the arguing. A well-constructed memo about why we should work differently is less persuasive than one project that demonstrably went better."

*Notes:* This is also a good 'success story' answer — the prompt-first methodology came from this experience.

---

**BQ5: "How do you validate AI output before shipping to a real user?"**
*Theme: AI-specific — this is now a standard question per the interview advice article, and for a tech lead at an AI lab it's almost guaranteed.*
*Format:* PCR

*Answer:*
"Three gates, in order. First, the pipeline passes its eval suite — meaning it meets or exceeds human agreement rates on a labelled test set that includes representative edge cases. If there's no eval suite, we're not ready to ship; we've just finished prototyping.

Second, I run the pipeline against 30 to 50 real-world inputs that weren't in the test set. This is the second eval phase. The failures here go directly into the labelled dataset — they're the inputs I didn't anticipate and they're the most valuable additions to the test set I'll ever get. If the failure rate on real inputs is dramatically higher than on the curated test set, the test set isn't representative enough and we go back.

Third, observability goes on before the first live user touches it — not after. LangSmith traces per node, structured logging on inputs and outputs, score distribution monitoring. Without this, when something fails on a specific input in production, I'm debugging blind.

For editorial content at The Economist specifically, I'd add a fourth gate: a manual review phase with actual editors on the first 50 outputs post-launch. Editors are faster at identifying quality failures than any automated metric — they can see voice drift, subtle factual errors, and tonal problems that don't register in an LLM judge. You need to understand how the pipeline fails on your content before the number of users scales up.

The underlying principle is: production failures are expensive to debug and expensive for trust. Every hour spent on pre-launch validation is worth more than a day of post-launch incident response."

---

**BQ6: "Describe a situation where you disagreed with a technical approach and what you did."**
*Theme: Conflict — tests whether you'll push back constructively or just go along with things.*
*Format:* STAR

*Answer:*
"During the telecom RAG evaluation, the initial brief from the client's internal team was to evaluate the four platforms — LangChain, Dialogflow CX, Stack AI, and OpenAI GPTs — against a standard accuracy benchmark and recommend the highest scorer. My view was that accuracy as the primary metric would give them a misleading answer, because the most dangerous failure mode in a contact centre RAG system isn't low accuracy — it's confident wrong answers. A system that scores 78% accuracy but hallucinates convincingly on the 22% is worse in practice than one that scores 70% but surfaces uncertainty rather than fabricating.

I disagreed with the framing but I didn't just say so. I built the case first: I pulled examples of each system's failure mode from the evaluation data and categorised them — right answers, wrong answers that the system flagged as uncertain, and wrong answers the system delivered with high confidence. The third category was the one that mattered. I presented that categorisation alongside the accuracy numbers and asked the client which failure mode they were most afraid of for their agents.

They immediately said the confident wrong answer. So we restructured the evaluation framework to weight hallucination rate — specifically confident hallucination — more heavily than raw accuracy. The recommendation changed. The platform they'd been leaning toward based on accuracy scores turned out to have the highest confident hallucination rate; a different system won on the revised framework.

The technical lesson: the metric you choose determines the answer you get. Disagreeing with the metric was the right call, but it only landed because I built the evidence before making the argument."

---

## Section 4 — Key Shifts vs Round 1

**In round 1:** you established credibility through narrative, named specific projects, and demonstrated self-awareness about gaps. That worked.

**In round 2:** the tech lead already knows you passed round 1. The question is whether you can hold your own technically. Concretely:

- **Open with position, not setup.** When asked about evals or RAG, state your view first. "I use hybrid retrieval because..." not "there are several approaches, including..."
- **Name the failure modes.** The thing that most signals real experience is knowing what breaks. Include failure modes unprompted.
- **Use numbers when you have them.** 50,000+ conversations, 96% F1, 500-conversation baseline — these are in your background, use them.
- **Don't over-explain the fine-tuning gap.** Round 1 addressed it. If it comes up again, acknowledge once and move on. The tech lead will have read round 1 notes.
- **Ask genuinely technical questions.** The questions in Section 1 are designed for this. Use them. A tech lead respects a candidate who asks about prompt versioning and model version drift — those are operational concerns that signal real experience.
