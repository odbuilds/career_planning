"""
The Rundown AI Jobs source — AI-focused remote jobs embedded as window.jobsList.
No API key required. Paginates /jobs?remote=true&page=N until jobs age out.
"""

import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone


_BASE_URL = "https://jobs.therundown.ai/jobs"
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
_MAX_PAGES = 10


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    cutoff = datetime.now(timezone.utc).timestamp() - days * 86400
    jobs_out = []
    kw_lower = keywords.lower()

    for page in range(1, _MAX_PAGES + 1):
        try:
            resp = requests.get(
                _BASE_URL,
                params={"remote": "true", "page": page},
                headers=_HEADERS,
                timeout=15,
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            if page == 1:
                raise RuntimeError(f"TheRundown request failed: {e}") from e
            break

        page_jobs = _extract_jobs(resp.text)
        if not page_jobs:
            break

        all_old = True
        for item in page_jobs:
            posted_ts = _parse_ts(item.get("posted_at", ""))
            if posted_ts and posted_ts < cutoff:
                continue
            all_old = False

            company = (item.get("employer") or {}).get("name", "").strip()
            role = (item.get("title") or "").strip()
            if not company or not role:
                continue

            # Keyword filter on title + description since source has no server-side search
            jd = item.get("description") or ""
            if kw_lower and kw_lower not in role.lower() and kw_lower not in jd.lower():
                continue

            url = item.get("apply_to") or f"https://jobs.therundown.ai{item.get('job_details_path', '')}"
            jobs_out.append({"company": company, "role": role, "url": url, "jd_text": jd})

        if all_old:
            break

    return jobs_out


def _extract_jobs(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    jobs = []
    for script in soup.find_all("script"):
        txt = script.string or ""
        if "window.jobsList" not in txt:
            continue
        for match in re.findall(r"window\.jobsList\.concat\((\[.*?\])\);", txt, re.DOTALL):
            try:
                jobs.extend(json.loads(match))
            except json.JSONDecodeError:
                pass
        break
    return jobs


def _parse_ts(s: str) -> float | None:
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return dt.timestamp()
    except ValueError:
        return None
