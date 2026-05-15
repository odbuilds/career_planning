# Career Planning — Claude Context

## Active pipeline

See [pipeline.md](pipeline.md) for jobs currently in screening or interview.
Update it manually when status changes or new interviews are booked.

## Key tools

- **JobPilot** — Streamlit job search tracker at `jobpilot/`. Launch with `/jobpilot` or `streamlit run jobpilot/app.py`.
- **CVs** — variants in `cvs/`. Three active: `cv_agentic.md`, `cv_cx.md`, `cv_consulting.md`.
- **Context** — `context/built.md` contains Oliver's project narratives used to ground cover letters.
- **Proficiently** — resume/cover letter tool at `proficiently/`.

## Discovery scripts

All run from `jobpilot/`:

| Script | Purpose |
|--------|---------|
| `scripts/discover_uk_remote.py` | 7-day run, all sources, UK + remote locations |
| `scripts/discover_uk_7day_noreed.py` | 7-day run, all sources except Reed, UK + remote |
| `scripts/discover_linkedin_1day.py` | LinkedIn only, 1-day age, UK + remote |
| `scripts/rescore_401_errors.py` | Rescore jobs that failed pipeline scoring with a 401 auth error |

## Interview prep

Prep docs live in `intv/`. Generate with `/intv-prep <JD URL or text>`.
