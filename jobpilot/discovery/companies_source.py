"""
Company watchlist source — searches LinkedIn globally per keyword and filters results
to companies in config.company_watchlist.

No API key required. Adds one global LinkedIn search per keyword per run.
Results are filtered post-fetch by fuzzy company name matching.
"""

import re
import pandas as pd

_UNSUPPORTED_COUNTRY_RE = re.compile(r',\s*(Serbia)$', re.IGNORECASE)

_ALLOWED_LOCATION_TERMS = [
    "uk", "united kingdom", "england", "scotland", "wales",
    "spain", "serbia", "italy",
    "sweden", "norway", "denmark", "finland", "slovenia",
    "remote", "worldwide", "anywhere",
]


def _is_allowed_location(loc: str) -> bool:
    lower = loc.lower()
    return any(term in lower for term in _ALLOWED_LOCATION_TERMS)


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    from jobspy import scrape_jobs

    watchlist = _build_index(config.company_watchlist)
    if not watchlist:
        return []

    is_remote = (source_cfg or {}).get("_is_remote", False)
    effective_location = "" if is_remote else _UNSUPPORTED_COUNTRY_RE.sub("", location).strip(", ")
    results_wanted = (source_cfg or {}).get("results_wanted", 200)

    try:
        df = scrape_jobs(
            site_name=["linkedin"],
            search_term=keywords,
            location=effective_location,
            results_wanted=results_wanted,
            hours_old=days * 24,
            is_remote=is_remote,
        )
    except Exception as e:
        if "Invalid country string" in str(e):
            return []
        raise RuntimeError(f"companies watchlist scrape failed: {e}") from e

    if df is None or df.empty:
        return []

    jobs = []
    for _, row in df.iterrows():
        raw_company = _str(row.get("company"))
        canonical = _match(raw_company, watchlist)
        if not canonical:
            continue
        role = _str(row.get("title"))
        if not role:
            continue
        loc = _str(row.get("location"))
        if not loc or not _is_allowed_location(loc):
            continue
        jobs.append({
            "company": canonical,
            "role": role,
            "url": _str(row.get("job_url")),
            "jd_text": _str(row.get("description")),
            "location": loc,
        })
    return jobs


def _build_index(watchlist: list[dict]) -> dict[str, str]:
    """Build normalised_key → canonical_name lookup."""
    return {_normalise(c["name"]): c["name"] for c in watchlist if c.get("name")}


def _match(raw: str, index: dict[str, str]) -> str | None:
    """Return canonical name if raw company name matches any watchlist entry."""
    if not raw:
        return None
    key = _normalise(raw)
    if key in index:
        return index[key]
    # Partial match — watchlist name contained in result name or vice versa
    for norm, canonical in index.items():
        if norm in key or key in norm:
            return canonical
    return None


def _normalise(name: str) -> str:
    return re.sub(r'\W+', '', name).lower()


def _str(val) -> str:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return ""
    return str(val).strip()
