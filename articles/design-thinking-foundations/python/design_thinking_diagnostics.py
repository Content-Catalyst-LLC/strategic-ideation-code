#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Design Thinking Foundations.

This dependency-light workflow uses only the Python standard library.

It produces:
- design capability scores
- stakeholder inquiry scores
- problem reframing scores
- idea portfolio scores
- prototype learning scores
- test evidence scores
- systems design review
- ethical design review
- decision linkage scores
- institutional learning scores
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


contexts = read_csv(RAW / "design_contexts.csv")
inquiries = read_csv(RAW / "stakeholder_inquiry.csv")
frames = read_csv(RAW / "problem_frames.csv")
ideas = read_csv(RAW / "idea_portfolios.csv")
prototypes = read_csv(RAW / "prototypes.csv")
tests = read_csv(RAW / "test_evidence.csv")
systems = read_csv(RAW / "systems_design.csv")
ethics = read_csv(RAW / "ethical_design.csv")
decisions = read_csv(RAW / "decision_linkage.csv")
learning = read_csv(RAW / "institutional_learning.csv")

context_names = {row["context_id"]: row["context_name"] for row in contexts}
idea_names = {row["idea_id"]: row["idea_name"] for row in ideas}
prototype_names = {row["prototype_id"]: row["prototype_name"] for row in prototypes}

# ---------------------------------------------------------------------
# 1. Design capability scoring
# ---------------------------------------------------------------------

capability_rows: list[dict[str, object]] = []

for row in contexts:
    capability_score = (
        0.12 * f(row, "empathy_depth")
        + 0.13 * f(row, "reframing_capacity")
        + 0.10 * f(row, "divergence_quality")
        + 0.10 * f(row, "convergence_quality")
        + 0.12 * f(row, "prototyping_strength")
        + 0.12 * f(row, "testing_quality")
        + 0.11 * f(row, "systems_awareness")
        + 0.10 * f(row, "ethical_review")
        + 0.10 * f(row, "decision_linkage")
        + 0.06 * f(row, "adaptability")
        + 0.04 * f(row, "institutional_memory")
    )

    superficiality_risk = (
        0.18 * (1 - f(row, "empathy_depth"))
        + 0.14 * (1 - f(row, "reframing_capacity"))
        + 0.12 * (1 - f(row, "testing_quality"))
        + 0.12 * (1 - f(row, "systems_awareness"))
        + 0.12 * (1 - f(row, "ethical_review"))
        + 0.16 * (1 - f(row, "decision_linkage"))
        + 0.10 * (1 - f(row, "institutional_memory"))
        + 0.06 * (1 - f(row, "adaptability"))
    )

    if capability_score >= 0.72:
        diagnosis = "strong_design_thinking_capability"
    elif superficiality_risk >= 0.62:
        diagnosis = "high_superficiality_risk"
    elif f(row, "decision_linkage") < 0.45:
        diagnosis = "weak_decision_linkage"
    elif f(row, "systems_awareness") < 0.45:
        diagnosis = "add_systems_review"
    elif f(row, "ethical_review") < 0.45:
        diagnosis = "add_ethics_and_power_review"
    else:
        diagnosis = "developing_capability"

    capability_rows.append(
        {
            "context_id": row["context_id"],
            "context_name": row["context_name"],
            "organization_type": row["organization_type"],
            "domain": row["domain"],
            "design_capability_score": round(capability_score, 4),
            "superficiality_risk": round(superficiality_risk, 4),
            "diagnosis": diagnosis,
            "empathy_depth": row["empathy_depth"],
            "reframing_capacity": row["reframing_capacity"],
            "divergence_quality": row["divergence_quality"],
            "convergence_quality": row["convergence_quality"],
            "prototyping_strength": row["prototyping_strength"],
            "testing_quality": row["testing_quality"],
            "systems_awareness": row["systems_awareness"],
            "ethical_review": row["ethical_review"],
            "decision_linkage": row["decision_linkage"],
            "adaptability": row["adaptability"],
            "institutional_memory": row["institutional_memory"],
            "description": row["description"],
        }
    )

capability_rows.sort(key=lambda item: item["design_capability_score"], reverse=True)

capability_fields = [
    "context_id",
    "context_name",
    "organization_type",
    "domain",
    "design_capability_score",
    "superficiality_risk",
    "diagnosis",
    "empathy_depth",
    "reframing_capacity",
    "divergence_quality",
    "convergence_quality",
    "prototyping_strength",
    "testing_quality",
    "systems_awareness",
    "ethical_review",
    "decision_linkage",
    "adaptability",
    "institutional_memory",
    "description",
]

write_csv(TABLES / "design_capability_scores.csv", capability_rows, capability_fields)
write_csv(PROCESSED / "design_capability_scores.csv", capability_rows, capability_fields)

# ---------------------------------------------------------------------
# 2. Stakeholder inquiry scoring
# ---------------------------------------------------------------------

inquiry_rows: list[dict[str, object]] = []

for row in inquiries:
    inquiry_quality = (
        0.13 * f(row, "sample_quality")
        + 0.16 * f(row, "contextual_depth")
        + 0.14 * f(row, "behavioral_observation")
        + 0.11 * f(row, "trust_sensitivity")
        + 0.12 * f(row, "burden_visibility")
        + 0.12 * f(row, "representation_quality")
        + 0.12 * f(row, "interpretation_quality")
        + 0.10 * f(row, "decision_relevance")
    )

    if inquiry_quality >= 0.74:
        action = "strong_inquiry_base"
    elif f(row, "behavioral_observation") < 0.40:
        action = "add_observation_not_only_interviews"
    elif f(row, "representation_quality") < 0.45:
        action = "improve_representation"
    elif f(row, "decision_relevance") < 0.45:
        action = "connect_inquiry_to_decision"
    else:
        action = "strengthen_inquiry"

    inquiry_rows.append(
        {
            "inquiry_id": row["inquiry_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "stakeholder_group": row["stakeholder_group"],
            "inquiry_method": row["inquiry_method"],
            "inquiry_quality_score": round(inquiry_quality, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "sample_quality": row["sample_quality"],
            "contextual_depth": row["contextual_depth"],
            "behavioral_observation": row["behavioral_observation"],
            "trust_sensitivity": row["trust_sensitivity"],
            "burden_visibility": row["burden_visibility"],
            "representation_quality": row["representation_quality"],
            "interpretation_quality": row["interpretation_quality"],
            "decision_relevance": row["decision_relevance"],
        }
    )

inquiry_rows.sort(key=lambda item: item["inquiry_quality_score"], reverse=True)

write_csv(
    TABLES / "stakeholder_inquiry_scores.csv",
    inquiry_rows,
    [
        "inquiry_id",
        "context_id",
        "context_name",
        "stakeholder_group",
        "inquiry_method",
        "inquiry_quality_score",
        "recommended_action",
        "source_review_action",
        "sample_quality",
        "contextual_depth",
        "behavioral_observation",
        "trust_sensitivity",
        "burden_visibility",
        "representation_quality",
        "interpretation_quality",
        "decision_relevance",
    ],
)

# ---------------------------------------------------------------------
# 3. Problem reframing scoring
# ---------------------------------------------------------------------

frame_rows: list[dict[str, object]] = []

for row in frames:
    reframing_quality = (
        0.14 * f(row, "inquiry_influence")
        + 0.12 * f(row, "boundary_quality")
        + 0.13 * f(row, "stakeholder_evidence")
        + 0.14 * f(row, "causal_depth")
        + 0.13 * f(row, "systems_context")
        + 0.12 * f(row, "ethical_awareness")
        + 0.10 * f(row, "decision_usefulness")
        + 0.12 * f(row, "reframing_maturity")
    )

    if reframing_quality >= 0.75:
        action = "strong_reframe_ready_for_prototyping"
    elif f(row, "inquiry_influence") < 0.45:
        action = "increase_inquiry_before_reframing"
    elif f(row, "causal_depth") < 0.45:
        action = "deepen_causal_analysis"
    elif f(row, "systems_context") < 0.45:
        action = "add_systems_context"
    else:
        action = "strengthen_reframe"

    frame_rows.append(
        {
            "frame_id": row["frame_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "initial_frame": row["initial_frame"],
            "reframed_problem": row["reframed_problem"],
            "frame_source": row["frame_source"],
            "reframing_quality_score": round(reframing_quality, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "inquiry_influence": row["inquiry_influence"],
            "boundary_quality": row["boundary_quality"],
            "stakeholder_evidence": row["stakeholder_evidence"],
            "causal_depth": row["causal_depth"],
            "systems_context": row["systems_context"],
            "ethical_awareness": row["ethical_awareness"],
            "decision_usefulness": row["decision_usefulness"],
            "reframing_maturity": row["reframing_maturity"],
        }
    )

frame_rows.sort(key=lambda item: item["reframing_quality_score"], reverse=True)

write_csv(
    TABLES / "problem_reframing_scores.csv",
    frame_rows,
    [
        "frame_id",
        "context_id",
        "context_name",
        "initial_frame",
        "reframed_problem",
        "frame_source",
        "reframing_quality_score",
        "recommended_action",
        "source_review_action",
        "inquiry_influence",
        "boundary_quality",
        "stakeholder_evidence",
        "causal_depth",
        "systems_context",
        "ethical_awareness",
        "decision_usefulness",
        "reframing_maturity",
    ],
)

# ---------------------------------------------------------------------
# 4. Idea portfolio scoring
# ---------------------------------------------------------------------

idea_rows: list[dict[str, object]] = []

for row in ideas:
    idea_quality = (
        0.10 * f(row, "novelty")
        + 0.14 * f(row, "strategic_fit")
        + 0.14 * f(row, "human_centered_fit")
        + 0.10 * f(row, "feasibility")
        + 0.12 * f(row, "evidence_strength")
        + 0.12 * f(row, "system_awareness")
        + 0.12 * f(row, "ethical_quality")
        + 0.10 * f(row, "learning_value")
        + 0.06 * f(row, "reversibility")
    )

    premature_scale_risk = (
        0.22 * (1 - f(row, "evidence_strength"))
        + 0.16 * (1 - f(row, "system_awareness"))
        + 0.14 * (1 - f(row, "ethical_quality"))
        + 0.16 * (1 - f(row, "learning_value"))
        + 0.12 * (1 - f(row, "reversibility"))
        + 0.10 * (1 - f(row, "human_centered_fit"))
        + 0.10 * (1 - f(row, "feasibility"))
    )

    if idea_quality >= 0.74:
        action = "strong_candidate_for_prototype"
    elif premature_scale_risk >= 0.56:
        action = "do_not_scale_test_assumptions"
    elif f(row, "evidence_strength") < 0.45:
        action = "evidence_gap_before_commitment"
    elif f(row, "ethical_quality") < 0.45:
        action = "ethical_review_required"
    else:
        action = "prototype_and_monitor"

    idea_rows.append(
        {
            "idea_id": row["idea_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "idea_name": row["idea_name"],
            "idea_type": row["idea_type"],
            "idea_quality_score": round(idea_quality, 4),
            "premature_scale_risk": round(premature_scale_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "novelty": row["novelty"],
            "strategic_fit": row["strategic_fit"],
            "human_centered_fit": row["human_centered_fit"],
            "feasibility": row["feasibility"],
            "evidence_strength": row["evidence_strength"],
            "system_awareness": row["system_awareness"],
            "ethical_quality": row["ethical_quality"],
            "learning_value": row["learning_value"],
            "reversibility": row["reversibility"],
        }
    )

idea_rows.sort(key=lambda item: item["idea_quality_score"], reverse=True)

write_csv(
    TABLES / "idea_portfolio_scores.csv",
    idea_rows,
    [
        "idea_id",
        "context_id",
        "context_name",
        "idea_name",
        "idea_type",
        "idea_quality_score",
        "premature_scale_risk",
        "recommended_action",
        "source_review_action",
        "novelty",
        "strategic_fit",
        "human_centered_fit",
        "feasibility",
        "evidence_strength",
        "system_awareness",
        "ethical_quality",
        "learning_value",
        "reversibility",
    ],
)

# ---------------------------------------------------------------------
# 5. Prototype learning scoring
# ---------------------------------------------------------------------

prototype_rows: list[dict[str, object]] = []

for row in prototypes:
    prototype_learning_score = (
        0.08 * f(row, "prototype_fidelity")
        + 0.16 * f(row, "learning_potential")
        + 0.10 * f(row, "test_speed")
        + 0.12 * f(row, "stakeholder_inclusion")
        + 0.12 * f(row, "realism")
        + 0.12 * f(row, "system_signal_quality")
        + 0.11 * f(row, "ethical_safety")
        + 0.08 * f(row, "cost_efficiency")
        + 0.11 * f(row, "decision_usefulness")
    )

    if prototype_learning_score >= 0.75:
        action = "strong_learning_prototype"
    elif f(row, "decision_usefulness") < 0.45:
        action = "connect_prototype_to_decision"
    elif f(row, "stakeholder_inclusion") < 0.50:
        action = "increase_stakeholder_inclusion"
    elif f(row, "system_signal_quality") < 0.45:
        action = "add_system_signal_review"
    else:
        action = "usable_prototype_test"

    prototype_rows.append(
        {
            "prototype_id": row["prototype_id"],
            "idea_id": row["idea_id"],
            "idea_name": idea_names.get(row["idea_id"], row["idea_id"]),
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "prototype_name": row["prototype_name"],
            "prototype_type": row["prototype_type"],
            "assumption_tested": row["assumption_tested"],
            "prototype_learning_score": round(prototype_learning_score, 4),
            "recommended_action": action,
            "success_threshold": row["success_threshold"],
            "decision_if_failed": row["decision_if_failed"],
            "prototype_fidelity": row["prototype_fidelity"],
            "learning_potential": row["learning_potential"],
            "test_speed": row["test_speed"],
            "stakeholder_inclusion": row["stakeholder_inclusion"],
            "realism": row["realism"],
            "system_signal_quality": row["system_signal_quality"],
            "ethical_safety": row["ethical_safety"],
            "cost_efficiency": row["cost_efficiency"],
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
        "context_id",
        "context_name",
        "prototype_name",
        "prototype_type",
        "assumption_tested",
        "prototype_learning_score",
        "recommended_action",
        "success_threshold",
        "decision_if_failed",
        "prototype_fidelity",
        "learning_potential",
        "test_speed",
        "stakeholder_inclusion",
        "realism",
        "system_signal_quality",
        "ethical_safety",
        "cost_efficiency",
        "decision_usefulness",
    ],
)

# ---------------------------------------------------------------------
# 6. Test evidence scoring
# ---------------------------------------------------------------------

test_rows: list[dict[str, object]] = []

for row in tests:
    evidence_quality = (
        0.13 * f(row, "reliability")
        + 0.17 * f(row, "relevance")
        + 0.11 * f(row, "transferability")
        + 0.13 * f(row, "behavioral_signal")
        + 0.12 * f(row, "stakeholder_signal")
        + 0.10 * f(row, "implementation_signal")
        + 0.10 * f(row, "system_signal")
        - 0.08 * f(row, "bias_risk")
        + 0.12 * f(row, "interpretation_quality")
    )

    if evidence_quality >= 0.70:
        action = "strong_test_evidence"
    elif f(row, "relevance") < 0.45:
        action = "evidence_mismatch"
    elif f(row, "behavioral_signal") < 0.40:
        action = "do_not_claim_behavior_change"
    elif f(row, "system_signal") < 0.40:
        action = "add_system_effect_review"
    else:
        action = "strengthen_test_evidence"

    test_rows.append(
        {
            "test_id": row["test_id"],
            "prototype_id": row["prototype_id"],
            "prototype_name": prototype_names.get(row["prototype_id"], row["prototype_id"]),
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "test_method": row["test_method"],
            "evidence_type": row["evidence_type"],
            "evidence_quality_score": round(evidence_quality, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "reliability": row["reliability"],
            "relevance": row["relevance"],
            "transferability": row["transferability"],
            "behavioral_signal": row["behavioral_signal"],
            "stakeholder_signal": row["stakeholder_signal"],
            "implementation_signal": row["implementation_signal"],
            "system_signal": row["system_signal"],
            "bias_risk": row["bias_risk"],
            "interpretation_quality": row["interpretation_quality"],
        }
    )

test_rows.sort(key=lambda item: item["evidence_quality_score"], reverse=True)

write_csv(
    TABLES / "test_evidence_scores.csv",
    test_rows,
    [
        "test_id",
        "prototype_id",
        "prototype_name",
        "context_id",
        "context_name",
        "test_method",
        "evidence_type",
        "evidence_quality_score",
        "recommended_action",
        "source_review_action",
        "reliability",
        "relevance",
        "transferability",
        "behavioral_signal",
        "stakeholder_signal",
        "implementation_signal",
        "system_signal",
        "bias_risk",
        "interpretation_quality",
    ],
)

# ---------------------------------------------------------------------
# 7. Systems design review
# ---------------------------------------------------------------------

system_rows: list[dict[str, object]] = []

for row in systems:
    system_risk = (
        0.14 * f(row, "feedback_risk")
        + 0.11 * f(row, "delay_risk")
        + 0.16 * f(row, "burden_shift_risk")
        + 0.14 * f(row, "incentive_misalignment")
        + 0.12 * f(row, "metric_gaming_risk")
        + 0.12 * f(row, "context_dependency")
        + 0.11 * f(row, "leverage_relevance")
        - 0.10 * f(row, "monitoring_quality")
    )

    if system_risk >= 0.60:
        action = "systems_review_required"
    elif f(row, "burden_shift_risk") >= 0.75:
        action = "burden_shift_review_required"
    elif f(row, "monitoring_quality") < 0.45:
        action = "improve_system_monitoring"
    elif f(row, "metric_gaming_risk") >= 0.65:
        action = "add_countermetrics"
    else:
        action = "monitor_system_effects"

    system_rows.append(
        {
            "system_id": row["system_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "design_issue": row["design_issue"],
            "systems_design_risk": round(system_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "feedback_risk": row["feedback_risk"],
            "delay_risk": row["delay_risk"],
            "burden_shift_risk": row["burden_shift_risk"],
            "incentive_misalignment": row["incentive_misalignment"],
            "metric_gaming_risk": row["metric_gaming_risk"],
            "context_dependency": row["context_dependency"],
            "leverage_relevance": row["leverage_relevance"],
            "monitoring_quality": row["monitoring_quality"],
        }
    )

system_rows.sort(key=lambda item: item["systems_design_risk"], reverse=True)

write_csv(
    TABLES / "systems_design_review.csv",
    system_rows,
    [
        "system_id",
        "context_id",
        "context_name",
        "design_issue",
        "systems_design_risk",
        "recommended_action",
        "source_review_action",
        "feedback_risk",
        "delay_risk",
        "burden_shift_risk",
        "incentive_misalignment",
        "metric_gaming_risk",
        "context_dependency",
        "leverage_relevance",
        "monitoring_quality",
    ],
)

# ---------------------------------------------------------------------
# 8. Ethical design review
# ---------------------------------------------------------------------

ethics_rows: list[dict[str, object]] = []

for row in ethics:
    ethics_score = (
        0.13 * f(row, "participation_quality")
        + 0.14 * f(row, "power_awareness")
        + 0.13 * f(row, "burden_visibility")
        + 0.11 * f(row, "consent_quality")
        + 0.12 * f(row, "representation_quality")
        + 0.12 * f(row, "redress_quality")
        + 0.13 * f(row, "decision_traceability")
        + 0.12 * f(row, "harm_monitoring")
    )

    ethical_risk = 1 - ethics_score

    if ethics_score >= 0.76:
        action = "strong_ethical_design_review"
    elif f(row, "power_awareness") < 0.45:
        action = "add_power_mapping"
    elif f(row, "redress_quality") < 0.45:
        action = "add_redress_path"
    elif f(row, "decision_traceability") < 0.45:
        action = "trace_feedback_to_decisions"
    else:
        action = "strengthen_ethics_review"

    ethics_rows.append(
        {
            "ethics_id": row["ethics_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "ethical_issue": row["ethical_issue"],
            "ethical_design_score": round(ethics_score, 4),
            "ethical_design_risk": round(ethical_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "participation_quality": row["participation_quality"],
            "power_awareness": row["power_awareness"],
            "burden_visibility": row["burden_visibility"],
            "consent_quality": row["consent_quality"],
            "representation_quality": row["representation_quality"],
            "redress_quality": row["redress_quality"],
            "decision_traceability": row["decision_traceability"],
            "harm_monitoring": row["harm_monitoring"],
        }
    )

ethics_rows.sort(key=lambda item: item["ethical_design_risk"], reverse=True)

write_csv(
    TABLES / "ethical_design_review.csv",
    ethics_rows,
    [
        "ethics_id",
        "context_id",
        "context_name",
        "ethical_issue",
        "ethical_design_score",
        "ethical_design_risk",
        "recommended_action",
        "source_review_action",
        "participation_quality",
        "power_awareness",
        "burden_visibility",
        "consent_quality",
        "representation_quality",
        "redress_quality",
        "decision_traceability",
        "harm_monitoring",
    ],
)

# ---------------------------------------------------------------------
# 9. Decision linkage scoring
# ---------------------------------------------------------------------

decision_rows: list[dict[str, object]] = []

for row in decisions:
    decision_linkage_score = (
        0.12 * f(row, "artifact_quality")
        + 0.14 * f(row, "evidence_quality")
        + 0.15 * f(row, "decision_relevance")
        + 0.15 * f(row, "authority_connection")
        + 0.11 * f(row, "resource_connection")
        + 0.12 * f(row, "revision_trigger_quality")
        + 0.10 * f(row, "learning_memory_quality")
        + 0.11 * f(row, "implementation_path_quality")
    )

    if decision_linkage_score >= 0.72:
        action = "strong_decision_linkage"
    elif f(row, "authority_connection") < 0.45:
        action = "connect_to_decision_authority"
    elif f(row, "resource_connection") < 0.45:
        action = "connect_to_resource_decisions"
    elif f(row, "revision_trigger_quality") < 0.45:
        action = "define_revision_triggers"
    else:
        action = "strengthen_decision_linkage"

    decision_rows.append(
        {
            "decision_id": row["decision_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "design_artifact": row["design_artifact"],
            "decision_type": row["decision_type"],
            "decision_linkage_score": round(decision_linkage_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "artifact_quality": row["artifact_quality"],
            "evidence_quality": row["evidence_quality"],
            "decision_relevance": row["decision_relevance"],
            "authority_connection": row["authority_connection"],
            "resource_connection": row["resource_connection"],
            "revision_trigger_quality": row["revision_trigger_quality"],
            "learning_memory_quality": row["learning_memory_quality"],
            "implementation_path_quality": row["implementation_path_quality"],
        }
    )

decision_rows.sort(key=lambda item: item["decision_linkage_score"], reverse=True)

write_csv(
    TABLES / "decision_linkage_scores.csv",
    decision_rows,
    [
        "decision_id",
        "context_id",
        "context_name",
        "design_artifact",
        "decision_type",
        "decision_linkage_score",
        "recommended_action",
        "source_review_action",
        "artifact_quality",
        "evidence_quality",
        "decision_relevance",
        "authority_connection",
        "resource_connection",
        "revision_trigger_quality",
        "learning_memory_quality",
        "implementation_path_quality",
    ],
)

# ---------------------------------------------------------------------
# 10. Institutional learning scores
# ---------------------------------------------------------------------

learning_rows: list[dict[str, object]] = []

for row in learning:
    institutional_learning_score = (
        0.12 * f(row, "observation_quality")
        + 0.13 * f(row, "frame_revision_quality")
        + 0.12 * f(row, "prototype_record_quality")
        + 0.12 * f(row, "test_record_quality")
        + 0.13 * f(row, "decision_memory_quality")
        + 0.12 * f(row, "reuse_quality")
        + 0.13 * f(row, "governance_review_quality")
        + 0.13 * f(row, "adaptation_quality")
    )

    if institutional_learning_score >= 0.74:
        action = "strong_design_learning_system"
    elif f(row, "decision_memory_quality") < 0.45:
        action = "build_decision_memory"
    elif f(row, "reuse_quality") < 0.45:
        action = "improve_reuse_and_retrieval"
    elif f(row, "governance_review_quality") < 0.45:
        action = "connect_learning_to_governance"
    else:
        action = "strengthen_learning_system"

    learning_rows.append(
        {
            "learning_id": row["learning_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "learning_system": row["learning_system"],
            "institutional_learning_score": round(institutional_learning_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "observation_quality": row["observation_quality"],
            "frame_revision_quality": row["frame_revision_quality"],
            "prototype_record_quality": row["prototype_record_quality"],
            "test_record_quality": row["test_record_quality"],
            "decision_memory_quality": row["decision_memory_quality"],
            "reuse_quality": row["reuse_quality"],
            "governance_review_quality": row["governance_review_quality"],
            "adaptation_quality": row["adaptation_quality"],
        }
    )

learning_rows.sort(key=lambda item: item["institutional_learning_score"], reverse=True)

write_csv(
    TABLES / "institutional_learning_scores.csv",
    learning_rows,
    [
        "learning_id",
        "context_id",
        "context_name",
        "learning_system",
        "institutional_learning_score",
        "recommended_action",
        "source_review_action",
        "observation_quality",
        "frame_revision_quality",
        "prototype_record_quality",
        "test_record_quality",
        "decision_memory_quality",
        "reuse_quality",
        "governance_review_quality",
        "adaptation_quality",
    ],
)

# ---------------------------------------------------------------------
# 11. Strategist report
# ---------------------------------------------------------------------

top_capability = capability_rows[:5]
high_superficiality = sorted(capability_rows, key=lambda item: item["superficiality_risk"], reverse=True)[:5]
top_inquiry = inquiry_rows[:5]
top_frames = frame_rows[:5]
top_ideas = idea_rows[:5]
top_prototypes = prototype_rows[:5]
top_tests = test_rows[:5]
system_risks = system_rows[:5]
ethical_risks = ethics_rows[:5]
top_decisions = decision_rows[:5]
top_learning = learning_rows[:5]

report: list[str] = []

report.append("# Design Thinking Foundations Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic evaluates design thinking as a strategic capability rather than a workshop ritual. It assesses empathy depth, reframing, "
    "divergence and convergence, prototype learning, testing quality, systems awareness, ethical review, decision linkage, and institutional memory."
)

report.append("")
report.append("## Strongest design thinking capability profiles")
report.append("")
for item in top_capability:
    report.append(
        f"- **{item['context_id']} — {item['context_name']}**: capability {item['design_capability_score']}; "
        f"superficiality risk {item['superficiality_risk']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest superficiality risks")
report.append("")
for item in high_superficiality:
    report.append(
        f"- **{item['context_id']} — {item['context_name']}**: superficiality risk {item['superficiality_risk']}; "
        f"diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Strong stakeholder inquiry examples")
report.append("")
for item in top_inquiry:
    report.append(
        f"- **{item['inquiry_id']} — {item['stakeholder_group']}** in **{item['context_name']}**: "
        f"inquiry quality {item['inquiry_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strong reframing examples")
report.append("")
for item in top_frames:
    report.append(
        f"- **{item['frame_id']} — {item['reframed_problem']}**: "
        f"reframing quality {item['reframing_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strong idea candidates")
report.append("")
for item in top_ideas:
    report.append(
        f"- **{item['idea_id']} — {item['idea_name']}**: "
        f"idea quality {item['idea_quality_score']}; premature scale risk {item['premature_scale_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strong prototype learning candidates")
report.append("")
for item in top_prototypes:
    report.append(
        f"- **{item['prototype_id']} — {item['prototype_name']}**: "
        f"learning score {item['prototype_learning_score']}; threshold {item['success_threshold']}; if failed: {item['decision_if_failed']}."
    )

report.append("")
report.append("## Strong test evidence")
report.append("")
for item in top_tests:
    report.append(
        f"- **{item['test_id']} — {item['test_method']}** for **{item['prototype_name']}**: "
        f"evidence quality {item['evidence_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Systems design risks")
report.append("")
for item in system_risks:
    report.append(
        f"- **{item['system_id']} — {item['design_issue']}**: "
        f"systems risk {item['systems_design_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Ethical design risks")
report.append("")
for item in ethical_risks:
    report.append(
        f"- **{item['ethics_id']} — {item['ethical_issue']}**: "
        f"ethical risk {item['ethical_design_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strong decision linkage")
report.append("")
for item in top_decisions:
    report.append(
        f"- **{item['decision_id']} — {item['design_artifact']}**: "
        f"decision linkage {item['decision_linkage_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strong institutional learning systems")
report.append("")
for item in top_learning:
    report.append(
        f"- **{item['learning_id']} — {item['learning_system']}**: "
        f"institutional learning {item['institutional_learning_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "Design thinking becomes strategically valuable when inquiry changes framing, prototypes test real assumptions, evidence affects decisions, "
    "systems review prevents local fixes from producing broader harm, ethical review addresses power and burden, and institutional memory preserves learning."
)

(REPORTS / "design_thinking_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_capability": top_capability,
    "high_superficiality": high_superficiality,
    "top_inquiry": top_inquiry,
    "top_frames": top_frames,
    "top_ideas": top_ideas,
    "top_prototypes": top_prototypes,
    "top_tests": top_tests,
    "system_risks": system_risks,
    "ethical_risks": ethical_risks,
    "top_decisions": top_decisions,
    "top_learning": top_learning,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced design thinking diagnostics complete.")
print(f"Wrote: {TABLES / 'design_capability_scores.csv'}")
print(f"Wrote: {TABLES / 'stakeholder_inquiry_scores.csv'}")
print(f"Wrote: {TABLES / 'problem_reframing_scores.csv'}")
print(f"Wrote: {TABLES / 'idea_portfolio_scores.csv'}")
print(f"Wrote: {TABLES / 'prototype_learning_scores.csv'}")
print(f"Wrote: {TABLES / 'test_evidence_scores.csv'}")
print(f"Wrote: {TABLES / 'systems_design_review.csv'}")
print(f"Wrote: {TABLES / 'ethical_design_review.csv'}")
print(f"Wrote: {TABLES / 'decision_linkage_scores.csv'}")
print(f"Wrote: {TABLES / 'institutional_learning_scores.csv'}")
print(f"Wrote: {REPORTS / 'design_thinking_diagnostic_report.md'}")
