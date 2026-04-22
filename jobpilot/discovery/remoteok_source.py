"""
RemoteOK source — global remote jobs via public JSON API.
API docs: https://remoteok.com/api
No API key required. Returns up to ~100 current listings.
"""

import requests


_API_URL = "https://remoteok.com/api"
_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; JobPilot/1.0)"}


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    try:
        resp = requests.get(_API_URL, headers=_HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"RemoteOK API request failed: {e}") from e

    # First element is a legal notice dict, not a job — skip it
    raw = resp.json()
    jobs_raw = [item for item in raw if isinstance(item, dict) and "position" in item]

    jobs = []
    for item in jobs_raw:
        role = (item.get("position") or "").strip()
        company = (item.get("company") or "").strip()
        url = (item.get("url") or "").strip()
        jd_text = (item.get("description") or "").strip()

        if not role or not company:
            continue

        jobs.append({"company": company, "role": role, "url": url, "jd_text": jd_text})

    return jobs
