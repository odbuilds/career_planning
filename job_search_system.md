# Job Search System — Oliver Day
*Last updated: 2026-04-03*

---

## North Star

**Get the right job offer, fast.** Everything in this system exists to serve that goal. The trap is spending two weeks building infrastructure before sending a single application. The rule: only build a component if the ROI is clear and the build time is bounded.

---

## Overview — Seven Pillars

1. **Strategy Lock** — position, target market, constraints
2. **Target Intelligence** — finding the right roles and companies
3. **CV & Cover Letter Factory** — fast, high-quality, tailored output
4. **Application Tracking** — nothing falls through the cracks
5. **Outreach Engine** — warm paths in, not cold queue submissions
6. **Email Monitoring & Response Management** — stay on top of inbound
7. **Dashboard** — situational awareness without overhead

---

## Pillar 1 — Strategy Lock

**Why first:** Every other component depends on this. Without a clear position, your CV tries to be for everyone, your cover letters are generic, your target list is unfocused, and your outreach has no hook. A locked position also means Claude can do more of the heavy lifting — it needs a spine to work from.

### 1a. The four decisions to make

These came out of prior strategy work and are still unresolved:

**Decision 1 — Employment type**
- Employed role (PAYE): stability, benefits, single focus
- Consulting/fractional: multiple clients, higher day rate, more control, more selling


**Decision 2 — Vertical focus**
- CX/contact centre AI: deep domain, clear ROI narrative, strong existing experience, smaller market
- Broader AI engineering: larger market, more competitive, harder to differentiate
- AI consulting and enablement

**Decision 3 — Primary position (pick one of three)**
- Agentic workflow/operations architecture: broad market, high demand, competitive
- AI evaluation & reliability: most defensible, most compounding, smaller but growing market
- CX AI transformation: most direct from background, clearest ROI story, more vertical-locked
- willing to go wider

**Decision 4 — Timing and constraints**
- Minimum acceptable salary UK 90k GBP - Serbia (paid as a consultant with lump sum taxation 5500 euro), other locations comparative to these values
- Geography: London, Cambridge, Norwich, Edinburgh, Spain, Scandinavia, Slovenia, Serbia, Italy  remote, 
- Full-time preferred

### 1b. Positioning statement (output of 1a)

> "I build production-grade agentic systems — evaluation frameworks, LLM pipelines, and multi-agent workflows — with a background shipping these in customer-facing environments at scale. I work best at the point where a team has moved past the POC and needs someone who can make it reliable, observable, and actually improve over time."

### 1c. Target role titles (output of positioning)

- AI/ML Engineer (Applied)
- Conversational AI Engineer
- AI Reliability / Evaluation Engineer
- LLM Platform Engineer
- Agentic Systems Engineer
- Head of AI (small company)
- AI Solutions Architect
- Generative AI Consultant
- CX AI Professional Services / Forward-deployed AI Engineer
- AI Transformation Lead / CX AI Transformation
- CX AI Product Manager
- Conversation Designer *(fallback only)*

---

## Pillar 2 — Target Intelligence

**Goal:** A continuously refreshed pipeline of 30–50 qualified opportunities. Quality filtered before you ever look at them.

### 2a. Job board strategy

Not all boards are equal. Prioritise by signal-to-noise ratio for your level and market.

| Board | Signal | Best for | Setup effort |
|---|---|---|---|
| LinkedIn Jobs | High | Mid-large companies, UK+remote | Low — alerts by keyword |
| Otta / Welcome to the Jungle | High | UK tech, culture-fit info | Low — set preferences once |
| Cord.co | High | UK tech, direct to hiring manager | Low — good profile needed |
| WorkAtAStartup (YC) | High | AI-native startups, global | Low — one-time filter setup |
| Ashby job boards | Medium | AI-first companies (many use Ashby ATS) | Medium — manual monitoring |
| Greenhouse / Lever job boards | Medium | Mid-market tech | Low — Google alerts |
| Wellfound (AngelList) | Medium | Startups, equity-focused roles | Low |
| Twitter/X #hiring | Low-medium | Real-time, informal, AI community | Low — search saved |
| Substack newsletters | Medium | Curated, less competition | Low — subscribe once |
| Company career pages (direct) | High | Dream companies | Medium — manual or monitored |

**Alert setup per board:**
- LinkedIn: 3–5 keyword alerts (exact role titles from 1c), daily digest
- Otta: preferences set to your vertical + seniority
- Cord: complete profile fully (they match algorithmically)
- YC: filter by AI/ML + remote/UK
- Google Alerts: `"{company name}" "we're hiring" OR "job opening"` for 10–15 target companies

### 2b. Company target list

Build a list of 30–50 companies to proactively target, separate from reactive job board browsing. These are companies you'd want to work for even if they haven't posted a specific role.

**Criteria:**
- AI-native or AI-first product (not "adding AI to existing product")
- Has deployed LLM/agent systems in production (look for engineering blog posts, conference talks)
- <500 people (your impact will be higher; politics lower)
- UK-based or remote-friendly
- Not pure research — applied, product-facing AI

**Sources for building this list:**
- YC companies (W23, S23, W24, S24, W25 batches) — filter AI + UK/remote
- ARIA portfolio (UK AI-focused fund)
- Notion AI, Hebbia, Cohere, Anthropic partner companies
- Companies hiring from the AI Twitter community
- Companies whose engineering blogs you read / find interesting
- Companies presenting at AI Engineer World's Fair, AI Engineer London, etc.

**Output:** `applications/target_companies.md`

Schema:
```
| Company | What they do | Why relevant to you | Size | Remote? | Source | Status |
```

### 2c. Role qualification criteria

Before adding a role to your tracker, run it through this filter. Takes 2 minutes.

**Must have (any one):**
- LLM/agent systems in production or near-production
- Evaluation, observability, or quality systems mentioned
- Conversational AI / voice AI / NLU
- Multi-agent or workflow orchestration

**Strong positive signals:**
- Mentions specific tools: LangChain/LangGraph, Anthropic/OpenAI, LangSmith, Weights & Biases
- Engineering blog exists and is technical
- Role asks for "production experience" not just "familiarity"
- Team size suggests real ownership (not a cog in a large ML org)

**Red flags:**
- "AI strategy" without "engineering" or "implementation"
- "POC development" as the main output (you want to ship, not prototype)
- Pure research or academia
- "Prompt engineer" as the title
- Large enterprise where you'd be in an AI centre of excellence doing governance

### 2d. Automation: role discovery pipeline (optional, build later)

A lightweight n8n workflow that aggregates job postings from multiple sources into one place.

**Architecture:**
```
[LinkedIn RSS feed] ─┐
[Otta RSS/scrape]  ──┤
[WorkAtAStartup]   ──┼──> [n8n aggregator] ──> [filter by keywords] ──> [Google Sheet / MD file]
[Google Alerts]    ──┤
[Twitter search]   ──┘
```

**Reality check:** RSS feeds and APIs exist for some of these, scraping is fragile for others. The manual version (checking boards daily, 15 min) may have better ROI than building this automation. Build it only if daily checking becomes a real friction point.

---

## Pillar 3 — CV & Cover Letter Factory

**Principle:** One master CV plus modular blocks. Cover letters generated by Claude, reviewed by you. Total time per application: <30 minutes including review.

### 3a. Master CV

You already have drafts: `cv_draft.md`, `cv_healthtech.md`.

**What needs to happen:**
- Lock the structure once Position is decided (Pillar 1)
- ATS-safe format (no tables, no columns, no headers as images)
- 2 pages max, PDF export
- Opening summary is swappable (the modular block)
- Skills section is swappable
- Experience bullets remain stable; reordering is the main tailoring

**Export pipeline:**
- Write in Markdown
- Pandoc → PDF (clean, minimal, professional)
- Or: Markdown → simple HTML template → print to PDF via browser
- Keep source in Markdown; never edit the PDF directly

### 3b. Modular block library

A set of pre-written, pre-approved components that get assembled per application. Writing these once means every application can be assembled in minutes.

**Directory:** `cv_blocks/`

Files to create:

| File | Contents | Length |
|---|---|---|
| `summary_agentic.md` | 3-line summary for agentic/workflow roles | 60 words |
| `summary_eval.md` | 3-line summary for eval/reliability roles | 60 words |
| `summary_cx.md` | 3-line summary for CX transformation roles | 60 words |
| `projects_full.md` | All 6 projects, full bullets | As needed |
| `projects_short.md` | Top 5 projects, one-liner each | 5 lines |
| `projects_agentic.md` | Projects selected/weighted for agentic roles | As needed |
| `projects_eval.md` | Projects selected/weighted for eval roles | As needed |
| `skills_technical.md` | Full stack with proficiency indicators | As needed |
| `skills_domain.md` | Domain expertise bullets (CX, NLU, eval) | As needed |
| `achievements.md` | Quantified outcomes across all roles | As needed |

**Process:** Write these once, maintain them. When you build something new, add it here immediately.

### 3c. Cover letter generation script

**What it does:** Takes a JD + company context, reads from your block library, produces a first-draft cover letter in your voice.

**Input (three options):**
1. Paste JD text directly
2. Provide URL (script fetches and extracts)
3. Provide company name + role title (script does a web search)

**Output:** `applications/{company}_{role}_cover_letter.md` — 250 words, ready for your review

**Script design:**

```python
# scripts/cover_letter_gen.py
# Usage: python cover_letter_gen.py --company "Acme" --role "AI Engineer" --jd "path/to/jd.txt"
#        python cover_letter_gen.py --company "Acme" --role "AI Engineer" --jd-url "https://..."

# What it does:
# 1. Load JD (from file, URL, or search)
# 2. Load relevant cv_blocks based on role type (auto-detect or flag)
# 3. Call Claude API with structured prompt
# 4. Extract 3 specific matches between JD and Oliver's background
# 5. Draft 250-word cover letter grounded in specific projects
# 6. Output to applications/ directory
# 7. Print to terminal for quick review
```

**Prompt design principles:**
- Ground every claim in a specific named project
- Match JD language without keyword stuffing
- No filler ("I am passionate about", "I would love the opportunity")
- End with a specific why-this-company hook
- Keep it under 250 words — recruiters do not read long cover letters

**Model:** Claude (you have API access; this is a natural use case)

### 3d. CV tailoring script

Same architecture as 3c. Given a JD, reorders and reweights your existing bullets to match — does not rewrite from scratch.

**What it changes:**
- Swaps in the most relevant summary block
- Reorders experience bullets to lead with most relevant
- Adjusts skills section emphasis
- Does not invent bullets or fabricate experience

**What it does not change:**
- Core experience bullets (these should be stable and honest)
- Employment history structure
- Dates, companies, titles

**Output:** `applications/{company}_{role}_cv.md` — ready for your review and PDF export

### 3e. Quality gate (your review, not skippable)

Both scripts produce drafts. You review before anything goes out. Checklist:

- [ ] All project references are accurate and I can speak to them
- [ ] No claims I can't back up in an interview
- [ ] Matches the actual role (not a generic letter)
- [ ] Reads like me, not like an AI wrote it
- [ ] PDF exports cleanly, no formatting breakage

**Time budget:** 10 min per cover letter, 5 min per CV check. If it's taking longer, the script prompt needs improving.

---

## Pillar 4 — Application Tracking

**Philosophy:** The simplest system you will actually use beats the most powerful system you won't. Start with flat markdown files. Add complexity only if you hit real friction.

### 4a. Applications tracker

**File:** `applications/index.md`

Schema:
```markdown
| Company | Role | Source | Applied | Status | Next action | Due | Notes |
```

**Statuses (linear pipeline):**
- `target` — identified, not yet applied
- `applied` — submitted, awaiting response
- `screening` — recruiter/HR screen scheduled or done
- `interview` — technical or hiring manager interview stage
- `final` — final round
- `offer` — offer received
- `rejected` — closed, no offer
- `withdrawn` — removed yourself

**Rules:**
- One row per application
- Update same day as status change
- "Next action" column is always filled in — never leave it blank
- Archive rejected/withdrawn to a separate section, don't delete (useful for patterns)

### 4b. Next actions list

**File:** `applications/next_actions.md`

Flat list, sorted by urgency. This is your daily to-do list for job search.

```markdown
# Next Actions

## Today
- [ ] Follow up with Quadrivia recruiter (applied 2026-04-01, no update)
- [ ] Send cover letter to Acme AI (draft ready, needs 10 min review)

## This week
- [ ] Set up LinkedIn alerts for: "AI Engineer", "Conversational AI Engineer", "Agentic Systems"
- [ ] Complete Cord.co profile
- [ ] Build target company list (first 20 companies)

## Backlog
- [ ] Build cover letter generation script
- [ ] Set up Gmail label + n8n trigger
```

Review this every morning. Add items same day as they arise.

### 4c. Skills gap tracker

Already exists: `skills_gap_tracker.md`

Keep updating this as you see patterns across JDs. It tells you where to spend learning time and what to be honest about in interviews.

### 4d. Optional: move to a lightweight database later

If you end up with >50 applications and the markdown file becomes unwieldy, options:
- Teal (free job tracker, browser extension)
- Huntr (similar, slightly more visual)
- Notion database (if you already use Notion)
- Airtable (overkill unless you're doing fractional/consulting with multiple pipelines)

Avoid these until you actually need them.

---

## Pillar 5 — Outreach Engine

**Why this matters:** A warm introduction or direct message to a hiring manager converts at 3–5x the rate of a cold queue submission through an ATS. At your level, relationship-driven application is the highest-leverage activity.

### 5a. LinkedIn warm outreach (primary channel)

You already built a 15k-profile LinkedIn automation with 70% connection rate. Apply the same thinking at a much smaller, higher-quality scale.

**Target:** Hiring managers, AI leads, and technical co-founders at target companies — not recruiters (yet).

**Volume:** 5–10 connection requests per day maximum. Quality, not spray.

**Message sequence:**

*Connection request (note — 300 chars max):*
> "Hi [Name] — I've been following [Company]'s work on [specific thing]. I'm an AI engineer with a background in [relevant area] exploring new roles. Would be good to connect."

*Follow-up message (3–5 days after connect):*
> "Thanks for connecting. I've been building [specific relevant thing] and [Company]'s approach to [X] resonates with how I think about [Y]. Are you hiring on the [area] side, or would you be the right person to point me to?"

**What not to do:**
- Don't lead with "I'm looking for a job" — lead with relevance
- Don't send a CV unprompted
- Don't send a wall of text
- Don't automate the messages themselves — personalisation is the point

**Tracking:** Add a `outreach` section to `applications/index.md` or a separate `applications/outreach.md`

### 5b. n8n automation for LinkedIn outreach (light assist)

Not full automation — LinkedIn detects and blocks that at scale. Instead, n8n assists:

**What to automate:**
- Pull your target company list, cross-reference with LinkedIn company pages
- Find AI leads/engineering leads at each company (LinkedIn search, manual step)
- Queue connection requests into a daily list (5–10 per day)
- Track sent/connected/replied in a simple log

**What stays manual:**
- The actual personalised note
- The follow-up message
- Any substantive conversation

### 5c. Recruiter network (separate strategy)

Specialist tech recruiters are a different channel from direct outreach. They're useful for:
- Roles not publicly advertised
- Companies where you don't have a direct in
- Market intelligence (what companies are hiring, what salary ranges look like)

**Target:** 5–10 specialist recruiters in AI/ML/LLM space in your market.

*Finding them:*
- Search LinkedIn: "AI recruiter London" / "ML engineer recruiter UK"
- Ask peers who placed them recently
- Note which recruiters post good AI roles in your feed

*Outreach message shape:*
> "Hi [Name] — I'm an AI engineer with [X years] building [LLM pipelines / agentic systems / etc.]. I'm actively exploring new roles and specialise in [position]. Happy to share my CV — do you work in this space?"

**One message each, no follow-up if no reply within 2 weeks. Move on.**

### 5d. Community presence (passive pipeline)

Not automatable, but compounds over time:

- **AI Engineer Discord / Slack communities** — be visible, answer questions, mention you're open to roles
- **Twitter/X** — post about what you're building; hiring managers will find you
- **GitHub** — your projects are visible; keep them up to date
- **LinkedIn posts** — one post per week about something you've built or learned; "open to work" quietly visible to recruiters

---

## Pillar 6 — Email Monitoring & Response Management

**Goal:** Zero missed responses. All job-related emails categorised, tracked, and actioned within 24 hours.

### 6a. Gmail setup (do this immediately)

**Step 1: Create a label** — `job-search` in Gmail

**Step 2: Create filters to auto-label**
Senders/subjects that should auto-apply the label:
- From domains: `greenhouse.io`, `lever.co`, `ashbyhq.com`, `workable.com`, `bamboohr.com`, `smartrecruiters.com`, `jobvite.com`, `taleo.net`
- Subject contains: "your application", "application received", "interview", "next steps", "we reviewed your", "we're moving forward", "unfortunately"
- Any email where you CC'd or BCC'd a specific tracking address (see 6b)

**Step 3: Add a `job-search/action-needed` sub-label**
Manually apply this to anything requiring a response. Clear it when actioned.

### 6b. n8n email monitoring workflow

**What it does:**
- Trigger: new email with `job-search` label (Gmail trigger in n8n)
- Action: classify the email type (acknowledgement / screen request / interview invite / rejection / other)
- Action: append a row to your applications tracker with the classification and timestamp
- Action: if "action needed" (screen request, interview invite), send you a push notification or add to `next_actions.md`

**Classification prompt (Claude node in n8n):**
```
Classify this job search email into one of:
- application_acknowledgement
- recruiter_screen_request
- interview_invite
- rejection
- offer
- general_info
- action_needed_other

Email: {email_body}

Return JSON: {"type": "...", "company": "...", "urgency": "high/medium/low", "summary": "one line"}
```

**Output:** Appends to a Google Sheet or local JSON file that feeds your dashboard.

### 6c. Response time targets

| Email type | Target response time |
|---|---|
| Recruiter screen request | Same day, within 4 hours if possible |
| Interview invite | Same day |
| Offer | Acknowledge same day; take time to decide |
| Application acknowledgement | No response needed |
| Rejection | Optional: brief thank you (keeps relationship warm) |

### 6d. Weekly digest (n8n cron)

Every Monday at 9am, n8n runs a summary:

```
Job Search Weekly Digest — week of [date]

Applications sent this week: N
Total active pipeline: N
Action needed: [list]
Stale (>14 days, no update): [list]
Interviews this week: [list]
```

Output options: email to yourself, append to a weekly log file, Slack/Telegram message.

---

## Pillar 7 — Dashboard

**Philosophy:** Start with the minimum. Add a visual layer only when the text files create real friction.

### 7a. Level 1 — Markdown files (start here)

Two files, reviewed daily:
- `applications/next_actions.md` — what to do today
- `applications/index.md` — full pipeline view

Five minutes every morning. This is enough to run a focused job search.

### 7b. Level 2 — Google Sheets (add if markdown gets unwieldy)

When you have >20 active applications, a spreadsheet is easier to scan than a markdown table.

**Sheets:**
1. `Applications` — main tracker, filterable by status
2. `Outreach` — LinkedIn and email outreach log
3. `Target Companies` — target list with status
4. `Weekly metrics` — trend over time (applications/week, response rate, conversion at each stage)

**Automation:** n8n writes to Sheets directly via Google Sheets node. No manual copy-paste.

### 7c. Level 3 — Local HTML dashboard (build if you want a visual)

A single static HTML file, no server needed. Reads from a JSON applications log (written by n8n).

**What it shows:**
- Kanban-style pipeline: target → applied → screen → interview → offer
- Weekly application count (bar chart)
- Response rate by source (which boards convert best)
- Days since last activity per application (flag stale ones)

**Build cost:** 2–3 hours with Claude writing the HTML/JS. Only worth it if you're managing 30+ active applications.

### 7d. Metrics to track (when you have enough data)

- Applications per week
- Source conversion rate (which boards lead to screens)
- Cover letter response rate (with script vs without)
- Outreach conversion rate (connection request → reply)
- Time from apply to first response (by company size, source)

These patterns tell you where to invest more effort.

---

## Build Sequence — Phased Rollout

The danger is building the machine instead of using it. This sequence keeps the job search active from Day 1.

### Week 1 — Foundation (job search active by end of week)

| Day | Task | Time | Pillar |
|---|---|---|---|
| Mon | Resolve four strategic decisions; write positioning statement | 2h | 1 |
| Mon | Set up Gmail label + filters | 30m | 6 |
| Tue | Finalise master CV based on locked position | 3h | 3 |
| Tue | Set up LinkedIn job alerts (3–5 keyword alerts) | 30m | 2 |
| Tue | Set up applications/index.md and next_actions.md | 30m | 4 |
| Wed | Sign up for Otta, Cord, WorkAtAStartup, set preferences | 1h | 2 |
| Wed | Write cv_blocks/ — summary variants + skills | 2h | 3 |
| Thu | Build cover letter generation script | 3h | 3 |
| Thu | Apply to first 3–5 roles | 2h | 3+4 |
| Fri | Build target company list (first 20 companies) | 2h | 2 |
| Fri | Begin LinkedIn warm outreach (5 connection requests) | 30m | 5 |

**End of Week 1:** Active applications in flight, system running, cover letter script working.

### Week 2 — Outreach + Monitoring

| Day | Task | Time | Pillar |
|---|---|---|---|
| Mon | Set up n8n email monitoring workflow | 2h | 6 |
| Mon–Fri | 5–10 LinkedIn outreach per day | 30m/day | 5 |
| Tue | Contact 5–10 specialist recruiters | 1h | 5 |
| Wed | Apply to next 5–10 roles | 3h | 3+4 |
| Thu | Complete target company list to 40–50 | 1h | 2 |
| Fri | Weekly review — update tracker, check metrics | 30m | 4+7 |

### Week 3 onwards — Steady state

**Daily (15–20 min):**
- Check next_actions.md
- Process job-search emails
- Send 5 LinkedIn outreach (until target list exhausted)

**Weekly (1–2 hours):**
- Apply to 5–10 new roles
- Update tracker
- Weekly digest review
- Adjust focus based on response patterns

**Build when needed (not before):**
- Google Sheets view — if markdown gets unwieldy (>30 applications)
- n8n role aggregator — if daily board checking is real friction
- HTML dashboard — if you want visual pipeline view
- LinkedIn Easy Apply automation — if volume strategy needed

---

## Tools & Stack

| Component | Tool | Why |
|---|---|---|
| CV writing | Markdown + Pandoc | ATS-safe, version-controllable, clean PDF |
| Cover letter generation | Python + Claude API | Your existing stack |
| Application tracking | Markdown files → Google Sheets | Start simple, upgrade if needed |
| Job alerts | LinkedIn, Otta, Google Alerts | Native alerting is sufficient |
| Outreach tracking | `applications/outreach.md` | Flat file, simple |
| Email monitoring | Gmail labels + n8n | Your existing n8n, low friction |
| Weekly digest | n8n cron | Reuse existing workflow engine |
| Dashboard (later) | Static HTML + JSON | No server, low maintenance |
| Form filling | Simplify.jobs extension | Browser extension, free |
| LinkedIn Easy Apply | LinkedIn native | For volume plays on strong-match roles |

---

## What NOT to Build

These are tempting but not worth the time at this stage:

| Idea | Why to skip for now |
|---|---|
| Full ATS form-scraping auto-apply | High build cost, fragile, low quality — wrong for senior roles |
| Custom job aggregator / scraper | Alerts on existing boards is sufficient; scrapers break constantly |
| Resume parser / JD matcher scoring | Manual review with the script is faster to build and more accurate |
| Slack notification bot | Email digest is enough; another integration to maintain |
| LinkedIn automation at scale | You're targeting quality, not volume; and LinkedIn detects it |
| Complex database with tags/categories | Markdown → Sheets progression is sufficient |
| Interview prep AI (yet) | Not needed until you have interviews; build it then |

---

## Open Questions (to discuss)

These need answers before the system can be fully configured:

1. **Strategic position:** Which of the three positions is primary? (agentic / eval / CX transformation)
2. **Employment type:** Employed role vs consulting/fractional?
3. **Geography:** London, remote, or flexible?
4. **Runway:** How many months before income pressure? This affects urgency and selectivity.
5. **LinkedIn premium:** Do you have it? Useful for InMail + who-viewed-your-profile for outreach.
6. **n8n instance:** Self-hosted or cloud? (affects which Gmail integrations are available)
7. **Email provider:** Gmail confirmed? (the monitoring architecture assumes Gmail)
8. **Current CV status:** Is `cv_draft.md` the most current version, or has it been updated since?

---

## Files Structure (target state)

```
career_planning/
├── job_search_system.md              ← this file (strategy + plan)
├── skills_gap_tracker.md             ← active, keep updating
│
├── cvs/
│   ├── cv_draft.md                   ← master CV (Markdown source)
│   ├── cv_healthtech.md              ← health tech variant
│   └── cv_blocks/
│       ├── summary_agentic.md
│       ├── summary_eval.md
│       ├── summary_cx.md
│       ├── projects_full.md
│       ├── projects_agentic.md
│       ├── projects_eval.md
│       ├── projects_short.md
│       ├── skills_technical.md
│       ├── skills_domain.md
│       └── achievements.md
│
├── context/
│   └── built.md                      ← projects and experience reference
│
├── learning/
│   └── learning_list.md
│
├── archive/                          ← old strategy notes and research
│
├── scripts/
│   ├── cover_letter_gen.py           ← Claude-powered CL generator
│   └── cv_tailor.py                  ← CV reweighting script
│
└── applications/
    ├── index.md                      ← main tracker
    ├── next_actions.md               ← daily action list
    ├── target_companies.md           ← proactive target list
    ├── outreach.md                   ← LinkedIn + email outreach log
    └── {company}_{role}_cl.md        ← generated cover letters
```
