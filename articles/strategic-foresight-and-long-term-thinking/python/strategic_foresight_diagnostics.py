#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Strategic Foresight and Long-Term Thinking.

This dependency-light workflow uses only the Python standard library.

It produces:
- foresight profile scores
- horizon signal scores
- driver uncertainty scores
- strategy stress-test scores
- path-dependence scores
- adaptive pathway scores
- anticipatory governance scores
- futures ethics scores
- foresight learning-memory scores
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


profiles = read_csv(RAW / "foresight_profiles.csv")
signals = read_csv(RAW / "horizon_signals.csv")
drivers = read_csv(RAW / "driver_uncertainties.csv")
stress_tests = read_csv(RAW / "strategy_stress_tests.csv")
path_dependencies = read_csv(RAW / "path_dependence.csv")
pathways = read_csv(RAW / "adaptive_pathways.csv")
governance = read_csv(RAW / "anticipatory_governance.csv")
ethics = read_csv(RAW / "futures_ethics.csv")
memory = read_csv(RAW / "foresight_learning_memory.csv")

profile_names = {row["profile_id"]: row["strategy_name"] for row in profiles}

# ---------------------------------------------------------------------
# 1. Foresight profile scoring
# ---------------------------------------------------------------------

profile_rows: list[dict[str, object]] = []

for row in profiles:
    foresight_profile = (
        0.08 * f(row, "short_term_return")
        + 0.15 * f(row, "foresight_depth")
        + 0.14 * f(row, "resilience")
        + 0.12 * f(row, "flexibility")
        - 0.12 * f(row, "path_dependence_risk")
        + 0.10 * f(row, "signal_capacity")
        + 0.10 * f(row, "scenario_capacity")
        + 0.10 * f(row, "option_value")
        + 0.07 * f(row, "ethics_review")
        + 0.08 * f(row, "governance_capacity")
        + 0.08 * f(row, "learning_memory")
    )

    short_term_bias = (
        f(row, "short_term_return")
        - (
            f(row, "foresight_depth")
            + f(row, "resilience")
            + f(row, "flexibility")
            + f(row, "option_value")
        ) / 4
    )

    future_viability = (
        0.18 * f(row, "foresight_depth")
        + 0.18 * f(row, "resilience")
        + 0.16 * f(row, "flexibility")
        + 0.14 * f(row, "option_value")
        + 0.12 * f(row, "scenario_capacity")
        + 0.10 * f(row, "signal_capacity")
        + 0.08 * f(row, "governance_capacity")
        + 0.08 * f(row, "ethics_review")
        - 0.14 * f(row, "path_dependence_risk")
    )

    if future_viability >= 0.70:
        diagnosis = "strong_long_term_foresight_profile"
    elif short_term_bias >= 0.35:
        diagnosis = "short_term_optimization_risk"
    elif f(row, "path_dependence_risk") >= 0.72:
        diagnosis = "high_path_dependence_and_lock_in_risk"
    elif f(row, "foresight_depth") < 0.45:
        diagnosis = "weak_temporal_depth"
    elif f(row, "ethics_review") < 0.45:
        diagnosis = "futures_ethics_gap"
    else:
        diagnosis = "developing_foresight_capability"

    profile_rows.append(
        {
            "profile_id": row["profile_id"],
            "strategy_name": row["strategy_name"],
            "organization_type": row["organization_type"],
            "domain": row["domain"],
            "foresight_profile_score": round(foresight_profile, 4),
            "future_viability_score": round(future_viability, 4),
            "short_term_bias": round(short_term_bias, 4),
            "diagnosis": diagnosis,
            "short_term_return": row["short_term_return"],
            "foresight_depth": row["foresight_depth"],
            "resilience": row["resilience"],
            "flexibility": row["flexibility"],
            "path_dependence_risk": row["path_dependence_risk"],
            "signal_capacity": row["signal_capacity"],
            "scenario_capacity": row["scenario_capacity"],
            "option_value": row["option_value"],
            "ethics_review": row["ethics_review"],
            "governance_capacity": row["governance_capacity"],
            "learning_memory": row["learning_memory"],
            "description": row["description"],
        }
    )

profile_rows.sort(key=lambda item: item["future_viability_score"], reverse=True)
write_csv(TABLES / "foresight_profile_scores.csv", profile_rows, list(profile_rows[0].keys()))
write_csv(PROCESSED / "foresight_profile_scores.csv", profile_rows, list(profile_rows[0].keys()))

# ---------------------------------------------------------------------
# 2. Horizon signal scoring
# ---------------------------------------------------------------------

signal_rows: list[dict[str, object]] = []

for row in signals:
    signal_value = (
        0.16 * f(row, "signal_strength")
        - 0.12 * f(row, "noise_risk")
        + 0.18 * f(row, "lead_time_value")
        + 0.18 * f(row, "strategic_relevance")
        + 0.15 * f(row, "interpretation_quality")
        + 0.13 * f(row, "monitoring_quality")
        + 0.08 * f(row, "owner_clarity")
    )

    response_priority = (
        0.20 * f(row, "strategic_relevance")
        + 0.18 * f(row, "lead_time_value")
        + 0.16 * f(row, "signal_strength")
        + 0.14 * f(row, "interpretation_quality")
        + 0.12 * f(row, "monitoring_quality")
        + 0.10 * f(row, "owner_clarity")
        - 0.10 * f(row, "noise_risk")
    )

    if f(row, "noise_risk") >= 0.65:
        action = "avoid_overinterpreting_noisy_signal"
    elif response_priority >= 0.68:
        action = "high_priority_horizon_signal"
    elif f(row, "owner_clarity") < 0.45:
        action = "assign_signal_owner"
    elif f(row, "monitoring_quality") < 0.45:
        action = "improve_signal_monitoring"
    else:
        action = "maintain_signal_review"

    signal_rows.append(
        {
            "signal_id": row["signal_id"],
            "profile_id": row["profile_id"],
            "strategy_name": profile_names.get(row["profile_id"], row["profile_id"]),
            "signal_name": row["signal_name"],
            "signal_category": row["signal_category"],
            "signal_value": round(signal_value, 4),
            "response_priority": round(response_priority, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "signal_strength": row["signal_strength"],
            "noise_risk": row["noise_risk"],
            "lead_time_value": row["lead_time_value"],
            "strategic_relevance": row["strategic_relevance"],
            "interpretation_quality": row["interpretation_quality"],
            "monitoring_quality": row["monitoring_quality"],
            "owner_clarity": row["owner_clarity"],
        }
    )

signal_rows.sort(key=lambda item: item["response_priority"], reverse=True)
write_csv(TABLES / "horizon_signal_scores.csv", signal_rows, list(signal_rows[0].keys()))

# ---------------------------------------------------------------------
# 3. Driver uncertainty scoring
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
        action = "use_as_core_foresight_uncertainty"
    elif watch_priority >= 0.70:
        action = "monitor_as_high_priority_driver"
    elif f(row, "evidence_quality") < 0.45:
        action = "strengthen_evidence_base"
    else:
        action = "include_in_driver_scan"

    driver_rows.append(
        {
            "driver_id": row["driver_id"],
            "profile_id": row["profile_id"],
            "strategy_name": profile_names.get(row["profile_id"], row["profile_id"]),
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
# 4. Strategy stress-test scoring
# ---------------------------------------------------------------------

future_cols = [
    "future_stable_growth",
    "future_tech_disruption",
    "future_environmental_stress",
    "future_institutional_fragmentation",
    "future_public_trust_crisis",
]

stress_rows: list[dict[str, object]] = []

for row in stress_tests:
    values = [f(row, col) for col in future_cols]
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
        action = "strong_cross_future_strategy"
    elif fragility_risk >= 0.55:
        action = "reduce_future_fragility"
    elif worst_case < 0.45:
        action = "address_worst_case_exposure"
    elif f(row, "option_value") < 0.45:
        action = "increase_option_value"
    else:
        action = "strengthen_future_resilience"

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
            "future_stable_growth": row["future_stable_growth"],
            "future_tech_disruption": row["future_tech_disruption"],
            "future_environmental_stress": row["future_environmental_stress"],
            "future_institutional_fragmentation": row["future_institutional_fragmentation"],
            "future_public_trust_crisis": row["future_public_trust_crisis"],
            "flexibility": row["flexibility"],
            "implementation_readiness": row["implementation_readiness"],
            "ethical_resilience": row["ethical_resilience"],
            "option_value": row["option_value"],
        }
    )

stress_rows.sort(key=lambda item: item["robustness_profile"], reverse=True)
write_csv(TABLES / "strategy_stress_test_scores.csv", stress_rows, list(stress_rows[0].keys()))

# ---------------------------------------------------------------------
# 5. Path dependence scoring
# ---------------------------------------------------------------------

path_dependence_rows: list[dict[str, object]] = []

for row in path_dependencies:
    lock_in_risk = (
        0.20 * f(row, "lock_in_strength")
        + 0.18 * (1 - f(row, "reversibility"))
        + 0.16 * f(row, "transition_cost")
        + 0.14 * f(row, "capability_gap")
        + 0.12 * f(row, "governance_constraint")
        + 0.10 * f(row, "stakeholder_constraint")
        + 0.10 * f(row, "option_loss_risk")
    )

    transition_readiness_gap = (
        0.24 * (1 - f(row, "reversibility"))
        + 0.20 * f(row, "capability_gap")
        + 0.18 * f(row, "transition_cost")
        + 0.16 * f(row, "governance_constraint")
        + 0.12 * f(row, "stakeholder_constraint")
        + 0.10 * f(row, "option_loss_risk")
    )

    if lock_in_risk >= 0.70:
        action = "urgent_lock_in_reduction_required"
    elif transition_readiness_gap >= 0.62:
        action = "build_transition_readiness"
    elif f(row, "reversibility") < 0.40:
        action = "increase_reversibility"
    else:
        action = "monitor_path_dependence"

    path_dependence_rows.append(
        {
            "path_id": row["path_id"],
            "profile_id": row["profile_id"],
            "strategy_name": profile_names.get(row["profile_id"], row["profile_id"]),
            "path_dependency": row["path_dependency"],
            "dependency_type": row["dependency_type"],
            "lock_in_risk": round(lock_in_risk, 4),
            "transition_readiness_gap": round(transition_readiness_gap, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "lock_in_strength": row["lock_in_strength"],
            "reversibility": row["reversibility"],
            "transition_cost": row["transition_cost"],
            "capability_gap": row["capability_gap"],
            "governance_constraint": row["governance_constraint"],
            "stakeholder_constraint": row["stakeholder_constraint"],
            "option_loss_risk": row["option_loss_risk"],
        }
    )

path_dependence_rows.sort(key=lambda item: item["lock_in_risk"], reverse=True)
write_csv(TABLES / "path_dependence_scores.csv", path_dependence_rows, list(path_dependence_rows[0].keys()))

# ---------------------------------------------------------------------
# 6. Adaptive pathway scoring
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

    future_flexibility_gap = 1 - pathway_score

    if pathway_score >= 0.72:
        action = "strong_adaptive_pathway"
    elif f(row, "trigger_clarity") < 0.45:
        action = "define_trigger_conditions"
    elif f(row, "reversibility") < 0.45:
        action = "increase_reversibility"
    elif f(row, "governance_clarity") < 0.45:
        action = "clarify_pathway_governance"
    else:
        action = "strengthen_adaptive_pathway"

    pathway_rows.append(
        {
            "pathway_id": row["pathway_id"],
            "profile_id": row["profile_id"],
            "strategy_name": profile_names.get(row["profile_id"], row["profile_id"]),
            "pathway_name": row["pathway_name"],
            "adaptive_pathway_score": round(pathway_score, 4),
            "future_flexibility_gap": round(future_flexibility_gap, 4),
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
# 7. Anticipatory governance scoring
# ---------------------------------------------------------------------

governance_rows: list[dict[str, object]] = []

for row in governance:
    governance_score = (
        0.13 * f(row, "decision_rights_clarity")
        + 0.13 * f(row, "evidence_standard_quality")
        + 0.13 * f(row, "foresight_review_cadence")
        + 0.12 * f(row, "signal_owner_clarity")
        + 0.14 * f(row, "trigger_condition_quality")
        + 0.13 * f(row, "ethics_review_quality")
        + 0.11 * f(row, "documentation_quality")
        + 0.11 * f(row, "accountability_quality")
    )

    if governance_score >= 0.74:
        action = "strong_anticipatory_governance"
    elif f(row, "trigger_condition_quality") < 0.45:
        action = "define_trigger_conditions"
    elif f(row, "foresight_review_cadence") < 0.45:
        action = "define_review_cadence"
    elif f(row, "ethics_review_quality") < 0.45:
        action = "strengthen_ethics_review"
    else:
        action = "strengthen_anticipatory_governance"

    governance_rows.append(
        {
            "governance_id": row["governance_id"],
            "profile_id": row["profile_id"],
            "strategy_name": profile_names.get(row["profile_id"], row["profile_id"]),
            "governance_practice": row["governance_practice"],
            "anticipatory_governance_score": round(governance_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "decision_rights_clarity": row["decision_rights_clarity"],
            "evidence_standard_quality": row["evidence_standard_quality"],
            "foresight_review_cadence": row["foresight_review_cadence"],
            "signal_owner_clarity": row["signal_owner_clarity"],
            "trigger_condition_quality": row["trigger_condition_quality"],
            "ethics_review_quality": row["ethics_review_quality"],
            "documentation_quality": row["documentation_quality"],
            "accountability_quality": row["accountability_quality"],
        }
    )

governance_rows.sort(key=lambda item: item["anticipatory_governance_score"], reverse=True)
write_csv(TABLES / "anticipatory_governance_scores.csv", governance_rows, list(governance_rows[0].keys()))

# ---------------------------------------------------------------------
# 8. Futures ethics scoring
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
            "profile_id": row["profile_id"],
            "strategy_name": profile_names.get(row["profile_id"], row["profile_id"]),
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
# 9. Foresight learning memory scoring
# ---------------------------------------------------------------------

memory_rows: list[dict[str, object]] = []

for row in memory:
    memory_score = (
        0.11 * f(row, "focal_question_record")
        + 0.12 * f(row, "signal_record_quality")
        + 0.11 * f(row, "driver_record_quality")
        + 0.11 * f(row, "uncertainty_record_quality")
        + 0.12 * f(row, "scenario_record_quality")
        + 0.13 * f(row, "decision_traceability")
        + 0.11 * f(row, "pathway_record_quality")
        + 0.10 * f(row, "remaining_uncertainty_quality")
        + 0.09 * f(row, "reuse_quality")
    )

    if memory_score >= 0.72:
        action = "strong_foresight_learning_memory"
    elif f(row, "decision_traceability") < 0.45:
        action = "improve_decision_traceability"
    elif f(row, "remaining_uncertainty_quality") < 0.45:
        action = "document_remaining_uncertainty"
    elif f(row, "scenario_record_quality") < 0.45:
        action = "document_scenario_logic"
    else:
        action = "strengthen_foresight_memory"

    memory_rows.append(
        {
            "memory_id": row["memory_id"],
            "profile_id": row["profile_id"],
            "strategy_name": profile_names.get(row["profile_id"], row["profile_id"]),
            "memory_practice": row["memory_practice"],
            "foresight_learning_memory_score": round(memory_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "focal_question_record": row["focal_question_record"],
            "signal_record_quality": row["signal_record_quality"],
            "driver_record_quality": row["driver_record_quality"],
            "uncertainty_record_quality": row["uncertainty_record_quality"],
            "scenario_record_quality": row["scenario_record_quality"],
            "decision_traceability": row["decision_traceability"],
            "pathway_record_quality": row["pathway_record_quality"],
            "remaining_uncertainty_quality": row["remaining_uncertainty_quality"],
            "reuse_quality": row["reuse_quality"],
        }
    )

memory_rows.sort(key=lambda item: item["foresight_learning_memory_score"], reverse=True)
write_csv(TABLES / "foresight_learning_memory_scores.csv", memory_rows, list(memory_rows[0].keys()))

# ---------------------------------------------------------------------
# 10. Strategist report
# ---------------------------------------------------------------------

top_profiles = profile_rows[:5]
short_term_risks = sorted(profile_rows, key=lambda item: item["short_term_bias"], reverse=True)[:5]
top_signals = signal_rows[:7]
top_drivers = driver_rows[:7]
top_stress = stress_rows[:7]
fragility_warnings = sorted(stress_rows, key=lambda item: item["fragility_risk"], reverse=True)[:5]
path_lockins = path_dependence_rows[:6]
top_pathways = pathway_rows[:6]
weak_pathways = sorted(pathway_rows, key=lambda item: item["adaptive_pathway_score"])[:4]
top_governance = governance_rows[:6]
weak_governance = sorted(governance_rows, key=lambda item: item["anticipatory_governance_score"])[:4]
ethics_risks = ethics_rows[:6]
top_memory = memory_rows[:6]
weak_memory = sorted(memory_rows, key=lambda item: item["foresight_learning_memory_score"])[:4]

report: list[str] = []
report.append("# Strategic Foresight and Long-Term Thinking Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic evaluates strategic foresight as structured anticipation. It assesses temporal depth, future viability, horizon signals, driver uncertainty, "
    "scenario stress tests, path dependence, adaptive pathways, anticipatory governance, futures ethics, and learning memory."
)

report.append("")
report.append("## Strongest long-term foresight profiles")
report.append("")
for item in top_profiles:
    report.append(
        f"- **{item['profile_id']} — {item['strategy_name']}**: future viability {item['future_viability_score']}; "
        f"foresight profile {item['foresight_profile_score']}; short-term bias {item['short_term_bias']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest short-term optimization risks")
report.append("")
for item in short_term_risks:
    report.append(
        f"- **{item['profile_id']} — {item['strategy_name']}**: short-term bias {item['short_term_bias']}; "
        f"future viability {item['future_viability_score']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Horizon-signal priorities")
report.append("")
for item in top_signals:
    report.append(
        f"- **{item['signal_id']} — {item['signal_name']}**: response priority {item['response_priority']}; "
        f"signal value {item['signal_value']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Critical drivers and uncertainties")
report.append("")
for item in top_drivers:
    report.append(
        f"- **{item['driver_id']} — {item['driver_name']}**: critical uncertainty {item['critical_uncertainty_score']}; "
        f"watch priority {item['watch_priority']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strategy stress-test profiles")
report.append("")
for item in top_stress:
    report.append(
        f"- **{item['test_id']} — {item['strategy_name']}**: robustness {item['robustness_profile']}; "
        f"worst case {item['worst_case']}; fragility risk {item['fragility_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Fragility warnings")
report.append("")
for item in fragility_warnings:
    report.append(
        f"- **{item['test_id']} — {item['strategy_name']}**: fragility risk {item['fragility_risk']}; "
        f"worst case {item['worst_case']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Path-dependence and lock-in risks")
report.append("")
for item in path_lockins:
    report.append(
        f"- **{item['path_id']} — {item['path_dependency']}**: lock-in risk {item['lock_in_risk']}; "
        f"transition gap {item['transition_readiness_gap']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Adaptive pathways")
report.append("")
for item in top_pathways:
    report.append(
        f"- **{item['pathway_id']} — {item['pathway_name']}**: pathway score {item['adaptive_pathway_score']}; "
        f"future-flexibility gap {item['future_flexibility_gap']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weak adaptive pathway warnings")
report.append("")
for item in weak_pathways:
    report.append(
        f"- **{item['pathway_id']} — {item['pathway_name']}**: pathway score {item['adaptive_pathway_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Anticipatory governance")
report.append("")
for item in top_governance:
    report.append(
        f"- **{item['governance_id']} — {item['governance_practice']}**: governance score {item['anticipatory_governance_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weak governance warnings")
report.append("")
for item in weak_governance:
    report.append(
        f"- **{item['governance_id']} — {item['governance_practice']}**: governance score {item['anticipatory_governance_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Futures ethics risks")
report.append("")
for item in ethics_risks:
    report.append(
        f"- **{item['ethics_id']} — {item['ethical_issue']}**: futures ethics risk {item['futures_ethics_risk']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Foresight learning memory")
report.append("")
for item in top_memory:
    report.append(
        f"- **{item['memory_id']} — {item['memory_practice']}**: memory score {item['foresight_learning_memory_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weak learning-memory warnings")
report.append("")
for item in weak_memory:
    report.append(
        f"- **{item['memory_id']} — {item['memory_practice']}**: memory score {item['foresight_learning_memory_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "Strategic foresight is strongest when long-term thinking is connected to signals, scenarios, strategy stress tests, option value, ethical review, governance, and learning memory. "
    "The central risk is not uncertainty itself, but short-term optimization that creates path dependence before future conditions are understood."
)

(REPORTS / "strategic_foresight_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_profiles": top_profiles,
    "short_term_risks": short_term_risks,
    "top_signals": top_signals,
    "top_drivers": top_drivers,
    "top_stress": top_stress,
    "fragility_warnings": fragility_warnings,
    "path_lockins": path_lockins,
    "top_pathways": top_pathways,
    "weak_pathways": weak_pathways,
    "top_governance": top_governance,
    "weak_governance": weak_governance,
    "ethics_risks": ethics_risks,
    "top_memory": top_memory,
    "weak_memory": weak_memory,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced strategic foresight and long-term thinking diagnostics complete.")
print(f"Wrote: {TABLES / 'foresight_profile_scores.csv'}")
print(f"Wrote: {TABLES / 'horizon_signal_scores.csv'}")
print(f"Wrote: {TABLES / 'driver_uncertainty_scores.csv'}")
print(f"Wrote: {TABLES / 'strategy_stress_test_scores.csv'}")
print(f"Wrote: {TABLES / 'path_dependence_scores.csv'}")
print(f"Wrote: {TABLES / 'adaptive_pathway_scores.csv'}")
print(f"Wrote: {TABLES / 'anticipatory_governance_scores.csv'}")
print(f"Wrote: {TABLES / 'futures_ethics_scores.csv'}")
print(f"Wrote: {TABLES / 'foresight_learning_memory_scores.csv'}")
print(f"Wrote: {REPORTS / 'strategic_foresight_diagnostic_report.md'}")
