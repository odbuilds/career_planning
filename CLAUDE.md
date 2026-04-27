# email-classify

Classifies and labels incoming Gmail emails into preset categories using a cheap LLM via OpenRouter.

## Purpose

Automatically triage an AI-focused Gmail inbox by applying Gmail labels as emails arrive, so newsletters, tutorials, promos, and product releases are sorted without manual effort.

## Categories (Gmail Labels)

| Label | Description |
|---|---|
| `ai/news` | AI industry news, research papers, announcements from third parties |
| `ai/use-cases` | Real-world applications and case studies of AI |
| `ai/product-release` | New releases of **your own** products/services only |
| `ai/tutorial` | How-to guides, walkthroughs, educational content |
| `ai/sales-promo` | Sales emails, promotional offers, discounts |
| `non-ai` | Emails unrelated to AI |
| `ai/unclassified` | Could not be confidently assigned to any category |

> **Important distinction:** A third-party product launch is `ai/news`, not `ai/product-release`. Only releases from domains/products you own count as `ai/product-release`.

## Stack

- **Runtime:** n8n (self-hosted free tier or n8n.cloud free plan) or equivalent free workflow runner
- **Model:** OpenRouter — target cheapest capable model (e.g. `google/gemini-flash-1.5` or `mistralai/mistral-7b-instruct`)
- **Email source:** Gmail API (OAuth2) or Gmail node in n8n
- **Classification input:** Subject line + email snippet only (keep token usage minimal)
- **Output:** Gmail label applied via API

## Classification Logic

1. Fetch new/unread emails from inbox
2. Send `subject` + `body_snippet` (first ~200 chars) to the model with a structured prompt
3. Model returns one of the 7 category keys
4. Apply corresponding Gmail label (create label if it doesn't exist)
5. Add a `classified` label to prevent reprocessing

## Prompt Design

- System prompt lists all categories with clear definitions and the own-product distinction
- Ask for JSON output: `{"category": "<key>", "confidence": "high|low"}`
- If confidence is low, override to `ai/unclassified`
- Few-shot examples in the prompt for ambiguous cases (news vs product-release, tutorial vs use-case)

## Own Product Domains

List of domains/sender addresses that count as your own products (populate before deploying):

```
# example
myproduct.com
myapp.io
```

## Cost Target

- Subject + snippet ≈ 100-150 tokens per email
- Target model cost: < $0.001 per classification
- 1000 emails/month ≈ < $1

## Running

### n8n (preferred)

1. Import the n8n workflow JSON (`workflow.json`)
2. Set credentials: Gmail OAuth2, OpenRouter API key
3. Set trigger: Gmail trigger node (polling or webhook)
4. Configure own-product domains in the workflow config node

### Local / Cron (fallback)

```bash
pip install -r requirements.txt
cp .env.example .env  # fill in OPENROUTER_API_KEY, Gmail credentials
python classify.py
```

## Environment Variables

```
OPENROUTER_API_KEY=
GMAIL_CLIENT_ID=
GMAIL_CLIENT_SECRET=
GMAIL_REFRESH_TOKEN=
OWN_PRODUCT_DOMAINS=domain1.com,domain2.io
```

## Files

```
workflow.json        # n8n workflow export
classify.py          # standalone Python fallback script
prompt.txt           # classification system prompt
requirements.txt     # Python dependencies
.env.example         # env var template
```
