"""
AIJobster source — AI-focused jobs via aijobster.work Supabase API.

No auth required beyond the public anon JWT embedded in the site's JS bundle.
API: POST https://dqzefhtxrsxlxcednqfs.supabase.co/functions/v1/jobs-proxy
     body: {"page": N}  — returns 20 jobs per page, ordered by date desc.

8,000+ AI jobs. Descriptions are not available in the API; jd_text is
constructed from title, department, skills, and location fields.

If the JWT stops working, re-fetch it from the JS bundle:
  curl https://aijobster.work/assets/index-*.js | grep -oP 'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+'
"""

import re

import requests
from datetime import datetime, timezone, timedelta


_ENDPOINT = "https://dqzefhtxrsxlxcednqfs.supabase.co/functions/v1/jobs-proxy"
_BASE_URL = "https://aijobster.work"

# Public anon JWT — designed to be client-side readable (Supabase anon key).
# Refresh if requests start returning 401 by re-running _get_jwt() without a cache.
_ANON_JWT = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRxemVmaHR4cnN4bHhjZWRucWZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM1MTg0MTAsImV4cCI6MjA3OTA5NDQxMH0"
    ".BnAIM59CXOAARmFJYn3VhFxcbLIwTbVxXjURSIO-9lg"
)


def _get_jwt(source_cfg: dict) -> str:
    """Return JWT from source_cfg override, cached constant, or re-fetch from JS bundle."""
    if source_cfg and source_cfg.get("jwt"):
        return source_cfg["jwt"]
    return _ANON_JWT


def _refresh_jwt() -> str:
    """Re-fetch JWT from the live JS bundle (call if _ANON_JWT starts returning 401)."""
    from curl_cffi import requests as cffi
    r = cffi.get(f"{_BASE_URL}/", impersonate="chrome", timeout=15)
    scripts = re.findall(r'src="(/assets/index-[^"]+\.js)"', r.text)
    if not scripts:
        raise RuntimeError("aijobster: could not find JS bundle URL")
    bundle = cffi.get(f"{_BASE_URL}{scripts[0]}", impersonate="chrome", timeout=20)
    jwts = re.findall(r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+', bundle.text)
    if not jwts:
        raise RuntimeError("aijobster: could not extract JWT from JS bundle")
    return jwts[0]


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    jwt = _get_jwt(source_cfg or {})
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json",
    }

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    kw_lower = keywords.lower()
    kw_terms = [t.strip() for t in kw_lower.replace(",", " ").split() if len(t.strip()) > 2]

    jobs_out: list[dict] = []
    page = 1

    while True:
        resp = requests.post(_ENDPOINT, json={"page": page}, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        batch = data.get("jobs", [])
        if not batch:
            break

        all_old = True
        for item in batch:
            date_str = item.get("date_posted") or ""
            if date_str:
                try:
                    posted = datetime.fromisoformat(date_str).replace(tzinfo=timezone.utc)
                    if posted < cutoff:
                        continue
                    all_old = False
                except ValueError:
                    all_old = False
            else:
                all_old = False

            title = (item.get("job_title") or "").strip()
            company = (item.get("company_name") or "").strip()
            if not title or not company:
                continue

            job_url = (item.get("job_url") or "").strip()
            if not job_url:
                slug = (item.get("slug_url") or "").strip("/")
                job_url = f"{_BASE_URL}/{slug}" if slug else ""

            # Construct jd_text from available structured fields
            parts = [title]
            if item.get("department"):
                parts.append(f"Department: {item['department']}")
            if item.get("ai_category"):
                parts.append(f"Category: {item['ai_category']}")
            skills = [s for s in (item.get("skills") or []) if s and s.strip()]
            if skills:
                parts.append(f"Skills: {', '.join(skills)}")
            locations = [l for l in (item.get("work_location") or []) if l and l.strip()]
            if locations:
                parts.append(f"Location: {', '.join(locations)}")
            if item.get("is_remote"):
                parts.append(f"Remote: {item['is_remote']}")
            jd_text = "\n".join(parts)

            # Keyword filter — title or skills must contain at least one term
            searchable = (title + " " + " ".join(skills)).lower()
            if kw_terms and not any(t in searchable for t in kw_terms):
                continue

            jobs_out.append({
                "company": company,
                "role": title,
                "url": job_url,
                "jd_text": jd_text,
            })

        if all_old:
            break
        page += 1

    return jobs_out
