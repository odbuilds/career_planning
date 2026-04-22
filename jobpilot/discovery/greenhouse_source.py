"""
Watched Companies source — polls public job boards for companies in profile.yaml watched_companies.
Supports Greenhouse, Lever, and Ashby ATS platforms.
No API key required (all public endpoints).

Greenhouse requires a second request per job to fetch the full JD content.
Lever and Ashby return description in the listing response.
"""

import re
import requests


_GREENHOUSE_JOBS = "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
_GREENHOUSE_JOB  = "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs/{job_id}"
_LEVER           = "https://api.lever.co/v0/postings/{slug}?mode=json"
_ASHBY           = "https://api.ashbyhq.com/posting-api/job-board/{slug}"


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    kw_list = [k.lower() for k in keywords.split() if k]
    jobs = []

    for company in config.watched_companies:
        name = company["name"]
        slug = company["slug"]
        ats = company["ats"]

        try:
            raw_jobs = _fetch_listing(ats, slug)
        except Exception:
            continue

        for job in raw_jobs:
            title = job.get("role", "")
            if kw_list and not any(kw in title.lower() for kw in kw_list):
                continue

            # Fetch full JD for Greenhouse (listing endpoint omits content)
            jd_text = job.get("jd_text", "")
            if ats == "greenhouse" and not jd_text and job.get("job_id"):
                jd_text = _fetch_greenhouse_jd(slug, job["job_id"])

            jobs.append({
                "company": name,
                "role": title,
                "url": job.get("url", ""),
                "jd_text": jd_text,
            })

    return jobs


def _fetch_listing(ats: str, slug: str) -> list[dict]:
    if ats == "greenhouse":
        resp = requests.get(_GREENHOUSE_JOBS.format(slug=slug), timeout=10)
        resp.raise_for_status()
        return [
            {
                "role":   j.get("title", ""),
                "url":    j.get("absolute_url", ""),
                "job_id": j.get("id", ""),
                "jd_text": "",  # fetched separately after keyword filter
            }
            for j in resp.json().get("jobs", [])
        ]

    elif ats == "lever":
        resp = requests.get(_LEVER.format(slug=slug), timeout=10)
        resp.raise_for_status()
        return [
            {
                "role":    j.get("text", ""),
                "url":     j.get("hostedUrl", ""),
                "jd_text": j.get("descriptionPlain", "") or _strip_html(j.get("description", "")),
            }
            for j in resp.json()
        ]

    elif ats == "ashby":
        resp = requests.get(_ASHBY.format(slug=slug), timeout=10)
        resp.raise_for_status()
        return [
            {
                "role":    j.get("title", ""),
                "url":     j.get("jobUrl", ""),
                "jd_text": j.get("descriptionPlain", "") or _strip_html(j.get("descriptionHtml", "")),
            }
            for j in resp.json().get("jobs", [])
        ]

    return []


def _fetch_greenhouse_jd(slug: str, job_id) -> str:
    try:
        resp = requests.get(
            _GREENHOUSE_JOB.format(slug=slug, job_id=job_id),
            timeout=10,
        )
        resp.raise_for_status()
        html = resp.json().get("content", "")
        return _strip_html(html)
    except Exception:
        return ""


def _strip_html(html: str) -> str:
    if not html:
        return ""
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()
