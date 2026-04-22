# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

JobPilot is a personal job search management tool for Oliver Day. It is a local Streamlit multi-page app backed by SQLite. Oliver applies to jobs manually — there is no form automation. The system discovers jobs, recommends CVs, generates cover letters via Claude API, tracks application status, and processes job-related emails.

## Running the app

All commands run from `jobpilot/`:

```bash
# Start the UI
streamlit run app.py

# Test core logic without starting Streamlit
python3 -c "from core.config import load_config; from core import database as db; db.init_db(); print('OK')"

# Test scoring
python3 -c "
import sys; sys.path.insert(0, '.')
from core.config import load_config; from core.scoring import score_job, recommend_cv
cfg = load_config()
print(score_job('agentic LLM multi-agent evaluation production', cfg))
print(recommend_cv('NHS EHR clinical patient', cfg))
"

# Test cover letter generation (requires ANTHROPIC_API_KEY in .env)
python3 -m generation.cover_letter

# Run email ingest CLI
python3 scripts/ingest_email.py --gmail-id "abc" --subject "Interview" \
  --sender "hr@co.com" --classification "interview_invite" \
  --company "Acme" --status-update "interview" --update-last-check
```

## Environment

Copy `.env.example` to `.env` and fill in:
- `ANTHROPIC_API_KEY` — required for cover letter generation
- `ADZUNA_APP_ID` + `ADZUNA_API_KEY` — free at developer.adzuna.com
- `REED_API_KEY` — free at reed.co.uk/developers

All imports assume the working directory is `jobpilot/`. Each page and script does `sys.path.insert(0, ...)` to add the parent.

## Architecture

```
jobpilot/
├── app.py                  # Streamlit entrypoint — init_db(), sidebar, home splash
├── profile.yaml            # ALL user config: scoring weights, CV paths, sources registry
├── pages/
│   ├── 1_pipeline.py       # Kanban view: active stages + backlog + closed
│   ├── 2_jobs_list.py      # Filterable table, Add Job form, Discover Jobs form, Generate CL
│   └── 3_job_detail.py     # 4 tabs: Application, Emails, Interviews, Notes
├── core/
│   ├── config.py           # Loads profile.yaml + .env → Config object (singleton, cached)
│   ├── database.py         # All SQLite CRUD — no ORM, WAL mode, context manager pattern
│   ├── models.py           # Dataclasses + constants (PIPELINE_STAGES, INTERVIEW_TYPES, etc.)
│   └── scoring.py          # score_job(), recommend_cv(), explain_cv_recommendation()
├── generation/
│   ├── cover_letter.py     # Claude API call — reads CV file + built.md, returns plain text
│   └── cv_recommendation.py # Reads CV files from disk; thin wrapper over scoring.py
├── discovery/              # One module per source — all stub files, not yet implemented
└── scripts/
    └── ingest_email.py     # CLI called by Claude during "check job emails" sessions
```

**Data flow:**
1. Jobs enter via "Add Job" form (manual) or `discovery/runner.py` (automated)
2. `scoring.py` scores each JD and recommends a CV variant — pure functions, no I/O
3. Cover letters are generated on demand via `generation/cover_letter.py` → stored in `materials` table
4. Email check: Oliver asks Claude Code "check my job emails" → Claude uses Gmail MCP → calls `scripts/ingest_email.py` → DB updated
5. All state lives in `jobpilot.db` (SQLite, WAL mode)

## Key design decisions

**Config is the single source of truth.** `profile.yaml` controls scoring weights, CV variant keywords, the discovery sources registry, target countries, and salary floors. Change behaviour by editing the YAML, not the code.

**Sources are config-driven.** The discovery sources registry in `profile.yaml` under `discovery.sources` lists all sources with `enabled: true/false`. The runner (not yet built) uses `importlib` to load only enabled source modules. Adding a new source = add a YAML entry + drop a `{slug}_source.py` in `discovery/`. No runner changes needed.

**Database connections are not shared.** Each `database.py` function opens and closes its own connection via `get_conn()` context manager. Do not pass connections between functions.

**CV recommendation is keyword-based, not LLM-based.** `recommend_cv()` counts healthtech keyword hits against a threshold (default 2). "NHS" and "EHR"/"EMR" count double as strong signals. Override is always available on the Job Detail page.

**Cover letters use `built.md` as grounding.** `career_planning/context/built.md` contains Oliver's actual project narratives. The prompt instructs Claude to name specific projects from this file and connect them to the JD. This prevents fabrication.

**Email ingest is manually triggered.** There is no daemon. Oliver triggers email checking as a Claude Code session using the Gmail MCP. Claude calls `scripts/ingest_email.py` once per email. The `gmail_message_id UNIQUE` constraint makes re-runs safe.

## Checking job emails (Gmail MCP workflow)

When Oliver says "check my job emails" or similar, follow these steps exactly:

**1. Fetch labelled emails**
Use the Gmail MCP to search for messages with the `application-response` label that haven't been processed yet:
- Query: `label:application-response`
- Fetch up to 50 messages; read subject, sender, received date, and body for each

**2. Skip already-ingested emails**
The DB deduplicates on `gmail_message_id`. You can attempt to ingest all results — duplicates will return `{"ok": false, "reason": "duplicate"}` and can be silently skipped. Alternatively, check `db.get_last_email_check()` to filter by date before ingesting.

**3. Classify each email**
For each unprocessed email, classify it into one of:
- `interview_invite` — invited to interview or asked to book a slot
- `recruiter_screen_request` — recruiter asking to schedule a call
- `offer` — job offer received
- `application_acknowledgement` — auto-confirm that application was received
- `rejection` — application unsuccessful
- `action_needed` — requires a response or action (e.g. complete a test)
- `general_info` — anything else job-related

**4. Match to a job**
Try to identify which job the email relates to by company name. Pass `--company "Acme Corp"` and the script will auto-match to the closest job in the DB. If confident of the job ID, pass `--job-id N` directly.

**5. Call ingest_email.py for each email**
Run from `jobpilot/`:
```bash
python scripts/ingest_email.py \
  --gmail-id "<message_id>" \
  --received-at "<ISO timestamp>" \
  --subject "<subject>" \
  --sender "<sender email>" \
  --classification "<classification>" \
  --body "<plain text body>" \
  --company "<company name>" \
  [--status-update "<new_status>"]  # only if classification warrants a pipeline move
```

Status updates to apply automatically:
- `interview_invite` → set status to `interview`
- `offer` → set status to `offer`
- `rejection` → set status based on the job's **current** status (company passed at that stage):
  - current status `applied` or `discovered` → `passed-application`
  - current status `screening` → `passed-screening`
  - current status `interview` → `passed-interview`
  - current status `final` → `passed-final`
  - if current status is unknown or already closed → `passed-application` as fallback
- `recruiter_screen_request` → set status to `screening`
- All others → no status change

**Status semantics:**
- `rejected` = Oliver chose not to pursue (he rejected it)
- `passed-*` = company declined at that stage (they passed on Oliver)

**6. Update last-check timestamp**
After processing all emails, run:
```bash
python scripts/ingest_email.py --update-last-check
```

**7. Report back**
Tell Oliver: how many emails found, how many new vs duplicate, any pipeline status changes made, and flag anything that needs his attention (interview invites, offers, action needed).

## Database schema (5 tables)

`jobs` — core record, one row per opportunity  
`materials` — CV and cover letter content (type: `cv` | `cover_letter`); `save_material()` replaces existing on type conflict  
`interviews` — one row per interview round; `notes` is free text  
`emails` — classified emails from Gmail; `gmail_message_id` is UNIQUE  
`meta` — key/value store; currently used for `last_email_check_at`

## CV files

Six CV variants live outside `jobpilot/` in `../cvs/`:

| File | Display name | Triggers on |
|---|---|---|
| `cv_cx.md` | Conversational AI / CX | Fallback — also: NLU, contact centre, Dialogflow, chatbot, conversational AI |
| `cv_agentic.md` | Agentic / LLM Engineering | LangGraph, multi-agent, agentic, workflow orchestration |
| `cv_consulting.md` | AI Consulting / Solutions Architect | consultant, fractional, solutions architect, AI enablement |

Paths are resolved relative to `profile.yaml` location in `core/config.py`. `context/built.md` is similarly resolved.

The recommender (`scoring.py:explain_cv_recommendation`) scores every non-fallback variant by keyword hits, with `strong_keywords` counting double. Highest scorer above `threshold` wins. All weights, keywords, and thresholds are in `profile.yaml` — no code changes needed to tune or add a variant.

## Discovery

Entry point: `discovery/runner.py` → `run_discovery(slugs, keywords, location, days, config)`.
Returns `{"new": N, "skipped": N, "errors": [...]}`.

Source module contract: each `discovery/{slug}_source.py` must implement:
```python
def fetch(keywords: str, location: str, days: int, config: Config, source_cfg: dict = None) -> list[dict]:
    # Returns list of normalised job dicts:
    # {company, role, url, jd_text}
    # runner adds: source, score, recommended_cv, status
```

Implemented sources:

| Slug | Module | Method | Notes |
|------|--------|--------|-------|
| linkedin | linkedin_source | JobSpy scraping | |
| indeed / glassdoor / google | jobspy_source | JobSpy | uses source_cfg["jobspy_site"] |
| adzuna | adzuna_source | REST API | loops over all target_countries in config |
| reed | reed_source | REST API | UK only |
| hn | hn_source | HN Algolia + Firebase API | parses monthly Who is Hiring thread |
| remotive | remotive_source | Public API | |
| greenhouse | greenhouse_source | Public ATS APIs | Greenhouse/Lever/Ashby for watched_companies |
| cvlibrary | cvlibrary_source | HTML scraping | selectors may drift |
| aijobs | aijobs_source | JSON API | falls back to scraping if endpoint changes |
| remoterocketship | remoterocketship_source | HTML scraping | selectors may drift |
| jobbland | jobbland_source | HTML scraping | Sweden only, selectors may drift |
| trueup | trueup_source | — | disabled — returns 403, needs investigation |
