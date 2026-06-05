#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for theory of change and strategic logic.

This dependency-light workflow uses only the Python standard library.

It produces:
- strategic logic scores
- theory-of-change link risk scores
- assumption link review
- evidence match review
- actor response review
- system feedback review
- outcome sequence review
- prototype test design scores
- implementation learning review
- revision trigger review
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


ideas = read_csv(RAW / "strategic_ideas.csv")
links = read_csv(RAW / "theory_links.csv")
assumptions = read_csv(RAW / "assumptions.csv")
evidence = read_csv(RAW / "evidence_sources.csv")
actors = read_csv(RAW / "actor_response.csv")
feedback = read_csv(RAW / "system_feedback.csv")
outcomes = read_csv(RAW / "outcome_sequence.csv")
prototypes = read_csv(RAW / "prototype_tests.csv")
learning = read_csv(RAW / "implementation_learning.csv")
triggers = read_csv(RAW / "revision_triggers.csv")

idea_names = {row["idea_id"]: row["idea_name"] for row in ideas}
link_names = {row["link_id"]: row["link_description"] for row in links}
assumption_names = {row["assumption_id"]: row["assumption_statement"] for row in assumptions}

# ---------------------------------------------------------------------
# 1. Strategic logic scores
# ---------------------------------------------------------------------

strategic_rows: list[dict[str, object]] = []

for row in ideas:
    strategic_logic_score = (
        0.14 * f(row, "problem_frame_quality")
        + 0.17 * f(row, "mechanism_clarity")
        + 0.12 * f(row, "strategic_alignment")
        + 0.11 * f(row, "implementation_feasibility")
        + 0.12 * f(row, "stakeholder_legitimacy")
        - 0.10 * f(row, "system_complexity")
        + 0.13 * f(row, "learning_value")
        + 0.11 * f(row, "reversibility")
    )

    logic_risk = (
        0.18 * (1 - f(row, "mechanism_clarity"))
        + 0.15 * (1 - f(row, "problem_frame_quality"))
        + 0.13 * (1 - f(row, "implementation_feasibility"))
        + 0.12 * (1 - f(row, "stakeholder_legitimacy"))
        + 0.18 * f(row, "system_complexity")
        + 0.12 * (1 - f(row, "learning_value"))
        + 0.12 * (1 - f(row, "reversibility"))
    )

    if strategic_logic_score >= 0.62:
        diagnosis = "strong_or_promising_strategic_logic"
    elif f(row, "mechanism_clarity") < 0.58:
        diagnosis = "clarify_change_mechanism"
    elif f(row, "learning_value") < 0.50:
        diagnosis = "weak_learning_pathway"
    else:
        diagnosis = "requires_theory_of_change_review"

    strategic_rows.append(
        {
            "idea_id": row["idea_id"],
            "idea_name": row["idea_name"],
            "idea_type": row["idea_type"],
            "domain": row["domain"],
            "strategic_logic_score": round(strategic_logic_score, 4),
            "logic_risk_score": round(logic_risk, 4),
            "diagnosis": diagnosis,
            "problem_frame_quality": row["problem_frame_quality"],
            "mechanism_clarity": row["mechanism_clarity"],
            "strategic_alignment": row["strategic_alignment"],
            "implementation_feasibility": row["implementation_feasibility"],
            "stakeholder_legitimacy": row["stakeholder_legitimacy"],
            "system_complexity": row["system_complexity"],
            "learning_value": row["learning_value"],
            "reversibility": row["reversibility"],
            "description": row["description"],
        }
    )

strategic_rows.sort(key=lambda item: item["strategic_logic_score"], reverse=True)

strategic_fields = [
    "idea_id",
    "idea_name",
    "idea_type",
    "domain",
    "strategic_logic_score",
    "logic_risk_score",
    "diagnosis",
    "problem_frame_quality",
    "mechanism_clarity",
    "strategic_alignment",
    "implementation_feasibility",
    "stakeholder_legitimacy",
    "system_complexity",
    "learning_value",
    "reversibility",
    "description",
]

write_csv(TABLES / "strategic_logic_scores.csv", strategic_rows, strategic_fields)
write_csv(PROCESSED / "strategic_logic_scores.csv", strategic_rows, strategic_fields)

# ---------------------------------------------------------------------
# 2. Theory link risk scores
# ---------------------------------------------------------------------

link_rows: list[dict[str, object]] = []

for row in links:
    link_risk = (
        0.16 * (1 - f(row, "mechanism_clarity"))
        + 0.18 * (1 - f(row, "evidence_strength"))
        + 0.13 * f(row, "actor_dependency")
        + 0.11 * f(row, "capacity_dependency")
        + 0.14 * f(row, "system_dependency")
        + 0.12 * f(row, "ethical_dependency")
        + 0.16 * f(row, "failure_consequence")
    )

    test_priority = link_risk * f(row, "testability")

    if link_risk >= 0.62 and f(row, "testability") >= 0.62:
        action = "test_first"
    elif link_risk >= 0.62:
        action = "reduce_commitment_before_scaling"
    elif f(row, "evidence_strength") <= 0.42:
        action = "evidence_gap"
    elif f(row, "mechanism_clarity") <= 0.55:
        action = "clarify_mechanism"
    else:
        action = "monitor"

    link_rows.append(
        {
            "link_id": row["link_id"],
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "link_stage": row["link_stage"],
            "from_element": row["from_element"],
            "to_element": row["to_element"],
            "link_description": row["link_description"],
            "link_risk_score": round(link_risk, 4),
            "test_priority_score": round(test_priority, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "mechanism_clarity": row["mechanism_clarity"],
            "evidence_strength": row["evidence_strength"],
            "actor_dependency": row["actor_dependency"],
            "capacity_dependency": row["capacity_dependency"],
            "system_dependency": row["system_dependency"],
            "ethical_dependency": row["ethical_dependency"],
            "failure_consequence": row["failure_consequence"],
            "testability": row["testability"],
        }
    )

link_rows.sort(key=lambda item: item["link_risk_score"], reverse=True)

write_csv(
    TABLES / "theory_link_risk_scores.csv",
    link_rows,
    [
        "link_id",
        "idea_id",
        "idea_name",
        "link_stage",
        "from_element",
        "to_element",
        "link_description",
        "link_risk_score",
        "test_priority_score",
        "recommended_action",
        "source_review_action",
        "mechanism_clarity",
        "evidence_strength",
        "actor_dependency",
        "capacity_dependency",
        "system_dependency",
        "ethical_dependency",
        "failure_consequence",
        "testability",
    ],
)

# ---------------------------------------------------------------------
# 3. Assumption link review
# ---------------------------------------------------------------------

assumption_rows: list[dict[str, object]] = []

for row in assumptions:
    evidence_composite = (
        0.40 * f(row, "evidence_strength")
        + 0.30 * f(row, "evidence_relevance")
        + 0.30 * f(row, "evidence_transferability")
    )

    assumption_risk = (
        f(row, "criticality")
        * f(row, "uncertainty")
        * (1 - evidence_composite)
    )

    learning_value = (
        0.34 * assumption_risk
        + 0.24 * f(row, "testability")
        + 0.18 * f(row, "stakeholder_sensitivity")
        + 0.14 * f(row, "system_sensitivity")
        + 0.10 * f(row, "criticality")
    )

    if assumption_risk >= 0.28 and f(row, "testability") >= 0.65:
        action = "test_first"
    elif assumption_risk >= 0.28:
        action = "reduce_commitment_before_testing"
    elif f(row, "stakeholder_sensitivity") >= 0.85:
        action = "stakeholder_review_required"
    else:
        action = "monitor"

    assumption_rows.append(
        {
            "assumption_id": row["assumption_id"],
            "link_id": row["link_id"],
            "link_description": link_names.get(row["link_id"], row["link_id"]),
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "assumption_statement": row["assumption_statement"],
            "assumption_type": row["assumption_type"],
            "assumption_risk_score": round(assumption_risk, 4),
            "evidence_composite": round(evidence_composite, 4),
            "learning_value": round(learning_value, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "criticality": row["criticality"],
            "uncertainty": row["uncertainty"],
            "evidence_strength": row["evidence_strength"],
            "evidence_relevance": row["evidence_relevance"],
            "evidence_transferability": row["evidence_transferability"],
            "testability": row["testability"],
            "stakeholder_sensitivity": row["stakeholder_sensitivity"],
            "system_sensitivity": row["system_sensitivity"],
            "decision_owner": row["decision_owner"],
        }
    )

assumption_rows.sort(key=lambda item: item["assumption_risk_score"], reverse=True)

write_csv(
    TABLES / "assumption_link_review.csv",
    assumption_rows,
    [
        "assumption_id",
        "link_id",
        "link_description",
        "idea_id",
        "idea_name",
        "assumption_statement",
        "assumption_type",
        "assumption_risk_score",
        "evidence_composite",
        "learning_value",
        "recommended_action",
        "source_review_action",
        "criticality",
        "uncertainty",
        "evidence_strength",
        "evidence_relevance",
        "evidence_transferability",
        "testability",
        "stakeholder_sensitivity",
        "system_sensitivity",
        "decision_owner",
    ],
)

# ---------------------------------------------------------------------
# 4. Evidence match review
# ---------------------------------------------------------------------

evidence_rows: list[dict[str, object]] = []

for row in evidence:
    evidence_match_score = (
        0.18 * f(row, "reliability")
        + 0.24 * f(row, "relevance")
        + 0.18 * f(row, "transferability")
        + 0.12 * f(row, "timeliness")
        - 0.10 * f(row, "bias_risk")
        + 0.12 * f(row, "coverage_quality")
        + 0.16 * f(row, "interpretation_quality")
    )

    if evidence_match_score >= 0.66:
        action = "strong_evidence_match"
    elif f(row, "relevance") < 0.60:
        action = "evidence_mismatch_review"
    elif f(row, "transferability") < 0.55:
        action = "test_context_transfer"
    elif f(row, "bias_risk") >= 0.40:
        action = "bias_review"
    else:
        action = "strengthen_evidence"

    evidence_rows.append(
        {
            "evidence_id": row["evidence_id"],
            "link_id": row["link_id"],
            "link_description": link_names.get(row["link_id"], row["link_id"]),
            "assumption_id": row["assumption_id"],
            "assumption_statement": assumption_names.get(row["assumption_id"], row["assumption_id"]),
            "evidence_type": row["evidence_type"],
            "evidence_description": row["evidence_description"],
            "evidence_match_score": round(evidence_match_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "reliability": row["reliability"],
            "relevance": row["relevance"],
            "transferability": row["transferability"],
            "timeliness": row["timeliness"],
            "bias_risk": row["bias_risk"],
            "coverage_quality": row["coverage_quality"],
            "interpretation_quality": row["interpretation_quality"],
        }
    )

evidence_rows.sort(key=lambda item: item["evidence_match_score"])

write_csv(
    TABLES / "evidence_match_review.csv",
    evidence_rows,
    [
        "evidence_id",
        "link_id",
        "link_description",
        "assumption_id",
        "assumption_statement",
        "evidence_type",
        "evidence_description",
        "evidence_match_score",
        "recommended_action",
        "source_review_action",
        "reliability",
        "relevance",
        "transferability",
        "timeliness",
        "bias_risk",
        "coverage_quality",
        "interpretation_quality",
    ],
)

# ---------------------------------------------------------------------
# 5. Actor response review
# ---------------------------------------------------------------------

actor_rows: list[dict[str, object]] = []

for row in actors:
    actor_response_risk = (
        0.16 * f(row, "response_dependency")
        - 0.12 * f(row, "incentive_alignment")
        + 0.14 * (1 - f(row, "trust_condition"))
        + 0.12 * (1 - f(row, "capacity_condition"))
        + 0.15 * f(row, "burden_risk")
        + 0.13 * f(row, "resistance_risk")
        - 0.08 * f(row, "participation_quality")
        + 0.10 * f(row, "knowledge_value")
    )

    if actor_response_risk >= 0.42:
        action = "actor_response_review_required"
    elif f(row, "incentive_alignment") < 0.50:
        action = "incentive_alignment_review"
    elif f(row, "trust_condition") < 0.55:
        action = "trust_review"
    elif f(row, "burden_risk") >= 0.75:
        action = "burden_review"
    else:
        action = "monitor_actor_response"

    actor_rows.append(
        {
            "actor_id": row["actor_id"],
            "link_id": row["link_id"],
            "link_description": link_names.get(row["link_id"], row["link_id"]),
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "actor_group": row["actor_group"],
            "expected_response": row["expected_response"],
            "actor_response_risk": round(actor_response_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "response_dependency": row["response_dependency"],
            "incentive_alignment": row["incentive_alignment"],
            "trust_condition": row["trust_condition"],
            "capacity_condition": row["capacity_condition"],
            "burden_risk": row["burden_risk"],
            "resistance_risk": row["resistance_risk"],
            "participation_quality": row["participation_quality"],
            "knowledge_value": row["knowledge_value"],
        }
    )

actor_rows.sort(key=lambda item: item["actor_response_risk"], reverse=True)

write_csv(
    TABLES / "actor_response_review.csv",
    actor_rows,
    [
        "actor_id",
        "link_id",
        "link_description",
        "idea_id",
        "idea_name",
        "actor_group",
        "expected_response",
        "actor_response_risk",
        "recommended_action",
        "source_review_action",
        "response_dependency",
        "incentive_alignment",
        "trust_condition",
        "capacity_condition",
        "burden_risk",
        "resistance_risk",
        "participation_quality",
        "knowledge_value",
    ],
)

# ---------------------------------------------------------------------
# 6. System feedback review
# ---------------------------------------------------------------------

feedback_rows: list[dict[str, object]] = []

for row in feedback:
    feedback_risk_score = (
        0.14 * f(row, "feedback_risk")
        + 0.13 * f(row, "adaptation_risk")
        + 0.12 * f(row, "delay_risk")
        + 0.15 * f(row, "burden_shift_risk")
        + 0.13 * f(row, "metric_gaming_risk")
        + 0.12 * f(row, "context_dependency")
        - 0.09 * f(row, "monitoring_quality")
        + 0.12 * f(row, "leverage_relevance")
    )

    if feedback_risk_score >= 0.58:
        action = "system_feedback_review_required"
    elif f(row, "monitoring_quality") < 0.58:
        action = "improve_system_monitoring"
    elif f(row, "burden_shift_risk") >= 0.75:
        action = "burden_shift_review_required"
    elif f(row, "metric_gaming_risk") >= 0.80:
        action = "metric_gaming_review"
    else:
        action = "monitor_system_feedback"

    feedback_rows.append(
        {
            "feedback_id": row["feedback_id"],
            "link_id": row["link_id"],
            "link_description": link_names.get(row["link_id"], row["link_id"]),
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "feedback_pattern": row["feedback_pattern"],
            "feedback_type": row["feedback_type"],
            "feedback_risk_score": round(feedback_risk_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "feedback_risk": row["feedback_risk"],
            "adaptation_risk": row["adaptation_risk"],
            "delay_risk": row["delay_risk"],
            "burden_shift_risk": row["burden_shift_risk"],
            "metric_gaming_risk": row["metric_gaming_risk"],
            "context_dependency": row["context_dependency"],
            "monitoring_quality": row["monitoring_quality"],
            "leverage_relevance": row["leverage_relevance"],
        }
    )

feedback_rows.sort(key=lambda item: item["feedback_risk_score"], reverse=True)

write_csv(
    TABLES / "system_feedback_review.csv",
    feedback_rows,
    [
        "feedback_id",
        "link_id",
        "link_description",
        "idea_id",
        "idea_name",
        "feedback_pattern",
        "feedback_type",
        "feedback_risk_score",
        "recommended_action",
        "source_review_action",
        "feedback_risk",
        "adaptation_risk",
        "delay_risk",
        "burden_shift_risk",
        "metric_gaming_risk",
        "context_dependency",
        "monitoring_quality",
        "leverage_relevance",
    ],
)

# ---------------------------------------------------------------------
# 7. Outcome sequence review
# ---------------------------------------------------------------------

outcome_rows: list[dict[str, object]] = []

for row in outcomes:
    outcome_quality = (
        0.14 * f(row, "precondition_quality")
        + 0.16 * f(row, "indicator_quality")
        + 0.13 * f(row, "measurement_feasibility")
        - 0.10 * f(row, "actor_dependency")
        - 0.12 * f(row, "system_dependency")
        - 0.15 * f(row, "impact_claim_risk")
        + 0.14 * f(row, "review_cadence_quality")
    )

    if f(row, "impact_claim_risk") >= 0.70:
        action = "avoid_impact_overclaiming"
    elif f(row, "indicator_quality") < 0.55:
        action = "improve_indicators"
    elif f(row, "review_cadence_quality") < 0.58:
        action = "strengthen_review_cadence"
    else:
        action = "sequence_usable_with_monitoring"

    outcome_rows.append(
        {
            "sequence_id": row["sequence_id"],
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "outcome_stage": row["outcome_stage"],
            "outcome_name": row["outcome_name"],
            "time_horizon": row["time_horizon"],
            "outcome_sequence_quality": round(outcome_quality, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "precondition_quality": row["precondition_quality"],
            "indicator_quality": row["indicator_quality"],
            "measurement_feasibility": row["measurement_feasibility"],
            "actor_dependency": row["actor_dependency"],
            "system_dependency": row["system_dependency"],
            "impact_claim_risk": row["impact_claim_risk"],
            "review_cadence_quality": row["review_cadence_quality"],
        }
    )

outcome_rows.sort(key=lambda item: item["outcome_sequence_quality"])

write_csv(
    TABLES / "outcome_sequence_review.csv",
    outcome_rows,
    [
        "sequence_id",
        "idea_id",
        "idea_name",
        "outcome_stage",
        "outcome_name",
        "time_horizon",
        "outcome_sequence_quality",
        "recommended_action",
        "source_review_action",
        "precondition_quality",
        "indicator_quality",
        "measurement_feasibility",
        "actor_dependency",
        "system_dependency",
        "impact_claim_risk",
        "review_cadence_quality",
    ],
)

# ---------------------------------------------------------------------
# 8. Prototype test design scores
# ---------------------------------------------------------------------

prototype_rows: list[dict[str, object]] = []

for row in prototypes:
    prototype_score = (
        0.16 * f(row, "link_fit")
        + 0.10 * f(row, "learning_speed")
        + 0.15 * f(row, "learning_depth")
        + 0.12 * f(row, "realism")
        + 0.12 * f(row, "stakeholder_inclusion")
        + 0.10 * f(row, "scale_signal_quality")
        + 0.08 * f(row, "cost_efficiency")
        + 0.09 * f(row, "ethical_safety")
        + 0.18 * f(row, "decision_usefulness")
    )

    if prototype_score >= 0.75:
        action = "strong_theory_test"
    elif f(row, "link_fit") < 0.70:
        action = "improve_link_fit"
    elif f(row, "decision_usefulness") < 0.70:
        action = "connect_test_to_decision"
    else:
        action = "usable_prototype_test"

    prototype_rows.append(
        {
            "prototype_id": row["prototype_id"],
            "link_id": row["link_id"],
            "link_description": link_names.get(row["link_id"], row["link_id"]),
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "prototype_name": row["prototype_name"],
            "prototype_type": row["prototype_type"],
            "prototype_test_score": round(prototype_score, 4),
            "recommended_action": action,
            "success_threshold": row["success_threshold"],
            "decision_if_failed": row["decision_if_failed"],
            "link_fit": row["link_fit"],
            "learning_speed": row["learning_speed"],
            "learning_depth": row["learning_depth"],
            "realism": row["realism"],
            "stakeholder_inclusion": row["stakeholder_inclusion"],
            "scale_signal_quality": row["scale_signal_quality"],
            "cost_efficiency": row["cost_efficiency"],
            "ethical_safety": row["ethical_safety"],
            "decision_usefulness": row["decision_usefulness"],
        }
    )

prototype_rows.sort(key=lambda item: item["prototype_test_score"], reverse=True)

write_csv(
    TABLES / "prototype_test_design_scores.csv",
    prototype_rows,
    [
        "prototype_id",
        "link_id",
        "link_description",
        "idea_id",
        "idea_name",
        "prototype_name",
        "prototype_type",
        "prototype_test_score",
        "recommended_action",
        "success_threshold",
        "decision_if_failed",
        "link_fit",
        "learning_speed",
        "learning_depth",
        "realism",
        "stakeholder_inclusion",
        "scale_signal_quality",
        "cost_efficiency",
        "ethical_safety",
        "decision_usefulness",
    ],
)

# ---------------------------------------------------------------------
# 9. Implementation learning review
# ---------------------------------------------------------------------

learning_rows: list[dict[str, object]] = []

for row in learning:
    learning_loop_quality = (
        0.14 * f(row, "evidence_quality")
        + 0.14 * f(row, "feedback_quality")
        + 0.16 * f(row, "decision_linkage")
        + 0.13 * f(row, "governance_owner_clarity")
        + 0.13 * f(row, "revision_capacity")
        + 0.10 * f(row, "stakeholder_visibility")
        + 0.09 * f(row, "timeliness")
        + 0.11 * f(row, "learning_memory_quality")
    )

    if learning_loop_quality >= 0.70:
        action = "strong_learning_loop"
    elif f(row, "decision_linkage") < 0.65:
        action = "connect_learning_to_decision"
    elif f(row, "revision_capacity") < 0.60:
        action = "increase_revision_capacity"
    else:
        action = "usable_with_learning_review"

    learning_rows.append(
        {
            "learning_id": row["learning_id"],
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "learning_focus": row["learning_focus"],
            "review_stage": row["review_stage"],
            "learning_loop_quality": round(learning_loop_quality, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "evidence_quality": row["evidence_quality"],
            "feedback_quality": row["feedback_quality"],
            "decision_linkage": row["decision_linkage"],
            "governance_owner_clarity": row["governance_owner_clarity"],
            "revision_capacity": row["revision_capacity"],
            "stakeholder_visibility": row["stakeholder_visibility"],
            "timeliness": row["timeliness"],
            "learning_memory_quality": row["learning_memory_quality"],
        }
    )

learning_rows.sort(key=lambda item: item["learning_loop_quality"], reverse=True)

write_csv(
    TABLES / "implementation_learning_review.csv",
    learning_rows,
    [
        "learning_id",
        "idea_id",
        "idea_name",
        "learning_focus",
        "review_stage",
        "learning_loop_quality",
        "recommended_action",
        "source_review_action",
        "evidence_quality",
        "feedback_quality",
        "decision_linkage",
        "governance_owner_clarity",
        "revision_capacity",
        "stakeholder_visibility",
        "timeliness",
        "learning_memory_quality",
    ],
)

# ---------------------------------------------------------------------
# 10. Revision trigger review
# ---------------------------------------------------------------------

trigger_rows: list[dict[str, object]] = []

for row in triggers:
    trigger_quality = (
        0.15 * f(row, "signal_quality")
        + 0.15 * f(row, "threshold_clarity")
        + 0.16 * f(row, "decision_linkage")
        + 0.12 * f(row, "timeliness")
        + 0.12 * f(row, "stakeholder_visibility")
        + 0.12 * f(row, "governance_owner_clarity")
        + 0.18 * f(row, "response_options_quality")
    )

    if trigger_quality >= 0.75:
        action = "strong_revision_trigger"
    elif f(row, "decision_linkage") < 0.65:
        action = "connect_trigger_to_decision_rights"
    elif f(row, "threshold_clarity") < 0.65:
        action = "clarify_trigger_threshold"
    else:
        action = "usable_with_trigger_review"

    trigger_rows.append(
        {
            "trigger_id": row["trigger_id"],
            "link_id": row["link_id"],
            "link_description": link_names.get(row["link_id"], row["link_id"]),
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "trigger_name": row["trigger_name"],
            "trigger_type": row["trigger_type"],
            "trigger_quality_score": round(trigger_quality, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "signal_quality": row["signal_quality"],
            "threshold_clarity": row["threshold_clarity"],
            "decision_linkage": row["decision_linkage"],
            "timeliness": row["timeliness"],
            "stakeholder_visibility": row["stakeholder_visibility"],
            "governance_owner_clarity": row["governance_owner_clarity"],
            "response_options_quality": row["response_options_quality"],
        }
    )

trigger_rows.sort(key=lambda item: item["trigger_quality_score"], reverse=True)

write_csv(
    TABLES / "revision_trigger_review.csv",
    trigger_rows,
    [
        "trigger_id",
        "link_id",
        "link_description",
        "idea_id",
        "idea_name",
        "trigger_name",
        "trigger_type",
        "trigger_quality_score",
        "recommended_action",
        "source_review_action",
        "signal_quality",
        "threshold_clarity",
        "decision_linkage",
        "timeliness",
        "stakeholder_visibility",
        "governance_owner_clarity",
        "response_options_quality",
    ],
)

# ---------------------------------------------------------------------
# 11. Strategist report
# ---------------------------------------------------------------------

strong_logic = strategic_rows[:5]
weak_links = link_rows[:8]
top_assumptions = assumption_rows[:8]
weak_evidence = evidence_rows[:6]
actor_risks = actor_rows[:6]
feedback_risks = feedback_rows[:6]
weak_outcomes = outcome_rows[:6]
top_prototypes = prototype_rows[:6]
learning_loops = learning_rows[:6]
top_triggers = trigger_rows[:6]

report: list[str] = []

report.append("# Theory of Change and Strategic Logic Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic evaluates whether strategic ideas have plausible pathways from action to result. It examines mechanism clarity, causal link risk, "
    "assumption risk, evidence fit, actor response, system feedback, outcome sequence, prototype-test quality, implementation learning, and revision triggers."
)

report.append("")
report.append("## Strongest strategic logic scores")
report.append("")
for item in strong_logic:
    report.append(
        f"- **{item['idea_id']} — {item['idea_name']}**: strategic logic {item['strategic_logic_score']}; "
        f"logic risk {item['logic_risk_score']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest-risk theory-of-change links")
report.append("")
for item in weak_links:
    report.append(
        f"- **{item['link_id']} — {item['link_description']}** for **{item['idea_name']}**: "
        f"link risk {item['link_risk_score']}; test priority {item['test_priority_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Load-bearing assumptions to review")
report.append("")
for item in top_assumptions:
    report.append(
        f"- **{item['assumption_id']} — {item['assumption_statement']}**: "
        f"risk {item['assumption_risk_score']}; learning value {item['learning_value']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Evidence match gaps")
report.append("")
for item in weak_evidence:
    report.append(
        f"- **{item['evidence_id']} — {item['evidence_type']}** for **{item['assumption_statement']}**: "
        f"evidence match {item['evidence_match_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Actor response risks")
report.append("")
for item in actor_risks:
    report.append(
        f"- **{item['actor_id']} — {item['actor_group']}** for **{item['idea_name']}**: "
        f"risk {item['actor_response_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## System feedback risks")
report.append("")
for item in feedback_risks:
    report.append(
        f"- **{item['feedback_id']} — {item['feedback_pattern']}**: "
        f"risk {item['feedback_risk_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Outcome sequence weaknesses")
report.append("")
for item in weak_outcomes:
    report.append(
        f"- **{item['sequence_id']} — {item['outcome_name']}** ({item['time_horizon']}): "
        f"quality {item['outcome_sequence_quality']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strong prototype tests")
report.append("")
for item in top_prototypes:
    report.append(
        f"- **{item['prototype_id']} — {item['prototype_name']}**: "
        f"test score {item['prototype_test_score']}; threshold {item['success_threshold']}; if failed: {item['decision_if_failed']}."
    )

report.append("")
report.append("## Strong implementation learning loops")
report.append("")
for item in learning_loops:
    report.append(
        f"- **{item['learning_id']} — {item['learning_focus']}** for **{item['idea_name']}**: "
        f"quality {item['learning_loop_quality']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strong revision triggers")
report.append("")
for item in top_triggers:
    report.append(
        f"- **{item['trigger_id']} — {item['trigger_name']}** for **{item['idea_name']}**: "
        f"trigger quality {item['trigger_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "Theory of change strengthens strategic ideation by forcing ideas to explain their pathway: what action is taken, how change is expected to occur, "
    "who must respond, what assumptions hold the causal links together, what evidence is needed, what system responses may occur, and what learning "
    "should alter the strategy. The highest-value use of this diagnostic is to test weak links before implementation scale."
)

(REPORTS / "theory_of_change_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "strong_logic": strong_logic,
    "weak_links": weak_links,
    "top_assumptions": top_assumptions,
    "weak_evidence": weak_evidence,
    "actor_risks": actor_risks,
    "feedback_risks": feedback_risks,
    "weak_outcomes": weak_outcomes,
    "top_prototypes": top_prototypes,
    "learning_loops": learning_loops,
    "top_triggers": top_triggers,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced theory-of-change diagnostics complete.")
print(f"Wrote: {TABLES / 'strategic_logic_scores.csv'}")
print(f"Wrote: {TABLES / 'theory_link_risk_scores.csv'}")
print(f"Wrote: {TABLES / 'assumption_link_review.csv'}")
print(f"Wrote: {TABLES / 'evidence_match_review.csv'}")
print(f"Wrote: {TABLES / 'actor_response_review.csv'}")
print(f"Wrote: {TABLES / 'system_feedback_review.csv'}")
print(f"Wrote: {TABLES / 'outcome_sequence_review.csv'}")
print(f"Wrote: {TABLES / 'prototype_test_design_scores.csv'}")
print(f"Wrote: {TABLES / 'implementation_learning_review.csv'}")
print(f"Wrote: {TABLES / 'revision_trigger_review.csv'}")
print(f"Wrote: {REPORTS / 'theory_of_change_diagnostic_report.md'}")
