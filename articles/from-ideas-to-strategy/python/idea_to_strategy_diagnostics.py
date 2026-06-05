#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for From Ideas to Strategy.

This dependency-light workflow uses only the Python standard library.

It produces:
- strategy conversion scores
- strategic fit scores
- integration readiness scores
- resource commitment scores
- alignment and coordination scores
- feedback and learning scores
- ethics and power scores
- governance review scores
- decision memory scores
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


initiatives = read_csv(RAW / "initiatives.csv")
strategic_fit = read_csv(RAW / "strategic_fit.csv")
integration = read_csv(RAW / "integration_readiness.csv")
resources = read_csv(RAW / "resource_commitment.csv")
alignment = read_csv(RAW / "alignment_coordination.csv")
feedback = read_csv(RAW / "feedback_learning.csv")
ethics_power = read_csv(RAW / "ethics_power.csv")
governance = read_csv(RAW / "governance_review.csv")
memory = read_csv(RAW / "decision_memory.csv")

initiative_names = {row["initiative_id"]: row["initiative_name"] for row in initiatives}

# ---------------------------------------------------------------------
# 1. Strategy conversion profile
# ---------------------------------------------------------------------

conversion_rows: list[dict[str, object]] = []

for row in initiatives:
    conversion_score = (
        0.14 * f(row, "feasibility")
        + 0.15 * f(row, "viability")
        + 0.13 * f(row, "desirability")
        - 0.11 * f(row, "integration_difficulty")
        + 0.15 * f(row, "execution_readiness")
        + 0.13 * f(row, "strategic_fit")
        + 0.08 * f(row, "evidence_confidence")
        + 0.08 * f(row, "ethical_resilience")
        - 0.07 * f(row, "resource_intensity")
        + 0.10 * f(row, "governance_readiness")
        + 0.06 * f(row, "learning_value")
    )

    confidence_adjusted = conversion_score * f(row, "evidence_confidence")
    implementation_warning = (
        0.32 * f(row, "integration_difficulty")
        + 0.26 * (1 - f(row, "execution_readiness"))
        + 0.16 * (1 - f(row, "governance_readiness"))
        + 0.14 * f(row, "resource_intensity")
        + 0.12 * (1 - f(row, "evidence_confidence"))
    )

    if f(row, "execution_readiness") < 0.50 and f(row, "integration_difficulty") > 0.65:
        diagnosis = "not_ready_for_strategy_commitment"
    elif f(row, "desirability") < 0.50:
        diagnosis = "weak_demand_or_desirability"
    elif implementation_warning >= 0.62:
        diagnosis = "implementation_review_required"
    elif conversion_score >= 0.62:
        diagnosis = "strong_strategy_conversion_candidate"
    elif f(row, "learning_value") >= 0.75:
        diagnosis = "protect_as_learning_pathway"
    else:
        diagnosis = "develop_before_commitment"

    conversion_rows.append(
        {
            "initiative_id": row["initiative_id"],
            "initiative_name": row["initiative_name"],
            "initiative_type": row["initiative_type"],
            "strategy_conversion_score": round(conversion_score, 4),
            "confidence_adjusted_score": round(confidence_adjusted, 4),
            "implementation_warning": round(implementation_warning, 4),
            "diagnosis": diagnosis,
            "feasibility": row["feasibility"],
            "viability": row["viability"],
            "desirability": row["desirability"],
            "integration_difficulty": row["integration_difficulty"],
            "execution_readiness": row["execution_readiness"],
            "strategic_fit": row["strategic_fit"],
            "evidence_confidence": row["evidence_confidence"],
            "ethical_resilience": row["ethical_resilience"],
            "resource_intensity": row["resource_intensity"],
            "governance_readiness": row["governance_readiness"],
            "learning_value": row["learning_value"],
            "description": row["description"],
        }
    )

conversion_rows.sort(key=lambda item: item["strategy_conversion_score"], reverse=True)
write_csv(TABLES / "strategy_conversion_scores.csv", conversion_rows, list(conversion_rows[0].keys()))
write_csv(PROCESSED / "strategy_conversion_scores.csv", conversion_rows, list(conversion_rows[0].keys()))

# ---------------------------------------------------------------------
# 2. Strategic fit and coherence
# ---------------------------------------------------------------------

fit_rows: list[dict[str, object]] = []

for row in strategic_fit:
    fit_score = (
        0.16 * f(row, "purpose_clarity")
        + 0.16 * f(row, "objective_alignment")
        + 0.14 * f(row, "portfolio_fit")
        + 0.13 * f(row, "capability_fit")
        + 0.12 * f(row, "time_horizon_fit")
        + 0.12 * f(row, "narrative_coherence")
        + 0.10 * f(row, "stakeholder_fit")
        + 0.07 * f(row, "opportunity_cost_clarity")
    )

    if fit_score >= 0.70:
        action = "strong_strategic_fit"
    elif f(row, "opportunity_cost_clarity") < 0.50:
        action = "clarify_opportunity_cost"
    elif f(row, "stakeholder_fit") < 0.50:
        action = "review_stakeholder_fit"
    else:
        action = row["review_action"]

    fit_rows.append(
        {
            "fit_id": row["fit_id"],
            "initiative_id": row["initiative_id"],
            "initiative_name": initiative_names[row["initiative_id"]],
            "strategic_fit_score": round(fit_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
        }
    )

fit_rows.sort(key=lambda item: item["strategic_fit_score"], reverse=True)
write_csv(TABLES / "strategic_fit_scores.csv", fit_rows, list(fit_rows[0].keys()))

# ---------------------------------------------------------------------
# 3. Integration readiness
# ---------------------------------------------------------------------

integration_rows: list[dict[str, object]] = []

for row in integration:
    readiness_score = (
        0.14 * f(row, "process_readiness")
        + 0.13 * f(row, "technology_readiness")
        + 0.13 * f(row, "role_clarity")
        + 0.13 * f(row, "governance_fit")
        + 0.12 * f(row, "culture_fit")
        + 0.12 * f(row, "stakeholder_absorption")
        + 0.12 * f(row, "data_readiness")
        - 0.11 * f(row, "dependency_complexity")
        + 0.12
    )

    if f(row, "dependency_complexity") >= 0.75:
        action = "sequence_dependencies_before_commitment"
    elif readiness_score >= 0.64:
        action = "integration_ready_or_manageable"
    elif f(row, "role_clarity") < 0.50:
        action = "clarify_roles_before_execution"
    else:
        action = row["review_action"]

    integration_rows.append(
        {
            "integration_id": row["integration_id"],
            "initiative_id": row["initiative_id"],
            "initiative_name": initiative_names[row["initiative_id"]],
            "integration_readiness_score": round(readiness_score, 4),
            "dependency_complexity": row["dependency_complexity"],
            "recommended_action": action,
            "source_review_action": row["review_action"],
        }
    )

integration_rows.sort(key=lambda item: item["integration_readiness_score"], reverse=True)
write_csv(TABLES / "integration_readiness_scores.csv", integration_rows, list(integration_rows[0].keys()))

# ---------------------------------------------------------------------
# 4. Resource commitment
# ---------------------------------------------------------------------

resource_rows: list[dict[str, object]] = []

for row in resources:
    commitment_score = (
        0.16 * f(row, "budget_commitment")
        + 0.16 * f(row, "staff_commitment")
        + 0.16 * f(row, "leadership_attention")
        + 0.13 * f(row, "authority_commitment")
        + 0.13 * f(row, "technical_capacity")
        + 0.12 * f(row, "communications_capacity")
        + 0.14 * f(row, "political_capital")
    )

    if row["commitment_stage"] == "exploratory":
        action = "keep_commitment_exploratory"
    elif commitment_score >= 0.66:
        action = "commitment_matches_strategy"
    elif f(row, "leadership_attention") < 0.50:
        action = "secure_leadership_attention"
    else:
        action = row["review_action"]

    resource_rows.append(
        {
            "resource_id": row["resource_id"],
            "initiative_id": row["initiative_id"],
            "initiative_name": initiative_names[row["initiative_id"]],
            "resource_commitment_score": round(commitment_score, 4),
            "commitment_stage": row["commitment_stage"],
            "recommended_action": action,
            "source_review_action": row["review_action"],
        }
    )

resource_rows.sort(key=lambda item: item["resource_commitment_score"], reverse=True)
write_csv(TABLES / "resource_commitment_scores.csv", resource_rows, list(resource_rows[0].keys()))

# ---------------------------------------------------------------------
# 5. Alignment and coordination
# ---------------------------------------------------------------------

alignment_rows: list[dict[str, object]] = []

for row in alignment:
    alignment_score = (
        0.14 * f(row, "purpose_alignment")
        + 0.13 * f(row, "role_alignment")
        + 0.13 * f(row, "incentive_alignment")
        + 0.12 * f(row, "communication_alignment")
        + 0.13 * f(row, "decision_rights_clarity")
        + 0.13 * f(row, "cross_function_coordination")
        + 0.12 * f(row, "stakeholder_alignment")
        + 0.10 * f(row, "dissent_capture")
    )

    if alignment_score >= 0.68:
        action = "strong_alignment"
    elif f(row, "decision_rights_clarity") < 0.50:
        action = "clarify_decision_rights"
    elif f(row, "role_alignment") < 0.50:
        action = "clarify_roles"
    else:
        action = row["review_action"]

    alignment_rows.append(
        {
            "alignment_id": row["alignment_id"],
            "initiative_id": row["initiative_id"],
            "initiative_name": initiative_names[row["initiative_id"]],
            "alignment_coordination_score": round(alignment_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
        }
    )

alignment_rows.sort(key=lambda item: item["alignment_coordination_score"], reverse=True)
write_csv(TABLES / "alignment_coordination_scores.csv", alignment_rows, list(alignment_rows[0].keys()))

# ---------------------------------------------------------------------
# 6. Feedback and learning
# ---------------------------------------------------------------------

feedback_rows: list[dict[str, object]] = []

for row in feedback:
    learning_score = (
        0.13 * f(row, "indicator_quality")
        + 0.12 * f(row, "feedback_frequency")
        + 0.14 * f(row, "assumption_tracking")
        + 0.14 * f(row, "revision_trigger_quality")
        + 0.13 * f(row, "after_action_learning")
        + 0.13 * f(row, "stakeholder_feedback")
        + 0.12 * f(row, "adaptation_capacity")
        + 0.09 * f(row, "drift_detection")
    )

    if learning_score >= 0.68:
        action = "strong_strategy_learning_loop"
    elif f(row, "revision_trigger_quality") < 0.50:
        action = "define_revision_triggers"
    elif f(row, "drift_detection") < 0.50:
        action = "build_drift_detection"
    else:
        action = row["review_action"]

    feedback_rows.append(
        {
            "feedback_id": row["feedback_id"],
            "initiative_id": row["initiative_id"],
            "initiative_name": initiative_names[row["initiative_id"]],
            "feedback_learning_score": round(learning_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
        }
    )

feedback_rows.sort(key=lambda item: item["feedback_learning_score"], reverse=True)
write_csv(TABLES / "feedback_learning_scores.csv", feedback_rows, list(feedback_rows[0].keys()))

# ---------------------------------------------------------------------
# 7. Ethics and power
# ---------------------------------------------------------------------

ethics_rows: list[dict[str, object]] = []

for row in ethics_power:
    power_risk = (
        0.16 * f(row, "sponsor_power")
        + 0.18 * (1 - f(row, "affected_stakeholder_voice"))
        + 0.16 * f(row, "benefit_concentration")
        + 0.18 * f(row, "burden_concentration")
        + 0.12 * (1 - f(row, "transparency"))
        + 0.10 * (1 - f(row, "redress_quality"))
        + 0.10 * (1 - f(row, "long_term_responsibility"))
    )
    responsibility_score = (
        0.18 * f(row, "affected_stakeholder_voice")
        + 0.17 * f(row, "transparency")
        + 0.17 * f(row, "redress_quality")
        + 0.18 * f(row, "long_term_responsibility")
        + 0.15 * (1 - f(row, "benefit_concentration"))
        + 0.15 * (1 - f(row, "burden_concentration"))
    )

    if power_risk >= 0.62:
        action = "urgent_ethics_and_power_review"
    elif f(row, "affected_stakeholder_voice") < 0.50:
        action = "increase_stakeholder_voice"
    else:
        action = row["review_action"]

    ethics_rows.append(
        {
            "ethics_id": row["ethics_id"],
            "initiative_id": row["initiative_id"],
            "initiative_name": initiative_names[row["initiative_id"]],
            "ethical_issue": row["ethical_issue"],
            "power_risk": round(power_risk, 4),
            "responsibility_score": round(responsibility_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
        }
    )

ethics_rows.sort(key=lambda item: item["power_risk"], reverse=True)
write_csv(TABLES / "ethics_power_scores.csv", ethics_rows, list(ethics_rows[0].keys()))

# ---------------------------------------------------------------------
# 8. Governance and decision memory
# ---------------------------------------------------------------------

governance_rows: list[dict[str, object]] = []

for row in governance:
    governance_score = (
        0.13 * f(row, "owner_clarity")
        + 0.14 * f(row, "decision_gate_quality")
        + 0.13 * f(row, "evidence_standard")
        + 0.12 * f(row, "review_cadence")
        + 0.12 * f(row, "escalation_path")
        + 0.12 * f(row, "stop_rule_quality")
        + 0.12 * f(row, "adaptation_authority")
        + 0.12 * f(row, "decision_memory_quality")
    )

    if governance_score >= 0.68:
        action = "strong_strategy_governance"
    elif f(row, "stop_rule_quality") < 0.50:
        action = "define_stop_rules"
    elif f(row, "decision_gate_quality") < 0.50:
        action = "strengthen_decision_gate"
    else:
        action = row["review_action"]

    governance_rows.append(
        {
            "governance_id": row["governance_id"],
            "initiative_id": row["initiative_id"],
            "initiative_name": initiative_names[row["initiative_id"]],
            "governance_score": round(governance_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
        }
    )

governance_rows.sort(key=lambda item: item["governance_score"], reverse=True)
write_csv(TABLES / "governance_review_scores.csv", governance_rows, list(governance_rows[0].keys()))

memory_rows: list[dict[str, object]] = []

for row in memory:
    memory_score = (
        0.10 * f(row, "purpose_record")
        + 0.10 * f(row, "evidence_record")
        + 0.10 * f(row, "tradeoff_record")
        + 0.10 * f(row, "capability_record")
        + 0.10 * f(row, "integration_record")
        + 0.10 * f(row, "resource_record")
        + 0.11 * f(row, "ethics_record")
        + 0.10 * f(row, "governance_record")
        + 0.10 * f(row, "revision_trigger_quality")
        + 0.09 * f(row, "reuse_quality")
    )

    if memory_score >= 0.70:
        action = "strong_decision_memory"
    elif f(row, "tradeoff_record") < 0.50:
        action = "document_tradeoffs"
    elif f(row, "governance_record") < 0.50:
        action = "document_governance_logic"
    else:
        action = row["review_action"]

    memory_rows.append(
        {
            "memory_id": row["memory_id"],
            "initiative_id": row["initiative_id"],
            "initiative_name": initiative_names[row["initiative_id"]],
            "memory_practice": row["memory_practice"],
            "decision_memory_score": round(memory_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
        }
    )

memory_rows.sort(key=lambda item: item["decision_memory_score"], reverse=True)
write_csv(TABLES / "decision_memory_scores.csv", memory_rows, list(memory_rows[0].keys()))

# ---------------------------------------------------------------------
# 9. Strategist report
# ---------------------------------------------------------------------

summary = {
    "highest_conversion_scores": conversion_rows[:5],
    "implementation_warnings": sorted(conversion_rows, key=lambda item: item["implementation_warning"], reverse=True)[:5],
    "strategic_fit": fit_rows[:5],
    "integration_readiness": integration_rows[:5],
    "resource_commitment": resource_rows[:5],
    "alignment": alignment_rows[:5],
    "feedback_learning": feedback_rows[:5],
    "ethics_power": ethics_rows[:5],
    "governance": governance_rows[:5],
    "decision_memory": memory_rows[:5],
}
(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

report: list[str] = []
report.append("# From Ideas to Strategy Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic evaluates initiatives across conversion strength, strategic fit, integration readiness, resource commitment, alignment and coordination, feedback and learning, ethics and power, governance, and decision memory."
)

report.append("")
report.append("## Strategy conversion candidates")
report.append("")
for item in conversion_rows:
    report.append(
        f"- **{item['initiative_id']} — {item['initiative_name']}**: conversion {item['strategy_conversion_score']}; "
        f"confidence-adjusted {item['confidence_adjusted_score']}; implementation warning {item['implementation_warning']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Strategic fit and coherence")
report.append("")
for item in fit_rows[:6]:
    report.append(
        f"- **{item['initiative_name']}**: strategic fit {item['strategic_fit_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Integration readiness")
report.append("")
for item in integration_rows[:6]:
    report.append(
        f"- **{item['initiative_name']}**: integration readiness {item['integration_readiness_score']}; "
        f"dependency complexity {item['dependency_complexity']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Resource commitment")
report.append("")
for item in resource_rows[:6]:
    report.append(
        f"- **{item['initiative_name']}**: commitment score {item['resource_commitment_score']}; "
        f"stage {item['commitment_stage']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Alignment and coordination")
report.append("")
for item in alignment_rows[:6]:
    report.append(
        f"- **{item['initiative_name']}**: alignment score {item['alignment_coordination_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Feedback and learning")
report.append("")
for item in feedback_rows[:6]:
    report.append(
        f"- **{item['initiative_name']}**: feedback-learning score {item['feedback_learning_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Ethics and power")
report.append("")
for item in ethics_rows[:6]:
    report.append(
        f"- **{item['initiative_name']}**: power risk {item['power_risk']}; "
        f"responsibility score {item['responsibility_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Governance")
report.append("")
for item in governance_rows[:6]:
    report.append(
        f"- **{item['initiative_name']}**: governance score {item['governance_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Decision memory")
report.append("")
for item in memory_rows[:6]:
    report.append(
        f"- **{item['initiative_name']}**: memory score {item['decision_memory_score']}; "
        f"practice: {item['memory_practice']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "Ideas become strategy when they develop enough purpose, evidence, feasibility, viability, integration readiness, resource commitment, governance, ethical responsibility, and feedback capacity to support coordinated action under constraint. Attractive ideas that lack execution readiness, decision gates, or integration logic should remain exploratory until the conversion conditions improve."
)

(REPORTS / "idea_to_strategy_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

print("Advanced idea-to-strategy diagnostics complete.")
print(f"Wrote: {TABLES / 'strategy_conversion_scores.csv'}")
print(f"Wrote: {TABLES / 'strategic_fit_scores.csv'}")
print(f"Wrote: {TABLES / 'integration_readiness_scores.csv'}")
print(f"Wrote: {TABLES / 'resource_commitment_scores.csv'}")
print(f"Wrote: {TABLES / 'alignment_coordination_scores.csv'}")
print(f"Wrote: {TABLES / 'feedback_learning_scores.csv'}")
print(f"Wrote: {TABLES / 'ethics_power_scores.csv'}")
print(f"Wrote: {TABLES / 'governance_review_scores.csv'}")
print(f"Wrote: {TABLES / 'decision_memory_scores.csv'}")
print(f"Wrote: {REPORTS / 'idea_to_strategy_diagnostic_report.md'}")
