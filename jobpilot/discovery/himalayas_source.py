"""
Himalayas source — global remote jobs via Himalayas public API.
No API key required.
API: https://himalayas.app/jobs/api
"""

import requests


_API_URL = "https://himalayas.app/jobs/api"
_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; JobPilot/1.0)"}


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    try:
        resp = requests.get(
            _API_URL,
            params={"q": keywords, "limit": 100},
            headers=_HEADERS,
            timeout=15,
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Himalayas request failed: {e}") from e

    jobs = []
    for item in resp.json().get("jobs", []):
        company = (item.get("companyName") or "").strip()
        role = (item.get("title") or "").strip()
        if not company or not role:
            continue
        url = item.get("applicationLink") or item.get("guid") or ""
        jd = item.get("description") or item.get("excerpt") or ""
        jobs.append({"company": company, "role": role, "url": url, "jd_text": jd})

    return jobs
