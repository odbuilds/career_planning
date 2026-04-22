"""
Arbeitnow source — EU-focused remote tech jobs via Arbeitnow public API.
No API key required. Returns remote-tagged listings; keyword filtering
is applied by the runner's title_positive_filter.
API: https://www.arbeitnow.com/api/job-board-api
"""

import requests


_API_URL = "https://www.arbeitnow.com/api/job-board-api"
_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; JobPilot/1.0)"}


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    try:
        resp = requests.get(_API_URL, headers=_HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Arbeitnow request failed: {e}") from e

    jobs = []
    for item in resp.json().get("data", []):
        # Only keep remote listings
        if not item.get("remote"):
            continue
        company = (item.get("company_name") or "").strip()
        role = (item.get("title") or "").strip()
        if not company or not role:
            continue
        url = item.get("url") or ""
        jd = item.get("description") or ""
        jobs.append({"company": company, "role": role, "url": url, "jd_text": jd})

    return jobs
