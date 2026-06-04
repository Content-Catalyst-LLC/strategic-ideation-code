#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for second-order effects and unintended consequences.

This dependency-light workflow uses only the Python standard library.

It produces:
- second-order effect scores
- propagation pathway review
- feedback-loop and policy-resistance review
- adaptive actor review
- burden-shift review
- fragility review
- scenario stress review
- early-warning indicator review
- learning-loop review
- intervention recommendations
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


interventions = read_csv(RAW / "interventions.csv")
pathways = read_csv(RAW / "propagation_pathways.csv")
feedback = read_csv(RAW / "feedback_loops.csv")
actors = read_csv(RAW / "adaptive_actors.csv")
burdens = read_csv(RAW / "burden_shifts.csv")
fragility = read_csv(RAW / "fragility_risks.csv")
scenarios = read_csv(RAW / "scenario_stress_tests.csv")
indicators = read_csv(RAW / "early_warning_indicators.csv")
learning = read_csv(RAW / "learning_loops.csv")
intervention_library = read_csv(RAW / "intervention_library.csv")

intervention_names = {row["intervention_id"]: row["intervention_name"] for row in interventions}

# ---------------------------------------------------------------------
# 1. Second-order effect profile scoring
# ---------------------------------------------------------------------

second_order_rows: list[dict[str, object]] = []

for row in interventions:
    second_order_profile = (
        0.14 * f(row, "first_order_gain")
        - 0.13 * f(row, "adaptation_pressure")
        - 0.13 * f(row, "feedback_amplification")
        - 0.11 * f(row, "delay_risk")
        - 0.12 * f(row, "burden_shift_risk")
        - 0.12 * f(row, "gaming_risk")
        - 0.15 * f(row, "long_term_fragility")
        + 0.14 * f(row, "learning_capacity")
        + 0.08 * f(row, "stakeholder_legitimacy")
        + 0.08 * f(row, "strategic_reversibility")
    )

    second_order_risk = (
        0.16 * f(row, "adaptation_pressure")
        + 0.15 * f(row, "feedback_amplification")
        + 0.14 * f(row, "delay_risk")
        + 0.15 * f(row, "burden_shift_risk")
        + 0.14 * f(row, "gaming_risk")
        + 0.16 * f(row, "long_term_fragility")
        - 0.10 * f(row, "learning_capacity")
        - 0.06 * f(row, "stakeholder_legitimacy")
        - 0.06 * f(row, "strategic_reversibility")
    )

    false_success_risk = (
        0.26 * f(row, "first_order_gain")
        + 0.20 * f(row, "long_term_fragility")
        + 0.16 * f(row, "delay_risk")
        + 0.14 * f(row, "gaming_risk")
        + 0.12 * f(row, "burden_shift_risk")
        - 0.16 * f(row, "learning_capacity")
    )

    if second_order_profile >= 0.14:
        diagnosis = "strategically_resilient_profile"
    elif false_success_risk >= 0.55:
        diagnosis = "false_first_order_success_risk"
    elif f(row, "gaming_risk") >= 0.70:
        diagnosis = "gaming_and_metric_distortion_risk"
    elif f(row, "burden_shift_risk") >= 0.70:
        diagnosis = "burden_shift_risk"
    elif f(row, "long_term_fragility") >= 0.70:
        diagnosis = "long_term_fragility_risk"
    elif f(row, "adaptation_pressure") >= 0.70:
        diagnosis = "adaptive_response_risk"
    else:
        diagnosis = "requires_second_order_review"

    second_order_rows.append(
        {
            "intervention_id": row["intervention_id"],
            "intervention_name": row["intervention_name"],
            "intervention_type": row["intervention_type"],
            "domain": row["domain"],
            "second_order_profile_score": round(second_order_profile, 4),
            "second_order_risk_score": round(second_order_risk, 4),
            "false_success_risk": round(false_success_risk, 4),
            "diagnosis": diagnosis,
            "first_order_gain": row["first_order_gain"],
            "adaptation_pressure": row["adaptation_pressure"],
            "feedback_amplification": row["feedback_amplification"],
            "delay_risk": row["delay_risk"],
            "burden_shift_risk": row["burden_shift_risk"],
            "gaming_risk": row["gaming_risk"],
            "long_term_fragility": row["long_term_fragility"],
            "learning_capacity": row["learning_capacity"],
            "stakeholder_legitimacy": row["stakeholder_legitimacy"],
            "strategic_reversibility": row["strategic_reversibility"],
            "description": row["description"],
        }
    )

second_order_rows.sort(key=lambda item: item["second_order_risk_score"], reverse=True)

second_order_fields = [
    "intervention_id",
    "intervention_name",
    "intervention_type",
    "domain",
    "second_order_profile_score",
    "second_order_risk_score",
    "false_success_risk",
    "diagnosis",
    "first_order_gain",
    "adaptation_pressure",
    "feedback_amplification",
    "delay_risk",
    "burden_shift_risk",
    "gaming_risk",
    "long_term_fragility",
    "learning_capacity",
    "stakeholder_legitimacy",
    "strategic_reversibility",
    "description",
]

write_csv(TABLES / "second_order_effect_scores.csv", second_order_rows, second_order_fields)
write_csv(PROCESSED / "second_order_effect_scores.csv", second_order_rows, second_order_fields)

# ---------------------------------------------------------------------
# 2. Propagation pathway review
# ---------------------------------------------------------------------

pathway_rows: list[dict[str, object]] = []

for row in pathways:
    pathway_risk = (
        0.16 * f(row, "cross_boundary_reach")
        + 0.15 * f(row, "dependency_creation")
        + 0.16 * f(row, "externality_risk")
        + 0.14 * f(row, "time_to_visibility")
        - 0.12 * f(row, "downstream_visibility")
        - 0.12 * f(row, "reversibility")
        - 0.10 * f(row, "monitoring_quality")
    )

    if f(row, "externality_risk") >= 0.70:
        action = "externality_and_burden_review_required"
    elif f(row, "dependency_creation") >= 0.75:
        action = "dependency_safeguards_required"
    elif pathway_risk >= 0.30:
        action = "map_propagation_before_scale"
    else:
        action = "monitor_pathway"

    pathway_rows.append(
        {
            "pathway_id": row["pathway_id"],
            "intervention_id": row["intervention_id"],
            "intervention_name": intervention_names.get(row["intervention_id"], row["intervention_id"]),
            "pathway_name": row["pathway_name"],
            "pathway_type": row["pathway_type"],
            "pathway_risk_score": round(pathway_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "cross_boundary_reach": row["cross_boundary_reach"],
            "dependency_creation": row["dependency_creation"],
            "externality_risk": row["externality_risk"],
            "downstream_visibility": row["downstream_visibility"],
            "time_to_visibility": row["time_to_visibility"],
            "reversibility": row["reversibility"],
            "monitoring_quality": row["monitoring_quality"],
        }
    )

pathway_rows.sort(key=lambda item: item["pathway_risk_score"], reverse=True)

write_csv(
    TABLES / "propagation_pathway_review.csv",
    pathway_rows,
    [
        "pathway_id",
        "intervention_id",
        "intervention_name",
        "pathway_name",
        "pathway_type",
        "pathway_risk_score",
        "recommended_action",
        "source_review_action",
        "cross_boundary_reach",
        "dependency_creation",
        "externality_risk",
        "downstream_visibility",
        "time_to_visibility",
        "reversibility",
        "monitoring_quality",
    ],
)

# ---------------------------------------------------------------------
# 3. Feedback-loop and policy-resistance review
# ---------------------------------------------------------------------

feedback_rows: list[dict[str, object]] = []

for row in feedback:
    feedback_risk = (
        0.16 * f(row, "loop_strength")
        + 0.16 * f(row, "reinforcing_risk")
        + 0.16 * f(row, "policy_resistance_risk")
        + 0.13 * f(row, "delay_risk")
        - 0.12 * f(row, "visibility")
        - 0.12 * f(row, "balancing_capacity")
        - 0.10 * f(row, "intervention_readiness")
    )

    if f(row, "policy_resistance_risk") >= 0.70:
        action = "policy_resistance_review_required"
    elif f(row, "reinforcing_risk") >= 0.75:
        action = "interrupt_reinforcing_problem_loop"
    elif f(row, "visibility") < 0.50 and feedback_risk >= 0.30:
        action = "make_feedback_visible"
    else:
        action = "monitor_feedback_loop"

    feedback_rows.append(
        {
            "loop_id": row["loop_id"],
            "intervention_id": row["intervention_id"],
            "intervention_name": intervention_names.get(row["intervention_id"], row["intervention_id"]),
            "loop_name": row["loop_name"],
            "loop_type": row["loop_type"],
            "feedback_risk_score": round(feedback_risk, 4),
            "recommended_action": action,
            "loop_strength": row["loop_strength"],
            "visibility": row["visibility"],
            "reinforcing_risk": row["reinforcing_risk"],
            "balancing_capacity": row["balancing_capacity"],
            "policy_resistance_risk": row["policy_resistance_risk"],
            "delay_risk": row["delay_risk"],
            "intervention_readiness": row["intervention_readiness"],
            "diagnostic_note": row["diagnostic_note"],
        }
    )

feedback_rows.sort(key=lambda item: item["feedback_risk_score"], reverse=True)

write_csv(
    TABLES / "feedback_loop_review.csv",
    feedback_rows,
    [
        "loop_id",
        "intervention_id",
        "intervention_name",
        "loop_name",
        "loop_type",
        "feedback_risk_score",
        "recommended_action",
        "loop_strength",
        "visibility",
        "reinforcing_risk",
        "balancing_capacity",
        "policy_resistance_risk",
        "delay_risk",
        "intervention_readiness",
        "diagnostic_note",
    ],
)

# ---------------------------------------------------------------------
# 4. Adaptive actor review
# ---------------------------------------------------------------------

actor_rows: list[dict[str, object]] = []

for row in actors:
    adaptation_risk = (
        0.14 * f(row, "adaptation_speed")
        + 0.14 * f(row, "strategic_awareness")
        + 0.14 * f(row, "workaround_likelihood")
        + 0.14 * f(row, "resistance_likelihood")
        + 0.14 * f(row, "gaming_likelihood")
        + 0.10 * f(row, "imitation_likelihood")
        + 0.12 * f(row, "influence_on_outcome")
        + 0.10 * f(row, "monitoring_gap")
        - 0.10 * f(row, "trust_sensitivity")
    )

    if f(row, "gaming_likelihood") >= 0.70:
        action = "gaming_and_metric_review_required"
    elif f(row, "workaround_likelihood") >= 0.70:
        action = "monitor_workarounds"
    elif f(row, "trust_sensitivity") >= 0.80:
        action = "legitimacy_review_required"
    elif adaptation_risk >= 0.50:
        action = "anticipate_adaptive_response"
    else:
        action = "monitor_actor_response"

    actor_rows.append(
        {
            "actor_id": row["actor_id"],
            "intervention_id": row["intervention_id"],
            "intervention_name": intervention_names.get(row["intervention_id"], row["intervention_id"]),
            "actor_group": row["actor_group"],
            "adaptation_risk_score": round(adaptation_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "adaptation_speed": row["adaptation_speed"],
            "strategic_awareness": row["strategic_awareness"],
            "workaround_likelihood": row["workaround_likelihood"],
            "resistance_likelihood": row["resistance_likelihood"],
            "gaming_likelihood": row["gaming_likelihood"],
            "imitation_likelihood": row["imitation_likelihood"],
            "trust_sensitivity": row["trust_sensitivity"],
            "influence_on_outcome": row["influence_on_outcome"],
            "monitoring_gap": row["monitoring_gap"],
        }
    )

actor_rows.sort(key=lambda item: item["adaptation_risk_score"], reverse=True)

write_csv(
    TABLES / "adaptive_actor_review.csv",
    actor_rows,
    [
        "actor_id",
        "intervention_id",
        "intervention_name",
        "actor_group",
        "adaptation_risk_score",
        "recommended_action",
        "source_review_action",
        "adaptation_speed",
        "strategic_awareness",
        "workaround_likelihood",
        "resistance_likelihood",
        "gaming_likelihood",
        "imitation_likelihood",
        "trust_sensitivity",
        "influence_on_outcome",
        "monitoring_gap",
    ],
)

# ---------------------------------------------------------------------
# 5. Burden-shift review
# ---------------------------------------------------------------------

burden_rows: list[dict[str, object]] = []

for row in burdens:
    burden_risk = (
        0.16 * f(row, "hidden_cost")
        + 0.15 * f(row, "administrative_load")
        + 0.13 * f(row, "emotional_load")
        + 0.14 * f(row, "risk_transfer")
        + 0.14 * f(row, "equity_risk")
        - 0.14 * f(row, "visibility_to_decision_makers")
        - 0.14 * f(row, "participatory_review_quality")
    )

    if burden_risk >= 0.45:
        action = "burden_shift_mitigation_required"
    elif f(row, "visibility_to_decision_makers") < 0.45:
        action = "make_hidden_burden_visible"
    elif f(row, "participatory_review_quality") < 0.45:
        action = "add_participatory_review"
    else:
        action = "monitor_burden"

    burden_rows.append(
        {
            "burden_id": row["burden_id"],
            "intervention_id": row["intervention_id"],
            "intervention_name": intervention_names.get(row["intervention_id"], row["intervention_id"]),
            "burden_location": row["burden_location"],
            "burden_type": row["burden_type"],
            "burden_risk_score": round(burden_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "hidden_cost": row["hidden_cost"],
            "administrative_load": row["administrative_load"],
            "emotional_load": row["emotional_load"],
            "risk_transfer": row["risk_transfer"],
            "equity_risk": row["equity_risk"],
            "visibility_to_decision_makers": row["visibility_to_decision_makers"],
            "participatory_review_quality": row["participatory_review_quality"],
        }
    )

burden_rows.sort(key=lambda item: item["burden_risk_score"], reverse=True)

write_csv(
    TABLES / "burden_shift_review.csv",
    burden_rows,
    [
        "burden_id",
        "intervention_id",
        "intervention_name",
        "burden_location",
        "burden_type",
        "burden_risk_score",
        "recommended_action",
        "source_review_action",
        "hidden_cost",
        "administrative_load",
        "emotional_load",
        "risk_transfer",
        "equity_risk",
        "visibility_to_decision_makers",
        "participatory_review_quality",
    ],
)

# ---------------------------------------------------------------------
# 6. Fragility review
# ---------------------------------------------------------------------

fragility_rows: list[dict[str, object]] = []

for row in fragility:
    fragility_score = (
        0.14 * f(row, "slack_reduction")
        + 0.13 * f(row, "redundancy_reduction")
        + 0.13 * f(row, "trust_erosion")
        + 0.13 * f(row, "option_closure")
        + 0.14 * f(row, "dependency_creation")
        + 0.14 * f(row, "recovery_capacity_loss")
        + 0.13 * f(row, "stress_exposure")
        - 0.12 * f(row, "monitoring_quality")
    )

    if fragility_score >= 0.55:
        action = "fragility_mitigation_required"
    elif f(row, "dependency_creation") >= 0.75:
        action = "fallback_capacity_required"
    elif f(row, "trust_erosion") >= 0.55:
        action = "trust_safeguards_required"
    else:
        action = "monitor_fragility"

    fragility_rows.append(
        {
            "fragility_id": row["fragility_id"],
            "intervention_id": row["intervention_id"],
            "intervention_name": intervention_names.get(row["intervention_id"], row["intervention_id"]),
            "fragility_type": row["fragility_type"],
            "fragility_score": round(fragility_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "slack_reduction": row["slack_reduction"],
            "redundancy_reduction": row["redundancy_reduction"],
            "trust_erosion": row["trust_erosion"],
            "option_closure": row["option_closure"],
            "dependency_creation": row["dependency_creation"],
            "recovery_capacity_loss": row["recovery_capacity_loss"],
            "stress_exposure": row["stress_exposure"],
            "monitoring_quality": row["monitoring_quality"],
        }
    )

fragility_rows.sort(key=lambda item: item["fragility_score"], reverse=True)

write_csv(
    TABLES / "fragility_review.csv",
    fragility_rows,
    [
        "fragility_id",
        "intervention_id",
        "intervention_name",
        "fragility_type",
        "fragility_score",
        "recommended_action",
        "source_review_action",
        "slack_reduction",
        "redundancy_reduction",
        "trust_erosion",
        "option_closure",
        "dependency_creation",
        "recovery_capacity_loss",
        "stress_exposure",
        "monitoring_quality",
    ],
)

# ---------------------------------------------------------------------
# 7. Scenario stress review
# ---------------------------------------------------------------------

scenario_rows: list[dict[str, object]] = []

for row in scenarios:
    scenario_risk = (
        0.12 * f(row, "plausibility")
        + 0.14 * f(row, "severity")
        + 0.13 * f(row, "delay_exposure")
        + 0.13 * f(row, "adaptation_exposure")
        + 0.13 * f(row, "feedback_exposure")
        + 0.13 * f(row, "burden_exposure")
        + 0.14 * f(row, "fragility_exposure")
        - 0.10 * f(row, "preparation_quality")
        - 0.08 * f(row, "response_flexibility")
    )

    if scenario_risk >= 0.58:
        action = "stress_test_before_scale"
    elif f(row, "burden_exposure") >= 0.75:
        action = "burden_scenario_review_required"
    elif f(row, "fragility_exposure") >= 0.75:
        action = "fragility_scenario_review_required"
    else:
        action = "monitor_scenario"

    scenario_rows.append(
        {
            "scenario_id": row["scenario_id"],
            "intervention_id": row["intervention_id"],
            "intervention_name": intervention_names.get(row["intervention_id"], row["intervention_id"]),
            "scenario_name": row["scenario_name"],
            "scenario_type": row["scenario_type"],
            "scenario_risk_score": round(scenario_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "plausibility": row["plausibility"],
            "severity": row["severity"],
            "delay_exposure": row["delay_exposure"],
            "adaptation_exposure": row["adaptation_exposure"],
            "feedback_exposure": row["feedback_exposure"],
            "burden_exposure": row["burden_exposure"],
            "fragility_exposure": row["fragility_exposure"],
            "preparation_quality": row["preparation_quality"],
            "response_flexibility": row["response_flexibility"],
        }
    )

scenario_rows.sort(key=lambda item: item["scenario_risk_score"], reverse=True)

write_csv(
    TABLES / "scenario_stress_review.csv",
    scenario_rows,
    [
        "scenario_id",
        "intervention_id",
        "intervention_name",
        "scenario_name",
        "scenario_type",
        "scenario_risk_score",
        "recommended_action",
        "source_review_action",
        "plausibility",
        "severity",
        "delay_exposure",
        "adaptation_exposure",
        "feedback_exposure",
        "burden_exposure",
        "fragility_exposure",
        "preparation_quality",
        "response_flexibility",
    ],
)

# ---------------------------------------------------------------------
# 8. Early-warning indicator review
# ---------------------------------------------------------------------

indicator_rows: list[dict[str, object]] = []

for row in indicators:
    indicator_quality = (
        0.15 * f(row, "leading_quality")
        + 0.13 * f(row, "visibility")
        + 0.13 * f(row, "reliability")
        + 0.13 * f(row, "timeliness")
        + 0.12 * f(row, "sensitivity")
        + 0.14 * f(row, "decision_linkage")
        - 0.08 * f(row, "false_positive_risk")
        - 0.08 * f(row, "monitoring_cost")
    )

    if indicator_quality >= 0.56:
        action = "use_as_early_warning_signal"
    elif f(row, "decision_linkage") < 0.55:
        action = "connect_signal_to_revision_trigger"
    elif f(row, "visibility") < 0.55:
        action = "improve_signal_visibility"
    else:
        action = "develop_indicator"

    indicator_rows.append(
        {
            "indicator_id": row["indicator_id"],
            "intervention_id": row["intervention_id"],
            "intervention_name": intervention_names.get(row["intervention_id"], row["intervention_id"]),
            "indicator_name": row["indicator_name"],
            "signal_type": row["signal_type"],
            "indicator_quality_score": round(indicator_quality, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "trigger_threshold": row["trigger_threshold"],
            "leading_quality": row["leading_quality"],
            "visibility": row["visibility"],
            "reliability": row["reliability"],
            "timeliness": row["timeliness"],
            "sensitivity": row["sensitivity"],
            "false_positive_risk": row["false_positive_risk"],
            "decision_linkage": row["decision_linkage"],
            "monitoring_cost": row["monitoring_cost"],
        }
    )

indicator_rows.sort(key=lambda item: item["indicator_quality_score"], reverse=True)

write_csv(
    TABLES / "early_warning_indicator_review.csv",
    indicator_rows,
    [
        "indicator_id",
        "intervention_id",
        "intervention_name",
        "indicator_name",
        "signal_type",
        "indicator_quality_score",
        "recommended_action",
        "source_review_action",
        "trigger_threshold",
        "leading_quality",
        "visibility",
        "reliability",
        "timeliness",
        "sensitivity",
        "false_positive_risk",
        "decision_linkage",
        "monitoring_cost",
    ],
)

# ---------------------------------------------------------------------
# 9. Learning-loop review
# ---------------------------------------------------------------------

learning_rows: list[dict[str, object]] = []

for row in learning:
    learning_quality = (
        0.14 * f(row, "feedback_quality")
        + 0.14 * f(row, "revision_trigger_clarity")
        + 0.14 * f(row, "decision_memory_quality")
        + 0.14 * f(row, "stakeholder_learning_visibility")
        + 0.12 * f(row, "scenario_update_quality")
        + 0.12 * f(row, "governance_response_capacity")
        + 0.08 * f(row, "cycle_time")
        - 0.10 * f(row, "learning_risk")
    )

    if learning_quality >= 0.58:
        action = "learning_loop_ready_for_use"
    elif f(row, "decision_memory_quality") < 0.55:
        action = "build_decision_memory"
    elif f(row, "revision_trigger_clarity") < 0.55:
        action = "define_revision_triggers"
    else:
        action = "strengthen_learning_loop"

    learning_rows.append(
        {
            "learning_id": row["learning_id"],
            "intervention_id": row["intervention_id"],
            "intervention_name": intervention_names.get(row["intervention_id"], row["intervention_id"]),
            "learning_loop_name": row["learning_loop_name"],
            "learning_quality_score": round(learning_quality, 4),
            "recommended_action": action,
            "action_if_triggered": row["action_if_triggered"],
            "feedback_quality": row["feedback_quality"],
            "revision_trigger_clarity": row["revision_trigger_clarity"],
            "decision_memory_quality": row["decision_memory_quality"],
            "stakeholder_learning_visibility": row["stakeholder_learning_visibility"],
            "scenario_update_quality": row["scenario_update_quality"],
            "governance_response_capacity": row["governance_response_capacity"],
            "cycle_time": row["cycle_time"],
            "learning_risk": row["learning_risk"],
        }
    )

learning_rows.sort(key=lambda item: item["learning_quality_score"])

write_csv(
    TABLES / "learning_loop_review.csv",
    learning_rows,
    [
        "learning_id",
        "intervention_id",
        "intervention_name",
        "learning_loop_name",
        "learning_quality_score",
        "recommended_action",
        "action_if_triggered",
        "feedback_quality",
        "revision_trigger_clarity",
        "decision_memory_quality",
        "stakeholder_learning_visibility",
        "scenario_update_quality",
        "governance_response_capacity",
        "cycle_time",
        "learning_risk",
    ],
)

# ---------------------------------------------------------------------
# 10. Intervention recommendations
# ---------------------------------------------------------------------

intervention_rows: list[dict[str, object]] = []

for row in intervention_library:
    intervention_value = (
        0.13 * f(row, "propagation_mapping_gain")
        + 0.14 * f(row, "feedback_review_gain")
        + 0.14 * f(row, "burden_review_gain")
        + 0.13 * f(row, "incentive_review_gain")
        + 0.13 * f(row, "fragility_review_gain")
        + 0.14 * f(row, "learning_gain")
        + 0.13 * f(row, "decision_memory_gain")
        - 0.08 * f(row, "process_cost")
        - 0.08 * f(row, "implementation_complexity")
        - 0.08 * f(row, "political_safety_need")
    )

    if f(row, "political_safety_need") >= 0.40:
        action = "requires_leadership_protection"
    elif intervention_value >= 0.56:
        action = "high_value_second_order_intervention"
    else:
        action = "supporting_intervention"

    intervention_rows.append(
        {
            "intervention_id": row["intervention_id"],
            "intervention_name": row["intervention_name"],
            "target_second_order_risk": row["target_second_order_risk"],
            "intervention_value_score": round(intervention_value, 4),
            "recommended_action": action,
            "process_cost": row["process_cost"],
            "implementation_complexity": row["implementation_complexity"],
            "propagation_mapping_gain": row["propagation_mapping_gain"],
            "feedback_review_gain": row["feedback_review_gain"],
            "burden_review_gain": row["burden_review_gain"],
            "incentive_review_gain": row["incentive_review_gain"],
            "fragility_review_gain": row["fragility_review_gain"],
            "learning_gain": row["learning_gain"],
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
        "target_second_order_risk",
        "intervention_value_score",
        "recommended_action",
        "process_cost",
        "implementation_complexity",
        "propagation_mapping_gain",
        "feedback_review_gain",
        "burden_review_gain",
        "incentive_review_gain",
        "fragility_review_gain",
        "learning_gain",
        "decision_memory_gain",
        "political_safety_need",
    ],
)

# ---------------------------------------------------------------------
# 11. Strategist report
# ---------------------------------------------------------------------

highest_risk = second_order_rows[:6]
most_resilient = sorted(second_order_rows, key=lambda item: item["second_order_profile_score"], reverse=True)[:5]
highest_pathways = pathway_rows[:5]
highest_feedback = feedback_rows[:5]
highest_adaptation = actor_rows[:5]
highest_burden = burden_rows[:5]
highest_fragility = fragility_rows[:5]
highest_scenarios = scenario_rows[:5]
top_indicators = indicator_rows[:6]
weak_learning = learning_rows[:5]
top_interventions = intervention_rows[:6]

report: list[str] = []

report.append("# Second-Order Effects and Unintended Consequences Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic separates first-order gain from second-order risk. It reviews propagation pathways, feedback loops, adaptive actors, "
    "burden shifts, fragility, scenario stress, early-warning indicators, learning loops, and intervention priorities. The purpose is to help "
    "strategists avoid false first-order success, delayed fragility, policy resistance, metric distortion, hidden burden, and unintended cascading effects."
)
report.append("")
report.append("## Highest second-order risk interventions")
report.append("")

for item in highest_risk:
    report.append(
        f"- **{item['intervention_id']} — {item['intervention_name']}**: risk {item['second_order_risk_score']}; "
        f"false-success risk {item['false_success_risk']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Most resilient second-order profiles")
report.append("")

for item in most_resilient:
    report.append(
        f"- **{item['intervention_id']} — {item['intervention_name']}**: profile {item['second_order_profile_score']}; "
        f"learning capacity {item['learning_capacity']}; legitimacy {item['stakeholder_legitimacy']}."
    )

report.append("")
report.append("## Propagation pathways requiring attention")
report.append("")

for item in highest_pathways:
    report.append(
        f"- **{item['pathway_id']} — {item['pathway_name']}** for **{item['intervention_name']}**: "
        f"pathway risk {item['pathway_risk_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Feedback loops and policy-resistance risks")
report.append("")

for item in highest_feedback:
    report.append(
        f"- **{item['loop_id']} — {item['loop_name']}** for **{item['intervention_name']}**: "
        f"feedback risk {item['feedback_risk_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Adaptive actors likely to change the outcome")
report.append("")

for item in highest_adaptation:
    report.append(
        f"- **{item['actor_id']} — {item['actor_group']}** for **{item['intervention_name']}**: "
        f"adaptation risk {item['adaptation_risk_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Burden shifts requiring review")
report.append("")

for item in highest_burden:
    report.append(
        f"- **{item['burden_id']} — {item['burden_location']}** under **{item['intervention_name']}**: "
        f"burden risk {item['burden_risk_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Fragility risks requiring mitigation")
report.append("")

for item in highest_fragility:
    report.append(
        f"- **{item['fragility_id']} — {item['fragility_type']}** under **{item['intervention_name']}**: "
        f"fragility score {item['fragility_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Scenario stress tests")
report.append("")

for item in highest_scenarios:
    report.append(
        f"- **{item['scenario_id']} — {item['scenario_name']}** for **{item['intervention_name']}**: "
        f"scenario risk {item['scenario_risk_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strong early-warning indicators")
report.append("")

for item in top_indicators:
    report.append(
        f"- **{item['indicator_id']} — {item['indicator_name']}** for **{item['intervention_name']}**: "
        f"indicator quality {item['indicator_quality_score']}; threshold: {item['trigger_threshold']}."
    )

report.append("")
report.append("## Learning loops needing repair")
report.append("")

for item in weak_learning:
    report.append(
        f"- **{item['learning_id']} — {item['learning_loop_name']}** for **{item['intervention_name']}**: "
        f"learning quality {item['learning_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest-value second-order interventions")
report.append("")

for item in top_interventions:
    report.append(
        f"- **{item['intervention_id']} — {item['intervention_name']}**: value {item['intervention_value_score']}; "
        f"target: {item['target_second_order_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "The value of this workflow is disciplined causal expansion. It helps teams avoid first-order fixation, boundary myopia, metric substitution, "
    "adaptation blindness, delay neglect, fragility creation, wrong escalation, and learning-loop failure. It supports second-order reasoning as a practical "
    "discipline: define the first-order effect, map propagation, anticipate actor response, review incentives, identify burden shifts, extend the time horizon, "
    "assess fragility, define early-warning signals, set revision triggers, and preserve decision memory."
)

(REPORTS / "second_order_effects_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "highest_risk": highest_risk,
    "most_resilient": most_resilient,
    "highest_pathways": highest_pathways,
    "highest_feedback": highest_feedback,
    "highest_adaptation": highest_adaptation,
    "highest_burden": highest_burden,
    "highest_fragility": highest_fragility,
    "highest_scenarios": highest_scenarios,
    "top_indicators": top_indicators,
    "weak_learning": weak_learning,
    "top_interventions": top_interventions,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced second-order effects diagnostics complete.")
print(f"Wrote: {TABLES / 'second_order_effect_scores.csv'}")
print(f"Wrote: {TABLES / 'propagation_pathway_review.csv'}")
print(f"Wrote: {TABLES / 'feedback_loop_review.csv'}")
print(f"Wrote: {TABLES / 'adaptive_actor_review.csv'}")
print(f"Wrote: {TABLES / 'burden_shift_review.csv'}")
print(f"Wrote: {TABLES / 'fragility_review.csv'}")
print(f"Wrote: {TABLES / 'scenario_stress_review.csv'}")
print(f"Wrote: {TABLES / 'early_warning_indicator_review.csv'}")
print(f"Wrote: {TABLES / 'learning_loop_review.csv'}")
print(f"Wrote: {TABLES / 'intervention_recommendations.csv'}")
print(f"Wrote: {REPORTS / 'second_order_effects_diagnostic_report.md'}")
