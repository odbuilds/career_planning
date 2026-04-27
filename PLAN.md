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
    ├── 4. Apply "classified" label → prevents reprocessing
    │
    └── 5. Increment daily counter (Script Properties)

Google Apps Script (triggered once daily at ~8am)
    │
    └── Read daily counter → POST summary → Telegram channel (UrlFetchApp)
                                             reset counter to 0
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

## Daily Telegram Summary

A second time-based trigger fires once per day (e.g. 8am) and sends a digest to a Telegram channel.

**Example message:**
```
📬 email-classify daily summary
Processed: 43 emails

ai/news           18
ai/tutorial        9
ai/sales-promo     7
ai/use-cases       4
non-ai             3
ai/unclassified    2
ai/product-release 0
```

**How counts are tracked:**
- Each classification run increments per-category counters stored in GAS `PropertiesService` (key-value store, persists between runs)
- Daily trigger reads all counters, formats the message, posts to Telegram, then resets counters to 0

**Telegram setup (one-time):**
1. Create a bot via [@BotFather](https://t.me/BotFather) → get `BOT_TOKEN`
2. Add the bot to your channel as an admin
3. Get the `CHAT_ID` (channel's numeric ID, e.g. `@mychannel` or `-1001234567890`)
4. Store both as GAS Script Properties

**API call** (no library needed):
```
POST https://api.telegram.org/bot<BOT_TOKEN>/sendMessage
{ "chat_id": "<CHAT_ID>", "text": "...", "parse_mode": "Markdown" }
```

---

## Files

```
Code.gs              # Main Apps Script file (fetch, classify, label, count)
Telegram.gs          # Daily summary trigger — format + send Telegram message
Prompt.gs            # System prompt string and few-shot examples
Config.gs            # Constants: model, own domains, label names
appsscript.json      # GAS project manifest (OAuth scopes)
README.md            # Setup instructions
.env.example         # Reference for keys stored in GAS Script Properties
```

---

## Setup Steps

1. **Create a new Google Apps Script project** at script.google.com
2. **Add Script Properties** via Project Settings → Script Properties:
   - `OPENROUTER_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
3. **Set own-product domains** in `Config.gs` (`OWN_DOMAINS` array)
4. **Run `setup()` once manually** — creates all Gmail labels
5. **Add triggers**:
   - `classifyEmails` → time-based, every 10 minutes
   - `sendDailySummary` → time-based, once per day (8am)
6. **Authorize** Gmail and external URL scopes on first run

Total setup time: ~20 minutes.

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
- **Telegram counter** uses GAS PropertiesService — survives between runs but resets if the script project is deleted

---

## Out of Scope (for now)

- Unsubscribe automation
- Priority scoring within categories
- Per-email Telegram alerts (only daily digest for now)
- Mobile push notifications
