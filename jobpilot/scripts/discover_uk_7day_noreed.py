"""
7-day UK+remote discovery, all sources except Reed.
Run from jobpilot/:
    python3 scripts/discover_uk_7day_noreed.py
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

enabled = cfg.get_enabled_sources()
location_aware = [s["slug"] for s in enabled if s.get("uses_location") and s["slug"] != "reed"]
location_free  = [s["slug"] for s in enabled if not s.get("uses_location")]

print(f"Locations ({len(cfg.search_locations)}): {[l['location'] for l in cfg.search_locations]}")
print(f"Location-aware (excl reed): {location_aware}")
print(f"Location-free: {location_free}")
print(f"{'=' * 70}")

totals = {"new": 0, "skipped": 0, "errors": []}

for kw in cfg.keyword_searches:
    if location_aware:
        for loc in cfg.search_locations:
            t0 = time.time()
            r = run_discovery(location_aware, kw, loc, 7, cfg)
            totals["new"] += r["new"]
            totals["skipped"] += r["skipped"]
            totals["errors"].extend(r["errors"])
            tag = "(remote)" if loc.get("remote") else ""
            print(f"[loc] kw={kw!r:28} loc={loc['location']!r:20}{tag:8} → new={r['new']} skip={r['skipped']} ({time.time()-t0:.1f}s)")
            for e in r["errors"]:
                print(f"  ERROR: {e}")

    if location_free:
        t0 = time.time()
        r = run_discovery(location_free, kw, "", 7, cfg)
        totals["new"] += r["new"]
        totals["skipped"] += r["skipped"]
        totals["errors"].extend(r["errors"])
        print(f"[global] kw={kw!r:28}                             → new={r['new']} skip={r['skipped']} ({time.time()-t0:.1f}s)")
        for e in r["errors"]:
            print(f"  ERROR: {e}")

print(f"\n{'=' * 70}")
print(f"TOTAL: new={totals['new']} skipped={totals['skipped']} errors={len(totals['errors'])}")
if totals["errors"]:
    for e in sorted(set(totals["errors"])):
        print(f"  {e}")
