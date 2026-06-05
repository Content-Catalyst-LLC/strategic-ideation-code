#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Scenario Planning and Futures Thinking.

This dependency-light workflow uses only the Python standard library.

It produces:
- scenario set scores
- driver and uncertainty scores
- strategy stress-test scores
- signal monitoring scores
- adaptive pathway scores
- futures ethics scores
- scenario governance scores
- scenario learning-memory scores
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


scenario_sets = read_csv(RAW / "scenario_sets.csv")
drivers = read_csv(RAW / "driver_uncertainties.csv")
stress_tests = read_csv(RAW / "strategy_stress_tests.csv")
signals = read_csv(RAW / "signal_monitoring.csv")
pathways = read_csv(RAW / "adaptive_pathways.csv")
ethics = read_csv(RAW / "futures_ethics.csv")
governance = read_csv(RAW / "scenario_governance.csv")
memory = read_csv(RAW / "scenario_learning_memory.csv")

scenario_names = {row["scenario_set_id"]: row["scenario_set_name"] for row in scenario_sets}

# ---------------------------------------------------------------------
# 1. Scenario set scoring
# ---------------------------------------------------------------------

scenario_rows: list[dict[str, object]] = []

for row in scenario_sets:
    scenario_quality = (
        0.10 * f(row, "focal_question_clarity")
        + 0.08 * f(row, "time_horizon_fit")
        + 0.11 * f(row, "driver_analysis_quality")
        + 0.12 * f(row, "critical_uncertainty_quality")
        + 0.09 * f(row, "plausibility")
        + 0.10 * f(row, "internal_coherence")
        + 0.11 * f(row, "scenario_divergence")
        + 0.12 * f(row, "strategic_implication_quality")
        + 0.08 * f(row, "signal_monitoring_quality")
        + 0.06 * f(row, "decision_linkage")
        + 0.07 * f(row, "ethics_review")
        + 0.06 * f(row, "learning_memory")
    )

    workshop_theater_risk = (
        0.16 * (1 - f(row, "decision_linkage"))
        + 0.14 * (1 - f(row, "strategic_implication_quality"))
        + 0.12 * (1 - f(row, "signal_monitoring_quality"))
        + 0.12 * (1 - f(row, "learning_memory"))
        + 0.11 * (1 - f(row, "focal_question_clarity"))
        + 0.11 * (1 - f(row, "critical_uncertainty_quality"))
        + 0.10 * (1 - f(row, "scenario_divergence"))
        + 0.08 * (1 - f(row, "ethics_review"))
        + 0.06 * (1 - f(row, "driver_analysis_quality"))
    )

    if scenario_quality >= 0.74:
        diagnosis = "strong_strategic_scenario_system"
    elif workshop_theater_risk >= 0.62:
        diagnosis = "high_workshop_theater_risk"
    elif f(row, "scenario_divergence") < 0.40:
        diagnosis = "scenarios_lack_meaningful_divergence"
    elif f(row, "decision_linkage") < 0.45:
        diagnosis = "scenario_work_not_connected_to_decisions"
    elif f(row, "ethics_review") < 0.35:
        diagnosis = "ethics_and_representation_gap"
    else:
        diagnosis = "developing_scenario_capability"

    scenario_rows.append(
        {
            "scenario_set_id": row["scenario_set_id"],
            "scenario_set_name": row["scenario_set_name"],
            "scenario_quality_score": round(scenario_quality, 4),
            "workshop_theater_risk": round(workshop_theater_risk, 4),
            "diagnosis": diagnosis,
            "focal_question_clarity": row["focal_question_clarity"],
            "time_horizon_fit": row["time_horizon_fit"],
            "driver_analysis_quality": row["driver_analysis_quality"],
            "critical_uncertainty_quality": row["critical_uncertainty_quality"],
            "plausibility": row["plausibility"],
            "internal_coherence": row["internal_coherence"],
            "scenario_divergence": row["scenario_divergence"],
            "strategic_implication_quality": row["strategic_implication_quality"],
            "signal_monitoring_quality": row["signal_monitoring_quality"],
            "decision_linkage": row["decision_linkage"],
            "ethics_review": row["ethics_review"],
            "learning_memory": row["learning_memory"],
            "description": row["description"],
        }
    )

scenario_rows.sort(key=lambda item: item["scenario_quality_score"], reverse=True)
write_csv(TABLES / "scenario_set_scores.csv", scenario_rows, list(scenario_rows[0].keys()))
write_csv(PROCESSED / "scenario_set_scores.csv", scenario_rows, list(scenario_rows[0].keys()))

# ---------------------------------------------------------------------
# 2. Driver and uncertainty scoring
# ---------------------------------------------------------------------

driver_rows: list[dict[str, object]] = []

for row in drivers:
    critical_uncertainty_score = (
        0.30 * f(row, "impact")
        + 0.26 * f(row, "uncertainty")
        + 0.16 * f(row, "systemic_interdependence")
        + 0.12 * f(row, "stakeholder_salience")
        + 0.08 * f(row, "evidence_quality")
        + 0.08 * f(row, "monitoring_feasibility")
    )

    watch_priority = (
        0.24 * f(row, "impact")
        + 0.22 * f(row, "uncertainty")
        + 0.18 * f(row, "systemic_interdependence")
        + 0.14 * f(row, "stakeholder_salience")
        + 0.12 * f(row, "monitoring_feasibility")
        + 0.10 * (1 - f(row, "predictability"))
    )

    if critical_uncertainty_score >= 0.76:
        action = "use_as_core_scenario_uncertainty"
    elif watch_priority >= 0.70:
        action = "monitor_as_high_priority_driver"
    elif f(row, "evidence_quality") < 0.45:
        action = "strengthen_evidence_base"
    elif f(row, "monitoring_feasibility") < 0.45:
        action = "define_monitoring_proxy"
    else:
        action = "include_in_driver_scan"

    driver_rows.append(
        {
            "driver_id": row["driver_id"],
            "scenario_set_id": row["scenario_set_id"],
            "scenario_set_name": scenario_names.get(row["scenario_set_id"], row["scenario_set_id"]),
            "driver_name": row["driver_name"],
            "driver_category": row["driver_category"],
            "critical_uncertainty_score": round(critical_uncertainty_score, 4),
            "watch_priority": round(watch_priority, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "impact": row["impact"],
            "predictability": row["predictability"],
            "uncertainty": row["uncertainty"],
            "systemic_interdependence": row["systemic_interdependence"],
            "evidence_quality": row["evidence_quality"],
            "stakeholder_salience": row["stakeholder_salience"],
            "monitoring_feasibility": row["monitoring_feasibility"],
        }
    )

driver_rows.sort(key=lambda item: item["critical_uncertainty_score"], reverse=True)
write_csv(TABLES / "driver_uncertainty_scores.csv", driver_rows, list(driver_rows[0].keys()))

# ---------------------------------------------------------------------
# 3. Strategy stress-test scoring
# ---------------------------------------------------------------------

scenario_cols = [
    "scenario_stable_growth",
    "scenario_tech_disruption",
    "scenario_environmental_stress",
    "scenario_institutional_fragmentation",
    "scenario_supply_disruption",
]

stress_rows: list[dict[str, object]] = []

for row in stress_tests:
    values = [f(row, col) for col in scenario_cols]
    mean_performance = sum(values) / len(values)
    worst_case = min(values)
    best_case = max(values)
    variance = sum((value - mean_performance) ** 2 for value in values) / len(values)
    volatility = math.sqrt(variance)

    robustness_profile = (
        0.30 * worst_case
        + 0.24 * mean_performance
        + 0.16 * f(row, "flexibility")
        + 0.12 * f(row, "implementation_readiness")
        + 0.10 * f(row, "ethical_resilience")
        + 0.10 * f(row, "option_value")
        - 0.12 * volatility
    )

    fragility_risk = (
        0.30 * (1 - worst_case)
        + 0.18 * volatility
        + 0.14 * (1 - f(row, "flexibility"))
        + 0.12 * (1 - f(row, "option_value"))
        + 0.10 * (1 - f(row, "ethical_resilience"))
        + 0.08 * (1 - f(row, "implementation_readiness"))
    )

    if robustness_profile >= 0.70:
        action = "strong_cross_scenario_strategy"
    elif fragility_risk >= 0.55:
        action = "reduce_scenario_fragility"
    elif worst_case < 0.45:
        action = "address_worst_case_exposure"
    elif f(row, "option_value") < 0.45:
        action = "add_option_value"
    else:
        action = "strengthen_scenario_resilience"

    stress_rows.append(
        {
            "test_id": row["test_id"],
            "strategy_name": row["strategy_name"],
            "mean_performance": round(mean_performance, 4),
            "worst_case": round(worst_case, 4),
            "best_case": round(best_case, 4),
            "volatility": round(volatility, 4),
            "robustness_profile": round(robustness_profile, 4),
            "fragility_risk": round(fragility_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "scenario_stable_growth": row["scenario_stable_growth"],
            "scenario_tech_disruption": row["scenario_tech_disruption"],
            "scenario_environmental_stress": row["scenario_environmental_stress"],
            "scenario_institutional_fragmentation": row["scenario_institutional_fragmentation"],
            "scenario_supply_disruption": row["scenario_supply_disruption"],
            "flexibility": row["flexibility"],
            "implementation_readiness": row["implementation_readiness"],
            "ethical_resilience": row["ethical_resilience"],
            "option_value": row["option_value"],
        }
    )

stress_rows.sort(key=lambda item: item["robustness_profile"], reverse=True)
write_csv(TABLES / "strategy_stress_test_scores.csv", stress_rows, list(stress_rows[0].keys()))

# ---------------------------------------------------------------------
# 4. Signal monitoring scoring
# ---------------------------------------------------------------------

signal_rows: list[dict[str, object]] = []

for row in signals:
    monitoring_score = (
        0.15 * f(row, "signal_strength")
        - 0.12 * f(row, "noise_risk")
        + 0.16 * f(row, "lead_time_value")
        + 0.17 * f(row, "decision_relevance")
        + 0.16 * f(row, "monitoring_quality")
        + 0.13 * f(row, "interpretation_quality")
        + 0.07 * f(row, "owner_clarity")
    )

    response_priority = (
        0.20 * f(row, "decision_relevance")
        + 0.18 * f(row, "lead_time_value")
        + 0.16 * f(row, "signal_strength")
        + 0.14 * f(row, "interpretation_quality")
        + 0.12 * f(row, "monitoring_quality")
        + 0.10 * f(row, "owner_clarity")
        - 0.10 * f(row, "noise_risk")
    )

    if f(row, "noise_risk") >= 0.70:
        action = "avoid_overinterpreting_noisy_signal"
    elif response_priority >= 0.68:
        action = "high_priority_signal_monitoring"
    elif f(row, "owner_clarity") < 0.45:
        action = "assign_signal_owner"
    elif f(row, "monitoring_quality") < 0.45:
        action = "improve_monitoring_quality"
    else:
        action = "maintain_signal_review"

    signal_rows.append(
        {
            "signal_id": row["signal_id"],
            "scenario_set_id": row["scenario_set_id"],
            "scenario_set_name": scenario_names.get(row["scenario_set_id"], row["scenario_set_id"]),
            "signal_name": row["signal_name"],
            "signal_category": row["signal_category"],
            "monitoring_score": round(monitoring_score, 4),
            "response_priority": round(response_priority, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "signal_strength": row["signal_strength"],
            "noise_risk": row["noise_risk"],
            "lead_time_value": row["lead_time_value"],
            "decision_relevance": row["decision_relevance"],
            "monitoring_quality": row["monitoring_quality"],
            "interpretation_quality": row["interpretation_quality"],
            "owner_clarity": row["owner_clarity"],
        }
    )

signal_rows.sort(key=lambda item: item["response_priority"], reverse=True)
write_csv(TABLES / "signal_monitoring_scores.csv", signal_rows, list(signal_rows[0].keys()))

# ---------------------------------------------------------------------
# 5. Adaptive pathway scoring
# ---------------------------------------------------------------------

pathway_rows: list[dict[str, object]] = []

for row in pathways:
    pathway_score = (
        0.15 * f(row, "trigger_clarity")
        + 0.14 * f(row, "reversibility")
        + 0.16 * f(row, "option_value")
        + 0.13 * f(row, "resource_flexibility")
        + 0.13 * f(row, "capability_readiness")
        + 0.12 * f(row, "governance_clarity")
        + 0.10 * f(row, "stakeholder_alignment")
        + 0.07 * f(row, "learning_memory")
    )

    lock_in_risk = (
        0.22 * (1 - f(row, "reversibility"))
        + 0.20 * (1 - f(row, "option_value"))
        + 0.16 * (1 - f(row, "trigger_clarity"))
        + 0.14 * (1 - f(row, "resource_flexibility"))
        + 0.12 * (1 - f(row, "governance_clarity"))
        + 0.08 * (1 - f(row, "learning_memory"))
        + 0.08 * (1 - f(row, "stakeholder_alignment"))
    )

    if pathway_score >= 0.72:
        action = "strong_adaptive_pathway"
    elif lock_in_risk >= 0.58:
        action = "reduce_lock_in_risk"
    elif f(row, "trigger_clarity") < 0.45:
        action = "define_trigger_conditions"
    elif f(row, "governance_clarity") < 0.45:
        action = "clarify_pathway_governance"
    else:
        action = "strengthen_adaptive_pathway"

    pathway_rows.append(
        {
            "pathway_id": row["pathway_id"],
            "scenario_set_id": row["scenario_set_id"],
            "scenario_set_name": scenario_names.get(row["scenario_set_id"], row["scenario_set_id"]),
            "pathway_name": row["pathway_name"],
            "adaptive_pathway_score": round(pathway_score, 4),
            "lock_in_risk": round(lock_in_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "trigger_clarity": row["trigger_clarity"],
            "reversibility": row["reversibility"],
            "option_value": row["option_value"],
            "resource_flexibility": row["resource_flexibility"],
            "capability_readiness": row["capability_readiness"],
            "governance_clarity": row["governance_clarity"],
            "stakeholder_alignment": row["stakeholder_alignment"],
            "learning_memory": row["learning_memory"],
        }
    )

pathway_rows.sort(key=lambda item: item["adaptive_pathway_score"], reverse=True)
write_csv(TABLES / "adaptive_pathway_scores.csv", pathway_rows, list(pathway_rows[0].keys()))

# ---------------------------------------------------------------------
# 6. Futures ethics scoring
# ---------------------------------------------------------------------

ethics_rows: list[dict[str, object]] = []

for row in ethics:
    ethics_score = (
        0.16 * f(row, "representation_quality")
        + 0.15 * f(row, "power_review_quality")
        + 0.16 * f(row, "burden_shift_review")
        + 0.14 * f(row, "intergenerational_review")
        + 0.13 * f(row, "accessibility_quality")
        + 0.14 * f(row, "accountability_quality")
        + 0.12 * f(row, "redress_path_quality")
    )

    ethics_risk = 1 - ethics_score

    if ethics_score >= 0.74:
        action = "strong_futures_ethics_review"
    elif f(row, "representation_quality") < 0.45:
        action = "expand_representation"
    elif f(row, "power_review_quality") < 0.45:
        action = "review_power_and_plausibility"
    elif f(row, "burden_shift_review") < 0.45:
        action = "review_future_burden_shifts"
    elif f(row, "redress_path_quality") < 0.45:
        action = "define_redress_path"
    else:
        action = "strengthen_futures_ethics"

    ethics_rows.append(
        {
            "ethics_id": row["ethics_id"],
            "scenario_set_id": row["scenario_set_id"],
            "scenario_set_name": scenario_names.get(row["scenario_set_id"], row["scenario_set_id"]),
            "ethical_issue": row["ethical_issue"],
            "futures_ethics_score": round(ethics_score, 4),
            "futures_ethics_risk": round(ethics_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "representation_quality": row["representation_quality"],
            "power_review_quality": row["power_review_quality"],
            "burden_shift_review": row["burden_shift_review"],
            "intergenerational_review": row["intergenerational_review"],
            "accessibility_quality": row["accessibility_quality"],
            "accountability_quality": row["accountability_quality"],
            "redress_path_quality": row["redress_path_quality"],
        }
    )

ethics_rows.sort(key=lambda item: item["futures_ethics_risk"], reverse=True)
write_csv(TABLES / "futures_ethics_scores.csv", ethics_rows, list(ethics_rows[0].keys()))

# ---------------------------------------------------------------------
# 7. Scenario governance scoring
# ---------------------------------------------------------------------

governance_rows: list[dict[str, object]] = []

for row in governance:
    governance_score = (
        0.14 * f(row, "decision_rights_clarity")
        + 0.14 * f(row, "evidence_standard_quality")
        + 0.14 * f(row, "scenario_review_cadence")
        + 0.13 * f(row, "signal_owner_clarity")
        + 0.15 * f(row, "trigger_condition_quality")
        + 0.15 * f(row, "documentation_quality")
        + 0.15 * f(row, "accountability_quality")
    )

    if governance_score >= 0.72:
        action = "strong_scenario_governance"
    elif f(row, "trigger_condition_quality") < 0.45:
        action = "define_trigger_conditions"
    elif f(row, "decision_rights_clarity") < 0.45:
        action = "clarify_decision_rights"
    elif f(row, "scenario_review_cadence") < 0.45:
        action = "define_review_cadence"
    else:
        action = "strengthen_scenario_governance"

    governance_rows.append(
        {
            "governance_id": row["governance_id"],
            "scenario_set_id": row["scenario_set_id"],
            "scenario_set_name": scenario_names.get(row["scenario_set_id"], row["scenario_set_id"]),
            "governance_practice": row["governance_practice"],
            "scenario_governance_score": round(governance_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "decision_rights_clarity": row["decision_rights_clarity"],
            "evidence_standard_quality": row["evidence_standard_quality"],
            "scenario_review_cadence": row["scenario_review_cadence"],
            "signal_owner_clarity": row["signal_owner_clarity"],
            "trigger_condition_quality": row["trigger_condition_quality"],
            "documentation_quality": row["documentation_quality"],
            "accountability_quality": row["accountability_quality"],
        }
    )

governance_rows.sort(key=lambda item: item["scenario_governance_score"], reverse=True)
write_csv(TABLES / "scenario_governance_scores.csv", governance_rows, list(governance_rows[0].keys()))

# ---------------------------------------------------------------------
# 8. Scenario learning-memory scoring
# ---------------------------------------------------------------------

memory_rows: list[dict[str, object]] = []

for row in memory:
    memory_score = (
        0.11 * f(row, "focal_question_record")
        + 0.11 * f(row, "driver_record_quality")
        + 0.12 * f(row, "uncertainty_record_quality")
        + 0.12 * f(row, "scenario_logic_record")
        + 0.13 * f(row, "implication_record_quality")
        + 0.11 * f(row, "signal_record_quality")
        + 0.13 * f(row, "decision_traceability")
        + 0.09 * f(row, "remaining_uncertainty_quality")
        + 0.08 * f(row, "reuse_quality")
    )

    if memory_score >= 0.72:
        action = "strong_scenario_learning_memory"
    elif f(row, "decision_traceability") < 0.45:
        action = "improve_decision_traceability"
    elif f(row, "implication_record_quality") < 0.45:
        action = "document_strategic_implications"
    elif f(row, "remaining_uncertainty_quality") < 0.45:
        action = "document_remaining_uncertainty"
    else:
        action = "strengthen_scenario_memory"

    memory_rows.append(
        {
            "memory_id": row["memory_id"],
            "scenario_set_id": row["scenario_set_id"],
            "scenario_set_name": scenario_names.get(row["scenario_set_id"], row["scenario_set_id"]),
            "memory_practice": row["memory_practice"],
            "scenario_learning_memory_score": round(memory_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "focal_question_record": row["focal_question_record"],
            "driver_record_quality": row["driver_record_quality"],
            "uncertainty_record_quality": row["uncertainty_record_quality"],
            "scenario_logic_record": row["scenario_logic_record"],
            "implication_record_quality": row["implication_record_quality"],
            "signal_record_quality": row["signal_record_quality"],
            "decision_traceability": row["decision_traceability"],
            "remaining_uncertainty_quality": row["remaining_uncertainty_quality"],
            "reuse_quality": row["reuse_quality"],
        }
    )

memory_rows.sort(key=lambda item: item["scenario_learning_memory_score"], reverse=True)
write_csv(TABLES / "scenario_learning_memory_scores.csv", memory_rows, list(memory_rows[0].keys()))

# ---------------------------------------------------------------------
# 9. Strategist report
# ---------------------------------------------------------------------

top_scenarios = scenario_rows[:5]
highest_theater = sorted(scenario_rows, key=lambda item: item["workshop_theater_risk"], reverse=True)[:5]
top_drivers = driver_rows[:8]
top_strategies = stress_rows[:6]
fragile_strategies = sorted(stress_rows, key=lambda item: item["fragility_risk"], reverse=True)[:5]
top_signals = signal_rows[:8]
top_pathways = pathway_rows[:6]
lock_in_risks = sorted(pathway_rows, key=lambda item: item["lock_in_risk"], reverse=True)[:5]
ethics_risks = ethics_rows[:6]
top_governance = governance_rows[:6]
weak_governance = sorted(governance_rows, key=lambda item: item["scenario_governance_score"])[:4]
top_memory = memory_rows[:6]
weak_memory = sorted(memory_rows, key=lambda item: item["scenario_learning_memory_score"])[:4]

report: list[str] = []
report.append("# Scenario Planning and Futures Thinking Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic evaluates scenario planning and futures thinking as strategic ideation capabilities. It assesses scenario quality, workshop-theater risk, "
    "driver and uncertainty selection, strategy robustness, signal monitoring, adaptive pathways, futures ethics, governance, and learning memory."
)

report.append("")
report.append("## Strongest scenario sets")
report.append("")
for item in top_scenarios:
    report.append(
        f"- **{item['scenario_set_id']} — {item['scenario_set_name']}**: scenario quality {item['scenario_quality_score']}; "
        f"workshop-theater risk {item['workshop_theater_risk']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest workshop-theater risks")
report.append("")
for item in highest_theater:
    report.append(
        f"- **{item['scenario_set_id']} — {item['scenario_set_name']}**: workshop-theater risk {item['workshop_theater_risk']}; "
        f"diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest-priority drivers and uncertainties")
report.append("")
for item in top_drivers:
    report.append(
        f"- **{item['driver_id']} — {item['driver_name']}**: critical uncertainty {item['critical_uncertainty_score']}; "
        f"watch priority {item['watch_priority']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strongest strategy stress-test profiles")
report.append("")
for item in top_strategies:
    report.append(
        f"- **{item['test_id']} — {item['strategy_name']}**: robustness {item['robustness_profile']}; "
        f"worst case {item['worst_case']}; fragility risk {item['fragility_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Fragility warnings")
report.append("")
for item in fragile_strategies:
    report.append(
        f"- **{item['test_id']} — {item['strategy_name']}**: fragility risk {item['fragility_risk']}; "
        f"worst case {item['worst_case']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Signal monitoring priorities")
report.append("")
for item in top_signals:
    report.append(
        f"- **{item['signal_id']} — {item['signal_name']}**: response priority {item['response_priority']}; "
        f"monitoring score {item['monitoring_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strong adaptive pathways")
report.append("")
for item in top_pathways:
    report.append(
        f"- **{item['pathway_id']} — {item['pathway_name']}**: pathway score {item['adaptive_pathway_score']}; "
        f"lock-in risk {item['lock_in_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Lock-in risk warnings")
report.append("")
for item in lock_in_risks:
    report.append(
        f"- **{item['pathway_id']} — {item['pathway_name']}**: lock-in risk {item['lock_in_risk']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Futures ethics risks")
report.append("")
for item in ethics_risks:
    report.append(
        f"- **{item['ethics_id']} — {item['ethical_issue']}**: ethics risk {item['futures_ethics_risk']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Scenario governance")
report.append("")
for item in top_governance:
    report.append(
        f"- **{item['governance_id']} — {item['governance_practice']}**: governance score {item['scenario_governance_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weak governance warnings")
report.append("")
for item in weak_governance:
    report.append(
        f"- **{item['governance_id']} — {item['governance_practice']}**: governance score {item['scenario_governance_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Scenario learning memory")
report.append("")
for item in top_memory:
    report.append(
        f"- **{item['memory_id']} — {item['memory_practice']}**: memory score {item['scenario_learning_memory_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weak learning-memory warnings")
report.append("")
for item in weak_memory:
    report.append(
        f"- **{item['memory_id']} — {item['memory_practice']}**: memory score {item['scenario_learning_memory_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "Scenario planning strengthens strategy when scenarios are plausible, divergent, structurally informed, ethically reviewed, connected to decisions, and monitored over time. "
    "Scenario work weakens when it becomes workshop theater: vivid narratives without driver discipline, strategic implications, signal monitoring, adaptive pathways, or decision memory."
)

(REPORTS / "scenario_planning_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_scenarios": top_scenarios,
    "highest_theater": highest_theater,
    "top_drivers": top_drivers,
    "top_strategies": top_strategies,
    "fragile_strategies": fragile_strategies,
    "top_signals": top_signals,
    "top_pathways": top_pathways,
    "lock_in_risks": lock_in_risks,
    "ethics_risks": ethics_risks,
    "top_governance": top_governance,
    "weak_governance": weak_governance,
    "top_memory": top_memory,
    "weak_memory": weak_memory,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced scenario planning and futures thinking diagnostics complete.")
print(f"Wrote: {TABLES / 'scenario_set_scores.csv'}")
print(f"Wrote: {TABLES / 'driver_uncertainty_scores.csv'}")
print(f"Wrote: {TABLES / 'strategy_stress_test_scores.csv'}")
print(f"Wrote: {TABLES / 'signal_monitoring_scores.csv'}")
print(f"Wrote: {TABLES / 'adaptive_pathway_scores.csv'}")
print(f"Wrote: {TABLES / 'futures_ethics_scores.csv'}")
print(f"Wrote: {TABLES / 'scenario_governance_scores.csv'}")
print(f"Wrote: {TABLES / 'scenario_learning_memory_scores.csv'}")
print(f"Wrote: {REPORTS / 'scenario_planning_diagnostic_report.md'}")
