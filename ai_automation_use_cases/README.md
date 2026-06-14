# AI Automation Use Cases Library

A library of **100 AI automation opportunities** for companies with 50–100 employees.
Each document covers the business problem, automation overview, workflow stages,
tool recommendations with SMB pricing, implementation steps, real GitHub repos &
tutorials, challenges, KPIs, and an investment estimate.

---

## Departments Covered

| Department | Use Cases | Description |
|---|---|---|
| Finance | 25 | AP/AR automation, forecasting, expense management, compliance |
| HR | 25 | Recruiting, onboarding, performance, payroll, L&D |
| Operations | 20 | Supply chain, project management, quality control, facilities |
| IT | 10 | Helpdesk, security monitoring, asset management, infrastructure |
| Legal | 10 | Contract review, compliance monitoring, policy management |
| Customer Success | 5 | Ticket routing, churn prediction, NPS analysis |
| Marketing | 5 | Content generation, SEO, campaign analytics |

---

## Quick Start

### 1. Install dependencies

```bash
cd scripts
pip install -r requirements.txt
```

### 2. Set your API key

```bash
cp scripts/.env.example scripts/.env
# Edit scripts/.env and add your ANTHROPIC_API_KEY
```

### 3. Run the full library generation (~4–8 hours, ~$50–100 in API costs)

```bash
cd scripts
python orchestrator.py
```

### Common options

```bash
# Test a single department first
python orchestrator.py --dept finance

# Test a single use case
python orchestrator.py --id fin_001

# Quick smoke test (3 use cases)
python orchestrator.py --limit 3

# Resume an interrupted run
python orchestrator.py --resume

# Rebuild the index without re-running agents
python orchestrator.py --index-only
```

---

## Agent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     orchestrator.py                         │
│   Reads use_case_seeds.py → loops over 100 use cases        │
└──────────────────────┬──────────────────────────────────────┘
                       │  for each use case:
                       ▼
            ┌──────────────────────┐
            │   Research Agent     │  claude-opus-4-7
            │   + web_search       │  adaptive thinking
            │   + prompt cache     │  → business problem,
            │                      │    workflow stages,
            │                      │    tools & KPIs
            └──────────┬───────────┘
                       │  research_brief (JSON)
                       ▼
            ┌──────────────────────┐
            │ Implementation Agent │  claude-opus-4-7
            │   + web_search       │  → real GitHub repos,
            │   + prompt cache     │    Medium / Substack
            │                      │    tutorials,
            │                      │    code patterns
            └──────────┬───────────┘
                       │  impl_data (JSON)
                       ▼
            ┌──────────────────────┐
            │  Evaluation Agent    │  claude-opus-4-7
            │   + prompt cache     │  adaptive thinking
            │   (no web search)    │  scores C1–C8 (0-2 each)
            │                      │  pass if total ≥ 12/16
            └──────────┬───────────┘
                       │  eval_result (JSON)
                       │
                       │  if failed & retries remain:
                       │    inject feedback → retry Research
                       ▼
            ┌──────────────────────┐
            │     md_writer.py     │  renders full Markdown doc
            └──────────┬───────────┘
                       │
                       ▼
            use_cases/{dept}/{id}.md
```

---

## Output Structure

```
ai_automation_use_cases/
├── README.md                    ← this file
├── use_cases/
│   ├── index.md                 ← full index grouped by dept
│   ├── finance/
│   │   ├── fin_001.md
│   │   ├── fin_002.md
│   │   └── ...                  (25 files)
│   ├── hr/
│   │   └── ...                  (25 files)
│   ├── operations/
│   │   └── ...                  (20 files)
│   ├── it/
│   │   └── ...                  (10 files)
│   ├── legal/
│   │   └── ...                  (10 files)
│   ├── customer_success/
│   │   └── ...                  (5 files)
│   └── marketing/
│       └── ...                  (5 files)
└── scripts/
    ├── orchestrator.py          ← main entry point
    ├── agents.py                ← three Claude agents
    ├── md_writer.py             ← Markdown renderer
    ├── use_case_seeds.py        ← 100 use case definitions
    ├── requirements.txt
    ├── .env.example
    └── progress.json            ← auto-created; tracks completed IDs
```

---

## Each Use Case Document Contains

- **Business Problem** — exact pain point, time/cost wasted, who is affected
- **Automation Overview** — concise description of the full automation
- **Workflow Stages** — 4+ numbered stages with input/process/output tables
- **Tools & Technologies** — 5+ named tools with SMB pricing tiers
- **Implementation Steps** — 6+ concrete, actionable steps
- **Real-World Implementations** — GitHub repos (stars, key patterns) + articles
- **Challenges & Mitigations** — table of realistic hurdles and solutions
- **Metrics & KPIs** — 4+ KPIs with baseline vs. target values
- **Investment Estimate** — setup cost, monthly cost, break-even, FTE savings

---

## Evaluation Rubric

Each document is scored by the Evaluation Agent before being written:

| Criterion | Max | What's checked |
|---|---|---|
| C1 workflow_stages | 2 | ≥4 stages with input/process/output |
| C2 tools_and_tech | 2 | ≥4 specific named tools with pricing |
| C3 implementation | 2 | ≥5 concrete, actionable steps |
| C4 challenges | 2 | ≥3 challenges with mitigations |
| C5 metrics | 2 | ≥4 KPIs with baseline + target |
| C6 github_resources | 2 | ≥1 real GitHub resource |
| C7 tutorials | 2 | ≥2 tutorial/article resources |
| C8 investment | 2 | setup cost, monthly cost, break-even present |
| **Total** | **16** | **Pass threshold: ≥12** |

Documents that fail on the first pass are automatically retried (up to 2×)
with the evaluator's feedback injected as additional search context.
