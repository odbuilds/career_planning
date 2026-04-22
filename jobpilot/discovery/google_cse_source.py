"""
Serper.dev source — surfaces job postings via Google search results (Serper.dev API).

Useful for finding roles on company career pages, Workday/Taleo/iCIMS/SAP instances,
and niche job boards not covered by other discovery sources. Complements the existing
Google Jobs (jobspy) source which only searches the Google Jobs tab.

Setup (one-time):
  1. Sign up at https://serper.dev — 2,500 free searches included
  2. Copy your API key from the dashboard
  3. Add to jobpilot/.env:
       SERPER_API_KEY=your_api_key

Each fetch() call uses 1 search credit and returns up to 10 results.
JD fetching is disabled by default (uses snippet as jd_text) — enable with fetch_jd: true
in profile.yaml source config, but note it adds ~10 HTTP requests per run.
"""

import requests
from core.jd_fetch import fetch_jd as _fetch_jd

_API_URL = "https://google.serper.dev/search"


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    api_key = getattr(config, "serper_api_key", "")
    if not api_key:
        raise RuntimeError(
            "SERPER_API_KEY must be set in .env — sign up free at https://serper.dev"
        )

    source_cfg = source_cfg or {}
    do_fetch_jd: bool = source_cfg.get("fetch_jd", False)

    loc_part = f" {location}" if location else ""
    query = f"{keywords} jobs{loc_part}"
    extra = source_cfg.get("extra_query", "")
    if extra:
        query = f"{query} {extra}"

    try:
        resp = requests.post(
            _API_URL,
            headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
            json={"q": query, "num": 10},
            timeout=15,
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Serper request failed: {e}") from e

    jobs = []
    for item in resp.json().get("organic", []):
        url = item.get("link", "")
        if not url:
            continue

        role, company = _parse_title(item.get("title", ""))
        jd_text = item.get("snippet", "")

        if do_fetch_jd:
            fetched = _fetch_jd(url)
            if not fetched.get("error"):
                jd_text = fetched.get("jd_text") or jd_text
                if not role:
                    role = fetched.get("role", "")
                if not company:
                    company = fetched.get("company", "")

        if not role or not company:
            continue

        jobs.append({"company": company, "role": role, "url": url, "jd_text": jd_text})

    return jobs


def _parse_title(title: str) -> tuple[str, str]:
    """
    Parse search result titles into (role, company).
    Handles common formats: "Role - Company", "Role | Company", "Role at Company".
    """
    for sep in (" | ", " – ", " - "):
        if sep in title:
            parts = title.split(sep)
            return parts[0].strip(), parts[-1].strip()
    if " at " in title:
        parts = title.split(" at ", 1)
        return parts[0].strip(), parts[1].strip()
    return title.strip(), ""
