"""
LinkedIn-only discovery: UK + remote, 1-day post age.
Run from jobpilot/:
    python3 scripts/discover_linkedin_1day.py
"""
import sys
import time
sys.path.insert(0, ".")

from core.config import load_config
from core import database as db
from discovery.runner import run_discovery

db.init_db()
cfg = load_config()

cfg.search_locations = [
    loc for loc in (cfg.search_locations or [])
    if "UK" in loc.get("location", "") or loc.get("remote")
]

totals = {"new": 0, "skipped": 0, "errors": []}

for kw in cfg.keyword_searches:
    for loc in cfg.search_locations:
        t0 = time.time()
        r = run_discovery(["linkedin"], kw, loc, 1, cfg)
        totals["new"] += r["new"]
        totals["skipped"] += r["skipped"]
        totals["errors"].extend(r["errors"])
        tag = "(remote)" if loc.get("remote") else ""
        print(f"kw={kw!r:30} loc={loc['location']!r:20}{tag:8} → new={r['new']} skip={r['skipped']} ({time.time()-t0:.1f}s)")
        for e in r["errors"]:
            print(f"  ERROR: {e}")

print(f"\nTOTAL: new={totals['new']} skipped={totals['skipped']} errors={len(totals['errors'])}")
