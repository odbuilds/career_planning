"""
Reed.co.uk source — UK jobs via Reed REST API.
Requires: REED_API_KEY in .env (free at reed.co.uk/developers)
API docs: https://www.reed.co.uk/developers/jobseeker
"""

import base64
import requests


def fetch(keywords: str, location: str, days: int, config, source_cfg: dict = None) -> list[dict]:
    if not config.reed_api_key:
        raise RuntimeError("REED_API_KEY must be set in .env")

    # Reed uses HTTP Basic auth: API key as username, empty password
    token = base64.b64encode(f"{config.reed_api_key}:".encode()).decode()
    headers = {"Authorization": f"Basic {token}"}

    params = {
        "keywords": keywords,
        "locationName": location or "London",
        "distancefrom": 30,
        "maximumDaysAgo": days,
        "resultsToTake": 100,
        "fullTime": "true",
    }

    try:
        resp = requests.get(
            "https://www.reed.co.uk/api/1.0/search",
            headers=headers,
            params=params,
            timeout=15,
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Reed API request failed: {e}") from e

    jobs = []
    for item in resp.json().get("results", []):
        company = (item.get("employerName") or "").strip()
        role = (item.get("jobTitle") or "").strip()
        if not company or not role:
            continue
        job_id = item.get("jobId", "")
        url = item.get("jobUrl") or (f"https://www.reed.co.uk/jobs/{job_id}" if job_id else "")
        jobs.append({
            "company": company,
            "role": role,
            "url": url,
            "jd_text": item.get("jobDescription", ""),
        })

    return jobs
