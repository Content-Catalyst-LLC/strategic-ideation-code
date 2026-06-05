#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Portfolio Thinking in Strategic Ideation.

This dependency-light workflow uses only the Python standard library.

It produces:
- portfolio idea scores
- role balance scores
- risk-learning scores
- capacity load scores
- dependency and sequencing scores
- time-horizon scores
- ethics and power scores
- governance review scores
- decision memory scores
- a markdown strategist diagnostic report
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
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


ideas = read_csv(RAW / "strategic_ideas.csv")
targets = read_csv(RAW / "portfolio_targets.csv")
risk_learning = read_csv(RAW / "risk_learning_profiles.csv")
capacity = read_csv(RAW / "capacity_load.csv")
dependencies = read_csv(RAW / "dependencies.csv")
time_horizons = read_csv(RAW / "time_horizons.csv")
ethics_power = read_csv(RAW / "ethics_power.csv")
governance = read_csv(RAW / "governance_review.csv")
memory = read_csv(RAW / "decision_memory.csv")

idea_names = {row["idea_id"]: row["idea_name"] for row in ideas}

# ---------------------------------------------------------------------
# 1. Strategic idea portfolio scoring
# ---------------------------------------------------------------------

idea_rows: list[dict[str, object]] = []

for row in ideas:
    portfolio_contribution = (
        0.17 * f(row, "impact")
        + 0.16 * f(row, "strategic_fit")
        + 0.15 * f(row, "learning_value")
        + 0.15 * f(row, "option_value")
        + 0.12 * f(row, "ethical_resilience")
        + 0.10 * f(row, "evidence_strength")
        + 0.08 * f(row, "governance_readiness")
        - 0.10 * f(row, "risk")
        - 0.08 * f(row, "capacity_demand")
        - 0.04 * min(f(row, "dependency_count") / 6.0, 1.0)
    )

    overload_warning = (
        0.30 * f(row, "capacity_demand")
        + 0.24 * f(row, "risk")
        + 0.14 * (1 - f(row, "strategic_fit"))
        + 0.12 * (1 - f(row, "ethical_resilience"))
        + 0.10 * (1 - f(row, "option_value"))
        + 0.10 * min(f(row, "dependency_count") / 6.0, 1.0)
    )

    if portfolio_contribution >= 0.66:
        diagnosis = "strong_portfolio_contribution"
    elif overload_warning >= 0.66:
        diagnosis = "high_overload_warning"
    elif f(row, "learning_value") >= 0.80:
        diagnosis = "high_learning_option"
    elif f(row, "option_value") >= 0.80:
        diagnosis = "high_option_value"
    elif f(row, "ethical_resilience") >= 0.82:
        diagnosis = "strong_ethics_or_legitimacy_role"
    elif f(row, "strategic_fit") < 0.52:
        diagnosis = "fit_gap"
    else:
        diagnosis = "developing_portfolio_role"

    idea_rows.append(
        {
            "idea_id": row["idea_id"],
            "idea_name": row["idea_name"],
            "role": row["role"],
            "time_horizon": row["time_horizon"],
            "portfolio_contribution": round(portfolio_contribution, 4),
            "overload_warning": round(overload_warning, 4),
            "diagnosis": diagnosis,
            "impact": row["impact"],
            "risk": row["risk"],
            "learning_value": row["learning_value"],
            "option_value": row["option_value"],
            "strategic_fit": row["strategic_fit"],
            "capacity_demand": row["capacity_demand"],
            "ethical_resilience": row["ethical_resilience"],
            "evidence_strength": row["evidence_strength"],
            "dependency_count": row["dependency_count"],
            "governance_readiness": row["governance_readiness"],
            "description": row["description"],
        }
    )

idea_rows.sort(key=lambda item: item["portfolio_contribution"], reverse=True)
write_csv(TABLES / "portfolio_idea_scores.csv", idea_rows, list(idea_rows[0].keys()))
write_csv(PROCESSED / "portfolio_idea_scores.csv", idea_rows, list(idea_rows[0].keys()))

# ---------------------------------------------------------------------
# 2. Role balance scoring
# ---------------------------------------------------------------------

role_counts = Counter(row["role"] for row in ideas)
total_ideas = len(ideas)
target_by_role = {row["role"]: row for row in targets}
role_balance_rows: list[dict[str, object]] = []

for target in targets:
    role = target["role"]
    current_share = role_counts.get(role, 0) / total_ideas
    target_share = f(target, "target_share")
    min_share = f(target, "minimum_share")
    max_share = f(target, "maximum_share")
    absolute_gap = abs(current_share - target_share)

    if current_share < min_share:
        diagnosis = "underrepresented"
    elif current_share > max_share:
        diagnosis = "overrepresented"
    elif absolute_gap <= 0.04:
        diagnosis = "well_balanced"
    else:
        diagnosis = "minor_balance_gap"

    role_balance_rows.append(
        {
            "role": role,
            "current_count": role_counts.get(role, 0),
            "current_share": round(current_share, 4),
            "target_share": round(target_share, 4),
            "minimum_share": round(min_share, 4),
            "maximum_share": round(max_share, 4),
            "absolute_gap": round(absolute_gap, 4),
            "diagnosis": diagnosis,
            "strategic_rationale": target["strategic_rationale"],
        }
    )

role_balance_rows.sort(key=lambda item: item["absolute_gap"], reverse=True)
write_csv(TABLES / "role_balance_scores.csv", role_balance_rows, list(role_balance_rows[0].keys()))

# ---------------------------------------------------------------------
# 3. Risk-learning profiles
# ---------------------------------------------------------------------

risk_learning_rows: list[dict[str, object]] = []

for row in risk_learning:
    exposure_score = (
        0.20 * f(row, "implementation_risk")
        + 0.22 * f(row, "strategic_risk")
        + 0.18 * f(row, "ethical_risk")
        + 0.18 * f(row, "systemic_risk")
        + 0.22 * f(row, "opportunity_cost")
    )

    learning_strength = (
        0.36 * f(row, "learning_quality")
        + 0.24 * f(row, "assumption_clarity")
        + 0.22 * (1 - f(row, "evidence_gap"))
        + 0.18 * (1 - exposure_score)
    )

    if exposure_score >= 0.66:
        action = "stage_or_reduce_exposure"
    elif learning_strength >= 0.70:
        action = "protect_learning_pathway"
    elif f(row, "evidence_gap") >= 0.56:
        action = "run_decision_relevant_experiment"
    else:
        action = row["review_action"]

    risk_learning_rows.append(
        {
            "profile_id": row["profile_id"],
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "exposure_score": round(exposure_score, 4),
            "learning_strength": round(learning_strength, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "implementation_risk": row["implementation_risk"],
            "strategic_risk": row["strategic_risk"],
            "ethical_risk": row["ethical_risk"],
            "systemic_risk": row["systemic_risk"],
            "opportunity_cost": row["opportunity_cost"],
            "learning_quality": row["learning_quality"],
            "assumption_clarity": row["assumption_clarity"],
            "evidence_gap": row["evidence_gap"],
        }
    )

risk_learning_rows.sort(key=lambda item: item["exposure_score"], reverse=True)
write_csv(TABLES / "risk_learning_scores.csv", risk_learning_rows, list(risk_learning_rows[0].keys()))

# ---------------------------------------------------------------------
# 4. Capacity load scores
# ---------------------------------------------------------------------

capacity_rows: list[dict[str, object]] = []

for row in capacity:
    gross_demand = (
        0.16 * f(row, "budget_demand")
        + 0.16 * f(row, "staff_demand")
        + 0.14 * f(row, "leadership_attention")
        + 0.14 * f(row, "technical_capacity_demand")
        + 0.14 * f(row, "governance_bandwidth")
        + 0.12 * f(row, "stakeholder_absorption")
        + 0.10 * f(row, "communication_load")
    )
    capacity_load = gross_demand / max(f(row, "available_capacity"), 0.01)

    if capacity_load >= 1.0:
        action = "over_capacity_stage_or_prune"
    elif capacity_load >= 0.82:
        action = "watch_capacity_load"
    elif f(row, "stakeholder_absorption") >= 0.68:
        action = "manage_stakeholder_fatigue"
    else:
        action = row["review_action"]

    capacity_rows.append(
        {
            "capacity_id": row["capacity_id"],
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "gross_demand": round(gross_demand, 4),
            "available_capacity": row["available_capacity"],
            "capacity_load": round(capacity_load, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "budget_demand": row["budget_demand"],
            "staff_demand": row["staff_demand"],
            "leadership_attention": row["leadership_attention"],
            "technical_capacity_demand": row["technical_capacity_demand"],
            "governance_bandwidth": row["governance_bandwidth"],
            "stakeholder_absorption": row["stakeholder_absorption"],
            "communication_load": row["communication_load"],
        }
    )

capacity_rows.sort(key=lambda item: item["capacity_load"], reverse=True)
write_csv(TABLES / "capacity_load_scores.csv", capacity_rows, list(capacity_rows[0].keys()))

# ---------------------------------------------------------------------
# 5. Dependency and sequencing scores
# ---------------------------------------------------------------------

dependency_rows: list[dict[str, object]] = []

for row in dependencies:
    sequence_priority = (
        0.30 * f(row, "dependency_strength")
        + 0.26 * f(row, "sequencing_urgency")
        + 0.24 * f(row, "readiness_gap")
        + 0.20 * f(row, "criticality")
    )

    if sequence_priority >= 0.68:
        action = "high_priority_sequence_dependency"
    elif f(row, "readiness_gap") >= 0.52:
        action = "close_readiness_gap_before_scaling"
    else:
        action = row["review_action"]

    dependency_rows.append(
        {
            "dependency_id": row["dependency_id"],
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "depends_on": row["depends_on"],
            "depends_on_name": idea_names.get(row["depends_on"], row["depends_on"]),
            "dependency_type": row["dependency_type"],
            "sequence_priority": round(sequence_priority, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "dependency_strength": row["dependency_strength"],
            "sequencing_urgency": row["sequencing_urgency"],
            "readiness_gap": row["readiness_gap"],
            "criticality": row["criticality"],
        }
    )

dependency_rows.sort(key=lambda item: item["sequence_priority"], reverse=True)
write_csv(TABLES / "dependency_sequence_scores.csv", dependency_rows, list(dependency_rows[0].keys()))

# ---------------------------------------------------------------------
# 6. Time horizon scores
# ---------------------------------------------------------------------

horizon_rows: list[dict[str, object]] = []

for row in time_horizons:
    future_value = (
        0.20 * f(row, "medium_term_value")
        + 0.30 * f(row, "long_term_value")
        + 0.24 * f(row, "intergenerational_value")
        + 0.16 * f(row, "deferred_value")
        + 0.10 * f(row, "short_term_value")
    )

    present_bias_warning = (
        0.40 * f(row, "near_term_pressure")
        + 0.26 * f(row, "immediate_value")
        + 0.18 * (1 - f(row, "long_term_value"))
        + 0.16 * (1 - f(row, "intergenerational_value"))
    )

    if future_value >= 0.76:
        action = "protect_long_horizon_value"
    elif present_bias_warning >= 0.62:
        action = "review_present_bias"
    else:
        action = row["review_action"]

    horizon_rows.append(
        {
            "horizon_id": row["horizon_id"],
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "future_value": round(future_value, 4),
            "present_bias_warning": round(present_bias_warning, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "immediate_value": row["immediate_value"],
            "short_term_value": row["short_term_value"],
            "medium_term_value": row["medium_term_value"],
            "long_term_value": row["long_term_value"],
            "intergenerational_value": row["intergenerational_value"],
            "near_term_pressure": row["near_term_pressure"],
            "deferred_value": row["deferred_value"],
        }
    )

horizon_rows.sort(key=lambda item: item["future_value"], reverse=True)
write_csv(TABLES / "time_horizon_scores.csv", horizon_rows, list(horizon_rows[0].keys()))

# ---------------------------------------------------------------------
# 7. Ethics and power scores
# ---------------------------------------------------------------------

ethics_rows: list[dict[str, object]] = []

for row in ethics_power:
    power_risk = (
        0.18 * f(row, "sponsor_power")
        + 0.18 * (1 - f(row, "affected_stakeholder_voice"))
        + 0.16 * f(row, "benefit_concentration")
        + 0.18 * f(row, "burden_concentration")
        + 0.12 * (1 - f(row, "transparency"))
        + 0.10 * (1 - f(row, "redress_quality"))
        + 0.08 * (1 - f(row, "long_term_responsibility"))
    )

    responsibility_score = (
        0.20 * f(row, "affected_stakeholder_voice")
        + 0.18 * f(row, "long_term_responsibility")
        + 0.18 * f(row, "transparency")
        + 0.18 * f(row, "redress_quality")
        + 0.14 * (1 - f(row, "burden_concentration"))
        + 0.12 * (1 - f(row, "benefit_concentration"))
    )

    if power_risk >= 0.62:
        action = "urgent_power_and_burden_review"
    elif f(row, "affected_stakeholder_voice") < 0.45:
        action = "expand_stakeholder_voice"
    elif f(row, "redress_quality") < 0.45:
        action = "define_redress_path"
    else:
        action = row["review_action"]

    ethics_rows.append(
        {
            "ethics_id": row["ethics_id"],
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "ethical_issue": row["ethical_issue"],
            "power_risk": round(power_risk, 4),
            "responsibility_score": round(responsibility_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "sponsor_power": row["sponsor_power"],
            "affected_stakeholder_voice": row["affected_stakeholder_voice"],
            "benefit_concentration": row["benefit_concentration"],
            "burden_concentration": row["burden_concentration"],
            "long_term_responsibility": row["long_term_responsibility"],
            "transparency": row["transparency"],
            "redress_quality": row["redress_quality"],
        }
    )

ethics_rows.sort(key=lambda item: item["power_risk"], reverse=True)
write_csv(TABLES / "ethics_power_scores.csv", ethics_rows, list(ethics_rows[0].keys()))

# ---------------------------------------------------------------------
# 8. Governance review scores
# ---------------------------------------------------------------------

governance_rows: list[dict[str, object]] = []

for row in governance:
    governance_score = (
        0.12 * f(row, "entry_rule_quality")
        + 0.12 * f(row, "review_cadence_quality")
        + 0.13 * f(row, "pruning_rule_quality")
        + 0.14 * f(row, "evidence_standard_quality")
        + 0.13 * f(row, "decision_rights_clarity")
        + 0.12 * f(row, "escalation_path_quality")
        + 0.12 * f(row, "decision_memory_quality")
        + 0.12 * f(row, "portfolio_visibility")
    )

    governance_gap = 1 - governance_score

    if governance_score >= 0.70:
        action = "strong_portfolio_governance"
    elif governance_gap >= 0.50:
        action = "build_portfolio_governance"
    elif f(row, "pruning_rule_quality") < 0.50:
        action = "define_pruning_rules"
    else:
        action = row["review_action"]

    governance_rows.append(
        {
            "governance_id": row["governance_id"],
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "governance_score": round(governance_score, 4),
            "governance_gap": round(governance_gap, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "entry_rule_quality": row["entry_rule_quality"],
            "review_cadence_quality": row["review_cadence_quality"],
            "pruning_rule_quality": row["pruning_rule_quality"],
            "evidence_standard_quality": row["evidence_standard_quality"],
            "decision_rights_clarity": row["decision_rights_clarity"],
            "escalation_path_quality": row["escalation_path_quality"],
            "decision_memory_quality": row["decision_memory_quality"],
            "portfolio_visibility": row["portfolio_visibility"],
        }
    )

governance_rows.sort(key=lambda item: item["governance_score"], reverse=True)
write_csv(TABLES / "governance_review_scores.csv", governance_rows, list(governance_rows[0].keys()))

# ---------------------------------------------------------------------
# 9. Decision memory scores
# ---------------------------------------------------------------------

memory_rows: list[dict[str, object]] = []

for row in memory:
    memory_score = (
        0.11 * f(row, "role_record_quality")
        + 0.12 * f(row, "evidence_record_quality")
        + 0.12 * f(row, "risk_record_quality")
        + 0.12 * f(row, "dependency_record_quality")
        + 0.11 * f(row, "capacity_record_quality")
        + 0.12 * f(row, "ethics_record_quality")
        + 0.11 * f(row, "decision_gate_record_quality")
        + 0.10 * f(row, "revision_history_quality")
        + 0.09 * f(row, "reuse_quality")
    )

    if memory_score >= 0.70:
        action = "strong_portfolio_memory"
    elif f(row, "role_record_quality") < 0.50:
        action = "document_portfolio_role"
    elif f(row, "decision_gate_record_quality") < 0.50:
        action = "document_decision_gates"
    elif f(row, "revision_history_quality") < 0.50:
        action = "document_revision_history"
    else:
        action = row["review_action"]

    memory_rows.append(
        {
            "memory_id": row["memory_id"],
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "memory_practice": row["memory_practice"],
            "decision_memory_score": round(memory_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "role_record_quality": row["role_record_quality"],
            "evidence_record_quality": row["evidence_record_quality"],
            "risk_record_quality": row["risk_record_quality"],
            "dependency_record_quality": row["dependency_record_quality"],
            "capacity_record_quality": row["capacity_record_quality"],
            "ethics_record_quality": row["ethics_record_quality"],
            "decision_gate_record_quality": row["decision_gate_record_quality"],
            "revision_history_quality": row["revision_history_quality"],
            "reuse_quality": row["reuse_quality"],
        }
    )

memory_rows.sort(key=lambda item: item["decision_memory_score"], reverse=True)
write_csv(TABLES / "decision_memory_scores.csv", memory_rows, list(memory_rows[0].keys()))

# ---------------------------------------------------------------------
# 10. Portfolio-level summary
# ---------------------------------------------------------------------

role_summary = defaultdict(list)
for row in idea_rows:
    role_summary[row["role"]].append(row)

time_summary = Counter(row["time_horizon"] for row in ideas)

portfolio_summary = {
    "idea_count": total_ideas,
    "average_portfolio_contribution": round(sum(float(row["portfolio_contribution"]) for row in idea_rows) / total_ideas, 4),
    "average_overload_warning": round(sum(float(row["overload_warning"]) for row in idea_rows) / total_ideas, 4),
    "role_counts": dict(role_counts),
    "time_horizon_counts": dict(time_summary),
    "highest_contribution_ideas": idea_rows[:5],
    "highest_overload_warnings": sorted(idea_rows, key=lambda item: item["overload_warning"], reverse=True)[:5],
    "role_balance_gaps": role_balance_rows[:5],
    "capacity_warnings": capacity_rows[:5],
    "dependency_priorities": dependency_rows[:5],
    "ethics_power_warnings": ethics_rows[:5],
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(portfolio_summary, indent=2), encoding="utf-8")

report: list[str] = []
report.append("# Portfolio Thinking in Strategic Ideation Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic evaluates a strategic idea portfolio across portfolio contribution, overload risk, role balance, risk-learning tradeoffs, capacity load, dependencies, time horizons, ethics and power, governance, and decision memory."
)
report.append("")
report.append(f"- Idea count: **{total_ideas}**")
report.append(f"- Average portfolio contribution: **{portfolio_summary['average_portfolio_contribution']}**")
report.append(f"- Average overload warning: **{portfolio_summary['average_overload_warning']}**")

report.append("")
report.append("## Strongest portfolio contributions")
report.append("")
for item in idea_rows[:6]:
    report.append(
        f"- **{item['idea_id']} — {item['idea_name']}**: contribution {item['portfolio_contribution']}; "
        f"overload {item['overload_warning']}; role: {item['role']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest overload warnings")
report.append("")
for item in sorted(idea_rows, key=lambda row: row["overload_warning"], reverse=True)[:6]:
    report.append(
        f"- **{item['idea_id']} — {item['idea_name']}**: overload {item['overload_warning']}; "
        f"capacity demand {item['capacity_demand']}; risk {item['risk']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Role balance gaps")
report.append("")
for item in role_balance_rows[:8]:
    report.append(
        f"- **{item['role']}**: current share {item['current_share']}; target {item['target_share']}; "
        f"gap {item['absolute_gap']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Risk-learning priorities")
report.append("")
for item in risk_learning_rows[:6]:
    report.append(
        f"- **{item['profile_id']} — {item['idea_name']}**: exposure {item['exposure_score']}; "
        f"learning strength {item['learning_strength']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Capacity load warnings")
report.append("")
for item in capacity_rows[:6]:
    report.append(
        f"- **{item['capacity_id']} — {item['idea_name']}**: capacity load {item['capacity_load']}; "
        f"gross demand {item['gross_demand']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Dependency and sequencing priorities")
report.append("")
for item in dependency_rows[:6]:
    report.append(
        f"- **{item['dependency_id']} — {item['idea_name']} depends on {item['depends_on_name']}**: "
        f"sequence priority {item['sequence_priority']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Long-horizon value")
report.append("")
for item in horizon_rows[:6]:
    report.append(
        f"- **{item['horizon_id']} — {item['idea_name']}**: future value {item['future_value']}; "
        f"present-bias warning {item['present_bias_warning']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Ethics and power warnings")
report.append("")
for item in ethics_rows[:6]:
    report.append(
        f"- **{item['ethics_id']} — {item['idea_name']}**: power risk {item['power_risk']}; "
        f"responsibility score {item['responsibility_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Governance strengths and gaps")
report.append("")
for item in governance_rows[:5]:
    report.append(
        f"- **{item['governance_id']} — {item['idea_name']}**: governance score {item['governance_score']}; "
        f"action: {item['recommended_action']}."
    )
for item in sorted(governance_rows, key=lambda row: row["governance_score"])[:4]:
    report.append(
        f"- **Governance gap — {item['idea_name']}**: governance score {item['governance_score']}; "
        f"gap {item['governance_gap']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Decision memory")
report.append("")
for item in memory_rows[:5]:
    report.append(
        f"- **{item['memory_id']} — {item['memory_practice']}**: memory score {item['decision_memory_score']}; "
        f"action: {item['recommended_action']}."
    )
for item in sorted(memory_rows, key=lambda row: row["decision_memory_score"])[:4]:
    report.append(
        f"- **Memory gap — {item['memory_practice']}**: memory score {item['decision_memory_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "Portfolio thinking is strongest when each idea has a clear strategic role, portfolio balance is visible, learning options are protected, capacity limits are respected, dependencies are sequenced, ethics and power are reviewed, and decision memory is preserved. The goal is not to fund every attractive idea; it is to build a coherent, adaptive, accountable idea system."
)

(REPORTS / "portfolio_thinking_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

print("Advanced portfolio thinking diagnostics complete.")
print(f"Wrote: {TABLES / 'portfolio_idea_scores.csv'}")
print(f"Wrote: {TABLES / 'role_balance_scores.csv'}")
print(f"Wrote: {TABLES / 'risk_learning_scores.csv'}")
print(f"Wrote: {TABLES / 'capacity_load_scores.csv'}")
print(f"Wrote: {TABLES / 'dependency_sequence_scores.csv'}")
print(f"Wrote: {TABLES / 'time_horizon_scores.csv'}")
print(f"Wrote: {TABLES / 'ethics_power_scores.csv'}")
print(f"Wrote: {TABLES / 'governance_review_scores.csv'}")
print(f"Wrote: {TABLES / 'decision_memory_scores.csv'}")
print(f"Wrote: {REPORTS / 'portfolio_thinking_diagnostic_report.md'}")
