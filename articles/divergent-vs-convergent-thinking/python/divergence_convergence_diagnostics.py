#!/usr/bin/env python3
"""
Advanced strategist-facing divergence-convergence diagnostics.

This dependency-light workflow uses only the Python standard library.

It produces:
- divergence-convergence process profiles
- premature convergence risk
- unbounded divergence risk
- criteria quality review
- constraint classification
- idea portfolio scores
- selection integrity review
- stakeholder inclusion review
- iteration and learning register
- a markdown strategist diagnostic report

The workflow is designed for strategy teams that need to govern movement
between possibility and commitment.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean

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


def bool_text(value: str) -> bool:
    return value.strip().lower() == "true"


contexts = read_csv(RAW / "ideation_contexts.csv")
ideas = read_csv(RAW / "idea_portfolio.csv")
criteria = read_csv(RAW / "evaluation_criteria.csv")
constraints = read_csv(RAW / "constraint_register.csv")
rounds = read_csv(RAW / "evaluation_rounds.csv")
cycles = read_csv(RAW / "learning_cycles.csv")
stakeholders = read_csv(RAW / "stakeholder_review.csv")

context_names = {row["context_id"]: row["context_name"] for row in contexts}

# ---------------------------------------------------------------------
# 1. Divergence-convergence profile
# ---------------------------------------------------------------------

profile_rows: list[dict[str, object]] = []

for row in contexts:
    profile_score = (
        0.16 * f(row, "exploratory_breadth")
        + 0.16 * f(row, "evaluative_discipline")
        + 0.18 * f(row, "iteration_quality")
        + 0.14 * f(row, "constraint_clarity")
        + 0.12 * f(row, "stakeholder_inclusion")
        + 0.12 * f(row, "evidence_contact")
        + 0.08 * f(row, "action_readiness")
        + 0.04 * f(row, "decision_memory_quality")
    )

    premature_convergence_risk = (1 - f(row, "exploratory_breadth")) * f(row, "closure_pressure")
    unbounded_divergence_risk = f(row, "exploratory_breadth") * (1 - f(row, "evaluative_discipline"))
    legitimacy_gap = max(0.0, f(row, "evaluative_discipline") - f(row, "stakeholder_inclusion"))
    learning_gap = max(0.0, 0.70 - f(row, "iteration_quality"))

    if premature_convergence_risk >= 0.55:
        diagnosis = "premature_convergence_risk"
    elif unbounded_divergence_risk >= 0.55:
        diagnosis = "unbounded_divergence_risk"
    elif legitimacy_gap >= 0.35:
        diagnosis = "power_or_inclusion_gap"
    elif learning_gap >= 0.25:
        diagnosis = "weak_iteration_capacity"
    elif profile_score >= 0.70:
        diagnosis = "balanced_and_adaptive"
    else:
        diagnosis = "requires_process_review"

    profile_rows.append(
        {
            "context_id": row["context_id"],
            "context_name": row["context_name"],
            "context_type": row["context_type"],
            "divergence_convergence_profile_score": round(profile_score, 4),
            "premature_convergence_risk": round(premature_convergence_risk, 4),
            "unbounded_divergence_risk": round(unbounded_divergence_risk, 4),
            "legitimacy_gap": round(legitimacy_gap, 4),
            "learning_gap": round(learning_gap, 4),
            "diagnosis": diagnosis,
            "exploratory_breadth": row["exploratory_breadth"],
            "evaluative_discipline": row["evaluative_discipline"],
            "iteration_quality": row["iteration_quality"],
            "constraint_clarity": row["constraint_clarity"],
            "stakeholder_inclusion": row["stakeholder_inclusion"],
            "evidence_contact": row["evidence_contact"],
            "action_readiness": row["action_readiness"],
            "decision_memory_quality": row["decision_memory_quality"],
            "closure_pressure": row["closure_pressure"],
        }
    )

profile_rows.sort(key=lambda item: item["divergence_convergence_profile_score"], reverse=True)

write_csv(
    TABLES / "divergence_convergence_profiles.csv",
    profile_rows,
    [
        "context_id",
        "context_name",
        "context_type",
        "divergence_convergence_profile_score",
        "premature_convergence_risk",
        "unbounded_divergence_risk",
        "legitimacy_gap",
        "learning_gap",
        "diagnosis",
        "exploratory_breadth",
        "evaluative_discipline",
        "iteration_quality",
        "constraint_clarity",
        "stakeholder_inclusion",
        "evidence_contact",
        "action_readiness",
        "decision_memory_quality",
        "closure_pressure",
    ],
)

write_csv(
    PROCESSED / "divergence_convergence_profiles.csv",
    profile_rows,
    [
        "context_id",
        "context_name",
        "context_type",
        "divergence_convergence_profile_score",
        "premature_convergence_risk",
        "unbounded_divergence_risk",
        "legitimacy_gap",
        "learning_gap",
        "diagnosis",
        "exploratory_breadth",
        "evaluative_discipline",
        "iteration_quality",
        "constraint_clarity",
        "stakeholder_inclusion",
        "evidence_contact",
        "action_readiness",
        "decision_memory_quality",
        "closure_pressure",
    ],
)

# ---------------------------------------------------------------------
# 2. Premature convergence and unbounded divergence tables
# ---------------------------------------------------------------------

premature_rows = sorted(
    [
        {
            "context_id": row["context_id"],
            "context_name": row["context_name"],
            "premature_convergence_risk": row["premature_convergence_risk"],
            "diagnosis": row["diagnosis"],
            "recommended_action": "protect_exploration_before_selection"
            if float(row["premature_convergence_risk"]) >= 0.55
            else "monitor",
        }
        for row in profile_rows
    ],
    key=lambda item: float(item["premature_convergence_risk"]),
    reverse=True,
)

unbounded_rows = sorted(
    [
        {
            "context_id": row["context_id"],
            "context_name": row["context_name"],
            "unbounded_divergence_risk": row["unbounded_divergence_risk"],
            "diagnosis": row["diagnosis"],
            "recommended_action": "define_convergence_gates_and_thresholds"
            if float(row["unbounded_divergence_risk"]) >= 0.55
            else "monitor",
        }
        for row in profile_rows
    ],
    key=lambda item: float(item["unbounded_divergence_risk"]),
    reverse=True,
)

write_csv(
    TABLES / "premature_convergence_risk.csv",
    premature_rows,
    ["context_id", "context_name", "premature_convergence_risk", "diagnosis", "recommended_action"],
)

write_csv(
    TABLES / "unbounded_divergence_risk.csv",
    unbounded_rows,
    ["context_id", "context_name", "unbounded_divergence_risk", "diagnosis", "recommended_action"],
)

# ---------------------------------------------------------------------
# 3. Criteria quality review
# ---------------------------------------------------------------------

criteria_rows: list[dict[str, object]] = []

for row in criteria:
    criteria_quality = (
        0.24 * f(row, "definition_clarity")
        + 0.18 * f(row, "weight_justification")
        + 0.20 * f(row, "measurement_validity")
        - 0.18 * f(row, "bias_risk")
        + 0.16 * f(row, "stakeholder_relevance")
        + 0.12 * f(row, "strategic_importance")
    )

    if f(row, "bias_risk") >= 0.70:
        action = "audit_criterion_for_bias"
    elif f(row, "measurement_validity") < 0.45:
        action = "repair_measurement_validity"
    elif f(row, "stakeholder_relevance") < 0.35:
        action = "add_stakeholder_relevance_review"
    elif criteria_quality < 0.45:
        action = "criteria_review_needed"
    else:
        action = "criteria_manageable"

    criteria_rows.append(
        {
            "criteria_id": row["criteria_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "criterion_name": row["criterion_name"],
            "criteria_quality_score": round(criteria_quality, 4),
            "recommended_action": action,
            "review_priority": row["review_priority"],
            "definition_clarity": row["definition_clarity"],
            "weight_justification": row["weight_justification"],
            "measurement_validity": row["measurement_validity"],
            "bias_risk": row["bias_risk"],
            "stakeholder_relevance": row["stakeholder_relevance"],
            "strategic_importance": row["strategic_importance"],
        }
    )

criteria_rows.sort(key=lambda item: item["criteria_quality_score"])

write_csv(
    TABLES / "criteria_quality_review.csv",
    criteria_rows,
    [
        "criteria_id",
        "context_id",
        "context_name",
        "criterion_name",
        "criteria_quality_score",
        "recommended_action",
        "review_priority",
        "definition_clarity",
        "weight_justification",
        "measurement_validity",
        "bias_risk",
        "stakeholder_relevance",
        "strategic_importance",
    ],
)

# ---------------------------------------------------------------------
# 4. Constraint classification
# ---------------------------------------------------------------------

constraint_rows: list[dict[str, object]] = []

for row in constraints:
    real = bool_text(row["is_real_constraint"])
    if real:
        priority = f(row, "strategic_importance") * f(row, "certainty") * (1 - f(row, "redesign_potential"))
        classification = "real_constraint"
    else:
        priority = f(row, "strategic_importance") * f(row, "redesign_potential") * (1 - f(row, "evidence_quality") + 0.25)
        classification = "assumed_constraint"

    if not real and priority >= 0.55:
        action = "challenge_before_convergence"
    elif real and priority >= 0.55:
        action = "respect_and_design_around"
    elif not real:
        action = "review_assumption_status"
    else:
        action = "monitor"

    constraint_rows.append(
        {
            "constraint_id": row["constraint_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "constraint_name": row["constraint_name"],
            "constraint_type": row["constraint_type"],
            "classification": classification,
            "constraint_priority": round(priority, 4),
            "recommended_action": action,
            "certainty": row["certainty"],
            "strategic_importance": row["strategic_importance"],
            "redesign_potential": row["redesign_potential"],
            "evidence_quality": row["evidence_quality"],
            "notes": row["notes"],
        }
    )

constraint_rows.sort(key=lambda item: item["constraint_priority"], reverse=True)

write_csv(
    TABLES / "constraint_classification_review.csv",
    constraint_rows,
    [
        "constraint_id",
        "context_id",
        "context_name",
        "constraint_name",
        "constraint_type",
        "classification",
        "constraint_priority",
        "recommended_action",
        "certainty",
        "strategic_importance",
        "redesign_potential",
        "evidence_quality",
        "notes",
    ],
)

# ---------------------------------------------------------------------
# 5. Idea portfolio scoring
# ---------------------------------------------------------------------

idea_rows: list[dict[str, object]] = []

for row in ideas:
    option_score = (
        0.12 * f(row, "novelty")
        + 0.18 * f(row, "strategic_fit")
        + 0.14 * f(row, "evidence_strength")
        + 0.12 * f(row, "feasibility")
        + 0.14 * f(row, "stakeholder_value")
        + 0.10 * f(row, "risk_visibility")
        + 0.12 * f(row, "ethical_legitimacy")
        + 0.10 * f(row, "implementation_readiness")
        - 0.08 * f(row, "assumption_burden")
    )

    if option_score >= 0.72:
        recommendation = "advance_to_evidence_gate"
    elif f(row, "stakeholder_value") < 0.35 or f(row, "ethical_legitimacy") < 0.35:
        recommendation = "stakeholder_or_ethics_review_before_advancing"
    elif f(row, "assumption_burden") >= 0.60:
        recommendation = "assumption_mapping_required"
    elif option_score >= 0.58:
        recommendation = "revise_and_retest"
    else:
        recommendation = "hold_or_reframe"

    idea_rows.append(
        {
            "idea_id": row["idea_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "idea_name": row["idea_name"],
            "idea_score": round(option_score, 4),
            "recommendation": recommendation,
            "novelty": row["novelty"],
            "strategic_fit": row["strategic_fit"],
            "evidence_strength": row["evidence_strength"],
            "feasibility": row["feasibility"],
            "stakeholder_value": row["stakeholder_value"],
            "risk_visibility": row["risk_visibility"],
            "ethical_legitimacy": row["ethical_legitimacy"],
            "implementation_readiness": row["implementation_readiness"],
            "assumption_burden": row["assumption_burden"],
        }
    )

idea_rows.sort(key=lambda item: item["idea_score"], reverse=True)

write_csv(
    TABLES / "idea_portfolio_scores.csv",
    idea_rows,
    [
        "idea_id",
        "context_id",
        "context_name",
        "idea_name",
        "idea_score",
        "recommendation",
        "novelty",
        "strategic_fit",
        "evidence_strength",
        "feasibility",
        "stakeholder_value",
        "risk_visibility",
        "ethical_legitimacy",
        "implementation_readiness",
        "assumption_burden",
    ],
)

# ---------------------------------------------------------------------
# 6. Selection integrity review
# ---------------------------------------------------------------------

round_rows: list[dict[str, object]] = []

for row in rounds:
    selection_integrity = (
        0.16 * f(row, "mode_clarity")
        + 0.14 * f(row, "participation_quality")
        + 0.18 * f(row, "criteria_transparency")
        + 0.18 * f(row, "evidence_use")
        + 0.14 * f(row, "stakeholder_voice")
        + 0.10 * f(row, "decision_documentation")
        + 0.10 * f(row, "iteration_trigger_quality")
    )

    if f(row, "mode_clarity") < 0.50:
        action = "clarify_current_mode"
    elif f(row, "criteria_transparency") < 0.45:
        action = "make_selection_criteria_explicit"
    elif f(row, "stakeholder_voice") < 0.35:
        action = "add_stakeholder_voice_before_selection"
    elif selection_integrity < 0.50:
        action = "selection_integrity_review"
    else:
        action = "selection_process_manageable"

    round_rows.append(
        {
            "round_id": row["round_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "round_name": row["round_name"],
            "mode": row["mode"],
            "selection_integrity_score": round(selection_integrity, 4),
            "recommended_action": action,
            "mode_clarity": row["mode_clarity"],
            "participation_quality": row["participation_quality"],
            "criteria_transparency": row["criteria_transparency"],
            "evidence_use": row["evidence_use"],
            "stakeholder_voice": row["stakeholder_voice"],
            "decision_documentation": row["decision_documentation"],
            "iteration_trigger_quality": row["iteration_trigger_quality"],
        }
    )

round_rows.sort(key=lambda item: item["selection_integrity_score"])

write_csv(
    TABLES / "selection_integrity_review.csv",
    round_rows,
    [
        "round_id",
        "context_id",
        "context_name",
        "round_name",
        "mode",
        "selection_integrity_score",
        "recommended_action",
        "mode_clarity",
        "participation_quality",
        "criteria_transparency",
        "evidence_use",
        "stakeholder_voice",
        "decision_documentation",
        "iteration_trigger_quality",
    ],
)

# ---------------------------------------------------------------------
# 7. Stakeholder inclusion review
# ---------------------------------------------------------------------

stakeholder_rows: list[dict[str, object]] = []

for row in stakeholders:
    inclusion_score = (
        0.18 * f(row, "inclusion_level")
        + 0.18 * f(row, "influence_on_criteria")
        + 0.18 * f(row, "influence_on_selection")
        + 0.14 * f(row, "burden_visibility")
        + 0.14 * f(row, "knowledge_recognition")
        + 0.10 * f(row, "legitimacy_signal")
        + 0.08 * f(row, "review_quality")
    )

    if f(row, "influence_on_selection") < 0.25:
        action = "give_stakeholders_influence_before_convergence"
    elif f(row, "burden_visibility") < 0.35:
        action = "add_burden_visibility_review"
    elif inclusion_score < 0.50:
        action = "stakeholder_inclusion_review"
    else:
        action = "inclusion_manageable"

    stakeholder_rows.append(
        {
            "review_id": row["review_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "stakeholder_group": row["stakeholder_group"],
            "stakeholder_inclusion_score": round(inclusion_score, 4),
            "recommended_action": action,
            "inclusion_level": row["inclusion_level"],
            "influence_on_criteria": row["influence_on_criteria"],
            "influence_on_selection": row["influence_on_selection"],
            "burden_visibility": row["burden_visibility"],
            "knowledge_recognition": row["knowledge_recognition"],
            "legitimacy_signal": row["legitimacy_signal"],
            "review_quality": row["review_quality"],
        }
    )

stakeholder_rows.sort(key=lambda item: item["stakeholder_inclusion_score"])

write_csv(
    TABLES / "stakeholder_inclusion_review.csv",
    stakeholder_rows,
    [
        "review_id",
        "context_id",
        "context_name",
        "stakeholder_group",
        "stakeholder_inclusion_score",
        "recommended_action",
        "inclusion_level",
        "influence_on_criteria",
        "influence_on_selection",
        "burden_visibility",
        "knowledge_recognition",
        "legitimacy_signal",
        "review_quality",
    ],
)

# ---------------------------------------------------------------------
# 8. Iteration and learning register
# ---------------------------------------------------------------------

cycle_rows: list[dict[str, object]] = []

for row in cycles:
    learning_score = (
        0.14 * f(row, "divergence_quality")
        + 0.14 * f(row, "convergence_quality")
        + 0.16 * f(row, "evidence_learning")
        + 0.14 * f(row, "frame_revision")
        + 0.12 * f(row, "assumption_revision")
        + 0.12 * f(row, "decision_memory")
        + 0.10 * f(row, "implementation_feedback")
        + 0.08 * f(row, "next_cycle_readiness")
    )

    if f(row, "frame_revision") < 0.45:
        action = "add_frame_revision_gate"
    elif f(row, "decision_memory") < 0.45:
        action = "create_decision_memory_record"
    elif learning_score < 0.55:
        action = "strengthen_iteration_cycle"
    else:
        action = "learning_cycle_manageable"

    cycle_rows.append(
        {
            "cycle_id": row["cycle_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "cycle_name": row["cycle_name"],
            "iteration_learning_score": round(learning_score, 4),
            "recommended_action": action,
            "divergence_quality": row["divergence_quality"],
            "convergence_quality": row["convergence_quality"],
            "evidence_learning": row["evidence_learning"],
            "frame_revision": row["frame_revision"],
            "assumption_revision": row["assumption_revision"],
            "decision_memory": row["decision_memory"],
            "implementation_feedback": row["implementation_feedback"],
            "next_cycle_readiness": row["next_cycle_readiness"],
        }
    )

cycle_rows.sort(key=lambda item: item["iteration_learning_score"], reverse=True)

write_csv(
    TABLES / "iteration_learning_register.csv",
    cycle_rows,
    [
        "cycle_id",
        "context_id",
        "context_name",
        "cycle_name",
        "iteration_learning_score",
        "recommended_action",
        "divergence_quality",
        "convergence_quality",
        "evidence_learning",
        "frame_revision",
        "assumption_revision",
        "decision_memory",
        "implementation_feedback",
        "next_cycle_readiness",
    ],
)

# ---------------------------------------------------------------------
# 9. Strategist report
# ---------------------------------------------------------------------

weakest_profiles = sorted(profile_rows, key=lambda item: item["divergence_convergence_profile_score"])[:5]
highest_premature = premature_rows[:5]
highest_unbounded = unbounded_rows[:5]
weakest_criteria = criteria_rows[:5]
highest_constraints = constraint_rows[:6]
top_ideas = idea_rows[:6]
weakest_selection = round_rows[:5]
weakest_stakeholders = stakeholder_rows[:5]
top_learning = cycle_rows[:5]

report: list[str] = []

report.append("# Divergence-Convergence Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic separates exploratory breadth, evaluative discipline, iteration quality, "
    "constraint clarity, stakeholder inclusion, evidence contact, action readiness, and decision memory. "
    "The purpose is to help strategists identify whether the process closes too early, remains too open, "
    "or governs the movement between possibility and commitment."
)
report.append("")
report.append("## Contexts requiring the most process review")
report.append("")

for item in weakest_profiles:
    report.append(
        f"- **{item['context_id']} — {item['context_name']}**: profile score {item['divergence_convergence_profile_score']}; "
        f"diagnosis: {item['diagnosis']}; premature risk {item['premature_convergence_risk']}; "
        f"unbounded risk {item['unbounded_divergence_risk']}."
    )

report.append("")
report.append("## Highest premature convergence risks")
report.append("")

for item in highest_premature:
    report.append(
        f"- **{item['context_id']} — {item['context_name']}**: risk {item['premature_convergence_risk']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest unbounded divergence risks")
report.append("")

for item in highest_unbounded:
    report.append(
        f"- **{item['context_id']} — {item['context_name']}**: risk {item['unbounded_divergence_risk']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weakest evaluation criteria")
report.append("")

for item in weakest_criteria:
    report.append(
        f"- **{item['criteria_id']} — {item['criterion_name']}** in **{item['context_name']}**: "
        f"quality score {item['criteria_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest-priority constraints")
report.append("")

for item in highest_constraints:
    report.append(
        f"- **{item['constraint_id']} — {item['constraint_name']}**: {item['classification']}; "
        f"priority {item['constraint_priority']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Top idea portfolio candidates")
report.append("")

for item in top_ideas:
    report.append(
        f"- **{item['idea_id']} — {item['idea_name']}**: score {item['idea_score']}; "
        f"recommendation: {item['recommendation']}."
    )

report.append("")
report.append("## Weakest selection-integrity rounds")
report.append("")

for item in weakest_selection:
    report.append(
        f"- **{item['round_id']} — {item['round_name']}** in **{item['context_name']}**: "
        f"selection integrity {item['selection_integrity_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weakest stakeholder inclusion reviews")
report.append("")

for item in weakest_stakeholders:
    report.append(
        f"- **{item['review_id']} — {item['stakeholder_group']}** in **{item['context_name']}**: "
        f"inclusion score {item['stakeholder_inclusion_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strongest learning cycles")
report.append("")

for item in top_learning:
    report.append(
        f"- **{item['cycle_id']} — {item['cycle_name']}**: learning score {item['iteration_learning_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "The value of this workflow is disciplined movement. It helps a strategist ask whether the process "
    "has generated enough meaningful variety, applied criteria fairly, classified constraints properly, "
    "included relevant stakeholders, used evidence, documented selection, and preserved the ability to iterate."
)

(REPORTS / "divergence_convergence_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "weakest_profiles": weakest_profiles,
    "highest_premature": highest_premature,
    "highest_unbounded": highest_unbounded,
    "weakest_criteria": weakest_criteria,
    "highest_constraints": highest_constraints,
    "top_ideas": top_ideas,
    "weakest_selection": weakest_selection,
    "weakest_stakeholders": weakest_stakeholders,
    "top_learning": top_learning,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced divergence-convergence diagnostics complete.")
print(f"Wrote: {TABLES / 'divergence_convergence_profiles.csv'}")
print(f"Wrote: {TABLES / 'premature_convergence_risk.csv'}")
print(f"Wrote: {TABLES / 'unbounded_divergence_risk.csv'}")
print(f"Wrote: {TABLES / 'criteria_quality_review.csv'}")
print(f"Wrote: {TABLES / 'selection_integrity_review.csv'}")
print(f"Wrote: {TABLES / 'stakeholder_inclusion_review.csv'}")
print(f"Wrote: {TABLES / 'iteration_learning_register.csv'}")
print(f"Wrote: {REPORTS / 'divergence_convergence_diagnostic_report.md'}")
