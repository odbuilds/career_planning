# email-classify

Classifies incoming Gmail emails into preset categories and applies labels automatically.
Runs on Google Apps Script — no server required.

## Setup (~20 minutes)

### 1. Create the Apps Script project

1. Go to [script.google.com](https://script.google.com) and click **New project**
2. Delete the default `Code.gs` content
3. Copy each `.gs` file from this repo into its own file in the editor (use the **+** button to add files):
   - `Config.gs`
   - `Prompt.gs`
   - `Code.gs`
   - `Telegram.gs`
4. Replace the contents of `appsscript.json` (Project Settings → edit manifest) with the file from this repo

### 2. Set Script Properties

Go to **Project Settings → Script Properties** and add:

| Key | Value |
|---|---|
| `OPENROUTER_API_KEY` | Your OpenRouter API key |
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token (from @BotFather) |
| `TELEGRAM_CHAT_ID` | Channel ID, e.g. `@mychannel` or `-1001234567890` |

### 3. Configure your own product domains

Open `Config.gs` and add your own product/service domains to the `OWN_DOMAINS` array:

```javascript
OWN_DOMAINS: [
  'myproduct.com',
  'myapp.io',
],
```

Emails from these domains can be classified as `ai/product-release`.
All other product launches go to `ai/news`.

### 4. Run setup

In the editor, select the `setup` function from the dropdown and click **Run**.
This creates all Gmail labels. Approve the OAuth permissions when prompted.

### 5. Add triggers

Go to **Triggers** (clock icon) and add two triggers:

| Function | Event source | Type | Frequency |
|---|---|---|---|
| `classifyEmails` | Time-driven | Minutes timer | Every 10 minutes |
| `sendDailySummary` | Time-driven | Day timer | 8am (your timezone) |

That's it. Emails in your inbox will be classified and labelled automatically.

---

## Gmail Labels

| Label | Description |
|---|---|
| `ai/news` | AI industry news, research, third-party announcements |
| `ai/use-cases` | Real-world AI applications and case studies |
| `ai/product-release` | Releases from your own products/domains only |
| `ai/tutorial` | How-to guides, walkthroughs, educational content |
| `ai/sales-promo` | Sales emails, discounts, promotional offers |
| `non-ai` | Emails unrelated to AI |
| `ai/unclassified` | Ambiguous — review manually |
| `classified` | Internal marker — added to every processed email |

---

## Telegram Bot Setup

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow the prompts → copy the **token**
3. Add the bot to your channel as an **admin**
4. Get the channel ID:
   - Public channel: use `@channelname`
   - Private channel: forward a message to [@userinfobot](https://t.me/userinfobot) to get the numeric ID
5. Add both values to Script Properties

---

## Model

Default: `google/gemini-flash-1.5` via [OpenRouter](https://openrouter.ai)

To switch models, update `MODEL` in `Config.gs`. Any OpenRouter model works.

Estimated cost: **< $0.05 / 1,000 emails**

---

## Files

```
Config.gs         Constants: model, labels, own domains, batch size
Prompt.gs         System prompt and user message builder
Code.gs           Classification logic, Gmail labelling, counter tracking
Telegram.gs       Daily summary trigger
appsscript.json   OAuth scopes and runtime config
README.md         This file
.env.example      Script Properties reference
```
