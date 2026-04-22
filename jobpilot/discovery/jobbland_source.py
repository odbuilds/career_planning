"""
Jobbland source (jobbland.se) — Swedish job board, HTML scraping.
Sweden-only. Uses natural language search.
"""

import requests
from bs4 import BeautifulSoup


_SEARCH_URL = "https://jobbland.se/lediga-jobb"
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "sv-SE,sv;q=0.9,en;q=0.8",
}


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    params = {"q": keywords}

    try:
        resp = requests.get(_SEARCH_URL, params=params, headers=_HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Jobbland request failed: {e}") from e

    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = []

    for card in soup.select("article, .job-card, [class*='JobCard'], [class*='job-item']"):
        role_el = card.select_one("h2, h3, [class*='title']")
        company_el = card.select_one("[class*='company'], [class*='employer']")
        link_el = card.select_one("a[href]")

        role = role_el.get_text(strip=True) if role_el else ""
        company = company_el.get_text(strip=True) if company_el else ""
        href = link_el["href"] if link_el else ""
        url = href if href.startswith("http") else f"https://jobbland.se{href}"

        if role and company:
            jobs.append({"company": company, "role": role, "url": url, "jd_text": ""})

    return jobs
