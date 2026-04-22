"""
Remotive source — global remote jobs via Remotive public API.
No API key required.
API docs: https://remotive.com/api/remote-jobs
"""

import requests


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    try:
        resp = requests.get(
            "https://remotive.com/api/remote-jobs",
            params={"search": keywords, "limit": 100},
            timeout=15,
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Remotive API request failed: {e}") from e

    jobs = []
    for item in resp.json().get("jobs", []):
        company = (item.get("company_name") or "").strip()
        role = (item.get("title") or "").strip()
        if not company or not role:
            continue
        jobs.append({
            "company": company,
            "role": role,
            "url": item.get("url", ""),
            "jd_text": item.get("description", ""),
        })

    return jobs
