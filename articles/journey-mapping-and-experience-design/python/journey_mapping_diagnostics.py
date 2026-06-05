#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Journey Mapping and Experience Design.

This dependency-light workflow uses only the Python standard library.

It produces:
- journey profile scores
- stage friction scores
- touchpoint quality scores
- transition risk scores
- accessibility and dignity review
- trust and status scores
- decision pathway scores
- service blueprint dependency scores
- redesign priority scores
- measurement and learning scores
- a markdown strategist diagnostic report
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


contexts = read_csv(RAW / "journey_contexts.csv")
stages = read_csv(RAW / "journey_stages.csv")
touchpoints = read_csv(RAW / "touchpoints.csv")
transitions = read_csv(RAW / "transitions.csv")
accessibility = read_csv(RAW / "accessibility_dignity.csv")
trust = read_csv(RAW / "trust_status.csv")
decision_paths = read_csv(RAW / "decision_pathways.csv")
blueprints = read_csv(RAW / "service_blueprint.csv")
interventions = read_csv(RAW / "redesign_interventions.csv")
learning = read_csv(RAW / "measurement_learning.csv")

journey_names = {row["journey_id"]: row["journey_name"] for row in contexts}
stage_names = {row["stage_id"]: row["stage_name"] for row in stages}

# ---------------------------------------------------------------------
# 1. Journey profile scoring
# ---------------------------------------------------------------------

journey_rows: list[dict[str, object]] = []

for row in contexts:
    profile_score = (
        0.15 * f(row, "clarity")
        + 0.12 * f(row, "emotional_confidence")
        - 0.18 * f(row, "friction")
        + 0.14 * f(row, "transition_quality")
        + 0.12 * f(row, "accessibility")
        + 0.12 * f(row, "trust")
        + 0.10 * f(row, "completion_support")
        + 0.10 * f(row, "backstage_alignment")
        + 0.07 * f(row, "measurement_quality")
    )

    redesign_need = (
        0.22 * f(row, "friction")
        + 0.16 * (1 - f(row, "transition_quality"))
        + 0.14 * (1 - f(row, "accessibility"))
        + 0.13 * (1 - f(row, "trust"))
        + 0.12 * (1 - f(row, "clarity"))
        + 0.11 * (1 - f(row, "backstage_alignment"))
        + 0.07 * (1 - f(row, "completion_support"))
        + 0.05 * (1 - f(row, "measurement_quality"))
    )

    if profile_score >= 0.58:
        diagnosis = "strong_experience_design_profile"
    elif redesign_need >= 0.62:
        diagnosis = "high_redesign_priority"
    elif f(row, "transition_quality") < 0.45:
        diagnosis = "transition_and_handoff_failure"
    elif f(row, "accessibility") < 0.50:
        diagnosis = "accessibility_and_access_burden_risk"
    else:
        diagnosis = "developing_journey_quality"

    journey_rows.append(
        {
            "journey_id": row["journey_id"],
            "journey_name": row["journey_name"],
            "organization_type": row["organization_type"],
            "domain": row["domain"],
            "journey_profile_score": round(profile_score, 4),
            "redesign_need_score": round(redesign_need, 4),
            "diagnosis": diagnosis,
            "clarity": row["clarity"],
            "emotional_confidence": row["emotional_confidence"],
            "friction": row["friction"],
            "transition_quality": row["transition_quality"],
            "accessibility": row["accessibility"],
            "trust": row["trust"],
            "completion_support": row["completion_support"],
            "backstage_alignment": row["backstage_alignment"],
            "measurement_quality": row["measurement_quality"],
            "description": row["description"],
        }
    )

journey_rows.sort(key=lambda item: item["journey_profile_score"], reverse=True)

journey_fields = [
    "journey_id",
    "journey_name",
    "organization_type",
    "domain",
    "journey_profile_score",
    "redesign_need_score",
    "diagnosis",
    "clarity",
    "emotional_confidence",
    "friction",
    "transition_quality",
    "accessibility",
    "trust",
    "completion_support",
    "backstage_alignment",
    "measurement_quality",
    "description",
]

write_csv(TABLES / "journey_profile_scores.csv", journey_rows, journey_fields)
write_csv(PROCESSED / "journey_profile_scores.csv", journey_rows, journey_fields)

# ---------------------------------------------------------------------
# 2. Stage friction scoring
# ---------------------------------------------------------------------

stage_rows: list[dict[str, object]] = []

for row in stages:
    accumulated_friction = (
        0.13 * f(row, "time_cost")
        + 0.14 * f(row, "cognitive_load")
        + 0.14 * f(row, "emotional_cost")
        + 0.14 * f(row, "trust_risk")
        + 0.12 * f(row, "accessibility_burden")
        + 0.13 * f(row, "uncertainty")
        + 0.10 * f(row, "workaround_dependency")
        + 0.10 * f(row, "dropoff_risk")
    )

    if accumulated_friction >= 0.68:
        action = "high_priority_friction_reduction"
    elif f(row, "trust_risk") >= 0.70:
        action = "trust_repair_required"
    elif f(row, "accessibility_burden") >= 0.65:
        action = "accessibility_redesign_required"
    elif f(row, "dropoff_risk") >= 0.65:
        action = "dropoff_intervention_required"
    else:
        action = "monitor_and_refine"

    stage_rows.append(
        {
            "stage_id": row["stage_id"],
            "journey_id": row["journey_id"],
            "journey_name": journey_names.get(row["journey_id"], row["journey_id"]),
            "stage_order": row["stage_order"],
            "stage_name": row["stage_name"],
            "touchpoint_type": row["touchpoint_type"],
            "accumulated_friction_score": round(accumulated_friction, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "time_cost": row["time_cost"],
            "cognitive_load": row["cognitive_load"],
            "emotional_cost": row["emotional_cost"],
            "trust_risk": row["trust_risk"],
            "accessibility_burden": row["accessibility_burden"],
            "uncertainty": row["uncertainty"],
            "workaround_dependency": row["workaround_dependency"],
            "dropoff_risk": row["dropoff_risk"],
        }
    )

stage_rows.sort(key=lambda item: item["accumulated_friction_score"], reverse=True)

write_csv(
    TABLES / "stage_friction_scores.csv",
    stage_rows,
    [
        "stage_id",
        "journey_id",
        "journey_name",
        "stage_order",
        "stage_name",
        "touchpoint_type",
        "accumulated_friction_score",
        "recommended_action",
        "source_review_action",
        "time_cost",
        "cognitive_load",
        "emotional_cost",
        "trust_risk",
        "accessibility_burden",
        "uncertainty",
        "workaround_dependency",
        "dropoff_risk",
    ],
)

# ---------------------------------------------------------------------
# 3. Touchpoint quality scoring
# ---------------------------------------------------------------------

touchpoint_rows: list[dict[str, object]] = []

for row in touchpoints:
    touchpoint_quality = (
        0.14 * f(row, "clarity")
        + 0.13 * f(row, "status_visibility")
        + 0.12 * f(row, "response_quality")
        + 0.11 * f(row, "emotional_support")
        + 0.12 * f(row, "accessibility_quality")
        + 0.13 * f(row, "error_recovery")
        + 0.11 * f(row, "privacy_confidence")
        + 0.14 * f(row, "decision_support")
    )

    if touchpoint_quality >= 0.74:
        action = "strong_touchpoint"
    elif f(row, "error_recovery") < 0.40:
        action = "redesign_error_recovery"
    elif f(row, "status_visibility") < 0.40:
        action = "improve_status_visibility"
    elif f(row, "accessibility_quality") < 0.45:
        action = "accessibility_review_required"
    else:
        action = "improve_touchpoint_quality"

    touchpoint_rows.append(
        {
            "touchpoint_id": row["touchpoint_id"],
            "journey_id": row["journey_id"],
            "journey_name": journey_names.get(row["journey_id"], row["journey_id"]),
            "stage_id": row["stage_id"],
            "stage_name": stage_names.get(row["stage_id"], row["stage_id"]),
            "touchpoint_name": row["touchpoint_name"],
            "channel": row["channel"],
            "touchpoint_quality_score": round(touchpoint_quality, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "clarity": row["clarity"],
            "status_visibility": row["status_visibility"],
            "response_quality": row["response_quality"],
            "emotional_support": row["emotional_support"],
            "accessibility_quality": row["accessibility_quality"],
            "error_recovery": row["error_recovery"],
            "privacy_confidence": row["privacy_confidence"],
            "decision_support": row["decision_support"],
        }
    )

touchpoint_rows.sort(key=lambda item: item["touchpoint_quality_score"], reverse=True)

write_csv(
    TABLES / "touchpoint_quality_scores.csv",
    touchpoint_rows,
    [
        "touchpoint_id",
        "journey_id",
        "journey_name",
        "stage_id",
        "stage_name",
        "touchpoint_name",
        "channel",
        "touchpoint_quality_score",
        "recommended_action",
        "source_review_action",
        "clarity",
        "status_visibility",
        "response_quality",
        "emotional_support",
        "accessibility_quality",
        "error_recovery",
        "privacy_confidence",
        "decision_support",
    ],
)

# ---------------------------------------------------------------------
# 4. Transition risk scoring
# ---------------------------------------------------------------------

transition_rows: list[dict[str, object]] = []

for row in transitions:
    transition_risk = (
        0.15 * f(row, "context_loss")
        + 0.13 * f(row, "ownership_ambiguity")
        + 0.12 * f(row, "delay_risk")
        + 0.13 * f(row, "repetition_required")
        + 0.14 * f(row, "status_gap")
        + 0.08 * f(row, "privacy_risk")
        + 0.13 * f(row, "user_coordination_labor")
        + 0.12 * f(row, "transition_criticality")
    )

    if transition_risk >= 0.70:
        action = "critical_transition_redesign"
    elif f(row, "context_loss") >= 0.75:
        action = "fix_context_transfer"
    elif f(row, "status_gap") >= 0.70:
        action = "make_status_visible"
    elif f(row, "user_coordination_labor") >= 0.70:
        action = "reduce_user_coordination_labor"
    else:
        action = "monitor_transition"

    transition_rows.append(
        {
            "transition_id": row["transition_id"],
            "journey_id": row["journey_id"],
            "journey_name": journey_names.get(row["journey_id"], row["journey_id"]),
            "from_stage": row["from_stage"],
            "to_stage": row["to_stage"],
            "transition_type": row["transition_type"],
            "transition_risk_score": round(transition_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "context_loss": row["context_loss"],
            "ownership_ambiguity": row["ownership_ambiguity"],
            "delay_risk": row["delay_risk"],
            "repetition_required": row["repetition_required"],
            "status_gap": row["status_gap"],
            "privacy_risk": row["privacy_risk"],
            "user_coordination_labor": row["user_coordination_labor"],
            "transition_criticality": row["transition_criticality"],
        }
    )

transition_rows.sort(key=lambda item: item["transition_risk_score"], reverse=True)

write_csv(
    TABLES / "transition_risk_scores.csv",
    transition_rows,
    [
        "transition_id",
        "journey_id",
        "journey_name",
        "from_stage",
        "to_stage",
        "transition_type",
        "transition_risk_score",
        "recommended_action",
        "source_review_action",
        "context_loss",
        "ownership_ambiguity",
        "delay_risk",
        "repetition_required",
        "status_gap",
        "privacy_risk",
        "user_coordination_labor",
        "transition_criticality",
    ],
)

# ---------------------------------------------------------------------
# 5. Accessibility and dignity review
# ---------------------------------------------------------------------

access_rows: list[dict[str, object]] = []

for row in accessibility:
    accessibility_score = (
        0.14 * f(row, "language_access")
        + 0.16 * f(row, "disability_access")
        + 0.12 * f(row, "device_access")
        + 0.13 * f(row, "literacy_support")
        + 0.11 * f(row, "time_flexibility")
        + 0.16 * f(row, "dignity_protection")
        + 0.12 * f(row, "recovery_path_quality")
        - 0.12 * f(row, "equity_risk")
    )

    risk_score = 1 - min(max(accessibility_score, 0), 1)

    if risk_score >= 0.58:
        action = "accessibility_and_dignity_redesign_required"
    elif f(row, "disability_access") < 0.50:
        action = "disability_access_review_required"
    elif f(row, "recovery_path_quality") < 0.45:
        action = "build_recovery_path"
    elif f(row, "equity_risk") >= 0.65:
        action = "equity_risk_review_required"
    else:
        action = "maintain_and_monitor_access"

    access_rows.append(
        {
            "access_id": row["access_id"],
            "journey_id": row["journey_id"],
            "journey_name": journey_names.get(row["journey_id"], row["journey_id"]),
            "access_issue": row["access_issue"],
            "accessibility_dignity_score": round(accessibility_score, 4),
            "accessibility_dignity_risk": round(risk_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "language_access": row["language_access"],
            "disability_access": row["disability_access"],
            "device_access": row["device_access"],
            "literacy_support": row["literacy_support"],
            "time_flexibility": row["time_flexibility"],
            "dignity_protection": row["dignity_protection"],
            "recovery_path_quality": row["recovery_path_quality"],
            "equity_risk": row["equity_risk"],
        }
    )

access_rows.sort(key=lambda item: item["accessibility_dignity_risk"], reverse=True)

write_csv(
    TABLES / "accessibility_dignity_review.csv",
    access_rows,
    [
        "access_id",
        "journey_id",
        "journey_name",
        "access_issue",
        "accessibility_dignity_score",
        "accessibility_dignity_risk",
        "recommended_action",
        "source_review_action",
        "language_access",
        "disability_access",
        "device_access",
        "literacy_support",
        "time_flexibility",
        "dignity_protection",
        "recovery_path_quality",
        "equity_risk",
    ],
)

# ---------------------------------------------------------------------
# 6. Trust and status review
# ---------------------------------------------------------------------

trust_rows: list[dict[str, object]] = []

for row in trust:
    trust_score = (
        0.16 * f(row, "status_visibility")
        + 0.13 * f(row, "commitment_clarity")
        + 0.12 * f(row, "privacy_confidence")
        + 0.13 * f(row, "consistency")
        + 0.12 * f(row, "response_timeliness")
        + 0.13 * f(row, "explanation_quality")
        + 0.10 * f(row, "escalation_visibility")
        + 0.11 * f(row, "trust_repair_capacity")
    )

    if trust_score >= 0.75:
        action = "strong_trust_status_design"
    elif f(row, "status_visibility") < 0.45:
        action = "make_status_visible"
    elif f(row, "explanation_quality") < 0.45:
        action = "improve_explanation_quality"
    elif f(row, "trust_repair_capacity") < 0.45:
        action = "design_trust_repair"
    else:
        action = "strengthen_trust_signals"

    trust_rows.append(
        {
            "trust_id": row["trust_id"],
            "journey_id": row["journey_id"],
            "journey_name": journey_names.get(row["journey_id"], row["journey_id"]),
            "trust_issue": row["trust_issue"],
            "trust_status_score": round(trust_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "status_visibility": row["status_visibility"],
            "commitment_clarity": row["commitment_clarity"],
            "privacy_confidence": row["privacy_confidence"],
            "consistency": row["consistency"],
            "response_timeliness": row["response_timeliness"],
            "explanation_quality": row["explanation_quality"],
            "escalation_visibility": row["escalation_visibility"],
            "trust_repair_capacity": row["trust_repair_capacity"],
        }
    )

trust_rows.sort(key=lambda item: item["trust_status_score"], reverse=True)

write_csv(
    TABLES / "trust_status_scores.csv",
    trust_rows,
    [
        "trust_id",
        "journey_id",
        "journey_name",
        "trust_issue",
        "trust_status_score",
        "recommended_action",
        "source_review_action",
        "status_visibility",
        "commitment_clarity",
        "privacy_confidence",
        "consistency",
        "response_timeliness",
        "explanation_quality",
        "escalation_visibility",
        "trust_repair_capacity",
    ],
)

# ---------------------------------------------------------------------
# 7. Decision pathway scoring
# ---------------------------------------------------------------------

decision_rows: list[dict[str, object]] = []

for row in decision_paths:
    decision_quality = (
        0.14 * f(row, "choice_clarity")
        + 0.12 * f(row, "risk_visibility")
        + 0.11 * f(row, "default_quality")
        + 0.10 * f(row, "timing_fit")
        + 0.15 * f(row, "cognitive_support")
        + 0.14 * f(row, "consequence_clarity")
        + 0.12 * f(row, "recovery_visibility")
        - 0.12 * f(row, "behavioral_risk")
    )

    risk_score = 1 - min(max(decision_quality, 0), 1)

    if risk_score >= 0.60:
        action = "redesign_decision_pathway"
    elif f(row, "choice_clarity") < 0.45:
        action = "clarify_choice"
    elif f(row, "recovery_visibility") < 0.45:
        action = "make_recovery_visible"
    elif f(row, "behavioral_risk") >= 0.70:
        action = "reduce_behavioral_risk"
    else:
        action = "maintain_decision_support"

    decision_rows.append(
        {
            "decision_id": row["decision_id"],
            "journey_id": row["journey_id"],
            "journey_name": journey_names.get(row["journey_id"], row["journey_id"]),
            "stage_id": row["stage_id"],
            "stage_name": stage_names.get(row["stage_id"], row["stage_id"]),
            "decision_point": row["decision_point"],
            "decision_pathway_score": round(decision_quality, 4),
            "decision_pathway_risk": round(risk_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "choice_clarity": row["choice_clarity"],
            "risk_visibility": row["risk_visibility"],
            "default_quality": row["default_quality"],
            "timing_fit": row["timing_fit"],
            "cognitive_support": row["cognitive_support"],
            "consequence_clarity": row["consequence_clarity"],
            "recovery_visibility": row["recovery_visibility"],
            "behavioral_risk": row["behavioral_risk"],
        }
    )

decision_rows.sort(key=lambda item: item["decision_pathway_risk"], reverse=True)

write_csv(
    TABLES / "decision_pathway_scores.csv",
    decision_rows,
    [
        "decision_id",
        "journey_id",
        "journey_name",
        "stage_id",
        "stage_name",
        "decision_point",
        "decision_pathway_score",
        "decision_pathway_risk",
        "recommended_action",
        "source_review_action",
        "choice_clarity",
        "risk_visibility",
        "default_quality",
        "timing_fit",
        "cognitive_support",
        "consequence_clarity",
        "recovery_visibility",
        "behavioral_risk",
    ],
)

# ---------------------------------------------------------------------
# 8. Service blueprint dependency scoring
# ---------------------------------------------------------------------

blueprint_rows: list[dict[str, object]] = []

for row in blueprints:
    dependency_score = (
        0.14 * f(row, "dependency_quality")
        + 0.14 * f(row, "data_continuity")
        + 0.12 * f(row, "role_clarity")
        + 0.12 * f(row, "workflow_fit")
        + 0.10 * f(row, "staff_capacity")
        + 0.12 * f(row, "governance_alignment")
        + 0.12 * f(row, "feedback_loop_quality")
        - 0.14 * f(row, "implementation_risk")
    )

    dependency_risk = 1 - min(max(dependency_score, 0), 1)

    if dependency_risk >= 0.60:
        action = "backstage_redesign_required"
    elif f(row, "data_continuity") < 0.45:
        action = "fix_data_continuity"
    elif f(row, "role_clarity") < 0.45:
        action = "clarify_roles"
    elif f(row, "governance_alignment") < 0.45:
        action = "align_governance"
    else:
        action = "maintain_blueprint_alignment"

    blueprint_rows.append(
        {
            "blueprint_id": row["blueprint_id"],
            "journey_id": row["journey_id"],
            "journey_name": journey_names.get(row["journey_id"], row["journey_id"]),
            "visible_experience": row["visible_experience"],
            "backstage_dependency": row["backstage_dependency"],
            "service_blueprint_score": round(dependency_score, 4),
            "service_blueprint_risk": round(dependency_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "dependency_quality": row["dependency_quality"],
            "data_continuity": row["data_continuity"],
            "role_clarity": row["role_clarity"],
            "workflow_fit": row["workflow_fit"],
            "staff_capacity": row["staff_capacity"],
            "governance_alignment": row["governance_alignment"],
            "feedback_loop_quality": row["feedback_loop_quality"],
            "implementation_risk": row["implementation_risk"],
        }
    )

blueprint_rows.sort(key=lambda item: item["service_blueprint_risk"], reverse=True)

write_csv(
    TABLES / "service_blueprint_dependency_scores.csv",
    blueprint_rows,
    [
        "blueprint_id",
        "journey_id",
        "journey_name",
        "visible_experience",
        "backstage_dependency",
        "service_blueprint_score",
        "service_blueprint_risk",
        "recommended_action",
        "source_review_action",
        "dependency_quality",
        "data_continuity",
        "role_clarity",
        "workflow_fit",
        "staff_capacity",
        "governance_alignment",
        "feedback_loop_quality",
        "implementation_risk",
    ],
)

# ---------------------------------------------------------------------
# 9. Redesign priority scoring
# ---------------------------------------------------------------------

redesign_rows: list[dict[str, object]] = []

for row in interventions:
    redesign_value = (
        0.17 * f(row, "friction_reduction")
        + 0.14 * f(row, "trust_gain")
        + 0.14 * f(row, "accessibility_gain")
        + 0.15 * f(row, "transition_gain")
        + 0.10 * f(row, "implementation_feasibility")
        + 0.08 * f(row, "cost_efficiency")
        + 0.12 * f(row, "ethical_quality")
        + 0.10 * f(row, "learning_value")
    )

    if redesign_value >= 0.72:
        action = "high_value_redesign_candidate"
    elif f(row, "implementation_feasibility") < 0.48:
        action = "phase_or_pilot_before_scale"
    elif f(row, "ethical_quality") < 0.55:
        action = "ethical_review_before_implementation"
    else:
        action = "prototype_and_measure"

    redesign_rows.append(
        {
            "intervention_id": row["intervention_id"],
            "journey_id": row["journey_id"],
            "journey_name": journey_names.get(row["journey_id"], row["journey_id"]),
            "intervention_name": row["intervention_name"],
            "intervention_type": row["intervention_type"],
            "redesign_value_score": round(redesign_value, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "friction_reduction": row["friction_reduction"],
            "trust_gain": row["trust_gain"],
            "accessibility_gain": row["accessibility_gain"],
            "transition_gain": row["transition_gain"],
            "implementation_feasibility": row["implementation_feasibility"],
            "cost_efficiency": row["cost_efficiency"],
            "ethical_quality": row["ethical_quality"],
            "learning_value": row["learning_value"],
        }
    )

redesign_rows.sort(key=lambda item: item["redesign_value_score"], reverse=True)

write_csv(
    TABLES / "redesign_priority_scores.csv",
    redesign_rows,
    [
        "intervention_id",
        "journey_id",
        "journey_name",
        "intervention_name",
        "intervention_type",
        "redesign_value_score",
        "recommended_action",
        "source_review_action",
        "friction_reduction",
        "trust_gain",
        "accessibility_gain",
        "transition_gain",
        "implementation_feasibility",
        "cost_efficiency",
        "ethical_quality",
        "learning_value",
    ],
)

# ---------------------------------------------------------------------
# 10. Measurement and learning scoring
# ---------------------------------------------------------------------

learning_rows: list[dict[str, object]] = []

for row in learning:
    learning_score = (
        0.12 * f(row, "completion_tracking")
        + 0.12 * f(row, "dropoff_tracking")
        + 0.12 * f(row, "support_signal_tracking")
        + 0.12 * f(row, "trust_measurement")
        + 0.13 * f(row, "accessibility_monitoring")
        + 0.14 * f(row, "qualitative_review")
        + 0.13 * f(row, "revision_trigger_quality")
        + 0.12 * f(row, "decision_memory_quality")
    )

    if learning_score >= 0.72:
        action = "strong_experience_learning_system"
    elif f(row, "accessibility_monitoring") < 0.45:
        action = "add_accessibility_monitoring"
    elif f(row, "qualitative_review") < 0.45:
        action = "add_qualitative_review"
    elif f(row, "revision_trigger_quality") < 0.45:
        action = "define_revision_triggers"
    else:
        action = "strengthen_learning_loop"

    learning_rows.append(
        {
            "metric_id": row["metric_id"],
            "journey_id": row["journey_id"],
            "journey_name": journey_names.get(row["journey_id"], row["journey_id"]),
            "learning_system": row["learning_system"],
            "measurement_learning_score": round(learning_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "completion_tracking": row["completion_tracking"],
            "dropoff_tracking": row["dropoff_tracking"],
            "support_signal_tracking": row["support_signal_tracking"],
            "trust_measurement": row["trust_measurement"],
            "accessibility_monitoring": row["accessibility_monitoring"],
            "qualitative_review": row["qualitative_review"],
            "revision_trigger_quality": row["revision_trigger_quality"],
            "decision_memory_quality": row["decision_memory_quality"],
        }
    )

learning_rows.sort(key=lambda item: item["measurement_learning_score"], reverse=True)

write_csv(
    TABLES / "measurement_learning_scores.csv",
    learning_rows,
    [
        "metric_id",
        "journey_id",
        "journey_name",
        "learning_system",
        "measurement_learning_score",
        "recommended_action",
        "source_review_action",
        "completion_tracking",
        "dropoff_tracking",
        "support_signal_tracking",
        "trust_measurement",
        "accessibility_monitoring",
        "qualitative_review",
        "revision_trigger_quality",
        "decision_memory_quality",
    ],
)

# ---------------------------------------------------------------------
# 11. Strategist report
# ---------------------------------------------------------------------

top_journeys = journey_rows[:5]
high_redesign_need = sorted(journey_rows, key=lambda item: item["redesign_need_score"], reverse=True)[:5]
top_stage_friction = stage_rows[:6]
lowest_touchpoints = sorted(touchpoint_rows, key=lambda item: item["touchpoint_quality_score"])[:6]
top_transitions = transition_rows[:6]
access_risks = access_rows[:6]
trust_low = sorted(trust_rows, key=lambda item: item["trust_status_score"])[:6]
decision_risks = decision_rows[:6]
blueprint_risks = blueprint_rows[:6]
top_redesigns = redesign_rows[:6]
top_learning = learning_rows[:6]

report: list[str] = []
report.append("# Journey Mapping and Experience Design Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic evaluates journeys as lived sequences rather than isolated touchpoints. It assesses clarity, emotional confidence, accumulated friction, "
    "transition quality, accessibility, trust, completion support, backstage alignment, redesign priority, and experience-learning systems."
)

report.append("")
report.append("## Strongest journey profiles")
report.append("")
for item in top_journeys:
    report.append(
        f"- **{item['journey_id']} — {item['journey_name']}**: journey profile {item['journey_profile_score']}; "
        f"redesign need {item['redesign_need_score']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest redesign need")
report.append("")
for item in high_redesign_need:
    report.append(
        f"- **{item['journey_id']} — {item['journey_name']}**: redesign need {item['redesign_need_score']}; "
        f"diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest accumulated friction stages")
report.append("")
for item in top_stage_friction:
    report.append(
        f"- **{item['stage_id']} — {item['stage_name']}** in **{item['journey_name']}**: "
        f"friction {item['accumulated_friction_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Lowest-quality touchpoints")
report.append("")
for item in lowest_touchpoints:
    report.append(
        f"- **{item['touchpoint_id']} — {item['touchpoint_name']}**: "
        f"quality {item['touchpoint_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest transition risks")
report.append("")
for item in top_transitions:
    report.append(
        f"- **{item['transition_id']} — {item['from_stage']} → {item['to_stage']}**: "
        f"transition risk {item['transition_risk_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Accessibility and dignity risks")
report.append("")
for item in access_risks:
    report.append(
        f"- **{item['access_id']} — {item['access_issue']}**: "
        f"risk {item['accessibility_dignity_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Trust and status weaknesses")
report.append("")
for item in trust_low:
    report.append(
        f"- **{item['trust_id']} — {item['trust_issue']}**: "
        f"trust/status score {item['trust_status_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Decision pathway risks")
report.append("")
for item in decision_risks:
    report.append(
        f"- **{item['decision_id']} — {item['decision_point']}**: "
        f"decision pathway risk {item['decision_pathway_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Service blueprint dependency risks")
report.append("")
for item in blueprint_risks:
    report.append(
        f"- **{item['blueprint_id']} — {item['visible_experience']}** depends on **{item['backstage_dependency']}**: "
        f"blueprint risk {item['service_blueprint_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## High-value redesign candidates")
report.append("")
for item in top_redesigns:
    report.append(
        f"- **{item['intervention_id']} — {item['intervention_name']}**: "
        f"redesign value {item['redesign_value_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strong measurement and learning systems")
report.append("")
for item in top_learning:
    report.append(
        f"- **{item['metric_id']} — {item['learning_system']}**: "
        f"learning score {item['measurement_learning_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "Journey mapping strengthens strategic ideation when it reveals accumulated friction, transition failure, accessibility barriers, trust erosion, "
    "decision-pathway weaknesses, and backstage dependencies. Experience design creates strategic value when those insights change system sequence, "
    "handoffs, information architecture, recovery paths, measurement, and institutional learning."
)

(REPORTS / "journey_mapping_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_journeys": top_journeys,
    "high_redesign_need": high_redesign_need,
    "top_stage_friction": top_stage_friction,
    "lowest_touchpoints": lowest_touchpoints,
    "top_transitions": top_transitions,
    "access_risks": access_risks,
    "trust_low": trust_low,
    "decision_risks": decision_risks,
    "blueprint_risks": blueprint_risks,
    "top_redesigns": top_redesigns,
    "top_learning": top_learning,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced journey mapping diagnostics complete.")
print(f"Wrote: {TABLES / 'journey_profile_scores.csv'}")
print(f"Wrote: {TABLES / 'stage_friction_scores.csv'}")
print(f"Wrote: {TABLES / 'touchpoint_quality_scores.csv'}")
print(f"Wrote: {TABLES / 'transition_risk_scores.csv'}")
print(f"Wrote: {TABLES / 'accessibility_dignity_review.csv'}")
print(f"Wrote: {TABLES / 'trust_status_scores.csv'}")
print(f"Wrote: {TABLES / 'decision_pathway_scores.csv'}")
print(f"Wrote: {TABLES / 'service_blueprint_dependency_scores.csv'}")
print(f"Wrote: {TABLES / 'redesign_priority_scores.csv'}")
print(f"Wrote: {TABLES / 'measurement_learning_scores.csv'}")
print(f"Wrote: {REPORTS / 'journey_mapping_diagnostic_report.md'}")
