"""
JD fetcher — given a job posting URL, returns extracted text and best-guess company/role.
Uses requests + BeautifulSoup. Handles common ATS patterns (Greenhouse, Lever, Ashby, Workday)
and generic HTML pages.
"""

import re
import requests
from bs4 import BeautifulSoup


_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-GB,en;q=0.9",
}

# CSS selectors tried in order — first match wins
_JD_SELECTORS = [
    # Greenhouse
    "#content",
    ".job__description",
    # Lever
    ".posting-description",
    ".posting-requirements",
    # Ashby
    "[data-testid='job-description']",
    # Workday
    ".css-16i4snm",
    # Reed
    ".description",
    # Generic
    "[class*='job-description']",
    "[class*='jobDescription']",
    "[class*='job_description']",
    "[id*='job-description']",
    "[id*='jobDescription']",
    "article",
    "main",
]

_TITLE_SELECTORS = [
    "h1.posting-headline",   # Lever
    "h1.app-title",          # Greenhouse
    "h1[data-testid='job-title']",  # Ashby
    "h1",
]

_COMPANY_SELECTORS = [
    ".company-name",
    "[class*='company']",
    "[itemprop='hiringOrganization']",
]


def fetch_jd(url: str) -> dict:
    """
    Fetch a job posting URL and extract job description, role, and company.

    Returns:
        {
            "jd_text": str,   # extracted plain text
            "role": str,      # best-guess title (may be empty)
            "company": str,   # best-guess company (may be empty)
            "error": str,     # non-empty if fetch failed
        }
    """
    result = {"jd_text": "", "role": "", "company": "", "error": ""}

    try:
        resp = requests.get(url, headers=_HEADERS, timeout=15, allow_redirects=True)
        resp.raise_for_status()
    except requests.RequestException as e:
        result["error"] = f"Could not fetch URL: {e}"
        return result

    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove noise
    for tag in soup.select("script, style, nav, header, footer, [aria-hidden='true']"):
        tag.decompose()

    # Extract JD text
    jd_el = None
    for selector in _JD_SELECTORS:
        jd_el = soup.select_one(selector)
        if jd_el and len(jd_el.get_text(strip=True)) > 100:
            break

    if jd_el:
        result["jd_text"] = _clean_text(jd_el.get_text(separator="\n"))
    else:
        # Fallback: body text
        result["jd_text"] = _clean_text(soup.get_text(separator="\n"))

    # Extract role / title
    for selector in _TITLE_SELECTORS:
        el = soup.select_one(selector)
        if el:
            text = el.get_text(strip=True)
            if text and len(text) < 120:
                result["role"] = text
                break

    # Try <title> tag as fallback for role
    if not result["role"] and soup.title:
        title = soup.title.get_text(strip=True)
        # Strip common suffixes: "Role | Company", "Role at Company", "Role - Company"
        for sep in [" | ", " at ", " - ", " – "]:
            if sep in title:
                result["role"] = title.split(sep)[0].strip()
                break
        else:
            result["role"] = title

    # Extract company
    for selector in _COMPANY_SELECTORS:
        el = soup.select_one(selector)
        if el:
            text = el.get_text(strip=True)
            if text and len(text) < 80:
                result["company"] = text
                break

    # Fallback: parse company from <title> "Role | Company" or "Role at Company"
    if not result["company"] and soup.title:
        title = soup.title.get_text(strip=True)
        for sep in [" | ", " – ", " - "]:
            if sep in title:
                parts = title.split(sep)
                if len(parts) >= 2:
                    result["company"] = parts[-1].strip()
                    break
        if not result["company"] and " at " in title:
            result["company"] = title.split(" at ")[-1].strip()

    return result


def _clean_text(text: str) -> str:
    # Collapse excessive blank lines
    lines = [line.rstrip() for line in text.splitlines()]
    cleaned = re.sub(r"\n{3,}", "\n\n", "\n".join(lines))
    return cleaned.strip()
