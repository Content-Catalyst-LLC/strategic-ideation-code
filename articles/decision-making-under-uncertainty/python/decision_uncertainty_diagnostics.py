#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Decision-Making Under Uncertainty.

This dependency-light workflow uses only the Python standard library.

It produces:
- decision option scores
- uncertainty classification scores
- assumption risk scores
- scenario stress-test scores
- option value scores
- experiment design scores
- heuristic and bias scores
- ethical uncertainty scores
- decision governance scores
- decision learning-memory scores
- a markdown strategist diagnostic report
"""

from __future__ import annotations

import csv
import json
import math
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


options = read_csv(RAW / "decision_options.csv")
uncertainties = read_csv(RAW / "uncertainty_classifications.csv")
assumptions = read_csv(RAW / "assumption_register.csv")
stress_tests = read_csv(RAW / "scenario_stress_tests.csv")
option_values = read_csv(RAW / "option_value_reviews.csv")
experiments = read_csv(RAW / "experiment_designs.csv")
biases = read_csv(RAW / "heuristic_bias_reviews.csv")
ethics = read_csv(RAW / "ethical_uncertainty.csv")
governance = read_csv(RAW / "decision_governance.csv")
memory = read_csv(RAW / "decision_learning_memory.csv")

option_names = {row["option_id"]: row["option_name"] for row in options}

# ---------------------------------------------------------------------
# 1. Decision option scoring
# ---------------------------------------------------------------------

option_rows: list[dict[str, object]] = []

for row in options:
    decision_profile = (
        0.14 * f(row, "expected_return")
        + 0.18 * f(row, "robustness")
        + 0.16 * f(row, "flexibility")
        + 0.12 * f(row, "information_quality")
        - 0.16 * f(row, "exposure")
        + 0.14 * f(row, "option_value")
        + 0.10 * f(row, "reversibility")
        + 0.08 * f(row, "implementation_readiness")
        + 0.10 * f(row, "ethical_resilience")
        + 0.10 * f(row, "learning_value")
    )

    fragility_risk = (
        0.24 * f(row, "exposure")
        + 0.18 * (1 - f(row, "robustness"))
        + 0.14 * (1 - f(row, "flexibility"))
        + 0.13 * (1 - f(row, "option_value"))
        + 0.12 * (1 - f(row, "reversibility"))
        + 0.10 * (1 - f(row, "ethical_resilience"))
        + 0.09 * (1 - f(row, "information_quality"))
    )

    if decision_profile >= 0.70:
        diagnosis = "strong_uncertainty_sensitive_option"
    elif fragility_risk >= 0.62:
        diagnosis = "high_fragility_under_uncertainty"
    elif f(row, "option_value") < 0.40:
        diagnosis = "low_option_value"
    elif f(row, "ethical_resilience") < 0.45:
        diagnosis = "ethical_resilience_gap"
    elif f(row, "learning_value") < 0.40:
        diagnosis = "low_learning_value"
    else:
        diagnosis = "developing_decision_option"

    option_rows.append(
        {
            "option_id": row["option_id"],
            "option_name": row["option_name"],
            "decision_frame": row["decision_frame"],
            "decision_profile_score": round(decision_profile, 4),
            "fragility_risk": round(fragility_risk, 4),
            "diagnosis": diagnosis,
            "expected_return": row["expected_return"],
            "robustness": row["robustness"],
            "flexibility": row["flexibility"],
            "information_quality": row["information_quality"],
            "exposure": row["exposure"],
            "option_value": row["option_value"],
            "reversibility": row["reversibility"],
            "implementation_readiness": row["implementation_readiness"],
            "ethical_resilience": row["ethical_resilience"],
            "learning_value": row["learning_value"],
            "description": row["description"],
        }
    )

option_rows.sort(key=lambda item: item["decision_profile_score"], reverse=True)
write_csv(TABLES / "decision_option_scores.csv", option_rows, list(option_rows[0].keys()))
write_csv(PROCESSED / "decision_option_scores.csv", option_rows, list(option_rows[0].keys()))

# ---------------------------------------------------------------------
# 2. Uncertainty classification scoring
# ---------------------------------------------------------------------

uncertainty_rows: list[dict[str, object]] = []

for row in uncertainties:
    classification_difficulty = (
        0.15 * (1 - f(row, "probability_clarity"))
        + 0.13 * (1 - f(row, "outcome_clarity"))
        + 0.13 * (1 - f(row, "causal_clarity"))
        + 0.12 * (1 - f(row, "interpretive_agreement"))
        + 0.17 * f(row, "system_complexity")
        + 0.14 * f(row, "stakes")
        + 0.08 * (1 - f(row, "reversibility"))
        + 0.08 * (1 - f(row, "evidence_quality"))
    )

    clarity_score = 1 - classification_difficulty

    if classification_difficulty >= 0.68:
        action = "use_deep_uncertainty_governance"
    elif row["uncertainty_type"] in ("ambiguity", "ambiguity_complexity"):
        action = "add_frame_and_stakeholder_review"
    elif row["uncertainty_type"] == "risk":
        action = "use_probabilistic_analysis_with_sensitivity"
    elif row["uncertainty_type"] == "complexity":
        action = "use_systems_experimentation"
    elif row["uncertainty_type"] == "ignorance":
        action = "use_horizon_scanning_and_challenge"
    else:
        action = "combine_scenarios_and_triggers"

    uncertainty_rows.append(
        {
            "uncertainty_id": row["uncertainty_id"],
            "option_id": row["option_id"],
            "option_name": option_names.get(row["option_id"], row["option_id"]),
            "uncertainty_type": row["uncertainty_type"],
            "classification_difficulty": round(classification_difficulty, 4),
            "clarity_score": round(clarity_score, 4),
            "recommended_action": action,
            "decision_logic": row["decision_logic"],
            "probability_clarity": row["probability_clarity"],
            "outcome_clarity": row["outcome_clarity"],
            "causal_clarity": row["causal_clarity"],
            "interpretive_agreement": row["interpretive_agreement"],
            "system_complexity": row["system_complexity"],
            "stakes": row["stakes"],
            "reversibility": row["reversibility"],
            "evidence_quality": row["evidence_quality"],
        }
    )

uncertainty_rows.sort(key=lambda item: item["classification_difficulty"], reverse=True)
write_csv(TABLES / "uncertainty_classification_scores.csv", uncertainty_rows, list(uncertainty_rows[0].keys()))

# ---------------------------------------------------------------------
# 3. Assumption risk scoring
# ---------------------------------------------------------------------

assumption_rows: list[dict[str, object]] = []

for row in assumptions:
    assumption_risk = (
        0.25 * f(row, "uncertainty")
        + 0.25 * f(row, "consequence")
        + 0.15 * (1 - f(row, "evidence_quality"))
        + 0.14 * f(row, "decay_risk")
        + 0.11 * (1 - f(row, "monitorability"))
        + 0.10 * (1 - f(row, "owner_clarity"))
    )

    if assumption_risk >= 0.70:
        action = "urgent_assumption_test_required"
    elif f(row, "monitorability") < 0.50:
        action = "define_monitoring_proxy"
    elif f(row, "owner_clarity") < 0.50:
        action = "assign_assumption_owner"
    elif f(row, "evidence_quality") < 0.50:
        action = "strengthen_evidence_base"
    else:
        action = "monitor_assumption"

    assumption_rows.append(
        {
            "assumption_id": row["assumption_id"],
            "option_id": row["option_id"],
            "option_name": option_names.get(row["option_id"], row["option_id"]),
            "assumption": row["assumption"],
            "assumption_risk": round(assumption_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "uncertainty": row["uncertainty"],
            "consequence": row["consequence"],
            "evidence_quality": row["evidence_quality"],
            "decay_risk": row["decay_risk"],
            "monitorability": row["monitorability"],
            "owner_clarity": row["owner_clarity"],
        }
    )

assumption_rows.sort(key=lambda item: item["assumption_risk"], reverse=True)
write_csv(TABLES / "assumption_risk_scores.csv", assumption_rows, list(assumption_rows[0].keys()))

# ---------------------------------------------------------------------
# 4. Scenario stress-test scoring
# ---------------------------------------------------------------------

scenario_cols = [
    "scenario_stable_growth",
    "scenario_tech_disruption",
    "scenario_environmental_stress",
    "scenario_regulatory_shift",
    "scenario_trust_crisis",
    "scenario_resource_constraint",
]

stress_rows: list[dict[str, object]] = []

for row in stress_tests:
    values = [f(row, col) for col in scenario_cols]
    mean_performance = sum(values) / len(values)
    worst_case = min(values)
    best_case = max(values)
    variance = sum((value - mean_performance) ** 2 for value in values) / len(values)
    volatility = math.sqrt(variance)

    robustness_score = (
        0.42 * worst_case
        + 0.30 * mean_performance
        - 0.18 * volatility
        + 0.10 * best_case
    )

    if robustness_score >= 0.70:
        action = "strong_cross_scenario_decision"
    elif worst_case < 0.45:
        action = "address_worst_case_exposure"
    elif volatility > 0.15:
        action = "reduce_scenario_volatility"
    else:
        action = "strengthen_robustness"

    stress_rows.append(
        {
            "test_id": row["test_id"],
            "option_id": row["option_id"],
            "option_name": option_names.get(row["option_id"], row["option_id"]),
            "mean_performance": round(mean_performance, 4),
            "worst_case": round(worst_case, 4),
            "best_case": round(best_case, 4),
            "volatility": round(volatility, 4),
            "robustness_score": round(robustness_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "scenario_stable_growth": row["scenario_stable_growth"],
            "scenario_tech_disruption": row["scenario_tech_disruption"],
            "scenario_environmental_stress": row["scenario_environmental_stress"],
            "scenario_regulatory_shift": row["scenario_regulatory_shift"],
            "scenario_trust_crisis": row["scenario_trust_crisis"],
            "scenario_resource_constraint": row["scenario_resource_constraint"],
        }
    )

stress_rows.sort(key=lambda item: item["robustness_score"], reverse=True)
write_csv(TABLES / "scenario_stress_test_scores.csv", stress_rows, list(stress_rows[0].keys()))

# ---------------------------------------------------------------------
# 5. Option value scoring
# ---------------------------------------------------------------------

option_value_rows: list[dict[str, object]] = []

for row in option_values:
    option_value_score = (
        0.18 * f(row, "learning_value")
        + 0.18 * f(row, "future_flexibility")
        + 0.15 * f(row, "reversibility")
        + 0.13 * f(row, "staged_commitment_quality")
        + 0.12 * f(row, "modularity")
        + 0.11 * f(row, "exit_path_quality")
        - 0.15 * f(row, "lock_in_cost")
        + 0.08 * f(row, "monitoring_quality")
    )

    lock_in_warning = (
        0.35 * f(row, "lock_in_cost")
        + 0.20 * (1 - f(row, "reversibility"))
        + 0.18 * (1 - f(row, "exit_path_quality"))
        + 0.15 * (1 - f(row, "modularity"))
        + 0.12 * (1 - f(row, "future_flexibility"))
    )

    if option_value_score >= 0.68:
        action = "strong_option_value"
    elif lock_in_warning >= 0.62:
        action = "reduce_lock_in_and_build_exit_path"
    elif f(row, "learning_value") < 0.45:
        action = "increase_learning_value"
    else:
        action = "strengthen_option_design"

    option_value_rows.append(
        {
            "review_id": row["review_id"],
            "option_id": row["option_id"],
            "option_name": option_names.get(row["option_id"], row["option_id"]),
            "option_value_score": round(option_value_score, 4),
            "lock_in_warning": round(lock_in_warning, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "learning_value": row["learning_value"],
            "future_flexibility": row["future_flexibility"],
            "reversibility": row["reversibility"],
            "staged_commitment_quality": row["staged_commitment_quality"],
            "modularity": row["modularity"],
            "exit_path_quality": row["exit_path_quality"],
            "lock_in_cost": row["lock_in_cost"],
            "monitoring_quality": row["monitoring_quality"],
        }
    )

option_value_rows.sort(key=lambda item: item["option_value_score"], reverse=True)
write_csv(TABLES / "option_value_scores.csv", option_value_rows, list(option_value_rows[0].keys()))

# ---------------------------------------------------------------------
# 6. Experiment design scoring
# ---------------------------------------------------------------------

experiment_rows: list[dict[str, object]] = []

for row in experiments:
    experiment_quality = (
        0.16 * f(row, "learning_question_quality")
        + 0.14 * f(row, "reversibility")
        + 0.14 * f(row, "exposure_control")
        + 0.15 * f(row, "evidence_quality")
        + 0.12 * f(row, "stakeholder_feedback_quality")
        + 0.14 * f(row, "scaling_trigger_clarity")
        + 0.15 * f(row, "decision_relevance")
    )

    if experiment_quality >= 0.72:
        action = "strong_learning_experiment"
    elif f(row, "exposure_control") < 0.50:
        action = "reduce_experiment_exposure"
    elif f(row, "scaling_trigger_clarity") < 0.50:
        action = "define_scaling_triggers"
    elif f(row, "learning_question_quality") < 0.55:
        action = "clarify_learning_question"
    else:
        action = "strengthen_experiment_design"

    experiment_rows.append(
        {
            "experiment_id": row["experiment_id"],
            "option_id": row["option_id"],
            "option_name": option_names.get(row["option_id"], row["option_id"]),
            "experiment_name": row["experiment_name"],
            "experiment_quality": round(experiment_quality, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "learning_question_quality": row["learning_question_quality"],
            "reversibility": row["reversibility"],
            "exposure_control": row["exposure_control"],
            "evidence_quality": row["evidence_quality"],
            "stakeholder_feedback_quality": row["stakeholder_feedback_quality"],
            "scaling_trigger_clarity": row["scaling_trigger_clarity"],
            "decision_relevance": row["decision_relevance"],
        }
    )

experiment_rows.sort(key=lambda item: item["experiment_quality"], reverse=True)
write_csv(TABLES / "experiment_design_scores.csv", experiment_rows, list(experiment_rows[0].keys()))

# ---------------------------------------------------------------------
# 7. Heuristic and bias scoring
# ---------------------------------------------------------------------

bias_rows: list[dict[str, object]] = []

for row in biases:
    bias_risk = (
        0.26 * f(row, "exposure_level")
        + 0.26 * f(row, "decision_influence")
        + 0.16 * (1 - f(row, "detectability"))
        + 0.16 * (1 - f(row, "mitigation_quality"))
        + 0.16 * (1 - f(row, "challenge_process_quality"))
    )

    if bias_risk >= 0.70:
        action = "urgent_bias_mitigation_required"
    elif f(row, "challenge_process_quality") < 0.50:
        action = "strengthen_challenge_process"
    elif f(row, "mitigation_quality") < 0.50:
        action = "add_bias_mitigation"
    else:
        action = "monitor_bias_risk"

    bias_rows.append(
        {
            "bias_id": row["bias_id"],
            "option_id": row["option_id"],
            "option_name": option_names.get(row["option_id"], row["option_id"]),
            "bias_or_heuristic": row["bias_or_heuristic"],
            "bias_risk": round(bias_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "exposure_level": row["exposure_level"],
            "decision_influence": row["decision_influence"],
            "detectability": row["detectability"],
            "mitigation_quality": row["mitigation_quality"],
            "challenge_process_quality": row["challenge_process_quality"],
        }
    )

bias_rows.sort(key=lambda item: item["bias_risk"], reverse=True)
write_csv(TABLES / "heuristic_bias_scores.csv", bias_rows, list(bias_rows[0].keys()))

# ---------------------------------------------------------------------
# 8. Ethical uncertainty scoring
# ---------------------------------------------------------------------

ethics_rows: list[dict[str, object]] = []

for row in ethics:
    ethics_score = (
        0.14 * f(row, "transparency")
        + 0.15 * f(row, "burden_shift_review")
        + 0.15 * f(row, "stakeholder_representation")
        + 0.14 * f(row, "accountability")
        + 0.14 * f(row, "revisability")
        + 0.14 * f(row, "precaution_quality")
        + 0.14 * f(row, "redress_path_quality")
    )

    ethics_risk = 1 - ethics_score

    if ethics_score >= 0.74:
        action = "strong_ethical_uncertainty_review"
    elif f(row, "burden_shift_review") < 0.45:
        action = "review_burden_shifting"
    elif f(row, "stakeholder_representation") < 0.45:
        action = "expand_stakeholder_representation"
    elif f(row, "redress_path_quality") < 0.45:
        action = "define_redress_path"
    else:
        action = "strengthen_ethics_review"

    ethics_rows.append(
        {
            "ethics_id": row["ethics_id"],
            "option_id": row["option_id"],
            "option_name": option_names.get(row["option_id"], row["option_id"]),
            "ethical_issue": row["ethical_issue"],
            "ethical_uncertainty_score": round(ethics_score, 4),
            "ethical_uncertainty_risk": round(ethics_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "transparency": row["transparency"],
            "burden_shift_review": row["burden_shift_review"],
            "stakeholder_representation": row["stakeholder_representation"],
            "accountability": row["accountability"],
            "revisability": row["revisability"],
            "precaution_quality": row["precaution_quality"],
            "redress_path_quality": row["redress_path_quality"],
        }
    )

ethics_rows.sort(key=lambda item: item["ethical_uncertainty_risk"], reverse=True)
write_csv(TABLES / "ethical_uncertainty_scores.csv", ethics_rows, list(ethics_rows[0].keys()))

# ---------------------------------------------------------------------
# 9. Decision governance scoring
# ---------------------------------------------------------------------

governance_rows: list[dict[str, object]] = []

for row in governance:
    governance_score = (
        0.12 * f(row, "decision_rights_clarity")
        + 0.12 * f(row, "evidence_standard_quality")
        + 0.13 * f(row, "uncertainty_disclosure")
        + 0.12 * f(row, "review_cadence")
        + 0.14 * f(row, "trigger_condition_quality")
        + 0.13 * f(row, "dissent_protection")
        + 0.12 * f(row, "documentation_quality")
        + 0.12 * f(row, "accountability_quality")
    )

    if governance_score >= 0.72:
        action = "strong_uncertainty_governance"
    elif f(row, "uncertainty_disclosure") < 0.50:
        action = "improve_uncertainty_disclosure"
    elif f(row, "trigger_condition_quality") < 0.50:
        action = "define_trigger_conditions"
    elif f(row, "dissent_protection") < 0.50:
        action = "protect_dissent_and_challenge"
    else:
        action = "strengthen_governance"

    governance_rows.append(
        {
            "governance_id": row["governance_id"],
            "option_id": row["option_id"],
            "option_name": option_names.get(row["option_id"], row["option_id"]),
            "governance_practice": row["governance_practice"],
            "decision_governance_score": round(governance_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "decision_rights_clarity": row["decision_rights_clarity"],
            "evidence_standard_quality": row["evidence_standard_quality"],
            "uncertainty_disclosure": row["uncertainty_disclosure"],
            "review_cadence": row["review_cadence"],
            "trigger_condition_quality": row["trigger_condition_quality"],
            "dissent_protection": row["dissent_protection"],
            "documentation_quality": row["documentation_quality"],
            "accountability_quality": row["accountability_quality"],
        }
    )

governance_rows.sort(key=lambda item: item["decision_governance_score"], reverse=True)
write_csv(TABLES / "decision_governance_scores.csv", governance_rows, list(governance_rows[0].keys()))

# ---------------------------------------------------------------------
# 10. Decision learning memory scoring
# ---------------------------------------------------------------------

memory_rows: list[dict[str, object]] = []

for row in memory:
    memory_score = (
        0.11 * f(row, "decision_question_record")
        + 0.11 * f(row, "frame_record_quality")
        + 0.11 * f(row, "option_record_quality")
        + 0.12 * f(row, "assumption_record_quality")
        + 0.12 * f(row, "uncertainty_record_quality")
        + 0.11 * f(row, "evidence_record_quality")
        + 0.12 * f(row, "trigger_record_quality")
        + 0.10 * f(row, "revision_record_quality")
        + 0.10 * f(row, "reuse_quality")
    )

    if memory_score >= 0.72:
        action = "strong_decision_learning_memory"
    elif f(row, "uncertainty_record_quality") < 0.45:
        action = "document_uncertainty_more_clearly"
    elif f(row, "trigger_record_quality") < 0.45:
        action = "document_triggers"
    elif f(row, "revision_record_quality") < 0.45:
        action = "document_revision_logic"
    else:
        action = "strengthen_decision_memory"

    memory_rows.append(
        {
            "memory_id": row["memory_id"],
            "option_id": row["option_id"],
            "option_name": option_names.get(row["option_id"], row["option_id"]),
            "memory_practice": row["memory_practice"],
            "decision_learning_memory_score": round(memory_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "decision_question_record": row["decision_question_record"],
            "frame_record_quality": row["frame_record_quality"],
            "option_record_quality": row["option_record_quality"],
            "assumption_record_quality": row["assumption_record_quality"],
            "uncertainty_record_quality": row["uncertainty_record_quality"],
            "evidence_record_quality": row["evidence_record_quality"],
            "trigger_record_quality": row["trigger_record_quality"],
            "revision_record_quality": row["revision_record_quality"],
            "reuse_quality": row["reuse_quality"],
        }
    )

memory_rows.sort(key=lambda item: item["decision_learning_memory_score"], reverse=True)
write_csv(TABLES / "decision_learning_memory_scores.csv", memory_rows, list(memory_rows[0].keys()))

# ---------------------------------------------------------------------
# 11. Strategist report
# ---------------------------------------------------------------------

top_options = option_rows[:6]
fragile_options = sorted(option_rows, key=lambda item: item["fragility_risk"], reverse=True)[:5]
hard_uncertainties = uncertainty_rows[:6]
top_assumptions = assumption_rows[:6]
top_robust = stress_rows[:6]
worst_cases = sorted(stress_rows, key=lambda item: item["worst_case"])[:5]
top_option_value = option_value_rows[:6]
lock_in_warnings = sorted(option_value_rows, key=lambda item: item["lock_in_warning"], reverse=True)[:5]
top_experiments = experiment_rows[:6]
bias_risks = bias_rows[:6]
ethics_risks = ethics_rows[:6]
top_governance = governance_rows[:6]
weak_governance = sorted(governance_rows, key=lambda item: item["decision_governance_score"])[:4]
top_memory = memory_rows[:6]
weak_memory = sorted(memory_rows, key=lambda item: item["decision_learning_memory_score"])[:4]

report: list[str] = []
report.append("# Decision-Making Under Uncertainty Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic evaluates uncertainty-sensitive decision quality. It reviews option profiles, uncertainty classification, assumption risk, scenario robustness, "
    "option value, experiment design, heuristic and bias exposure, ethical uncertainty, governance, and decision-learning memory."
)

report.append("")
report.append("## Strongest decision options")
report.append("")
for item in top_options:
    report.append(
        f"- **{item['option_id']} — {item['option_name']}**: profile {item['decision_profile_score']}; "
        f"fragility risk {item['fragility_risk']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest fragility risks")
report.append("")
for item in fragile_options:
    report.append(
        f"- **{item['option_id']} — {item['option_name']}**: fragility risk {item['fragility_risk']}; "
        f"profile {item['decision_profile_score']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Most difficult uncertainty classifications")
report.append("")
for item in hard_uncertainties:
    report.append(
        f"- **{item['uncertainty_id']} — {item['option_name']}**: type {item['uncertainty_type']}; "
        f"difficulty {item['classification_difficulty']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest-risk assumptions")
report.append("")
for item in top_assumptions:
    report.append(
        f"- **{item['assumption_id']} — {item['option_name']}**: risk {item['assumption_risk']}; "
        f"action: {item['recommended_action']}; assumption: {item['assumption']}."
    )

report.append("")
report.append("## Strongest scenario stress-test profiles")
report.append("")
for item in top_robust:
    report.append(
        f"- **{item['test_id']} — {item['option_name']}**: robustness {item['robustness_score']}; "
        f"worst case {item['worst_case']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Worst-case warnings")
report.append("")
for item in worst_cases:
    report.append(
        f"- **{item['test_id']} — {item['option_name']}**: worst case {item['worst_case']}; "
        f"robustness {item['robustness_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strongest option-value profiles")
report.append("")
for item in top_option_value:
    report.append(
        f"- **{item['review_id']} — {item['option_name']}**: option value {item['option_value_score']}; "
        f"lock-in warning {item['lock_in_warning']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Lock-in warnings")
report.append("")
for item in lock_in_warnings:
    report.append(
        f"- **{item['review_id']} — {item['option_name']}**: lock-in warning {item['lock_in_warning']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strongest experiments")
report.append("")
for item in top_experiments:
    report.append(
        f"- **{item['experiment_id']} — {item['experiment_name']}**: quality {item['experiment_quality']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Heuristic and bias risks")
report.append("")
for item in bias_risks:
    report.append(
        f"- **{item['bias_id']} — {item['bias_or_heuristic']} / {item['option_name']}**: risk {item['bias_risk']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Ethical uncertainty risks")
report.append("")
for item in ethics_risks:
    report.append(
        f"- **{item['ethics_id']} — {item['ethical_issue']}**: risk {item['ethical_uncertainty_risk']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Decision governance")
report.append("")
for item in top_governance:
    report.append(
        f"- **{item['governance_id']} — {item['governance_practice']}**: governance score {item['decision_governance_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weak governance warnings")
report.append("")
for item in weak_governance:
    report.append(
        f"- **{item['governance_id']} — {item['governance_practice']}**: governance score {item['decision_governance_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Decision learning memory")
report.append("")
for item in top_memory:
    report.append(
        f"- **{item['memory_id']} — {item['memory_practice']}**: memory score {item['decision_learning_memory_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weak learning-memory warnings")
report.append("")
for item in weak_memory:
    report.append(
        f"- **{item['memory_id']} — {item['memory_practice']}**: memory score {item['decision_learning_memory_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "Decision-making under uncertainty is strongest when uncertainty is named accurately, assumptions are explicit, options are stress tested across futures, "
    "option value is preserved, experiments generate learning, bias is challenged, ethics are reviewed, and decision logic is documented for later revision."
)

(REPORTS / "decision_uncertainty_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_options": top_options,
    "fragile_options": fragile_options,
    "hard_uncertainties": hard_uncertainties,
    "top_assumptions": top_assumptions,
    "top_robust": top_robust,
    "worst_cases": worst_cases,
    "top_option_value": top_option_value,
    "lock_in_warnings": lock_in_warnings,
    "top_experiments": top_experiments,
    "bias_risks": bias_risks,
    "ethics_risks": ethics_risks,
    "top_governance": top_governance,
    "weak_governance": weak_governance,
    "top_memory": top_memory,
    "weak_memory": weak_memory,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced decision-making under uncertainty diagnostics complete.")
print(f"Wrote: {TABLES / 'decision_option_scores.csv'}")
print(f"Wrote: {TABLES / 'uncertainty_classification_scores.csv'}")
print(f"Wrote: {TABLES / 'assumption_risk_scores.csv'}")
print(f"Wrote: {TABLES / 'scenario_stress_test_scores.csv'}")
print(f"Wrote: {TABLES / 'option_value_scores.csv'}")
print(f"Wrote: {TABLES / 'experiment_design_scores.csv'}")
print(f"Wrote: {TABLES / 'heuristic_bias_scores.csv'}")
print(f"Wrote: {TABLES / 'ethical_uncertainty_scores.csv'}")
print(f"Wrote: {TABLES / 'decision_governance_scores.csv'}")
print(f"Wrote: {TABLES / 'decision_learning_memory_scores.csv'}")
print(f"Wrote: {REPORTS / 'decision_uncertainty_diagnostic_report.md'}")
