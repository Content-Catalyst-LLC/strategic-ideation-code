#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Adaptive Strategy and Iteration.

This dependency-light workflow uses only the Python standard library.

It produces:
- adaptive strategy profile scores
- feedback signal scores
- assumption revision scores
- trigger condition scores
- experiment portfolio scores
- timing responsiveness scores
- exploration/exploitation balance scores
- systems impact scores
- adaptive governance scores
- learning memory scores
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


profiles = read_csv(RAW / "strategy_profiles.csv")
signals = read_csv(RAW / "feedback_signals.csv")
assumptions = read_csv(RAW / "assumption_register.csv")
triggers = read_csv(RAW / "trigger_conditions.csv")
experiments = read_csv(RAW / "experiment_portfolio.csv")
timing = read_csv(RAW / "timing_responsiveness.csv")
portfolio = read_csv(RAW / "portfolio_balance.csv")
impacts = read_csv(RAW / "systems_impacts.csv")
governance = read_csv(RAW / "governance_reviews.csv")
memory = read_csv(RAW / "learning_memory.csv")

strategy_names = {row["strategy_id"]: row["strategy_name"] for row in profiles}

# ---------------------------------------------------------------------
# 1. Adaptive strategy profile scoring
# ---------------------------------------------------------------------

profile_rows: list[dict[str, object]] = []

for row in profiles:
    adaptive_score = (
        0.13 * f(row, "flexibility")
        + 0.15 * f(row, "learning_capacity")
        + 0.09 * f(row, "exploration")
        + 0.11 * f(row, "exploitation_balance")
        + 0.15 * f(row, "coherence")
        + 0.13 * f(row, "feedback_intelligence")
        + 0.10 * f(row, "governance")
        + 0.08 * f(row, "systems_awareness")
        + 0.06 * f(row, "learning_memory")
    )

    over_adaptation_risk = (
        0.20 * f(row, "flexibility") * (1 - f(row, "coherence"))
        + 0.18 * (1 - f(row, "governance"))
        + 0.16 * (1 - f(row, "feedback_intelligence"))
        + 0.14 * (1 - f(row, "learning_capacity"))
        + 0.12 * (1 - f(row, "exploitation_balance"))
        + 0.10 * (1 - f(row, "learning_memory"))
        + 0.10 * (1 - f(row, "systems_awareness"))
    )

    if adaptive_score >= 0.74:
        diagnosis = "strong_adaptive_strategy_system"
    elif over_adaptation_risk >= 0.60:
        diagnosis = "high_over_adaptation_or_reactivity_risk"
    elif f(row, "flexibility") < 0.45 and f(row, "learning_capacity") < 0.55:
        diagnosis = "static_strategy_decay_risk"
    elif f(row, "coherence") < 0.45:
        diagnosis = "strategic_drift_risk"
    else:
        diagnosis = "developing_adaptive_capability"

    profile_rows.append(
        {
            "strategy_id": row["strategy_id"],
            "strategy_name": row["strategy_name"],
            "organization_type": row["organization_type"],
            "domain": row["domain"],
            "adaptive_strategy_score": round(adaptive_score, 4),
            "over_adaptation_risk": round(over_adaptation_risk, 4),
            "diagnosis": diagnosis,
            "flexibility": row["flexibility"],
            "learning_capacity": row["learning_capacity"],
            "exploration": row["exploration"],
            "exploitation_balance": row["exploitation_balance"],
            "coherence": row["coherence"],
            "feedback_intelligence": row["feedback_intelligence"],
            "governance": row["governance"],
            "systems_awareness": row["systems_awareness"],
            "learning_memory": row["learning_memory"],
            "description": row["description"],
        }
    )

profile_rows.sort(key=lambda item: item["adaptive_strategy_score"], reverse=True)
write_csv(TABLES / "adaptive_strategy_profile_scores.csv", profile_rows, list(profile_rows[0].keys()))
write_csv(PROCESSED / "adaptive_strategy_profile_scores.csv", profile_rows, list(profile_rows[0].keys()))

# ---------------------------------------------------------------------
# 2. Feedback signal scoring
# ---------------------------------------------------------------------

signal_rows: list[dict[str, object]] = []

for row in signals:
    signal_value = (
        0.20 * f(row, "signal_strength")
        - 0.12 * f(row, "noise_risk")
        - 0.08 * f(row, "delay_risk")
        + 0.18 * f(row, "interpretation_quality")
        + 0.18 * f(row, "decision_relevance")
        + 0.12 * f(row, "stakeholder_impact")
        + 0.12 * f(row, "systems_relevance")
    )

    response_priority = (
        0.18 * f(row, "signal_strength")
        + 0.16 * f(row, "decision_relevance")
        + 0.16 * f(row, "stakeholder_impact")
        + 0.16 * f(row, "systems_relevance")
        + 0.12 * f(row, "delay_risk")
        - 0.14 * f(row, "noise_risk")
        + 0.08 * f(row, "interpretation_quality")
    )

    if f(row, "noise_risk") >= 0.70:
        action = "avoid_overreaction_to_noise"
    elif response_priority >= 0.62:
        action = "prioritize_adaptive_response"
    elif f(row, "delay_risk") >= 0.60:
        action = "monitor_lagging_effects"
    elif f(row, "interpretation_quality") < 0.45:
        action = "improve_signal_interpretation"
    else:
        action = "monitor_and_contextualize_signal"

    signal_rows.append(
        {
            "signal_id": row["signal_id"],
            "strategy_id": row["strategy_id"],
            "strategy_name": strategy_names.get(row["strategy_id"], row["strategy_id"]),
            "signal_type": row["signal_type"],
            "signal_description": row["signal_description"],
            "signal_value": round(signal_value, 4),
            "response_priority": round(response_priority, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "signal_strength": row["signal_strength"],
            "noise_risk": row["noise_risk"],
            "delay_risk": row["delay_risk"],
            "interpretation_quality": row["interpretation_quality"],
            "decision_relevance": row["decision_relevance"],
            "stakeholder_impact": row["stakeholder_impact"],
            "systems_relevance": row["systems_relevance"],
        }
    )

signal_rows.sort(key=lambda item: item["response_priority"], reverse=True)
write_csv(TABLES / "feedback_signal_scores.csv", signal_rows, list(signal_rows[0].keys()))

# ---------------------------------------------------------------------
# 3. Assumption revision scoring
# ---------------------------------------------------------------------

assumption_rows: list[dict[str, object]] = []

for row in assumptions:
    criticality = 0.50 * f(row, "uncertainty") + 0.50 * f(row, "consequence")
    revision_need = (
        0.24 * f(row, "uncertainty")
        + 0.24 * f(row, "consequence")
        + 0.22 * f(row, "decay_risk")
        - 0.16 * f(row, "evidence_strength")
        - 0.08 * f(row, "revision_readiness")
        - 0.06 * f(row, "owner_clarity")
    )

    readiness_score = (
        0.34 * f(row, "evidence_strength")
        + 0.34 * f(row, "revision_readiness")
        + 0.32 * f(row, "owner_clarity")
    )

    if revision_need >= 0.52:
        action = "assumption_revision_required"
    elif f(row, "decay_risk") >= 0.70:
        action = "monitor_assumption_decay"
    elif readiness_score < 0.45:
        action = "improve_evidence_owner_and_revision_readiness"
    else:
        action = "maintain_assumption_monitoring"

    assumption_rows.append(
        {
            "assumption_id": row["assumption_id"],
            "strategy_id": row["strategy_id"],
            "strategy_name": strategy_names.get(row["strategy_id"], row["strategy_id"]),
            "assumption": row["assumption"],
            "assumption_type": row["assumption_type"],
            "criticality": round(criticality, 4),
            "revision_need": round(revision_need, 4),
            "readiness_score": round(readiness_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "uncertainty": row["uncertainty"],
            "consequence": row["consequence"],
            "evidence_strength": row["evidence_strength"],
            "decay_risk": row["decay_risk"],
            "revision_readiness": row["revision_readiness"],
            "owner_clarity": row["owner_clarity"],
        }
    )

assumption_rows.sort(key=lambda item: item["revision_need"], reverse=True)
write_csv(TABLES / "assumption_revision_scores.csv", assumption_rows, list(assumption_rows[0].keys()))

# ---------------------------------------------------------------------
# 4. Trigger condition scoring
# ---------------------------------------------------------------------

trigger_rows: list[dict[str, object]] = []

for row in triggers:
    trigger_score = (
        0.15 * f(row, "trigger_clarity")
        + 0.15 * f(row, "evidence_threshold")
        + 0.16 * f(row, "decision_path_clarity")
        + 0.13 * f(row, "response_speed_fit")
        + 0.13 * f(row, "ethical_safeguards")
        + 0.13 * f(row, "authority_clarity")
        + 0.15 * f(row, "monitoring_quality")
    )

    if trigger_score >= 0.72:
        action = "strong_trigger_condition"
    elif f(row, "evidence_threshold") < 0.45:
        action = "define_evidence_threshold"
    elif f(row, "decision_path_clarity") < 0.45:
        action = "clarify_decision_path"
    elif f(row, "ethical_safeguards") < 0.45:
        action = "add_ethical_safeguards"
    else:
        action = "strengthen_trigger_condition"

    trigger_rows.append(
        {
            "trigger_id": row["trigger_id"],
            "strategy_id": row["strategy_id"],
            "strategy_name": strategy_names.get(row["strategy_id"], row["strategy_id"]),
            "trigger_name": row["trigger_name"],
            "trigger_condition_score": round(trigger_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "trigger_clarity": row["trigger_clarity"],
            "evidence_threshold": row["evidence_threshold"],
            "decision_path_clarity": row["decision_path_clarity"],
            "response_speed_fit": row["response_speed_fit"],
            "ethical_safeguards": row["ethical_safeguards"],
            "authority_clarity": row["authority_clarity"],
            "monitoring_quality": row["monitoring_quality"],
        }
    )

trigger_rows.sort(key=lambda item: item["trigger_condition_score"], reverse=True)
write_csv(TABLES / "trigger_condition_scores.csv", trigger_rows, list(trigger_rows[0].keys()))

# ---------------------------------------------------------------------
# 5. Experiment portfolio scoring
# ---------------------------------------------------------------------

experiment_rows: list[dict[str, object]] = []

for row in experiments:
    experiment_score = (
        0.16 * f(row, "critical_assumption_fit")
        + 0.16 * f(row, "evidence_standard_quality")
        + 0.17 * f(row, "learning_value")
        + 0.16 * f(row, "decision_linkage")
        + 0.11 * f(row, "resource_fit")
        + 0.12 * f(row, "scale_relevance")
        + 0.12 * f(row, "ethical_review")
    )

    if experiment_score >= 0.72:
        action = "strong_strategic_experiment"
    elif f(row, "decision_linkage") < 0.45:
        action = "connect_experiment_to_decision"
    elif f(row, "evidence_standard_quality") < 0.45:
        action = "define_evidence_standard"
    elif f(row, "critical_assumption_fit") < 0.45:
        action = "test_more_critical_assumption"
    else:
        action = "strengthen_experiment_design"

    experiment_rows.append(
        {
            "experiment_id": row["experiment_id"],
            "strategy_id": row["strategy_id"],
            "strategy_name": strategy_names.get(row["strategy_id"], row["strategy_id"]),
            "experiment_type": row["experiment_type"],
            "experiment_score": round(experiment_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "critical_assumption_fit": row["critical_assumption_fit"],
            "evidence_standard_quality": row["evidence_standard_quality"],
            "learning_value": row["learning_value"],
            "decision_linkage": row["decision_linkage"],
            "resource_fit": row["resource_fit"],
            "scale_relevance": row["scale_relevance"],
            "ethical_review": row["ethical_review"],
        }
    )

experiment_rows.sort(key=lambda item: item["experiment_score"], reverse=True)
write_csv(TABLES / "experiment_portfolio_scores.csv", experiment_rows, list(experiment_rows[0].keys()))

# ---------------------------------------------------------------------
# 6. Timing responsiveness scoring
# ---------------------------------------------------------------------

timing_rows: list[dict[str, object]] = []

for row in timing:
    timing_score = (
        0.11 * f(row, "response_speed")
        + 0.16 * f(row, "signal_interpretation")
        + 0.15 * f(row, "noise_filtering")
        + 0.13 * f(row, "delay_awareness")
        + 0.14 * f(row, "revision_cadence")
        + 0.13 * f(row, "stakeholder_communication")
        + 0.18 * f(row, "stability_preservation")
    )

    whiplash_risk = (
        0.25 * f(row, "response_speed") * (1 - f(row, "noise_filtering"))
        + 0.20 * (1 - f(row, "signal_interpretation"))
        + 0.18 * (1 - f(row, "stability_preservation"))
        + 0.15 * (1 - f(row, "revision_cadence"))
        + 0.12 * (1 - f(row, "stakeholder_communication"))
        + 0.10 * (1 - f(row, "delay_awareness"))
    )

    if whiplash_risk >= 0.58:
        action = "reduce_reactive_whiplash"
    elif timing_score >= 0.72:
        action = "strong_timing_discipline"
    elif f(row, "response_speed") < 0.45:
        action = "increase_responsiveness"
    elif f(row, "noise_filtering") < 0.45:
        action = "improve_noise_filtering"
    else:
        action = "strengthen_timing_discipline"

    timing_rows.append(
        {
            "timing_id": row["timing_id"],
            "strategy_id": row["strategy_id"],
            "strategy_name": strategy_names.get(row["strategy_id"], row["strategy_id"]),
            "timing_issue": row["timing_issue"],
            "timing_discipline_score": round(timing_score, 4),
            "whiplash_risk": round(whiplash_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "response_speed": row["response_speed"],
            "signal_interpretation": row["signal_interpretation"],
            "noise_filtering": row["noise_filtering"],
            "delay_awareness": row["delay_awareness"],
            "revision_cadence": row["revision_cadence"],
            "stakeholder_communication": row["stakeholder_communication"],
            "stability_preservation": row["stability_preservation"],
        }
    )

timing_rows.sort(key=lambda item: item["timing_discipline_score"], reverse=True)
write_csv(TABLES / "timing_responsiveness_scores.csv", timing_rows, list(timing_rows[0].keys()))

# ---------------------------------------------------------------------
# 7. Exploration/exploitation portfolio balance
# ---------------------------------------------------------------------

portfolio_rows: list[dict[str, object]] = []

for row in portfolio:
    portfolio_score = (
        0.15 * f(row, "exploration_strength")
        + 0.15 * f(row, "exploitation_strength")
        + 0.18 * f(row, "balance_quality")
        + 0.14 * f(row, "option_value")
        + 0.13 * f(row, "resource_discipline")
        + 0.13 * f(row, "focus_quality")
        + 0.12 * f(row, "transition_path_quality")
    )

    imbalance = abs(f(row, "exploration_strength") - f(row, "exploitation_strength"))

    if portfolio_score >= 0.72:
        action = "strong_adaptive_portfolio_balance"
    elif imbalance >= 0.42 and f(row, "exploration_strength") > f(row, "exploitation_strength"):
        action = "add_selection_scaling_and_exploitation_discipline"
    elif imbalance >= 0.42:
        action = "add_exploration_and_option_value"
    elif f(row, "transition_path_quality") < 0.45:
        action = "improve_transition_path"
    else:
        action = "strengthen_portfolio_balance"

    portfolio_rows.append(
        {
            "portfolio_id": row["portfolio_id"],
            "strategy_id": row["strategy_id"],
            "strategy_name": strategy_names.get(row["strategy_id"], row["strategy_id"]),
            "portfolio_name": row["portfolio_name"],
            "portfolio_balance_score": round(portfolio_score, 4),
            "exploration_exploitation_imbalance": round(imbalance, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "exploration_strength": row["exploration_strength"],
            "exploitation_strength": row["exploitation_strength"],
            "balance_quality": row["balance_quality"],
            "option_value": row["option_value"],
            "resource_discipline": row["resource_discipline"],
            "focus_quality": row["focus_quality"],
            "transition_path_quality": row["transition_path_quality"],
        }
    )

portfolio_rows.sort(key=lambda item: item["portfolio_balance_score"], reverse=True)
write_csv(TABLES / "exploration_exploitation_scores.csv", portfolio_rows, list(portfolio_rows[0].keys()))

# ---------------------------------------------------------------------
# 8. Systems impact scoring
# ---------------------------------------------------------------------

impact_rows: list[dict[str, object]] = []

for row in impacts:
    systems_risk = (
        0.14 * f(row, "feedback_loop_risk")
        + 0.13 * f(row, "delay_risk")
        + 0.16 * f(row, "burden_shift_risk")
        + 0.15 * f(row, "capacity_risk")
        + 0.12 * f(row, "incentive_risk")
        + 0.14 * f(row, "scale_uncertainty")
        - 0.16 * f(row, "monitoring_quality")
    )

    if systems_risk >= 0.58:
        action = "systems_impact_review_required"
    elif f(row, "burden_shift_risk") >= 0.70:
        action = "burden_shift_review_required"
    elif f(row, "capacity_risk") >= 0.70:
        action = "capacity_review_required"
    elif f(row, "monitoring_quality") < 0.45:
        action = "improve_system_monitoring"
    else:
        action = "monitor_system_effects"

    impact_rows.append(
        {
            "impact_id": row["impact_id"],
            "strategy_id": row["strategy_id"],
            "strategy_name": strategy_names.get(row["strategy_id"], row["strategy_id"]),
            "systems_issue": row["systems_issue"],
            "systems_impact_risk": round(systems_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "feedback_loop_risk": row["feedback_loop_risk"],
            "delay_risk": row["delay_risk"],
            "burden_shift_risk": row["burden_shift_risk"],
            "capacity_risk": row["capacity_risk"],
            "incentive_risk": row["incentive_risk"],
            "scale_uncertainty": row["scale_uncertainty"],
            "monitoring_quality": row["monitoring_quality"],
        }
    )

impact_rows.sort(key=lambda item: item["systems_impact_risk"], reverse=True)
write_csv(TABLES / "systems_impact_scores.csv", impact_rows, list(impact_rows[0].keys()))

# ---------------------------------------------------------------------
# 9. Adaptive governance scoring
# ---------------------------------------------------------------------

governance_rows: list[dict[str, object]] = []

for row in governance:
    governance_score = (
        0.15 * f(row, "decision_rights_clarity")
        + 0.15 * f(row, "evidence_standard_quality")
        + 0.14 * f(row, "revision_authority_clarity")
        + 0.14 * f(row, "ethical_threshold_quality")
        + 0.13 * f(row, "stakeholder_review_quality")
        + 0.14 * f(row, "documentation_quality")
        + 0.15 * f(row, "accountability_quality")
    )

    if governance_score >= 0.72:
        action = "strong_adaptive_governance"
    elif f(row, "evidence_standard_quality") < 0.45:
        action = "define_evidence_standards"
    elif f(row, "revision_authority_clarity") < 0.45:
        action = "clarify_revision_authority"
    elif f(row, "ethical_threshold_quality") < 0.45:
        action = "add_ethical_thresholds"
    else:
        action = "strengthen_adaptive_governance"

    governance_rows.append(
        {
            "governance_id": row["governance_id"],
            "strategy_id": row["strategy_id"],
            "strategy_name": strategy_names.get(row["strategy_id"], row["strategy_id"]),
            "governance_practice": row["governance_practice"],
            "adaptive_governance_score": round(governance_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "decision_rights_clarity": row["decision_rights_clarity"],
            "evidence_standard_quality": row["evidence_standard_quality"],
            "revision_authority_clarity": row["revision_authority_clarity"],
            "ethical_threshold_quality": row["ethical_threshold_quality"],
            "stakeholder_review_quality": row["stakeholder_review_quality"],
            "documentation_quality": row["documentation_quality"],
            "accountability_quality": row["accountability_quality"],
        }
    )

governance_rows.sort(key=lambda item: item["adaptive_governance_score"], reverse=True)
write_csv(TABLES / "adaptive_governance_scores.csv", governance_rows, list(governance_rows[0].keys()))

# ---------------------------------------------------------------------
# 10. Learning memory scoring
# ---------------------------------------------------------------------

memory_rows: list[dict[str, object]] = []

for row in memory:
    memory_score = (
        0.14 * f(row, "assumption_record_quality")
        + 0.14 * f(row, "feedback_record_quality")
        + 0.15 * f(row, "interpretation_quality")
        + 0.15 * f(row, "revision_rationale_quality")
        + 0.14 * f(row, "decision_traceability")
        + 0.14 * f(row, "remaining_uncertainty_quality")
        + 0.14 * f(row, "reuse_quality")
    )

    if memory_score >= 0.72:
        action = "strong_adaptive_learning_memory"
    elif f(row, "revision_rationale_quality") < 0.45:
        action = "document_revision_rationale"
    elif f(row, "remaining_uncertainty_quality") < 0.45:
        action = "document_remaining_uncertainty"
    elif f(row, "decision_traceability") < 0.45:
        action = "improve_decision_traceability"
    else:
        action = "strengthen_learning_memory"

    memory_rows.append(
        {
            "memory_id": row["memory_id"],
            "strategy_id": row["strategy_id"],
            "strategy_name": strategy_names.get(row["strategy_id"], row["strategy_id"]),
            "memory_practice": row["memory_practice"],
            "learning_memory_score": round(memory_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "assumption_record_quality": row["assumption_record_quality"],
            "feedback_record_quality": row["feedback_record_quality"],
            "interpretation_quality": row["interpretation_quality"],
            "revision_rationale_quality": row["revision_rationale_quality"],
            "decision_traceability": row["decision_traceability"],
            "remaining_uncertainty_quality": row["remaining_uncertainty_quality"],
            "reuse_quality": row["reuse_quality"],
        }
    )

memory_rows.sort(key=lambda item: item["learning_memory_score"], reverse=True)
write_csv(TABLES / "learning_memory_scores.csv", memory_rows, list(memory_rows[0].keys()))

# ---------------------------------------------------------------------
# 11. Strategist report
# ---------------------------------------------------------------------

top_profiles = profile_rows[:5]
highest_over_adaptation = sorted(profile_rows, key=lambda item: item["over_adaptation_risk"], reverse=True)[:5]
top_signals = signal_rows[:6]
assumption_revisions = assumption_rows[:6]
top_triggers = trigger_rows[:6]
weak_triggers = sorted(trigger_rows, key=lambda item: item["trigger_condition_score"])[:4]
top_experiments = experiment_rows[:6]
weak_experiments = sorted(experiment_rows, key=lambda item: item["experiment_score"])[:4]
timing_review = timing_rows[:6]
whiplash_risks = sorted(timing_rows, key=lambda item: item["whiplash_risk"], reverse=True)[:5]
top_portfolios = portfolio_rows[:6]
systems_risks = impact_rows[:6]
top_governance = governance_rows[:6]
weak_governance = sorted(governance_rows, key=lambda item: item["adaptive_governance_score"])[:4]
top_memory = memory_rows[:6]
low_memory = sorted(memory_rows, key=lambda item: item["learning_memory_score"])[:4]

report: list[str] = []
report.append("# Adaptive Strategy and Iteration Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic evaluates adaptive strategy as disciplined learning under changing conditions. It assesses flexibility, learning capacity, exploration, "
    "exploitation balance, coherence, feedback intelligence, governance, systems awareness, trigger conditions, experiments, timing discipline, systems impacts, "
    "over-adaptation risk, and learning memory."
)

report.append("")
report.append("## Strongest adaptive strategy profiles")
report.append("")
for item in top_profiles:
    report.append(
        f"- **{item['strategy_id']} — {item['strategy_name']}**: adaptive score {item['adaptive_strategy_score']}; "
        f"over-adaptation risk {item['over_adaptation_risk']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest over-adaptation or reactivity risks")
report.append("")
for item in highest_over_adaptation:
    report.append(
        f"- **{item['strategy_id']} — {item['strategy_name']}**: over-adaptation risk {item['over_adaptation_risk']}; "
        f"diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Priority feedback signals")
report.append("")
for item in top_signals:
    report.append(
        f"- **{item['signal_id']} — {item['signal_type']}**: priority {item['response_priority']}; "
        f"signal value {item['signal_value']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Assumptions requiring review")
report.append("")
for item in assumption_revisions:
    report.append(
        f"- **{item['assumption_id']} — {item['assumption']}**: revision need {item['revision_need']}; "
        f"readiness {item['readiness_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strong trigger conditions")
report.append("")
for item in top_triggers:
    report.append(
        f"- **{item['trigger_id']} — {item['trigger_name']}**: trigger score {item['trigger_condition_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weak trigger-condition warnings")
report.append("")
for item in weak_triggers:
    report.append(
        f"- **{item['trigger_id']} — {item['trigger_name']}**: trigger score {item['trigger_condition_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strategic experiments")
report.append("")
for item in top_experiments:
    report.append(
        f"- **{item['experiment_id']} — {item['experiment_type']}**: experiment score {item['experiment_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weak experiment-design warnings")
report.append("")
for item in weak_experiments:
    report.append(
        f"- **{item['experiment_id']} — {item['experiment_type']}**: experiment score {item['experiment_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Timing discipline")
report.append("")
for item in timing_review:
    report.append(
        f"- **{item['timing_id']} — {item['timing_issue']}**: timing score {item['timing_discipline_score']}; "
        f"whiplash risk {item['whiplash_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest whiplash risks")
report.append("")
for item in whiplash_risks:
    report.append(
        f"- **{item['timing_id']} — {item['timing_issue']}**: whiplash risk {item['whiplash_risk']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Portfolio balance")
report.append("")
for item in top_portfolios:
    report.append(
        f"- **{item['portfolio_id']} — {item['portfolio_name']}**: portfolio score {item['portfolio_balance_score']}; "
        f"imbalance {item['exploration_exploitation_imbalance']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Systems impact risks")
report.append("")
for item in systems_risks:
    report.append(
        f"- **{item['impact_id']} — {item['systems_issue']}**: systems risk {item['systems_impact_risk']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Adaptive governance")
report.append("")
for item in top_governance:
    report.append(
        f"- **{item['governance_id']} — {item['governance_practice']}**: governance score {item['adaptive_governance_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weak governance warnings")
report.append("")
for item in weak_governance:
    report.append(
        f"- **{item['governance_id']} — {item['governance_practice']}**: governance score {item['adaptive_governance_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Learning memory")
report.append("")
for item in top_memory:
    report.append(
        f"- **{item['memory_id']} — {item['memory_practice']}**: memory score {item['learning_memory_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Low learning-memory warnings")
report.append("")
for item in low_memory:
    report.append(
        f"- **{item['memory_id']} — {item['memory_practice']}**: memory score {item['learning_memory_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "Adaptive strategy is strongest when flexibility is balanced by learning capacity, coherence, feedback intelligence, governance, systems awareness, and decision memory. "
    "Static strategies risk assumption decay, while reactive strategies risk over-adaptation and strategic whiplash. Disciplined adaptation preserves strategic intent while revising pathways through interpreted evidence."
)

(REPORTS / "adaptive_strategy_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_profiles": top_profiles,
    "highest_over_adaptation": highest_over_adaptation,
    "top_signals": top_signals,
    "assumption_revisions": assumption_revisions,
    "top_triggers": top_triggers,
    "weak_triggers": weak_triggers,
    "top_experiments": top_experiments,
    "weak_experiments": weak_experiments,
    "timing_review": timing_review,
    "whiplash_risks": whiplash_risks,
    "top_portfolios": top_portfolios,
    "systems_risks": systems_risks,
    "top_governance": top_governance,
    "weak_governance": weak_governance,
    "top_memory": top_memory,
    "low_memory": low_memory,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced adaptive strategy and iteration diagnostics complete.")
print(f"Wrote: {TABLES / 'adaptive_strategy_profile_scores.csv'}")
print(f"Wrote: {TABLES / 'feedback_signal_scores.csv'}")
print(f"Wrote: {TABLES / 'assumption_revision_scores.csv'}")
print(f"Wrote: {TABLES / 'trigger_condition_scores.csv'}")
print(f"Wrote: {TABLES / 'experiment_portfolio_scores.csv'}")
print(f"Wrote: {TABLES / 'timing_responsiveness_scores.csv'}")
print(f"Wrote: {TABLES / 'exploration_exploitation_scores.csv'}")
print(f"Wrote: {TABLES / 'systems_impact_scores.csv'}")
print(f"Wrote: {TABLES / 'adaptive_governance_scores.csv'}")
print(f"Wrote: {TABLES / 'learning_memory_scores.csv'}")
print(f"Wrote: {REPORTS / 'adaptive_strategy_diagnostic_report.md'}")
