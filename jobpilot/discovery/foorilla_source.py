"""
Foorilla source — topic-filtered tech jobs via foorilla.com.

Two auth modes (in priority order):

  1. API key  — set FOORILLA_API_KEY in .env.
     Uses REST API at /api/v1/hiring/job/ with full company data.
     Get a key at foorilla.com/account/ (paid).

  2. Session cookie — set FOORILLA_SESSION in .env.
     Uses the HTMX web UI. Free account is sufficient.
     To get the cookie value:
       a. Log in at foorilla.com
       b. Open DevTools → Application → Cookies → foorilla.com
       c. Copy the value of the 'sessionid' cookie
       d. Add to .env:  FOORILLA_SESSION=<value>
     Session cookies expire after a few weeks — refresh as needed.

Topics targeted (edit TOPIC_IDS to tune):
  11  — Artificial Intelligence (1,657 jobs)
  24  — Natural Language Processing (150 jobs)
  31  — Robotic Process Automation (455 jobs)
  56  — Autonomous Systems (977 jobs)
  85  — Workflow Automation (7,095 jobs)
"""

import os
import re
import requests
from bs4 import BeautifulSoup
from curl_cffi import requests as cffi_requests
from datetime import datetime, timezone, timedelta


_BASE_API = "https://foorilla.com/api/v1"
_BASE_WEB = "https://foorilla.com"

TOPIC_IDS = [11, 24, 31, 56, 85]


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    api_key = getattr(config, "foorilla_api_key", "") or os.environ.get("FOORILLA_API_KEY", "")
    session_cookie = getattr(config, "foorilla_session", "") or os.environ.get("FOORILLA_SESSION", "")

    if api_key:
        return _fetch_via_api(api_key, days)
    elif session_cookie:
        return _fetch_via_session(session_cookie, days)
    else:
        raise RuntimeError(
            "Foorilla needs auth: set FOORILLA_API_KEY (paid) or FOORILLA_SESSION "
            "(free — copy 'sessionid' cookie from browser after logging in to foorilla.com)"
        )


# ── API key path ──────────────────────────────────────────────────────────────

def _fetch_via_api(api_key: str, days: int) -> list[dict]:
    published_after = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    headers = {"Api-Key": api_key}
    seen_ids: set[int] = set()
    jobs_out: list[dict] = []

    for topic_id in TOPIC_IDS:
        page = 1
        while True:
            resp = requests.get(
                f"{_BASE_API}/hiring/job/",
                params={
                    "topic": topic_id,
                    "published_after": published_after,
                    "language": "en",
                    "page": page,
                    "page_size": 100,
                },
                headers=headers,
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            results = data.get("results", [])
            if not results:
                break

            for item in results:
                job_id = item.get("id")
                if job_id in seen_ids:
                    continue
                seen_ids.add(job_id)

                company = (item.get("company") or {}).get("name", "").strip()
                role = (item.get("title") or "").strip()
                if not company or not role:
                    continue

                url = item.get("apply_url") or f"{_BASE_WEB}/hiring/jobs/{job_id}/"
                tags = [t.get("name", "") for t in (item.get("tags") or []) if t.get("name")]
                topics = [t.get("name", "") for t in (item.get("topics") or []) if t.get("name")]
                jd_parts = []
                if item.get("location"):
                    jd_parts.append(f"Location: {item['location']}")
                if tags:
                    jd_parts.append(f"Skills: {', '.join(tags)}")
                if topics:
                    jd_parts.append(f"Topics: {', '.join(topics)}")
                if item.get("has_remote"):
                    jd_parts.append("Remote: yes")

                jobs_out.append({
                    "company": company,
                    "role": role,
                    "url": url,
                    "jd_text": "\n".join(jd_parts),
                })

            if page >= data.get("pages", 1):
                break
            page += 1

    return jobs_out


# ── Session cookie path ───────────────────────────────────────────────────────

def _fetch_via_session(session_cookie: str, days: int) -> list[dict]:
    session = cffi_requests.Session()
    session.cookies.set("sessionid", session_cookie, domain="foorilla.com")

    # Get CSRF token
    r0 = session.get(f"{_BASE_WEB}/hiring/", impersonate="chrome", timeout=15)
    soup0 = BeautifulSoup(r0.text, "html.parser")
    body_hx = (soup0.body or soup0).get("hx-headers", "") if hasattr(soup0, "get") else ""
    if not body_hx and soup0.body:
        body_hx = soup0.body.get("hx-headers", "")
    csrf_match = re.search(r"X-CSRFToken.*?([A-Za-z0-9]{20,})", body_hx)
    if not csrf_match:
        raise RuntimeError("Foorilla: could not extract CSRF token — session cookie may be expired")
    token = csrf_match.group(1)

    base_hdrs = {
        "HX-Request": "true",
        "HX-Current-URL": f"{_BASE_WEB}/hiring/",
        "X-CSRFToken": token,
        "X-Screen": "D",
        "Referer": f"{_BASE_WEB}/hiring/",
    }

    cutoff = datetime.now(timezone.utc).timestamp() - days * 86400
    seen_slugs: set[str] = set()
    jobs_out: list[dict] = []

    for topic_id in TOPIC_IDS:
        # POST topic selection — sets filter in session
        session.post(
            f"{_BASE_WEB}/topics/hiring/",
            data={"topic": str(topic_id)},
            headers={**base_hdrs, "HX-Target": "mc_1", "Content-Type": "application/x-www-form-urlencoded"},
            impersonate="chrome",
            timeout=15,
        )

        # Fetch job list
        r = session.get(
            f"{_BASE_WEB}/hiring/jobs/",
            headers=base_hdrs,
            impersonate="chrome",
            timeout=15,
        )
        soup = BeautifulSoup(r.text, "html.parser")

        for li in soup.find_all("li", class_="list-group-item"):
            link = li.find("a", attrs={"hx-get": re.compile(r"/hiring/jobs/\w")})
            if not link:
                continue
            slug_path = link.get("hx-get", "")
            slug = slug_path.strip("/").split("/")[-1]
            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)

            role = link.get_text(strip=True)
            if not role:
                continue

            # Age check from "Xh ago" / "Xd ago" text
            age_text = li.get_text(separator=" ")
            if not _within_days(age_text, cutoff):
                continue

            # Fetch detail page to get company name + JD
            detail = _fetch_detail(session, slug_path, base_hdrs)
            company = detail.get("company", "")
            if not company:
                continue

            jobs_out.append({
                "company": company,
                "role": role,
                "url": f"{_BASE_WEB}{slug_path}",
                "jd_text": detail.get("jd_text", ""),
            })

    return jobs_out


def _fetch_detail(session, path: str, base_hdrs: dict) -> dict:
    try:
        r = session.get(
            f"{_BASE_WEB}{path}",
            headers=base_hdrs,
            impersonate="chrome",
            timeout=15,
        )
        soup = BeautifulSoup(r.text, "html.parser")

        # Company name: <a href="/hiring/companies/">@ CompanyName</a>
        company = ""
        for a in soup.find_all("a", href="/hiring/companies/"):
            txt = a.get_text(strip=True)
            if txt.startswith("@"):
                name = txt[1:].strip()
                if "..." not in name:
                    company = name
                break

        # JD text: largest text block
        jd = soup.get_text(separator="\n", strip=True)
        return {"company": company, "jd_text": jd[:3000]}
    except Exception:
        return {}


def _within_days(text: str, cutoff_ts: float) -> bool:
    """Return True if the age string (e.g. '3h ago', '2d ago') is within cutoff."""
    now = datetime.now(timezone.utc).timestamp()
    m = re.search(r"(\d+)\s*(h|d|w)\s*ago", text, re.IGNORECASE)
    if not m:
        return True  # unknown age — include it
    n, unit = int(m.group(1)), m.group(2).lower()
    delta = n * {"h": 3600, "d": 86400, "w": 604800}[unit]
    return (now - delta) >= cutoff_ts
