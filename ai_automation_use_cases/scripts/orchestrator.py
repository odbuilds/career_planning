#!/usr/bin/env python3
"""
AI Automation Use Cases Research Orchestrator
============================================
Coordinates three Claude-powered agents to produce 100 detailed Markdown
documents on AI automation opportunities for 50-100 person businesses.

Usage:
  # Research all 100 use cases (long-running, ~4-8 hours)
  python orchestrator.py

  # Research a single department slice for testing
  python orchestrator.py --dept finance

  # Research a specific use case by ID
  python orchestrator.py --id fin_001

  # Limit to N use cases (for quick testing)
  python orchestrator.py --limit 3

  # Resume from saved progress
  python orchestrator.py --resume
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Load .env if present (before importing anthropic)
_env_file = Path(__file__).parent / ".env"
if _env_file.exists():
    for _line in _env_file.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _, _v = _line.partition("=")
            os.environ.setdefault(_k.strip(), _v.strip())

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.table import Table

# ── Path setup ────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR.parent
PROGRESS_FILE = SCRIPT_DIR / "progress.json"

sys.path.insert(0, str(SCRIPT_DIR))

from use_case_seeds import USE_CASES
from agents import run_evaluation_agent, run_implementation_agent, run_research_agent
from md_writer import write_use_case

console = Console()

# ── Progress persistence ───────────────────────────────────────────────────────

def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        try:
            return json.loads(PROGRESS_FILE.read_text())
        except Exception:
            pass
    return {"completed": [], "failed": []}


def save_progress(state: dict) -> None:
    PROGRESS_FILE.write_text(json.dumps(state, indent=2))


# ── Single use-case pipeline ──────────────────────────────────────────────────

def process_use_case(use_case: dict, max_retries: int = 2) -> dict:
    """
    Run the full three-agent pipeline for one use case.
    Returns a result dict with status, file_path, scores, etc.
    """
    uid = use_case["id"]
    name = use_case["name"]

    for attempt in range(1, max_retries + 2):  # 1-indexed, up to max_retries+1 total
        try:
            console.print(f"  [cyan]→ Research agent[/cyan]  (attempt {attempt})")
            research = run_research_agent(use_case)
            if not research:
                raise ValueError("Research agent returned empty result")

            console.print(f"  [cyan]→ Implementation agent[/cyan]")
            impl = run_implementation_agent(use_case, research)

            console.print(f"  [cyan]→ Evaluation agent[/cyan]")
            eval_result = run_evaluation_agent(use_case, research, impl)

            passed = eval_result.get("passed", False)
            score = eval_result.get("total", 0)

            if not passed and attempt <= max_retries:
                feedback = eval_result.get("feedback", "")
                console.print(
                    f"  [yellow]⚠ Score {score}/16 — retrying with feedback:[/yellow] {feedback}"
                )
                # Enrich the search hint with eval feedback for the retry
                use_case = {
                    **use_case,
                    "search_hint": f"{use_case['search_hint']} {feedback}",
                }
                time.sleep(2)  # brief pause before retry
                continue

            # Write the file regardless of pass/fail on last attempt
            file_path = write_use_case(use_case, research, impl, eval_result, OUTPUT_DIR)

            return {
                "id": uid,
                "name": name,
                "status": "completed",
                "score": score,
                "passed": passed,
                "file": str(file_path.relative_to(OUTPUT_DIR)),
                "attempts": attempt,
            }

        except Exception as exc:
            if attempt <= max_retries:
                console.print(f"  [red]✗ Error (attempt {attempt}): {exc}[/red] — retrying…")
                time.sleep(5 * attempt)
            else:
                console.print(f"  [red]✗ Failed after {attempt} attempts: {exc}[/red]")
                return {
                    "id": uid,
                    "name": name,
                    "status": "failed",
                    "error": str(exc),
                    "attempts": attempt,
                }

    # Should not reach here
    return {"id": uid, "name": name, "status": "failed", "error": "max retries exceeded"}


# ── Index builder ─────────────────────────────────────────────────────────────

def build_index(results: list[dict]) -> None:
    """Write use_cases/index.md and the top-level README.md."""
    from use_case_seeds import DEPT_LABELS

    # Group by dept
    by_dept: dict[str, list[dict]] = {}
    for r in results:
        if r.get("status") != "completed":
            continue
        seed = next((u for u in USE_CASES if u["id"] == r["id"]), None)
        if not seed:
            continue
        by_dept.setdefault(seed["dept"], []).append({**r, "seed": seed})

    lines = [
        "# AI Automation Use Cases — Index",
        "",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d')} | Total: {len(results)} use cases*",
        "",
        "## Summary",
        "",
        "| Department | Count | Avg Score |",
        "|---|---|---|",
    ]
    for dept, items in sorted(by_dept.items()):
        avg = sum(i.get("score", 0) for i in items) / len(items) if items else 0
        label = DEPT_LABELS.get(dept, dept)
        lines.append(f"| {label} | {len(items)} | {avg:.1f}/16 |")
    lines.append("")

    for dept, items in sorted(by_dept.items()):
        label = DEPT_LABELS.get(dept, dept)
        lines += [f"## {label}", ""]
        for item in sorted(items, key=lambda x: x["id"]):
            name = item["seed"]["name"]
            uid = item["id"]
            score = item.get("score", 0)
            file_rel = item.get("file", "")
            lines.append(f"- [{name}](../{file_rel}) `{uid}` — {score}/16")
        lines.append("")

    index_path = OUTPUT_DIR / "use_cases" / "index.md"
    index_path.write_text("\n".join(lines), encoding="utf-8")

    # Top-level README
    readme_lines = [
        "# AI Automation Use Cases Library",
        "",
        "A library of **100 AI automation opportunities** for companies with 50-100 employees.",
        "Each document covers the business problem, workflow stages, tool options,",
        "implementation steps, challenges, KPIs, and links to real GitHub repos and tutorials.",
        "",
        "## Departments Covered",
        "",
    ]
    from use_case_seeds import DEPT_LABELS
    dept_counts = {}
    for r in results:
        if r.get("status") == "completed":
            seed = next((u for u in USE_CASES if u["id"] == r["id"]), None)
            if seed:
                dept_counts[seed["dept"]] = dept_counts.get(seed["dept"], 0) + 1
    for dept, count in sorted(dept_counts.items()):
        label = DEPT_LABELS.get(dept, dept)
        readme_lines.append(f"- **{label}** — {count} use cases")
    readme_lines += [
        "",
        "## Usage",
        "",
        "Browse the [full index](use_cases/index.md) or navigate directly into a department folder.",
        "",
        "Each Markdown file includes:",
        "- Business problem statement",
        "- Automation overview",
        "- Step-by-step workflow stages",
        "- Tool & vendor recommendations (SMB pricing)",
        "- Implementation steps",
        "- Real GitHub repos & tutorial links",
        "- Challenges & mitigations",
        "- KPIs with baseline vs. target",
        "- Investment estimate & break-even timeline",
        "",
        "## Regenerating",
        "",
        "```bash",
        "cd scripts",
        "pip install -r requirements.txt",
        "python orchestrator.py --resume   # pick up where it left off",
        "```",
    ]
    readme_path = OUTPUT_DIR / "README.md"
    readme_path.write_text("\n".join(readme_lines), encoding="utf-8")
    console.print(f"\n[green]✓ Index written to {index_path}[/green]")
    console.print(f"[green]✓ README written to {readme_path}[/green]")


# ── CLI entry point ───────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="AI Automation Use Cases Orchestrator")
    parser.add_argument("--dept",   help="Only process one department (e.g. finance, hr)")
    parser.add_argument("--id",     help="Only process one use case by ID (e.g. fin_001)")
    parser.add_argument("--limit",  type=int, help="Stop after N use cases (for testing)")
    parser.add_argument("--resume", action="store_true", help="Skip already-completed IDs")
    parser.add_argument("--index-only", action="store_true", help="Only rebuild the index")
    args = parser.parse_args()

    state = load_progress()
    completed_ids = set(state.get("completed", []))

    # ── Filter seed list ──────────────────────────────────────────────────────
    seeds = USE_CASES
    if args.id:
        seeds = [u for u in seeds if u["id"] == args.id]
    elif args.dept:
        seeds = [u for u in seeds if u["dept"] == args.dept]
    if args.resume:
        seeds = [u for u in seeds if u["id"] not in completed_ids]
    if args.limit:
        seeds = seeds[: args.limit]

    if args.index_only:
        existing = [{"id": uid, "status": "completed", "score": 12} for uid in completed_ids]
        build_index(existing)
        return

    if not seeds:
        console.print("[yellow]No use cases to process.[/yellow]")
        return

    console.print(
        Panel(
            f"[bold]AI Automation Research System[/bold]\n"
            f"Processing [cyan]{len(seeds)}[/cyan] use cases → [green]{OUTPUT_DIR}[/green]",
            border_style="blue",
        )
    )

    all_results = []
    summary_table = Table(title="Results", show_lines=True)
    summary_table.add_column("ID", style="cyan", no_wrap=True)
    summary_table.add_column("Name")
    summary_table.add_column("Score", justify="center")
    summary_table.add_column("Status")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
        transient=False,
    ) as progress:
        task = progress.add_task("Researching use cases…", total=len(seeds))

        for use_case in seeds:
            progress.update(task, description=f"[bold]{use_case['name'][:55]}[/bold]")
            console.print(f"\n[bold blue]▶ {use_case['id']}:[/bold blue] {use_case['name']}")

            result = process_use_case(use_case)
            all_results.append(result)

            if result["status"] == "completed":
                state["completed"] = list(set(state.get("completed", [])) | {use_case["id"]})
                score_str = f"{result.get('score', 0)}/16"
                passed_icon = "✓" if result.get("passed") else "~"
                status_style = "green" if result.get("passed") else "yellow"
                summary_table.add_row(
                    use_case["id"],
                    use_case["name"][:60],
                    score_str,
                    f"[{status_style}]{passed_icon} {result['status']}[/{status_style}]",
                )
                console.print(f"  [green]✓ Written: {result.get('file', '')} (score {score_str})[/green]")
            else:
                state.setdefault("failed", []).append(use_case["id"])
                summary_table.add_row(
                    use_case["id"],
                    use_case["name"][:60],
                    "—",
                    f"[red]✗ {result.get('error', 'failed')[:40]}[/red]",
                )

            save_progress(state)
            progress.advance(task)

            # Polite rate-limit pause between use cases
            time.sleep(1)

    # ── Summary ───────────────────────────────────────────────────────────────
    console.print("\n")
    console.print(summary_table)

    completed = [r for r in all_results if r["status"] == "completed"]
    failed = [r for r in all_results if r["status"] != "completed"]
    avg_score = sum(r.get("score", 0) for r in completed) / len(completed) if completed else 0

    console.print(
        Panel(
            f"[green]Completed:[/green] {len(completed)}  "
            f"[red]Failed:[/red] {len(failed)}  "
            f"[cyan]Avg score:[/cyan] {avg_score:.1f}/16",
            title="Run Summary",
            border_style="green",
        )
    )

    # Rebuild the index from all completed use cases in state
    all_completed = [
        {"id": uid, "status": "completed", "score": 12}
        for uid in state.get("completed", [])
    ]
    # Overwrite with richer result data from this run
    id_to_result = {r["id"]: r for r in all_results if r["status"] == "completed"}
    merged = []
    for item in all_completed:
        merged.append(id_to_result.get(item["id"], item))

    build_index(merged)


if __name__ == "__main__":
    main()
