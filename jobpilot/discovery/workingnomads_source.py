"""
Working Nomads source — global remote jobs via public JSON API.
API docs: https://www.workingnomads.com/api/exposed_jobs/
No API key required. Returns all current listings in one call.
"""

import requests
from datetime import datetime, timezone, timedelta


_API_URL = "https://www.workingnomads.com/api/exposed_jobs/"


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    try:
        resp = requests.get(_API_URL, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Working Nomads API request failed: {e}") from e

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    jobs = []

    for item in resp.json():
        role = (item.get("title") or "").strip()
        company = (item.get("company_name") or "").strip()
        url = (item.get("url") or "").strip()
        jd_text = (item.get("description") or "").strip()
        pub_date_str = item.get("pub_date") or ""

        if not role or not company:
            continue

        # Date filter
        if pub_date_str:
            try:
                pub_date = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00"))
                if pub_date < cutoff:
                    continue
            except ValueError:
                pass

        jobs.append({"company": company, "role": role, "url": url, "jd_text": jd_text})

    return jobs
