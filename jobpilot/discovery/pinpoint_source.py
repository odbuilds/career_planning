"""
Pinpoint HQ source — polls public job boards for companies using Pinpoint ATS.
Uses the undocumented but consistent /jobs.json endpoint (no auth required).

Each company entry in profile.yaml pinpoint_companies requires:
  name: display name
  url:  base URL of their Pinpoint board (e.g. "https://sabio.pinpointhq.com")
"""

import requests

_ALLOWED_LOCATION_TERMS = [
    "uk", "united kingdom", "england", "scotland", "wales",
    # UK cities
    "london", "manchester", "edinburgh", "cambridge", "bristol",
    "birmingham", "leeds", "sheffield", "liverpool", "oxford",
    "reading", "brighton", "glasgow", "belfast", "cardiff",
    # Other target countries
    "spain", "serbia", "italy",
    "sweden", "norway", "denmark", "finland", "slovenia",
    "netherlands", "ireland", "luxembourg", "switzerland",
    "remote", "worldwide", "anywhere", "hybrid",
]

_HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0",
}


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    companies = getattr(config, "pinpoint_companies", [])
    if not companies:
        return []

    kw_list = [k.lower() for k in keywords.split() if k]
    results = []

    for company in companies:
        name = company.get("name", "")
        base_url = company.get("url", "").rstrip("/")
        if not name or not base_url:
            continue

        try:
            jobs = _fetch_jobs(base_url)
        except Exception:
            continue

        for job in jobs:
            title = job.get("title", "")
            if not title:
                continue
            if kw_list and not any(kw in title.lower() for kw in kw_list):
                continue
            loc = _extract_location(job)
            if loc and not _is_allowed_location(loc):
                continue
            results.append({
                "company": name,
                "role":    title,
                "url":     base_url + job.get("path", ""),
                "jd_text": _extract_jd(job),
                "location": loc,
            })

    return results


def _fetch_jobs(base_url: str) -> list[dict]:
    resp = requests.get(f"{base_url}/jobs.json", headers=_HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.json().get("data", [])


def _extract_location(job: dict) -> str:
    loc = job.get("location")
    if isinstance(loc, dict):
        return loc.get("name", "")
    return str(loc) if loc else ""


def _extract_jd(job: dict) -> str:
    parts = []
    for field in ("description", "key_responsibilities", "skills_knowledge_expertise"):
        val = job.get(field, "")
        if val:
            import re
            parts.append(re.sub(r"<[^>]+>", " ", str(val)).strip())
    return " ".join(parts)[:4000]


def _is_allowed_location(loc: str) -> bool:
    lower = loc.lower()
    return any(term in lower for term in _ALLOWED_LOCATION_TERMS)
