# email-classify — Implementation Plan

## Approach

Run entirely inside **Google Apps Script** (GAS). No server, no laptop dependency, no cost.
GAS lives in Google's cloud, has native Gmail access, and supports HTTP calls to OpenRouter.
A time-based trigger polls for new emails every 10 minutes, classifies them, and applies labels.

---

## Architecture

```
Gmail Inbox
    │
    ▼
Google Apps Script (triggered every 10 min)
    │
    ├── 1. Fetch unread, unclassified emails (GmailApp)
    │
    ├── 2. For each email:
    │       └── POST subject + snippet → OpenRouter API (UrlFetchApp)
    │               model: google/gemini-flash-1.5 (or cheapest available)
    │               response: { "category": "ai/news", "confidence": "high" }
    │
    ├── 3. Apply Gmail label (create if missing)
    │
    └── 4. Apply "classified" label → prevents reprocessing
```

---

## Gmail Labels

| Label | When to apply |
|---|---|
| `ai/news` | AI industry news, research, third-party announcements |
| `ai/use-cases` | Real-world AI applications and case studies |
| `ai/product-release` | New releases from **your own** products/domains only |
| `ai/tutorial` | How-to guides, walkthroughs, educational content |
| `ai/sales-promo` | Sales emails, discounts, promotional offers |
| `non-ai` | Emails unrelated to AI |
| `ai/unclassified` | Low confidence or ambiguous — review manually |
| `classified` | Internal marker — applied to every processed email |

> Third-party product launches → `ai/news`. Own-product launches → `ai/product-release`.
> Determined by checking sender domain against a hardcoded `OWN_DOMAINS` list in the script.

---

## Prompt Design

**Input to model** (kept minimal to reduce cost):
```
Subject: <subject line>
Snippet: <first 200 chars of email body>
Sender domain: <domain extracted from From address>
```

**System prompt** lists all 7 categories with definitions, the own-product rule, and 4–5 few-shot examples covering the trickiest distinctions:
- Third-party product launch → `ai/news` (not `ai/product-release`)
- Tutorial from a company → `ai/tutorial` (not `ai/news`)
- Use-case article vs tutorial → key is whether it teaches or just shows
- Sales email disguised as news → `ai/sales-promo`

**Expected response:**
```json
{ "category": "ai/news", "confidence": "high" }
```

If `confidence` is `"low"` → override category to `ai/unclassified`.

---

## Model Selection

Target: **OpenRouter**, cheapest model that reliably returns valid JSON.

| Model | Cost (input+output per 1k emails) | Notes |
|---|---|---|
| `google/gemini-flash-1.5` | ~$0.05 | First choice — fast, cheap, good instruction following |
| `mistralai/mistral-7b-instruct` | ~$0.08 | Fallback |
| `openai/gpt-4o-mini` | ~$0.15 | Fallback if others misbehave |

Model is set as a script constant — easy to swap.

---

## Files

```
Code.gs              # Main Apps Script file (fetch, classify, label)
Prompt.gs            # System prompt string and few-shot examples
Config.gs            # Constants: model, own domains, label names
appsscript.json      # GAS project manifest (OAuth scopes)
README.md            # Setup instructions
.env.example         # Reference for OpenRouter API key (stored in GAS Properties)
```

---

## Setup Steps

1. **Create a new Google Apps Script project** at script.google.com
2. **Add OpenRouter API key** via Project Settings → Script Properties
   - Key: `OPENROUTER_API_KEY`
3. **Set own-product domains** in `Config.gs` (`OWN_DOMAINS` array)
4. **Run `setup()` once manually** — creates all Gmail labels
5. **Add time-based trigger**: `classifyEmails` → every 10 minutes
6. **Authorize** Gmail and external URL scopes on first run

Total setup time: ~15 minutes.

---

## Cost Estimate

- ~150 tokens per email (subject + snippet + prompt overhead)
- Gemini Flash 1.5: $0.075 per 1M input tokens
- 1,000 emails/month ≈ **$0.01–0.05/month**

---

## Constraints & Limitations

- **6-minute execution limit** per GAS run — safe up to ~200 emails per trigger firing; batching handles overflow
- **OpenRouter key** stored in GAS Script Properties (not in source code)
- **No own-product detection via AI** — domain matching only, to keep prompt simple and avoid false positives
- **Snippet only** — full email body not sent to model; reduces tokens and avoids sending sensitive content

---

## Out of Scope (for now)

- Unsubscribe automation
- Priority scoring within categories
- Digest/summary emails
- Mobile notifications
