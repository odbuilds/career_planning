"""
LinkedIn source — uses python-jobspy's LinkedIn scraper.
Requires: python-jobspy (already in requirements.txt)
"""

import re

import pandas as pd

# Countries not accepted by JobSpy's LinkedIn scraper — strip the country
# suffix so the city name is still used for geo-filtering.
_UNSUPPORTED_COUNTRY_RE = re.compile(r',\s*(Serbia)$', re.IGNORECASE)

# Allowlist: location strings containing any of these terms are kept.
_ALLOWED_LOCATION_TERMS = [
    "uk", "united kingdom", "england", "scotland", "wales",
    "spain", "serbia", "italy",
    "sweden", "norway", "denmark", "finland", "slovenia",
    "remote", "worldwide", "anywhere",
]


def _is_allowed_location(loc: str) -> bool:
    """Return True if the location matches a preferred region or is explicitly remote/worldwide."""
    lower = loc.lower()
    return any(term in lower for term in _ALLOWED_LOCATION_TERMS)


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    from jobspy import scrape_jobs

    # source_cfg may carry is_remote flag set by runner from location config
    is_remote = (source_cfg or {}).get("_is_remote", False)

    # When searching remote-only, drop the location string — passing a broad
    # geographic term like "Europe" causes JobSpy's country validator to fail.
    # Also strip countries not supported by JobSpy (e.g. Serbia).
    effective_location = "" if is_remote else _UNSUPPORTED_COUNTRY_RE.sub("", location).strip(", ")
    results_wanted = (source_cfg or {}).get("results_wanted", 50)

    try:
        df = scrape_jobs(
            site_name=["linkedin"],
            search_term=keywords,
            location=effective_location,
            results_wanted=results_wanted,
            hours_old=days * 24,
            is_remote=is_remote,
        )
    except Exception as e:
        if "Invalid country string" in str(e):
            return []
        raise RuntimeError(f"LinkedIn scrape failed: {e}") from e

    if df is None or df.empty:
        return []

    jobs = []
    for _, row in df.iterrows():
        company = _str(row.get("company"))
        role = _str(row.get("title"))
        if not company or not role:
            continue
        loc = _str(row.get("location"))

        # Always enforce allowlist — remote searches also include "remote"/"worldwide" terms
        if not loc or not _is_allowed_location(loc):
            continue

        jobs.append({
            "company": company,
            "role": role,
            "url": _str(row.get("job_url")),
            "jd_text": _str(row.get("description")),
            "location": loc,
        })
    return jobs


def _str(val) -> str:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return ""
    return str(val).strip()
