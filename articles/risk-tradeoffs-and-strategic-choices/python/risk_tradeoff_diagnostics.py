#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Risk, Tradeoffs, and Strategic Choices.

This dependency-light workflow uses only the Python standard library.

It produces:
- strategic tradeoff scores
- risk exposure scores
- opportunity cost scores
- temporal tradeoff scores
- scenario stress-test scores
- lock-in and reversibility scores
- resource allocation scores
- value conflict scores
- ethical burden scores
- decision memory scores
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


options = read_csv(RAW / "strategic_options.csv")
risks = read_csv(RAW / "risk_exposures.csv")
opportunity_costs = read_csv(RAW / "opportunity_costs.csv")
temporal = read_csv(RAW / "temporal_tradeoffs.csv")
scenarios = read_csv(RAW / "scenario_stress_tests.csv")
lock_in = read_csv(RAW / "lock_in_reversibility.csv")
resources = read_csv(RAW / "resource_allocation.csv")
values = read_csv(RAW / "value_conflicts.csv")
ethics = read_csv(RAW / "ethical_burdens.csv")
memory = read_csv(RAW / "decision_memory.csv")

option_names = {row["option_id"]: row["option_name"] for row in options}

# ---------------------------------------------------------------------
# 1. Strategic tradeoff scoring
# ---------------------------------------------------------------------

tradeoff_rows: list[dict[str, object]] = []

for row in options:
    profile_score = (
        0.18 * f(row, "short_term_return")
        + 0.20 * f(row, "resilience")
        + 0.16 * f(row, "flexibility")
        + 0.14 * f(row, "stakeholder_legitimacy")
        + 0.14 * f(row, "opportunity_value")
        - 0.18 * f(row, "exposure")
        + 0.08 * f(row, "reversibility")
        + 0.06 * f(row, "implementation_readiness")
        + 0.08 * f(row, "ethical_resilience")
        + 0.08 * f(row, "learning_value")
    )

    fragility_warning = (
        0.26 * f(row, "exposure")
        + 0.18 * (1 - f(row, "resilience"))
        + 0.14 * (1 - f(row, "flexibility"))
        + 0.12 * (1 - f(row, "stakeholder_legitimacy"))
        + 0.12 * (1 - f(row, "opportunity_value"))
        + 0.10 * (1 - f(row, "reversibility"))
        + 0.08 * (1 - f(row, "ethical_resilience"))
    )

    if profile_score >= 0.68:
        diagnosis = "strong_tradeoff_profile"
    elif fragility_warning >= 0.62:
        diagnosis = "high_fragility_warning"
    elif f(row, "exposure") >= 0.72:
        diagnosis = "high_exposure_option"
    elif f(row, "opportunity_value") < 0.42:
        diagnosis = "low_option_value"
    elif f(row, "stakeholder_legitimacy") < 0.48:
        diagnosis = "legitimacy_gap"
    else:
        diagnosis = "developing_tradeoff_profile"

    tradeoff_rows.append(
        {
            "option_id": row["option_id"],
            "option_name": row["option_name"],
            "option_type": row["option_type"],
            "strategic_tradeoff_score": round(profile_score, 4),
            "fragility_warning": round(fragility_warning, 4),
            "diagnosis": diagnosis,
            "short_term_return": row["short_term_return"],
            "resilience": row["resilience"],
            "flexibility": row["flexibility"],
            "stakeholder_legitimacy": row["stakeholder_legitimacy"],
            "opportunity_value": row["opportunity_value"],
            "exposure": row["exposure"],
            "reversibility": row["reversibility"],
            "implementation_readiness": row["implementation_readiness"],
            "ethical_resilience": row["ethical_resilience"],
            "learning_value": row["learning_value"],
            "description": row["description"],
        }
    )

tradeoff_rows.sort(key=lambda item: item["strategic_tradeoff_score"], reverse=True)
write_csv(TABLES / "strategic_tradeoff_scores.csv", tradeoff_rows, list(tradeoff_rows[0].keys()))
write_csv(PROCESSED / "strategic_tradeoff_scores.csv", tradeoff_rows, list(tradeoff_rows[0].keys()))

# ---------------------------------------------------------------------
# 2. Risk exposure scoring
# ---------------------------------------------------------------------

risk_rows: list[dict[str, object]] = []

for row in risks:
    gross_exposure = (
        0.13 * f(row, "financial_exposure")
        + 0.13 * f(row, "implementation_exposure")
        + 0.12 * f(row, "reputation_exposure")
        + 0.11 * f(row, "regulatory_exposure")
        + 0.13 * f(row, "ethical_exposure")
        + 0.14 * f(row, "systemic_exposure")
        + 0.14 * f(row, "strategic_exposure")
        + 0.10 * (1 - f(row, "absorptive_capacity"))
    )

    net_exposure = gross_exposure - 0.18 * f(row, "absorptive_capacity")

    if net_exposure >= 0.58:
        action = "urgent_exposure_reduction"
    elif f(row, "systemic_exposure") >= 0.65:
        action = "map_systemic_risk"
    elif f(row, "ethical_exposure") >= 0.60:
        action = "conduct_ethics_review"
    elif f(row, "strategic_exposure") >= 0.68:
        action = "review_future_option_loss"
    else:
        action = row["review_action"]

    risk_rows.append(
        {
            "risk_id": row["risk_id"],
            "option_id": row["option_id"],
            "option_name": option_names.get(row["option_id"], row["option_id"]),
            "risk_type": row["risk_type"],
            "gross_exposure": round(gross_exposure, 4),
            "net_exposure": round(net_exposure, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "financial_exposure": row["financial_exposure"],
            "implementation_exposure": row["implementation_exposure"],
            "reputation_exposure": row["reputation_exposure"],
            "regulatory_exposure": row["regulatory_exposure"],
            "ethical_exposure": row["ethical_exposure"],
            "systemic_exposure": row["systemic_exposure"],
            "strategic_exposure": row["strategic_exposure"],
            "absorptive_capacity": row["absorptive_capacity"],
        }
    )

risk_rows.sort(key=lambda item: item["net_exposure"], reverse=True)
write_csv(TABLES / "risk_exposure_scores.csv", risk_rows, list(risk_rows[0].keys()))

# ---------------------------------------------------------------------
# 3. Opportunity cost scoring
# ---------------------------------------------------------------------

opportunity_rows: list[dict[str, object]] = []

for row in opportunity_costs:
    opportunity_cost_score = (
        0.15 * f(row, "capability_cost")
        + 0.15 * f(row, "learning_cost")
        + 0.14 * f(row, "flexibility_cost")
        + 0.15 * f(row, "preparedness_cost")
        + 0.13 * f(row, "legitimacy_cost")
        + 0.12 * f(row, "innovation_cost")
        + 0.08 * f(row, "delay_cost")
        + 0.08 * (1 - f(row, "visibility"))
    )

    hidden_cost_risk = opportunity_cost_score * (1 + (1 - f(row, "visibility")) * 0.35)

    if hidden_cost_risk >= 0.75:
        action = "make_hidden_cost_visible"
    elif f(row, "preparedness_cost") >= 0.70:
        action = "review_preparedness_tradeoff"
    elif f(row, "learning_cost") >= 0.68:
        action = "review_learning_cost"
    elif f(row, "legitimacy_cost") >= 0.68:
        action = "review_legitimacy_cost"
    else:
        action = row["review_action"]

    opportunity_rows.append(
        {
            "cost_id": row["cost_id"],
            "option_id": row["option_id"],
            "option_name": option_names.get(row["option_id"], row["option_id"]),
            "forgone_alternative": row["forgone_alternative"],
            "opportunity_cost_score": round(opportunity_cost_score, 4),
            "hidden_cost_risk": round(hidden_cost_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "capability_cost": row["capability_cost"],
            "learning_cost": row["learning_cost"],
            "flexibility_cost": row["flexibility_cost"],
            "preparedness_cost": row["preparedness_cost"],
            "legitimacy_cost": row["legitimacy_cost"],
            "innovation_cost": row["innovation_cost"],
            "delay_cost": row["delay_cost"],
            "visibility": row["visibility"],
        }
    )

opportunity_rows.sort(key=lambda item: item["hidden_cost_risk"], reverse=True)
write_csv(TABLES / "opportunity_cost_scores.csv", opportunity_rows, list(opportunity_rows[0].keys()))

# ---------------------------------------------------------------------
# 4. Temporal tradeoff scoring
# ---------------------------------------------------------------------

temporal_rows: list[dict[str, object]] = []

for row in temporal:
    future_value = (
        0.20 * f(row, "medium_term_value")
        + 0.28 * f(row, "long_term_value")
        + 0.24 * f(row, "intergenerational_value")
        + 0.14 * f(row, "short_term_value")
        + 0.14 * f(row, "immediate_value")
    )

    temporal_risk = (
        0.26 * f(row, "deferred_cost")
        + 0.22 * f(row, "benefit_cost_misalignment")
        + 0.16 * f(row, "near_term_cost")
        + 0.14 * (1 - f(row, "long_term_value"))
        + 0.12 * (1 - f(row, "intergenerational_value"))
        + 0.10 * (f(row, "immediate_value") - f(row, "long_term_value") if f(row, "immediate_value") > f(row, "long_term_value") else 0)
    )

    if temporal_risk >= 0.62:
        action = "review_deferred_costs"
    elif future_value >= 0.76:
        action = "protect_long_term_value"
    elif f(row, "benefit_cost_misalignment") >= 0.70:
        action = "make_timing_misalignment_explicit"
    else:
        action = row["review_action"]

    temporal_rows.append(
        {
            "temporal_id": row["temporal_id"],
            "option_id": row["option_id"],
            "option_name": option_names.get(row["option_id"], row["option_id"]),
            "future_value_score": round(future_value, 4),
            "temporal_risk": round(temporal_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "immediate_value": row["immediate_value"],
            "short_term_value": row["short_term_value"],
            "medium_term_value": row["medium_term_value"],
            "long_term_value": row["long_term_value"],
            "intergenerational_value": row["intergenerational_value"],
            "near_term_cost": row["near_term_cost"],
            "deferred_cost": row["deferred_cost"],
            "benefit_cost_misalignment": row["benefit_cost_misalignment"],
        }
    )

temporal_rows.sort(key=lambda item: item["temporal_risk"], reverse=True)
write_csv(TABLES / "temporal_tradeoff_scores.csv", temporal_rows, list(temporal_rows[0].keys()))

# ---------------------------------------------------------------------
# 5. Scenario stress testing
# ---------------------------------------------------------------------

scenario_cols = [
    "stable_growth",
    "resource_constraint",
    "trust_crisis",
    "regulatory_shift",
    "system_disruption",
    "climate_or_environmental_stress",
    "implementation_delay",
]

scenario_rows: list[dict[str, object]] = []

for row in scenarios:
    values = [f(row, col) for col in scenario_cols]
    mean_performance = sum(values) / len(values)
    worst_case = min(values)
    best_case = max(values)
    variance = sum((value - mean_performance) ** 2 for value in values) / len(values)
    volatility = math.sqrt(variance)

    robustness_score = (
        0.40 * worst_case
        + 0.32 * mean_performance
        + 0.10 * best_case
        - 0.18 * volatility
    )

    if robustness_score >= 0.70:
        action = "strong_cross_scenario_option"
    elif worst_case < 0.42:
        action = "address_worst_case_fragility"
    elif volatility >= 0.16:
        action = "reduce_scenario_volatility"
    else:
        action = row["review_action"]

    scenario_rows.append(
        {
            "scenario_id": row["scenario_id"],
            "option_id": row["option_id"],
            "option_name": option_names.get(row["option_id"], row["option_id"]),
            "mean_performance": round(mean_performance, 4),
            "worst_case": round(worst_case, 4),
            "best_case": round(best_case, 4),
            "volatility": round(volatility, 4),
            "robustness_score": round(robustness_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "stable_growth": row["stable_growth"],
            "resource_constraint": row["resource_constraint"],
            "trust_crisis": row["trust_crisis"],
            "regulatory_shift": row["regulatory_shift"],
            "system_disruption": row["system_disruption"],
            "climate_or_environmental_stress": row["climate_or_environmental_stress"],
            "implementation_delay": row["implementation_delay"],
        }
    )

scenario_rows.sort(key=lambda item: item["robustness_score"], reverse=True)
write_csv(TABLES / "scenario_stress_test_scores.csv", scenario_rows, list(scenario_rows[0].keys()))

# ---------------------------------------------------------------------
# 6. Lock-in and reversibility scoring
# ---------------------------------------------------------------------

lock_rows: list[dict[str, object]] = []

for row in lock_in:
    lock_in_score = (
        0.16 * f(row, "irreversibility")
        + 0.15 * f(row, "switching_cost")
        + 0.14 * f(row, "ecosystem_dependence")
        + 0.12 * f(row, "contractual_constraint")
        + 0.13 * f(row, "data_or_platform_dependence")
        + 0.10 * f(row, "governance_constraint")
        - 0.12 * f(row, "retained_flexibility")
        - 0.08 * f(row, "exit_path_quality")
    )

    reversibility_score = (
        0.38 * f(row, "retained_flexibility")
        + 0.30 * f(row, "exit_path_quality")
        + 0.12 * (1 - f(row, "irreversibility"))
        + 0.10 * (1 - f(row, "switching_cost"))
        + 0.10 * (1 - f(row, "ecosystem_dependence"))
    )

    if lock_in_score >= 0.48:
        action = "reduce_lock_in_before_commitment"
    elif reversibility_score >= 0.68:
        action = "strong_reversibility_profile"
    elif f(row, "exit_path_quality") < 0.42:
        action = "build_exit_path"
    else:
        action = row["review_action"]

    lock_rows.append(
        {
            "lock_id": row["lock_id"],
            "option_id": row["option_id"],
            "option_name": option_names.get(row["option_id"], row["option_id"]),
            "lock_in_score": round(lock_in_score, 4),
            "reversibility_score": round(reversibility_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "irreversibility": row["irreversibility"],
            "switching_cost": row["switching_cost"],
            "ecosystem_dependence": row["ecosystem_dependence"],
            "contractual_constraint": row["contractual_constraint"],
            "data_or_platform_dependence": row["data_or_platform_dependence"],
            "governance_constraint": row["governance_constraint"],
            "retained_flexibility": row["retained_flexibility"],
            "exit_path_quality": row["exit_path_quality"],
        }
    )

lock_rows.sort(key=lambda item: item["lock_in_score"], reverse=True)
write_csv(TABLES / "lock_in_reversibility_scores.csv", lock_rows, list(lock_rows[0].keys()))

# ---------------------------------------------------------------------
# 7. Resource allocation scoring
# ---------------------------------------------------------------------

resource_rows: list[dict[str, object]] = []

for row in resources:
    resource_coherence = (
        0.14 * f(row, "budget_alignment")
        + 0.14 * f(row, "staffing_alignment")
        + 0.12 * f(row, "executive_attention")
        + 0.12 * f(row, "measurement_alignment")
        + 0.13 * f(row, "contingency_reserve")
        + 0.13 * f(row, "learning_budget")
        + 0.12 * f(row, "stakeholder_review_budget")
        + 0.10 * f(row, "declared_priority_match")
    )

    rhetoric_gap = 1 - f(row, "declared_priority_match")
    resilience_resource_gap = 1 - ((f(row, "contingency_reserve") + f(row, "learning_budget") + f(row, "stakeholder_review_budget")) / 3)

    if resource_coherence >= 0.70:
        action = "strong_resource_coherence"
    elif rhetoric_gap >= 0.52:
        action = "align_resources_with_declared_priorities"
    elif resilience_resource_gap >= 0.58:
        action = "fund_resilience_and_learning"
    else:
        action = row["review_action"]

    resource_rows.append(
        {
            "resource_id": row["resource_id"],
            "option_id": row["option_id"],
            "option_name": option_names.get(row["option_id"], row["option_id"]),
            "resource_coherence": round(resource_coherence, 4),
            "rhetoric_gap": round(rhetoric_gap, 4),
            "resilience_resource_gap": round(resilience_resource_gap, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "budget_alignment": row["budget_alignment"],
            "staffing_alignment": row["staffing_alignment"],
            "executive_attention": row["executive_attention"],
            "measurement_alignment": row["measurement_alignment"],
            "contingency_reserve": row["contingency_reserve"],
            "learning_budget": row["learning_budget"],
            "stakeholder_review_budget": row["stakeholder_review_budget"],
            "declared_priority_match": row["declared_priority_match"],
        }
    )

resource_rows.sort(key=lambda item: item["resource_coherence"], reverse=True)
write_csv(TABLES / "resource_allocation_scores.csv", resource_rows, list(resource_rows[0].keys()))

# ---------------------------------------------------------------------
# 8. Value conflict scoring
# ---------------------------------------------------------------------

value_rows: list[dict[str, object]] = []

for row in values:
    pressure_values = [
        f(row, "efficiency_pressure"),
        f(row, "resilience_pressure"),
        f(row, "equity_pressure"),
        f(row, "speed_pressure"),
        f(row, "legitimacy_pressure"),
        f(row, "innovation_pressure"),
        f(row, "control_pressure"),
    ]
    max_pressure = max(pressure_values)
    min_pressure = min(pressure_values)
    spread = max_pressure - min_pressure

    value_conflict_intensity = (
        0.30 * spread
        + 0.20 * (1 - f(row, "clarity_of_priority"))
        + 0.10 * f(row, "efficiency_pressure")
        + 0.10 * f(row, "resilience_pressure")
        + 0.10 * f(row, "equity_pressure")
        + 0.10 * f(row, "legitimacy_pressure")
        + 0.10 * f(row, "innovation_pressure")
    )

    if value_conflict_intensity >= 0.58:
        action = "clarify_value_priority"
    elif f(row, "clarity_of_priority") < 0.48:
        action = "write_value_priority_statement"
    elif spread >= 0.48:
        action = "review_high_value_tension"
    else:
        action = row["review_action"]

    value_rows.append(
        {
            "conflict_id": row["conflict_id"],
            "option_id": row["option_id"],
            "option_name": option_names.get(row["option_id"], row["option_id"]),
            "value_conflict": row["value_conflict"],
            "value_conflict_intensity": round(value_conflict_intensity, 4),
            "pressure_spread": round(spread, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "efficiency_pressure": row["efficiency_pressure"],
            "resilience_pressure": row["resilience_pressure"],
            "equity_pressure": row["equity_pressure"],
            "speed_pressure": row["speed_pressure"],
            "legitimacy_pressure": row["legitimacy_pressure"],
            "innovation_pressure": row["innovation_pressure"],
            "control_pressure": row["control_pressure"],
            "clarity_of_priority": row["clarity_of_priority"],
        }
    )

value_rows.sort(key=lambda item: item["value_conflict_intensity"], reverse=True)
write_csv(TABLES / "value_conflict_scores.csv", value_rows, list(value_rows[0].keys()))

# ---------------------------------------------------------------------
# 9. Ethical burden scoring
# ---------------------------------------------------------------------

ethics_rows: list[dict[str, object]] = []

for row in ethics:
    burden_risk = (
        0.15 * f(row, "benefit_concentration")
        + 0.18 * f(row, "burden_concentration")
        + 0.13 * (1 - f(row, "stakeholder_voice"))
        + 0.11 * (1 - f(row, "transparency"))
        + 0.11 * (1 - f(row, "redress_quality"))
        + 0.16 * f(row, "future_generation_burden")
        + 0.10 * (1 - f(row, "distributional_review_quality"))
        + 0.06 * (1 - f(row, "accountability_clarity"))
    )

    responsibility_score = 1 - burden_risk

    if burden_risk >= 0.62:
        action = "urgent_burden_review"
    elif f(row, "future_generation_burden") >= 0.70:
        action = "review_future_burden"
    elif f(row, "stakeholder_voice") < 0.45:
        action = "expand_stakeholder_voice"
    elif f(row, "redress_quality") < 0.45:
        action = "define_redress_path"
    else:
        action = row["review_action"]

    ethics_rows.append(
        {
            "ethics_id": row["ethics_id"],
            "option_id": row["option_id"],
            "option_name": option_names.get(row["option_id"], row["option_id"]),
            "ethical_issue": row["ethical_issue"],
            "ethical_burden_risk": round(burden_risk, 4),
            "responsibility_score": round(responsibility_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "benefit_concentration": row["benefit_concentration"],
            "burden_concentration": row["burden_concentration"],
            "stakeholder_voice": row["stakeholder_voice"],
            "transparency": row["transparency"],
            "redress_quality": row["redress_quality"],
            "future_generation_burden": row["future_generation_burden"],
            "distributional_review_quality": row["distributional_review_quality"],
            "accountability_clarity": row["accountability_clarity"],
        }
    )

ethics_rows.sort(key=lambda item: item["ethical_burden_risk"], reverse=True)
write_csv(TABLES / "ethical_burden_scores.csv", ethics_rows, list(ethics_rows[0].keys()))

# ---------------------------------------------------------------------
# 10. Decision memory scoring
# ---------------------------------------------------------------------

memory_rows: list[dict[str, object]] = []

for row in memory:
    memory_score = (
        0.11 * f(row, "decision_question_record")
        + 0.12 * f(row, "objective_conflict_record")
        + 0.10 * f(row, "option_record")
        + 0.12 * f(row, "exposure_record")
        + 0.13 * f(row, "opportunity_cost_record")
        + 0.12 * f(row, "temporal_tradeoff_record")
        + 0.12 * f(row, "value_priority_record")
        + 0.10 * f(row, "revision_trigger_record")
        + 0.08 * f(row, "reuse_quality")
    )

    if memory_score >= 0.70:
        action = "strong_tradeoff_memory"
    elif f(row, "opportunity_cost_record") < 0.45:
        action = "document_opportunity_cost"
    elif f(row, "value_priority_record") < 0.45:
        action = "document_value_priority"
    elif f(row, "revision_trigger_record") < 0.45:
        action = "define_revision_triggers"
    else:
        action = row["review_action"]

    memory_rows.append(
        {
            "memory_id": row["memory_id"],
            "option_id": row["option_id"],
            "option_name": option_names.get(row["option_id"], row["option_id"]),
            "memory_practice": row["memory_practice"],
            "decision_memory_score": round(memory_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "decision_question_record": row["decision_question_record"],
            "objective_conflict_record": row["objective_conflict_record"],
            "option_record": row["option_record"],
            "exposure_record": row["exposure_record"],
            "opportunity_cost_record": row["opportunity_cost_record"],
            "temporal_tradeoff_record": row["temporal_tradeoff_record"],
            "value_priority_record": row["value_priority_record"],
            "revision_trigger_record": row["revision_trigger_record"],
            "reuse_quality": row["reuse_quality"],
        }
    )

memory_rows.sort(key=lambda item: item["decision_memory_score"], reverse=True)
write_csv(TABLES / "decision_memory_scores.csv", memory_rows, list(memory_rows[0].keys()))

# ---------------------------------------------------------------------
# 11. Strategist report
# ---------------------------------------------------------------------

top_tradeoffs = tradeoff_rows[:6]
fragility_warnings = sorted(tradeoff_rows, key=lambda item: item["fragility_warning"], reverse=True)[:5]
risk_warnings = risk_rows[:6]
hidden_costs = opportunity_rows[:6]
temporal_risks = temporal_rows[:6]
scenario_robust = scenario_rows[:6]
scenario_weak = sorted(scenario_rows, key=lambda item: item["worst_case"])[:5]
lock_warnings = lock_rows[:6]
resource_strengths = resource_rows[:5]
resource_gaps = sorted(resource_rows, key=lambda item: item["resource_coherence"])[:5]
value_conflicts = value_rows[:6]
ethical_risks = ethics_rows[:6]
memory_strengths = memory_rows[:5]
memory_gaps = sorted(memory_rows, key=lambda item: item["decision_memory_score"])[:5]

report: list[str] = []
report.append("# Risk, Tradeoffs, and Strategic Choices Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic evaluates strategic choices under scarcity, risk, tradeoff, uncertainty, value conflict, and system consequence. "
    "It reviews option profiles, exposure, opportunity cost, temporal tradeoffs, scenario robustness, lock-in, resource allocation, value priorities, ethical burden, and decision memory."
)

report.append("")
report.append("## Strongest strategic tradeoff profiles")
report.append("")
for item in top_tradeoffs:
    report.append(
        f"- **{item['option_id']} — {item['option_name']}**: tradeoff score {item['strategic_tradeoff_score']}; "
        f"fragility warning {item['fragility_warning']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest fragility warnings")
report.append("")
for item in fragility_warnings:
    report.append(
        f"- **{item['option_id']} — {item['option_name']}**: fragility warning {item['fragility_warning']}; "
        f"tradeoff score {item['strategic_tradeoff_score']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest risk exposures")
report.append("")
for item in risk_warnings:
    report.append(
        f"- **{item['risk_id']} — {item['option_name']}**: net exposure {item['net_exposure']}; "
        f"gross exposure {item['gross_exposure']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Hidden opportunity costs")
report.append("")
for item in hidden_costs:
    report.append(
        f"- **{item['cost_id']} — {item['option_name']}**: hidden cost risk {item['hidden_cost_risk']}; "
        f"forgone alternative: {item['forgone_alternative']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Temporal tradeoff risks")
report.append("")
for item in temporal_risks:
    report.append(
        f"- **{item['temporal_id']} — {item['option_name']}**: temporal risk {item['temporal_risk']}; "
        f"future value {item['future_value_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strongest scenario robustness profiles")
report.append("")
for item in scenario_robust:
    report.append(
        f"- **{item['scenario_id']} — {item['option_name']}**: robustness {item['robustness_score']}; "
        f"worst case {item['worst_case']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Worst-case scenario warnings")
report.append("")
for item in scenario_weak:
    report.append(
        f"- **{item['scenario_id']} — {item['option_name']}**: worst case {item['worst_case']}; "
        f"robustness {item['robustness_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Lock-in warnings")
report.append("")
for item in lock_warnings:
    report.append(
        f"- **{item['lock_id']} — {item['option_name']}**: lock-in score {item['lock_in_score']}; "
        f"reversibility score {item['reversibility_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strongest resource coherence")
report.append("")
for item in resource_strengths:
    report.append(
        f"- **{item['resource_id']} — {item['option_name']}**: resource coherence {item['resource_coherence']}; "
        f"rhetoric gap {item['rhetoric_gap']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Resource allocation gaps")
report.append("")
for item in resource_gaps:
    report.append(
        f"- **{item['resource_id']} — {item['option_name']}**: resource coherence {item['resource_coherence']}; "
        f"resilience resource gap {item['resilience_resource_gap']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest value conflict intensity")
report.append("")
for item in value_conflicts:
    report.append(
        f"- **{item['conflict_id']} — {item['value_conflict']}**: intensity {item['value_conflict_intensity']}; "
        f"pressure spread {item['pressure_spread']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Ethical burden risks")
report.append("")
for item in ethical_risks:
    report.append(
        f"- **{item['ethics_id']} — {item['ethical_issue']}**: burden risk {item['ethical_burden_risk']}; "
        f"responsibility score {item['responsibility_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strongest decision memory")
report.append("")
for item in memory_strengths:
    report.append(
        f"- **{item['memory_id']} — {item['memory_practice']}**: memory score {item['decision_memory_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weak decision-memory warnings")
report.append("")
for item in memory_gaps:
    report.append(
        f"- **{item['memory_id']} — {item['memory_practice']}**: memory score {item['decision_memory_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "Risk and tradeoff analysis is strongest when it makes conflict, exposure, opportunity cost, time horizon, reversibility, resource allocation, value priorities, ethical burden, and decision memory visible before commitment. "
    "The purpose is not to remove sacrifice, but to decide consciously which risks and sacrifices are justified by which goals."
)

(REPORTS / "risk_tradeoff_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_tradeoffs": top_tradeoffs,
    "fragility_warnings": fragility_warnings,
    "risk_warnings": risk_warnings,
    "hidden_costs": hidden_costs,
    "temporal_risks": temporal_risks,
    "scenario_robust": scenario_robust,
    "scenario_weak": scenario_weak,
    "lock_warnings": lock_warnings,
    "resource_strengths": resource_strengths,
    "resource_gaps": resource_gaps,
    "value_conflicts": value_conflicts,
    "ethical_risks": ethical_risks,
    "memory_strengths": memory_strengths,
    "memory_gaps": memory_gaps,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced risk, tradeoffs, and strategic choices diagnostics complete.")
print(f"Wrote: {TABLES / 'strategic_tradeoff_scores.csv'}")
print(f"Wrote: {TABLES / 'risk_exposure_scores.csv'}")
print(f"Wrote: {TABLES / 'opportunity_cost_scores.csv'}")
print(f"Wrote: {TABLES / 'temporal_tradeoff_scores.csv'}")
print(f"Wrote: {TABLES / 'scenario_stress_test_scores.csv'}")
print(f"Wrote: {TABLES / 'lock_in_reversibility_scores.csv'}")
print(f"Wrote: {TABLES / 'resource_allocation_scores.csv'}")
print(f"Wrote: {TABLES / 'value_conflict_scores.csv'}")
print(f"Wrote: {TABLES / 'ethical_burden_scores.csv'}")
print(f"Wrote: {TABLES / 'decision_memory_scores.csv'}")
print(f"Wrote: {REPORTS / 'risk_tradeoff_diagnostic_report.md'}")
