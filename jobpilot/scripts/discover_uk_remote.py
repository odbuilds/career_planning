"""
Discovery run: UK + remote locations only, all keywords, last 7 days.
Mirrors the UI discovery flow exactly.
Run from jobpilot/:
    python3 scripts/discover_uk_remote.py
"""
import sys
import time
sys.path.insert(0, ".")

from core.config import load_config
from core import database as db
from discovery.runner import run_discovery

db.init_db()
cfg = load_config()

# UK + remote locations only
UK_REMOTE_LOCS = [
    loc for loc in (cfg.search_locations or [])
    if "UK" in loc.get("location", "") or loc.get("remote")
]

enabled = cfg.get_enabled_sources()
location_aware = [s["slug"] for s in enabled if s.get("uses_location")]
location_free  = [s["slug"] for s in enabled if not s.get("uses_location")]
keywords = cfg.keyword_searches

print(f"Locations ({len(UK_REMOTE_LOCS)}): {[l['location'] for l in UK_REMOTE_LOCS]}")
print(f"Keywords  ({len(keywords)}): {keywords}")
print(f"Location-aware sources  ({len(location_aware)}): {location_aware}")
print(f"Location-free sources   ({len(location_free)}): {location_free}")
print(f"Days: 7\n{'=' * 70}")

totals = {"new": 0, "skipped": 0, "errors": []}
run_count = 0
start = time.time()

for kw in keywords:
    # Location-aware sources: one call per UK/remote location
    if location_aware:
        for loc in UK_REMOTE_LOCS:
            t0 = time.time()
            r = run_discovery(location_aware, kw, loc, 7, cfg)
            totals["new"] += r["new"]
            totals["skipped"] += r["skipped"]
            totals["errors"].extend(r["errors"])
            run_count += 1
            loc_str = loc.get("location", "")
            tag = "(remote)" if loc.get("remote") else ""
            print(f"[loc-aware] kw={kw!r:30} loc={loc_str!r:20}{tag:8} → new={r['new']} skip={r['skipped']} ({time.time()-t0:.1f}s)")
            for e in r["errors"]:
                print(f"  ERROR: {e}")

    # Location-free sources: one call per keyword
    if location_free:
        t0 = time.time()
        r = run_discovery(location_free, kw, "", 7, cfg)
        totals["new"] += r["new"]
        totals["skipped"] += r["skipped"]
        totals["errors"].extend(r["errors"])
        run_count += 1
        print(f"[global]    kw={kw!r:30}                             → new={r['new']} skip={r['skipped']} ({time.time()-t0:.1f}s)")
        for e in r["errors"]:
            print(f"  ERROR: {e}")

elapsed = time.time() - start
print(f"\n{'=' * 70}")
print(f"DONE in {elapsed:.0f}s — {run_count} runs — new={totals['new']} skipped={totals['skipped']} errors={len(totals['errors'])}")
if totals["errors"]:
    print("\nAll errors:")
    for e in sorted(set(totals["errors"])):
        print(f"  {e}")
