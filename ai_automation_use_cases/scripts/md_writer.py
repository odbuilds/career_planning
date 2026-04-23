"""
Renders a complete Markdown document from the combined research + implementation data.
"""
from pathlib import Path
from use_case_seeds import DEPT_LABELS


def _stars(n: int) -> str:
    return "★" * n + "☆" * (5 - n)


def render_md(use_case: dict, research: dict, impl: dict, eval_result: dict) -> str:
    dept_label = DEPT_LABELS.get(use_case["dept"], use_case["dept"].replace("_", " ").title())
    invest = research.get("investment_estimate", {})
    stages = research.get("workflow_stages", [])
    tools = research.get("tools_and_tech", [])
    steps = research.get("implementation_steps", [])
    challenges = research.get("challenges", [])
    kpis = research.get("metrics_and_kpis", [])
    github = impl.get("github_resources", [])
    tutorials = impl.get("tutorial_resources", [])
    score = eval_result.get("total", 0)

    lines = []

    # ── Header ─────────────────────────────────────────────────────────────
    lines += [
        f"# {use_case['name']}",
        "",
        f"**Department:** {dept_label}  ",
        f"**Use Case ID:** `{use_case['id']}`  ",
        f"**Completeness Score:** {score}/16  ",
        f"**Setup Cost:** {invest.get('setup_cost', 'TBD')}  ",
        f"**Monthly Cost:** {invest.get('monthly_cost', 'TBD')}  ",
        f"**Break-even:** {invest.get('break_even', 'TBD')}  ",
        f"**FTE Savings:** {invest.get('fte_savings', 'TBD')}  ",
        "",
        "---",
        "",
    ]

    # ── Business Problem ────────────────────────────────────────────────────
    lines += [
        "## Business Problem",
        "",
        research.get("business_problem", "_Not available._"),
        "",
    ]

    # ── Automation Overview ─────────────────────────────────────────────────
    lines += [
        "## Automation Overview",
        "",
        research.get("automation_overview", "_Not available._"),
        "",
    ]

    # ── Workflow Stages ─────────────────────────────────────────────────────
    lines += ["## Workflow Stages", ""]
    for s in stages:
        lines += [
            f"### Stage {s.get('stage', '?')}: {s.get('name', '')}",
            "",
            f"| | |",
            f"|---|---|",
            f"| **Input** | {s.get('input', '')} |",
            f"| **Process** | {s.get('process', '')} |",
            f"| **Output** | {s.get('output', '')} |",
            "",
        ]
    if not stages:
        lines.append("_No stages documented._\n")

    # ── Tools & Technologies ────────────────────────────────────────────────
    lines += [
        "## Tools & Technologies",
        "",
        "| Tool / Vendor | Role | SMB Tier | Approx. Cost |",
        "|---|---|---|---|",
    ]
    for t in tools:
        lines.append(
            f"| **{t.get('name', '')}** | {t.get('role', '')} | {t.get('smb_tier', '')} | {t.get('approx_cost', '')} |"
        )
    lines.append("")

    # ── Implementation Steps ────────────────────────────────────────────────
    lines += ["## Implementation Steps", ""]
    for i, step in enumerate(steps, 1):
        lines.append(f"{i}. {step}")
    lines.append("")

    # ── Real-World Implementations ──────────────────────────────────────────
    lines += ["## Real-World Implementations", ""]

    if github:
        lines += ["### GitHub Repositories", ""]
        for r in github:
            url = r.get("url", "URL not confirmed")
            stars = r.get("stars", "?")
            lines += [
                f"#### [{r.get('title', 'Repository')}]({url})",
                f"**Stars:** {stars}",
                "",
                r.get("description", ""),
                "",
            ]
            patterns = r.get("key_patterns", [])
            if patterns:
                lines += ["**Key patterns demonstrated:**", ""]
                for p in patterns:
                    lines.append(f"- {p}")
                lines.append("")
    else:
        lines += [
            "### GitHub Repositories",
            "",
            "> No confirmed repositories found. "
            f"Search GitHub for: `{use_case['search_hint']}`",
            "",
        ]

    if tutorials:
        lines += ["### Articles & Tutorials", ""]
        for r in tutorials:
            url = r.get("url", "URL not confirmed")
            source = r.get("source", "Web")
            lines += [
                f"#### [{r.get('title', 'Article')}]({url})",
                f"**Source:** {source}",
                "",
                r.get("description", ""),
                "",
            ]
            topics = r.get("topics_covered", [])
            if topics:
                lines += ["**Topics covered:**", ""]
                for tp in topics:
                    lines.append(f"- {tp}")
                lines.append("")
    else:
        lines += [
            "### Articles & Tutorials",
            "",
            "> No confirmed articles found. "
            f"Search Medium/Substack for: `{use_case['search_hint']}`",
            "",
        ]

    step_summary = impl.get("step_by_step_summary", "")
    if step_summary:
        lines += ["### Step-by-Step Implementation Summary", "", step_summary, ""]

    code_hint = impl.get("code_snippet_hint", "")
    if code_hint:
        lines += ["### Code Patterns to Reference", "", f"> {code_hint}", ""]

    # ── Challenges & Mitigations ────────────────────────────────────────────
    lines += [
        "## Challenges & Mitigations",
        "",
        "| Challenge | Mitigation Strategy |",
        "|---|---|",
    ]
    for c in challenges:
        lines.append(f"| {c.get('challenge', '')} | {c.get('mitigation', '')} |")
    lines.append("")

    # ── Metrics & KPIs ──────────────────────────────────────────────────────
    lines += [
        "## Metrics & KPIs",
        "",
        "| KPI | Baseline | Target | How to Measure |",
        "|---|---|---|---|",
    ]
    for k in kpis:
        lines.append(
            f"| {k.get('kpi', '')} | {k.get('baseline', '')} | {k.get('target', '')} | {k.get('measurement', '')} |"
        )
    lines.append("")

    # ── Investment Estimate ─────────────────────────────────────────────────
    lines += [
        "## Investment Estimate",
        "",
        f"| Item | Estimate |",
        f"|---|---|",
        f"| Initial setup / implementation | {invest.get('setup_cost', 'TBD')} |",
        f"| Ongoing monthly cost | {invest.get('monthly_cost', 'TBD')} |",
        f"| Break-even timeline | {invest.get('break_even', 'TBD')} |",
        f"| FTE savings equivalent | {invest.get('fte_savings', 'TBD')} |",
        "",
    ]

    # ── Footer ──────────────────────────────────────────────────────────────
    lines += [
        "---",
        "",
        f"*Generated by the AI Automation Use Case Research System.*  ",
        f"*Use case ID: `{use_case['id']}` · Department: {dept_label}*",
    ]

    return "\n".join(lines)


def write_use_case(
    use_case: dict,
    research: dict,
    impl: dict,
    eval_result: dict,
    output_dir: Path,
) -> Path:
    dept_dir = output_dir / "use_cases" / use_case["dept"]
    dept_dir.mkdir(parents=True, exist_ok=True)
    file_path = dept_dir / f"{use_case['id']}.md"
    file_path.write_text(render_md(use_case, research, impl, eval_result), encoding="utf-8")
    return file_path
