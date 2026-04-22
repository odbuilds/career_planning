import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))

from core.config import load_config
from core import database as db

st.set_page_config(
    page_title="JobPilot",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .block-container { padding-left: 1rem; padding-right: 1rem; max-width: 100%; }
</style>
""", unsafe_allow_html=True)

# Initialise on every run
config = load_config()
db.init_db()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🎯 JobPilot")
    st.caption(f"Searching as: **{config.name}**")
    st.divider()

    counts = db.get_pipeline_counts()
    total = sum(counts.values())
    active = sum(counts.get(s, 0) for s in ["applied", "replied", "screening", "interview", "final"])

    st.metric("Total tracked", total)
    col1, col2 = st.columns(2)
    col1.metric("Active", active)
    col2.metric("Interviews", counts.get("interview", 0) + counts.get("final", 0))

    st.divider()

    last_check = db.get_meta("last_email_check_at")
    if last_check:
        st.caption(f"Last email check: {last_check[:10]}")
    else:
        st.caption("Email check: never run")

    st.divider()
    st.caption("Pages")
    st.page_link("pages/1_pipeline.py",  label="📋 Pipeline",  icon=None)
    st.page_link("pages/2_jobs_list.py", label="🔍 Jobs",      icon=None)

# ── Home splash (only shown on root page) ─────────────────────────────────────
st.header("JobPilot")
st.write("Use the sidebar to navigate.")

if total == 0:
    st.info("No jobs tracked yet. Go to **Jobs** to add your first role or run discovery.")
else:
    # Quick status summary table
    stage_order = ["applied", "replied", "screening", "interview", "final", "offer", "rejected", "withdrawn", "discovered", "queued"]
    rows = [(s, counts[s]) for s in stage_order if s in counts]
    if rows:
        import pandas as pd
        df = pd.DataFrame(rows, columns=["Stage", "Count"])
        st.dataframe(df, use_container_width=False, hide_index=True)
