"""
Playwright source — scrapes JS-rendered career pages that block simple HTTP scrapers.
Supports three site types:
  phenom     — Phenom People ATS (NTT Data, IBM). Reads data attributes directly.
  cognizant  — Cognizant custom careers site.
  ripplehire — RippleHire ATS (LTIMindtree).

Each entry in profile.yaml playwright_companies requires:
  name: display name
  url:  full search URL including filters
  site: phenom | cognizant | ripplehire
"""

import re

_ALLOWED_LOCATION_TERMS = [
    "uk", "united kingdom", "england", "scotland", "wales",
    "london", "manchester", "edinburgh", "cambridge", "bristol",
    "birmingham", "leeds", "sheffield", "liverpool", "oxford",
    "reading", "brighton", "glasgow", "belfast", "cardiff",
    "spain", "serbia", "italy", "netherlands", "ireland",
    "sweden", "norway", "denmark", "finland", "slovenia", "switzerland",
    "remote", "worldwide", "anywhere", "hybrid",
]

_BROWSER = None


def _get_browser():
    global _BROWSER
    if _BROWSER is None or not _BROWSER.is_connected():
        from playwright.sync_api import sync_playwright
        _pw = sync_playwright().start()
        _BROWSER = _pw.chromium.launch(args=["--no-sandbox"])
    return _BROWSER


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    companies = getattr(config, "playwright_companies", [])
    if not companies:
        return []

    kw_list = [k.lower() for k in keywords.split() if k]
    results = []

    browser = _get_browser()
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    for company in companies:
        name = company.get("name", "")
        url  = company.get("url", "")
        site = company.get("site", "")
        if not name or not url or not site:
            continue

        page = ctx.new_page()
        try:
            jobs = _scrape(page, name, url, site)
        except Exception:
            jobs = []
        finally:
            page.close()

        for job in jobs:
            title = job.get("role", "")
            if not title:
                continue
            if kw_list and not any(kw in title.lower() for kw in kw_list):
                continue
            loc = job.get("location", "")
            if loc and not _is_allowed_location(loc):
                continue
            results.append({
                "company":  name,
                "role":     title,
                "url":      job.get("url", ""),
                "jd_text":  "",
                "location": loc,
            })

    ctx.close()
    return results


def _scrape(page, name: str, url: str, site: str) -> list[dict]:
    if site == "phenom":
        return _scrape_phenom(page, url)
    elif site == "cognizant":
        return _scrape_cognizant(page, url)
    elif site == "ripplehire":
        return _scrape_ripplehire(page, url)
    return []


# ── Phenom People (NTT Data) ─────────────────────────────────────────────────

def _scrape_phenom(page, url: str) -> list[dict]:
    page.goto(url, timeout=30000, wait_until="domcontentloaded")
    page.wait_for_selector("a[data-ph-at-id='job-link']", timeout=15000)

    links = page.query_selector_all("a[data-ph-at-id='job-link']")
    jobs = []
    for link in links:
        title = link.get_attribute("data-ph-at-job-title-text") or link.inner_text().strip()
        loc   = link.get_attribute("data-ph-at-job-location-text") or ""
        href  = link.get_attribute("href") or ""
        if title:
            jobs.append({"role": title, "location": loc, "url": href})
    return jobs


# ── Cognizant ────────────────────────────────────────────────────────────────

def _scrape_cognizant(page, url: str) -> list[dict]:
    base = "https://careers.cognizant.com"
    page.goto(url, timeout=30000, wait_until="domcontentloaded")
    page.wait_for_selector(".card", timeout=15000)

    cards = page.query_selector_all(".card")
    jobs = []
    for card in cards:
        title_el = card.query_selector("h2 a, .card-title a")
        if not title_el:
            continue
        title = title_el.inner_text().strip()
        href  = title_el.get_attribute("href") or ""
        # Location is first item in card-meta list
        meta_items = card.query_selector_all(".card-meta li, [class*=meta] li")
        loc = meta_items[0].inner_text().strip() if meta_items else ""
        # Clean up repeated country name (e.g. "London,UK, United Kingdom, United Kingdom")
        loc = loc.split(",")[0].strip() if loc else ""
        jobs.append({"role": title, "location": loc, "url": base + href if href.startswith("/") else href})
    return jobs


# ── RippleHire (LTIMindtree) ─────────────────────────────────────────────────

def _scrape_ripplehire(page, url: str) -> list[dict]:
    base = re.match(r"(https://[^/]+/candidate/\?[^#]+)", url)
    base_url = base.group(1) if base else url.split("#")[0]

    page.goto(url, timeout=30000, wait_until="domcontentloaded")
    page.wait_for_selector("li[id='row']", timeout=15000)

    rows = page.query_selector_all("li[id='row']")
    jobs = []
    for row in rows:
        title_el = row.query_selector("a.job-title")
        if not title_el:
            continue
        title = title_el.inner_text().strip()
        href  = title_el.get_attribute("href") or ""
        # Location is third li in list-job section
        loc_items = row.query_selector_all("div.row.list-job li")
        loc = loc_items[2].inner_text().strip() if len(loc_items) >= 3 else ""
        job_url = base_url + href if href.startswith("#") else href
        jobs.append({"role": title, "location": loc, "url": job_url})
    return jobs


def _is_allowed_location(loc: str) -> bool:
    lower = loc.lower()
    return any(term in lower for term in _ALLOWED_LOCATION_TERMS)
