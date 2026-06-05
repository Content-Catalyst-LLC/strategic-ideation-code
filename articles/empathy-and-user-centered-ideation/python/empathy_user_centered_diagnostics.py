#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Empathy and User-Centered Ideation.

This dependency-light workflow uses only the Python standard library.

It produces:
- empathy profile scores
- stakeholder field scores
- observation quality scores
- journey friction scores
- unmet need scores
- preference-behavior gap scores
- reframing quality scores
- ethical empathy review
- systems empathy review
- decision linkage scores
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


contexts = read_csv(RAW / "empathy_contexts.csv")
stakeholders = read_csv(RAW / "stakeholder_field.csv")
observations = read_csv(RAW / "observations.csv")
journeys = read_csv(RAW / "journey_friction.csv")
needs = read_csv(RAW / "unmet_needs.csv")
gaps = read_csv(RAW / "preference_behavior.csv")
reframes = read_csv(RAW / "problem_reframes.csv")
ethics = read_csv(RAW / "ethical_empathy.csv")
systems = read_csv(RAW / "systems_empathy.csv")
decisions = read_csv(RAW / "decision_linkage.csv")

context_names = {row["context_id"]: row["context_name"] for row in contexts}
stakeholder_names = {row["stakeholder_id"]: row["stakeholder_group"] for row in stakeholders}

# ---------------------------------------------------------------------
# 1. Empathy profile scoring
# ---------------------------------------------------------------------

profile_rows: list[dict[str, object]] = []

for row in contexts:
    empathy_profile = (
        0.16 * f(row, "observational_depth")
        - 0.14 * f(row, "projection_risk")
        + 0.16 * f(row, "unmet_need_visibility")
        + 0.12 * f(row, "stakeholder_breadth")
        + 0.16 * f(row, "reframing_potential")
        + 0.10 * f(row, "ethical_review")
        + 0.10 * f(row, "systems_awareness")
        + 0.14 * f(row, "decision_linkage")
        + 0.10 * f(row, "institutional_memory")
    )

    superficiality_risk = (
        0.20 * f(row, "projection_risk")
        + 0.16 * (1 - f(row, "decision_linkage"))
        + 0.14 * (1 - f(row, "observational_depth"))
        + 0.12 * (1 - f(row, "unmet_need_visibility"))
        + 0.12 * (1 - f(row, "ethical_review"))
        + 0.10 * (1 - f(row, "systems_awareness"))
        + 0.08 * (1 - f(row, "stakeholder_breadth"))
        + 0.08 * (1 - f(row, "institutional_memory"))
    )

    if empathy_profile >= 0.64:
        diagnosis = "strong_user_centered_ideation_capability"
    elif superficiality_risk >= 0.62:
        diagnosis = "high_empathy_theater_or_projection_risk"
    elif f(row, "decision_linkage") < 0.42:
        diagnosis = "insight_not_linked_to_decisions"
    elif f(row, "observational_depth") < 0.42:
        diagnosis = "insufficient_observation"
    else:
        diagnosis = "developing_user_centered_capability"

    profile_rows.append(
        {
            "context_id": row["context_id"],
            "context_name": row["context_name"],
            "organization_type": row["organization_type"],
            "domain": row["domain"],
            "empathy_profile_score": round(empathy_profile, 4),
            "superficiality_risk": round(superficiality_risk, 4),
            "diagnosis": diagnosis,
            "observational_depth": row["observational_depth"],
            "projection_risk": row["projection_risk"],
            "unmet_need_visibility": row["unmet_need_visibility"],
            "stakeholder_breadth": row["stakeholder_breadth"],
            "reframing_potential": row["reframing_potential"],
            "ethical_review": row["ethical_review"],
            "systems_awareness": row["systems_awareness"],
            "decision_linkage": row["decision_linkage"],
            "institutional_memory": row["institutional_memory"],
            "description": row["description"],
        }
    )

profile_rows.sort(key=lambda item: item["empathy_profile_score"], reverse=True)

profile_fields = [
    "context_id",
    "context_name",
    "organization_type",
    "domain",
    "empathy_profile_score",
    "superficiality_risk",
    "diagnosis",
    "observational_depth",
    "projection_risk",
    "unmet_need_visibility",
    "stakeholder_breadth",
    "reframing_potential",
    "ethical_review",
    "systems_awareness",
    "decision_linkage",
    "institutional_memory",
    "description",
]

write_csv(TABLES / "empathy_profile_scores.csv", profile_rows, profile_fields)
write_csv(PROCESSED / "empathy_profile_scores.csv", profile_rows, profile_fields)

# ---------------------------------------------------------------------
# 2. Stakeholder field scoring
# ---------------------------------------------------------------------

stakeholder_rows: list[dict[str, object]] = []

for row in stakeholders:
    inclusion_priority = (
        0.14 * (1 - f(row, "visibility"))
        + 0.12 * f(row, "influence")
        + 0.18 * f(row, "vulnerability")
        + 0.16 * f(row, "knowledge_value")
        + 0.12 * (1 - f(row, "participation_access"))
        + 0.12 * f(row, "burden_risk")
        + 0.10 * f(row, "representation_gap")
        + 0.06 * f(row, "decision_relevance")
    )

    if inclusion_priority >= 0.58:
        action = "prioritize_for_inquiry"
    elif f(row, "representation_gap") >= 0.65:
        action = "close_representation_gap"
    elif f(row, "burden_risk") >= 0.70:
        action = "burden_review_required"
    else:
        action = "include_in_standard_mapping"

    stakeholder_rows.append(
        {
            "stakeholder_id": row["stakeholder_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "stakeholder_group": row["stakeholder_group"],
            "relationship_to_system": row["relationship_to_system"],
            "inclusion_priority_score": round(inclusion_priority, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "visibility": row["visibility"],
            "influence": row["influence"],
            "vulnerability": row["vulnerability"],
            "knowledge_value": row["knowledge_value"],
            "participation_access": row["participation_access"],
            "burden_risk": row["burden_risk"],
            "representation_gap": row["representation_gap"],
            "decision_relevance": row["decision_relevance"],
        }
    )

stakeholder_rows.sort(key=lambda item: item["inclusion_priority_score"], reverse=True)

write_csv(
    TABLES / "stakeholder_field_scores.csv",
    stakeholder_rows,
    [
        "stakeholder_id",
        "context_id",
        "context_name",
        "stakeholder_group",
        "relationship_to_system",
        "inclusion_priority_score",
        "recommended_action",
        "source_review_action",
        "visibility",
        "influence",
        "vulnerability",
        "knowledge_value",
        "participation_access",
        "burden_risk",
        "representation_gap",
        "decision_relevance",
    ],
)

# ---------------------------------------------------------------------
# 3. Observation quality scoring
# ---------------------------------------------------------------------

observation_rows: list[dict[str, object]] = []

for row in observations:
    observation_quality = (
        0.15 * f(row, "contextual_depth")
        + 0.15 * f(row, "behavioral_clarity")
        + 0.14 * f(row, "workaround_visibility")
        + 0.11 * f(row, "emotional_signal")
        + 0.10 * f(row, "accessibility_signal")
        + 0.11 * f(row, "trust_signal")
        + 0.12 * f(row, "interpretation_confidence")
        + 0.12 * f(row, "strategic_relevance")
    )

    if observation_quality >= 0.75:
        action = "strong_observation_evidence"
    elif f(row, "behavioral_clarity") < 0.45:
        action = "add_behavioral_observation"
    elif f(row, "workaround_visibility") >= 0.75:
        action = "treat_workaround_as_design_evidence"
    elif f(row, "interpretation_confidence") < 0.45:
        action = "strengthen_interpretation"
    else:
        action = "use_with_synthesis"

    observation_rows.append(
        {
            "observation_id": row["observation_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "stakeholder_id": row["stakeholder_id"],
            "stakeholder_group": stakeholder_names.get(row["stakeholder_id"], row["stakeholder_id"]),
            "observation_method": row["observation_method"],
            "observed_signal": row["observed_signal"],
            "observation_quality_score": round(observation_quality, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "contextual_depth": row["contextual_depth"],
            "behavioral_clarity": row["behavioral_clarity"],
            "workaround_visibility": row["workaround_visibility"],
            "emotional_signal": row["emotional_signal"],
            "accessibility_signal": row["accessibility_signal"],
            "trust_signal": row["trust_signal"],
            "interpretation_confidence": row["interpretation_confidence"],
            "strategic_relevance": row["strategic_relevance"],
        }
    )

observation_rows.sort(key=lambda item: item["observation_quality_score"], reverse=True)

write_csv(
    TABLES / "observation_quality_scores.csv",
    observation_rows,
    [
        "observation_id",
        "context_id",
        "context_name",
        "stakeholder_id",
        "stakeholder_group",
        "observation_method",
        "observed_signal",
        "observation_quality_score",
        "recommended_action",
        "source_review_action",
        "contextual_depth",
        "behavioral_clarity",
        "workaround_visibility",
        "emotional_signal",
        "accessibility_signal",
        "trust_signal",
        "interpretation_confidence",
        "strategic_relevance",
    ],
)

# ---------------------------------------------------------------------
# 4. Journey friction and accumulated burden
# ---------------------------------------------------------------------

journey_rows: list[dict[str, object]] = []

for row in journeys:
    burden_score = (
        0.13 * f(row, "time_cost")
        + 0.14 * f(row, "cognitive_load")
        + 0.14 * f(row, "emotional_cost")
        + 0.14 * f(row, "trust_risk")
        + 0.12 * f(row, "accessibility_burden")
        + 0.13 * f(row, "uncertainty")
        + 0.10 * f(row, "workaround_dependency")
        + 0.10 * f(row, "dropoff_risk")
    )

    if burden_score >= 0.70:
        action = "high_priority_burden_reduction"
    elif f(row, "trust_risk") >= 0.75:
        action = "trust_repair_required"
    elif f(row, "accessibility_burden") >= 0.75:
        action = "accessibility_review_required"
    elif f(row, "dropoff_risk") >= 0.70:
        action = "dropoff_intervention_required"
    else:
        action = "monitor_and_reduce_friction"

    journey_rows.append(
        {
            "journey_id": row["journey_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "stage_name": row["stage_name"],
            "stakeholder_group": row["stakeholder_group"],
            "accumulated_burden_score": round(burden_score, 4),
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

journey_rows.sort(key=lambda item: item["accumulated_burden_score"], reverse=True)

write_csv(
    TABLES / "journey_friction_scores.csv",
    journey_rows,
    [
        "journey_id",
        "context_id",
        "context_name",
        "stage_name",
        "stakeholder_group",
        "accumulated_burden_score",
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
# 5. Unmet need scoring
# ---------------------------------------------------------------------

need_rows: list[dict[str, object]] = []

for row in needs:
    need_priority = (
        0.10 * (1 - f(row, "visibility"))
        + 0.18 * f(row, "criticality")
        + 0.12 * f(row, "frequency")
        + 0.16 * f(row, "burden_intensity")
        + 0.12 * f(row, "evidence_strength")
        + 0.14 * f(row, "solution_fit_uncertainty")
        + 0.18 * f(row, "stakeholder_sensitivity")
    )

    if need_priority >= 0.72:
        action = "priority_unmet_need"
    elif f(row, "evidence_strength") < 0.40:
        action = "needs_more_evidence"
    elif f(row, "solution_fit_uncertainty") >= 0.70:
        action = "prototype_solution_fit"
    else:
        action = "include_in_ideation"

    need_rows.append(
        {
            "need_id": row["need_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "stakeholder_group": row["stakeholder_group"],
            "need_statement": row["need_statement"],
            "need_type": row["need_type"],
            "unmet_need_priority": round(need_priority, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "visibility": row["visibility"],
            "criticality": row["criticality"],
            "frequency": row["frequency"],
            "burden_intensity": row["burden_intensity"],
            "evidence_strength": row["evidence_strength"],
            "solution_fit_uncertainty": row["solution_fit_uncertainty"],
            "stakeholder_sensitivity": row["stakeholder_sensitivity"],
        }
    )

need_rows.sort(key=lambda item: item["unmet_need_priority"], reverse=True)

write_csv(
    TABLES / "unmet_need_scores.csv",
    need_rows,
    [
        "need_id",
        "context_id",
        "context_name",
        "stakeholder_group",
        "need_statement",
        "need_type",
        "unmet_need_priority",
        "recommended_action",
        "source_review_action",
        "visibility",
        "criticality",
        "frequency",
        "burden_intensity",
        "evidence_strength",
        "solution_fit_uncertainty",
        "stakeholder_sensitivity",
    ],
)

# ---------------------------------------------------------------------
# 6. Preference-behavior gap scoring
# ---------------------------------------------------------------------

gap_rows: list[dict[str, object]] = []

for row in gaps:
    gap_score = (
        0.18 * (1 - f(row, "alignment_score"))
        + 0.16 * f(row, "behavioral_evidence")
        + 0.14 * f(row, "interpretive_uncertainty")
        + 0.16 * f(row, "strategic_importance")
        + 0.10 * f(row, "preference_clarity")
    )

    if gap_score >= 0.60:
        action = "interpret_preference_behavior_gap"
    elif f(row, "behavioral_evidence") < 0.35:
        action = "collect_behavioral_evidence"
    else:
        action = "monitor_gap"

    gap_rows.append(
        {
            "gap_id": row["gap_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "stakeholder_group": row["stakeholder_group"],
            "stated_preference": row["stated_preference"],
            "observed_behavior": row["observed_behavior"],
            "preference_behavior_gap_score": round(gap_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "preference_clarity": row["preference_clarity"],
            "behavioral_evidence": row["behavioral_evidence"],
            "alignment_score": row["alignment_score"],
            "interpretive_uncertainty": row["interpretive_uncertainty"],
            "strategic_importance": row["strategic_importance"],
        }
    )

gap_rows.sort(key=lambda item: item["preference_behavior_gap_score"], reverse=True)

write_csv(
    TABLES / "preference_behavior_gap_scores.csv",
    gap_rows,
    [
        "gap_id",
        "context_id",
        "context_name",
        "stakeholder_group",
        "stated_preference",
        "observed_behavior",
        "preference_behavior_gap_score",
        "recommended_action",
        "source_review_action",
        "preference_clarity",
        "behavioral_evidence",
        "alignment_score",
        "interpretive_uncertainty",
        "strategic_importance",
    ],
)

# ---------------------------------------------------------------------
# 7. Reframing quality scores
# ---------------------------------------------------------------------

reframe_rows: list[dict[str, object]] = []

for row in reframes:
    reframing_quality = (
        0.14 * f(row, "inquiry_influence")
        + 0.14 * f(row, "projection_reduction")
        + 0.14 * f(row, "causal_depth")
        + 0.13 * f(row, "stakeholder_evidence")
        + 0.12 * f(row, "systems_context")
        + 0.11 * f(row, "ethical_awareness")
        + 0.12 * f(row, "decision_usefulness")
    )

    if reframing_quality >= 0.74:
        action = "strong_reframe_ready_for_prototyping"
    elif f(row, "projection_reduction") < 0.45:
        action = "reduce_projection_before_ideation"
    elif f(row, "decision_usefulness") < 0.45:
        action = "connect_reframe_to_decision"
    else:
        action = "strengthen_reframe"

    reframe_rows.append(
        {
            "reframe_id": row["reframe_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "initial_frame": row["initial_frame"],
            "reframed_problem": row["reframed_problem"],
            "evidence_basis": row["evidence_basis"],
            "reframing_quality_score": round(reframing_quality, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "inquiry_influence": row["inquiry_influence"],
            "projection_reduction": row["projection_reduction"],
            "causal_depth": row["causal_depth"],
            "stakeholder_evidence": row["stakeholder_evidence"],
            "systems_context": row["systems_context"],
            "ethical_awareness": row["ethical_awareness"],
            "decision_usefulness": row["decision_usefulness"],
        }
    )

reframe_rows.sort(key=lambda item: item["reframing_quality_score"], reverse=True)

write_csv(
    TABLES / "reframing_quality_scores.csv",
    reframe_rows,
    [
        "reframe_id",
        "context_id",
        "context_name",
        "initial_frame",
        "reframed_problem",
        "evidence_basis",
        "reframing_quality_score",
        "recommended_action",
        "source_review_action",
        "inquiry_influence",
        "projection_reduction",
        "causal_depth",
        "stakeholder_evidence",
        "systems_context",
        "ethical_awareness",
        "decision_usefulness",
    ],
)

# ---------------------------------------------------------------------
# 8. Ethical empathy review
# ---------------------------------------------------------------------

ethics_rows: list[dict[str, object]] = []

for row in ethics:
    ethical_score = (
        0.13 * f(row, "participation_quality")
        + 0.14 * f(row, "power_awareness")
        + 0.13 * f(row, "burden_visibility")
        + 0.11 * f(row, "consent_quality")
        + 0.12 * f(row, "representation_quality")
        + 0.12 * f(row, "redress_quality")
        + 0.13 * f(row, "decision_traceability")
        + 0.12 * f(row, "harm_monitoring")
    )

    ethical_risk = 1 - ethical_score

    if ethical_score >= 0.76:
        action = "strong_ethical_empathy_review"
    elif f(row, "power_awareness") < 0.45:
        action = "add_power_mapping"
    elif f(row, "decision_traceability") < 0.45:
        action = "trace_participation_to_decisions"
    elif f(row, "redress_quality") < 0.45:
        action = "add_redress_pathway"
    else:
        action = "strengthen_ethical_review"

    ethics_rows.append(
        {
            "ethics_id": row["ethics_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "ethical_issue": row["ethical_issue"],
            "ethical_empathy_score": round(ethical_score, 4),
            "ethical_empathy_risk": round(ethical_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "participation_quality": row["participation_quality"],
            "power_awareness": row["power_awareness"],
            "burden_visibility": row["burden_visibility"],
            "consent_quality": row["consent_quality"],
            "representation_quality": row["representation_quality"],
            "redress_quality": row["redress_quality"],
            "decision_traceability": row["decision_traceability"],
            "harm_monitoring": row["harm_monitoring"],
        }
    )

ethics_rows.sort(key=lambda item: item["ethical_empathy_risk"], reverse=True)

write_csv(
    TABLES / "ethical_empathy_review.csv",
    ethics_rows,
    [
        "ethics_id",
        "context_id",
        "context_name",
        "ethical_issue",
        "ethical_empathy_score",
        "ethical_empathy_risk",
        "recommended_action",
        "source_review_action",
        "participation_quality",
        "power_awareness",
        "burden_visibility",
        "consent_quality",
        "representation_quality",
        "redress_quality",
        "decision_traceability",
        "harm_monitoring",
    ],
)

# ---------------------------------------------------------------------
# 9. Systems empathy review
# ---------------------------------------------------------------------

system_rows: list[dict[str, object]] = []

for row in systems:
    system_risk = (
        0.14 * f(row, "feedback_risk")
        + 0.11 * f(row, "delay_risk")
        + 0.16 * f(row, "burden_shift_risk")
        + 0.14 * f(row, "incentive_misalignment")
        + 0.12 * f(row, "metric_gaming_risk")
        + 0.12 * f(row, "context_dependency")
        + 0.11 * f(row, "leverage_relevance")
        - 0.10 * f(row, "monitoring_quality")
    )

    if system_risk >= 0.60:
        action = "systems_empathy_review_required"
    elif f(row, "burden_shift_risk") >= 0.75:
        action = "burden_shift_review_required"
    elif f(row, "monitoring_quality") < 0.45:
        action = "improve_monitoring"
    else:
        action = "monitor_system_effects"

    system_rows.append(
        {
            "system_id": row["system_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "system_issue": row["system_issue"],
            "systems_empathy_risk": round(system_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "feedback_risk": row["feedback_risk"],
            "delay_risk": row["delay_risk"],
            "burden_shift_risk": row["burden_shift_risk"],
            "incentive_misalignment": row["incentive_misalignment"],
            "metric_gaming_risk": row["metric_gaming_risk"],
            "context_dependency": row["context_dependency"],
            "leverage_relevance": row["leverage_relevance"],
            "monitoring_quality": row["monitoring_quality"],
        }
    )

system_rows.sort(key=lambda item: item["systems_empathy_risk"], reverse=True)

write_csv(
    TABLES / "systems_empathy_review.csv",
    system_rows,
    [
        "system_id",
        "context_id",
        "context_name",
        "system_issue",
        "systems_empathy_risk",
        "recommended_action",
        "source_review_action",
        "feedback_risk",
        "delay_risk",
        "burden_shift_risk",
        "incentive_misalignment",
        "metric_gaming_risk",
        "context_dependency",
        "leverage_relevance",
        "monitoring_quality",
    ],
)

# ---------------------------------------------------------------------
# 10. Decision linkage scores
# ---------------------------------------------------------------------

decision_rows: list[dict[str, object]] = []

for row in decisions:
    decision_score = (
        0.12 * f(row, "artifact_quality")
        + 0.14 * f(row, "evidence_quality")
        + 0.15 * f(row, "decision_relevance")
        + 0.15 * f(row, "authority_connection")
        + 0.11 * f(row, "resource_connection")
        + 0.12 * f(row, "revision_trigger_quality")
        + 0.10 * f(row, "learning_memory_quality")
        + 0.11 * f(row, "implementation_path_quality")
    )

    if decision_score >= 0.72:
        action = "strong_insight_to_decision_linkage"
    elif f(row, "authority_connection") < 0.45:
        action = "connect_to_decision_authority"
    elif f(row, "resource_connection") < 0.45:
        action = "connect_to_resource_decisions"
    elif f(row, "revision_trigger_quality") < 0.45:
        action = "define_revision_triggers"
    else:
        action = "strengthen_decision_linkage"

    decision_rows.append(
        {
            "decision_id": row["decision_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "insight_artifact": row["insight_artifact"],
            "decision_type": row["decision_type"],
            "decision_linkage_score": round(decision_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "artifact_quality": row["artifact_quality"],
            "evidence_quality": row["evidence_quality"],
            "decision_relevance": row["decision_relevance"],
            "authority_connection": row["authority_connection"],
            "resource_connection": row["resource_connection"],
            "revision_trigger_quality": row["revision_trigger_quality"],
            "learning_memory_quality": row["learning_memory_quality"],
            "implementation_path_quality": row["implementation_path_quality"],
        }
    )

decision_rows.sort(key=lambda item: item["decision_linkage_score"], reverse=True)

write_csv(
    TABLES / "decision_linkage_scores.csv",
    decision_rows,
    [
        "decision_id",
        "context_id",
        "context_name",
        "insight_artifact",
        "decision_type",
        "decision_linkage_score",
        "recommended_action",
        "source_review_action",
        "artifact_quality",
        "evidence_quality",
        "decision_relevance",
        "authority_connection",
        "resource_connection",
        "revision_trigger_quality",
        "learning_memory_quality",
        "implementation_path_quality",
    ],
)

# ---------------------------------------------------------------------
# 11. Strategist report
# ---------------------------------------------------------------------

top_profiles = profile_rows[:5]
high_superficiality = sorted(profile_rows, key=lambda item: item["superficiality_risk"], reverse=True)[:5]
top_stakeholders = stakeholder_rows[:6]
top_observations = observation_rows[:6]
top_journeys = journey_rows[:6]
top_needs = need_rows[:6]
top_gaps = gap_rows[:6]
top_reframes = reframe_rows[:6]
ethical_risks = ethics_rows[:6]
system_risks = system_rows[:6]
top_decisions = decision_rows[:6]

report: list[str] = []
report.append("# Empathy and User-Centered Ideation Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic evaluates empathy as disciplined strategic inquiry. It examines observation depth, projection risk, unmet need, stakeholder breadth, "
    "journey friction, preference-behavior gaps, reframing quality, ethical legitimacy, systems effects, decision linkage, and institutional learning."
)

report.append("")
report.append("## Strongest user-centered ideation profiles")
report.append("")
for item in top_profiles:
    report.append(
        f"- **{item['context_id']} — {item['context_name']}**: empathy profile {item['empathy_profile_score']}; "
        f"superficiality risk {item['superficiality_risk']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest superficiality or projection risks")
report.append("")
for item in high_superficiality:
    report.append(
        f"- **{item['context_id']} — {item['context_name']}**: superficiality risk {item['superficiality_risk']}; "
        f"diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Stakeholders to prioritize")
report.append("")
for item in top_stakeholders:
    report.append(
        f"- **{item['stakeholder_id']} — {item['stakeholder_group']}** in **{item['context_name']}**: "
        f"inclusion priority {item['inclusion_priority_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strongest observation evidence")
report.append("")
for item in top_observations:
    report.append(
        f"- **{item['observation_id']} — {item['observed_signal']}**: "
        f"observation quality {item['observation_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest journey friction and accumulated burden")
report.append("")
for item in top_journeys:
    report.append(
        f"- **{item['journey_id']} — {item['stage_name']}** for **{item['stakeholder_group']}**: "
        f"burden score {item['accumulated_burden_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Priority unmet needs")
report.append("")
for item in top_needs:
    report.append(
        f"- **{item['need_id']} — {item['need_statement']}**: "
        f"priority {item['unmet_need_priority']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Preference-behavior gaps")
report.append("")
for item in top_gaps:
    report.append(
        f"- **{item['gap_id']} — stated:** {item['stated_preference']} | **observed:** {item['observed_behavior']}. "
        f"Gap score {item['preference_behavior_gap_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strong reframes")
report.append("")
for item in top_reframes:
    report.append(
        f"- **{item['reframe_id']} — {item['reframed_problem']}**: "
        f"reframing quality {item['reframing_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Ethical empathy risks")
report.append("")
for item in ethical_risks:
    report.append(
        f"- **{item['ethics_id']} — {item['ethical_issue']}**: "
        f"ethical risk {item['ethical_empathy_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Systems empathy risks")
report.append("")
for item in system_risks:
    report.append(
        f"- **{item['system_id']} — {item['system_issue']}**: "
        f"systems risk {item['systems_empathy_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strong decision linkage")
report.append("")
for item in top_decisions:
    report.append(
        f"- **{item['decision_id']} — {item['insight_artifact']}**: "
        f"decision linkage {item['decision_linkage_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "Empathy strengthens strategic ideation when it reduces projection, reveals hidden burden, includes the right stakeholders, changes the problem frame, "
    "tests behavior rather than only preference, accounts for systems effects, addresses power and ethics, and links evidence to real decisions."
)

(REPORTS / "empathy_user_centered_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_profiles": top_profiles,
    "high_superficiality": high_superficiality,
    "top_stakeholders": top_stakeholders,
    "top_observations": top_observations,
    "top_journeys": top_journeys,
    "top_needs": top_needs,
    "top_gaps": top_gaps,
    "top_reframes": top_reframes,
    "ethical_risks": ethical_risks,
    "system_risks": system_risks,
    "top_decisions": top_decisions,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced empathy and user-centered ideation diagnostics complete.")
print(f"Wrote: {TABLES / 'empathy_profile_scores.csv'}")
print(f"Wrote: {TABLES / 'stakeholder_field_scores.csv'}")
print(f"Wrote: {TABLES / 'observation_quality_scores.csv'}")
print(f"Wrote: {TABLES / 'journey_friction_scores.csv'}")
print(f"Wrote: {TABLES / 'unmet_need_scores.csv'}")
print(f"Wrote: {TABLES / 'preference_behavior_gap_scores.csv'}")
print(f"Wrote: {TABLES / 'reframing_quality_scores.csv'}")
print(f"Wrote: {TABLES / 'ethical_empathy_review.csv'}")
print(f"Wrote: {TABLES / 'systems_empathy_review.csv'}")
print(f"Wrote: {TABLES / 'decision_linkage_scores.csv'}")
print(f"Wrote: {REPORTS / 'empathy_user_centered_diagnostic_report.md'}")
