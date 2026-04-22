"""
We Work Remotely source — remote jobs via RSS feeds.
No API key required. RSS feeds are per category; no keyword search supported.
Keyword filtering is applied post-fetch on title + description text.
"""

import feedparser


# Category RSS feeds most relevant to Oliver's target roles
_FEEDS = [
    "https://weworkremotely.com/categories/remote-programming-jobs.rss",
    "https://weworkremotely.com/categories/remote-devops-sysadmin-jobs.rss",
    "https://weworkremotely.com/categories/remote-product-jobs.rss",
    "https://weworkremotely.com/categories/remote-sales-jobs.rss",
]


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    kw_lower = keywords.lower()
    seen_urls = set()
    jobs = []

    for feed_url in _FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            title = (entry.get("title") or "").strip()
            link = (entry.get("link") or "").strip()
            summary = (entry.get("summary") or "").strip()

            if not title or not link or link in seen_urls:
                continue

            # WWR titles are formatted as "Company: Role Title"
            if ": " in title:
                company, role = title.split(": ", 1)
            else:
                company, role = "", title

            company = company.strip()
            role = role.strip()

            # Keyword filter on role + description
            if kw_lower and kw_lower not in role.lower() and kw_lower not in summary.lower():
                continue

            seen_urls.add(link)
            jobs.append({"company": company, "role": role, "url": link, "jd_text": summary})

    return jobs
