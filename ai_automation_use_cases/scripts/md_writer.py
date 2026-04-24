"""
Renders a complete Markdown document from the combined research + implementation data.
Document order: Problem → Challenges → ROI/KPIs → Solution → Workflow → Tools →
                Implementation → Examples → Resources → Sources
"""
from pathlib import Path
from use_case_seeds import DEPT_LABELS

_SOURCE_BADGE = {"vendor": " *(vendor-sourced)*", "practitioner": "", "independent": ""}


def _cite(url: str, label: str = "source") -> str:
    return f" [[{label}]]({url})" if url else ""


def render_md(use_case: dict, research: dict, impl: dict, eval_result: dict) -> str:
    dept_label = DEPT_LABELS.get(use_case["dept"], use_case["dept"].replace("_", " ").title())
    invest = research.get("investment_estimate", {})
    prob = research.get("problem_breakdown", {})
    challenges = research.get("challenges", [])
    roi = research.get("roi_and_kpis", {})
    kpis = roi.get("kpis", []) or research.get("metrics_and_kpis", [])
    stages = research.get("workflow_stages", [])
    tools = research.get("tools_and_tech", [])
    steps = research.get("implementation_steps", [])
    company_examples = research.get("company_examples", [])
    sources = research.get("sources", [])
    github = impl.get("github_resources", [])
    tutorials = impl.get("tutorial_resources", [])
    score = eval_result.get("total", 0)

    lines = []

    # ── Header ──────────────────────────────────────────────────────────────
    invest_src = invest.get("source_url", "")
    lines += [
        f"# {use_case['name']}",
        "",
        f"**Department:** {dept_label}  ",
        f"**Use Case ID:** `{use_case['id']}`  ",
        f"**Completeness Score:** {score}/20  ",
        f"**Setup Cost:** {invest.get('setup_cost', 'TBD')}{_cite(invest_src)}  ",
        f"**Monthly Cost:** {invest.get('monthly_cost', 'TBD')}  ",
        f"**Break-even:** {invest.get('break_even', 'TBD')}  ",
        f"**FTE Savings:** {invest.get('fte_savings', 'TBD')}  ",
        "",
        "---",
        "",
    ]

    # ── 1. The Problem ───────────────────────────────────────────────────────
    lines += ["## The Problem", ""]
    if prob:
        lines += [prob.get("summary", ""), ""]
        manual_tasks = prob.get("manual_tasks", [])
        if manual_tasks:
            lines += ["### Manual Tasks Being Replaced", ""]
            lines += ["| Task | Who | Time/Week | Pain Point |", "|---|---|---|---|"]
            for t in manual_tasks:
                lines.append(
                    f"| {t.get('task','')} | {t.get('who','')} | "
                    f"{t.get('time_per_week','')} | {t.get('pain_point','')} |"
                )
            lines.append("")
        bc = prob.get("benchmark_cost", "")
        bc_url = prob.get("benchmark_source_url", "")
        bc_src = prob.get("benchmark_source", "")
        if bc:
            lines += [
                f"> **Industry benchmark:** {bc}  ",
                f"> *Source: [{bc_src}]({bc_url})*" if bc_url else f"> *Source: {bc_src}*",
                "",
            ]
    else:
        lines += [research.get("business_problem", "_Not available._"), ""]

    # ── 2. Why It's Hard (Challenges) ───────────────────────────────────────
    lines += ["## Why This Is Hard to Automate", ""]
    if challenges:
        for c in challenges:
            lines += [
                f"### {c.get('challenge', '')}",
                "",
                f"**Why it matters:** {c.get('why_it_matters', '')}  ",
                f"**Mitigation:** {c.get('mitigation', '')}",
                "",
            ]
    else:
        lines.append("_No challenges documented._\n")

    # ── 3. ROI & KPIs ────────────────────────────────────────────────────────
    lines += ["## ROI & KPIs", ""]
    roi_formula = roi.get("roi_formula", "")
    payback = roi.get("payback_period", invest.get("break_even", ""))
    if roi_formula:
        lines += [
            "### ROI Calculation",
            "",
            f"```\n{roi_formula}\n```",
            "",
        ]
    if payback:
        lines += [f"**Typical payback period:** {payback}", ""]

    if kpis:
        lines += [
            "### Key Performance Indicators",
            "",
            "| KPI | Before | After | How to Measure | Source |",
            "|---|---|---|---|---|",
        ]
        for k in kpis:
            src = k.get("source_url", "")
            src_type = k.get("source_type", "")
            badge = _SOURCE_BADGE.get(src_type, "")
            src_str = f"[↗]({src}){badge}" if src else f"—{badge}"
            lines.append(
                f"| {k.get('kpi','')} | {k.get('baseline','')} | "
                f"{k.get('target','')} | {k.get('measurement','')} | {src_str} |"
            )
        lines.append("")

    # ── 4. Automation Overview ───────────────────────────────────────────────
    lines += [
        "## Automation Overview",
        "",
        research.get("automation_overview", "_Not available._"),
        "",
    ]

    # ── 5. Workflow Stages ───────────────────────────────────────────────────
    lines += ["## Workflow Stages", ""]
    for s in stages:
        lines += [
            f"### Stage {s.get('stage','?')}: {s.get('name','')}",
            "",
            "| | |",
            "|---|---|",
            f"| **Input** | {s.get('input','')} |",
            f"| **Process** | {s.get('process','')} |",
            f"| **Output** | {s.get('output','')} |",
            "",
        ]
    if not stages:
        lines.append("_No stages documented._\n")

    # ── 6. Tools & Technologies ──────────────────────────────────────────────
    lines += [
        "## Tools & Technologies",
        "",
        "| Tool / Vendor | Role | Path | SMB Tier | Approx. Cost |",
        "|---|---|---|---|---|",
    ]
    for t in tools:
        src = t.get("source_url", "")
        name = t.get("name", "")
        name_str = f"[**{name}**]({src})" if src else f"**{name}**"
        path = t.get("path", "—")
        lines.append(
            f"| {name_str} | {t.get('role','')} | {path} | "
            f"{t.get('smb_tier','')} | {t.get('approx_cost','')} |"
        )
    lines.append("")

    # ── 7. Implementation Steps ──────────────────────────────────────────────
    lines += ["## Implementation Steps", ""]
    for i, step in enumerate(steps, 1):
        lines.append(f"{i}. {step}")
    lines.append("")

    # ── 8. Company Examples ──────────────────────────────────────────────────
    if company_examples:
        lines += ["## Company Examples", ""]
        for ex in company_examples:
            src = ex.get("source_url", "")
            co = ex.get("company", "")
            industry = ex.get("industry", "")
            src_type = ex.get("source_type", "")
            badge = _SOURCE_BADGE.get(src_type, "")
            header = f"[{co}]({src})" if src else co
            lines += [
                f"### {co}{badge}",
                "",
                f"**Industry:** {industry}  ",
                f"**What they did:** {ex.get('what_they_did','')}  ",
                f"**Result:** {ex.get('result','')}  ",
            ]
            if src:
                lines.append(f"**Source:** [{src}]({src}){badge}  ")
            lines.append("")

    # ── 9. Real-World Implementations ───────────────────────────────────────
    lines += ["## Real-World Implementations", ""]

    if github:
        lines += ["### GitHub Repositories", ""]
        for r in github:
            url = r.get("url", "URL not confirmed")
            stars = r.get("stars", "?")
            lines += [
                f"#### [{r.get('title','Repository')}]({url})",
                f"**Stars:** {stars}",
                "",
                r.get("description", ""),
                "",
            ]
            for p in r.get("key_patterns", []):
                lines.append(f"- {p}")
            if r.get("key_patterns"):
                lines.append("")
    else:
        lines += [
            "### GitHub Repositories",
            "",
            f"> Search GitHub for: `{use_case['search_hint']}`",
            "",
        ]

    if tutorials:
        lines += ["### Articles & Tutorials", ""]
        for r in tutorials:
            url = r.get("url", "URL not confirmed")
            lines += [
                f"#### [{r.get('title','Article')}]({url})",
                f"**Source:** {r.get('source','Web')}",
                "",
                r.get("description", ""),
                "",
            ]
            for tp in r.get("topics_covered", []):
                lines.append(f"- {tp}")
            if r.get("topics_covered"):
                lines.append("")
    else:
        lines += [
            "### Articles & Tutorials",
            "",
            f"> Search Medium/Substack for: `{use_case['search_hint']}`",
            "",
        ]

    if impl.get("step_by_step_summary"):
        lines += ["### Step-by-Step Implementation Summary", "", impl["step_by_step_summary"], ""]
    if impl.get("code_snippet_hint"):
        lines += ["### Code Patterns to Reference", "", f"> {impl['code_snippet_hint']}", ""]

    # ── 10. Sources ──────────────────────────────────────────────────────────
    all_sources = list(sources)
    for r in tutorials:
        url = r.get("url", "")
        if url and url != "URL not confirmed":
            all_sources.append({"title": r.get("title", url), "url": url, "source_type": "practitioner"})

    if all_sources:
        lines += ["## Sources", ""]
        seen: set = set()
        for s in all_sources:
            url = s.get("url", "")
            title = s.get("title", url)
            stype = s.get("source_type", "")
            badge = _SOURCE_BADGE.get(stype, "")
            if url and url not in seen:
                lines.append(f"- [{title}]({url}){badge}")
                seen.add(url)
        lines.append("")

    # ── Footer ───────────────────────────────────────────────────────────────
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
