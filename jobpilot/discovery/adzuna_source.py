"""
Adzuna source — multi-country search via Adzuna REST API.
Loops over all target_countries defined in profile.yaml.
Requires: ADZUNA_APP_ID + ADZUNA_API_KEY in .env
API docs: https://developer.adzuna.com/
"""

import requests


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    if not config.adzuna_app_id or not config.adzuna_api_key:
        raise RuntimeError("ADZUNA_APP_ID and ADZUNA_API_KEY must be set in .env")

    jobs = []

    for country in config.target_countries:
        code = country["code"]
        country_location = country.get("location", location)

        params = {
            "app_id": config.adzuna_app_id,
            "app_key": config.adzuna_api_key,
            "what": keywords,
            "where": country_location,
            "max_days_old": days,
            "results_per_page": 50,
            "content-type": "application/json",
        }

        try:
            resp = requests.get(
                f"https://api.adzuna.com/v1/api/jobs/{code}/search/1",
                params=params,
                timeout=15,
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            # Skip this country but continue with others
            continue

        for item in resp.json().get("results", []):
            company = (item.get("company") or {}).get("display_name", "").strip()
            role = (item.get("title") or "").strip()
            if not company or not role:
                continue
            jobs.append({
                "company": company,
                "role": role,
                "url": item.get("redirect_url", ""),
                "jd_text": item.get("description", ""),
            })

    return jobs
