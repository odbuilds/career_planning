"""
Remote Rocketship source (remoterocketship.com) — global remote jobs.
Claims 61% of listings are not on LinkedIn.
Uses HTML scraping with BeautifulSoup.
"""

import requests
from bs4 import BeautifulSoup


_SEARCH_URL = "https://www.remoterocketship.com/jobs"
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    params = {"search": keywords}

    try:
        resp = requests.get(_SEARCH_URL, params=params, headers=_HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Remote Rocketship request failed: {e}") from e

    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = []

    # Job cards are in <a> tags with job info as child elements
    for card in soup.select("a[href*='/jobs/']"):
        role_el = card.select_one("h2, h3, .job-title, [class*='title']")
        company_el = card.select_one(".company, [class*='company']")

        role = role_el.get_text(strip=True) if role_el else ""
        company = company_el.get_text(strip=True) if company_el else ""
        href = card.get("href", "")
        url = href if href.startswith("http") else f"https://www.remoterocketship.com{href}"

        if role and company:
            jobs.append({"company": company, "role": role, "url": url, "jd_text": ""})

    return jobs
