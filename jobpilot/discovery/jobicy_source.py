"""
Jobicy source — global remote jobs via Jobicy public API.
No API key required.
API: https://jobicy.com/api/v2/remote-jobs
Note: 'tag' param requires 3–50 characters.
"""

import requests


_API_URL = "https://jobicy.com/api/v2/remote-jobs"
_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; JobPilot/1.0)"}


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    # API requires tag to be 3–50 chars; truncate if needed, skip if too short
    tag = keywords.strip()[:50]
    if len(tag) < 3:
        return []

    try:
        resp = requests.get(
            _API_URL,
            params={"count": 50, "tag": tag},
            headers=_HEADERS,
            timeout=15,
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Jobicy request failed: {e}") from e

    jobs = []
    for item in resp.json().get("jobs", []):
        company = (item.get("companyName") or "").strip()
        role = (item.get("jobTitle") or "").strip()
        if not company or not role:
            continue
        url = item.get("url") or ""
        jd = item.get("jobDescription") or item.get("jobExcerpt") or ""
        jobs.append({"company": company, "role": role, "url": url, "jd_text": jd})

    return jobs
