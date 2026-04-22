"""
EuRemoteJobs source — EU-focused remote jobs via WP Job Manager REST API.
No API key required. Uses curl_cffi to bypass Cloudflare.
API: https://euremotejobs.com/wp-json/wp/v2/job-listings
"""

from datetime import datetime, timezone
from curl_cffi import requests as cffi_requests
from bs4 import BeautifulSoup


_API_URL = "https://euremotejobs.com/wp-json/wp/v2/job-listings"
_PER_PAGE = 100
_MAX_PAGES = 5


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    cutoff = datetime.now(timezone.utc).timestamp() - days * 86400
    kw_lower = keywords.lower()
    jobs_out = []

    for page in range(1, _MAX_PAGES + 1):
        try:
            resp = cffi_requests.get(
                _API_URL,
                params={"per_page": _PER_PAGE, "page": page, "orderby": "date", "order": "desc"},
                impersonate="chrome",
                timeout=20,
            )
            resp.raise_for_status()
        except Exception as e:
            if page == 1:
                raise RuntimeError(f"EuRemoteJobs request failed: {e}") from e
            break

        items = resp.json()
        if not items:
            break

        all_old = True
        for item in items:
            posted_ts = _parse_ts(item.get("date", ""))
            if posted_ts and posted_ts < cutoff:
                continue
            all_old = False

            company = ((item.get("meta") or {}).get("_company_name") or "").strip()
            role = (item.get("title") or {}).get("rendered", "").strip()
            if not company or not role:
                continue

            # Keyword filter on role + JD text (no server-side search on this endpoint)
            jd_html = (item.get("content") or {}).get("rendered", "")
            jd_text = BeautifulSoup(jd_html, "html.parser").get_text(" ", strip=True)
            if kw_lower and kw_lower not in role.lower() and kw_lower not in jd_text.lower():
                continue

            url = item.get("link") or ""
            jobs_out.append({"company": company, "role": role, "url": url, "jd_text": jd_text})

        if all_old:
            break

    return jobs_out


def _parse_ts(s: str) -> float | None:
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.timestamp()
    except ValueError:
        return None
