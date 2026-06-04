#!/usr/bin/env python3
"""
Advanced strategist-facing conceptual clarity diagnostics.

This dependency-light workflow uses only the Python standard library.

It produces:
- conceptual clarity scores
- interpretation variance and false-consensus risk
- boundary clarity review
- distinction map scores
- metric validity and proxy-risk review
- conceptual drift register
- concept governance actions
- a markdown strategist diagnostic report

The workflow is designed for strategy teams that need to turn abstract
strategic language into decision-ready concepts.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev

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


concepts = read_csv(RAW / "concept_inventory.csv")
interpretations = read_csv(RAW / "interpretation_survey.csv")
boundaries = read_csv(RAW / "concept_boundaries.csv")
distinctions = read_csv(RAW / "distinction_map.csv")
metrics = read_csv(RAW / "metric_register.csv")
implications = read_csv(RAW / "decision_implications.csv")
drift_events = read_csv(RAW / "drift_events.csv")
governance = read_csv(RAW / "governance_reviews.csv")

# ---------------------------------------------------------------------
# 1. Conceptual clarity scores
# ---------------------------------------------------------------------

clarity_rows: list[dict[str, object]] = []

for row in concepts:
    clarity_score = (
        0.17 * f(row, "definition_clarity")
        + 0.14 * f(row, "boundary_clarity")
        + 0.14 * f(row, "distinction_quality")
        + 0.13 * f(row, "operational_implication")
        + 0.15 * f(row, "measurement_validity")
        + 0.10 * f(row, "revision_capacity")
        + 0.07 * f(row, "stakeholder_visibility")
        + 0.06 * f(row, "ethical_visibility")
        + 0.04 * f(row, "governance_maturity")
    )

    ambiguity_risk = 1 - clarity_score

    if f(row, "definition_clarity") < 0.45 and f(row, "measurement_validity") < 0.45:
        diagnosis = "high_false_precision_risk"
    elif f(row, "boundary_clarity") < 0.40:
        diagnosis = "concept_expansion_or_boundary_risk"
    elif f(row, "revision_capacity") < 0.35:
        diagnosis = "conceptual_drift_risk"
    elif f(row, "ethical_visibility") < 0.45 or f(row, "stakeholder_visibility") < 0.45:
        diagnosis = "ethical_or_stakeholder_visibility_gap"
    elif clarity_score >= 0.64:
        diagnosis = "usable_for_strategy"
    else:
        diagnosis = "requires_clarity_review"

    clarity_rows.append(
        {
            "concept_id": row["concept_id"],
            "concept_name": row["concept_name"],
            "domain": row["domain"],
            "conceptual_clarity_score": round(clarity_score, 4),
            "ambiguity_risk": round(ambiguity_risk, 4),
            "diagnosis": diagnosis,
            "definition_clarity": row["definition_clarity"],
            "boundary_clarity": row["boundary_clarity"],
            "distinction_quality": row["distinction_quality"],
            "operational_implication": row["operational_implication"],
            "measurement_validity": row["measurement_validity"],
            "revision_capacity": row["revision_capacity"],
            "stakeholder_visibility": row["stakeholder_visibility"],
            "ethical_visibility": row["ethical_visibility"],
            "governance_maturity": row["governance_maturity"],
        }
    )

clarity_rows.sort(key=lambda item: item["conceptual_clarity_score"], reverse=True)

write_csv(
    TABLES / "conceptual_clarity_scores.csv",
    clarity_rows,
    [
        "concept_id",
        "concept_name",
        "domain",
        "conceptual_clarity_score",
        "ambiguity_risk",
        "diagnosis",
        "definition_clarity",
        "boundary_clarity",
        "distinction_quality",
        "operational_implication",
        "measurement_validity",
        "revision_capacity",
        "stakeholder_visibility",
        "ethical_visibility",
        "governance_maturity",
    ],
)

write_csv(
    PROCESSED / "conceptual_clarity_scores.csv",
    clarity_rows,
    [
        "concept_id",
        "concept_name",
        "domain",
        "conceptual_clarity_score",
        "ambiguity_risk",
        "diagnosis",
        "definition_clarity",
        "boundary_clarity",
        "distinction_quality",
        "operational_implication",
        "measurement_validity",
        "revision_capacity",
        "stakeholder_visibility",
        "ethical_visibility",
        "governance_maturity",
    ],
)

# ---------------------------------------------------------------------
# 2. Interpretation variance and false consensus
# ---------------------------------------------------------------------

interpretation_rows: list[dict[str, object]] = []
by_concept: dict[str, list[dict[str, str]]] = defaultdict(list)

for row in interpretations:
    by_concept[row["concept_id"]].append(row)

concept_names = {row["concept_id"]: row["concept_name"] for row in concepts}

for concept_id, rows in by_concept.items():
    interpretation_scores = [f(row, "interpretation_alignment") for row in rows]
    decision_scores = [f(row, "decision_implication_alignment") for row in rows]
    contestation = [f(row, "contestation_level") for row in rows]

    interpretation_variance = pstdev(interpretation_scores) if len(interpretation_scores) > 1 else 0.0
    decision_variance = pstdev(decision_scores) if len(decision_scores) > 1 else 0.0
    mean_alignment = mean(interpretation_scores)
    mean_decision_alignment = mean(decision_scores)
    mean_contestation = mean(contestation)

    false_consensus_risk = (
        0.30 * (1 - mean_alignment)
        + 0.25 * (1 - mean_decision_alignment)
        + 0.25 * mean_contestation
        + 0.20 * min(1.0, interpretation_variance * 3)
    )

    if false_consensus_risk >= 0.62:
        flag = "high_false_consensus_risk"
    elif false_consensus_risk >= 0.48:
        flag = "interpretation_review_needed"
    else:
        flag = "interpretation_alignment_manageable"

    interpretation_rows.append(
        {
            "concept_id": concept_id,
            "concept_name": concept_names.get(concept_id, concept_id),
            "actor_group_count": len(rows),
            "mean_interpretation_alignment": round(mean_alignment, 4),
            "mean_decision_implication_alignment": round(mean_decision_alignment, 4),
            "interpretation_variance": round(interpretation_variance, 4),
            "decision_variance": round(decision_variance, 4),
            "mean_contestation": round(mean_contestation, 4),
            "false_consensus_risk": round(false_consensus_risk, 4),
            "flag": flag,
        }
    )

interpretation_rows.sort(key=lambda item: item["false_consensus_risk"], reverse=True)

write_csv(
    TABLES / "interpretation_variance_register.csv",
    interpretation_rows,
    [
        "concept_id",
        "concept_name",
        "actor_group_count",
        "mean_interpretation_alignment",
        "mean_decision_implication_alignment",
        "interpretation_variance",
        "decision_variance",
        "mean_contestation",
        "false_consensus_risk",
        "flag",
    ],
)

# ---------------------------------------------------------------------
# 3. Boundary review
# ---------------------------------------------------------------------

boundary_rows: list[dict[str, object]] = []

for row in boundaries:
    boundary_score = (
        0.32 * f(row, "inclusion_clarity")
        + 0.32 * f(row, "exclusion_clarity")
        + 0.18 * f(row, "strategic_importance")
        - 0.18 * f(row, "boundary_contestation")
    )

    if f(row, "boundary_contestation") >= 0.58 and f(row, "exclusion_clarity") < 0.40:
        action = "urgent_boundary_definition"
    elif boundary_score < 0.45:
        action = "boundary_review_needed"
    else:
        action = "boundary_manageable"

    boundary_rows.append(
        {
            "boundary_id": row["boundary_id"],
            "concept_id": row["concept_id"],
            "concept_name": concept_names.get(row["concept_id"], row["concept_id"]),
            "boundary_score": round(boundary_score, 4),
            "recommended_action": action,
            "review_priority": row["review_priority"],
            "inclusion_clarity": row["inclusion_clarity"],
            "exclusion_clarity": row["exclusion_clarity"],
            "strategic_importance": row["strategic_importance"],
            "boundary_contestation": row["boundary_contestation"],
            "boundary_rule": row["boundary_rule"],
        }
    )

boundary_rows.sort(key=lambda item: item["boundary_score"])

write_csv(
    TABLES / "boundary_clarity_review.csv",
    boundary_rows,
    [
        "boundary_id",
        "concept_id",
        "concept_name",
        "boundary_score",
        "recommended_action",
        "review_priority",
        "inclusion_clarity",
        "exclusion_clarity",
        "strategic_importance",
        "boundary_contestation",
        "boundary_rule",
    ],
)

# ---------------------------------------------------------------------
# 4. Distinction mapping
# ---------------------------------------------------------------------

distinction_rows: list[dict[str, object]] = []

for row in distinctions:
    distinction_risk = (
        0.52 * f(row, "confusion_risk")
        + 0.48 * (1 - f(row, "distinction_clarity"))
    )

    if distinction_risk >= 0.65:
        action = "urgent_distinction_clarification"
    elif distinction_risk >= 0.50:
        action = "distinction_review_needed"
    else:
        action = "distinction_manageable"

    distinction_rows.append(
        {
            "distinction_id": row["distinction_id"],
            "concept_id": row["concept_id"],
            "concept_name": concept_names.get(row["concept_id"], row["concept_id"]),
            "confused_with": row["confused_with"],
            "distinction_risk": round(distinction_risk, 4),
            "recommended_action": action,
            "distinction_clarity": row["distinction_clarity"],
            "confusion_risk": row["confusion_risk"],
            "distinction_statement": row["distinction_statement"],
            "decision_consequence": row["decision_consequence"],
        }
    )

distinction_rows.sort(key=lambda item: item["distinction_risk"], reverse=True)

write_csv(
    TABLES / "distinction_map_scores.csv",
    distinction_rows,
    [
        "distinction_id",
        "concept_id",
        "concept_name",
        "confused_with",
        "distinction_risk",
        "recommended_action",
        "distinction_clarity",
        "confusion_risk",
        "distinction_statement",
        "decision_consequence",
    ],
)

# ---------------------------------------------------------------------
# 5. Metric validity and proxy-risk review
# ---------------------------------------------------------------------

metric_rows: list[dict[str, object]] = []

for row in metrics:
    metric_validity_score = (
        0.34 * f(row, "proxy_strength")
        - 0.22 * f(row, "proxy_risk")
        - 0.18 * f(row, "incentive_distortion_risk")
        - 0.12 * f(row, "qualitative_gap")
        + 0.26 * f(row, "validity_confidence")
    )

    proxy_failure_risk = (
        0.28 * f(row, "proxy_risk")
        + 0.26 * f(row, "incentive_distortion_risk")
        + 0.22 * f(row, "qualitative_gap")
        + 0.24 * (1 - f(row, "validity_confidence"))
    )

    if proxy_failure_risk >= 0.68:
        action = "replace_or_supplement_metric"
    elif metric_validity_score < 0.36:
        action = "metric_validity_review"
    else:
        action = "metric_manageable_with_context"

    metric_rows.append(
        {
            "metric_id": row["metric_id"],
            "concept_id": row["concept_id"],
            "concept_name": concept_names.get(row["concept_id"], row["concept_id"]),
            "metric_name": row["metric_name"],
            "metric_type": row["metric_type"],
            "metric_validity_score": round(metric_validity_score, 4),
            "proxy_failure_risk": round(proxy_failure_risk, 4),
            "recommended_action": action,
            "proxy_strength": row["proxy_strength"],
            "proxy_risk": row["proxy_risk"],
            "incentive_distortion_risk": row["incentive_distortion_risk"],
            "qualitative_gap": row["qualitative_gap"],
            "validity_confidence": row["validity_confidence"],
        }
    )

metric_rows.sort(key=lambda item: item["proxy_failure_risk"], reverse=True)

write_csv(
    TABLES / "metric_validity_review.csv",
    metric_rows,
    [
        "metric_id",
        "concept_id",
        "concept_name",
        "metric_name",
        "metric_type",
        "metric_validity_score",
        "proxy_failure_risk",
        "recommended_action",
        "proxy_strength",
        "proxy_risk",
        "incentive_distortion_risk",
        "qualitative_gap",
        "validity_confidence",
    ],
)

# ---------------------------------------------------------------------
# 6. Decision implication strength
# ---------------------------------------------------------------------

implication_rows: list[dict[str, object]] = []

for row in implications:
    decision_power = (
        0.26 * f(row, "decision_relevance")
        + 0.20 * f(row, "resource_allocation_effect")
        + 0.18 * f(row, "role_clarity_effect")
        + 0.20 * f(row, "tradeoff_visibility")
        + 0.16 * f(row, "escalation_need")
    )

    if decision_power >= 0.78:
        action = "must_define_before_decision"
    elif decision_power >= 0.65:
        action = "define_during_strategy_review"
    else:
        action = "standard_concept_review"

    implication_rows.append(
        {
            "implication_id": row["implication_id"],
            "concept_id": row["concept_id"],
            "concept_name": concept_names.get(row["concept_id"], row["concept_id"]),
            "decision_context": row["decision_context"],
            "decision_power": round(decision_power, 4),
            "recommended_action": action,
            "decision_relevance": row["decision_relevance"],
            "resource_allocation_effect": row["resource_allocation_effect"],
            "role_clarity_effect": row["role_clarity_effect"],
            "tradeoff_visibility": row["tradeoff_visibility"],
            "escalation_need": row["escalation_need"],
        }
    )

implication_rows.sort(key=lambda item: item["decision_power"], reverse=True)

write_csv(
    TABLES / "decision_implication_scores.csv",
    implication_rows,
    [
        "implication_id",
        "concept_id",
        "concept_name",
        "decision_context",
        "decision_power",
        "recommended_action",
        "decision_relevance",
        "resource_allocation_effect",
        "role_clarity_effect",
        "tradeoff_visibility",
        "escalation_need",
    ],
)

# ---------------------------------------------------------------------
# 7. Conceptual drift register
# ---------------------------------------------------------------------

drift_rows: list[dict[str, object]] = []

for row in drift_events:
    drift_priority = (
        0.34 * f(row, "drift_severity")
        + 0.34 * f(row, "strategic_exposure")
        + 0.18 * f(row, "detection_confidence")
        + 0.14 * (1.0 if row["drift_type"] in ("proxy_substitution", "politicization", "messaging_dilution") else 0.65)
    )

    if drift_priority >= 0.78:
        urgency = "urgent_concept_recovery"
    elif drift_priority >= 0.62:
        urgency = "scheduled_concept_review"
    else:
        urgency = "monitor"

    drift_rows.append(
        {
            "drift_id": row["drift_id"],
            "concept_id": row["concept_id"],
            "concept_name": concept_names.get(row["concept_id"], row["concept_id"]),
            "drift_type": row["drift_type"],
            "drift_priority": round(drift_priority, 4),
            "urgency": urgency,
            "drift_severity": row["drift_severity"],
            "strategic_exposure": row["strategic_exposure"],
            "detection_confidence": row["detection_confidence"],
            "recommended_response": row["recommended_response"],
            "drift_description": row["drift_description"],
        }
    )

drift_rows.sort(key=lambda item: item["drift_priority"], reverse=True)

write_csv(
    TABLES / "conceptual_drift_register.csv",
    drift_rows,
    [
        "drift_id",
        "concept_id",
        "concept_name",
        "drift_type",
        "drift_priority",
        "urgency",
        "drift_severity",
        "strategic_exposure",
        "detection_confidence",
        "recommended_response",
        "drift_description",
    ],
)

# ---------------------------------------------------------------------
# 8. Concept governance actions
# ---------------------------------------------------------------------

governance_rows: list[dict[str, object]] = []

for row in governance:
    governance_strength = (
        0.18 * f(row, "definition_owner")
        + 0.16 * f(row, "metric_owner")
        + 0.20 * f(row, "revision_trigger_quality")
        + 0.18 * f(row, "documentation_quality")
        + 0.20 * f(row, "stakeholder_review_quality")
        - 0.14 * f(row, "governance_risk")
    )

    if governance_strength < 0.34:
        action = "establish_concept_governance"
    elif f(row, "revision_trigger_quality") < 0.45:
        action = "define_revision_triggers"
    elif f(row, "stakeholder_review_quality") < 0.45:
        action = "add_stakeholder_review"
    else:
        action = "governance_manageable"

    governance_rows.append(
        {
            "review_id": row["review_id"],
            "concept_id": row["concept_id"],
            "concept_name": concept_names.get(row["concept_id"], row["concept_id"]),
            "owner_group": row["owner_group"],
            "review_cadence": row["review_cadence"],
            "governance_strength": round(governance_strength, 4),
            "recommended_action": action,
            "definition_owner": row["definition_owner"],
            "metric_owner": row["metric_owner"],
            "revision_trigger_quality": row["revision_trigger_quality"],
            "documentation_quality": row["documentation_quality"],
            "stakeholder_review_quality": row["stakeholder_review_quality"],
            "governance_risk": row["governance_risk"],
        }
    )

governance_rows.sort(key=lambda item: item["governance_strength"])

write_csv(
    TABLES / "concept_governance_actions.csv",
    governance_rows,
    [
        "review_id",
        "concept_id",
        "concept_name",
        "owner_group",
        "review_cadence",
        "governance_strength",
        "recommended_action",
        "definition_owner",
        "metric_owner",
        "revision_trigger_quality",
        "documentation_quality",
        "stakeholder_review_quality",
        "governance_risk",
    ],
)

# ---------------------------------------------------------------------
# 9. Strategist report
# ---------------------------------------------------------------------

weakest_concepts = sorted(clarity_rows, key=lambda item: item["conceptual_clarity_score"])[:5]
highest_false_consensus = interpretation_rows[:5]
highest_metric_risk = metric_rows[:6]
highest_drift = drift_rows[:5]
weakest_governance = governance_rows[:5]
highest_decision_power = implication_rows[:5]
highest_distinction_risk = distinction_rows[:5]

report: list[str] = []

report.append("# Conceptual Clarity Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic separates concept clarity, interpretation variance, boundary quality, "
    "distinction risk, metric validity, decision implications, conceptual drift, and governance maturity. "
    "The purpose is to help strategists identify when the problem is not weak execution, but weak meaning."
)
report.append("")
report.append("## Concepts requiring the most clarity work")
report.append("")

for item in weakest_concepts:
    report.append(
        f"- **{item['concept_id']} — {item['concept_name']}**: clarity score {item['conceptual_clarity_score']}; "
        f"ambiguity risk {item['ambiguity_risk']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest false-consensus risks")
report.append("")

for item in highest_false_consensus:
    report.append(
        f"- **{item['concept_id']} — {item['concept_name']}**: false-consensus risk {item['false_consensus_risk']}; "
        f"mean alignment {item['mean_interpretation_alignment']}; flag: {item['flag']}."
    )

report.append("")
report.append("## Highest metric proxy risks")
report.append("")

for item in highest_metric_risk:
    report.append(
        f"- **{item['metric_id']} — {item['metric_name']}** for **{item['concept_name']}**: "
        f"proxy failure risk {item['proxy_failure_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest conceptual drift priorities")
report.append("")

for item in highest_drift:
    report.append(
        f"- **{item['drift_id']} — {item['concept_name']}**: drift type {item['drift_type']}; "
        f"priority {item['drift_priority']}; response: {item['recommended_response']}."
    )

report.append("")
report.append("## Weakest concept governance areas")
report.append("")

for item in weakest_governance:
    report.append(
        f"- **{item['review_id']} — {item['concept_name']}**: governance strength {item['governance_strength']}; "
        f"owner group: {item['owner_group']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Concepts that must be clarified before major decisions")
report.append("")

for item in highest_decision_power:
    report.append(
        f"- **{item['concept_id']} — {item['concept_name']}** in **{item['decision_context']}**: "
        f"decision power {item['decision_power']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest distinction risks")
report.append("")

for item in highest_distinction_risk:
    report.append(
        f"- **{item['concept_name']} vs {item['confused_with']}**: distinction risk {item['distinction_risk']}; "
        f"consequence: {item['decision_consequence']}"
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "The value of this workflow is disciplined meaning management. It helps a strategist ask whether "
    "a concept is clear enough to govern decisions, whether different teams interpret it consistently, "
    "whether its metrics are valid, whether its boundaries are stable, whether it has drifted, and whether "
    "its governance is strong enough to preserve meaning over time."
)

(REPORTS / "conceptual_clarity_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "weakest_concepts": weakest_concepts,
    "highest_false_consensus": highest_false_consensus,
    "highest_metric_risk": highest_metric_risk,
    "highest_drift": highest_drift,
    "weakest_governance": weakest_governance,
    "highest_decision_power": highest_decision_power,
    "highest_distinction_risk": highest_distinction_risk,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced conceptual clarity diagnostics complete.")
print(f"Wrote: {TABLES / 'conceptual_clarity_scores.csv'}")
print(f"Wrote: {TABLES / 'interpretation_variance_register.csv'}")
print(f"Wrote: {TABLES / 'metric_validity_review.csv'}")
print(f"Wrote: {TABLES / 'distinction_map_scores.csv'}")
print(f"Wrote: {TABLES / 'conceptual_drift_register.csv'}")
print(f"Wrote: {TABLES / 'concept_governance_actions.csv'}")
print(f"Wrote: {REPORTS / 'conceptual_clarity_diagnostic_report.md'}")
