#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for leverage points in systems change.

This dependency-light workflow uses only the Python standard library.

It produces:
- leverage point scores
- feedback leverage review
- information-flow review
- rule and incentive review
- system-goal review
- paradigm review
- tipping threshold review
- governance-need review
- early-warning indicator review
- learning-loop review
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


leverage_points = read_csv(RAW / "leverage_points.csv")
feedback = read_csv(RAW / "feedback_leverage.csv")
information = read_csv(RAW / "information_flows.csv")
rules = read_csv(RAW / "rules_incentives.csv")
goals = read_csv(RAW / "system_goals.csv")
paradigms = read_csv(RAW / "paradigms.csv")
thresholds = read_csv(RAW / "tipping_thresholds.csv")
governance = read_csv(RAW / "governance_needs.csv")
indicators = read_csv(RAW / "early_warning_indicators.csv")
learning = read_csv(RAW / "learning_loops.csv")

leverage_names = {row["leverage_id"]: row["intervention_name"] for row in leverage_points}

# ---------------------------------------------------------------------
# 1. Leverage point scoring
# ---------------------------------------------------------------------

leverage_rows: list[dict[str, object]] = []

for row in leverage_points:
    leverage_profile = (
        0.06 * f(row, "implementation_ease")
        + 0.16 * f(row, "structural_depth")
        + 0.14 * f(row, "system_sensitivity")
        + 0.13 * f(row, "feedback_influence")
        + 0.11 * f(row, "information_effect")
        + 0.13 * f(row, "rule_power")
        + 0.13 * f(row, "goal_alignment")
        + 0.08 * f(row, "paradigm_relevance")
        + 0.14 * f(row, "transformative_potential")
        + 0.08 * f(row, "learning_capacity")
        - 0.06 * f(row, "unintended_consequence_risk")
    )

    governance_need = (
        0.26 * f(row, "legitimacy_requirement")
        + 0.24 * f(row, "unintended_consequence_risk")
        + 0.22 * f(row, "transformative_potential")
        + 0.14 * (1 - f(row, "implementation_ease"))
        + 0.14 * f(row, "paradigm_relevance")
    )

    shallow_but_easy = f(row, "implementation_ease") >= 0.70 and f(row, "structural_depth") <= 0.45
    high_leverage_high_governance = leverage_profile >= 0.72 and governance_need >= 0.68

    if high_leverage_high_governance:
        diagnosis = "high_leverage_high_governance_need"
    elif leverage_profile >= 0.68:
        diagnosis = "high_leverage_candidate"
    elif shallow_but_easy:
        diagnosis = "easy_but_shallow"
    elif f(row, "feedback_influence") >= 0.75:
        diagnosis = "feedback_sensitive_candidate"
    elif f(row, "information_effect") >= 0.80:
        diagnosis = "information_flow_candidate"
    else:
        diagnosis = "moderate_leverage_review"

    leverage_rows.append(
        {
            "leverage_id": row["leverage_id"],
            "intervention_name": row["intervention_name"],
            "leverage_level": row["leverage_level"],
            "domain": row["domain"],
            "leverage_profile_score": round(leverage_profile, 4),
            "governance_need_score": round(governance_need, 4),
            "diagnosis": diagnosis,
            "implementation_ease": row["implementation_ease"],
            "structural_depth": row["structural_depth"],
            "system_sensitivity": row["system_sensitivity"],
            "feedback_influence": row["feedback_influence"],
            "information_effect": row["information_effect"],
            "rule_power": row["rule_power"],
            "goal_alignment": row["goal_alignment"],
            "paradigm_relevance": row["paradigm_relevance"],
            "transformative_potential": row["transformative_potential"],
            "legitimacy_requirement": row["legitimacy_requirement"],
            "unintended_consequence_risk": row["unintended_consequence_risk"],
            "learning_capacity": row["learning_capacity"],
            "description": row["description"],
        }
    )

leverage_rows.sort(key=lambda item: item["leverage_profile_score"], reverse=True)

leverage_fields = [
    "leverage_id",
    "intervention_name",
    "leverage_level",
    "domain",
    "leverage_profile_score",
    "governance_need_score",
    "diagnosis",
    "implementation_ease",
    "structural_depth",
    "system_sensitivity",
    "feedback_influence",
    "information_effect",
    "rule_power",
    "goal_alignment",
    "paradigm_relevance",
    "transformative_potential",
    "legitimacy_requirement",
    "unintended_consequence_risk",
    "learning_capacity",
    "description",
]

write_csv(TABLES / "leverage_point_scores.csv", leverage_rows, leverage_fields)
write_csv(PROCESSED / "leverage_point_scores.csv", leverage_rows, leverage_fields)

# ---------------------------------------------------------------------
# 2. Feedback leverage review
# ---------------------------------------------------------------------

feedback_rows: list[dict[str, object]] = []

for row in feedback:
    feedback_leverage = (
        0.14 * f(row, "loop_strength")
        + 0.12 * f(row, "current_visibility")
        + 0.16 * f(row, "reinforcing_potential")
        + 0.12 * f(row, "balancing_capacity")
        - 0.10 * f(row, "delay_risk")
        + 0.10 * f(row, "intervention_readiness")
        + 0.18 * f(row, "positive_cascade_potential")
        - 0.10 * f(row, "policy_resistance_risk")
    )

    if f(row, "policy_resistance_risk") >= 0.65:
        action = "policy_resistance_governance_required"
    elif feedback_leverage >= 0.60:
        action = "high_value_feedback_leverage"
    elif f(row, "current_visibility") < 0.50:
        action = "make_loop_visible_before_intervening"
    else:
        action = "monitor_feedback_leverage"

    feedback_rows.append(
        {
            "feedback_id": row["feedback_id"],
            "leverage_id": row["leverage_id"],
            "intervention_name": leverage_names.get(row["leverage_id"], row["leverage_id"]),
            "loop_name": row["loop_name"],
            "loop_type": row["loop_type"],
            "feedback_leverage_score": round(feedback_leverage, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "loop_strength": row["loop_strength"],
            "current_visibility": row["current_visibility"],
            "reinforcing_potential": row["reinforcing_potential"],
            "balancing_capacity": row["balancing_capacity"],
            "delay_risk": row["delay_risk"],
            "intervention_readiness": row["intervention_readiness"],
            "positive_cascade_potential": row["positive_cascade_potential"],
            "policy_resistance_risk": row["policy_resistance_risk"],
        }
    )

feedback_rows.sort(key=lambda item: item["feedback_leverage_score"], reverse=True)

write_csv(
    TABLES / "feedback_leverage_review.csv",
    feedback_rows,
    [
        "feedback_id",
        "leverage_id",
        "intervention_name",
        "loop_name",
        "loop_type",
        "feedback_leverage_score",
        "recommended_action",
        "source_review_action",
        "loop_strength",
        "current_visibility",
        "reinforcing_potential",
        "balancing_capacity",
        "delay_risk",
        "intervention_readiness",
        "positive_cascade_potential",
        "policy_resistance_risk",
    ],
)

# ---------------------------------------------------------------------
# 3. Information-flow review
# ---------------------------------------------------------------------

information_rows: list[dict[str, object]] = []

for row in information:
    information_value = (
        0.15 * f(row, "visibility_gain")
        + 0.14 * f(row, "signal_quality")
        + 0.15 * f(row, "decision_linkage")
        + 0.12 * f(row, "stakeholder_access")
        + 0.12 * f(row, "delay_reduction")
        + 0.12 * f(row, "context_quality")
        - 0.10 * f(row, "gaming_risk")
        - 0.08 * f(row, "data_burden")
    )

    if information_value >= 0.60:
        action = "high_value_information_leverage"
    elif f(row, "gaming_risk") >= 0.55:
        action = "add_countermetrics_and_learning_governance"
    elif f(row, "decision_linkage") < 0.60:
        action = "connect_information_to_decision_rights"
    else:
        action = "monitor_information_flow"

    information_rows.append(
        {
            "flow_id": row["flow_id"],
            "leverage_id": row["leverage_id"],
            "intervention_name": leverage_names.get(row["leverage_id"], row["leverage_id"]),
            "flow_name": row["flow_name"],
            "flow_type": row["flow_type"],
            "information_value_score": round(information_value, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "visibility_gain": row["visibility_gain"],
            "signal_quality": row["signal_quality"],
            "decision_linkage": row["decision_linkage"],
            "stakeholder_access": row["stakeholder_access"],
            "delay_reduction": row["delay_reduction"],
            "context_quality": row["context_quality"],
            "gaming_risk": row["gaming_risk"],
            "data_burden": row["data_burden"],
        }
    )

information_rows.sort(key=lambda item: item["information_value_score"], reverse=True)

write_csv(
    TABLES / "information_flow_review.csv",
    information_rows,
    [
        "flow_id",
        "leverage_id",
        "intervention_name",
        "flow_name",
        "flow_type",
        "information_value_score",
        "recommended_action",
        "source_review_action",
        "visibility_gain",
        "signal_quality",
        "decision_linkage",
        "stakeholder_access",
        "delay_reduction",
        "context_quality",
        "gaming_risk",
        "data_burden",
    ],
)

# ---------------------------------------------------------------------
# 4. Rule and incentive review
# ---------------------------------------------------------------------

rule_rows: list[dict[str, object]] = []

for row in rules:
    rule_leverage = (
        0.14 * f(row, "current_misalignment")
        + 0.18 * f(row, "behavioral_power")
        + 0.12 * f(row, "incentive_clarity")
        + 0.12 * f(row, "cross_boundary_effect")
        - 0.10 * f(row, "implementation_complexity")
        - 0.10 * f(row, "political_resistance")
        + 0.12 * f(row, "governance_readiness")
        + 0.12 * f(row, "countermetric_quality")
    )

    if rule_leverage >= 0.58 and f(row, "political_resistance") >= 0.65:
        action = "high_leverage_requires_coalition"
    elif rule_leverage >= 0.58:
        action = "priority_rule_or_incentive_leverage"
    elif f(row, "countermetric_quality") < 0.55:
        action = "add_countermetrics_before_scale"
    else:
        action = "monitor_rule_design"

    rule_rows.append(
        {
            "rule_id": row["rule_id"],
            "leverage_id": row["leverage_id"],
            "intervention_name": leverage_names.get(row["leverage_id"], row["leverage_id"]),
            "rule_name": row["rule_name"],
            "rule_type": row["rule_type"],
            "rule_leverage_score": round(rule_leverage, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "current_misalignment": row["current_misalignment"],
            "behavioral_power": row["behavioral_power"],
            "incentive_clarity": row["incentive_clarity"],
            "cross_boundary_effect": row["cross_boundary_effect"],
            "implementation_complexity": row["implementation_complexity"],
            "political_resistance": row["political_resistance"],
            "governance_readiness": row["governance_readiness"],
            "countermetric_quality": row["countermetric_quality"],
        }
    )

rule_rows.sort(key=lambda item: item["rule_leverage_score"], reverse=True)

write_csv(
    TABLES / "rule_incentive_review.csv",
    rule_rows,
    [
        "rule_id",
        "leverage_id",
        "intervention_name",
        "rule_name",
        "rule_type",
        "rule_leverage_score",
        "recommended_action",
        "source_review_action",
        "current_misalignment",
        "behavioral_power",
        "incentive_clarity",
        "cross_boundary_effect",
        "implementation_complexity",
        "political_resistance",
        "governance_readiness",
        "countermetric_quality",
    ],
)

# ---------------------------------------------------------------------
# 5. System-goal review
# ---------------------------------------------------------------------

goal_rows: list[dict[str, object]] = []

for row in goals:
    goal_change_need = (
        0.20 * f(row, "goal_misalignment")
        - 0.10 * f(row, "metric_alignment")
        - 0.10 * f(row, "budget_alignment")
        - 0.10 * f(row, "decision_right_alignment")
        + 0.12 * (1 - f(row, "tradeoff_clarity"))
        + 0.12 * f(row, "stakeholder_legitimacy")
        + 0.12 * (1 - f(row, "long_term_orientation"))
        + 0.10 * f(row, "revision_readiness")
    )

    if f(row, "goal_misalignment") >= 0.80:
        action = "operating_goal_diagnosis_required"
    elif goal_change_need >= 0.35:
        action = "align_metrics_budget_and_decision_rights"
    else:
        action = "monitor_goal_alignment"

    goal_rows.append(
        {
            "goal_id": row["goal_id"],
            "leverage_id": row["leverage_id"],
            "intervention_name": leverage_names.get(row["leverage_id"], row["leverage_id"]),
            "stated_goal": row["stated_goal"],
            "operating_goal": row["operating_goal"],
            "goal_change_need_score": round(goal_change_need, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "goal_misalignment": row["goal_misalignment"],
            "metric_alignment": row["metric_alignment"],
            "budget_alignment": row["budget_alignment"],
            "decision_right_alignment": row["decision_right_alignment"],
            "tradeoff_clarity": row["tradeoff_clarity"],
            "stakeholder_legitimacy": row["stakeholder_legitimacy"],
            "long_term_orientation": row["long_term_orientation"],
            "revision_readiness": row["revision_readiness"],
        }
    )

goal_rows.sort(key=lambda item: item["goal_change_need_score"], reverse=True)

write_csv(
    TABLES / "system_goal_review.csv",
    goal_rows,
    [
        "goal_id",
        "leverage_id",
        "intervention_name",
        "stated_goal",
        "operating_goal",
        "goal_change_need_score",
        "recommended_action",
        "source_review_action",
        "goal_misalignment",
        "metric_alignment",
        "budget_alignment",
        "decision_right_alignment",
        "tradeoff_clarity",
        "stakeholder_legitimacy",
        "long_term_orientation",
        "revision_readiness",
    ],
)

# ---------------------------------------------------------------------
# 6. Paradigm review
# ---------------------------------------------------------------------

paradigm_rows: list[dict[str, object]] = []

for row in paradigms:
    paradigm_transition_readiness = (
        0.10 * f(row, "assumption_visibility")
        - 0.12 * f(row, "paradigm_lock_in")
        + 0.16 * f(row, "conceptual_clarity")
        + 0.16 * f(row, "coalition_strength")
        + 0.16 * f(row, "evidence_base")
        + 0.18 * f(row, "transition_pathway_quality")
        + 0.16 * f(row, "practice_embedding")
    )

    paradigm_risk = (
        0.24 * f(row, "paradigm_lock_in")
        - 0.12 * f(row, "assumption_visibility")
        - 0.16 * f(row, "conceptual_clarity")
        - 0.16 * f(row, "coalition_strength")
        - 0.16 * f(row, "transition_pathway_quality")
        - 0.16 * f(row, "practice_embedding")
    )

    if paradigm_transition_readiness >= 0.55:
        action = "paradigm_shift_has_practical_pathway"
    elif paradigm_risk >= 0.20:
        action = "build_conceptual_clarity_coalition_and_practice"
    else:
        action = "continue_paradigm_review"

    paradigm_rows.append(
        {
            "paradigm_id": row["paradigm_id"],
            "leverage_id": row["leverage_id"],
            "intervention_name": leverage_names.get(row["leverage_id"], row["leverage_id"]),
            "paradigm_name": row["paradigm_name"],
            "current_assumption": row["current_assumption"],
            "alternative_frame": row["alternative_frame"],
            "paradigm_transition_readiness": round(paradigm_transition_readiness, 4),
            "paradigm_transition_risk": round(paradigm_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "assumption_visibility": row["assumption_visibility"],
            "paradigm_lock_in": row["paradigm_lock_in"],
            "conceptual_clarity": row["conceptual_clarity"],
            "coalition_strength": row["coalition_strength"],
            "evidence_base": row["evidence_base"],
            "transition_pathway_quality": row["transition_pathway_quality"],
            "practice_embedding": row["practice_embedding"],
        }
    )

paradigm_rows.sort(key=lambda item: item["paradigm_transition_risk"], reverse=True)

write_csv(
    TABLES / "paradigm_review.csv",
    paradigm_rows,
    [
        "paradigm_id",
        "leverage_id",
        "intervention_name",
        "paradigm_name",
        "current_assumption",
        "alternative_frame",
        "paradigm_transition_readiness",
        "paradigm_transition_risk",
        "recommended_action",
        "source_review_action",
        "assumption_visibility",
        "paradigm_lock_in",
        "conceptual_clarity",
        "coalition_strength",
        "evidence_base",
        "transition_pathway_quality",
        "practice_embedding",
    ],
)

# ---------------------------------------------------------------------
# 7. Tipping threshold review
# ---------------------------------------------------------------------

threshold_rows: list[dict[str, object]] = []

for row in thresholds:
    distance_to_threshold = max(0.0, f(row, "threshold_level") - f(row, "current_progress"))

    tipping_readiness = (
        0.12 * (1 - distance_to_threshold)
        + 0.14 * f(row, "diffusion_potential")
        + 0.16 * f(row, "self_reinforcement_strength")
        + 0.14 * f(row, "complementary_condition_quality")
        + 0.14 * f(row, "legitimacy_support")
        + 0.14 * f(row, "infrastructure_support")
        + 0.12 * f(row, "monitoring_quality")
    )

    if tipping_readiness >= 0.68 and distance_to_threshold <= 0.25:
        action = "near_positive_tipping_candidate"
    elif f(row, "complementary_condition_quality") < 0.55:
        action = "build_complementary_conditions"
    elif f(row, "legitimacy_support") < 0.55:
        action = "strengthen_legitimacy_support"
    else:
        action = "monitor_threshold_progress"

    threshold_rows.append(
        {
            "threshold_id": row["threshold_id"],
            "leverage_id": row["leverage_id"],
            "intervention_name": leverage_names.get(row["leverage_id"], row["leverage_id"]),
            "threshold_name": row["threshold_name"],
            "threshold_type": row["threshold_type"],
            "distance_to_threshold": round(distance_to_threshold, 4),
            "tipping_readiness_score": round(tipping_readiness, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "current_progress": row["current_progress"],
            "threshold_level": row["threshold_level"],
            "diffusion_potential": row["diffusion_potential"],
            "self_reinforcement_strength": row["self_reinforcement_strength"],
            "complementary_condition_quality": row["complementary_condition_quality"],
            "legitimacy_support": row["legitimacy_support"],
            "infrastructure_support": row["infrastructure_support"],
            "monitoring_quality": row["monitoring_quality"],
        }
    )

threshold_rows.sort(key=lambda item: item["tipping_readiness_score"], reverse=True)

write_csv(
    TABLES / "tipping_threshold_review.csv",
    threshold_rows,
    [
        "threshold_id",
        "leverage_id",
        "intervention_name",
        "threshold_name",
        "threshold_type",
        "distance_to_threshold",
        "tipping_readiness_score",
        "recommended_action",
        "source_review_action",
        "current_progress",
        "threshold_level",
        "diffusion_potential",
        "self_reinforcement_strength",
        "complementary_condition_quality",
        "legitimacy_support",
        "infrastructure_support",
        "monitoring_quality",
    ],
)

# ---------------------------------------------------------------------
# 8. Governance need review
# ---------------------------------------------------------------------

governance_rows: list[dict[str, object]] = []

for row in governance:
    governance_need_score = (
        0.14 * f(row, "legitimacy_requirement")
        + 0.14 * f(row, "unintended_consequence_risk")
        + 0.13 * f(row, "implementation_complexity")
        + 0.14 * f(row, "monitoring_need")
        + 0.13 * f(row, "stakeholder_inclusion_need")
        + 0.12 * f(row, "decision_memory_need")
        - 0.08 * f(row, "revision_trigger_clarity")
        - 0.10 * f(row, "current_governance_capacity")
    )

    if governance_need_score >= 0.50:
        action = "strengthen_governance_before_scale"
    elif f(row, "revision_trigger_clarity") < 0.50:
        action = "define_revision_triggers"
    elif f(row, "current_governance_capacity") < 0.50:
        action = "build_governance_capacity"
    else:
        action = "governance_ready_with_monitoring"

    governance_rows.append(
        {
            "governance_id": row["governance_id"],
            "leverage_id": row["leverage_id"],
            "intervention_name": leverage_names.get(row["leverage_id"], row["leverage_id"]),
            "governance_focus": row["governance_focus"],
            "governance_need_score": round(governance_need_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "legitimacy_requirement": row["legitimacy_requirement"],
            "unintended_consequence_risk": row["unintended_consequence_risk"],
            "implementation_complexity": row["implementation_complexity"],
            "monitoring_need": row["monitoring_need"],
            "stakeholder_inclusion_need": row["stakeholder_inclusion_need"],
            "decision_memory_need": row["decision_memory_need"],
            "revision_trigger_clarity": row["revision_trigger_clarity"],
            "current_governance_capacity": row["current_governance_capacity"],
        }
    )

governance_rows.sort(key=lambda item: item["governance_need_score"], reverse=True)

write_csv(
    TABLES / "governance_need_review.csv",
    governance_rows,
    [
        "governance_id",
        "leverage_id",
        "intervention_name",
        "governance_focus",
        "governance_need_score",
        "recommended_action",
        "source_review_action",
        "legitimacy_requirement",
        "unintended_consequence_risk",
        "implementation_complexity",
        "monitoring_need",
        "stakeholder_inclusion_need",
        "decision_memory_need",
        "revision_trigger_clarity",
        "current_governance_capacity",
    ],
)

# ---------------------------------------------------------------------
# 9. Early-warning indicator review
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
    elif f(row, "decision_linkage") < 0.60:
        action = "connect_signal_to_revision_trigger"
    elif f(row, "visibility") < 0.55:
        action = "improve_signal_visibility"
    else:
        action = "develop_indicator"

    indicator_rows.append(
        {
            "indicator_id": row["indicator_id"],
            "leverage_id": row["leverage_id"],
            "intervention_name": leverage_names.get(row["leverage_id"], row["leverage_id"]),
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
        "leverage_id",
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
# 10. Learning-loop review
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

    if learning_quality >= 0.60:
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
            "leverage_id": row["leverage_id"],
            "intervention_name": leverage_names.get(row["leverage_id"], row["leverage_id"]),
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

learning_rows.sort(key=lambda item: item["learning_quality_score"], reverse=True)

write_csv(
    TABLES / "learning_loop_review.csv",
    learning_rows,
    [
        "learning_id",
        "leverage_id",
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
# 11. Strategist report
# ---------------------------------------------------------------------

top_leverage = leverage_rows[:6]
easy_shallow = [row for row in leverage_rows if row["diagnosis"] == "easy_but_shallow"]
top_feedback = feedback_rows[:5]
top_information = information_rows[:5]
top_rules = rule_rows[:5]
highest_goal_need = goal_rows[:5]
highest_paradigm_risk = paradigm_rows[:5]
top_thresholds = threshold_rows[:5]
highest_governance_need = governance_rows[:5]
top_indicators = indicator_rows[:6]
top_learning = learning_rows[:5]

report: list[str] = []

report.append("# Leverage Points in Systems Change Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic compares intervention points by structural depth, system sensitivity, feedback influence, information effect, rule power, "
    "goal alignment, paradigm relevance, transformative potential, governance need, unintended-consequence risk, tipping readiness, early-warning "
    "signals, and learning-loop quality. The purpose is to help strategists distinguish visible activity from structurally intelligent intervention."
)
report.append("")
report.append("## Highest leverage candidates")
report.append("")

for item in top_leverage:
    report.append(
        f"- **{item['leverage_id']} — {item['intervention_name']}** ({item['leverage_level']}): "
        f"leverage score {item['leverage_profile_score']}; governance need {item['governance_need_score']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Easy but shallow interventions")
report.append("")

if easy_shallow:
    for item in easy_shallow:
        report.append(
            f"- **{item['leverage_id']} — {item['intervention_name']}**: implementation ease {item['implementation_ease']}; "
            f"structural depth {item['structural_depth']}. Use only when surface adjustment is sufficient or as a bridge to deeper change."
        )
else:
    report.append("- No interventions were classified as easy but shallow.")

report.append("")
report.append("## Feedback leverage opportunities")
report.append("")

for item in top_feedback:
    report.append(
        f"- **{item['feedback_id']} — {item['loop_name']}** for **{item['intervention_name']}**: "
        f"feedback leverage {item['feedback_leverage_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Information-flow leverage opportunities")
report.append("")

for item in top_information:
    report.append(
        f"- **{item['flow_id']} — {item['flow_name']}** for **{item['intervention_name']}**: "
        f"information value {item['information_value_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Rule and incentive leverage opportunities")
report.append("")

for item in top_rules:
    report.append(
        f"- **{item['rule_id']} — {item['rule_name']}** for **{item['intervention_name']}**: "
        f"rule leverage {item['rule_leverage_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Operating-goal misalignment priorities")
report.append("")

for item in highest_goal_need:
    report.append(
        f"- **{item['goal_id']} — {item['intervention_name']}**: stated goal **{item['stated_goal']}**; "
        f"operating goal **{item['operating_goal']}**; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Paradigm transition risks")
report.append("")

for item in highest_paradigm_risk:
    report.append(
        f"- **{item['paradigm_id']} — {item['paradigm_name']}** for **{item['intervention_name']}**: "
        f"transition risk {item['paradigm_transition_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Positive tipping threshold candidates")
report.append("")

for item in top_thresholds:
    report.append(
        f"- **{item['threshold_id']} — {item['threshold_name']}** for **{item['intervention_name']}**: "
        f"tipping readiness {item['tipping_readiness_score']}; distance to threshold {item['distance_to_threshold']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Governance needs before scale")
report.append("")

for item in highest_governance_need:
    report.append(
        f"- **{item['governance_id']} — {item['governance_focus']}** for **{item['intervention_name']}**: "
        f"governance need {item['governance_need_score']}; action: {item['recommended_action']}."
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
report.append("## Strongest learning loops")
report.append("")

for item in top_learning:
    report.append(
        f"- **{item['learning_id']} — {item['learning_loop_name']}** for **{item['intervention_name']}**: "
        f"learning quality {item['learning_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "Leverage-point strategy is not a search for the largest intervention. It is a search for structurally intelligent placement. "
    "A strong leverage hypothesis names the recurring pattern, classifies the intervention level, identifies the feedback or rule structure being changed, "
    "reviews operating goals and paradigms, tests second-order effects, monitors tipping thresholds, and preserves decision memory so the strategy can learn."
)

(REPORTS / "leverage_point_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_leverage": top_leverage,
    "easy_shallow": easy_shallow,
    "top_feedback": top_feedback,
    "top_information": top_information,
    "top_rules": top_rules,
    "highest_goal_need": highest_goal_need,
    "highest_paradigm_risk": highest_paradigm_risk,
    "top_thresholds": top_thresholds,
    "highest_governance_need": highest_governance_need,
    "top_indicators": top_indicators,
    "top_learning": top_learning,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced leverage-point diagnostics complete.")
print(f"Wrote: {TABLES / 'leverage_point_scores.csv'}")
print(f"Wrote: {TABLES / 'feedback_leverage_review.csv'}")
print(f"Wrote: {TABLES / 'information_flow_review.csv'}")
print(f"Wrote: {TABLES / 'rule_incentive_review.csv'}")
print(f"Wrote: {TABLES / 'system_goal_review.csv'}")
print(f"Wrote: {TABLES / 'paradigm_review.csv'}")
print(f"Wrote: {TABLES / 'tipping_threshold_review.csv'}")
print(f"Wrote: {TABLES / 'governance_need_review.csv'}")
print(f"Wrote: {TABLES / 'early_warning_indicator_review.csv'}")
print(f"Wrote: {TABLES / 'learning_loop_review.csv'}")
print(f"Wrote: {REPORTS / 'leverage_point_diagnostic_report.md'}")
