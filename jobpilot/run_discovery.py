"""CLI discovery runner — mirrors the Streamlit UI logic."""
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.config import load_config
from core import database as db
from discovery.runner import run_discovery

parser = argparse.ArgumentParser()
parser.add_argument("--days", type=int, default=None)
args = parser.parse_args()

db.init_db()
config = load_config()

enabled = config.get_enabled_sources()
all_slugs = [s["slug"] for s in enabled]
location_aware = [s["slug"] for s in enabled if s.get("uses_location")]
location_free = [s["slug"] for s in enabled if not s.get("uses_location")]
keywords = config.keyword_searches
locations = config.search_locations
days = args.days if args.days is not None else config.default_days_old

total = {"new": 0, "skipped": 0, "errors": []}

total_steps = len(keywords) * ((len(locations) if location_aware else 0) + (1 if location_free else 0))
step = 0

print(f"Discovery: {len(keywords)} keywords × ({len(locations)} locations + 1 global) = {total_steps} steps")
print(f"Location-aware: {location_aware}")
print(f"Location-free:  {location_free}\n")

for kw in keywords:
    if location_aware:
        for loc in locations:
            loc_str = loc.get("location", "") if isinstance(loc, dict) else loc
            step += 1
            print(f"[{step}/{total_steps}] {kw!r} @ {loc_str!r} ({', '.join(location_aware)})")
            sys.stdout.flush()
            try:
                r = run_discovery(location_aware, kw, loc, days, config)
                total["new"] += r["new"]
                total["skipped"] += r["skipped"]
                total["errors"].extend(r["errors"])
                print(f"  → new={r['new']} skipped={r['skipped']} errors={r['errors']}")
            except Exception as e:
                total["errors"].append(str(e))
                print(f"  → ERROR: {e}")
            sys.stdout.flush()

    if location_free:
        step += 1
        print(f"[{step}/{total_steps}] {kw!r} (global, {', '.join(location_free)})")
        sys.stdout.flush()
        try:
            r = run_discovery(location_free, kw, "", days, config)
            total["new"] += r["new"]
            total["skipped"] += r["skipped"]
            total["errors"].extend(r["errors"])
            print(f"  → new={r['new']} skipped={r['skipped']} errors={r['errors']}")
        except Exception as e:
            total["errors"].append(str(e))
            print(f"  → ERROR: {e}")
        sys.stdout.flush()

print(f"\n=== DONE === new={total['new']} skipped={total['skipped']} errors={len(total['errors'])}")
if total["errors"]:
    print("Errors:")
    for e in total["errors"]:
        print(f"  {e}")
