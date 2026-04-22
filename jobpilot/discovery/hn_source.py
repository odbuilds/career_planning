"""
Hacker News "Who is Hiring" source.
Finds the latest monthly thread via Algolia, then fetches top-level comments
and filters those matching the search keywords.
No API key required.
"""

import re
import requests


_ALGOLIA_URL = "https://hn.algolia.com/api/v1/search"
_HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{id}.json"
_COMMENT_LIMIT = 150  # top-level comments to check


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    # Find the latest "Ask HN: Who is Hiring?" post
    post_id = _find_latest_thread()
    if not post_id:
        raise RuntimeError("Could not find HN Who is Hiring thread")

    # Get list of top-level comment IDs
    item = _get_item(post_id)
    kids = (item.get("kids") or [])[:_COMMENT_LIMIT]

    kw_list = [k.lower() for k in keywords.split() if k]
    jobs = []

    for kid_id in kids:
        comment = _get_item(kid_id)
        text = comment.get("text") or ""
        if not text:
            continue

        text_lower = text.lower()
        if not any(kw in text_lower for kw in kw_list):
            continue

        # HN hiring convention: first line is "Company | Role | Location | ..."
        # Strip HTML tags for the first line
        first_line = re.sub(r"<[^>]+>", "", text.split("<p>")[0]).strip()
        parts = [p.strip() for p in re.split(r"\s*\|\s*", first_line) if p.strip()]

        company = parts[0] if parts else "Unknown"
        role = parts[1] if len(parts) > 1 else first_line[:80]

        # Plain text body: strip HTML
        plain_body = re.sub(r"<[^>]+>", " ", text).strip()

        jobs.append({
            "company": company,
            "role": role,
            "url": f"https://news.ycombinator.com/item?id={kid_id}",
            "jd_text": plain_body,
        })

    return jobs


def _find_latest_thread() -> str | None:
    try:
        resp = requests.get(
            _ALGOLIA_URL,
            params={
                "query": "Ask HN: Who is Hiring?",
                "tags": "story,ask_hn",
                "hitsPerPage": 3,
            },
            timeout=10,
        )
        resp.raise_for_status()
        hits = resp.json().get("hits", [])
        if hits:
            return hits[0]["objectID"]
    except requests.RequestException:
        pass
    return None


def _get_item(item_id: str | int) -> dict:
    try:
        resp = requests.get(
            _HN_ITEM_URL.format(id=item_id),
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json() or {}
    except requests.RequestException:
        return {}
