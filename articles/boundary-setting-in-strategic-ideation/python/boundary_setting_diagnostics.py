#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for boundary setting in strategic ideation.

This dependency-light workflow uses only the Python standard library.

It produces:
- boundary quality scores
- stakeholder boundary review
- causal boundary review
- temporal boundary review
- institutional boundary review
- evidence boundary review
- ethical boundary review
- boundary sensitivity scores
- boundary drift review
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


boundaries = read_csv(RAW / "boundary_frames.csv")
stakeholders = read_csv(RAW / "stakeholder_boundaries.csv")
causes = read_csv(RAW / "causal_boundaries.csv")
temporal = read_csv(RAW / "temporal_boundaries.csv")
institutions = read_csv(RAW / "institutional_boundaries.csv")
evidence = read_csv(RAW / "evidence_boundaries.csv")
ethics = read_csv(RAW / "ethical_boundaries.csv")
options = read_csv(RAW / "options.csv")
drift = read_csv(RAW / "boundary_drift.csv")
triggers = read_csv(RAW / "revision_triggers.csv")

boundary_names = {row["boundary_id"]: row["boundary_name"] for row in boundaries}

# ---------------------------------------------------------------------
# 1. Boundary quality scoring
# ---------------------------------------------------------------------

boundary_rows: list[dict[str, object]] = []

for row in boundaries:
    boundary_quality = (
        0.12 * f(row, "problem_clarity")
        + 0.13 * f(row, "system_context")
        + 0.14 * f(row, "stakeholder_inclusion")
        + 0.14 * f(row, "causal_adequacy")
        + 0.12 * f(row, "temporal_adequacy")
        + 0.11 * f(row, "institutional_responsibility")
        + 0.11 * f(row, "evidence_diversity")
        + 0.10 * f(row, "ethical_review")
        + 0.09 * f(row, "revision_readiness")
        + 0.04 * f(row, "actionability")
    )

    boundary_risk = (
        0.12 * (1 - f(row, "problem_clarity"))
        + 0.13 * (1 - f(row, "system_context"))
        + 0.14 * (1 - f(row, "stakeholder_inclusion"))
        + 0.14 * (1 - f(row, "causal_adequacy"))
        + 0.12 * (1 - f(row, "temporal_adequacy"))
        + 0.11 * (1 - f(row, "institutional_responsibility"))
        + 0.11 * (1 - f(row, "evidence_diversity"))
        + 0.10 * (1 - f(row, "ethical_review"))
        + 0.09 * (1 - f(row, "revision_readiness"))
    )

    if boundary_quality >= 0.78:
        diagnosis = "strong_boundary_design"
    elif f(row, "stakeholder_inclusion") < 0.40:
        diagnosis = "stakeholder_exclusion_risk"
    elif f(row, "temporal_adequacy") < 0.40:
        diagnosis = "temporal_boundary_risk"
    elif f(row, "causal_adequacy") < 0.45:
        diagnosis = "causal_boundary_risk"
    elif f(row, "evidence_diversity") < 0.40:
        diagnosis = "evidence_boundary_risk"
    elif boundary_quality >= 0.62:
        diagnosis = "usable_with_boundary_review"
    else:
        diagnosis = "boundary_revision_required"

    boundary_rows.append(
        {
            "boundary_id": row["boundary_id"],
            "boundary_name": row["boundary_name"],
            "frame_type": row["frame_type"],
            "domain": row["domain"],
            "boundary_quality_score": round(boundary_quality, 4),
            "boundary_risk_score": round(boundary_risk, 4),
            "diagnosis": diagnosis,
            "problem_clarity": row["problem_clarity"],
            "system_context": row["system_context"],
            "stakeholder_inclusion": row["stakeholder_inclusion"],
            "causal_adequacy": row["causal_adequacy"],
            "temporal_adequacy": row["temporal_adequacy"],
            "institutional_responsibility": row["institutional_responsibility"],
            "evidence_diversity": row["evidence_diversity"],
            "ethical_review": row["ethical_review"],
            "revision_readiness": row["revision_readiness"],
            "actionability": row["actionability"],
            "description": row["description"],
        }
    )

boundary_rows.sort(key=lambda item: item["boundary_quality_score"], reverse=True)

boundary_fields = [
    "boundary_id",
    "boundary_name",
    "frame_type",
    "domain",
    "boundary_quality_score",
    "boundary_risk_score",
    "diagnosis",
    "problem_clarity",
    "system_context",
    "stakeholder_inclusion",
    "causal_adequacy",
    "temporal_adequacy",
    "institutional_responsibility",
    "evidence_diversity",
    "ethical_review",
    "revision_readiness",
    "actionability",
    "description",
]

write_csv(TABLES / "boundary_quality_scores.csv", boundary_rows, boundary_fields)
write_csv(PROCESSED / "boundary_quality_scores.csv", boundary_rows, boundary_fields)

# ---------------------------------------------------------------------
# 2. Stakeholder boundary review
# ---------------------------------------------------------------------

stakeholder_rows: list[dict[str, object]] = []

for row in stakeholders:
    exclusion_risk = (
        0.18 * f(row, "affectedness")
        + 0.15 * f(row, "knowledge_value")
        + 0.15 * f(row, "burden_risk")
        + 0.14 * f(row, "trust_sensitivity")
        + 0.12 * f(row, "implementation_role")
        - 0.15 * f(row, "inclusion_quality")
        - 0.11 * f(row, "representation_quality")
    )

    if exclusion_risk >= 0.45:
        action = "increase_stakeholder_inclusion"
    elif f(row, "representation_quality") < 0.45:
        action = "improve_representation_quality"
    elif f(row, "burden_risk") >= 0.70:
        action = "review_hidden_burden"
    else:
        action = "maintain_stakeholder_review"

    stakeholder_rows.append(
        {
            "stakeholder_id": row["stakeholder_id"],
            "boundary_id": row["boundary_id"],
            "boundary_name": boundary_names.get(row["boundary_id"], row["boundary_id"]),
            "stakeholder_group": row["stakeholder_group"],
            "role_type": row["role_type"],
            "stakeholder_exclusion_risk": round(exclusion_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "inclusion_quality": row["inclusion_quality"],
            "affectedness": row["affectedness"],
            "decision_power": row["decision_power"],
            "implementation_role": row["implementation_role"],
            "knowledge_value": row["knowledge_value"],
            "burden_risk": row["burden_risk"],
            "trust_sensitivity": row["trust_sensitivity"],
            "representation_quality": row["representation_quality"],
        }
    )

stakeholder_rows.sort(key=lambda item: item["stakeholder_exclusion_risk"], reverse=True)

write_csv(
    TABLES / "stakeholder_boundary_review.csv",
    stakeholder_rows,
    [
        "stakeholder_id",
        "boundary_id",
        "boundary_name",
        "stakeholder_group",
        "role_type",
        "stakeholder_exclusion_risk",
        "recommended_action",
        "source_review_action",
        "inclusion_quality",
        "affectedness",
        "decision_power",
        "implementation_role",
        "knowledge_value",
        "burden_risk",
        "trust_sensitivity",
        "representation_quality",
    ],
)

# ---------------------------------------------------------------------
# 3. Causal boundary review
# ---------------------------------------------------------------------

causal_rows: list[dict[str, object]] = []

for row in causes:
    causal_quality = (
        0.13 * f(row, "causal_plausibility")
        + 0.12 * f(row, "evidence_strength")
        + 0.16 * f(row, "structural_depth")
        + 0.11 * f(row, "actor_adaptation_considered")
        + 0.14 * f(row, "feedback_considered")
        + 0.13 * f(row, "incentive_considered")
        + 0.10 * f(row, "historical_context_considered")
        + 0.11 * f(row, "implementation_relevance")
    )

    if causal_quality >= 0.72:
        action = "strong_causal_frame"
    elif f(row, "structural_depth") < 0.40:
        action = "compare_with_structural_causal_frame"
    elif f(row, "feedback_considered") < 0.45:
        action = "add_feedback_review"
    elif f(row, "incentive_considered") < 0.45:
        action = "add_incentive_review"
    else:
        action = "usable_with_causal_review"

    causal_rows.append(
        {
            "cause_id": row["cause_id"],
            "boundary_id": row["boundary_id"],
            "boundary_name": boundary_names.get(row["boundary_id"], row["boundary_id"]),
            "causal_frame": row["causal_frame"],
            "causal_level": row["causal_level"],
            "causal_quality_score": round(causal_quality, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "causal_plausibility": row["causal_plausibility"],
            "evidence_strength": row["evidence_strength"],
            "structural_depth": row["structural_depth"],
            "actor_adaptation_considered": row["actor_adaptation_considered"],
            "feedback_considered": row["feedback_considered"],
            "incentive_considered": row["incentive_considered"],
            "historical_context_considered": row["historical_context_considered"],
            "implementation_relevance": row["implementation_relevance"],
        }
    )

causal_rows.sort(key=lambda item: item["causal_quality_score"], reverse=True)

write_csv(
    TABLES / "causal_boundary_review.csv",
    causal_rows,
    [
        "cause_id",
        "boundary_id",
        "boundary_name",
        "causal_frame",
        "causal_level",
        "causal_quality_score",
        "recommended_action",
        "source_review_action",
        "causal_plausibility",
        "evidence_strength",
        "structural_depth",
        "actor_adaptation_considered",
        "feedback_considered",
        "incentive_considered",
        "historical_context_considered",
        "implementation_relevance",
    ],
)

# ---------------------------------------------------------------------
# 4. Temporal boundary review
# ---------------------------------------------------------------------

temporal_rows: list[dict[str, object]] = []

for row in temporal:
    temporal_quality = (
        0.10 * f(row, "immediate_signal_quality")
        + 0.12 * f(row, "short_term_signal_quality")
        + 0.15 * f(row, "medium_term_signal_quality")
        + 0.16 * f(row, "long_term_signal_quality")
        - 0.13 * f(row, "delayed_effect_risk")
        + 0.14 * f(row, "resilience_relevance")
        + 0.10 * f(row, "ownership_continuity")
        + 0.10 * f(row, "revision_cadence_quality")
    )

    compression_risk = (
        0.28 * f(row, "delayed_effect_risk")
        + 0.22 * (1 - f(row, "medium_term_signal_quality"))
        + 0.24 * (1 - f(row, "long_term_signal_quality"))
        + 0.14 * (1 - f(row, "ownership_continuity"))
        + 0.12 * (1 - f(row, "revision_cadence_quality"))
    )

    if compression_risk >= 0.55:
        action = "extend_temporal_boundary"
    elif temporal_quality >= 0.60:
        action = "temporal_boundary_usable"
    else:
        action = "add_delayed_effect_review"

    temporal_rows.append(
        {
            "time_id": row["time_id"],
            "boundary_id": row["boundary_id"],
            "boundary_name": boundary_names.get(row["boundary_id"], row["boundary_id"]),
            "time_horizon": row["time_horizon"],
            "review_stage": row["review_stage"],
            "temporal_quality_score": round(temporal_quality, 4),
            "temporal_compression_risk": round(compression_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "immediate_signal_quality": row["immediate_signal_quality"],
            "short_term_signal_quality": row["short_term_signal_quality"],
            "medium_term_signal_quality": row["medium_term_signal_quality"],
            "long_term_signal_quality": row["long_term_signal_quality"],
            "delayed_effect_risk": row["delayed_effect_risk"],
            "resilience_relevance": row["resilience_relevance"],
            "ownership_continuity": row["ownership_continuity"],
            "revision_cadence_quality": row["revision_cadence_quality"],
        }
    )

temporal_rows.sort(key=lambda item: item["temporal_compression_risk"], reverse=True)

write_csv(
    TABLES / "temporal_boundary_review.csv",
    temporal_rows,
    [
        "time_id",
        "boundary_id",
        "boundary_name",
        "time_horizon",
        "review_stage",
        "temporal_quality_score",
        "temporal_compression_risk",
        "recommended_action",
        "source_review_action",
        "immediate_signal_quality",
        "short_term_signal_quality",
        "medium_term_signal_quality",
        "long_term_signal_quality",
        "delayed_effect_risk",
        "resilience_relevance",
        "ownership_continuity",
        "revision_cadence_quality",
    ],
)

# ---------------------------------------------------------------------
# 5. Institutional boundary review
# ---------------------------------------------------------------------

institution_rows: list[dict[str, object]] = []

for row in institutions:
    responsibility_quality = (
        0.12 * f(row, "authority_clarity")
        + 0.12 * f(row, "influence_capacity")
        + 0.15 * f(row, "consequence_visibility")
        + 0.14 * f(row, "accountability_clarity")
        + 0.13 * f(row, "cross_boundary_coordination")
        - 0.13 * f(row, "externality_risk")
        + 0.10 * f(row, "escalation_path_quality")
        + 0.11 * f(row, "learning_flow_quality")
    )

    authority_consequence_gap = max(0.0, f(row, "authority_clarity") - f(row, "consequence_visibility"))

    if authority_consequence_gap >= 0.30:
        action = "map_consequence_boundary"
    elif f(row, "cross_boundary_coordination") < 0.45:
        action = "build_cross_boundary_coordination"
    elif f(row, "externality_risk") >= 0.65:
        action = "review_externalized_consequences"
    else:
        action = "institutional_boundary_usable"

    institution_rows.append(
        {
            "institution_id": row["institution_id"],
            "boundary_id": row["boundary_id"],
            "boundary_name": boundary_names.get(row["boundary_id"], row["boundary_id"]),
            "institutional_frame": row["institutional_frame"],
            "responsibility_quality_score": round(responsibility_quality, 4),
            "authority_consequence_gap": round(authority_consequence_gap, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "authority_clarity": row["authority_clarity"],
            "influence_capacity": row["influence_capacity"],
            "consequence_visibility": row["consequence_visibility"],
            "accountability_clarity": row["accountability_clarity"],
            "cross_boundary_coordination": row["cross_boundary_coordination"],
            "externality_risk": row["externality_risk"],
            "escalation_path_quality": row["escalation_path_quality"],
            "learning_flow_quality": row["learning_flow_quality"],
        }
    )

institution_rows.sort(key=lambda item: item["authority_consequence_gap"], reverse=True)

write_csv(
    TABLES / "institutional_boundary_review.csv",
    institution_rows,
    [
        "institution_id",
        "boundary_id",
        "boundary_name",
        "institutional_frame",
        "responsibility_quality_score",
        "authority_consequence_gap",
        "recommended_action",
        "source_review_action",
        "authority_clarity",
        "influence_capacity",
        "consequence_visibility",
        "accountability_clarity",
        "cross_boundary_coordination",
        "externality_risk",
        "escalation_path_quality",
        "learning_flow_quality",
    ],
)

# ---------------------------------------------------------------------
# 6. Evidence boundary review
# ---------------------------------------------------------------------

evidence_rows: list[dict[str, object]] = []

for row in evidence:
    evidence_diversity_score = (
        0.12 * f(row, "quantitative_quality")
        + 0.13 * f(row, "qualitative_quality")
        + 0.14 * f(row, "stakeholder_testimony_quality")
        + 0.12 * f(row, "prototype_evidence_quality")
        + 0.12 * f(row, "scenario_evidence_quality")
        + 0.11 * f(row, "expert_judgment_quality")
        + 0.13 * f(row, "ethical_reasoning_quality")
        + 0.13 * f(row, "interpretation_discipline")
        - 0.12 * f(row, "blind_spot_risk")
    )

    if f(row, "blind_spot_risk") >= 0.70:
        action = "expand_evidence_boundary"
    elif f(row, "qualitative_quality") < 0.40 or f(row, "stakeholder_testimony_quality") < 0.40:
        action = "add_lived_experience_and_qualitative_review"
    elif evidence_diversity_score >= 0.60:
        action = "evidence_boundary_strong"
    else:
        action = "strengthen_evidence_interpretation"

    evidence_rows.append(
        {
            "evidence_id": row["evidence_id"],
            "boundary_id": row["boundary_id"],
            "boundary_name": boundary_names.get(row["boundary_id"], row["boundary_id"]),
            "evidence_frame": row["evidence_frame"],
            "evidence_diversity_score": round(evidence_diversity_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "quantitative_quality": row["quantitative_quality"],
            "qualitative_quality": row["qualitative_quality"],
            "stakeholder_testimony_quality": row["stakeholder_testimony_quality"],
            "prototype_evidence_quality": row["prototype_evidence_quality"],
            "scenario_evidence_quality": row["scenario_evidence_quality"],
            "expert_judgment_quality": row["expert_judgment_quality"],
            "ethical_reasoning_quality": row["ethical_reasoning_quality"],
            "interpretation_discipline": row["interpretation_discipline"],
            "blind_spot_risk": row["blind_spot_risk"],
        }
    )

evidence_rows.sort(key=lambda item: item["evidence_diversity_score"])

write_csv(
    TABLES / "evidence_boundary_review.csv",
    evidence_rows,
    [
        "evidence_id",
        "boundary_id",
        "boundary_name",
        "evidence_frame",
        "evidence_diversity_score",
        "recommended_action",
        "source_review_action",
        "quantitative_quality",
        "qualitative_quality",
        "stakeholder_testimony_quality",
        "prototype_evidence_quality",
        "scenario_evidence_quality",
        "expert_judgment_quality",
        "ethical_reasoning_quality",
        "interpretation_discipline",
        "blind_spot_risk",
    ],
)

# ---------------------------------------------------------------------
# 7. Ethical boundary review
# ---------------------------------------------------------------------

ethical_rows: list[dict[str, object]] = []

for row in ethics:
    ethical_risk = (
        0.14 * f(row, "exclusion_risk")
        + 0.15 * f(row, "burden_shift_risk")
        - 0.12 * f(row, "harm_visibility")
        + 0.13 * f(row, "future_consequence_risk")
        + 0.13 * f(row, "power_asymmetry")
        - 0.11 * f(row, "redress_path_quality")
        - 0.11 * f(row, "participation_quality")
        - 0.11 * f(row, "accountability_quality")
    )

    if ethical_risk >= 0.30:
        action = "ethical_boundary_review_required"
    elif f(row, "redress_path_quality") < 0.45:
        action = "build_redress_path"
    elif f(row, "participation_quality") < 0.45:
        action = "increase_participation"
    else:
        action = "ethical_boundary_usable"

    ethical_rows.append(
        {
            "ethics_id": row["ethics_id"],
            "boundary_id": row["boundary_id"],
            "boundary_name": boundary_names.get(row["boundary_id"], row["boundary_id"]),
            "ethical_issue": row["ethical_issue"],
            "ethical_risk_score": round(ethical_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "exclusion_risk": row["exclusion_risk"],
            "burden_shift_risk": row["burden_shift_risk"],
            "harm_visibility": row["harm_visibility"],
            "future_consequence_risk": row["future_consequence_risk"],
            "power_asymmetry": row["power_asymmetry"],
            "redress_path_quality": row["redress_path_quality"],
            "participation_quality": row["participation_quality"],
            "accountability_quality": row["accountability_quality"],
        }
    )

ethical_rows.sort(key=lambda item: item["ethical_risk_score"], reverse=True)

write_csv(
    TABLES / "ethical_boundary_review.csv",
    ethical_rows,
    [
        "ethics_id",
        "boundary_id",
        "boundary_name",
        "ethical_issue",
        "ethical_risk_score",
        "recommended_action",
        "source_review_action",
        "exclusion_risk",
        "burden_shift_risk",
        "harm_visibility",
        "future_consequence_risk",
        "power_asymmetry",
        "redress_path_quality",
        "participation_quality",
        "accountability_quality",
    ],
)

# ---------------------------------------------------------------------
# 8. Boundary-sensitive option evaluation
# ---------------------------------------------------------------------

boundary_weight_sets = {
    "internal_boundary": {
        "internal_efficiency": 0.38,
        "stakeholder_value": 0.10,
        "system_leverage": 0.10,
        "long_term_resilience": 0.10,
        "ethical_responsibility": 0.08,
        "implementation_feasibility": 0.16,
        "learning_value": 0.04,
        "strategic_reversibility": 0.04,
    },
    "stakeholder_boundary": {
        "internal_efficiency": 0.08,
        "stakeholder_value": 0.34,
        "system_leverage": 0.12,
        "long_term_resilience": 0.10,
        "ethical_responsibility": 0.20,
        "implementation_feasibility": 0.08,
        "learning_value": 0.05,
        "strategic_reversibility": 0.03,
    },
    "system_boundary": {
        "internal_efficiency": 0.08,
        "stakeholder_value": 0.12,
        "system_leverage": 0.34,
        "long_term_resilience": 0.18,
        "ethical_responsibility": 0.10,
        "implementation_feasibility": 0.06,
        "learning_value": 0.08,
        "strategic_reversibility": 0.04,
    },
    "long_term_boundary": {
        "internal_efficiency": 0.06,
        "stakeholder_value": 0.12,
        "system_leverage": 0.20,
        "long_term_resilience": 0.32,
        "ethical_responsibility": 0.14,
        "implementation_feasibility": 0.05,
        "learning_value": 0.08,
        "strategic_reversibility": 0.03,
    },
    "ethical_boundary": {
        "internal_efficiency": 0.06,
        "stakeholder_value": 0.22,
        "system_leverage": 0.12,
        "long_term_resilience": 0.16,
        "ethical_responsibility": 0.28,
        "implementation_feasibility": 0.05,
        "learning_value": 0.07,
        "strategic_reversibility": 0.04,
    },
}

option_rows: list[dict[str, object]] = []

for row in options:
    scores: dict[str, float] = {}
    for boundary, weights in boundary_weight_sets.items():
        scores[boundary] = sum(f(row, criterion) * weight for criterion, weight in weights.items())

    mean_score = sum(scores.values()) / len(scores)
    boundary_sensitivity = max(scores.values()) - min(scores.values())

    if boundary_sensitivity >= 0.18:
        diagnosis = "high_boundary_sensitivity"
    elif mean_score >= 0.72:
        diagnosis = "strong_across_boundaries"
    elif scores["internal_boundary"] > mean_score + 0.10:
        diagnosis = "internally_attractive_boundary_dependent"
    else:
        diagnosis = "moderate_boundary_stability"

    option_rows.append(
        {
            "option_id": row["option_id"],
            "option_name": row["option_name"],
            "internal_boundary_score": round(scores["internal_boundary"], 4),
            "stakeholder_boundary_score": round(scores["stakeholder_boundary"], 4),
            "system_boundary_score": round(scores["system_boundary"], 4),
            "long_term_boundary_score": round(scores["long_term_boundary"], 4),
            "ethical_boundary_score": round(scores["ethical_boundary"], 4),
            "mean_score": round(mean_score, 4),
            "boundary_sensitivity": round(boundary_sensitivity, 4),
            "diagnosis": diagnosis,
            "internal_efficiency": row["internal_efficiency"],
            "stakeholder_value": row["stakeholder_value"],
            "system_leverage": row["system_leverage"],
            "long_term_resilience": row["long_term_resilience"],
            "ethical_responsibility": row["ethical_responsibility"],
            "implementation_feasibility": row["implementation_feasibility"],
            "learning_value": row["learning_value"],
            "strategic_reversibility": row["strategic_reversibility"],
        }
    )

option_rows.sort(key=lambda item: item["mean_score"], reverse=True)

write_csv(
    TABLES / "boundary_sensitivity_scores.csv",
    option_rows,
    [
        "option_id",
        "option_name",
        "internal_boundary_score",
        "stakeholder_boundary_score",
        "system_boundary_score",
        "long_term_boundary_score",
        "ethical_boundary_score",
        "mean_score",
        "boundary_sensitivity",
        "diagnosis",
        "internal_efficiency",
        "stakeholder_value",
        "system_leverage",
        "long_term_resilience",
        "ethical_responsibility",
        "implementation_feasibility",
        "learning_value",
        "strategic_reversibility",
    ],
)

# ---------------------------------------------------------------------
# 9. Boundary drift review
# ---------------------------------------------------------------------

drift_rows: list[dict[str, object]] = []

for row in drift:
    drift_risk = (
        0.12 * f(row, "scope_change")
        + 0.12 * f(row, "stakeholder_change")
        + 0.14 * f(row, "metric_change")
        + 0.13 * f(row, "responsibility_change")
        + 0.13 * f(row, "evidence_change")
        - 0.14 * f(row, "explicitness")
        - 0.10 * f(row, "evidence_basis")
        + 0.12 * f(row, "coherence_risk")
    )

    if drift_risk >= 0.45:
        action = "boundary_drift_review_required"
    elif f(row, "explicitness") < 0.45:
        action = "document_boundary_change"
    elif f(row, "evidence_basis") < 0.45:
        action = "justify_boundary_change_with_evidence"
    else:
        action = "acceptable_boundary_revision"

    drift_rows.append(
        {
            "drift_id": row["drift_id"],
            "boundary_id": row["boundary_id"],
            "boundary_name": boundary_names.get(row["boundary_id"], row["boundary_id"]),
            "drift_type": row["drift_type"],
            "original_boundary": row["original_boundary"],
            "new_boundary": row["new_boundary"],
            "boundary_drift_risk": round(drift_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "scope_change": row["scope_change"],
            "stakeholder_change": row["stakeholder_change"],
            "metric_change": row["metric_change"],
            "responsibility_change": row["responsibility_change"],
            "evidence_change": row["evidence_change"],
            "explicitness": row["explicitness"],
            "evidence_basis": row["evidence_basis"],
            "coherence_risk": row["coherence_risk"],
        }
    )

drift_rows.sort(key=lambda item: item["boundary_drift_risk"], reverse=True)

write_csv(
    TABLES / "boundary_drift_review.csv",
    drift_rows,
    [
        "drift_id",
        "boundary_id",
        "boundary_name",
        "drift_type",
        "original_boundary",
        "new_boundary",
        "boundary_drift_risk",
        "recommended_action",
        "source_review_action",
        "scope_change",
        "stakeholder_change",
        "metric_change",
        "responsibility_change",
        "evidence_change",
        "explicitness",
        "evidence_basis",
        "coherence_risk",
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
        + 0.15 * f(row, "decision_linkage")
        + 0.12 * f(row, "timeliness")
        + 0.12 * f(row, "stakeholder_visibility")
        + 0.13 * f(row, "governance_owner_clarity")
        + 0.18 * f(row, "response_options_quality")
    )

    if trigger_quality >= 0.72:
        action = "strong_revision_trigger"
    elif f(row, "decision_linkage") < 0.60:
        action = "connect_trigger_to_decision_rights"
    elif f(row, "threshold_clarity") < 0.60:
        action = "clarify_trigger_threshold"
    else:
        action = "usable_with_trigger_review"

    trigger_rows.append(
        {
            "trigger_id": row["trigger_id"],
            "boundary_id": row["boundary_id"],
            "boundary_name": boundary_names.get(row["boundary_id"], row["boundary_id"]),
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
        "boundary_id",
        "boundary_name",
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

top_boundaries = boundary_rows[:5]
highest_boundary_risk = sorted(boundary_rows, key=lambda item: item["boundary_risk_score"], reverse=True)[:5]
highest_exclusion = stakeholder_rows[:5]
strongest_causes = causal_rows[:5]
temporal_risks = temporal_rows[:5]
institutional_gaps = institution_rows[:5]
weak_evidence = evidence_rows[:5]
ethical_risks = ethical_rows[:5]
high_sensitivity = sorted(option_rows, key=lambda item: item["boundary_sensitivity"], reverse=True)[:5]
highest_drift = drift_rows[:5]
top_triggers = trigger_rows[:5]

report: list[str] = []

report.append("# Boundary Setting in Strategic Ideation Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic evaluates boundary quality, stakeholder inclusion, causal adequacy, temporal scope, institutional responsibility, evidence diversity, "
    "ethical risk, boundary-sensitive option value, boundary drift, and revision-trigger quality. The purpose is to help strategists make problem frames "
    "explicit, contestable, ethically accountable, and revisable before ideas move into evaluation or implementation."
)

report.append("")
report.append("## Strongest boundary designs")
report.append("")
for item in top_boundaries:
    report.append(
        f"- **{item['boundary_id']} — {item['boundary_name']}** ({item['frame_type']}): "
        f"quality {item['boundary_quality_score']}; risk {item['boundary_risk_score']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest boundary-risk frames")
report.append("")
for item in highest_boundary_risk:
    report.append(
        f"- **{item['boundary_id']} — {item['boundary_name']}**: risk {item['boundary_risk_score']}; "
        f"diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Stakeholder exclusion risks")
report.append("")
for item in highest_exclusion:
    report.append(
        f"- **{item['stakeholder_id']} — {item['stakeholder_group']}** under **{item['boundary_name']}**: "
        f"exclusion risk {item['stakeholder_exclusion_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strong causal frames")
report.append("")
for item in strongest_causes:
    report.append(
        f"- **{item['cause_id']} — {item['causal_frame']}** under **{item['boundary_name']}**: "
        f"causal quality {item['causal_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Temporal compression risks")
report.append("")
for item in temporal_risks:
    report.append(
        f"- **{item['time_id']} — {item['time_horizon']}** under **{item['boundary_name']}**: "
        f"compression risk {item['temporal_compression_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Institutional authority-consequence gaps")
report.append("")
for item in institutional_gaps:
    report.append(
        f"- **{item['institution_id']} — {item['institutional_frame']}** under **{item['boundary_name']}**: "
        f"authority-consequence gap {item['authority_consequence_gap']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Evidence boundaries needing expansion")
report.append("")
for item in weak_evidence:
    report.append(
        f"- **{item['evidence_id']} — {item['evidence_frame']}** under **{item['boundary_name']}**: "
        f"evidence score {item['evidence_diversity_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Ethical boundary risks")
report.append("")
for item in ethical_risks:
    report.append(
        f"- **{item['ethics_id']} — {item['ethical_issue']}** under **{item['boundary_name']}**: "
        f"ethical risk {item['ethical_risk_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Boundary-sensitive options")
report.append("")
for item in high_sensitivity:
    report.append(
        f"- **{item['option_id']} — {item['option_name']}**: mean score {item['mean_score']}; "
        f"boundary sensitivity {item['boundary_sensitivity']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Boundary drift risks")
report.append("")
for item in highest_drift:
    report.append(
        f"- **{item['drift_id']} — {item['drift_type']}** under **{item['boundary_name']}**: "
        f"drift risk {item['boundary_drift_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strong revision triggers")
report.append("")
for item in top_triggers:
    report.append(
        f"- **{item['trigger_id']} — {item['trigger_name']}** under **{item['boundary_name']}**: "
        f"trigger quality {item['trigger_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "Boundary setting is the discipline of deciding what the strategy is responsible for seeing. Strong boundary work separates problem scope from system context, "
    "includes affected stakeholders, compares causal frames, extends temporal horizons, distinguishes authority from consequence, broadens evidence, reviews ethical "
    "exclusions, tests option value under alternative frames, detects boundary drift, and records revision triggers in decision memory."
)

(REPORTS / "boundary_setting_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_boundaries": top_boundaries,
    "highest_boundary_risk": highest_boundary_risk,
    "highest_exclusion": highest_exclusion,
    "strongest_causes": strongest_causes,
    "temporal_risks": temporal_risks,
    "institutional_gaps": institutional_gaps,
    "weak_evidence": weak_evidence,
    "ethical_risks": ethical_risks,
    "high_sensitivity": high_sensitivity,
    "highest_drift": highest_drift,
    "top_triggers": top_triggers,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced boundary-setting diagnostics complete.")
print(f"Wrote: {TABLES / 'boundary_quality_scores.csv'}")
print(f"Wrote: {TABLES / 'stakeholder_boundary_review.csv'}")
print(f"Wrote: {TABLES / 'causal_boundary_review.csv'}")
print(f"Wrote: {TABLES / 'temporal_boundary_review.csv'}")
print(f"Wrote: {TABLES / 'institutional_boundary_review.csv'}")
print(f"Wrote: {TABLES / 'evidence_boundary_review.csv'}")
print(f"Wrote: {TABLES / 'ethical_boundary_review.csv'}")
print(f"Wrote: {TABLES / 'boundary_sensitivity_scores.csv'}")
print(f"Wrote: {TABLES / 'boundary_drift_review.csv'}")
print(f"Wrote: {TABLES / 'revision_trigger_review.csv'}")
print(f"Wrote: {REPORTS / 'boundary_setting_diagnostic_report.md'}")
