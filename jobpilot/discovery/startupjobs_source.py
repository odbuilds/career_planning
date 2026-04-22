"""
startup.jobs source — startup job board with AI-specific categories.

Uses curl_cffi to bypass Cloudflare. Scrapes AI-relevant category pages:
  /ai-jobs, /machine-learning-jobs, /llm-jobs, /nlp-jobs

Each category page returns ~20 SSR-rendered jobs with title, company, location
and date in the listing HTML. Detail pages are fetched for jobs within the
date window to get the full JD text.
"""

import re
from datetime import datetime, timezone, timedelta

from bs4 import BeautifulSoup
from curl_cffi import requests as cffi


_BASE = "https://startup.jobs"
_CATEGORIES = ["/ai-jobs", "/machine-learning-jobs", "/llm-jobs", "/nlp-jobs"]
_JOB_LINK_RE = re.compile(r"^/[a-z0-9-]+-\d{6,}$")
_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC)")


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    categories = (source_cfg or {}).get("categories", _CATEGORIES)

    seen_slugs: set[str] = set()
    candidates: list[dict] = []  # (slug, title, company, posted_at)

    session = cffi.Session()

    for cat in categories:
        try:
            r = session.get(f"{_BASE}{cat}", impersonate="chrome", timeout=15)
            r.raise_for_status()
        except Exception:
            continue

        soup = BeautifulSoup(r.text, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if not _JOB_LINK_RE.match(href) or href in seen_slugs:
                continue
            seen_slugs.add(href)

            title = a.get_text(strip=True)
            if not title:
                continue

            # Parent block contains company name and date
            parent = a.find_parent()
            ctx = parent.get_text(separator="|", strip=True) if parent else ""
            parts = [p.strip() for p in ctx.split("|") if p.strip() and p.strip() not in ("·", ",", "Bookmark", "Apply")]

            company = ""
            posted_at = None

            date_match = _DATE_RE.search(ctx)
            if date_match:
                try:
                    posted_at = datetime.strptime(date_match.group(1), "%Y-%m-%d %H:%M:%S UTC").replace(tzinfo=timezone.utc)
                except ValueError:
                    pass

            # Company is the second meaningful part (after title)
            for part in parts:
                if part != title and not _DATE_RE.match(part) and len(part) > 1:
                    company = part
                    break

            if posted_at and posted_at < cutoff:
                continue

            candidates.append({
                "slug": href,
                "title": title,
                "company": company,
                "posted_at": posted_at,
            })

    jobs_out: list[dict] = []
    for c in candidates:
        detail = _fetch_detail(session, c["slug"])
        company = detail.get("company") or c["company"]
        if not company:
            continue
        jobs_out.append({
            "company": company,
            "role": c["title"],
            "url": f"{_BASE}{c['slug']}",
            "jd_text": detail.get("jd_text", c["title"]),
        })

    return jobs_out


def _fetch_detail(session, slug: str) -> dict:
    try:
        r = session.get(f"{_BASE}{slug}", impersonate="chrome", timeout=15)
        r.raise_for_status()
    except Exception:
        return {}

    soup = BeautifulSoup(r.text, "html.parser")
    main = soup.find("main") or soup

    h1 = main.find("h1")
    company = ""
    if h1:
        prev = h1.find_previous_sibling()
        if prev:
            company = prev.get_text(strip=True)

    # JD: all paragraphs and list items inside main
    jd_parts = [el.get_text(strip=True) for el in main.find_all(["p", "li", "h2", "h3"]) if el.get_text(strip=True)]
    jd_text = "\n".join(jd_parts)

    return {"company": company, "jd_text": jd_text[:4000]}
