"""
Renders a complete Markdown document from the combined research + implementation data.
"""
from pathlib import Path
from use_case_seeds import DEPT_LABELS


def render_md(use_case: dict, research: dict, impl: dict, eval_result: dict) -> str:
    dept_label = DEPT_LABELS.get(use_case["dept"], use_case["dept"].replace("_", " ").title())
    invest = research.get("investment_estimate", {})
    stages = research.get("workflow_stages", [])
    tools = research.get("tools_and_tech", [])
    steps = research.get("implementation_steps", [])
    challenges = research.get("challenges", [])
    kpis = research.get("metrics_and_kpis", [])
    company_examples = research.get("company_examples", [])
    sources = research.get("sources", [])
    github = impl.get("github_resources", [])
    tutorials = impl.get("tutorial_resources", [])
    score = eval_result.get("total", 0)

    lines = []

    # ── Header ─────────────────────────────────────────────────────────────
    invest_src = invest.get("source_url", "")
    invest_cite = f" [[source]]({invest_src})" if invest_src else ""
    lines += [
        f"# {use_case['name']}",
        "",
        f"**Department:** {dept_label}  ",
        f"**Use Case ID:** `{use_case['id']}`  ",
        f"**Completeness Score:** {score}/20  ",
        f"**Setup Cost:** {invest.get('setup_cost', 'TBD')}{invest_cite}  ",
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
        src = t.get("source_url", "")
        name = t.get("name", "")
        name_str = f"[**{name}**]({src})" if src else f"**{name}**"
        lines.append(
            f"| {name_str} | {t.get('role', '')} | {t.get('smb_tier', '')} | {t.get('approx_cost', '')} |"
        )
    lines.append("")

    # ── Implementation Steps ────────────────────────────────────────────────
    lines += ["## Implementation Steps", ""]
    for i, step in enumerate(steps, 1):
        lines.append(f"{i}. {step}")
    lines.append("")

    # ── Company Examples ────────────────────────────────────────────────────
    if company_examples:
        lines += ["## Company Examples", ""]
        for ex in company_examples:
            src = ex.get("source_url", "")
            co = ex.get("company", "")
            industry = ex.get("industry", "")
            header = f"**[{co}]({src})**" if src else f"**{co}**"
            lines += [
                f"### {co}",
                "",
                f"{header} _{industry}_  ",
                f"**What they did:** {ex.get('what_they_did', '')}  ",
                f"**Result:** {ex.get('result', '')}  ",
            ]
            if src:
                lines.append(f"**Source:** [{src}]({src})  ")
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
        "| KPI | Baseline | Target | How to Measure | Source |",
        "|---|---|---|---|---|",
    ]
    for k in kpis:
        src = k.get("source_url", "")
        src_str = f"[↗]({src})" if src else "—"
        lines.append(
            f"| {k.get('kpi', '')} | {k.get('baseline', '')} | {k.get('target', '')} | {k.get('measurement', '')} | {src_str} |"
        )
    lines.append("")

    # ── Investment Estimate ─────────────────────────────────────────────────
    invest_src = invest.get("source_url", "")
    invest_note = f"\n\n> Benchmarks sourced from: [{invest_src}]({invest_src})" if invest_src else ""
    lines += [
        "## Investment Estimate",
        "",
        f"| Item | Estimate |",
        f"|---|---|",
        f"| Initial setup / implementation | {invest.get('setup_cost', 'TBD')} |",
        f"| Ongoing monthly cost | {invest.get('monthly_cost', 'TBD')} |",
        f"| Break-even timeline | {invest.get('break_even', 'TBD')} |",
        f"| FTE savings equivalent | {invest.get('fte_savings', 'TBD')} |",
        invest_note,
        "",
    ]

    # ── Sources ─────────────────────────────────────────────────────────────
    all_sources = list(sources)
    # Pull any additional URLs from impl tutorials
    for r in tutorials:
        url = r.get("url", "")
        title = r.get("title", url)
        if url and url != "URL not confirmed":
            all_sources.append({"title": title, "url": url})

    if all_sources:
        lines += ["## Sources", ""]
        seen = set()
        for s in all_sources:
            url = s.get("url", "")
            title = s.get("title", url)
            if url and url not in seen:
                lines.append(f"- [{title}]({url})")
                seen.add(url)
        lines.append("")

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
