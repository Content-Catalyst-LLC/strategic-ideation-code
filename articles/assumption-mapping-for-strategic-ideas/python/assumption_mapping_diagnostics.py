#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for assumption mapping.

This dependency-light workflow uses only the Python standard library.

It produces:
- assumption risk scores
- evidence review scores
- test prioritization scores
- prototype learning scores
- theory-of-change assumption scores
- option confidence scores
- stakeholder assumption review
- system response assumption review
- future assumption review
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
assumptions = read_csv(RAW / "assumptions.csv")
evidence = read_csv(RAW / "evidence_sources.csv")
tests = read_csv(RAW / "assumption_tests.csv")
toc_links = read_csv(RAW / "theory_of_change_links.csv")
prototypes = read_csv(RAW / "prototype_learning.csv")
options = read_csv(RAW / "option_confidence.csv")
stakeholders = read_csv(RAW / "stakeholder_assumptions.csv")
system_responses = read_csv(RAW / "system_response_assumptions.csv")
future_assumptions = read_csv(RAW / "future_assumptions.csv")
triggers = read_csv(RAW / "revision_triggers.csv")

idea_names = {row["idea_id"]: row["idea_name"] for row in ideas}
assumption_names = {row["assumption_id"]: row["assumption_statement"] for row in assumptions}

# ---------------------------------------------------------------------
# 1. Assumption risk scoring
# ---------------------------------------------------------------------

assumption_rows: list[dict[str, object]] = []

for row in assumptions:
    evidence_composite = (
        0.40 * f(row, "evidence_strength")
        + 0.30 * f(row, "evidence_relevance")
        + 0.30 * f(row, "evidence_transferability")
    )

    priority_score = f(row, "criticality") * f(row, "uncertainty")
    evidence_adjusted_risk = (
        f(row, "criticality")
        * f(row, "uncertainty")
        * (1 - evidence_composite)
    )

    commitment_risk = evidence_adjusted_risk * (
        0.42 * (1 - f(row, "reversibility"))
        + 0.28 * f(row, "stakeholder_sensitivity")
        + 0.18 * f(row, "system_sensitivity")
        + 0.12 * f(row, "time_sensitivity")
    )

    learning_value = (
        0.34 * evidence_adjusted_risk
        + 0.24 * f(row, "testability")
        + 0.18 * f(row, "stakeholder_sensitivity")
        + 0.14 * f(row, "system_sensitivity")
        + 0.10 * f(row, "criticality")
    )

    if evidence_adjusted_risk >= 0.28 and f(row, "testability") >= 0.65:
        diagnosis = "test_first"
    elif evidence_adjusted_risk >= 0.28:
        diagnosis = "reduce_commitment_before_testing"
    elif f(row, "stakeholder_sensitivity") >= 0.85:
        diagnosis = "stakeholder_review_required"
    elif evidence_composite < 0.45:
        diagnosis = "evidence_gap"
    elif f(row, "time_sensitivity") >= 0.80:
        diagnosis = "time_sensitive_monitoring"
    else:
        diagnosis = "monitor"

    assumption_rows.append(
        {
            "assumption_id": row["assumption_id"],
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "assumption_statement": row["assumption_statement"],
            "assumption_type": row["assumption_type"],
            "priority_score": round(priority_score, 4),
            "evidence_composite": round(evidence_composite, 4),
            "evidence_adjusted_risk": round(evidence_adjusted_risk, 4),
            "commitment_risk": round(commitment_risk, 4),
            "learning_value": round(learning_value, 4),
            "diagnosis": diagnosis,
            "review_action": row["review_action"],
            "criticality": row["criticality"],
            "uncertainty": row["uncertainty"],
            "evidence_strength": row["evidence_strength"],
            "evidence_relevance": row["evidence_relevance"],
            "evidence_transferability": row["evidence_transferability"],
            "testability": row["testability"],
            "reversibility": row["reversibility"],
            "stakeholder_sensitivity": row["stakeholder_sensitivity"],
            "time_sensitivity": row["time_sensitivity"],
            "system_sensitivity": row["system_sensitivity"],
            "decision_owner": row["decision_owner"],
        }
    )

assumption_rows.sort(key=lambda item: item["evidence_adjusted_risk"], reverse=True)

assumption_fields = [
    "assumption_id",
    "idea_id",
    "idea_name",
    "assumption_statement",
    "assumption_type",
    "priority_score",
    "evidence_composite",
    "evidence_adjusted_risk",
    "commitment_risk",
    "learning_value",
    "diagnosis",
    "review_action",
    "criticality",
    "uncertainty",
    "evidence_strength",
    "evidence_relevance",
    "evidence_transferability",
    "testability",
    "reversibility",
    "stakeholder_sensitivity",
    "time_sensitivity",
    "system_sensitivity",
    "decision_owner",
]

write_csv(TABLES / "assumption_risk_scores.csv", assumption_rows, assumption_fields)
write_csv(PROCESSED / "assumption_risk_scores.csv", assumption_rows, assumption_fields)

# ---------------------------------------------------------------------
# 2. Evidence review
# ---------------------------------------------------------------------

evidence_rows: list[dict[str, object]] = []

for row in evidence:
    evidence_quality = (
        0.18 * f(row, "reliability")
        + 0.22 * f(row, "relevance")
        + 0.18 * f(row, "transferability")
        + 0.12 * f(row, "timeliness")
        - 0.10 * f(row, "bias_risk")
        + 0.12 * f(row, "coverage_quality")
        + 0.18 * f(row, "interpretation_quality")
    )

    if evidence_quality >= 0.68:
        action = "strong_evidence_for_assumption"
    elif f(row, "relevance") < 0.60:
        action = "evidence_mismatch_review"
    elif f(row, "transferability") < 0.55:
        action = "test_context_transfer"
    elif f(row, "bias_risk") >= 0.40:
        action = "bias_and_sampling_review"
    else:
        action = "strengthen_evidence"

    evidence_rows.append(
        {
            "evidence_id": row["evidence_id"],
            "assumption_id": row["assumption_id"],
            "assumption_statement": assumption_names.get(row["assumption_id"], row["assumption_id"]),
            "evidence_type": row["evidence_type"],
            "evidence_description": row["evidence_description"],
            "evidence_quality_score": round(evidence_quality, 4),
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

evidence_rows.sort(key=lambda item: item["evidence_quality_score"])

write_csv(
    TABLES / "evidence_review_scores.csv",
    evidence_rows,
    [
        "evidence_id",
        "assumption_id",
        "assumption_statement",
        "evidence_type",
        "evidence_description",
        "evidence_quality_score",
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
# 3. Test prioritization
# ---------------------------------------------------------------------

test_rows: list[dict[str, object]] = []

assumption_risk_lookup = {row["assumption_id"]: row for row in assumption_rows}

for row in tests:
    assumption_risk = float(assumption_risk_lookup[row["assumption_id"]]["evidence_adjusted_risk"])

    test_value = (
        0.24 * assumption_risk
        - 0.08 * f(row, "test_cost")
        + 0.10 * f(row, "test_speed")
        + 0.18 * f(row, "learning_quality")
        + 0.16 * f(row, "decision_relevance")
        + 0.10 * f(row, "stakeholder_inclusion")
        + 0.08 * f(row, "implementation_realism")
        + 0.07 * f(row, "scale_relevance")
        + 0.09 * f(row, "ethical_safety")
    )

    if test_value >= 0.60:
        action = "priority_test"
    elif f(row, "decision_relevance") < 0.60:
        action = "connect_test_to_decision"
    elif f(row, "stakeholder_inclusion") < 0.55:
        action = "increase_stakeholder_inclusion"
    else:
        action = "secondary_test"

    test_rows.append(
        {
            "test_id": row["test_id"],
            "assumption_id": row["assumption_id"],
            "assumption_statement": assumption_names.get(row["assumption_id"], row["assumption_id"]),
            "test_name": row["test_name"],
            "test_type": row["test_type"],
            "test_value_score": round(test_value, 4),
            "recommended_action": action,
            "success_threshold": row["success_threshold"],
            "decision_if_failed": row["decision_if_failed"],
            "test_cost": row["test_cost"],
            "test_speed": row["test_speed"],
            "learning_quality": row["learning_quality"],
            "decision_relevance": row["decision_relevance"],
            "stakeholder_inclusion": row["stakeholder_inclusion"],
            "implementation_realism": row["implementation_realism"],
            "scale_relevance": row["scale_relevance"],
            "ethical_safety": row["ethical_safety"],
        }
    )

test_rows.sort(key=lambda item: item["test_value_score"], reverse=True)

write_csv(
    TABLES / "test_prioritization_scores.csv",
    test_rows,
    [
        "test_id",
        "assumption_id",
        "assumption_statement",
        "test_name",
        "test_type",
        "test_value_score",
        "recommended_action",
        "success_threshold",
        "decision_if_failed",
        "test_cost",
        "test_speed",
        "learning_quality",
        "decision_relevance",
        "stakeholder_inclusion",
        "implementation_realism",
        "scale_relevance",
        "ethical_safety",
    ],
)

# ---------------------------------------------------------------------
# 4. Prototype learning
# ---------------------------------------------------------------------

prototype_rows: list[dict[str, object]] = []

for row in prototypes:
    learning_score = (
        0.18 * f(row, "assumption_fit")
        + 0.12 * f(row, "learning_speed")
        + 0.16 * f(row, "learning_depth")
        + 0.12 * f(row, "realism")
        + 0.12 * f(row, "stakeholder_inclusion")
        + 0.10 * f(row, "scale_signal_quality")
        + 0.08 * f(row, "cost_efficiency")
        + 0.10 * f(row, "ethical_safety")
        + 0.12 * f(row, "decision_usefulness")
    )

    if learning_score >= 0.75:
        action = "strong_learning_prototype"
    elif f(row, "assumption_fit") < 0.70:
        action = "improve_assumption_fit"
    elif f(row, "decision_usefulness") < 0.70:
        action = "connect_prototype_to_decision"
    else:
        action = "usable_prototype"

    prototype_rows.append(
        {
            "prototype_id": row["prototype_id"],
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "assumption_id": row["assumption_id"],
            "assumption_statement": assumption_names.get(row["assumption_id"], row["assumption_id"]),
            "prototype_name": row["prototype_name"],
            "prototype_type": row["prototype_type"],
            "prototype_learning_score": round(learning_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "assumption_fit": row["assumption_fit"],
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

prototype_rows.sort(key=lambda item: item["prototype_learning_score"], reverse=True)

write_csv(
    TABLES / "prototype_learning_scores.csv",
    prototype_rows,
    [
        "prototype_id",
        "idea_id",
        "idea_name",
        "assumption_id",
        "assumption_statement",
        "prototype_name",
        "prototype_type",
        "prototype_learning_score",
        "recommended_action",
        "source_review_action",
        "assumption_fit",
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
# 5. Theory of change assumption review
# ---------------------------------------------------------------------

toc_rows: list[dict[str, object]] = []

for row in toc_links:
    toc_risk = (
        0.16 * (1 - f(row, "mechanism_clarity"))
        + 0.18 * (1 - f(row, "evidence_strength"))
        + 0.14 * f(row, "actor_response_dependency")
        + 0.12 * f(row, "capacity_dependency")
        + 0.14 * f(row, "system_dependency")
        + 0.12 * f(row, "ethical_dependency")
        + 0.14 * f(row, "failure_consequence")
    )

    if toc_risk >= 0.62:
        action = "high_risk_theory_link"
    elif f(row, "mechanism_clarity") < 0.62:
        action = "clarify_mechanism"
    elif f(row, "evidence_strength") < 0.45:
        action = "strengthen_evidence_for_link"
    else:
        action = "monitor_theory_link"

    toc_rows.append(
        {
            "toc_link_id": row["toc_link_id"],
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "assumption_id": row["assumption_id"],
            "assumption_statement": assumption_names.get(row["assumption_id"], row["assumption_id"]),
            "link_stage": row["link_stage"],
            "link_description": row["link_description"],
            "theory_link_risk_score": round(toc_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "mechanism_clarity": row["mechanism_clarity"],
            "evidence_strength": row["evidence_strength"],
            "actor_response_dependency": row["actor_response_dependency"],
            "capacity_dependency": row["capacity_dependency"],
            "system_dependency": row["system_dependency"],
            "ethical_dependency": row["ethical_dependency"],
            "failure_consequence": row["failure_consequence"],
        }
    )

toc_rows.sort(key=lambda item: item["theory_link_risk_score"], reverse=True)

write_csv(
    TABLES / "theory_of_change_assumption_scores.csv",
    toc_rows,
    [
        "toc_link_id",
        "idea_id",
        "idea_name",
        "assumption_id",
        "assumption_statement",
        "link_stage",
        "link_description",
        "theory_link_risk_score",
        "recommended_action",
        "source_review_action",
        "mechanism_clarity",
        "evidence_strength",
        "actor_response_dependency",
        "capacity_dependency",
        "system_dependency",
        "ethical_dependency",
        "failure_consequence",
    ],
)

# ---------------------------------------------------------------------
# 6. Option confidence scoring
# ---------------------------------------------------------------------

option_rows: list[dict[str, object]] = []

for row in options:
    confidence_score = (
        0.18 * f(row, "expected_value")
        - 0.18 * f(row, "assumption_risk")
        - 0.10 * f(row, "commitment_risk")
        + 0.14 * f(row, "evidence_strength")
        + 0.12 * f(row, "learning_value")
        + 0.10 * f(row, "reversibility")
        + 0.12 * f(row, "stakeholder_legitimacy")
        + 0.08 * f(row, "implementation_readiness")
        + 0.08 * f(row, "system_resilience")
    )

    if confidence_score >= 0.50 and f(row, "learning_value") >= 0.80:
        action = "recommended_as_learning_pathway"
    elif f(row, "assumption_risk") >= 0.58:
        action = "do_not_scale_without_assumption_tests"
    elif f(row, "commitment_risk") >= 0.45:
        action = "phase_commitment"
    else:
        action = "consider_with_monitoring"

    option_rows.append(
        {
            "option_id": row["option_id"],
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "option_name": row["option_name"],
            "option_confidence_score": round(confidence_score, 4),
            "recommended_action": action,
            "source_recommendation": row["decision_recommendation"],
            "expected_value": row["expected_value"],
            "assumption_risk": row["assumption_risk"],
            "commitment_risk": row["commitment_risk"],
            "evidence_strength": row["evidence_strength"],
            "learning_value": row["learning_value"],
            "reversibility": row["reversibility"],
            "stakeholder_legitimacy": row["stakeholder_legitimacy"],
            "implementation_readiness": row["implementation_readiness"],
            "system_resilience": row["system_resilience"],
        }
    )

option_rows.sort(key=lambda item: item["option_confidence_score"], reverse=True)

write_csv(
    TABLES / "option_confidence_scores.csv",
    option_rows,
    [
        "option_id",
        "idea_id",
        "idea_name",
        "option_name",
        "option_confidence_score",
        "recommended_action",
        "source_recommendation",
        "expected_value",
        "assumption_risk",
        "commitment_risk",
        "evidence_strength",
        "learning_value",
        "reversibility",
        "stakeholder_legitimacy",
        "implementation_readiness",
        "system_resilience",
    ],
)

# ---------------------------------------------------------------------
# 7. Stakeholder assumption review
# ---------------------------------------------------------------------

stakeholder_rows: list[dict[str, object]] = []

for row in stakeholders:
    stakeholder_assumption_risk = (
        0.14 * f(row, "affectedness")
        + 0.14 * f(row, "trust_dependency")
        + 0.16 * f(row, "burden_risk")
        + 0.12 * f(row, "knowledge_value")
        - 0.14 * f(row, "inclusion_quality")
        - 0.12 * f(row, "representation_quality")
        + 0.14 * f(row, "redress_need")
    )

    if stakeholder_assumption_risk >= 0.48:
        action = "stakeholder_assumption_review_required"
    elif f(row, "representation_quality") < 0.45:
        action = "improve_representation_quality"
    elif f(row, "redress_need") >= 0.65:
        action = "design_redress_path"
    else:
        action = "monitor_stakeholder_assumption"

    stakeholder_rows.append(
        {
            "stakeholder_assumption_id": row["stakeholder_assumption_id"],
            "assumption_id": row["assumption_id"],
            "assumption_statement": assumption_names.get(row["assumption_id"], row["assumption_id"]),
            "stakeholder_group": row["stakeholder_group"],
            "assumed_response": row["assumed_response"],
            "stakeholder_assumption_risk": round(stakeholder_assumption_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "inclusion_quality": row["inclusion_quality"],
            "affectedness": row["affectedness"],
            "trust_dependency": row["trust_dependency"],
            "burden_risk": row["burden_risk"],
            "knowledge_value": row["knowledge_value"],
            "representation_quality": row["representation_quality"],
            "redress_need": row["redress_need"],
        }
    )

stakeholder_rows.sort(key=lambda item: item["stakeholder_assumption_risk"], reverse=True)

write_csv(
    TABLES / "stakeholder_assumption_review.csv",
    stakeholder_rows,
    [
        "stakeholder_assumption_id",
        "assumption_id",
        "assumption_statement",
        "stakeholder_group",
        "assumed_response",
        "stakeholder_assumption_risk",
        "recommended_action",
        "source_review_action",
        "inclusion_quality",
        "affectedness",
        "trust_dependency",
        "burden_risk",
        "knowledge_value",
        "representation_quality",
        "redress_need",
    ],
)

# ---------------------------------------------------------------------
# 8. System response review
# ---------------------------------------------------------------------

system_rows: list[dict[str, object]] = []

for row in system_responses:
    system_risk = (
        0.14 * f(row, "feedback_risk")
        + 0.13 * f(row, "adaptation_risk")
        + 0.15 * f(row, "burden_shift_risk")
        + 0.11 * f(row, "delay_risk")
        + 0.13 * f(row, "metric_gaming_risk")
        + 0.12 * f(row, "resistance_risk")
        + 0.12 * f(row, "leverage_relevance")
        - 0.10 * f(row, "monitoring_quality")
    )

    if system_risk >= 0.58:
        action = "system_response_review_required"
    elif f(row, "monitoring_quality") < 0.58:
        action = "improve_system_monitoring"
    elif f(row, "burden_shift_risk") >= 0.75:
        action = "burden_shift_review_required"
    else:
        action = "monitor_system_response"

    system_rows.append(
        {
            "system_assumption_id": row["system_assumption_id"],
            "assumption_id": row["assumption_id"],
            "assumption_statement": assumption_names.get(row["assumption_id"], row["assumption_id"]),
            "system_response": row["system_response"],
            "system_response_risk": round(system_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "feedback_risk": row["feedback_risk"],
            "adaptation_risk": row["adaptation_risk"],
            "burden_shift_risk": row["burden_shift_risk"],
            "delay_risk": row["delay_risk"],
            "metric_gaming_risk": row["metric_gaming_risk"],
            "resistance_risk": row["resistance_risk"],
            "leverage_relevance": row["leverage_relevance"],
            "monitoring_quality": row["monitoring_quality"],
        }
    )

system_rows.sort(key=lambda item: item["system_response_risk"], reverse=True)

write_csv(
    TABLES / "system_response_assumption_review.csv",
    system_rows,
    [
        "system_assumption_id",
        "assumption_id",
        "assumption_statement",
        "system_response",
        "system_response_risk",
        "recommended_action",
        "source_review_action",
        "feedback_risk",
        "adaptation_risk",
        "burden_shift_risk",
        "delay_risk",
        "metric_gaming_risk",
        "resistance_risk",
        "leverage_relevance",
        "monitoring_quality",
    ],
)

# ---------------------------------------------------------------------
# 9. Future-facing assumption review
# ---------------------------------------------------------------------

future_rows: list[dict[str, object]] = []

for row in future_assumptions:
    future_risk = (
        0.12 * (1 - f(row, "plausibility"))
        + 0.18 * f(row, "uncertainty")
        + 0.18 * f(row, "strategic_dependency")
        - 0.10 * f(row, "monitorability")
        + 0.14 * f(row, "scenario_sensitivity")
        - 0.10 * f(row, "early_signal_quality")
        - 0.10 * f(row, "adaptation_options")
        - 0.08 * f(row, "review_cadence_quality")
    )

    if future_risk >= 0.34:
        action = "scenario_stress_test_required"
    elif f(row, "monitorability") < 0.60:
        action = "improve_monitorability"
    elif f(row, "adaptation_options") < 0.60:
        action = "design_adaptive_pathway"
    else:
        action = "monitor_future_condition"

    future_rows.append(
        {
            "future_assumption_id": row["future_assumption_id"],
            "assumption_id": row["assumption_id"],
            "assumption_statement": assumption_names.get(row["assumption_id"], row["assumption_id"]),
            "future_condition": row["future_condition"],
            "future_assumption_risk": round(future_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "plausibility": row["plausibility"],
            "uncertainty": row["uncertainty"],
            "strategic_dependency": row["strategic_dependency"],
            "monitorability": row["monitorability"],
            "scenario_sensitivity": row["scenario_sensitivity"],
            "early_signal_quality": row["early_signal_quality"],
            "adaptation_options": row["adaptation_options"],
            "review_cadence_quality": row["review_cadence_quality"],
        }
    )

future_rows.sort(key=lambda item: item["future_assumption_risk"], reverse=True)

write_csv(
    TABLES / "future_assumption_review.csv",
    future_rows,
    [
        "future_assumption_id",
        "assumption_id",
        "assumption_statement",
        "future_condition",
        "future_assumption_risk",
        "recommended_action",
        "source_review_action",
        "plausibility",
        "uncertainty",
        "strategic_dependency",
        "monitorability",
        "scenario_sensitivity",
        "early_signal_quality",
        "adaptation_options",
        "review_cadence_quality",
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
            "assumption_id": row["assumption_id"],
            "assumption_statement": assumption_names.get(row["assumption_id"], row["assumption_id"]),
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
        "assumption_id",
        "assumption_statement",
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

top_assumptions = assumption_rows[:8]
top_tests = test_rows[:6]
weak_evidence = evidence_rows[:6]
top_prototypes = prototype_rows[:6]
top_toc_risk = toc_rows[:6]
top_options = option_rows[:5]
stakeholder_risks = stakeholder_rows[:6]
system_risks = system_rows[:6]
future_risks = future_rows[:6]
top_triggers = trigger_rows[:6]

report: list[str] = []

report.append("# Assumption Mapping for Strategic Ideas Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic identifies which strategic assumptions are most critical, uncertain, weakly evidenced, stakeholder-sensitive, system-sensitive, "
    "and worth testing before major commitment. It connects assumptions to evidence, tests, prototypes, theory-of-change links, option confidence, "
    "stakeholder risks, system response risks, future-facing uncertainty, revision triggers, and decision memory."
)

report.append("")
report.append("## Highest evidence-adjusted assumption risks")
report.append("")
for item in top_assumptions:
    report.append(
        f"- **{item['assumption_id']} — {item['assumption_statement']}** for **{item['idea_name']}**: "
        f"risk {item['evidence_adjusted_risk']}; learning value {item['learning_value']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Priority tests")
report.append("")
for item in top_tests:
    report.append(
        f"- **{item['test_id']} — {item['test_name']}** for **{item['assumption_statement']}**: "
        f"test value {item['test_value_score']}; action: {item['recommended_action']}; if failed: {item['decision_if_failed']}."
    )

report.append("")
report.append("## Evidence needing strengthening")
report.append("")
for item in weak_evidence:
    report.append(
        f"- **{item['evidence_id']} — {item['evidence_type']}** for **{item['assumption_statement']}**: "
        f"quality {item['evidence_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strong prototype learning candidates")
report.append("")
for item in top_prototypes:
    report.append(
        f"- **{item['prototype_id']} — {item['prototype_name']}** for **{item['idea_name']}**: "
        f"learning score {item['prototype_learning_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest-risk theory-of-change links")
report.append("")
for item in top_toc_risk:
    report.append(
        f"- **{item['toc_link_id']} — {item['link_stage']}** for **{item['idea_name']}**: "
        f"risk {item['theory_link_risk_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Option confidence")
report.append("")
for item in top_options:
    report.append(
        f"- **{item['option_id']} — {item['option_name']}** for **{item['idea_name']}**: "
        f"confidence {item['option_confidence_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Stakeholder assumption risks")
report.append("")
for item in stakeholder_risks:
    report.append(
        f"- **{item['stakeholder_assumption_id']} — {item['stakeholder_group']}**: "
        f"risk {item['stakeholder_assumption_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## System response assumption risks")
report.append("")
for item in system_risks:
    report.append(
        f"- **{item['system_assumption_id']} — {item['system_response']}**: "
        f"risk {item['system_response_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Future-facing assumption risks")
report.append("")
for item in future_risks:
    report.append(
        f"- **{item['future_assumption_id']} — {item['future_condition']}**: "
        f"risk {item['future_assumption_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strong revision triggers")
report.append("")
for item in top_triggers:
    report.append(
        f"- **{item['trigger_id']} — {item['trigger_name']}**: "
        f"trigger quality {item['trigger_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "Assumption mapping turns strategic belief into a learning agenda. The strongest use of this diagnostic is not to eliminate uncertainty, but to "
    "prioritize the assumptions that must be tested before commitment. High-criticality, high-uncertainty, weakly evidenced assumptions should shape "
    "prototype design, stakeholder inquiry, scenario review, governance gates, revision triggers, and decision-memory records."
)

(REPORTS / "assumption_mapping_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_assumptions": top_assumptions,
    "top_tests": top_tests,
    "weak_evidence": weak_evidence,
    "top_prototypes": top_prototypes,
    "top_toc_risk": top_toc_risk,
    "top_options": top_options,
    "stakeholder_risks": stakeholder_risks,
    "system_risks": system_risks,
    "future_risks": future_risks,
    "top_triggers": top_triggers,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced assumption mapping diagnostics complete.")
print(f"Wrote: {TABLES / 'assumption_risk_scores.csv'}")
print(f"Wrote: {TABLES / 'evidence_review_scores.csv'}")
print(f"Wrote: {TABLES / 'test_prioritization_scores.csv'}")
print(f"Wrote: {TABLES / 'prototype_learning_scores.csv'}")
print(f"Wrote: {TABLES / 'theory_of_change_assumption_scores.csv'}")
print(f"Wrote: {TABLES / 'option_confidence_scores.csv'}")
print(f"Wrote: {TABLES / 'stakeholder_assumption_review.csv'}")
print(f"Wrote: {TABLES / 'system_response_assumption_review.csv'}")
print(f"Wrote: {TABLES / 'future_assumption_review.csv'}")
print(f"Wrote: {TABLES / 'revision_trigger_review.csv'}")
print(f"Wrote: {REPORTS / 'assumption_mapping_diagnostic_report.md'}")
