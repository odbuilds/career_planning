"""
Discovery runner — loads enabled source modules and ingests results into the DB.

Usage (from jobpilot/):
    from discovery.runner import run_discovery
    result = run_discovery(["adzuna", "reed"], "AI engineer", "London", 7, config)
    # result = {"new": N, "skipped": N, "errors": [...]}
"""

import importlib
import re

from core import database as db
from core.scoring import score_job, recommend_cv


def run_discovery(
    slugs: list[str],
    keywords: str,
    location: str,
    days: int,
    config,
) -> dict:
    """
    Run discovery for the given source slugs.
    Each source module must implement:
        fetch(keywords, location, days, config, source_cfg=None) -> list[dict]
    Returned dicts must contain: company, role. url and jd_text are optional.
    """
    results = {"new": 0, "skipped": 0, "errors": []}
    source_map = {s["slug"]: s for s in config.get_enabled_sources()}

    for slug in slugs:
        source_cfg = source_map.get(slug)
        if not source_cfg:
            results["errors"].append(f"{slug}: not in enabled sources")
            continue

        try:
            module = importlib.import_module(f"discovery.{source_cfg['module']}")
        except ImportError as e:
            results["errors"].append(f"{slug}: import failed — {e}")
            continue

        # For location-aware sources, loop over all configured search locations.
        # location may be: a dict (from UI), a string, or empty.
        if isinstance(location, dict):
            loc_configs = [location]  # UI passed a full loc config dict — use as-is
        elif location:
            loc_configs = [{"location": location}]  # plain string override
        elif source_cfg.get("uses_location"):
            loc_configs = config.search_locations or [{"location": ""}]
        else:
            loc_configs = [{"location": ""}]

        jobs = []
        for loc_cfg in loc_configs:
            loc_str = loc_cfg.get("location", "") if isinstance(loc_cfg, dict) else loc_cfg
            title_filter = loc_cfg.get("title_filter") if isinstance(loc_cfg, dict) else None
            is_remote = loc_cfg.get("remote", False) if isinstance(loc_cfg, dict) else False

            # Pass remote flag into source via source_cfg copy
            effective_cfg = {**source_cfg, "_is_remote": is_remote}

            # Use source-specific days_old override if set, otherwise use the run-level value
            effective_days = source_cfg.get("days_old", days)

            try:
                batch = module.fetch(keywords, loc_str, effective_days, config, effective_cfg)
            except NotImplementedError:
                results["errors"].append(f"{slug}: not yet implemented")
                break
            except Exception as e:
                results["errors"].append(f"{slug} ({loc_str}): fetch error — {e}")
                continue

            # Global positive title filter — drop jobs with no matching term in title
            if config.title_positive_filter:
                tf_patterns = [re.compile(r'\b' + re.escape(t.lower()) + r'\b') for t in config.title_positive_filter]
                batch = [j for j in batch if any(p.search(j.get("role", "").lower()) for p in tf_patterns)]

            # Gap 1: title red flags — drop jobs whose title matches any disqualifying term
            if config.title_red_flags:
                trf = [t.lower() for t in config.title_red_flags]
                batch = [j for j in batch if not any(t in j.get("role", "").lower() for t in trf)]

            # Apply title filter if set for this location
            if title_filter:
                tf_lower = [t.lower() for t in title_filter]
                batch = [
                    j for j in batch
                    if any(t in j.get("role", "").lower() for t in tf_lower)
                ]

            # Drop non-ASCII titles (catches Spanish/non-English job titles)
            if loc_cfg.get("ascii_only") if isinstance(loc_cfg, dict) else False:
                batch = [j for j in batch if j.get("role", "").isascii()]

            jobs.extend(batch)

        # For LinkedIn: fetch missing JD text before scoring
        if slug == "linkedin":
            _fetch_missing_jds(jobs)

        # Filter valid jobs and do pass 1: keyword scoring
        valid_jobs = []
        for job in jobs:
            if not job.get("company") or not job.get("role"):
                continue
            jd = job.get("jd_text", "")

            # Gap 3: drop non-English JDs (catches Spanish JDs with English titles)
            if jd and _is_non_english(jd):
                results["skipped"] += 1
                continue
            job["source"] = slug
            job["status"] = "discovered"
            job["score"] = score_job(jd, config)
            job["recommended_cv"] = recommend_cv(jd, config)
            valid_jobs.append(job)

        # Pass 2: batch LLM scoring for jobs above threshold
        if (
            config.llm_scoring_enabled
            and config.openrouter_api_key
        ):
            llm_candidates = [
                {"id": i, "jd_text": j.get("jd_text", "")}
                for i, j in enumerate(valid_jobs)
                if j.get("jd_text", "").strip()
                and j["score"] >= config.llm_scoring_threshold
            ]
            if llm_candidates:
                from core.llm_scorer import llm_score_batch
                scored = llm_score_batch(llm_candidates, config)
                for idx, llm_val, _ in scored:
                    if llm_val is not None:
                        valid_jobs[idx]["score"] = llm_val

        # Pass 3: cascade pipeline scoring (A/B/C/D or DQ)
        if config.pipeline_scoring_enabled and config.openrouter_api_key:
            pipeline_candidates = [
                {"id": i, "jd_text": j.get("jd_text", "")}
                for i, j in enumerate(valid_jobs)
                if j.get("jd_text", "").strip()
            ]
            if pipeline_candidates:
                from core.pipeline_scorer import pipeline_score_batch
                pipeline_results = pipeline_score_batch(pipeline_candidates, config)
                for idx, ptier, preason in pipeline_results:
                    if ptier is not None:
                        valid_jobs[idx]["pipeline_tier"] = ptier
                        valid_jobs[idx]["pipeline_reason"] = preason

        for job in valid_jobs:
            is_new = _is_new_job(job)
            db.upsert_job(job)
            if is_new:
                results["new"] += 1
            else:
                results["skipped"] += 1

    return results


def _llm_scorer(jd: str, config):
    from core.llm_scorer import llm_score
    return llm_score(jd, config)


def _is_non_english(text: str) -> bool:
    """
    Heuristic: return True if the JD text appears to be non-English.
    Two signals: Spanish diacritic characters, and high frequency of Spanish stop words.
    """
    # Signal 1: Spanish/non-ASCII characters (á é í ó ú ñ ü and their capitals)
    spanish_chars = set("áéíóúñüÁÉÍÓÚÑÜ¿¡")
    if sum(1 for c in text if c in spanish_chars) > 3:
        return True
    # Signal 2: high hit count of Spanish stop words that rarely appear in English
    lower = text.lower()
    markers = [" que ", " para ", " con ", " los ", " las ", " del ", " una ", " por ", " como ", " también "]
    hits = sum(lower.count(m) for m in markers)
    return hits > 15


def _fetch_missing_jds(jobs: list[dict]) -> None:
    """Fetch JD text in-place for LinkedIn jobs where JobSpy returned no description."""
    import time
    from core.jd_fetch import fetch_jd
    for job in jobs:
        if job.get("jd_text") or not job.get("url"):
            continue
        result = fetch_jd(job["url"])
        if not result["error"] and result["jd_text"].strip():
            job["jd_text"] = result["jd_text"]
        time.sleep(0.3)


def _is_new_job(job: dict) -> bool:
    """Returns True if this job does not already exist in the DB."""
    with db.get_conn() as conn:
        if job.get("url"):
            row = conn.execute(
                "SELECT id FROM jobs WHERE url = ?", (job["url"],)
            ).fetchone()
            if row:
                return False

        company = (job.get("company") or "").strip().lower()
        role = (job.get("role") or "").strip().lower()
        if company and role:
            row = conn.execute(
                "SELECT id FROM jobs WHERE lower(company) = ? AND lower(role) = ?",
                (company, role),
            ).fetchone()
            if row:
                return False

    return True
