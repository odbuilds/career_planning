import sys
from pathlib import Path
from datetime import date

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import load_config
from core import database as db
from core.models import PIPELINE_STAGES, ACTIVE_STAGES, CLOSED_STAGES

config = load_config()
db.init_db()

st.set_page_config(layout="wide")
st.header("📋 Pipeline")

jobs = db.get_jobs()

if not jobs:
    st.info("No jobs tracked yet. Go to **Jobs** to add your first role.")
    st.stop()

# ── Filters ───────────────────────────────────────────────────────────────────
with st.expander("Filters", expanded=True):
    fc1, fc2, fc3 = st.columns(3)

    all_stages = PIPELINE_STAGES
    default_stages = ACTIVE_STAGES
    selected_stages = fc1.multiselect(
        "Status",
        options=all_stages,
        default=default_stages,
        format_func=str.title,
    )

    all_sources = sorted({j.get("source", "manual") or "manual" for j in jobs})
    selected_sources = fc2.multiselect("Source", options=all_sources, default=all_sources)

    score_min = fc3.slider("Min score", min_value=0, max_value=10, value=0)

# ── Apply filters ─────────────────────────────────────────────────────────────
filtered = [
    j for j in jobs
    if j.get("status", "discovered") in selected_stages
    and (j.get("source", "manual") or "manual") in selected_sources
    and (j.get("score") or 0) >= score_min
]

st.caption(f"Showing {len(filtered)} of {len(jobs)} jobs")

if not filtered:
    st.info("No jobs match the current filters.")
    st.stop()

# ── Sort ──────────────────────────────────────────────────────────────────────
sort_col, _ = st.columns([2, 6])
sort_by = sort_col.selectbox(
    "Sort by",
    options=["Score ↓", "Applied date ↓", "Company A–Z", "Status"],
    index=2,
    label_visibility="collapsed",
)

today = date.today()

def applied_days(job):
    raw = job.get("applied_at") or job.get("created_at") or ""
    try:
        return (today - date.fromisoformat(raw[:10])).days
    except (ValueError, TypeError):
        return 9999

if sort_by == "Score ↓":
    filtered.sort(key=lambda j: j.get("score") or 0, reverse=True)
elif sort_by == "Applied date ↓":
    filtered.sort(key=applied_days)
elif sort_by == "Company A–Z":
    filtered.sort(key=lambda j: (j.get("company") or "").lower())
else:
    filtered.sort(key=lambda j: PIPELINE_STAGES.index(j.get("status", "discovered")))

# ── Table header ──────────────────────────────────────────────────────────────
hc1, hc2, hc3, hc4, hc5, hc6 = st.columns([3, 3, 1.5, 1.5, 1, 1])
hc1.markdown("**Company**")
hc2.markdown("**Role**")
hc3.markdown("**Status**")
hc4.markdown("**CV**")
hc5.markdown("**Score**")
hc6.markdown("")

st.divider()

# ── Rows ──────────────────────────────────────────────────────────────────────
for job in filtered:
    c1, c2, c3, c4, c5, c6 = st.columns([3, 3, 1.5, 1.5, 1, 1])

    score = job.get("score") or 0
    badge = "🟢" if score >= 7 else "🟡" if score >= 4 else "🔴"
    status = job.get("status", "discovered")
    cv_name = config.get_cv_display_name(job.get("recommended_cv", "cv_draft"))
    days = applied_days(job)
    days_str = f"{days}d ago" if days < 9999 else "—"

    c1.write(f"**{job['company']}**")
    c2.write(job["role"])
    c3.write(status.title())
    c4.write(cv_name)
    c5.write(f"{badge} {score}")

    if c6.button("View", key=f"pipe_view_{job['id']}", use_container_width=True):
        st.session_state["selected_job_id"] = job["id"]
        st.switch_page("pages/3_job_detail.py")
