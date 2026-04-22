"""
CV Library source — UK job board, HTML scraping.
Note: CV Library is server-side rendered so BS4 scraping works, but
selectors may need updating if the site structure changes.
"""

import requests
from bs4 import BeautifulSoup


_SEARCH_URL = "https://www.cv-library.co.uk/search-jobs"
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    params = {
        "q": keywords,
        "l": location or "United Kingdom",
        "d": min(days, 30),
        "us": 1,      # sort by date
        "pg": 1,
    }

    try:
        resp = requests.get(_SEARCH_URL, params=params, headers=_HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"CV Library request failed: {e}") from e

    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = []

    for card in soup.select("article.job"):
        title_el = card.select_one("h2 a, h3 a")
        company_el = card.select_one(".job-company, [data-company]")
        link_el = card.select_one("a[href]")

        role = title_el.get_text(strip=True) if title_el else ""
        company = company_el.get_text(strip=True) if company_el else ""
        href = link_el["href"] if link_el else ""
        url = href if href.startswith("http") else f"https://www.cv-library.co.uk{href}"

        if role and company:
            jobs.append({"company": company, "role": role, "url": url, "jd_text": ""})

    return jobs
