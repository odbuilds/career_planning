# Cover Letter Generation — Classification-Routed Pipeline

**Date:** 2026-04-29

## Overview

Adds a JD classification step before the existing draft → critic → rewrite pipeline. Gemma reads the job description, identifies the role type, and produces a one-sentence reasoning string. That classification is prepended to every prompt in the chain as a `role_context` block. Each role type also loads a branch-specific example cover letter that replaces the current hardcoded examples in the draft prompt.

---

## Role Types

| Key | Description |
|-----|-------------|
| `builder` | Hands-on delivery, shipping automations, fast iteration, minimal process |
| `solutions_engineer` | Customer-facing technical work, scoping, POCs, translating problems into solutions |
| `enablement` | Embedding AI adoption across teams, training, coaching, change management |
| `ai_engineer` | Technical depth, production systems, architecture, evaluation frameworks |
| `strategic_pm` | Programme leadership, prioritisation, stakeholder management, governance, business outcomes |

---

## File Structure

```
generation/
  prompts.py               ← all prompt templates
  cover_letter.py          ← orchestrator (slimmed down)
  examples/
    builder.md             ← IFS letter
    strategic_pm.md        ← Miller letter
    enablement.md          ← Everfield letter
    solutions_engineer.md  ← stub
    ai_engineer.md         ← stub
```

---

## Data Flow

1. **Classify** — `classify(jd_text)` calls Gemma via OpenRouter. Returns `{"role_type": "<key>", "reasoning": "<one sentence>"}`. Falls back to `"builder"` if JSON parse fails.
2. **Load example** — `_load_example(role_type)` reads `generation/examples/{role_type}.md`. If file is missing or stub, falls back to `builder.md`.
3. **Assemble role context** — formats as: `Role classification: {role_type} — {reasoning}`
4. **Build prompts** — passes `role_context` and `example_letter` into templates from `prompts.py`
5. **Run pipeline** — draft → critic → rewrite, unchanged from current logic

---

## prompts.py

Contains four string templates. All templates that feed the model accept `{role_context}` as the first variable, prepended at the top of the prompt before any other instructions.

- `CLASSIFY_PROMPT` — instructs Gemma to read `{jd_text}` and return JSON `{"role_type": "<key>", "reasoning": "<one sentence>"}`. Includes the five role type keys and their descriptions so Gemma can choose correctly.
- `DRAFT_PROMPT` — current `_build_prompt()` content, with `{role_context}` at top and `{example_letter}` replacing the three hardcoded examples.
- `CRITIC_PROMPT` — current `_build_critic_prompt()` content, with `{role_context}` at top.
- `REWRITE_PROMPT` — current `_build_rewrite_prompt()` content, with `{role_context}` at top.

All other variables (`{company}`, `{role}`, `{jd_text}`, `{cv_content}`, etc.) remain unchanged.

---

## cover_letter.py Changes

- Imports all prompt templates from `prompts.py`
- `_build_prompt()`, `_build_critic_prompt()`, `_build_rewrite_prompt()` become thin wrappers that call `.format()` on the imported templates
- New `classify()` function: calls Gemma (`google/gemma-3-27b-it` or similar), parses JSON response, returns `(role_type, reasoning)`
- New `_load_example(role_type)` function: reads from `generation/examples/`, falls back to `builder.md`
- `generate()` gains two new steps at the top: `classify()` then `_load_example()`
- `role_context` and `example_letter` passed down into the three `_build_*` calls

---

## Example Files

Existing letters from `cover_ex.md` are cleaned and saved as individual files:
- `examples/builder.md` — IFS Forward Deployed AI Engineer letter
- `examples/strategic_pm.md` — Miller letter
- `examples/enablement.md` — Everfield letter
- `examples/solutions_engineer.md` — stub (copy of builder until a real example is available)
- `examples/ai_engineer.md` — stub (copy of builder until a real example is available)

---

## Error Handling

- If Gemma returns unparseable JSON: log a warning, default `role_type` to `"builder"`, `reasoning` to `"Classification failed — defaulting to builder"`
- If example file is missing: fall back to `builder.md`; if that's also missing, omit the example block rather than crashing

---

## Out of Scope

- No changes to the verify/strip dead code (leave in place, not called)
- No changes to model routing, timing logs, debug output, or CV recommendation logic
- Example letter quality improvements are a separate task
