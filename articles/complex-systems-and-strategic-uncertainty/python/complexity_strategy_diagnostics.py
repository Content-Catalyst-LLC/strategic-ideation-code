#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for complex systems and strategic uncertainty.

This dependency-light workflow uses only the Python standard library.

It produces:
- complexity profile scores
- structural uncertainty review
- feedback-loop review
- adaptive actor review
- path-dependence and lock-in review
- scenario robustness review
- adaptive option review
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


environments = read_csv(RAW / "complexity_environments.csv")
uncertainty = read_csv(RAW / "uncertainty_drivers.csv")
feedback = read_csv(RAW / "feedback_loops.csv")
actors = read_csv(RAW / "adaptive_actors.csv")
paths = read_csv(RAW / "path_dependence.csv")
scenarios = read_csv(RAW / "scenario_robustness.csv")
options = read_csv(RAW / "adaptive_options.csv")
indicators = read_csv(RAW / "early_warning_indicators.csv")
learning = read_csv(RAW / "learning_loops.csv")
interventions = read_csv(RAW / "intervention_library.csv")

environment_names = {row["environment_id"]: row["environment_name"] for row in environments}

# ---------------------------------------------------------------------
# 1. Complexity profile scoring
# ---------------------------------------------------------------------

environment_rows: list[dict[str, object]] = []

for row in environments:
    complexity_profile = (
        0.13 * f(row, "interdependence")
        + 0.13 * f(row, "nonlinearity")
        + 0.14 * f(row, "feedback_intensity")
        + 0.12 * f(row, "adaptation_pressure")
        + 0.11 * f(row, "path_dependence")
        + 0.10 * f(row, "boundary_ambiguity")
        + 0.10 * f(row, "emergence_potential")
        + 0.09 * f(row, "deep_uncertainty")
        + 0.09 * f(row, "scenario_need")
        + 0.09 * f(row, "learning_capacity_need")
    )

    linear_planning_risk = (
        0.20 * f(row, "nonlinearity")
        + 0.20 * f(row, "feedback_intensity")
        + 0.18 * f(row, "adaptation_pressure")
        + 0.16 * f(row, "deep_uncertainty")
        + 0.14 * f(row, "boundary_ambiguity")
        + 0.12 * f(row, "emergence_potential")
    )

    if complexity_profile >= 0.76:
        diagnosis = "adaptive_scenario_strategy_required"
    elif complexity_profile >= 0.60:
        diagnosis = "complexity_aware_strategy_recommended"
    elif linear_planning_risk >= 0.58:
        diagnosis = "linear_planning_risk"
    else:
        diagnosis = "standard_planning_may_be_sufficient"

    environment_rows.append(
        {
            "environment_id": row["environment_id"],
            "environment_name": row["environment_name"],
            "environment_type": row["environment_type"],
            "domain": row["domain"],
            "complexity_profile_score": round(complexity_profile, 4),
            "linear_planning_risk": round(linear_planning_risk, 4),
            "diagnosis": diagnosis,
            "interdependence": row["interdependence"],
            "nonlinearity": row["nonlinearity"],
            "feedback_intensity": row["feedback_intensity"],
            "adaptation_pressure": row["adaptation_pressure"],
            "path_dependence": row["path_dependence"],
            "boundary_ambiguity": row["boundary_ambiguity"],
            "emergence_potential": row["emergence_potential"],
            "deep_uncertainty": row["deep_uncertainty"],
            "scenario_need": row["scenario_need"],
            "learning_capacity_need": row["learning_capacity_need"],
            "description": row["description"],
        }
    )

environment_rows.sort(key=lambda item: item["complexity_profile_score"], reverse=True)

environment_fields = [
    "environment_id",
    "environment_name",
    "environment_type",
    "domain",
    "complexity_profile_score",
    "linear_planning_risk",
    "diagnosis",
    "interdependence",
    "nonlinearity",
    "feedback_intensity",
    "adaptation_pressure",
    "path_dependence",
    "boundary_ambiguity",
    "emergence_potential",
    "deep_uncertainty",
    "scenario_need",
    "learning_capacity_need",
    "description",
]

write_csv(TABLES / "complexity_profile_scores.csv", environment_rows, environment_fields)
write_csv(PROCESSED / "complexity_profile_scores.csv", environment_rows, environment_fields)

# ---------------------------------------------------------------------
# 2. Uncertainty driver review
# ---------------------------------------------------------------------

uncertainty_rows: list[dict[str, object]] = []

for row in uncertainty:
    uncertainty_intensity = (
        0.16 * f(row, "volatility")
        + 0.16 * f(row, "ambiguity")
        + 0.16 * f(row, "model_uncertainty")
        + 0.14 * f(row, "probability_instability")
        + 0.14 * f(row, "value_contestation")
        + 0.12 * f(row, "actor_reflexivity")
        - 0.08 * f(row, "monitoring_quality")
        - 0.08 * f(row, "mitigation_quality")
    )

    if uncertainty_intensity >= 0.55:
        action = "scenario_and_adaptive_pathway_required"
    elif f(row, "actor_reflexivity") >= 0.75:
        action = "monitor_adaptive_actor_response"
    elif f(row, "value_contestation") >= 0.75:
        action = "stakeholder_and_legitimacy_review_required"
    else:
        action = "manage_with_targeted_uncertainty_review"

    uncertainty_rows.append(
        {
            "driver_id": row["driver_id"],
            "environment_id": row["environment_id"],
            "environment_name": environment_names.get(row["environment_id"], row["environment_id"]),
            "driver_name": row["driver_name"],
            "driver_type": row["driver_type"],
            "uncertainty_intensity_score": round(uncertainty_intensity, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "volatility": row["volatility"],
            "ambiguity": row["ambiguity"],
            "model_uncertainty": row["model_uncertainty"],
            "probability_instability": row["probability_instability"],
            "value_contestation": row["value_contestation"],
            "actor_reflexivity": row["actor_reflexivity"],
            "monitoring_quality": row["monitoring_quality"],
            "mitigation_quality": row["mitigation_quality"],
        }
    )

uncertainty_rows.sort(key=lambda item: item["uncertainty_intensity_score"], reverse=True)

write_csv(
    TABLES / "uncertainty_driver_review.csv",
    uncertainty_rows,
    [
        "driver_id",
        "environment_id",
        "environment_name",
        "driver_name",
        "driver_type",
        "uncertainty_intensity_score",
        "recommended_action",
        "source_review_action",
        "volatility",
        "ambiguity",
        "model_uncertainty",
        "probability_instability",
        "value_contestation",
        "actor_reflexivity",
        "monitoring_quality",
        "mitigation_quality",
    ],
)

# ---------------------------------------------------------------------
# 3. Feedback-loop review
# ---------------------------------------------------------------------

feedback_rows: list[dict[str, object]] = []

for row in feedback:
    feedback_risk = (
        0.16 * f(row, "loop_strength")
        + 0.16 * f(row, "reinforcing_risk")
        + 0.14 * f(row, "delay_risk")
        + 0.12 * f(row, "stakeholder_burden_risk")
        - 0.12 * f(row, "visibility")
        - 0.12 * f(row, "balancing_capacity")
        - 0.10 * f(row, "intervention_readiness")
    )

    if feedback_risk >= 0.35 and f(row, "visibility") < 0.60:
        action = "map_and_make_feedback_visible"
    elif f(row, "reinforcing_risk") >= 0.75:
        action = "interrupt_reinforcing_problem_loop"
    elif f(row, "delay_risk") >= 0.65:
        action = "add_delayed_effect_review"
    else:
        action = "monitor_feedback_loop"

    feedback_rows.append(
        {
            "loop_id": row["loop_id"],
            "environment_id": row["environment_id"],
            "environment_name": environment_names.get(row["environment_id"], row["environment_id"]),
            "loop_name": row["loop_name"],
            "loop_type": row["loop_type"],
            "feedback_risk_score": round(feedback_risk, 4),
            "recommended_action": action,
            "loop_strength": row["loop_strength"],
            "visibility": row["visibility"],
            "reinforcing_risk": row["reinforcing_risk"],
            "balancing_capacity": row["balancing_capacity"],
            "delay_risk": row["delay_risk"],
            "intervention_readiness": row["intervention_readiness"],
            "stakeholder_burden_risk": row["stakeholder_burden_risk"],
            "diagnostic_note": row["diagnostic_note"],
        }
    )

feedback_rows.sort(key=lambda item: item["feedback_risk_score"], reverse=True)

write_csv(
    TABLES / "feedback_loop_review.csv",
    feedback_rows,
    [
        "loop_id",
        "environment_id",
        "environment_name",
        "loop_name",
        "loop_type",
        "feedback_risk_score",
        "recommended_action",
        "loop_strength",
        "visibility",
        "reinforcing_risk",
        "balancing_capacity",
        "delay_risk",
        "intervention_readiness",
        "stakeholder_burden_risk",
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
        + 0.12 * f(row, "imitation_likelihood")
        + 0.12 * f(row, "resistance_likelihood")
        + 0.12 * f(row, "gaming_likelihood")
        + 0.12 * f(row, "influence_on_system")
        - 0.10 * f(row, "learning_capacity")
        + 0.10 * f(row, "monitoring_gap")
    )

    if f(row, "gaming_likelihood") >= 0.65:
        action = "add_metric_gaming_review"
    elif f(row, "workaround_likelihood") >= 0.70:
        action = "monitor_workarounds"
    elif f(row, "resistance_likelihood") >= 0.70:
        action = "build_legitimacy_and_incentive_review"
    elif adaptation_risk >= 0.55:
        action = "anticipate_adaptive_response"
    else:
        action = "monitor_actor_response"

    actor_rows.append(
        {
            "actor_id": row["actor_id"],
            "environment_id": row["environment_id"],
            "environment_name": environment_names.get(row["environment_id"], row["environment_id"]),
            "actor_group": row["actor_group"],
            "adaptation_risk_score": round(adaptation_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "adaptation_speed": row["adaptation_speed"],
            "strategic_awareness": row["strategic_awareness"],
            "workaround_likelihood": row["workaround_likelihood"],
            "imitation_likelihood": row["imitation_likelihood"],
            "resistance_likelihood": row["resistance_likelihood"],
            "gaming_likelihood": row["gaming_likelihood"],
            "learning_capacity": row["learning_capacity"],
            "influence_on_system": row["influence_on_system"],
            "monitoring_gap": row["monitoring_gap"],
        }
    )

actor_rows.sort(key=lambda item: item["adaptation_risk_score"], reverse=True)

write_csv(
    TABLES / "adaptive_actor_review.csv",
    actor_rows,
    [
        "actor_id",
        "environment_id",
        "environment_name",
        "actor_group",
        "adaptation_risk_score",
        "recommended_action",
        "source_review_action",
        "adaptation_speed",
        "strategic_awareness",
        "workaround_likelihood",
        "imitation_likelihood",
        "resistance_likelihood",
        "gaming_likelihood",
        "learning_capacity",
        "influence_on_system",
        "monitoring_gap",
    ],
)

# ---------------------------------------------------------------------
# 5. Path-dependence review
# ---------------------------------------------------------------------

path_rows: list[dict[str, object]] = []

for row in paths:
    lock_in_risk = (
        0.14 * f(row, "legacy_strength")
        + 0.14 * f(row, "sunk_cost_pressure")
        + 0.14 * f(row, "coordination_lock_in")
        + 0.12 * f(row, "standardization_lock_in")
        + 0.12 * f(row, "trust_memory_effect")
        + 0.12 * f(row, "transition_cost")
        + 0.12 * f(row, "option_closure_risk")
        - 0.12 * f(row, "reversibility")
    )

    if lock_in_risk >= 0.60:
        action = "design_adaptive_transition_pathway"
    elif f(row, "option_closure_risk") >= 0.65:
        action = "preserve_future_options"
    elif f(row, "trust_memory_effect") >= 0.75:
        action = "include_history_and_trust_repair"
    else:
        action = "manage_path_dependence"

    path_rows.append(
        {
            "path_id": row["path_id"],
            "environment_id": row["environment_id"],
            "environment_name": environment_names.get(row["environment_id"], row["environment_id"]),
            "path_factor": row["path_factor"],
            "path_type": row["path_type"],
            "lock_in_risk_score": round(lock_in_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "legacy_strength": row["legacy_strength"],
            "sunk_cost_pressure": row["sunk_cost_pressure"],
            "coordination_lock_in": row["coordination_lock_in"],
            "standardization_lock_in": row["standardization_lock_in"],
            "trust_memory_effect": row["trust_memory_effect"],
            "transition_cost": row["transition_cost"],
            "option_closure_risk": row["option_closure_risk"],
            "reversibility": row["reversibility"],
        }
    )

path_rows.sort(key=lambda item: item["lock_in_risk_score"], reverse=True)

write_csv(
    TABLES / "path_dependence_review.csv",
    path_rows,
    [
        "path_id",
        "environment_id",
        "environment_name",
        "path_factor",
        "path_type",
        "lock_in_risk_score",
        "recommended_action",
        "source_review_action",
        "legacy_strength",
        "sunk_cost_pressure",
        "coordination_lock_in",
        "standardization_lock_in",
        "trust_memory_effect",
        "transition_cost",
        "option_closure_risk",
        "reversibility",
    ],
)

# ---------------------------------------------------------------------
# 6. Scenario robustness review
# ---------------------------------------------------------------------

scenario_rows: list[dict[str, object]] = []

for row in scenarios:
    scenario_risk = (
        0.14 * f(row, "plausibility")
        + 0.16 * f(row, "severity")
        + 0.12 * f(row, "novelty")
        + 0.16 * f(row, "strategic_disruption")
        + 0.14 * f(row, "robustness_gap")
        - 0.10 * f(row, "signal_visibility")
        - 0.10 * f(row, "preparation_quality")
        - 0.08 * f(row, "response_flexibility")
    )

    if scenario_risk >= 0.48:
        action = "stress_test_strategy_and_build_options"
    elif f(row, "robustness_gap") >= 0.60:
        action = "close_robustness_gap"
    elif f(row, "signal_visibility") < 0.45:
        action = "improve_signal_detection"
    else:
        action = "monitor_scenario"

    scenario_rows.append(
        {
            "scenario_id": row["scenario_id"],
            "environment_id": row["environment_id"],
            "environment_name": environment_names.get(row["environment_id"], row["environment_id"]),
            "scenario_name": row["scenario_name"],
            "scenario_type": row["scenario_type"],
            "scenario_risk_score": round(scenario_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "plausibility": row["plausibility"],
            "severity": row["severity"],
            "novelty": row["novelty"],
            "strategic_disruption": row["strategic_disruption"],
            "signal_visibility": row["signal_visibility"],
            "preparation_quality": row["preparation_quality"],
            "response_flexibility": row["response_flexibility"],
            "robustness_gap": row["robustness_gap"],
        }
    )

scenario_rows.sort(key=lambda item: item["scenario_risk_score"], reverse=True)

write_csv(
    TABLES / "scenario_robustness_review.csv",
    scenario_rows,
    [
        "scenario_id",
        "environment_id",
        "environment_name",
        "scenario_name",
        "scenario_type",
        "scenario_risk_score",
        "recommended_action",
        "source_review_action",
        "plausibility",
        "severity",
        "novelty",
        "strategic_disruption",
        "signal_visibility",
        "preparation_quality",
        "response_flexibility",
        "robustness_gap",
    ],
)

# ---------------------------------------------------------------------
# 7. Adaptive option review
# ---------------------------------------------------------------------

option_rows: list[dict[str, object]] = []

for row in options:
    option_value = (
        0.14 * f(row, "robustness")
        + 0.15 * f(row, "option_value")
        + 0.12 * f(row, "reversibility")
        + 0.14 * f(row, "learning_value")
        + 0.12 * f(row, "downside_protection")
        - 0.10 * f(row, "resource_intensity")
        - 0.08 * f(row, "time_to_learning")
        + 0.12 * f(row, "strategic_coherence")
        - 0.08 * f(row, "legitimacy_requirement")
        + 0.10 * f(row, "evidence_readiness")
    )

    if option_value >= 0.55:
        action = "priority_adaptive_option"
    elif f(row, "legitimacy_requirement") >= 0.80:
        action = "add_legitimacy_safeguards"
    elif f(row, "resource_intensity") >= 0.65:
        action = "stage_commitment"
    else:
        action = "develop_or_monitor_option"

    option_rows.append(
        {
            "option_id": row["option_id"],
            "environment_id": row["environment_id"],
            "environment_name": environment_names.get(row["environment_id"], row["environment_id"]),
            "option_name": row["option_name"],
            "option_type": row["option_type"],
            "adaptive_option_value_score": round(option_value, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "robustness": row["robustness"],
            "option_value": row["option_value"],
            "reversibility": row["reversibility"],
            "learning_value": row["learning_value"],
            "downside_protection": row["downside_protection"],
            "resource_intensity": row["resource_intensity"],
            "time_to_learning": row["time_to_learning"],
            "strategic_coherence": row["strategic_coherence"],
            "legitimacy_requirement": row["legitimacy_requirement"],
            "evidence_readiness": row["evidence_readiness"],
        }
    )

option_rows.sort(key=lambda item: item["adaptive_option_value_score"], reverse=True)

write_csv(
    TABLES / "adaptive_option_review.csv",
    option_rows,
    [
        "option_id",
        "environment_id",
        "environment_name",
        "option_name",
        "option_type",
        "adaptive_option_value_score",
        "recommended_action",
        "source_review_action",
        "robustness",
        "option_value",
        "reversibility",
        "learning_value",
        "downside_protection",
        "resource_intensity",
        "time_to_learning",
        "strategic_coherence",
        "legitimacy_requirement",
        "evidence_readiness",
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

    if indicator_quality >= 0.55:
        action = "use_as_early_warning_signal"
    elif f(row, "decision_linkage") < 0.55:
        action = "connect_signal_to_decision_trigger"
    elif f(row, "visibility") < 0.55:
        action = "improve_signal_visibility"
    else:
        action = "develop_indicator"

    indicator_rows.append(
        {
            "indicator_id": row["indicator_id"],
            "environment_id": row["environment_id"],
            "environment_name": environment_names.get(row["environment_id"], row["environment_id"]),
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
        "environment_id",
        "environment_name",
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
        + 0.14 * f(row, "scenario_update_quality")
        + 0.12 * f(row, "stakeholder_learning_visibility")
        + 0.12 * f(row, "governance_response_capacity")
        + 0.08 * f(row, "cycle_time")
        - 0.10 * f(row, "learning_risk")
    )

    if learning_quality >= 0.58:
        action = "learning_loop_ready_for_use"
    elif f(row, "decision_memory_quality") < 0.60:
        action = "build_decision_memory"
    elif f(row, "revision_trigger_clarity") < 0.60:
        action = "define_revision_triggers"
    else:
        action = "strengthen_learning_loop"

    learning_rows.append(
        {
            "learning_id": row["learning_id"],
            "environment_id": row["environment_id"],
            "environment_name": environment_names.get(row["environment_id"], row["environment_id"]),
            "learning_loop_name": row["learning_loop_name"],
            "learning_quality_score": round(learning_quality, 4),
            "recommended_action": action,
            "action_if_triggered": row["action_if_triggered"],
            "feedback_quality": row["feedback_quality"],
            "revision_trigger_clarity": row["revision_trigger_clarity"],
            "decision_memory_quality": row["decision_memory_quality"],
            "scenario_update_quality": row["scenario_update_quality"],
            "stakeholder_learning_visibility": row["stakeholder_learning_visibility"],
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
        "environment_id",
        "environment_name",
        "learning_loop_name",
        "learning_quality_score",
        "recommended_action",
        "action_if_triggered",
        "feedback_quality",
        "revision_trigger_clarity",
        "decision_memory_quality",
        "scenario_update_quality",
        "stakeholder_learning_visibility",
        "governance_response_capacity",
        "cycle_time",
        "learning_risk",
    ],
)

# ---------------------------------------------------------------------
# 10. Intervention recommendations
# ---------------------------------------------------------------------

intervention_rows: list[dict[str, object]] = []

for row in interventions:
    intervention_value = (
        0.13 * f(row, "complexity_diagnosis_gain")
        + 0.14 * f(row, "scenario_gain")
        + 0.14 * f(row, "feedback_gain")
        + 0.14 * f(row, "option_value_gain")
        + 0.14 * f(row, "learning_gain")
        + 0.12 * f(row, "resilience_gain")
        + 0.12 * f(row, "decision_memory_gain")
        - 0.08 * f(row, "process_cost")
        - 0.08 * f(row, "implementation_complexity")
        - 0.08 * f(row, "political_safety_need")
    )

    if f(row, "political_safety_need") >= 0.42:
        action = "requires_leadership_protection"
    elif intervention_value >= 0.55:
        action = "high_value_complexity_strategy_intervention"
    else:
        action = "supporting_intervention"

    intervention_rows.append(
        {
            "intervention_id": row["intervention_id"],
            "intervention_name": row["intervention_name"],
            "target_complexity_risk": row["target_complexity_risk"],
            "intervention_value_score": round(intervention_value, 4),
            "recommended_action": action,
            "process_cost": row["process_cost"],
            "implementation_complexity": row["implementation_complexity"],
            "complexity_diagnosis_gain": row["complexity_diagnosis_gain"],
            "scenario_gain": row["scenario_gain"],
            "feedback_gain": row["feedback_gain"],
            "option_value_gain": row["option_value_gain"],
            "learning_gain": row["learning_gain"],
            "resilience_gain": row["resilience_gain"],
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
        "target_complexity_risk",
        "intervention_value_score",
        "recommended_action",
        "process_cost",
        "implementation_complexity",
        "complexity_diagnosis_gain",
        "scenario_gain",
        "feedback_gain",
        "option_value_gain",
        "learning_gain",
        "resilience_gain",
        "decision_memory_gain",
        "political_safety_need",
    ],
)

# ---------------------------------------------------------------------
# 11. Strategist report
# ---------------------------------------------------------------------

top_environments = environment_rows[:5]
highest_uncertainty = uncertainty_rows[:5]
highest_feedback = feedback_rows[:5]
highest_adaptation = actor_rows[:5]
highest_lock_in = path_rows[:5]
highest_scenario = scenario_rows[:5]
top_options = option_rows[:6]
top_indicators = indicator_rows[:6]
weak_learning = sorted(learning_rows, key=lambda item: item["learning_quality_score"])[:5]
top_interventions = intervention_rows[:6]

report: list[str] = []

report.append("# Complex Systems and Strategic Uncertainty Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic separates complexity profile, linear-planning risk, uncertainty intensity, feedback risk, adaptive actor risk, "
    "path-dependence lock-in risk, scenario robustness gaps, adaptive option value, early-warning indicator quality, learning-loop quality, "
    "and intervention priority. The purpose is to help strategists decide when conventional planning is insufficient and when strategy "
    "requires scenarios, adaptive pathways, option portfolios, sensing, learning loops, and decision memory."
)
report.append("")
report.append("## Most complex strategic environments")
report.append("")

for item in top_environments:
    report.append(
        f"- **{item['environment_id']} — {item['environment_name']}**: complexity score {item['complexity_profile_score']}; "
        f"diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest structural uncertainty drivers")
report.append("")

for item in highest_uncertainty:
    report.append(
        f"- **{item['driver_id']} — {item['driver_name']}** in **{item['environment_name']}**: "
        f"uncertainty intensity {item['uncertainty_intensity_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Feedback loops requiring attention")
report.append("")

for item in highest_feedback:
    report.append(
        f"- **{item['loop_id']} — {item['loop_name']}** in **{item['environment_name']}**: "
        f"feedback risk {item['feedback_risk_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Adaptive actors most likely to change the game")
report.append("")

for item in highest_adaptation:
    report.append(
        f"- **{item['actor_id']} — {item['actor_group']}** in **{item['environment_name']}**: "
        f"adaptation risk {item['adaptation_risk_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest path-dependence and lock-in risks")
report.append("")

for item in highest_lock_in:
    report.append(
        f"- **{item['path_id']} — {item['path_factor']}** in **{item['environment_name']}**: "
        f"lock-in risk {item['lock_in_risk_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Scenarios with the largest robustness gaps")
report.append("")

for item in highest_scenario:
    report.append(
        f"- **{item['scenario_id']} — {item['scenario_name']}** in **{item['environment_name']}**: "
        f"scenario risk {item['scenario_risk_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest-value adaptive options")
report.append("")

for item in top_options:
    report.append(
        f"- **{item['option_id']} — {item['option_name']}** ({item['option_type']}): "
        f"option value {item['adaptive_option_value_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strongest early-warning indicators")
report.append("")

for item in top_indicators:
    report.append(
        f"- **{item['indicator_id']} — {item['indicator_name']}** in **{item['environment_name']}**: "
        f"indicator quality {item['indicator_quality_score']}; trigger threshold: {item['trigger_threshold']}."
    )

report.append("")
report.append("## Learning loops needing repair")
report.append("")

for item in weak_learning:
    report.append(
        f"- **{item['learning_id']} — {item['learning_loop_name']}** in **{item['environment_name']}**: "
        f"learning quality {item['learning_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest-value complexity strategy interventions")
report.append("")

for item in top_interventions:
    report.append(
        f"- **{item['intervention_id']} — {item['intervention_name']}**: value {item['intervention_value_score']}; "
        f"target: {item['target_complexity_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "The value of this workflow is disciplined action under uncertainty. It helps teams avoid linear causality bias, single-forecast dependence, "
    "local optimization, scale confusion, complexity paralysis, vague complexity language, adaptive actor blindness, and learning-loop failure. "
    "It supports complexity-aware strategy as a practical discipline: classify the environment, map interdependence, identify feedback, anticipate adaptation, "
    "review path dependence, stress-test scenarios, design adaptive options, monitor early-warning indicators, and preserve decision memory."
)

(REPORTS / "complexity_strategy_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_environments": top_environments,
    "highest_uncertainty": highest_uncertainty,
    "highest_feedback": highest_feedback,
    "highest_adaptation": highest_adaptation,
    "highest_lock_in": highest_lock_in,
    "highest_scenario": highest_scenario,
    "top_options": top_options,
    "top_indicators": top_indicators,
    "weak_learning": weak_learning,
    "top_interventions": top_interventions,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced complexity strategy diagnostics complete.")
print(f"Wrote: {TABLES / 'complexity_profile_scores.csv'}")
print(f"Wrote: {TABLES / 'uncertainty_driver_review.csv'}")
print(f"Wrote: {TABLES / 'feedback_loop_review.csv'}")
print(f"Wrote: {TABLES / 'adaptive_actor_review.csv'}")
print(f"Wrote: {TABLES / 'path_dependence_review.csv'}")
print(f"Wrote: {TABLES / 'scenario_robustness_review.csv'}")
print(f"Wrote: {TABLES / 'adaptive_option_review.csv'}")
print(f"Wrote: {TABLES / 'early_warning_indicator_review.csv'}")
print(f"Wrote: {TABLES / 'learning_loop_review.csv'}")
print(f"Wrote: {TABLES / 'intervention_recommendations.csv'}")
print(f"Wrote: {REPORTS / 'complexity_strategy_diagnostic_report.md'}")
