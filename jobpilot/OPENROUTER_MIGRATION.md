# OpenRouter / Kimi 2.5 Migration Plan

Swap Anthropic SDK calls (Sonnet + Haiku) for Kimi 2.5 via OpenRouter's OpenAI-compatible API.

## What changes

| File | Current | After |
|---|---|---|
| `core/config.py` | `ANTHROPIC_API_KEY`, `llm_scoring_model` default | `OPENROUTER_API_KEY`, Kimi model slug |
| `generation/cover_letter.py` | `anthropic.Anthropic`, `claude-sonnet-4-6` | `openai.OpenAI` + OpenRouter base URL |
| `generation/cv_customisation.py` | `anthropic.Anthropic`, `claude-sonnet-4-6` | same |
| `core/llm_scorer.py` | `anthropic.Anthropic` + `anthropic.AsyncAnthropic` | `openai.OpenAI` + `openai.AsyncOpenAI` |
| `.env` | `ANTHROPIC_API_KEY=sk-ant-...` | `OPENROUTER_API_KEY=sk-or-...` |
| `profile.yaml` | `llm_model: claude-haiku-4-5-20251001` | `llm_model: moonshotai/kimi-k2` (confirm slug) |

## Key API differences

```python
# Before (anthropic SDK)
client = anthropic.Anthropic(api_key=config.anthropic_api_key)
resp = client.messages.create(model=..., max_tokens=..., messages=[...])
text = resp.content[0].text

# After (openai SDK → OpenRouter)
from openai import OpenAI
client = OpenAI(api_key=config.openrouter_api_key, base_url="https://openrouter.ai/api/v1")
resp = client.chat.completions.create(model=..., max_tokens=..., messages=[...])
text = resp.choices[0].message.content
```

Async: `anthropic.AsyncAnthropic` → `openai.AsyncOpenAI` (same base URL/key pattern).

## Steps

1. **Confirm Kimi 2.5 model slug** at openrouter.ai/models (likely `moonshotai/kimi-k2` or `moonshotai/kimi-2.5`)
2. **Add dependency** — `pip install openai` (already present if used elsewhere; remove `anthropic` if desired)
3. **`core/config.py`** — rename `anthropic_api_key` → `openrouter_api_key`, read `OPENROUTER_API_KEY` from env
4. **`generation/cover_letter.py`** — replace client init + response access
5. **`generation/cv_customisation.py`** — same as above
6. **`core/llm_scorer.py`** — replace both sync and async client; update `except anthropic.APIError` → `except openai.OpenAIError`
7. **`.env`** — swap key; update `.env.example`
8. **`profile.yaml`** — update `llm_model` default
9. **Pages** — grep for `ANTHROPIC_API_KEY` error messages in `pages/` and update strings

## Notes

- OpenRouter supports `HTTP-Referer` and `X-Title` headers for dashboard tracking — optional but useful
- Kimi 2.5 context window is large (128k+); existing prompts fit comfortably
- LLM scoring is off by default (`llm_enabled: false`) so scorer changes are low-risk
