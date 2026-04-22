import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import load_config
from core import database as db
from core.models import PIPELINE_STAGES, INTERVIEW_TYPES
from core.scoring import explain_cv_recommendation

config = load_config()
db.init_db()

# ── Resolve job_id from session state or query params ─────────────────────────
job_id = st.session_state.get("selected_job_id")
if not job_id:
    params = st.query_params
    job_id = params.get("job_id")
    if job_id:
        try:
            job_id = int(job_id)
        except ValueError:
            job_id = None

if not job_id:
    st.warning("No job selected. Go to Jobs and click View.")
    if st.button("← Back to Jobs"):
        st.switch_page("pages/2_jobs_list.py")
    st.stop()

job = db.get_job(job_id)
if not job:
    st.error(f"Job #{job_id} not found.")
    st.stop()

# ── Header ────────────────────────────────────────────────────────────────────
back_col, title_col = st.columns([1, 8])
with back_col:
    if st.button("← Jobs"):
        st.switch_page("pages/2_jobs_list.py")

with title_col:
    st.subheader(f"{job['company']} — {job['role']}")

c1, c2, c3, c4 = st.columns([2, 1.5, 1.5, 2])

with c1:
    if job.get("url"):
        st.link_button("Open Job →", job["url"], use_container_width=True)
    else:
        st.caption("No URL saved")

with c2:
    score = job.get("score", 0)
    color = "🟢" if score >= 7 else "🟡" if score >= 4 else "🔴"
    st.metric("Score", f"{color} {score}")

with c3:
    current_status = job.get("status", "discovered")
    new_status = st.selectbox(
        "Status",
        options=PIPELINE_STAGES,
        index=PIPELINE_STAGES.index(current_status) if current_status in PIPELINE_STAGES else 0,
        key="detail_status",
    )
    if new_status != current_status:
        updates = {"status": new_status}
        if new_status == "applied" and not job.get("applied_at"):
            from datetime import date
            updates["applied_at"] = str(date.today())
        db.update_job(job_id, updates)
        st.rerun()

with c4:
    applied_at = job.get("applied_at") or ""
    new_applied = st.text_input("Applied date (YYYY-MM-DD)", value=applied_at, key="applied_date")
    if new_applied != applied_at:
        db.update_job(job_id, {"applied_at": new_applied})

st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_app, tab_emails, tab_interviews, tab_notes = st.tabs(
    ["📄 Application", "📬 Emails", "🗣 Interviews", "📝 Notes"]
)

# ── Tab 1: Application ────────────────────────────────────────────────────────
with tab_app:
    # JD
    with st.expander("Job Description", expanded=False):
        jd = job.get("jd_text") or ""
        if jd:
            st.text(jd)
        else:
            st.caption("No job description saved.")

    st.subheader("CV")
    cv_slug = job.get("recommended_cv", "cv_draft")
    _, matched_kws = explain_cv_recommendation(job.get("jd_text") or "", config)

    cv_col, override_col = st.columns([2, 2])
    with cv_col:
        display_name = config.get_cv_display_name(cv_slug)
        if matched_kws:
            st.success(f"**{display_name}** (matched: {', '.join(matched_kws[:4])}{'…' if len(matched_kws) > 4 else ''})")
        else:
            st.info(f"**{display_name}**")

        with st.expander("View CV content"):
            from generation.cv_recommendation import get_cv_content
            st.text(get_cv_content(cv_slug, config))

    with override_col:
        cv_slugs = list(config.cv_variants.keys())
        cv_names = [config.get_cv_display_name(s) for s in cv_slugs]
        current_idx = cv_slugs.index(cv_slug) if cv_slug in cv_slugs else 0
        new_cv_idx = st.selectbox(
            "Override CV",
            options=range(len(cv_slugs)),
            format_func=lambda i: cv_names[i],
            index=current_idx,
            key="cv_override",
        )
        if cv_slugs[new_cv_idx] != cv_slug:
            db.update_job(job_id, {"recommended_cv": cv_slugs[new_cv_idx]})
            st.rerun()

    # ── CV Customisation ──────────────────────────────────────────────────────
    st.subheader("Tailored CV")
    tailored = db.get_material(job_id, "cv_tailored")

    if tailored:
        with st.expander("Tailored CV content", expanded=False):
            edited_tailored = st.text_area(
                "Tailored CV (editable)",
                value=tailored["content"],
                height=400,
                key="tailored_cv_editor",
                label_visibility="collapsed",
            )
            tcol1, tcol2, tcol3 = st.columns([1, 1, 1])
            if tcol1.button("Save changes", key="save_tailored_cv", use_container_width=True):
                db.save_material(job_id, "cv_tailored", edited_tailored)
                st.toast("Saved", icon="✅")
                st.rerun()
            if tcol2.button("Re-customise", key="recustomise_cv", use_container_width=True):
                if not config.openrouter_api_key:
                    st.error("Set OPENROUTER_API_KEY in .env")
                else:
                    with st.spinner("Customising CV..."):
                        try:
                            from generation.cv_customisation import customise
                            tailored_content = customise(
                                job.get("jd_text", ""),
                                job.get("recommended_cv", "cv_draft"),
                                config,
                            )
                            db.save_material(job_id, "cv_tailored", tailored_content)
                            st.toast("CV customised", icon="✅")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Customisation failed: {e}")
            # PDF download for tailored CV
            cv_pdf_key = f"cv_pdf_{job_id}_{hash(tailored['content'])}"
            if cv_pdf_key not in st.session_state:
                try:
                    from generation.pdf import cv_to_pdf
                    st.session_state[cv_pdf_key] = cv_to_pdf(
                        tailored["content"], config.name
                    )
                except ImportError:
                    st.session_state[cv_pdf_key] = None
                except Exception:
                    st.session_state[cv_pdf_key] = None
            if st.session_state.get(cv_pdf_key):
                tcol3.download_button(
                    "⬇ PDF",
                    data=st.session_state[cv_pdf_key],
                    file_name=f"cv_{job['company'].replace(' ', '_').lower()}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            else:
                tcol3.caption("Install weasyprint for PDF")
    else:
        st.info("No tailored CV yet.")
        if st.button("Customise CV for this role", key="customise_cv_btn"):
            if not config.openrouter_api_key:
                st.error("Set OPENROUTER_API_KEY in .env")
            elif not job.get("jd_text"):
                st.error("No job description saved — add a JD first.")
            else:
                with st.spinner("Customising CV... this may take 20–30 seconds"):
                    try:
                        from generation.cv_customisation import customise
                        tailored_content = customise(
                            job.get("jd_text", ""),
                            job.get("recommended_cv", "cv_draft"),
                            config,
                        )
                        db.save_material(job_id, "cv_tailored", tailored_content)
                        st.toast("CV customised", icon="✅")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Customisation failed: {e}")

    st.subheader("Cover Letter")
    material = db.get_material(job_id, "cover_letter")

    if material:
        edited = st.text_area(
            "Cover letter (editable)",
            value=material["content"],
            height=350,
            key="cl_editor",
        )
        btn_col1, btn_col2, btn_col3, btn_col4 = st.columns([1, 1, 1, 2])
        if btn_col1.button("Save changes", use_container_width=True):
            db.save_material(job_id, "cover_letter", edited)
            st.toast("Saved", icon="✅")
            st.rerun()
        if btn_col2.button("Regenerate", use_container_width=True):
            if not config.openrouter_api_key:
                st.error("Set OPENROUTER_API_KEY in .env")
            else:
                with st.spinner("Regenerating..."):
                    try:
                        from generation.cover_letter import generate
                        letter = generate(
                            job["company"], job["role"],
                            job.get("jd_text", ""),
                            job.get("recommended_cv", "cv_draft"),
                            config,
                        )
                        db.save_material(job_id, "cover_letter", letter)
                        st.toast("Regenerated", icon="✅")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Generation failed: {e}")
        # PDF download — keyed off the live editor text so edits are reflected immediately
        cl_pdf_key = f"cl_pdf_{job_id}_{hash(edited)}"
        if cl_pdf_key not in st.session_state:
            try:
                from generation.pdf import cover_letter_to_pdf
                st.session_state[cl_pdf_key] = cover_letter_to_pdf(
                    edited, config.name, job["company"], job["role"]
                )
            except ImportError:
                st.session_state[cl_pdf_key] = None
            except Exception:
                st.session_state[cl_pdf_key] = None
        if st.session_state.get(cl_pdf_key):
            btn_col3.download_button(
                "⬇ PDF",
                data=st.session_state[cl_pdf_key],
                file_name=f"cover_letter_{job['company'].replace(' ', '_').lower()}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            btn_col3.caption("Install weasyprint for PDF")
        # Copy hint
        btn_col4.caption("Select all text above → Ctrl+A → Ctrl+C to copy")
    else:
        st.info("No cover letter yet.")
        if st.button("Generate Cover Letter", type="primary"):
            if not config.openrouter_api_key:
                st.error("Set OPENROUTER_API_KEY in .env")
            else:
                with st.spinner("Generating..."):
                    try:
                        from generation.cover_letter import generate
                        letter = generate(
                            job["company"], job["role"],
                            job.get("jd_text", ""),
                            job.get("recommended_cv", "cv_draft"),
                            config,
                        )
                        db.save_material(job_id, "cover_letter", letter)
                        st.toast("Cover letter generated", icon="✅")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Generation failed: {e}")

# ── Tab 2: Emails ─────────────────────────────────────────────────────────────
with tab_emails:
    emails = db.get_emails(job_id)
    if not emails:
        st.info("No emails yet. Ask Claude to 'check my job emails' to populate this.")
    else:
        classification_colors = {
            "interview_invite":         "🟢",
            "offer":                    "🟢",
            "recruiter_screen_request": "🟡",
            "action_needed":            "🟡",
            "application_acknowledgement": "⚪",
            "general_info":             "⚪",
            "rejection":                "🔴",
        }
        for email in emails:
            icon = classification_colors.get(email["classification"], "⚪")
            label = f"{icon} {email['received_at'][:10] if email['received_at'] else '?'} · {email['subject']} · {email['sender']}"
            with st.expander(label):
                st.caption(f"Classification: **{email['classification']}**")
                st.text(email.get("body") or "")

# ── Tab 3: Interviews ─────────────────────────────────────────────────────────
with tab_interviews:
    interviews = db.get_interviews(job_id)

    if interviews:
        for iv in interviews:
            with st.container(border=True):
                ic1, ic2 = st.columns([3, 1])
                with ic1:
                    st.markdown(f"**{iv['type']}** — {iv['date']}")
                    if iv.get("interviewer"):
                        st.caption(f"Interviewer: {iv['interviewer']}")
                with ic2:
                    if st.button("Delete", key=f"del_iv_{iv['id']}", type="secondary"):
                        db.delete_interview(iv["id"])
                        st.rerun()

                if iv.get("notes"):
                    with st.expander("Notes", expanded=True):
                        new_notes = st.text_area(
                            "Notes",
                            value=iv["notes"],
                            height=200,
                            key=f"iv_notes_{iv['id']}",
                            label_visibility="collapsed",
                        )
                        if st.button("Save notes", key=f"save_iv_{iv['id']}"):
                            db.update_interview(iv["id"], {"notes": new_notes})
                            st.toast("Saved", icon="✅")
                            st.rerun()
    else:
        st.info("No interviews recorded yet.")

    st.subheader("Add Interview")
    with st.form("add_interview_form", clear_on_submit=True):
        fc1, fc2 = st.columns(2)
        iv_date = fc1.date_input("Date")
        iv_type = fc2.selectbox("Type", INTERVIEW_TYPES)
        iv_interviewer = st.text_input("Interviewer name (optional)")
        iv_notes = st.text_area(
            "Notes (paste questions, answers, transcript — anything)",
            height=200,
            placeholder="Questions asked, your answers, impressions, anything useful for next round...",
        )
        if st.form_submit_button("Add Interview"):
            db.add_interview(
                job_id=job_id,
                date=str(iv_date),
                type_=iv_type,
                interviewer=iv_interviewer,
                notes=iv_notes,
            )
            st.toast("Interview added", icon="✅")
            st.rerun()

# ── Tab 4: Notes ──────────────────────────────────────────────────────────────
with tab_notes:
    current_notes = job.get("notes") or ""
    new_notes = st.text_area(
        "Notes",
        value=current_notes,
        height=400,
        placeholder="Recruiter name, salary discussed, things to research, gut feel, anything...",
        label_visibility="collapsed",
    )
    if st.button("Save Notes"):
        db.update_job(job_id, {"notes": new_notes})
        st.toast("Saved", icon="✅")
        st.rerun()
