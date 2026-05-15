"""
Rescore jobs that failed pipeline scoring with a 401 auth error.
Run from jobpilot/:
    python3 scripts/rescore_401_errors.py
"""
import sys
import sqlite3
sys.path.insert(0, ".")

from core.config import load_config
from core.pipeline_scorer import pipeline_score_batch

conn = sqlite3.connect("jobpilot.db")
rows = conn.execute(
    "SELECT id, jd_text FROM jobs "
    "WHERE (pipeline_reason LIKE '%User not found%' OR pipeline_reason LIKE '%401%') "
    "AND jd_text IS NOT NULL AND trim(jd_text) != ''"
).fetchall()

print(f"Rescoring {len(rows)} jobs...")
cfg = load_config()

jobs = [{"id": r[0], "jd_text": r[1]} for r in rows]
results = pipeline_score_batch(jobs, cfg)

updated = 0
for job_id, tier, reason in results:
    if tier is not None:
        conn.execute(
            "UPDATE jobs SET pipeline_tier=?, pipeline_reason=? WHERE id=?",
            (tier, reason, job_id),
        )
        updated += 1

conn.commit()
conn.close()

tiers = {}
for _, tier, _ in results:
    tiers[tier] = tiers.get(tier, 0) + 1

print(f"Done — {updated} updated")
print("Tier breakdown:", tiers)
