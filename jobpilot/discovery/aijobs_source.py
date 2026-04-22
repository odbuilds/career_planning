"""
AI Jobs source (aijobs.ai) — global AI/ML specialist job board.
Note: The site loads jobs via a JSON endpoint; this source uses that endpoint directly.
If the endpoint changes, fall back to HTML scraping.
"""

import requests


_API_URL = "https://aijobs.ai/api/jobs/"
_SEARCH_URL = "https://aijobs.ai/jobs/"
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Referer": "https://aijobs.ai/",
}


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    params = {"search": keywords, "page_size": 100}

    try:
        resp = requests.get(_API_URL, params=params, headers=_HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, ValueError) as e:
        raise RuntimeError(f"aijobs.ai request failed: {e}") from e

    # Handle both list and {"results": [...]} shapes
    items = data if isinstance(data, list) else data.get("results", data.get("jobs", []))

    jobs = []
    for item in items:
        company = (item.get("company") or item.get("company_name") or "").strip()
        role = (item.get("title") or item.get("position") or "").strip()
        if not company or not role:
            continue
        url = item.get("url") or item.get("apply_url") or item.get("link") or ""
        jd = item.get("description") or item.get("body") or ""
        jobs.append({"company": company, "role": role, "url": url, "jd_text": jd})

    return jobs
