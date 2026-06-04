#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for imagination, discipline, and strategic creativity.

This dependency-light workflow uses only the Python standard library.

It produces:
- strategic creativity scores
- novelty-depth review
- constraint audit
- stakeholder grounding review
- systems-fit review
- evidence pathway review
- idea maturation review
- creative portfolio review
- intervention recommendations
- a markdown strategist diagnostic report

The workflow is designed for strategy teams that need to distinguish
meaningful strategic creativity from novelty theater, premature convergence,
undisciplined imagination, or overdisciplined rejection.
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


ideas = read_csv(RAW / "creative_ideas.csv")
constraints = read_csv(RAW / "constraint_audit.csv")
stakeholders = read_csv(RAW / "stakeholder_reviews.csv")
systems = read_csv(RAW / "systems_fit.csv")
evidence = read_csv(RAW / "evidence_pathways.csv")
maturation = read_csv(RAW / "idea_maturation.csv")
portfolio = read_csv(RAW / "creative_portfolio.csv")
interventions = read_csv(RAW / "intervention_library.csv")

idea_names = {row["idea_id"]: row["idea_name"] for row in ideas}

# ---------------------------------------------------------------------
# 1. Strategic creativity scores
# ---------------------------------------------------------------------

creativity_rows: list[dict[str, object]] = []

for row in ideas:
    creativity_score = (
        0.14 * f(row, "novelty")
        + 0.16 * f(row, "strategic_relevance")
        + 0.13 * f(row, "conceptual_coherence")
        + 0.14 * f(row, "mechanism_clarity")
        + 0.11 * f(row, "testability")
        + 0.13 * f(row, "stakeholder_grounding")
        + 0.13 * f(row, "systems_fit")
        + 0.12 * f(row, "developmental_potential")
        + 0.08 * f(row, "revision_capacity")
        - 0.12 * f(row, "implementation_risk")
    )

    novelty_theater_risk = f(row, "novelty") * (
        1.0 - ((f(row, "mechanism_clarity") + f(row, "systems_fit") + f(row, "stakeholder_grounding")) / 3.0)
    )
    overdiscipline_risk = max(0.0, f(row, "strategic_relevance") - f(row, "developmental_potential")) * (1.0 - f(row, "revision_capacity"))
    stakeholder_gap = max(0.0, 0.65 - f(row, "stakeholder_grounding"))
    systems_gap = max(0.0, 0.70 - f(row, "systems_fit"))
    mechanism_gap = max(0.0, 0.70 - f(row, "mechanism_clarity"))

    if novelty_theater_risk >= 0.42:
        diagnosis = "novelty_theater_risk"
    elif f(row, "novelty") >= 0.70 and f(row, "mechanism_clarity") < 0.55:
        diagnosis = "undisciplined_novelty_risk"
    elif stakeholder_gap >= 0.25:
        diagnosis = "stakeholder_grounding_gap"
    elif systems_gap >= 0.25:
        diagnosis = "systems_fit_gap"
    elif mechanism_gap >= 0.25:
        diagnosis = "mechanism_clarity_gap"
    elif creativity_score >= 0.70:
        diagnosis = "strong_strategic_creativity_candidate"
    elif creativity_score >= 0.55:
        diagnosis = "develop_with_testing"
    else:
        diagnosis = "revise_or_reframe"

    creativity_rows.append(
        {
            "idea_id": row["idea_id"],
            "idea_name": row["idea_name"],
            "idea_type": row["idea_type"],
            "frame_family": row["frame_family"],
            "source_domain": row["source_domain"],
            "strategic_creativity_score": round(creativity_score, 4),
            "novelty_theater_risk": round(novelty_theater_risk, 4),
            "overdiscipline_risk": round(overdiscipline_risk, 4),
            "stakeholder_gap": round(stakeholder_gap, 4),
            "systems_gap": round(systems_gap, 4),
            "mechanism_gap": round(mechanism_gap, 4),
            "diagnosis": diagnosis,
            "novelty": row["novelty"],
            "strategic_relevance": row["strategic_relevance"],
            "conceptual_coherence": row["conceptual_coherence"],
            "mechanism_clarity": row["mechanism_clarity"],
            "testability": row["testability"],
            "stakeholder_grounding": row["stakeholder_grounding"],
            "systems_fit": row["systems_fit"],
            "developmental_potential": row["developmental_potential"],
            "implementation_risk": row["implementation_risk"],
            "revision_capacity": row["revision_capacity"],
            "description": row["description"],
        }
    )

creativity_rows.sort(key=lambda item: item["strategic_creativity_score"], reverse=True)

creativity_fields = [
    "idea_id",
    "idea_name",
    "idea_type",
    "frame_family",
    "source_domain",
    "strategic_creativity_score",
    "novelty_theater_risk",
    "overdiscipline_risk",
    "stakeholder_gap",
    "systems_gap",
    "mechanism_gap",
    "diagnosis",
    "novelty",
    "strategic_relevance",
    "conceptual_coherence",
    "mechanism_clarity",
    "testability",
    "stakeholder_grounding",
    "systems_fit",
    "developmental_potential",
    "implementation_risk",
    "revision_capacity",
    "description",
]

write_csv(TABLES / "strategic_creativity_scores.csv", creativity_rows, creativity_fields)
write_csv(PROCESSED / "strategic_creativity_scores.csv", creativity_rows, creativity_fields)

novelty_review = sorted(
    [
        {
            "idea_id": row["idea_id"],
            "idea_name": row["idea_name"],
            "novelty": row["novelty"],
            "mechanism_clarity": row["mechanism_clarity"],
            "stakeholder_grounding": row["stakeholder_grounding"],
            "systems_fit": row["systems_fit"],
            "novelty_theater_risk": row["novelty_theater_risk"],
            "diagnosis": row["diagnosis"],
        }
        for row in creativity_rows
    ],
    key=lambda item: float(item["novelty_theater_risk"]),
    reverse=True,
)

write_csv(
    TABLES / "novelty_depth_review.csv",
    novelty_review,
    [
        "idea_id",
        "idea_name",
        "novelty",
        "mechanism_clarity",
        "stakeholder_grounding",
        "systems_fit",
        "novelty_theater_risk",
        "diagnosis",
    ],
)

# ---------------------------------------------------------------------
# 2. Constraint audit
# ---------------------------------------------------------------------

constraint_rows: list[dict[str, object]] = []

for row in constraints:
    productive_constraint_value = (
        0.18 * f(row, "constraint_legitimacy")
        + 0.18 * f(row, "creative_focus_gain")
        + 0.16 * f(row, "ethical_importance")
        + 0.14 * f(row, "sequencing_value")
        - 0.12 * f(row, "search_narrowing_risk")
        - 0.12 * f(row, "assumption_disguise_risk")
    )

    dead_constraint_risk = (
        0.30 * f(row, "search_narrowing_risk")
        + 0.30 * f(row, "assumption_disguise_risk")
        + 0.18 * f(row, "changeability")
        - 0.18 * f(row, "constraint_legitimacy")
        - 0.12 * f(row, "ethical_importance")
    )

    if dead_constraint_risk >= 0.40:
        action = "challenge_as_possible_dead_constraint"
    elif f(row, "ethical_importance") >= 0.80 and f(row, "constraint_legitimacy") >= 0.75:
        action = "honor_as_productive_constraint"
    elif productive_constraint_value >= 0.45:
        action = "use_as_creative_design_condition"
    else:
        action = "review_constraint_role"

    constraint_rows.append(
        {
            "constraint_id": row["constraint_id"],
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "constraint_name": row["constraint_name"],
            "constraint_type": row["constraint_type"],
            "productive_constraint_value": round(productive_constraint_value, 4),
            "dead_constraint_risk": round(dead_constraint_risk, 4),
            "recommended_action": action,
            "source_action": row["review_action"],
            "constraint_legitimacy": row["constraint_legitimacy"],
            "creative_focus_gain": row["creative_focus_gain"],
            "search_narrowing_risk": row["search_narrowing_risk"],
            "assumption_disguise_risk": row["assumption_disguise_risk"],
            "ethical_importance": row["ethical_importance"],
            "changeability": row["changeability"],
            "sequencing_value": row["sequencing_value"],
        }
    )

constraint_rows.sort(key=lambda item: item["dead_constraint_risk"], reverse=True)

write_csv(
    TABLES / "constraint_audit.csv",
    constraint_rows,
    [
        "constraint_id",
        "idea_id",
        "idea_name",
        "constraint_name",
        "constraint_type",
        "productive_constraint_value",
        "dead_constraint_risk",
        "recommended_action",
        "source_action",
        "constraint_legitimacy",
        "creative_focus_gain",
        "search_narrowing_risk",
        "assumption_disguise_risk",
        "ethical_importance",
        "changeability",
        "sequencing_value",
    ],
)

# ---------------------------------------------------------------------
# 3. Stakeholder grounding review
# ---------------------------------------------------------------------

stakeholder_rows: list[dict[str, object]] = []

for row in stakeholders:
    stakeholder_score = (
        0.16 * f(row, "visibility_quality")
        + 0.16 * f(row, "burden_visibility")
        + 0.14 * f(row, "trust_sensitivity")
        + 0.14 * f(row, "agency_preservation")
        + 0.14 * f(row, "participation_quality")
        + 0.16 * f(row, "legitimacy_score")
        - 0.10 * f(row, "hidden_harm_risk")
    )

    if f(row, "hidden_harm_risk") >= 0.60:
        action = "hidden_harm_review_required"
    elif f(row, "burden_visibility") < 0.45:
        action = "add_burden_mapping"
    elif f(row, "participation_quality") < 0.45:
        action = "add_participatory_inquiry"
    elif stakeholder_score >= 0.60:
        action = "stakeholder_grounding_manageable"
    else:
        action = "strengthen_stakeholder_grounding"

    stakeholder_rows.append(
        {
            "review_id": row["review_id"],
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "stakeholder_group": row["stakeholder_group"],
            "stakeholder_grounding_score": round(stakeholder_score, 4),
            "recommended_action": action,
            "source_recommendation": row["review_recommendation"],
            "visibility_quality": row["visibility_quality"],
            "burden_visibility": row["burden_visibility"],
            "trust_sensitivity": row["trust_sensitivity"],
            "agency_preservation": row["agency_preservation"],
            "participation_quality": row["participation_quality"],
            "legitimacy_score": row["legitimacy_score"],
            "hidden_harm_risk": row["hidden_harm_risk"],
        }
    )

stakeholder_rows.sort(key=lambda item: item["stakeholder_grounding_score"], reverse=True)

write_csv(
    TABLES / "stakeholder_grounding_review.csv",
    stakeholder_rows,
    [
        "review_id",
        "idea_id",
        "idea_name",
        "stakeholder_group",
        "stakeholder_grounding_score",
        "recommended_action",
        "source_recommendation",
        "visibility_quality",
        "burden_visibility",
        "trust_sensitivity",
        "agency_preservation",
        "participation_quality",
        "legitimacy_score",
        "hidden_harm_risk",
    ],
)

# ---------------------------------------------------------------------
# 4. Systems-fit review
# ---------------------------------------------------------------------

systems_rows: list[dict[str, object]] = []

for row in systems:
    systems_score = (
        0.14 * f(row, "feedback_awareness")
        + 0.14 * f(row, "incentive_fit")
        + 0.12 * f(row, "dependency_visibility")
        + 0.12 * f(row, "delay_awareness")
        + 0.14 * f(row, "second_order_review")
        + 0.12 * f(row, "boundary_quality")
        + 0.12 * f(row, "adaptation_review")
        + 0.14 * f(row, "robustness_across_scenarios")
        - 0.12 * f(row, "systems_risk")
    )

    if f(row, "systems_risk") >= 0.60:
        action = "systems_review_before_advancing"
    elif f(row, "feedback_awareness") < 0.45:
        action = "map_feedback_loops"
    elif f(row, "second_order_review") < 0.45:
        action = "add_second_order_effects_review"
    elif systems_score >= 0.60:
        action = "systems_fit_manageable"
    else:
        action = "strengthen_systems_fit"

    systems_rows.append(
        {
            "systems_id": row["systems_id"],
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "systems_fit_score": round(systems_score, 4),
            "recommended_action": action,
            "source_recommendation": row["systems_recommendation"],
            "feedback_awareness": row["feedback_awareness"],
            "incentive_fit": row["incentive_fit"],
            "dependency_visibility": row["dependency_visibility"],
            "delay_awareness": row["delay_awareness"],
            "second_order_review": row["second_order_review"],
            "boundary_quality": row["boundary_quality"],
            "adaptation_review": row["adaptation_review"],
            "robustness_across_scenarios": row["robustness_across_scenarios"],
            "systems_risk": row["systems_risk"],
        }
    )

systems_rows.sort(key=lambda item: item["systems_fit_score"], reverse=True)

write_csv(
    TABLES / "systems_fit_review.csv",
    systems_rows,
    [
        "systems_id",
        "idea_id",
        "idea_name",
        "systems_fit_score",
        "recommended_action",
        "source_recommendation",
        "feedback_awareness",
        "incentive_fit",
        "dependency_visibility",
        "delay_awareness",
        "second_order_review",
        "boundary_quality",
        "adaptation_review",
        "robustness_across_scenarios",
        "systems_risk",
    ],
)

# ---------------------------------------------------------------------
# 5. Evidence pathway review
# ---------------------------------------------------------------------

evidence_rows: list[dict[str, object]] = []

for row in evidence:
    evidence_value = (
        0.16 * f(row, "evidence_strength")
        + 0.14 * f(row, "reliability")
        + 0.16 * f(row, "discrimination_power")
        + 0.18 * f(row, "learning_value")
        + 0.14 * f(row, "disconfirmation_quality")
        - 0.10 * f(row, "cost")
        - 0.08 * f(row, "time_to_learn")
    )

    if f(row, "disconfirmation_quality") < 0.40:
        action = "strengthen_disconfirmation_condition"
    elif f(row, "learning_value") >= 0.78 and f(row, "cost") <= 0.45:
        action = "priority_learning_test"
    elif evidence_value >= 0.55:
        action = "usable_evidence_pathway"
    else:
        action = "redesign_evidence_pathway"

    evidence_rows.append(
        {
            "evidence_id": row["evidence_id"],
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "evidence_name": row["evidence_name"],
            "evidence_type": row["evidence_type"],
            "evidence_value_score": round(evidence_value, 4),
            "recommended_action": action,
            "evidence_strength": row["evidence_strength"],
            "reliability": row["reliability"],
            "cost": row["cost"],
            "time_to_learn": row["time_to_learn"],
            "discrimination_power": row["discrimination_power"],
            "learning_value": row["learning_value"],
            "disconfirmation_quality": row["disconfirmation_quality"],
            "expected_if_promising": row["expected_if_promising"],
            "weakens_if": row["weakens_if"],
        }
    )

evidence_rows.sort(key=lambda item: item["evidence_value_score"], reverse=True)

write_csv(
    TABLES / "evidence_pathway_review.csv",
    evidence_rows,
    [
        "evidence_id",
        "idea_id",
        "idea_name",
        "evidence_name",
        "evidence_type",
        "evidence_value_score",
        "recommended_action",
        "evidence_strength",
        "reliability",
        "cost",
        "time_to_learn",
        "discrimination_power",
        "learning_value",
        "disconfirmation_quality",
        "expected_if_promising",
        "weakens_if",
    ],
)

# ---------------------------------------------------------------------
# 6. Idea maturation review
# ---------------------------------------------------------------------

maturation_rows: list[dict[str, object]] = []

for row in maturation:
    maturation_score = (
        0.14 * f(row, "clarification_gain")
        + 0.14 * f(row, "evidence_gain")
        + 0.14 * f(row, "stakeholder_gain")
        + 0.14 * f(row, "systems_gain")
        + 0.14 * f(row, "recombination_gain")
        + 0.16 * f(row, "revision_quality")
        + 0.14 * f(row, "stage_gate_quality")
    )

    if f(row, "stage_gate_quality") < 0.40:
        action = "do_not_advance_without_reframe"
    elif f(row, "revision_quality") >= 0.78 and f(row, "evidence_gain") >= 0.70:
        action = "advance_to_next_learning_stage"
    elif maturation_score >= 0.62:
        action = "develop_with_targeted_testing"
    else:
        action = "revise_before_advancing"

    maturation_rows.append(
        {
            "maturation_id": row["maturation_id"],
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "stage": row["stage"],
            "maturation_score": round(maturation_score, 4),
            "recommended_action": action,
            "source_next_stage": row["next_stage_recommendation"],
            "clarification_gain": row["clarification_gain"],
            "evidence_gain": row["evidence_gain"],
            "stakeholder_gain": row["stakeholder_gain"],
            "systems_gain": row["systems_gain"],
            "recombination_gain": row["recombination_gain"],
            "revision_quality": row["revision_quality"],
            "stage_gate_quality": row["stage_gate_quality"],
        }
    )

maturation_rows.sort(key=lambda item: item["maturation_score"], reverse=True)

write_csv(
    TABLES / "idea_maturation_review.csv",
    maturation_rows,
    [
        "maturation_id",
        "idea_id",
        "idea_name",
        "stage",
        "maturation_score",
        "recommended_action",
        "source_next_stage",
        "clarification_gain",
        "evidence_gain",
        "stakeholder_gain",
        "systems_gain",
        "recombination_gain",
        "revision_quality",
        "stage_gate_quality",
    ],
)

# ---------------------------------------------------------------------
# 7. Creative portfolio review
# ---------------------------------------------------------------------

portfolio_rows: list[dict[str, object]] = []

for row in portfolio:
    portfolio_value = (
        0.14 * f(row, "confidence_level")
        + 0.14 * f(row, "evidence_readiness")
        + 0.18 * f(row, "strategic_option_value")
        + 0.16 * f(row, "learning_value")
        - 0.10 * f(row, "resource_intensity")
        + 0.12 * f(row, "time_sensitivity")
        - 0.10 * f(row, "risk_exposure")
    )

    if row["portfolio_role"] == "novelty_theater_risk":
        action = "do_not_advance_as_strategy"
    elif f(row, "risk_exposure") >= 0.65 and f(row, "evidence_readiness") < 0.70:
        action = "stage_commitment_and_strengthen_evidence"
    elif portfolio_value >= 0.60:
        action = "active_creative_portfolio_priority"
    else:
        action = "monitor_archive_or_reframe"

    portfolio_rows.append(
        {
            "portfolio_id": row["portfolio_id"],
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "portfolio_role": row["portfolio_role"],
            "portfolio_value_score": round(portfolio_value, 4),
            "recommended_action": action,
            "source_portfolio_action": row["portfolio_action"],
            "confidence_level": row["confidence_level"],
            "evidence_readiness": row["evidence_readiness"],
            "strategic_option_value": row["strategic_option_value"],
            "learning_value": row["learning_value"],
            "resource_intensity": row["resource_intensity"],
            "time_sensitivity": row["time_sensitivity"],
            "risk_exposure": row["risk_exposure"],
        }
    )

portfolio_rows.sort(key=lambda item: item["portfolio_value_score"], reverse=True)

write_csv(
    TABLES / "creative_portfolio_review.csv",
    portfolio_rows,
    [
        "portfolio_id",
        "idea_id",
        "idea_name",
        "portfolio_role",
        "portfolio_value_score",
        "recommended_action",
        "source_portfolio_action",
        "confidence_level",
        "evidence_readiness",
        "strategic_option_value",
        "learning_value",
        "resource_intensity",
        "time_sensitivity",
        "risk_exposure",
    ],
)

# ---------------------------------------------------------------------
# 8. Intervention recommendations
# ---------------------------------------------------------------------

intervention_rows: list[dict[str, object]] = []

for row in interventions:
    intervention_value = (
        0.16 * f(row, "creativity_quality_gain")
        + 0.14 * f(row, "evidence_quality_gain")
        + 0.14 * f(row, "stakeholder_gain")
        + 0.14 * f(row, "systems_fit_gain")
        + 0.14 * f(row, "revision_gain")
        + 0.14 * f(row, "decision_memory_gain")
        - 0.10 * f(row, "process_cost")
        - 0.08 * f(row, "implementation_complexity")
        - 0.08 * f(row, "political_safety_need")
    )

    if f(row, "political_safety_need") >= 0.45:
        action = "requires_leadership_protection"
    elif intervention_value >= 0.50:
        action = "high_value_creativity_intervention"
    else:
        action = "supporting_intervention"

    intervention_rows.append(
        {
            "intervention_id": row["intervention_id"],
            "intervention_name": row["intervention_name"],
            "target_creativity_risk": row["target_creativity_risk"],
            "intervention_value_score": round(intervention_value, 4),
            "recommended_action": action,
            "process_cost": row["process_cost"],
            "implementation_complexity": row["implementation_complexity"],
            "creativity_quality_gain": row["creativity_quality_gain"],
            "evidence_quality_gain": row["evidence_quality_gain"],
            "stakeholder_gain": row["stakeholder_gain"],
            "systems_fit_gain": row["systems_fit_gain"],
            "revision_gain": row["revision_gain"],
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
        "target_creativity_risk",
        "intervention_value_score",
        "recommended_action",
        "process_cost",
        "implementation_complexity",
        "creativity_quality_gain",
        "evidence_quality_gain",
        "stakeholder_gain",
        "systems_fit_gain",
        "revision_gain",
        "decision_memory_gain",
        "political_safety_need",
    ],
)

# ---------------------------------------------------------------------
# 9. Strategist report
# ---------------------------------------------------------------------

top_ideas = creativity_rows[:6]
weak_ideas = sorted(creativity_rows, key=lambda item: item["strategic_creativity_score"])[:5]
novelty_risks = novelty_review[:5]
dead_constraints = constraint_rows[:5]
strong_stakeholders = stakeholder_rows[:5]
stakeholder_gaps = sorted(stakeholder_rows, key=lambda item: item["stakeholder_grounding_score"])[:5]
weak_systems = sorted(systems_rows, key=lambda item: item["systems_fit_score"])[:5]
top_evidence = evidence_rows[:6]
weak_maturation = sorted(maturation_rows, key=lambda item: item["maturation_score"])[:5]
top_portfolio = portfolio_rows[:6]
top_interventions = intervention_rows[:6]

report: list[str] = []

report.append("# Imagination, Discipline, and Strategic Creativity Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic separates strategic creativity score, novelty-theater risk, overdiscipline risk, stakeholder gaps, "
    "systems gaps, mechanism gaps, constraint quality, evidence pathways, idea maturation, creative portfolio value, and "
    "intervention priority. The purpose is to help strategists develop ideas that are imaginative, disciplined, grounded, "
    "testable, revisable, and strategically consequential."
)
report.append("")
report.append("## Strongest strategic creativity candidates")
report.append("")

for item in top_ideas:
    report.append(
        f"- **{item['idea_id']} — {item['idea_name']}**: creativity score {item['strategic_creativity_score']}; "
        f"diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Weakest or least ready ideas")
report.append("")

for item in weak_ideas:
    report.append(
        f"- **{item['idea_id']} — {item['idea_name']}**: creativity score {item['strategic_creativity_score']}; "
        f"novelty-theater risk {item['novelty_theater_risk']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest novelty-theater risks")
report.append("")

for item in novelty_risks:
    report.append(
        f"- **{item['idea_id']} — {item['idea_name']}**: novelty {item['novelty']}; "
        f"mechanism {item['mechanism_clarity']}; stakeholder grounding {item['stakeholder_grounding']}; "
        f"systems fit {item['systems_fit']}; novelty-theater risk {item['novelty_theater_risk']}."
    )

report.append("")
report.append("## Highest dead-constraint risks")
report.append("")

for item in dead_constraints:
    report.append(
        f"- **{item['constraint_id']} — {item['constraint_name']}** for **{item['idea_name']}**: "
        f"dead-constraint risk {item['dead_constraint_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strongest stakeholder grounding")
report.append("")

for item in strong_stakeholders:
    report.append(
        f"- **{item['review_id']} — {item['idea_name']}** ({item['stakeholder_group']}): "
        f"score {item['stakeholder_grounding_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Stakeholder grounding gaps")
report.append("")

for item in stakeholder_gaps:
    report.append(
        f"- **{item['review_id']} — {item['idea_name']}** ({item['stakeholder_group']}): "
        f"score {item['stakeholder_grounding_score']}; hidden harm risk {item['hidden_harm_risk']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weakest systems-fit reviews")
report.append("")

for item in weak_systems:
    report.append(
        f"- **{item['systems_id']} — {item['idea_name']}**: systems score {item['systems_fit_score']}; "
        f"systems risk {item['systems_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Priority evidence pathways")
report.append("")

for item in top_evidence:
    report.append(
        f"- **{item['evidence_id']} — {item['evidence_name']}** for **{item['idea_name']}**: "
        f"value {item['evidence_value_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Ideas needing maturation before advancement")
report.append("")

for item in weak_maturation:
    report.append(
        f"- **{item['maturation_id']} — {item['idea_name']}** ({item['stage']}): "
        f"maturation score {item['maturation_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest-value creative portfolio items")
report.append("")

for item in top_portfolio:
    report.append(
        f"- **{item['portfolio_id']} — {item['idea_name']}** ({item['portfolio_role']}): "
        f"portfolio value {item['portfolio_value_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest-value creativity interventions")
report.append("")

for item in top_interventions:
    report.append(
        f"- **{item['intervention_id']} — {item['intervention_name']}**: value {item['intervention_value_score']}; "
        f"target: {item['target_creativity_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "The value of this workflow is disciplined creative judgment. It helps teams avoid novelty theater, premature convergence, "
    "undisciplined imagination, overdiscipline, stakeholder blindness, systems mismatch, and institutional forgetting. "
    "It supports strategic creativity as a developmental process: imagine, clarify, challenge, test, refine, select, and preserve learning."
)

(REPORTS / "strategic_creativity_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_ideas": top_ideas,
    "weak_ideas": weak_ideas,
    "novelty_risks": novelty_risks,
    "dead_constraints": dead_constraints,
    "stakeholder_gaps": stakeholder_gaps,
    "weak_systems": weak_systems,
    "top_evidence": top_evidence,
    "weak_maturation": weak_maturation,
    "top_portfolio": top_portfolio,
    "top_interventions": top_interventions,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced strategic creativity diagnostics complete.")
print(f"Wrote: {TABLES / 'strategic_creativity_scores.csv'}")
print(f"Wrote: {TABLES / 'novelty_depth_review.csv'}")
print(f"Wrote: {TABLES / 'constraint_audit.csv'}")
print(f"Wrote: {TABLES / 'stakeholder_grounding_review.csv'}")
print(f"Wrote: {TABLES / 'systems_fit_review.csv'}")
print(f"Wrote: {TABLES / 'evidence_pathway_review.csv'}")
print(f"Wrote: {TABLES / 'idea_maturation_review.csv'}")
print(f"Wrote: {TABLES / 'creative_portfolio_review.csv'}")
print(f"Wrote: {TABLES / 'intervention_recommendations.csv'}")
print(f"Wrote: {REPORTS / 'strategic_creativity_diagnostic_report.md'}")
