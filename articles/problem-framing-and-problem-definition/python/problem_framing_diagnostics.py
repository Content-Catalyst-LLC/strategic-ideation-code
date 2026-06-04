#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for problem framing and problem definition.

This dependency-light workflow uses only the Python standard library.

It produces:
- problem-framing quality scores
- frame-origin and institutional lock-in review
- boundary quality review
- stakeholder frame review
- causal-depth review
- assumption transparency review
- alternative-frame comparison
- reframing trigger review
- intervention recommendations
- a markdown strategist diagnostic report

The workflow is designed for strategy teams that need to determine whether
they are defining the right problem before generating solutions.
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


frames = read_csv(RAW / "problem_frames.csv")
origins = read_csv(RAW / "frame_origins.csv")
boundaries = read_csv(RAW / "boundary_audit.csv")
stakeholders = read_csv(RAW / "stakeholder_frames.csv")
causal_models = read_csv(RAW / "causal_models.csv")
assumptions = read_csv(RAW / "assumption_audit.csv")
alternatives = read_csv(RAW / "alternative_frames.csv")
triggers = read_csv(RAW / "reframing_triggers.csv")
interventions = read_csv(RAW / "intervention_library.csv")

frame_names = {row["frame_id"]: row["frame_name"] for row in frames}

# ---------------------------------------------------------------------
# 1. Problem-framing quality scores
# ---------------------------------------------------------------------

frame_rows: list[dict[str, object]] = []

for row in frames:
    framing_score = (
        0.16 * f(row, "boundary_breadth")
        + 0.15 * f(row, "stakeholder_inclusion")
        + 0.15 * f(row, "systems_awareness")
        + 0.16 * f(row, "causal_depth")
        + 0.12 * f(row, "assumption_clarity")
        + 0.13 * f(row, "reframing_capacity")
        + 0.11 * f(row, "actionability")
        - 0.10 * f(row, "institutional_lock_in_risk")
        - 0.08 * f(row, "political_convenience_risk")
    )

    boundary_gap = max(0.0, 0.70 - f(row, "boundary_breadth"))
    stakeholder_gap = max(0.0, 0.70 - f(row, "stakeholder_inclusion"))
    causal_gap = max(0.0, 0.70 - f(row, "causal_depth"))
    assumption_gap = max(0.0, 0.65 - f(row, "assumption_clarity"))

    symptom_framing_risk = (
        (1.0 - f(row, "causal_depth")) * 0.30
        + (1.0 - f(row, "systems_awareness")) * 0.25
        + boundary_gap * 0.20
        + f(row, "institutional_lock_in_risk") * 0.15
        + f(row, "political_convenience_risk") * 0.10
    )

    if framing_score >= 0.68:
        diagnosis = "strong_problem_framing_capacity"
    elif symptom_framing_risk >= 0.62:
        diagnosis = "symptom_or_convenience_frame_risk"
    elif boundary_gap >= 0.30:
        diagnosis = "boundary_myopia_risk"
    elif stakeholder_gap >= 0.30:
        diagnosis = "stakeholder_blindness_risk"
    elif causal_gap >= 0.30:
        diagnosis = "causal_depth_gap"
    elif f(row, "institutional_lock_in_risk") >= 0.70:
        diagnosis = "institutional_lock_in_risk"
    else:
        diagnosis = "develop_with_frame_comparison"

    frame_rows.append(
        {
            "frame_id": row["frame_id"],
            "frame_name": row["frame_name"],
            "frame_type": row["frame_type"],
            "domain": row["domain"],
            "problem_framing_score": round(framing_score, 4),
            "symptom_framing_risk": round(symptom_framing_risk, 4),
            "boundary_gap": round(boundary_gap, 4),
            "stakeholder_gap": round(stakeholder_gap, 4),
            "causal_gap": round(causal_gap, 4),
            "assumption_gap": round(assumption_gap, 4),
            "diagnosis": diagnosis,
            "boundary_breadth": row["boundary_breadth"],
            "stakeholder_inclusion": row["stakeholder_inclusion"],
            "systems_awareness": row["systems_awareness"],
            "causal_depth": row["causal_depth"],
            "assumption_clarity": row["assumption_clarity"],
            "reframing_capacity": row["reframing_capacity"],
            "actionability": row["actionability"],
            "institutional_lock_in_risk": row["institutional_lock_in_risk"],
            "political_convenience_risk": row["political_convenience_risk"],
            "description": row["description"],
        }
    )

frame_rows.sort(key=lambda item: item["problem_framing_score"], reverse=True)

frame_fields = [
    "frame_id",
    "frame_name",
    "frame_type",
    "domain",
    "problem_framing_score",
    "symptom_framing_risk",
    "boundary_gap",
    "stakeholder_gap",
    "causal_gap",
    "assumption_gap",
    "diagnosis",
    "boundary_breadth",
    "stakeholder_inclusion",
    "systems_awareness",
    "causal_depth",
    "assumption_clarity",
    "reframing_capacity",
    "actionability",
    "institutional_lock_in_risk",
    "political_convenience_risk",
    "description",
]

write_csv(TABLES / "problem_framing_scores.csv", frame_rows, frame_fields)
write_csv(PROCESSED / "problem_framing_scores.csv", frame_rows, frame_fields)

# ---------------------------------------------------------------------
# 2. Frame-origin review
# ---------------------------------------------------------------------

origin_rows: list[dict[str, object]] = []

for row in origins:
    origin_quality = (
        0.16 * f(row, "stakeholder_evidence_strength")
        + 0.16 * f(row, "frontline_evidence_strength")
        + 0.16 * f(row, "diagnostic_independence")
        + 0.10 * f(row, "political_safety")
        - 0.14 * f(row, "authority_weight")
        - 0.12 * f(row, "metric_dependency")
        - 0.12 * f(row, "legacy_dependency")
        - 0.10 * f(row, "origin_risk")
    )

    lock_in_risk = (
        0.24 * f(row, "authority_weight")
        + 0.24 * f(row, "metric_dependency")
        + 0.24 * f(row, "legacy_dependency")
        + 0.18 * f(row, "origin_risk")
        - 0.16 * f(row, "diagnostic_independence")
    )

    if lock_in_risk >= 0.55:
        action = "challenge_frame_origin_before_commitment"
    elif f(row, "stakeholder_evidence_strength") < 0.45:
        action = "add_stakeholder_evidence"
    elif origin_quality >= 0.20:
        action = "origin_quality_manageable"
    else:
        action = "strengthen_diagnostic_independence"

    origin_rows.append(
        {
            "origin_id": row["origin_id"],
            "frame_id": row["frame_id"],
            "frame_name": frame_names.get(row["frame_id"], row["frame_id"]),
            "origin_source": row["origin_source"],
            "origin_quality_score": round(origin_quality, 4),
            "lock_in_risk": round(lock_in_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "authority_weight": row["authority_weight"],
            "metric_dependency": row["metric_dependency"],
            "legacy_dependency": row["legacy_dependency"],
            "stakeholder_evidence_strength": row["stakeholder_evidence_strength"],
            "frontline_evidence_strength": row["frontline_evidence_strength"],
            "political_safety": row["political_safety"],
            "diagnostic_independence": row["diagnostic_independence"],
            "origin_risk": row["origin_risk"],
        }
    )

origin_rows.sort(key=lambda item: item["lock_in_risk"], reverse=True)

write_csv(
    TABLES / "frame_origin_review.csv",
    origin_rows,
    [
        "origin_id",
        "frame_id",
        "frame_name",
        "origin_source",
        "origin_quality_score",
        "lock_in_risk",
        "recommended_action",
        "source_review_action",
        "authority_weight",
        "metric_dependency",
        "legacy_dependency",
        "stakeholder_evidence_strength",
        "frontline_evidence_strength",
        "political_safety",
        "diagnostic_independence",
        "origin_risk",
    ],
)

# ---------------------------------------------------------------------
# 3. Boundary quality review
# ---------------------------------------------------------------------

boundary_rows: list[dict[str, object]] = []

for row in boundaries:
    boundary_quality = (
        0.16 * f(row, "stakeholder_visibility")
        + 0.15 * f(row, "downstream_effect_visibility")
        + 0.14 * f(row, "externality_visibility")
        + 0.14 * f(row, "implementation_visibility")
        + 0.13 * f(row, "time_horizon_quality")
        + 0.14 * f(row, "hidden_dependency_visibility")
        - 0.12 * f(row, "boundary_risk")
        - 0.08 * f(row, "revision_need")
    )

    if f(row, "boundary_risk") >= 0.70:
        action = "expand_boundary_before_ideation"
    elif f(row, "stakeholder_visibility") < 0.45:
        action = "add_stakeholder_boundary_review"
    elif f(row, "time_horizon_quality") < 0.45:
        action = "extend_time_horizon_review"
    elif boundary_quality >= 0.50:
        action = "boundary_usable_with_review"
    else:
        action = "strengthen_boundary_definition"

    boundary_rows.append(
        {
            "boundary_id": row["boundary_id"],
            "frame_id": row["frame_id"],
            "frame_name": frame_names.get(row["frame_id"], row["frame_id"]),
            "boundary_name": row["boundary_name"],
            "boundary_type": row["boundary_type"],
            "boundary_quality_score": round(boundary_quality, 4),
            "recommended_action": action,
            "source_recommendation": row["review_recommendation"],
            "stakeholder_visibility": row["stakeholder_visibility"],
            "downstream_effect_visibility": row["downstream_effect_visibility"],
            "externality_visibility": row["externality_visibility"],
            "implementation_visibility": row["implementation_visibility"],
            "time_horizon_quality": row["time_horizon_quality"],
            "hidden_dependency_visibility": row["hidden_dependency_visibility"],
            "boundary_risk": row["boundary_risk"],
            "revision_need": row["revision_need"],
        }
    )

boundary_rows.sort(key=lambda item: item["boundary_quality_score"], reverse=True)

write_csv(
    TABLES / "boundary_quality_review.csv",
    boundary_rows,
    [
        "boundary_id",
        "frame_id",
        "frame_name",
        "boundary_name",
        "boundary_type",
        "boundary_quality_score",
        "recommended_action",
        "source_recommendation",
        "stakeholder_visibility",
        "downstream_effect_visibility",
        "externality_visibility",
        "implementation_visibility",
        "time_horizon_quality",
        "hidden_dependency_visibility",
        "boundary_risk",
        "revision_need",
    ],
)

# ---------------------------------------------------------------------
# 4. Stakeholder frame review
# ---------------------------------------------------------------------

stakeholder_rows: list[dict[str, object]] = []

for row in stakeholders:
    stakeholder_quality = (
        0.12 * f(row, "problem_definition_alignment")
        + 0.16 * f(row, "burden_visibility")
        + 0.14 * f(row, "trust_sensitivity")
        + 0.14 * f(row, "agency_visibility")
        + 0.16 * f(row, "legitimacy_contribution")
        + 0.12 * f(row, "conflict_visibility")
        + 0.14 * f(row, "participation_quality")
        - 0.12 * f(row, "hidden_harm_risk")
    )

    if f(row, "hidden_harm_risk") >= 0.60:
        action = "hidden_harm_review_required"
    elif f(row, "burden_visibility") < 0.45:
        action = "add_burden_mapping"
    elif f(row, "participation_quality") < 0.45:
        action = "add_participatory_frame_review"
    elif stakeholder_quality >= 0.55:
        action = "stakeholder_frame_quality_manageable"
    else:
        action = "strengthen_stakeholder_frame"

    stakeholder_rows.append(
        {
            "stakeholder_frame_id": row["stakeholder_frame_id"],
            "frame_id": row["frame_id"],
            "frame_name": frame_names.get(row["frame_id"], row["frame_id"]),
            "stakeholder_group": row["stakeholder_group"],
            "stakeholder_frame_quality_score": round(stakeholder_quality, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "problem_definition_alignment": row["problem_definition_alignment"],
            "burden_visibility": row["burden_visibility"],
            "trust_sensitivity": row["trust_sensitivity"],
            "agency_visibility": row["agency_visibility"],
            "legitimacy_contribution": row["legitimacy_contribution"],
            "conflict_visibility": row["conflict_visibility"],
            "participation_quality": row["participation_quality"],
            "hidden_harm_risk": row["hidden_harm_risk"],
        }
    )

stakeholder_rows.sort(key=lambda item: item["stakeholder_frame_quality_score"], reverse=True)

write_csv(
    TABLES / "stakeholder_frame_review.csv",
    stakeholder_rows,
    [
        "stakeholder_frame_id",
        "frame_id",
        "frame_name",
        "stakeholder_group",
        "stakeholder_frame_quality_score",
        "recommended_action",
        "source_review_action",
        "problem_definition_alignment",
        "burden_visibility",
        "trust_sensitivity",
        "agency_visibility",
        "legitimacy_contribution",
        "conflict_visibility",
        "participation_quality",
        "hidden_harm_risk",
    ],
)

# ---------------------------------------------------------------------
# 5. Causal-depth review
# ---------------------------------------------------------------------

causal_rows: list[dict[str, object]] = []

for row in causal_models:
    causal_quality = (
        0.18 * f(row, "causal_depth")
        + 0.16 * f(row, "mechanism_clarity")
        + 0.16 * f(row, "feedback_awareness")
        + 0.14 * f(row, "incentive_awareness")
        + 0.12 * f(row, "delay_awareness")
        + 0.12 * f(row, "evidence_strength")
        + 0.12 * f(row, "alternative_cause_review")
        - 0.14 * f(row, "linear_oversimplification_risk")
    )

    if f(row, "linear_oversimplification_risk") >= 0.70:
        action = "replace_linear_story_with_system_review"
    elif f(row, "mechanism_clarity") < 0.45:
        action = "clarify_mechanism_before_ideation"
    elif f(row, "alternative_cause_review") < 0.45:
        action = "test_rival_causal_stories"
    elif causal_quality >= 0.55:
        action = "causal_model_ready_for_testing"
    else:
        action = "strengthen_causal_depth"

    causal_rows.append(
        {
            "causal_id": row["causal_id"],
            "frame_id": row["frame_id"],
            "frame_name": frame_names.get(row["frame_id"], row["frame_id"]),
            "causal_story": row["causal_story"],
            "causal_quality_score": round(causal_quality, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "causal_depth": row["causal_depth"],
            "mechanism_clarity": row["mechanism_clarity"],
            "feedback_awareness": row["feedback_awareness"],
            "incentive_awareness": row["incentive_awareness"],
            "delay_awareness": row["delay_awareness"],
            "evidence_strength": row["evidence_strength"],
            "alternative_cause_review": row["alternative_cause_review"],
            "linear_oversimplification_risk": row["linear_oversimplification_risk"],
        }
    )

causal_rows.sort(key=lambda item: item["causal_quality_score"], reverse=True)

write_csv(
    TABLES / "causal_depth_review.csv",
    causal_rows,
    [
        "causal_id",
        "frame_id",
        "frame_name",
        "causal_story",
        "causal_quality_score",
        "recommended_action",
        "source_review_action",
        "causal_depth",
        "mechanism_clarity",
        "feedback_awareness",
        "incentive_awareness",
        "delay_awareness",
        "evidence_strength",
        "alternative_cause_review",
        "linear_oversimplification_risk",
    ],
)

# ---------------------------------------------------------------------
# 6. Assumption transparency review
# ---------------------------------------------------------------------

assumption_rows: list[dict[str, object]] = []

for row in assumptions:
    assumption_priority = (
        0.18 * f(row, "importance")
        + 0.16 * f(row, "uncertainty")
        + 0.16 * f(row, "stakeholder_sensitivity")
        + 0.14 * f(row, "assumption_risk")
        - 0.12 * f(row, "visibility")
        - 0.10 * f(row, "testability")
        - 0.10 * f(row, "disconfirmation_quality")
        - 0.08 * f(row, "reversibility")
    )

    assumption_readiness = (
        0.18 * f(row, "visibility")
        + 0.18 * f(row, "testability")
        + 0.18 * f(row, "disconfirmation_quality")
        + 0.12 * f(row, "reversibility")
        - 0.14 * f(row, "assumption_risk")
    )

    if assumption_priority >= 0.30:
        action = "priority_assumption_test_required"
    elif f(row, "visibility") < 0.45:
        action = "make_assumption_explicit"
    elif f(row, "disconfirmation_quality") < 0.45:
        action = "define_disconfirming_evidence"
    else:
        action = "monitor_assumption"

    assumption_rows.append(
        {
            "assumption_id": row["assumption_id"],
            "frame_id": row["frame_id"],
            "frame_name": frame_names.get(row["frame_id"], row["frame_id"]),
            "assumption_text": row["assumption_text"],
            "assumption_type": row["assumption_type"],
            "assumption_priority_score": round(assumption_priority, 4),
            "assumption_readiness_score": round(assumption_readiness, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "importance": row["importance"],
            "uncertainty": row["uncertainty"],
            "visibility": row["visibility"],
            "testability": row["testability"],
            "disconfirmation_quality": row["disconfirmation_quality"],
            "stakeholder_sensitivity": row["stakeholder_sensitivity"],
            "reversibility": row["reversibility"],
            "assumption_risk": row["assumption_risk"],
        }
    )

assumption_rows.sort(key=lambda item: item["assumption_priority_score"], reverse=True)

write_csv(
    TABLES / "assumption_transparency_review.csv",
    assumption_rows,
    [
        "assumption_id",
        "frame_id",
        "frame_name",
        "assumption_text",
        "assumption_type",
        "assumption_priority_score",
        "assumption_readiness_score",
        "recommended_action",
        "source_review_action",
        "importance",
        "uncertainty",
        "visibility",
        "testability",
        "disconfirmation_quality",
        "stakeholder_sensitivity",
        "reversibility",
        "assumption_risk",
    ],
)

# ---------------------------------------------------------------------
# 7. Alternative-frame comparison
# ---------------------------------------------------------------------

alternative_rows: list[dict[str, object]] = []

for row in alternatives:
    comparison_value = (
        0.16 * f(row, "novelty_gain")
        + 0.18 * f(row, "causal_gain")
        + 0.16 * f(row, "stakeholder_gain")
        + 0.16 * f(row, "boundary_gain")
        + 0.12 * f(row, "actionability_gain")
        - 0.10 * f(row, "evidence_need")
        - 0.08 * f(row, "risk_of_confusion")
    )

    if comparison_value >= 0.48:
        action = "high_value_reframing_candidate"
    elif f(row, "risk_of_confusion") >= 0.50:
        action = "facilitated_comparison_needed"
    else:
        action = "supporting_reframing_candidate"

    alternative_rows.append(
        {
            "comparison_id": row["comparison_id"],
            "primary_frame_id": row["primary_frame_id"],
            "primary_frame_name": frame_names.get(row["primary_frame_id"], row["primary_frame_id"]),
            "rival_frame_id": row["rival_frame_id"],
            "rival_frame_name": frame_names.get(row["rival_frame_id"], row["rival_frame_id"]),
            "comparison_focus": row["comparison_focus"],
            "comparison_value_score": round(comparison_value, 4),
            "recommended_action": action,
            "source_recommendation": row["recommendation"],
            "novelty_gain": row["novelty_gain"],
            "causal_gain": row["causal_gain"],
            "stakeholder_gain": row["stakeholder_gain"],
            "boundary_gain": row["boundary_gain"],
            "actionability_gain": row["actionability_gain"],
            "evidence_need": row["evidence_need"],
            "risk_of_confusion": row["risk_of_confusion"],
        }
    )

alternative_rows.sort(key=lambda item: item["comparison_value_score"], reverse=True)

write_csv(
    TABLES / "alternative_frame_review.csv",
    alternative_rows,
    [
        "comparison_id",
        "primary_frame_id",
        "primary_frame_name",
        "rival_frame_id",
        "rival_frame_name",
        "comparison_focus",
        "comparison_value_score",
        "recommended_action",
        "source_recommendation",
        "novelty_gain",
        "causal_gain",
        "stakeholder_gain",
        "boundary_gain",
        "actionability_gain",
        "evidence_need",
        "risk_of_confusion",
    ],
)

# ---------------------------------------------------------------------
# 8. Reframing trigger review
# ---------------------------------------------------------------------

trigger_rows: list[dict[str, object]] = []

for row in triggers:
    trigger_strength = (
        0.16 * f(row, "evidence_threshold")
        + 0.15 * f(row, "stakeholder_signal_strength")
        + 0.15 * f(row, "implementation_signal_strength")
        + 0.14 * f(row, "systems_signal_strength")
        + 0.12 * f(row, "urgency")
        + 0.10 * f(row, "reversibility")
        + 0.10 * f(row, "decision_memory_need")
        + 0.12 * f(row, "trigger_quality")
    )

    if trigger_strength >= 0.72:
        action = "high_priority_reframing_trigger"
    elif f(row, "decision_memory_need") >= 0.75:
        action = "decision_memory_required"
    elif f(row, "stakeholder_signal_strength") >= 0.80:
        action = "stakeholder_signal_review_required"
    else:
        action = "monitor_trigger"

    trigger_rows.append(
        {
            "trigger_id": row["trigger_id"],
            "frame_id": row["frame_id"],
            "frame_name": frame_names.get(row["frame_id"], row["frame_id"]),
            "trigger_name": row["trigger_name"],
            "trigger_type": row["trigger_type"],
            "trigger_strength_score": round(trigger_strength, 4),
            "recommended_action": action,
            "action_if_triggered": row["action_if_triggered"],
            "evidence_threshold": row["evidence_threshold"],
            "stakeholder_signal_strength": row["stakeholder_signal_strength"],
            "implementation_signal_strength": row["implementation_signal_strength"],
            "systems_signal_strength": row["systems_signal_strength"],
            "urgency": row["urgency"],
            "reversibility": row["reversibility"],
            "decision_memory_need": row["decision_memory_need"],
            "trigger_quality": row["trigger_quality"],
        }
    )

trigger_rows.sort(key=lambda item: item["trigger_strength_score"], reverse=True)

write_csv(
    TABLES / "reframing_trigger_review.csv",
    trigger_rows,
    [
        "trigger_id",
        "frame_id",
        "frame_name",
        "trigger_name",
        "trigger_type",
        "trigger_strength_score",
        "recommended_action",
        "action_if_triggered",
        "evidence_threshold",
        "stakeholder_signal_strength",
        "implementation_signal_strength",
        "systems_signal_strength",
        "urgency",
        "reversibility",
        "decision_memory_need",
        "trigger_quality",
    ],
)

# ---------------------------------------------------------------------
# 9. Intervention recommendations
# ---------------------------------------------------------------------

intervention_rows: list[dict[str, object]] = []

for row in interventions:
    intervention_value = (
        0.14 * f(row, "boundary_gain")
        + 0.16 * f(row, "causal_depth_gain")
        + 0.16 * f(row, "stakeholder_gain")
        + 0.14 * f(row, "assumption_clarity_gain")
        + 0.16 * f(row, "reframing_capacity_gain")
        + 0.14 * f(row, "decision_memory_gain")
        - 0.10 * f(row, "process_cost")
        - 0.08 * f(row, "implementation_complexity")
        - 0.08 * f(row, "political_safety_need")
    )

    if f(row, "political_safety_need") >= 0.44:
        action = "requires_leadership_protection"
    elif intervention_value >= 0.52:
        action = "high_value_framing_intervention"
    else:
        action = "supporting_intervention"

    intervention_rows.append(
        {
            "intervention_id": row["intervention_id"],
            "intervention_name": row["intervention_name"],
            "target_framing_risk": row["target_framing_risk"],
            "intervention_value_score": round(intervention_value, 4),
            "recommended_action": action,
            "process_cost": row["process_cost"],
            "implementation_complexity": row["implementation_complexity"],
            "boundary_gain": row["boundary_gain"],
            "causal_depth_gain": row["causal_depth_gain"],
            "stakeholder_gain": row["stakeholder_gain"],
            "assumption_clarity_gain": row["assumption_clarity_gain"],
            "reframing_capacity_gain": row["reframing_capacity_gain"],
            "decision_memory_gain": row["decision_memory_gain"],
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
        "target_framing_risk",
        "intervention_value_score",
        "recommended_action",
        "process_cost",
        "implementation_complexity",
        "boundary_gain",
        "causal_depth_gain",
        "stakeholder_gain",
        "assumption_clarity_gain",
        "reframing_capacity_gain",
        "decision_memory_gain",
        "political_safety_need",
    ],
)

# ---------------------------------------------------------------------
# 10. Strategist report
# ---------------------------------------------------------------------

top_frames = frame_rows[:5]
weak_frames = sorted(frame_rows, key=lambda item: item["problem_framing_score"])[:5]
lock_in = origin_rows[:5]
weak_boundaries = sorted(boundary_rows, key=lambda item: item["boundary_quality_score"])[:5]
stakeholder_gaps = sorted(stakeholder_rows, key=lambda item: item["stakeholder_frame_quality_score"])[:5]
weak_causal = sorted(causal_rows, key=lambda item: item["causal_quality_score"])[:5]
priority_assumptions = assumption_rows[:6]
top_reframes = alternative_rows[:6]
top_triggers = trigger_rows[:6]
top_interventions = intervention_rows[:6]

report: list[str] = []

report.append("# Problem Framing and Problem Definition Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic separates problem-framing quality, symptom-framing risk, frame-origin lock-in risk, boundary quality, "
    "stakeholder frame quality, causal-depth quality, assumption priority, alternative-frame value, reframing trigger strength, "
    "and intervention priority. The purpose is to help strategists avoid solving the wrong problem with impressive discipline."
)
report.append("")
report.append("## Strongest problem frames")
report.append("")

for item in top_frames:
    report.append(
        f"- **{item['frame_id']} — {item['frame_name']}**: score {item['problem_framing_score']}; "
        f"diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Weakest or riskiest frames")
report.append("")

for item in weak_frames:
    report.append(
        f"- **{item['frame_id']} — {item['frame_name']}**: score {item['problem_framing_score']}; "
        f"symptom-framing risk {item['symptom_framing_risk']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest frame-origin lock-in risks")
report.append("")

for item in lock_in:
    report.append(
        f"- **{item['origin_id']} — {item['frame_name']}** from **{item['origin_source']}**: "
        f"lock-in risk {item['lock_in_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weakest boundary definitions")
report.append("")

for item in weak_boundaries:
    report.append(
        f"- **{item['boundary_id']} — {item['boundary_name']}** for **{item['frame_name']}**: "
        f"boundary quality {item['boundary_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Stakeholder frame gaps")
report.append("")

for item in stakeholder_gaps:
    report.append(
        f"- **{item['stakeholder_frame_id']} — {item['stakeholder_group']}** under **{item['frame_name']}**: "
        f"quality {item['stakeholder_frame_quality_score']}; hidden harm risk {item['hidden_harm_risk']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weakest causal models")
report.append("")

for item in weak_causal:
    report.append(
        f"- **{item['causal_id']} — {item['frame_name']}**: causal quality {item['causal_quality_score']}; "
        f"linear oversimplification risk {item['linear_oversimplification_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Priority assumptions to test")
report.append("")

for item in priority_assumptions:
    report.append(
        f"- **{item['assumption_id']} — {item['frame_name']}**: {item['assumption_text']} "
        f"(priority {item['assumption_priority_score']}); action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest-value alternative frames")
report.append("")

for item in top_reframes:
    report.append(
        f"- **{item['comparison_id']}**: compare **{item['primary_frame_name']}** with **{item['rival_frame_name']}** "
        f"(value {item['comparison_value_score']}); action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strongest reframing triggers")
report.append("")

for item in top_triggers:
    report.append(
        f"- **{item['trigger_id']} — {item['trigger_name']}** for **{item['frame_name']}**: "
        f"trigger strength {item['trigger_strength_score']}; if triggered: {item['action_if_triggered']}."
    )

report.append("")
report.append("## Highest-value framing interventions")
report.append("")

for item in top_interventions:
    report.append(
        f"- **{item['intervention_id']} — {item['intervention_name']}**: value {item['intervention_value_score']}; "
        f"target: {item['target_framing_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "The value of this workflow is disciplined problem construction. It helps teams avoid premature closure, boundary myopia, "
    "stakeholder blindness, symptom framing, causal oversimplification, solution imposition, institutional lock-in, and frame rigidity. "
    "It supports problem framing as a strategic capability: state the frame, test its origin, expand the boundary, compare stakeholder "
    "definitions, examine causal mechanisms, surface assumptions, compare alternatives, set reframing triggers, and preserve decision memory."
)

(REPORTS / "problem_framing_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_frames": top_frames,
    "weak_frames": weak_frames,
    "lock_in": lock_in,
    "weak_boundaries": weak_boundaries,
    "stakeholder_gaps": stakeholder_gaps,
    "weak_causal": weak_causal,
    "priority_assumptions": priority_assumptions,
    "top_reframes": top_reframes,
    "top_triggers": top_triggers,
    "top_interventions": top_interventions,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced problem-framing diagnostics complete.")
print(f"Wrote: {TABLES / 'problem_framing_scores.csv'}")
print(f"Wrote: {TABLES / 'frame_origin_review.csv'}")
print(f"Wrote: {TABLES / 'boundary_quality_review.csv'}")
print(f"Wrote: {TABLES / 'stakeholder_frame_review.csv'}")
print(f"Wrote: {TABLES / 'causal_depth_review.csv'}")
print(f"Wrote: {TABLES / 'assumption_transparency_review.csv'}")
print(f"Wrote: {TABLES / 'alternative_frame_review.csv'}")
print(f"Wrote: {TABLES / 'reframing_trigger_review.csv'}")
print(f"Wrote: {TABLES / 'intervention_recommendations.csv'}")
print(f"Wrote: {REPORTS / 'problem_framing_diagnostic_report.md'}")
