#!/usr/bin/env python3
"""
Advanced strategist-facing strategic ideation diagnostics.

This dependency-light workflow uses only the Python standard library.

It produces:
- idea portfolio scores
- option architecture scores
- assumption risk register
- evidence strength register
- prototype learning plan
- implementation pathway scores
- a markdown strategic ideation diagnostic report

The workflow is designed for professional strategy teams that need to transform
ideas into structured strategic possibility, testable assumptions, prototype
plans, implementation pathways, and decision memory.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "outputs" / "tables"
REPORTS = ROOT / "outputs" / "reports"

for path in (PROCESSED, TABLES, REPORTS):
    path.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def f(row: dict[str, str], key: str) -> float:
    return float(row[key])


ideas = read_csv(RAW / "idea_portfolio.csv")
criteria = read_csv(RAW / "criteria_weights.csv")
options = read_csv(RAW / "option_architecture.csv")
assumptions = read_csv(RAW / "assumptions.csv")
evidence = read_csv(RAW / "evidence_register.csv")
prototypes = read_csv(RAW / "prototype_plan.csv")
pathways = read_csv(RAW / "implementation_pathways.csv")

weights = {row["criterion"]: float(row["weight"]) for row in criteria}

# ---------------------------------------------------------------------
# 1. Assumption-risk register
# ---------------------------------------------------------------------

assumption_rows: list[dict[str, object]] = []
assumption_risk_by_idea: dict[str, float] = {}

for idea_id in {row["idea_id"] for row in ideas}:
    linked = [row for row in assumptions if row["idea_id"] == idea_id]
    risks = []
    for item in linked:
        risk = (1.0 - f(item, "confidence")) * f(item, "criticality")
        risks.append(risk)
        if risk >= 0.42:
            urgency = "high"
        elif risk >= 0.28:
            urgency = "moderate"
        else:
            urgency = "monitor"

        assumption_rows.append(
            {
                "assumption_id": item["assumption_id"],
                "idea_id": item["idea_id"],
                "layer": item["layer"],
                "assumption": item["assumption"],
                "confidence": item["confidence"],
                "criticality": item["criticality"],
                "assumption_risk": round(risk, 4),
                "urgency": urgency,
                "test_method": item["test_method"],
                "evidence_status": item["evidence_status"],
            }
        )
    assumption_risk_by_idea[idea_id] = mean(risks) if risks else 0.0

assumption_rows.sort(key=lambda row: row["assumption_risk"], reverse=True)

write_csv(
    TABLES / "assumption_risk_register.csv",
    assumption_rows,
    [
        "assumption_id",
        "idea_id",
        "layer",
        "assumption",
        "confidence",
        "criticality",
        "assumption_risk",
        "urgency",
        "test_method",
        "evidence_status",
    ],
)

# ---------------------------------------------------------------------
# 2. Evidence strength register
# ---------------------------------------------------------------------

evidence_rows: list[dict[str, object]] = []
evidence_strength_by_idea: dict[str, float] = {}

for idea_id in {row["idea_id"] for row in ideas}:
    linked = [row for row in evidence if row["idea_id"] == idea_id]
    strengths = []
    for item in linked:
        strength = (
            0.34 * f(item, "evidence_quality")
            + 0.30 * f(item, "relevance")
            + 0.20 * f(item, "recency")
            - 0.16 * f(item, "contestation")
        )
        strengths.append(strength)

        if strength >= 0.72:
            interpretation = "strong_support"
        elif strength >= 0.58:
            interpretation = "usable_but_review"
        else:
            interpretation = "weak_or_contested"

        evidence_rows.append(
            {
                "evidence_id": item["evidence_id"],
                "idea_id": item["idea_id"],
                "evidence_type": item["evidence_type"],
                "evidence_strength": round(strength, 4),
                "interpretation": interpretation,
                "source_type": item["source_type"],
                "evidence_summary": item["evidence_summary"],
            }
        )
    evidence_strength_by_idea[idea_id] = mean(strengths) if strengths else 0.0

evidence_rows.sort(key=lambda row: row["evidence_strength"], reverse=True)

write_csv(
    TABLES / "evidence_strength_register.csv",
    evidence_rows,
    [
        "evidence_id",
        "idea_id",
        "evidence_type",
        "evidence_strength",
        "interpretation",
        "source_type",
        "evidence_summary",
    ],
)

# ---------------------------------------------------------------------
# 3. Idea portfolio scoring
# ---------------------------------------------------------------------

portfolio_rows: list[dict[str, object]] = []

for row in ideas:
    idea_id = row["idea_id"]
    assumption_risk = assumption_risk_by_idea.get(idea_id, 0.0)
    evidence_strength = evidence_strength_by_idea.get(idea_id, 0.0)

    base_score = (
        weights["strategic_fit"] * f(row, "strategic_fit")
        + weights["feasibility"] * f(row, "feasibility")
        + weights["systems_leverage"] * f(row, "systems_leverage")
        + weights["learning_value"] * f(row, "learning_value")
        + weights["ethical_legitimacy"] * f(row, "ethical_legitimacy")
        + weights["knowledge_reusability"] * f(row, "knowledge_reusability")
        - weights["uncertainty_penalty"] * f(row, "uncertainty")
        - weights["assumption_risk_penalty"] * assumption_risk
    )

    evidence_adjusted_score = base_score + 0.06 * evidence_strength

    if evidence_adjusted_score >= 0.82 and assumption_risk < 0.30:
        recommendation = "advance_to_strategy_review"
    elif evidence_adjusted_score >= 0.74:
        recommendation = "prototype_or_test_assumptions"
    elif assumption_risk >= 0.42:
        recommendation = "test_critical_assumptions_before_selection"
    else:
        recommendation = "hold_reframe_or_collect_evidence"

    portfolio_rows.append(
        {
            "idea_id": idea_id,
            "idea_name": row["idea_name"],
            "idea_type": row["idea_type"],
            "portfolio_score": round(evidence_adjusted_score, 4),
            "base_score": round(base_score, 4),
            "assumption_risk": round(assumption_risk, 4),
            "evidence_strength": round(evidence_strength, 4),
            "uncertainty": row["uncertainty"],
            "estimated_cost": row["estimated_cost"],
            "implementation_months": row["implementation_months"],
            "recommendation": recommendation,
            "problem_frame": row["problem_frame"],
        }
    )

portfolio_rows.sort(key=lambda row: row["portfolio_score"], reverse=True)

write_csv(
    TABLES / "idea_portfolio_scores.csv",
    portfolio_rows,
    [
        "idea_id",
        "idea_name",
        "idea_type",
        "portfolio_score",
        "base_score",
        "assumption_risk",
        "evidence_strength",
        "uncertainty",
        "estimated_cost",
        "implementation_months",
        "recommendation",
        "problem_frame",
    ],
)

write_csv(
    PROCESSED / "idea_portfolio_scores.csv",
    portfolio_rows,
    [
        "idea_id",
        "idea_name",
        "idea_type",
        "portfolio_score",
        "base_score",
        "assumption_risk",
        "evidence_strength",
        "uncertainty",
        "estimated_cost",
        "implementation_months",
        "recommendation",
        "problem_frame",
    ],
)

# ---------------------------------------------------------------------
# 4. Option architecture scoring
# ---------------------------------------------------------------------

option_rows: list[dict[str, object]] = []

for row in options:
    architecture_score = (
        0.16 * f(row, "reversibility")
        - 0.10 * f(row, "dependency_complexity")
        + 0.24 * f(row, "portfolio_fit")
        + 0.24 * f(row, "scenario_robustness")
        + 0.22 * f(row, "sequencing_value")
    )

    if row["commitment_level"] == "high" and f(row, "reversibility") < 0.50:
        architecture_flag = "high_commitment_low_reversibility"
    elif f(row, "dependency_complexity") > 0.60:
        architecture_flag = "dependency_complexity_review"
    elif architecture_score >= 0.75:
        architecture_flag = "strong_option_architecture"
    else:
        architecture_flag = "needs_architecture_refinement"

    option_rows.append(
        {
            "option_id": row["option_id"],
            "idea_id": row["idea_id"],
            "option_role": row["option_role"],
            "time_horizon": row["time_horizon"],
            "commitment_level": row["commitment_level"],
            "architecture_score": round(architecture_score, 4),
            "architecture_flag": architecture_flag,
            "reversibility": row["reversibility"],
            "dependency_complexity": row["dependency_complexity"],
            "portfolio_fit": row["portfolio_fit"],
            "scenario_robustness": row["scenario_robustness"],
            "sequencing_value": row["sequencing_value"],
        }
    )

option_rows.sort(key=lambda row: row["architecture_score"], reverse=True)

write_csv(
    TABLES / "option_architecture_scores.csv",
    option_rows,
    [
        "option_id",
        "idea_id",
        "option_role",
        "time_horizon",
        "commitment_level",
        "architecture_score",
        "architecture_flag",
        "reversibility",
        "dependency_complexity",
        "portfolio_fit",
        "scenario_robustness",
        "sequencing_value",
    ],
)

# ---------------------------------------------------------------------
# 5. Prototype learning plan
# ---------------------------------------------------------------------

prototype_rows: list[dict[str, object]] = []

for row in prototypes:
    idea_score = next((item["portfolio_score"] for item in portfolio_rows if item["idea_id"] == row["idea_id"]), 0.0)
    assumption_risk = assumption_risk_by_idea.get(row["idea_id"], 0.0)

    if assumption_risk >= 0.42:
        prototype_priority = "urgent_assumption_test"
    elif float(idea_score) >= 0.80:
        prototype_priority = "high_value_learning_probe"
    elif row["resource_intensity"] == "low":
        prototype_priority = "low_cost_learning_probe"
    else:
        prototype_priority = "standard_review"

    prototype_rows.append(
        {
            "prototype_id": row["prototype_id"],
            "idea_id": row["idea_id"],
            "prototype_name": row["prototype_name"],
            "review_layer": row["review_layer"],
            "estimated_weeks": row["estimated_weeks"],
            "resource_intensity": row["resource_intensity"],
            "prototype_priority": prototype_priority,
            "learning_goal": row["learning_goal"],
            "minimum_test": row["minimum_test"],
            "success_signal": row["success_signal"],
        }
    )

write_csv(
    TABLES / "prototype_learning_plan.csv",
    prototype_rows,
    [
        "prototype_id",
        "idea_id",
        "prototype_name",
        "review_layer",
        "estimated_weeks",
        "resource_intensity",
        "prototype_priority",
        "learning_goal",
        "minimum_test",
        "success_signal",
    ],
)

# ---------------------------------------------------------------------
# 6. Implementation pathway scoring
# ---------------------------------------------------------------------

pathway_rows: list[dict[str, object]] = []

for row in pathways:
    pathway_score = (
        0.20 * f(row, "owner_clarity")
        + 0.24 * f(row, "feedback_strength")
        + 0.22 * f(row, "governance_fit")
        - 0.10 * f(row, "scaling_risk")
        - 0.03 * f(row, "dependency_count")
    )

    if f(row, "owner_clarity") < 0.70:
        pathway_flag = "owner_clarity_gap"
    elif f(row, "scaling_risk") > 0.42:
        pathway_flag = "scaling_risk_review"
    elif f(row, "feedback_strength") < 0.75:
        pathway_flag = "feedback_weakness"
    else:
        pathway_flag = "implementation_ready_for_review"

    pathway_rows.append(
        {
            "pathway_id": row["pathway_id"],
            "idea_id": row["idea_id"],
            "pathway_name": row["pathway_name"],
            "pathway_score": round(pathway_score, 4),
            "pathway_flag": pathway_flag,
            "dependency_count": row["dependency_count"],
            "owner_clarity": row["owner_clarity"],
            "feedback_strength": row["feedback_strength"],
            "governance_fit": row["governance_fit"],
            "scaling_risk": row["scaling_risk"],
            "phase_1": row["phase_1"],
            "phase_2": row["phase_2"],
            "phase_3": row["phase_3"],
        }
    )

pathway_rows.sort(key=lambda row: row["pathway_score"], reverse=True)

write_csv(
    TABLES / "implementation_pathway_scores.csv",
    pathway_rows,
    [
        "pathway_id",
        "idea_id",
        "pathway_name",
        "pathway_score",
        "pathway_flag",
        "dependency_count",
        "owner_clarity",
        "feedback_strength",
        "governance_fit",
        "scaling_risk",
        "phase_1",
        "phase_2",
        "phase_3",
    ],
)

# ---------------------------------------------------------------------
# 7. Strategist report
# ---------------------------------------------------------------------

top_ideas = portfolio_rows[:5]
highest_risk_assumptions = assumption_rows[:5]
strongest_options = option_rows[:5]
prototype_priorities = [
    row for row in prototype_rows if row["prototype_priority"] in ("urgent_assumption_test", "high_value_learning_probe")
][:6]
pathway_gaps = [row for row in pathway_rows if row["pathway_flag"] != "implementation_ready_for_review"][:6]

report: list[str] = []

report.append("# Strategic Ideation Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic separates idea quality, option architecture, assumption risk, evidence strength, "
    "prototype design, and implementation pathway readiness. The purpose is to help strategists avoid "
    "confusing idea volume with strategic maturity."
)
report.append("")
report.append("## Top idea portfolio candidates")
report.append("")

for item in top_ideas:
    report.append(
        f"- **{item['idea_id']} — {item['idea_name']}**: score {item['portfolio_score']}; "
        f"recommendation: {item['recommendation']}; assumption risk: {item['assumption_risk']}; "
        f"evidence strength: {item['evidence_strength']}."
    )

report.append("")
report.append("## Strongest option architecture candidates")
report.append("")

for item in strongest_options:
    report.append(
        f"- **{item['option_id']} ({item['idea_id']})**: role {item['option_role']}; "
        f"score {item['architecture_score']}; flag: {item['architecture_flag']}."
    )

report.append("")
report.append("## Highest-risk assumptions")
report.append("")

for item in highest_risk_assumptions:
    report.append(
        f"- **{item['assumption_id']} ({item['idea_id']})**: risk {item['assumption_risk']}; "
        f"layer: {item['layer']}; urgency: {item['urgency']}; test: {item['test_method']}; "
        f"assumption: {item['assumption']}"
    )

report.append("")
report.append("## Prototype priorities")
report.append("")

for item in prototype_priorities:
    report.append(
        f"- **{item['prototype_id']} — {item['prototype_name']}**: {item['prototype_priority']}; "
        f"review layer: {item['review_layer']}; minimum test: {item['minimum_test']}."
    )

report.append("")
report.append("## Implementation pathway gaps")
report.append("")

for item in pathway_gaps:
    report.append(
        f"- **{item['pathway_id']} — {item['pathway_name']}**: flag {item['pathway_flag']}; "
        f"score {item['pathway_score']}; phases: {item['phase_1']} → {item['phase_2']} → {item['phase_3']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "The main value of this workflow is not the numeric score by itself. "
    "The value is disciplined separation: idea quality, strategic fit, assumption risk, evidence quality, "
    "option role, prototype design, implementation readiness, and learning governance can be reviewed separately "
    "before being combined into a strategic judgment."
)

(REPORTS / "strategic_ideation_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_ideas": top_ideas,
    "strongest_options": strongest_options,
    "highest_risk_assumptions": highest_risk_assumptions,
    "prototype_priorities": prototype_priorities,
    "pathway_gaps": pathway_gaps,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced strategic ideation diagnostics complete.")
print(f"Wrote: {TABLES / 'idea_portfolio_scores.csv'}")
print(f"Wrote: {TABLES / 'option_architecture_scores.csv'}")
print(f"Wrote: {TABLES / 'assumption_risk_register.csv'}")
print(f"Wrote: {TABLES / 'evidence_strength_register.csv'}")
print(f"Wrote: {TABLES / 'prototype_learning_plan.csv'}")
print(f"Wrote: {TABLES / 'implementation_pathway_scores.csv'}")
print(f"Wrote: {REPORTS / 'strategic_ideation_diagnostic_report.md'}")
