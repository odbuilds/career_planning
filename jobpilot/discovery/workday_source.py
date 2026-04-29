"""
Workday source — polls public Workday job boards for companies in config.workday_companies.
Uses Workday's undocumented but consistent CXS API (no auth required for public boards).

Each company entry in profile.yaml requires:
  name:    display name
  tenant:  Workday subdomain (e.g. "accenture")
  version: Workday instance version (e.g. "wd3", "wd103")
  jobsite: job board slug (e.g. "AccentureCareers")

To find a company's Workday details, visit their careers page, look for a URL like:
  https://{tenant}.{version}.myworkdayjobs.com/en-US/{jobsite}/jobs
then add {tenant}, {version}, {jobsite} to profile.yaml workday_companies.
"""

import re
import requests

_API = "https://{tenant}.{version}.myworkdayjobs.com/wday/cxs/{tenant}/{jobsite}/jobs"
_JOB_URL = "https://{tenant}.{version}.myworkdayjobs.com/en-US/{jobsite}{path}"
_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0",
}

_ALLOWED_LOCATION_TERMS = [
    "uk", "united kingdom", "england", "scotland", "wales",
    "spain", "serbia", "italy",
    "sweden", "norway", "denmark", "finland", "slovenia",
    "remote", "worldwide", "anywhere",
]


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    companies = getattr(config, "workday_companies", [])
    if not companies:
        return []

    kw_list = [k.lower() for k in keywords.split() if k]
    results = []

    for company in companies:
        name = company.get("name", "")
        tenant = company.get("tenant", "")
        version = company.get("version", "")
        jobsite = company.get("jobsite", "")
        if not all([name, tenant, version, jobsite]):
            continue

        try:
            # Use first keyword for API search; remaining terms filtered post-fetch
            search_term = keywords.split()[0] if keywords.strip() else "AI"
            jobs = _fetch_company(tenant, version, jobsite, search_term)
        except Exception:
            continue

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
                "company": name,
                "role": title,
                "url": job.get("url", ""),
                "jd_text": "",
                "location": loc,
            })

    return results


_PAGE_SIZE = 20  # Workday enforces a max of 20 per request


def _fetch_company(tenant: str, version: str, jobsite: str, search_text: str, max_results: int = 200) -> list[dict]:
    url = _API.format(tenant=tenant, version=version, jobsite=jobsite)
    jobs = []
    offset = 0
    while len(jobs) < max_results:
        body = {"appliedFacets": {}, "limit": _PAGE_SIZE, "offset": offset, "searchText": search_text}
        resp = requests.post(url, json=body, headers=_HEADERS, timeout=12)
        resp.raise_for_status()
        data = resp.json()
        postings = data.get("jobPostings", [])
        if not postings:
            break
        for j in postings:
            path = j.get("externalPath", "")
            job_url = _JOB_URL.format(tenant=tenant, version=version, jobsite=jobsite, path=path) if path else ""
            jobs.append({
                "role":     j.get("title", ""),
                "url":      job_url,
                "location": j.get("locationsText") or "",
            })
        total = data.get("total", 0)
        offset += _PAGE_SIZE
        if offset >= total:
            break
    return jobs


def _is_allowed_location(loc: str) -> bool:
    lower = loc.lower()
    return any(term in lower for term in _ALLOWED_LOCATION_TERMS)
