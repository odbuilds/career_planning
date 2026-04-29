"""
Backfill pipeline_tier for all jobs that have JD text but no tier.
Runs the three-stage cascade scorer in async batches.
"""

import sys
import time
sys.path.insert(0, str(__file__).rsplit("/scripts", 1)[0])

from core.config import load_config
from core.database import get_conn, init_db
from core.pipeline_scorer import pipeline_score_batch

BATCH_SIZE = 50
CONCURRENCY = 10


def main():
    init_db()
    cfg = load_config()

    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, jd_text FROM jobs WHERE pipeline_tier IS NULL AND jd_text IS NOT NULL AND jd_text != '' AND status = 'discovered'"
        ).fetchall()

    jobs = [{"id": r["id"], "jd_text": r["jd_text"]} for r in rows]
    total = len(jobs)
    print(f"Scoring {total} jobs...")

    scored = 0
    for i in range(0, total, BATCH_SIZE):
        batch = jobs[i : i + BATCH_SIZE]
        results = pipeline_score_batch(batch, cfg, concurrency=CONCURRENCY)

        with get_conn() as conn:
            for job_id, tier, reason in results:
                if tier is not None:
                    conn.execute(
                        "UPDATE jobs SET pipeline_tier = ?, pipeline_reason = ? WHERE id = ?",
                        (tier, reason, job_id),
                    )

        scored += len(batch)
        print(f"  {scored}/{total} done (last batch: {i}–{i+len(batch)-1})")

    print("Done.")


if __name__ == "__main__":
    main()
