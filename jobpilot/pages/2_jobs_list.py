import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import load_config
from core import database as db
from core.models import PIPELINE_STAGES
from core.scoring import score_job, recommend_cv

config = load_config()
db.init_db()

PAGE_SIZE = 20

st.markdown("""
<style>
    .block-container { padding-left: 1rem; padding-right: 1rem; max-width: 100%; }
</style>
""", unsafe_allow_html=True)

st.header("🔍 Jobs")

# ── Filters ───────────────────────────────────────────────────────────────────
with st.expander("Filters", expanded=False):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        _hidden_by_default = {"rejected", "withdrawn", "applied",
                              "screening", "interview", "final", "offer",
                              "passed-application", "passed-screening",
                              "passed-interview", "passed-final"}
        _default_statuses = [s for s in PIPELINE_STAGES if s not in _hidden_by_default]
        # Post-discovery: override default to show only newly discovered
        if st.session_state.get("post_discovery_filter"):
            _default_statuses = ["discovered"]
        status_filter = st.multiselect(
            "Status",
            options=PIPELINE_STAGES,
            default=_default_statuses,
            on_change=lambda: st.session_state.pop("post_discovery_filter", None),
        )
    with col2:
        enabled_slugs = [s["slug"] for s in config.get_enabled_sources()]
        source_filter = st.multiselect("Source", options=enabled_slugs + ["manual"])
    with col3:
        min_score = st.slider("Min score", 0.0, 10.0, 0.0, 0.5)
    with col4:
        search = st.text_input("Search company / role", placeholder="e.g. Anthropic")

jobs = db.get_jobs(
    status=status_filter or None,
    source=source_filter or None,
    min_score=min_score,
    search=search,
)

# ── Action buttons ────────────────────────────────────────────────────────────
col_add, col_discover, col_fetch_jd, col_spacer = st.columns([1, 1, 1.5, 4])

with col_add:
    add_open = st.button("➕ Add Job", use_container_width=True)

with col_discover:
    discover_open = st.button("🔎 Discover Jobs", use_container_width=True)

with col_fetch_jd:
    fetch_jds_open = st.button("📥 Fetch LinkedIn JDs", use_container_width=True)

# ── Add Job form ──────────────────────────────────────────────────────────────
if add_open:
    st.session_state["show_add_form"] = not st.session_state.get("show_add_form", False)
    if not st.session_state["show_add_form"]:
        for key in ("prefill_url", "prefill_company", "prefill_role", "prefill_jd"):
            st.session_state.pop(key, None)

if st.session_state.get("show_add_form"):
    st.subheader("Add Job Manually")

    # ── URL fetch (outside form so it can update session state dynamically) ──
    fetch_col, btn_col = st.columns([4, 1])
    url_input = fetch_col.text_input(
        "Job URL",
        value=st.session_state.get("prefill_url", ""),
        placeholder="Paste URL to auto-fill from job posting",
        key="url_prefill_input",
    )
    with btn_col:
        st.write("")  # vertical align
        st.write("")
        if st.button("Fetch JD", use_container_width=True):
            if url_input:
                with st.spinner("Fetching..."):
                    from core.jd_fetch import fetch_jd
                    fetched = fetch_jd(url_input)
                if fetched["error"]:
                    st.error(fetched["error"])
                else:
                    st.session_state["prefill_url"] = url_input
                    st.session_state["prefill_company"] = fetched["company"]
                    st.session_state["prefill_role"] = fetched["role"]
                    st.session_state["prefill_jd"] = fetched["jd_text"]
                    st.rerun()
            else:
                st.warning("Enter a URL first.")

    with st.form("add_job_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        company = c1.text_input("Company *", value=st.session_state.get("prefill_company", ""))
        role = c2.text_input("Role / Title *", value=st.session_state.get("prefill_role", ""))
        jd_text = st.text_area(
            "Job Description",
            value=st.session_state.get("prefill_jd", ""),
            height=200,
            placeholder="Auto-filled from URL, or paste manually",
        )
        source = st.selectbox("Source", ["manual"] + [s["slug"] for s in config.get_enabled_sources()])

        submitted = st.form_submit_button("Add Job")
        if submitted:
            url = st.session_state.get("prefill_url", "") or url_input
            if not company or not role:
                st.error("Company and Role are required.")
            else:
                s = score_job(jd_text, config)
                cv = recommend_cv(jd_text, config)
                db.upsert_job({
                    "company": company,
                    "role": role,
                    "url": url,
                    "jd_text": jd_text,
                    "source": source,
                    "score": s,
                    "recommended_cv": cv,
                    "status": "discovered",
                })
                st.success(f"Added: {company} — {role} (score {s}, CV: {config.get_cv_display_name(cv)})")
                for key in ("prefill_url", "prefill_company", "prefill_role", "prefill_jd"):
                    st.session_state.pop(key, None)
                st.session_state["show_add_form"] = False
                st.rerun()

# ── Discover Jobs form ────────────────────────────────────────────────────────
if discover_open:
    st.session_state["show_discover_form"] = not st.session_state.get("show_discover_form", False)

if st.session_state.get("show_discover_form"):
    with st.expander("Discovery Settings", expanded=True):

        # Keywords — one search per phrase
        st.write("**Keywords** (each searched separately)")
        kw_cols = st.columns(3)
        selected_keywords = []
        for i, kw in enumerate(config.keyword_searches):
            if kw_cols[i % 3].checkbox(kw, value=True, key=f"kw_{i}"):
                selected_keywords.append(kw)

        st.divider()

        # Locations — display only, driven by profile.yaml
        st.write("**Locations**")
        loc_cols = st.columns(3)
        selected_locations = []
        for i, loc_cfg in enumerate(config.search_locations):
            loc_str = loc_cfg.get("location", "") if isinstance(loc_cfg, dict) else loc_cfg
            label = loc_str
            if isinstance(loc_cfg, dict):
                if loc_cfg.get("remote"):
                    label += " (remote)"
                if loc_cfg.get("title_filter"):
                    label += " *"
            if loc_cols[i % 3].checkbox(label, value=True, key=f"loc_{i}"):
                selected_locations.append(loc_cfg)
        st.caption("Edit `search_locations` in profile.yaml to change this list.")

        st.divider()

        # Days
        days = st.number_input("Days old (max)", value=config.default_days_old, min_value=1, max_value=30)

        st.divider()

        # Sources
        st.write("**Sources**")
        enabled_sources = config.get_enabled_sources()
        selected_slugs = []
        src_cols = st.columns(3)
        for i, source in enumerate(enabled_sources):
            needs_key = source.get("requires_key", False)
            has_key = True
            if needs_key:
                if source["slug"] == "adzuna" and not (config.adzuna_app_id and config.adzuna_api_key):
                    has_key = False
                elif source["slug"] == "reed" and not config.reed_api_key:
                    has_key = False
            label = source["display"] if has_key else f"{source['display']} ⚠️ (no key)"
            checked = src_cols[i % 3].checkbox(label, value=has_key, disabled=not has_key, key=f"src_{source['slug']}")
            if checked and has_key:
                selected_slugs.append(source["slug"])

        if st.button("🚀 Run Discovery", type="primary"):
            if not selected_slugs:
                st.warning("Select at least one source.")
            elif not selected_keywords:
                st.warning("Select at least one keyword.")
            else:
                st.session_state["show_discover_form"] = False
                total = {"new": 0, "skipped": 0, "errors": []}
                from discovery.runner import run_discovery

                # Location-aware sources loop over selected_locations via runner.
                # Non-location sources just need one call per keyword.
                location_aware = [s for s in selected_slugs if any(
                    src["slug"] == s and src.get("uses_location")
                    for src in config.get_enabled_sources()
                )]
                location_free = [s for s in selected_slugs if s not in location_aware]

                progress = st.progress(0)
                total_steps = len(selected_keywords) * (
                    (len(selected_locations) if location_aware else 0) + (1 if location_free else 0)
                )
                step = 0

                for kw in selected_keywords:
                    # Location-aware sources: one call per location
                    for loc in (selected_locations if location_aware else []):
                        try:
                            r = run_discovery(location_aware, kw, loc, days, config)
                            total["new"] += r["new"]
                            total["skipped"] += r["skipped"]
                            total["errors"].extend(r["errors"])
                        except Exception as e:
                            total["errors"].append(str(e))
                        step += 1
                        progress.progress(step / max(total_steps, 1))

                    # Location-free sources: one call per keyword, no location
                    if location_free:
                        try:
                            r = run_discovery(location_free, kw, "", days, config)
                            total["new"] += r["new"]
                            total["skipped"] += r["skipped"]
                            total["errors"].extend(r["errors"])
                        except Exception as e:
                            total["errors"].append(str(e))
                        step += 1
                        progress.progress(step / max(total_steps, 1))

                progress.empty()
                st.success(f"Done — {total['new']} new, {total['skipped']} skipped")
                if total["errors"]:
                    with st.expander(f"{len(total['errors'])} errors"):
                        for err in total["errors"]:
                            st.caption(err)
                if total["new"] > 0:
                    st.session_state["post_discovery_filter"] = True
                st.rerun()

# ── Fetch LinkedIn JDs ────────────────────────────────────────────────────────
if fetch_jds_open:
    with db.get_conn() as conn:
        pending = conn.execute(
            """SELECT id, company, role, url FROM jobs
               WHERE source = 'linkedin'
               AND status NOT IN ('rejected','withdrawn')
               AND (jd_text IS NULL OR jd_text = '')
               AND url != ''"""
        ).fetchall()

    if not pending:
        st.info("No LinkedIn jobs with missing JDs.")
    else:
        st.write(f"**{len(pending)} LinkedIn jobs** with no JD text — fetching now...")
        from core.jd_fetch import fetch_jd

        progress = st.progress(0)
        fetched_ok = 0
        fetched_fail = 0
        for i, row in enumerate(pending):
            job_id_r, company, role, url = row["id"], row["company"], row["role"], row["url"]
            result = fetch_jd(url)
            if result["error"] or not result["jd_text"].strip():
                fetched_fail += 1
            else:
                jd = result["jd_text"]
                new_score = score_job(jd, config)
                new_cv = recommend_cv(jd, config)
                db.update_job(job_id_r, {"jd_text": jd, "score": new_score, "recommended_cv": new_cv})
                fetched_ok += 1
            progress.progress((i + 1) / len(pending))

        progress.empty()
        st.success(f"Done — {fetched_ok} JDs fetched, {fetched_fail} failed/empty")
        st.rerun()

st.divider()

# ── Reject dialog ────────────────────────────────────────────────────────────
@st.dialog("Reject job")
def _reject_dialog(job: dict):
    st.write(f"**{job['company']}** — {job['role']}")
    note = st.text_area("Reason (optional)", placeholder="e.g. salary too low, wrong stack, too junior...")
    c1, c2 = st.columns(2)
    if c1.button("Confirm reject", type="primary", use_container_width=True):
        updates = {"status": "rejected"}
        if note.strip():
            existing = job.get("notes") or ""
            updates["notes"] = (existing + f"\n[Rejected] {note.strip()}").strip()
        db.update_job(job["id"], updates)
        st.session_state.pop("reject_job", None)
        st.rerun()
    if c2.button("Cancel", use_container_width=True):
        st.session_state.pop("reject_job", None)
        st.rerun()

if "reject_job" in st.session_state:
    _reject_dialog(st.session_state["reject_job"])

# ── Jobs table ────────────────────────────────────────────────────────────────
if not jobs:
    st.info("No jobs match the current filters.")
else:
    total_jobs = len(jobs)
    total_pages = max(1, (total_jobs + PAGE_SIZE - 1) // PAGE_SIZE)

    # Reset page if filters changed and page is out of range
    if st.session_state.get("jobs_page", 1) > total_pages:
        st.session_state["jobs_page"] = 1
    page = st.session_state.get("jobs_page", 1)

    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    page_jobs = jobs[start:end]

    pg_left, pg_mid, pg_right = st.columns([1, 3, 1])
    with pg_left:
        if st.button("← Prev", disabled=page <= 1, use_container_width=True):
            st.session_state["jobs_page"] = page - 1
            st.rerun()
    with pg_mid:
        st.caption(f"{total_jobs} job{'s' if total_jobs != 1 else ''} · page {page} of {total_pages}")
    with pg_right:
        if st.button("Next →", disabled=page >= total_pages, use_container_width=True):
            st.session_state["jobs_page"] = page + 1
            st.rerun()

    for job in page_jobs:
        with st.container(border=True):
            col_info, col_score, col_cv, col_status, col_actions = st.columns([5, 1, 2, 1.5, 2])

            with col_info:
                url = job.get("url") or ""
                if url:
                    st.markdown(f"**[{job['company']}]({url})** — {job['role']}")
                else:
                    st.markdown(f"**{job['company']}** — {job['role']}")
                src = job.get("source") or "manual"
                created = (job.get("created_at") or "")[:10]
                loc = job.get("location") or ""
                caption = f"{src} · {created}"
                if loc:
                    caption += f" · 📍 {loc}"
                st.caption(caption)

            with col_score:
                score = job.get("score", 0)
                color = "🟢" if score >= 7 else "🟡" if score >= 4 else "🔴"
                st.metric("Score", f"{color} {score}")

            with col_cv:
                cv_slug = job.get("recommended_cv", "cv_draft")
                st.caption("Recommended CV")
                st.write(config.get_cv_display_name(cv_slug))

            with col_status:
                current_status = job.get("status", "discovered")
                new_status = st.selectbox(
                    "Status",
                    options=PIPELINE_STAGES,
                    index=PIPELINE_STAGES.index(current_status) if current_status in PIPELINE_STAGES else 0,
                    key=f"status_{job['id']}",
                    label_visibility="collapsed",
                )
                if new_status != current_status:
                    db.update_job(job["id"], {"status": new_status})
                    st.rerun()

            with col_actions:
                view_col, cl_col, apply_col, reject_col = st.columns(4)
                if view_col.button("View", key=f"view_{job['id']}", use_container_width=True):
                    st.session_state["selected_job_id"] = job["id"]
                    st.switch_page("pages/3_job_detail.py")

                if apply_col.button("✓", key=f"apply_{job['id']}", use_container_width=True, help="Mark as applied"):
                    from datetime import date
                    db.update_job(job["id"], {"status": "applied", "applied_at": str(date.today())})
                    st.rerun()

                if reject_col.button("✕", key=f"reject_{job['id']}", use_container_width=True, help="Reject this job"):
                    st.session_state["reject_job"] = job
                    st.rerun()

                cl_exists = db.get_material(job["id"], "cover_letter") is not None
                cl_label = "✓ CL" if cl_exists else "Gen CL"
                if cl_col.button(cl_label, key=f"cl_{job['id']}", use_container_width=True):
                    if not config.openrouter_api_key:
                        st.error("Set OPENROUTER_API_KEY in .env to generate cover letters.")
                    else:
                        with st.spinner(f"Generating cover letter for {job['company']}..."):
                            try:
                                from generation.cover_letter import generate
                                letter = generate(
                                    job["company"],
                                    job["role"],
                                    job.get("jd_text", ""),
                                    job.get("recommended_cv", "cv_draft"),
                                    config,
                                )
                                db.save_material(job["id"], "cover_letter", letter)
                                st.toast(f"Cover letter generated for {job['company']}", icon="✅")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Generation failed: {e}")
