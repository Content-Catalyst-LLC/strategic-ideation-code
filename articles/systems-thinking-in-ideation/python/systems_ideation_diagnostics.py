#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for systems thinking in ideation.

This dependency-light workflow uses only the Python standard library.

It produces:
- systems-ideation scores
- feedback-loop review
- leverage-point review
- boundary quality review
- unintended-consequence review
- structural intervention portfolio review
- learning-loop review
- intervention recommendations
- a markdown strategist diagnostic report

The workflow is designed for strategy teams that need to move from
symptom-focused ideation to structural intervention design.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

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


systems = read_csv(RAW / "systems_profiles.csv")
feedback_loops = read_csv(RAW / "feedback_loops.csv")
leverage_points = read_csv(RAW / "leverage_points.csv")
boundaries = read_csv(RAW / "boundary_reviews.csv")
consequences = read_csv(RAW / "unintended_consequences.csv")
portfolios = read_csv(RAW / "intervention_portfolio.csv")
learning_loops = read_csv(RAW / "learning_loops.csv")
interventions = read_csv(RAW / "intervention_library.csv")

system_names = {row["system_id"]: row["system_name"] for row in systems}

# ---------------------------------------------------------------------
# 1. Systems-ideation profile scoring
# ---------------------------------------------------------------------

systems_rows: list[dict[str, object]] = []

for row in systems:
    systems_score = (
        0.14 * f(row, "feedback_awareness")
        + 0.14 * f(row, "leverage_sensitivity")
        + 0.13 * f(row, "root_cause_depth")
        + 0.12 * f(row, "stakeholder_visibility")
        + 0.12 * f(row, "boundary_quality")
        + 0.10 * f(row, "stock_flow_awareness")
        + 0.10 * f(row, "delay_awareness")
        + 0.13 * f(row, "adaptive_learning")
        - 0.10 * f(row, "unintended_consequence_risk")
        - 0.08 * f(row, "local_optimization_risk")
    )

    symptom_focus_risk = (
        (1.0 - f(row, "root_cause_depth")) * 0.30
        + (1.0 - f(row, "leverage_sensitivity")) * 0.25
        + f(row, "local_optimization_risk") * 0.25
        + f(row, "unintended_consequence_risk") * 0.20
    )

    boundary_gap = max(0.0, 0.70 - f(row, "boundary_quality"))
    feedback_gap = max(0.0, 0.70 - f(row, "feedback_awareness"))
    learning_gap = max(0.0, 0.70 - f(row, "adaptive_learning"))
    stakeholder_gap = max(0.0, 0.65 - f(row, "stakeholder_visibility"))

    if systems_score >= 0.68:
        diagnosis = "strong_systems_ideation_capacity"
    elif symptom_focus_risk >= 0.62:
        diagnosis = "symptom_or_local_optimization_risk"
    elif boundary_gap >= 0.25:
        diagnosis = "boundary_quality_gap"
    elif feedback_gap >= 0.25:
        diagnosis = "feedback_awareness_gap"
    elif learning_gap >= 0.25:
        diagnosis = "adaptive_learning_gap"
    else:
        diagnosis = "develop_with_structural_review"

    systems_rows.append(
        {
            "system_id": row["system_id"],
            "system_name": row["system_name"],
            "system_type": row["system_type"],
            "domain": row["domain"],
            "systems_ideation_score": round(systems_score, 4),
            "symptom_focus_risk": round(symptom_focus_risk, 4),
            "boundary_gap": round(boundary_gap, 4),
            "feedback_gap": round(feedback_gap, 4),
            "learning_gap": round(learning_gap, 4),
            "stakeholder_gap": round(stakeholder_gap, 4),
            "diagnosis": diagnosis,
            "feedback_awareness": row["feedback_awareness"],
            "leverage_sensitivity": row["leverage_sensitivity"],
            "root_cause_depth": row["root_cause_depth"],
            "stakeholder_visibility": row["stakeholder_visibility"],
            "boundary_quality": row["boundary_quality"],
            "stock_flow_awareness": row["stock_flow_awareness"],
            "delay_awareness": row["delay_awareness"],
            "adaptive_learning": row["adaptive_learning"],
            "unintended_consequence_risk": row["unintended_consequence_risk"],
            "local_optimization_risk": row["local_optimization_risk"],
            "description": row["description"],
        }
    )

systems_rows.sort(key=lambda item: item["systems_ideation_score"], reverse=True)

systems_fields = [
    "system_id",
    "system_name",
    "system_type",
    "domain",
    "systems_ideation_score",
    "symptom_focus_risk",
    "boundary_gap",
    "feedback_gap",
    "learning_gap",
    "stakeholder_gap",
    "diagnosis",
    "feedback_awareness",
    "leverage_sensitivity",
    "root_cause_depth",
    "stakeholder_visibility",
    "boundary_quality",
    "stock_flow_awareness",
    "delay_awareness",
    "adaptive_learning",
    "unintended_consequence_risk",
    "local_optimization_risk",
    "description",
]

write_csv(TABLES / "systems_ideation_scores.csv", systems_rows, systems_fields)
write_csv(PROCESSED / "systems_ideation_scores.csv", systems_rows, systems_fields)

# ---------------------------------------------------------------------
# 2. Feedback-loop review
# ---------------------------------------------------------------------

feedback_rows: list[dict[str, object]] = []

for row in feedback_loops:
    loop_quality = (
        0.16 * f(row, "loop_strength")
        + 0.16 * f(row, "visibility")
        + 0.18 * f(row, "intervention_readiness")
        + 0.16 * f(row, "balancing_capacity")
        - 0.12 * f(row, "reinforcing_risk")
        - 0.10 * f(row, "delay_risk")
        - 0.10 * f(row, "stakeholder_burden_risk")
    )

    if f(row, "reinforcing_risk") >= 0.75 and f(row, "balancing_capacity") < 0.40:
        action = "interrupt_reinforcing_problem_loop"
    elif f(row, "visibility") < 0.50:
        action = "make_feedback_visible"
    elif f(row, "stakeholder_burden_risk") >= 0.60:
        action = "review_burden_transfer"
    elif loop_quality >= 0.45:
        action = "usable_feedback_intervention_pathway"
    else:
        action = "strengthen_feedback_diagnosis"

    feedback_rows.append(
        {
            "loop_id": row["loop_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "loop_name": row["loop_name"],
            "loop_type": row["loop_type"],
            "feedback_loop_quality_score": round(loop_quality, 4),
            "recommended_action": action,
            "loop_strength": row["loop_strength"],
            "visibility": row["visibility"],
            "intervention_readiness": row["intervention_readiness"],
            "reinforcing_risk": row["reinforcing_risk"],
            "balancing_capacity": row["balancing_capacity"],
            "delay_risk": row["delay_risk"],
            "stakeholder_burden_risk": row["stakeholder_burden_risk"],
            "diagnostic_note": row["diagnostic_note"],
        }
    )

feedback_rows.sort(key=lambda item: item["feedback_loop_quality_score"], reverse=True)

write_csv(
    TABLES / "feedback_loop_review.csv",
    feedback_rows,
    [
        "loop_id",
        "system_id",
        "system_name",
        "loop_name",
        "loop_type",
        "feedback_loop_quality_score",
        "recommended_action",
        "loop_strength",
        "visibility",
        "intervention_readiness",
        "reinforcing_risk",
        "balancing_capacity",
        "delay_risk",
        "stakeholder_burden_risk",
        "diagnostic_note",
    ],
)

# ---------------------------------------------------------------------
# 3. Leverage-point review
# ---------------------------------------------------------------------

leverage_rows: list[dict[str, object]] = []

for row in leverage_points:
    leverage_value = (
        0.22 * f(row, "leverage_depth")
        + 0.12 * f(row, "implementation_feasibility")
        + 0.12 * f(row, "evidence_quality")
        + 0.12 * f(row, "stakeholder_legitimacy")
        + 0.08 * f(row, "reversibility")
        + 0.16 * f(row, "system_sensitivity")
        - 0.10 * f(row, "risk_exposure")
        - 0.08 * f(row, "time_to_effect")
    )

    if f(row, "leverage_depth") >= 0.80 and f(row, "risk_exposure") >= 0.60:
        action = "stage_high_leverage_intervention_with_guardrails"
    elif f(row, "stakeholder_legitimacy") < 0.60:
        action = "add_stakeholder_legitimacy_review"
    elif leverage_value >= 0.55:
        action = "priority_leverage_candidate"
    elif f(row, "leverage_depth") < 0.35:
        action = "low_leverage_surface_fix"
    else:
        action = "develop_or_compare_with_rivals"

    leverage_rows.append(
        {
            "leverage_id": row["leverage_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "intervention_name": row["intervention_name"],
            "leverage_level": row["leverage_level"],
            "leverage_value_score": round(leverage_value, 4),
            "recommended_action": action,
            "leverage_depth": row["leverage_depth"],
            "implementation_feasibility": row["implementation_feasibility"],
            "evidence_quality": row["evidence_quality"],
            "stakeholder_legitimacy": row["stakeholder_legitimacy"],
            "reversibility": row["reversibility"],
            "system_sensitivity": row["system_sensitivity"],
            "risk_exposure": row["risk_exposure"],
            "time_to_effect": row["time_to_effect"],
            "expected_system_effect": row["expected_system_effect"],
        }
    )

leverage_rows.sort(key=lambda item: item["leverage_value_score"], reverse=True)

write_csv(
    TABLES / "leverage_point_review.csv",
    leverage_rows,
    [
        "leverage_id",
        "system_id",
        "system_name",
        "intervention_name",
        "leverage_level",
        "leverage_value_score",
        "recommended_action",
        "leverage_depth",
        "implementation_feasibility",
        "evidence_quality",
        "stakeholder_legitimacy",
        "reversibility",
        "system_sensitivity",
        "risk_exposure",
        "time_to_effect",
        "expected_system_effect",
    ],
)

# ---------------------------------------------------------------------
# 4. Boundary quality review
# ---------------------------------------------------------------------

boundary_rows: list[dict[str, object]] = []

for row in boundaries:
    boundary_quality = (
        0.16 * f(row, "stakeholder_inclusion")
        + 0.14 * f(row, "downstream_effect_visibility")
        + 0.14 * f(row, "externality_visibility")
        + 0.14 * f(row, "implementation_visibility")
        + 0.14 * f(row, "ecological_or_social_context")
        + 0.14 * f(row, "hidden_dependency_visibility")
        - 0.12 * f(row, "boundary_risk")
    )

    if f(row, "boundary_risk") >= 0.70:
        action = "expand_boundary_before_ideation"
    elif f(row, "stakeholder_inclusion") < 0.50:
        action = "add_stakeholder_boundary_review"
    elif boundary_quality >= 0.55:
        action = "boundary_usable_with_review"
    else:
        action = "strengthen_boundary_definition"

    boundary_rows.append(
        {
            "boundary_id": row["boundary_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "boundary_name": row["boundary_name"],
            "boundary_scope": row["boundary_scope"],
            "boundary_quality_score": round(boundary_quality, 4),
            "recommended_action": action,
            "source_recommendation": row["review_recommendation"],
            "stakeholder_inclusion": row["stakeholder_inclusion"],
            "downstream_effect_visibility": row["downstream_effect_visibility"],
            "externality_visibility": row["externality_visibility"],
            "implementation_visibility": row["implementation_visibility"],
            "ecological_or_social_context": row["ecological_or_social_context"],
            "hidden_dependency_visibility": row["hidden_dependency_visibility"],
            "boundary_risk": row["boundary_risk"],
        }
    )

boundary_rows.sort(key=lambda item: item["boundary_quality_score"], reverse=True)

write_csv(
    TABLES / "boundary_quality_review.csv",
    boundary_rows,
    [
        "boundary_id",
        "system_id",
        "system_name",
        "boundary_name",
        "boundary_scope",
        "boundary_quality_score",
        "recommended_action",
        "source_recommendation",
        "stakeholder_inclusion",
        "downstream_effect_visibility",
        "externality_visibility",
        "implementation_visibility",
        "ecological_or_social_context",
        "hidden_dependency_visibility",
        "boundary_risk",
    ],
)

# ---------------------------------------------------------------------
# 5. Unintended-consequence review
# ---------------------------------------------------------------------

consequence_rows: list[dict[str, object]] = []

for row in consequences:
    consequence_risk = (
        0.20 * f(row, "likelihood")
        + 0.20 * f(row, "severity")
        + 0.16 * f(row, "stakeholder_burden")
        + 0.12 * f(row, "delay_length")
        - 0.12 * f(row, "detectability")
        - 0.10 * f(row, "reversibility")
        - 0.10 * f(row, "mitigation_quality")
    )

    if consequence_risk >= 0.45 and f(row, "mitigation_quality") < 0.60:
        action = "mitigation_required_before_commitment"
    elif f(row, "stakeholder_burden") >= 0.70:
        action = "burden_safeguards_required"
    elif consequence_risk >= 0.35:
        action = "monitor_with_review_trigger"
    else:
        action = "risk_manageable_with_monitoring"

    consequence_rows.append(
        {
            "consequence_id": row["consequence_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "intervention_name": row["intervention_name"],
            "consequence_type": row["consequence_type"],
            "consequence_risk_score": round(consequence_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "likelihood": row["likelihood"],
            "severity": row["severity"],
            "detectability": row["detectability"],
            "reversibility": row["reversibility"],
            "stakeholder_burden": row["stakeholder_burden"],
            "delay_length": row["delay_length"],
            "mitigation_quality": row["mitigation_quality"],
        }
    )

consequence_rows.sort(key=lambda item: item["consequence_risk_score"], reverse=True)

write_csv(
    TABLES / "unintended_consequence_review.csv",
    consequence_rows,
    [
        "consequence_id",
        "system_id",
        "system_name",
        "intervention_name",
        "consequence_type",
        "consequence_risk_score",
        "recommended_action",
        "source_review_action",
        "likelihood",
        "severity",
        "detectability",
        "reversibility",
        "stakeholder_burden",
        "delay_length",
        "mitigation_quality",
    ],
)

# ---------------------------------------------------------------------
# 6. Structural intervention portfolio review
# ---------------------------------------------------------------------

portfolio_rows: list[dict[str, object]] = []

for row in portfolios:
    portfolio_value = (
        0.14 * f(row, "confidence_level")
        + 0.14 * f(row, "evidence_readiness")
        + 0.18 * f(row, "strategic_option_value")
        + 0.16 * f(row, "learning_value")
        - 0.10 * f(row, "resource_intensity")
        + 0.12 * f(row, "time_sensitivity")
        - 0.10 * f(row, "risk_exposure")
    )

    if row["portfolio_role"] == "surface_fix":
        action = "do_not_treat_as_structural_strategy"
    elif f(row, "risk_exposure") >= 0.60 and f(row, "evidence_readiness") < 0.65:
        action = "stage_commitment_and_strengthen_evidence"
    elif portfolio_value >= 0.58:
        action = "active_systems_intervention_priority"
    else:
        action = "monitor_or_reframe"

    portfolio_rows.append(
        {
            "portfolio_id": row["portfolio_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "intervention_name": row["intervention_name"],
            "portfolio_role": row["portfolio_role"],
            "leverage_level": row["leverage_level"],
            "portfolio_value_score": round(portfolio_value, 4),
            "recommended_action": action,
            "source_portfolio_action": row["portfolio_action"],
            "confidence_level": row["confidence_level"],
            "evidence_readiness": row["evidence_readiness"],
            "strategic_option_value": row["strategic_option_value"],
            "learning_value": row["learning_value"],
            "resource_intensity": row["resource_intensity"],
            "time_sensitivity": row["time_sensitivity"],
            "risk_exposure": row["risk_exposure"],
        }
    )

portfolio_rows.sort(key=lambda item: item["portfolio_value_score"], reverse=True)

write_csv(
    TABLES / "intervention_portfolio_review.csv",
    portfolio_rows,
    [
        "portfolio_id",
        "system_id",
        "system_name",
        "intervention_name",
        "portfolio_role",
        "leverage_level",
        "portfolio_value_score",
        "recommended_action",
        "source_portfolio_action",
        "confidence_level",
        "evidence_readiness",
        "strategic_option_value",
        "learning_value",
        "resource_intensity",
        "time_sensitivity",
        "risk_exposure",
    ],
)

# ---------------------------------------------------------------------
# 7. Learning-loop review
# ---------------------------------------------------------------------

learning_rows: list[dict[str, object]] = []

for row in learning_loops:
    learning_quality = (
        0.16 * f(row, "feedback_quality")
        + 0.16 * f(row, "revision_trigger_clarity")
        + 0.16 * f(row, "decision_memory_quality")
        + 0.14 * f(row, "stakeholder_learning_visibility")
        + 0.14 * f(row, "implementation_signal_quality")
        + 0.14 * f(row, "governance_response_capacity")
        + 0.08 * f(row, "cycle_time")
        - 0.10 * f(row, "learning_risk")
    )

    if f(row, "decision_memory_quality") < 0.45:
        action = "build_decision_memory"
    elif f(row, "revision_trigger_clarity") < 0.50:
        action = "define_revision_triggers"
    elif f(row, "learning_risk") >= 0.60:
        action = "repair_learning_loop"
    elif learning_quality >= 0.58:
        action = "learning_loop_ready_for_use"
    else:
        action = "strengthen_learning_loop"

    learning_rows.append(
        {
            "learning_id": row["learning_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "learning_loop_name": row["learning_loop_name"],
            "learning_quality_score": round(learning_quality, 4),
            "recommended_action": action,
            "action_if_triggered": row["action_if_triggered"],
            "feedback_quality": row["feedback_quality"],
            "revision_trigger_clarity": row["revision_trigger_clarity"],
            "decision_memory_quality": row["decision_memory_quality"],
            "stakeholder_learning_visibility": row["stakeholder_learning_visibility"],
            "implementation_signal_quality": row["implementation_signal_quality"],
            "governance_response_capacity": row["governance_response_capacity"],
            "cycle_time": row["cycle_time"],
            "learning_risk": row["learning_risk"],
        }
    )

learning_rows.sort(key=lambda item: item["learning_quality_score"], reverse=True)

write_csv(
    TABLES / "learning_loop_review.csv",
    learning_rows,
    [
        "learning_id",
        "system_id",
        "system_name",
        "learning_loop_name",
        "learning_quality_score",
        "recommended_action",
        "action_if_triggered",
        "feedback_quality",
        "revision_trigger_clarity",
        "decision_memory_quality",
        "stakeholder_learning_visibility",
        "implementation_signal_quality",
        "governance_response_capacity",
        "cycle_time",
        "learning_risk",
    ],
)

# ---------------------------------------------------------------------
# 8. Intervention recommendations
# ---------------------------------------------------------------------

intervention_rows: list[dict[str, object]] = []

for row in interventions:
    intervention_value = (
        0.14 * f(row, "structure_quality_gain")
        + 0.14 * f(row, "feedback_gain")
        + 0.16 * f(row, "leverage_gain")
        + 0.14 * f(row, "stakeholder_gain")
        + 0.14 * f(row, "boundary_gain")
        + 0.14 * f(row, "learning_gain")
        + 0.14 * f(row, "unintended_consequence_reduction")
        - 0.10 * f(row, "process_cost")
        - 0.08 * f(row, "implementation_complexity")
        - 0.08 * f(row, "political_safety_need")
    )

    if f(row, "political_safety_need") >= 0.45:
        action = "requires_leadership_protection"
    elif intervention_value >= 0.55:
        action = "high_value_systems_ideation_intervention"
    else:
        action = "supporting_intervention"

    intervention_rows.append(
        {
            "intervention_id": row["intervention_id"],
            "intervention_name": row["intervention_name"],
            "target_systems_risk": row["target_systems_risk"],
            "intervention_value_score": round(intervention_value, 4),
            "recommended_action": action,
            "process_cost": row["process_cost"],
            "implementation_complexity": row["implementation_complexity"],
            "structure_quality_gain": row["structure_quality_gain"],
            "feedback_gain": row["feedback_gain"],
            "leverage_gain": row["leverage_gain"],
            "stakeholder_gain": row["stakeholder_gain"],
            "boundary_gain": row["boundary_gain"],
            "learning_gain": row["learning_gain"],
            "unintended_consequence_reduction": row["unintended_consequence_reduction"],
            "political_safety_need": row["political_safety_need"],
        }
    )

intervention_rows.sort(key=lambda item: item["intervention_value_score"], reverse=True)

write_csv(
    TABLES / "intervention_recommendations.csv",
    intervention_rows,
    [
        "intervention_id",
        "intervention_name",
        "target_systems_risk",
        "intervention_value_score",
        "recommended_action",
        "process_cost",
        "implementation_complexity",
        "structure_quality_gain",
        "feedback_gain",
        "leverage_gain",
        "stakeholder_gain",
        "boundary_gain",
        "learning_gain",
        "unintended_consequence_reduction",
        "political_safety_need",
    ],
)

# ---------------------------------------------------------------------
# 9. Strategist report
# ---------------------------------------------------------------------

top_systems = systems_rows[:5]
weak_systems = sorted(systems_rows, key=lambda item: item["systems_ideation_score"])[:4]
feedback_risks = sorted(feedback_rows, key=lambda item: item["feedback_loop_quality_score"])[:5]
top_leverage = leverage_rows[:6]
weak_boundaries = sorted(boundary_rows, key=lambda item: item["boundary_quality_score"])[:5]
highest_consequence = consequence_rows[:5]
top_portfolio = portfolio_rows[:6]
weak_learning = sorted(learning_rows, key=lambda item: item["learning_quality_score"])[:5]
top_interventions = intervention_rows[:6]

report: list[str] = []

report.append("# Systems Thinking in Ideation Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic separates systems-ideation capacity, symptom-focus risk, feedback-loop quality, leverage-point value, "
    "boundary quality, unintended-consequence risk, intervention portfolio value, learning-loop quality, and intervention priority. "
    "The purpose is to help strategists move from surface ideation to structural intervention design."
)
report.append("")
report.append("## Strongest systems-ideation capacities")
report.append("")

for item in top_systems:
    report.append(
        f"- **{item['system_id']} — {item['system_name']}**: score {item['systems_ideation_score']}; "
        f"diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Weakest or most symptom-focused systems")
report.append("")

for item in weak_systems:
    report.append(
        f"- **{item['system_id']} — {item['system_name']}**: score {item['systems_ideation_score']}; "
        f"symptom-focus risk {item['symptom_focus_risk']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Feedback loops needing attention")
report.append("")

for item in feedback_risks:
    report.append(
        f"- **{item['loop_id']} — {item['loop_name']}** in **{item['system_name']}**: "
        f"quality {item['feedback_loop_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest-value leverage candidates")
report.append("")

for item in top_leverage:
    report.append(
        f"- **{item['leverage_id']} — {item['intervention_name']}** ({item['leverage_level']}): "
        f"value {item['leverage_value_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weakest boundary definitions")
report.append("")

for item in weak_boundaries:
    report.append(
        f"- **{item['boundary_id']} — {item['boundary_name']}** in **{item['system_name']}**: "
        f"boundary score {item['boundary_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest unintended-consequence risks")
report.append("")

for item in highest_consequence:
    report.append(
        f"- **{item['consequence_id']} — {item['intervention_name']}**: "
        f"{item['consequence_type']} risk {item['consequence_risk_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest-value structural intervention portfolio items")
report.append("")

for item in top_portfolio:
    report.append(
        f"- **{item['portfolio_id']} — {item['intervention_name']}** ({item['leverage_level']}): "
        f"portfolio value {item['portfolio_value_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Learning loops needing repair")
report.append("")

for item in weak_learning:
    report.append(
        f"- **{item['learning_id']} — {item['learning_loop_name']}** in **{item['system_name']}**: "
        f"learning quality {item['learning_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest-value systems-ideation interventions")
report.append("")

for item in top_interventions:
    report.append(
        f"- **{item['intervention_id']} — {item['intervention_name']}**: value {item['intervention_value_score']}; "
        f"target: {item['target_systems_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "The value of this workflow is structural creativity. It helps teams avoid symptom substitution, boundary blindness, "
    "local optimization, low-leverage surface fixes, unintended consequences, complexity paralysis, false precision, and "
    "learning-loop failure. It supports systems thinking as a strategy discipline: diagnose recurring patterns, map structure, "
    "locate leverage, test consequences, stage interventions, and learn from how the system responds."
)

(REPORTS / "systems_ideation_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_systems": top_systems,
    "weak_systems": weak_systems,
    "feedback_risks": feedback_risks,
    "top_leverage": top_leverage,
    "weak_boundaries": weak_boundaries,
    "highest_consequence": highest_consequence,
    "top_portfolio": top_portfolio,
    "weak_learning": weak_learning,
    "top_interventions": top_interventions,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced systems-ideation diagnostics complete.")
print(f"Wrote: {TABLES / 'systems_ideation_scores.csv'}")
print(f"Wrote: {TABLES / 'feedback_loop_review.csv'}")
print(f"Wrote: {TABLES / 'leverage_point_review.csv'}")
print(f"Wrote: {TABLES / 'boundary_quality_review.csv'}")
print(f"Wrote: {TABLES / 'unintended_consequence_review.csv'}")
print(f"Wrote: {TABLES / 'intervention_portfolio_review.csv'}")
print(f"Wrote: {TABLES / 'learning_loop_review.csv'}")
print(f"Wrote: {TABLES / 'intervention_recommendations.csv'}")
print(f"Wrote: {REPORTS / 'systems_ideation_diagnostic_report.md'}")
