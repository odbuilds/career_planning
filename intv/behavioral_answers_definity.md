# Behavioral Answers — Definity Project

*Source: Definity / Deloitte engagement at HumanFirst. Four NLP use cases built over ~4 months: Key Issue Topic Modelling, FAQ Extraction & Gap Analysis, Senior Agent Escalation, Callback Analysis. ~30,000+ insurance call-centre and chat conversations processed via LLM pipelines and NLU models.*

---

## "How do you keep stakeholders aligned when requirements change mid-project?"

The clearest example I have is the FAQ extraction work on Definity. We were building a system to extract customer questions from call-centre transcripts and map them against existing FAQ pages to find coverage gaps. Deloitte and the client had been insisting for weeks they wanted verbatim extraction — the exact words customers used, not reformulated questions. We built the verbatim model, got it to usable F1, but when we looked at the outputs at scale — things like "So there's no way I can just fast track that payment, like pay today type deal?" — it was obvious these couldn't be mapped to any FAQ page in a meaningful way. They were call-specific, not questions the business could act on.

Rather than just flagging a problem, I ran the inferred version in parallel — reformulating the customer's implicit intent into proper FAQ format — and showed both outputs side by side. The inferred model mapped more cleanly to the taxonomy and revealed gaps the verbatim approach missed entirely. The pivot was decided in one call. What made it land was having the comparison ready before the argument: evidence before opinion. The hard part wasn't the pivot — it was that Deloitte had already committed to verbatim internally to their client. What I did was document the decision and the rationale publicly in the project channel, so there was a shared record of what changed and why. That mattered when stakeholders who hadn't been on the call tried to revisit it later.

The lesson: on AI projects, teams align on a label ("verbatim", "inferred") before they've seen what the output looks like at scale. The real alignment work happens the first time you put 1,000 real outputs in front of domain experts and ask whether they're useful.

---

## "Describe a time you influenced a technical direction without formal authority."

About six weeks into the Definity project, we hit a problem with JSON output at scale. Gemini was producing valid-looking JSON on the five-to-ten sample tests we were running in the tool, but when we batched across thousands of conversations, roughly 6% of records were structurally invalid — comments injected into key names, missing closing brackets, unpredictable extra keys. On a pipeline where invalid output breaks the downstream classification step, that silently drops 1-in-16 records.

The instinct was to add validation and retry logic or tighten the JSON prompting. I pushed back on both. My argument was that working in JSON was pulling us away from something we could inspect — you couldn't sanity-check quality at a glance in the tool — and that key-value pair output was structurally more robust because the LLM didn't need to maintain a schema across a long generation. I ran a side-by-side: same prompt, JSON vs key-value, at scale. Key-value had 0% structural failures and was easier to read in every internal review. I didn't have authority over how Deloitte implemented their ETL — they were the systems integrator — but by having the working alternative ready before the conversation, the team moved to key-value. The approach I rely on: don't argue for a direction, build the small thing that demonstrates it and let the output argue.

---

## "How do you build an eval framework when there's no clear ground truth?"

For the FAQ extraction use case there was no existing labelled dataset of "the right questions to extract" — it genuinely didn't exist. What we had was a Deloitte test team who had manually reviewed a sample of conversations and annotated the questions they thought should be extracted.

I built the evaluation around semantic similarity rather than exact match — the right approach when paraphrase is expected. For each conversation in the test set, I compared the prompt's extracted questions against the test team's ground truth using embedding similarity, with a 0.55 confidence clip to mark pass/fail. Initial results: 60% pass on calls, 82% on chat. The 60% felt alarming until I dug into the failures — a significant portion were cases where the prompt had extracted a valid but *additional* question the test team hadn't flagged. The system wasn't wrong, it was finding things humans had missed. That reframe matters: if you score purely on recall against a human-annotated ground truth, you penalise the system for finding things you didn't think of.

What I'd do differently: the test team's annotation format had inconsistencies — "or" conditions, varying specificity — that made automated processing messy. I'd now lock down the annotation schema before anyone labels a single example, not after you're trying to run evals against it.

---

## "How do you work with domain experts who can't articulate the rules they're applying?"

For the Senior Agent Escalation use case, we needed to define a taxonomy of why junior agents escalate to senior agents. The business contact gave us three starting categories: "Frontline Agent Error," "Stubborn Customer," and "Website/Communication Unclear." That's not a taxonomy — that's a first guess from someone who'd never had to formalise this before.

I don't ask domain experts for the rubric upfront. You get the categories they can think of in the room, not the categories that exist in the data. Instead, I ran the prompt on the actual call transcripts and let the outputs surface the real distribution. What came back was far richer: "Underwriting Clarification" accounted for 46% of cases — the single biggest category — which nobody had identified. "System Error" was 10%. "Documentation or Process Unclear" was 28%. Only when those categories were visible did we get genuine engagement on whether the taxonomy was right. That conversation — reacting to real outputs rather than imagining hypothetical categories — is faster and more accurate than any interview-based requirements session. The implicit knowledge surfaces when you give experts something concrete to react to.

---

## "Handle it when scope keeps expanding?"

The Senior Agent Escalation use case is a good example. The brief was: classify why junior agents escalate to senior agents. But when we got into the data, there were two completely different call types in scope — support calls where a junior agent phones a senior directly, and escalation calls where the senior then phones the customer back. Different conversational structure, different signal, very different volumes (28 support calls vs ~280 escalation calls). Then Deloitte wanted output categories consistent across both call types *and* across two different brand lines.

I was direct about what was possible with the data. With 28 support calls I could validate whether they contained extractable escalation reasons — I couldn't build a production-grade model. I said that clearly and documented it. The scope expansion I pushed back on was combining both call types into a single prompt — I tested it and the prompt got confused, assigning "None" far more often because the two contexts were incompatible. The solution was two separate prompts sharing a common taxonomy: kept the output consistent for their Tableau dashboard, let each prompt do its job cleanly. The principle: accept that goals are expanding, but be explicit about where the architecture has to stay narrow to function.

---

## "What's the hardest part of getting an AI pilot to become a production system?"

The Definity go-live taught me something I now expect on every project. We'd cleared every technical blocker — models trained, prompts stable, pipelines running, FAQ live — and then at the go-live review, Deloitte revealed how they'd actually implemented data ingestion. Instead of the recommended pattern (multiple files per conversation set, rolling window, pipeline caching), they'd built a system that created a brand-new conversation set every hour, linked it, ran the full pipeline from scratch, downloaded, and unlinked. It worked. But it meant pipeline caching was never used, historical data wasn't visible in the tool, and every run reprocessed everything from the beginning.

This hadn't surfaced in any technical check-in because the Deloitte team owned the integration layer — we'd been focused on the NLP components, not the orchestration. They'd built what got them end-to-end working as fast as possible under PM pressure, not what was maintainable. The hard part wasn't the fix — we documented both patterns and their trade-offs clearly. The hard part was they'd already gone live and didn't want to rework it. What I took from this: on projects where another team owns the integration, you need to review their architecture at least once before go-live, not just your own components. The failure mode in AI projects is almost never the model — it's the infrastructure around it that nobody reviewed end to end.

---

## "Tell me about a time you had to get a sceptical team to trust an AI system."

When we transitioned ownership to Definity's internal team — the analytics group who'd maintain the system after Deloitte handed over — they were genuinely uncertain about what they'd inherited. They'd watched Deloitte operate it but had no hands-on understanding of how the models worked, what uncertainty scores meant, or how to know when something needed updating.

Rather than documentation, I ran working sessions directly in the tool. The key move was showing them how to use the uncertainty score to investigate model behaviour — sorting by low-confidence outputs, looking at what the system was unsure about, understanding the difference between a model gap and a genuinely ambiguous case. I walked them through the signal for when to re-train: if a new call type starts appearing consistently in the "other" bucket, that's the cue to go build a new class, not a sign something is broken. By making the failure modes visible and navigable rather than opaque, the system became something they could interact with and improve rather than a black box they'd inherited. The client leadership feedback at the end — "this looks fantastic, great job" — came specifically after seeing that breakdown clearly for the first time, which tells you something about how much the opacity had been the blocker.
