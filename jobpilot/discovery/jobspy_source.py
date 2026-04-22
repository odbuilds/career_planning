"""
JobSpy source — covers Indeed, Glassdoor, and Google Jobs.
Each is a separate slug in profile.yaml pointing at this module with a different jobspy_site value.
Requires: python-jobspy (already in requirements.txt)
"""

import pandas as pd


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    from jobspy import scrape_jobs

    site = (source_cfg or {}).get("jobspy_site", "indeed")

    country_indeed = _country_indeed(location)
    is_remote = (source_cfg or {}).get("_is_remote", False)
    scrape_kwargs = dict(
        site_name=[site],
        search_term=keywords,
        location=location,
        results_wanted=50,
        hours_old=days * 24,
        is_remote=is_remote,
    )
    if country_indeed:
        scrape_kwargs["country_indeed"] = country_indeed

    try:
        df = scrape_jobs(**scrape_kwargs)
    except Exception as e:
        raise RuntimeError(f"jobspy scrape failed for {site}: {e}") from e

    if df is None or df.empty:
        return []

    jobs = []
    for _, row in df.iterrows():
        company = _str(row.get("company"))
        role = _str(row.get("title"))
        if not company or not role:
            continue
        jobs.append({
            "company": company,
            "role": role,
            "url": _str(row.get("job_url")),
            "jd_text": _str(row.get("description")),
            "location": _str(row.get("location")),
        })
    return jobs


_COUNTRY_MAP = {
    "uk": "UK", "united kingdom": "UK", "london": "UK", "edinburgh": "UK",
    "cambridge": "UK", "norwich": "UK",
    "spain": "Spain", "valencia": "Spain", "madrid": "Spain",
    "usa": "USA", "us": "USA", "united states": "USA",
    "germany": "Germany", "france": "France", "netherlands": "Netherlands",
    "canada": "Canada", "australia": "Australia",
}


def _country_indeed(location: str) -> str | None:
    loc = location.lower()
    for key, val in _COUNTRY_MAP.items():
        if key in loc:
            return val
    return None


def _str(val) -> str:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return ""
    return str(val).strip()
