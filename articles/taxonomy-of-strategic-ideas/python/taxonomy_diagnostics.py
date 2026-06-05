#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Taxonomy of Strategic Ideas.

Uses only Python standard library.
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


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def f(row: dict[str, str], key: str) -> float:
    return float(row[key])


records = read_csv(RAW / "taxonomy_records.csv")
errors = read_csv(RAW / "classification_errors.csv")
relationships = read_csv(RAW / "idea_relationships.csv")
retrieval_tests = read_csv(RAW / "retrieval_tests.csv")
governance_ethics = read_csv(RAW / "governance_ethics.csv")

record_names = {row["record_id"]: row["idea_record"] for row in records}

# ---------------------------------------------------------------------
# 1. Taxonomy record strength
# ---------------------------------------------------------------------

record_rows: list[dict[str, object]] = []
for row in records:
    strength = (
        0.12 * f(row, "category_clarity")
        + 0.10 * f(row, "level_fit")
        + 0.10 * f(row, "maturity_accuracy")
        + 0.12 * f(row, "evidence_classification")
        + 0.12 * f(row, "function_clarity")
        + 0.10 * f(row, "relationship_mapping")
        + 0.12 * f(row, "retrieval_value")
        + 0.09 * f(row, "governance_strength")
        + 0.08 * f(row, "ethical_visibility")
        + 0.05 * f(row, "ai_classification_quality")
    )
    risk = (
        0.12 * (1 - f(row, "category_clarity"))
        + 0.10 * (1 - f(row, "level_fit"))
        + 0.10 * (1 - f(row, "maturity_accuracy"))
        + 0.12 * (1 - f(row, "evidence_classification"))
        + 0.12 * (1 - f(row, "function_clarity"))
        + 0.10 * (1 - f(row, "relationship_mapping"))
        + 0.12 * (1 - f(row, "retrieval_value"))
        + 0.09 * (1 - f(row, "governance_strength"))
        + 0.08 * (1 - f(row, "ethical_visibility"))
        + 0.05 * (1 - f(row, "ai_classification_quality"))
    )

    if strength >= 0.76:
        diagnosis = "strong_taxonomic_record"
    elif f(row, "category_clarity") < 0.65:
        diagnosis = "idea_type_classification_gap"
    elif f(row, "evidence_classification") < 0.60:
        diagnosis = "evidence_classification_gap"
    elif f(row, "function_clarity") < 0.65:
        diagnosis = "strategic_function_gap"
    elif f(row, "retrieval_value") < 0.65:
        diagnosis = "retrieval_gap"
    elif f(row, "governance_strength") < 0.60:
        diagnosis = "taxonomy_governance_gap"
    elif f(row, "ethical_visibility") < 0.60:
        diagnosis = "ethical_visibility_review_required"
    elif f(row, "ai_classification_quality") < 0.50:
        diagnosis = "ai_classification_review_required"
    else:
        diagnosis = "targeted_taxonomy_repair"

    weakest_dimension = min(
        [
            ("category_clarity", f(row, "category_clarity")),
            ("level_fit", f(row, "level_fit")),
            ("maturity_accuracy", f(row, "maturity_accuracy")),
            ("evidence_classification", f(row, "evidence_classification")),
            ("function_clarity", f(row, "function_clarity")),
            ("relationship_mapping", f(row, "relationship_mapping")),
            ("retrieval_value", f(row, "retrieval_value")),
            ("governance_strength", f(row, "governance_strength")),
            ("ethical_visibility", f(row, "ethical_visibility")),
            ("ai_classification_quality", f(row, "ai_classification_quality")),
        ],
        key=lambda item: item[1],
    )[0]

    record_rows.append({
        "record_id": row["record_id"],
        "idea_record": row["idea_record"],
        "idea_type": row["idea_type"],
        "strategic_level": row["strategic_level"],
        "maturity_state": row["maturity_state"],
        "evidence_status": row["evidence_status"],
        "strategic_function": row["strategic_function"],
        "taxonomy_strength": round(strength, 4),
        "taxonomy_risk": round(risk, 4),
        "weakest_dimension": weakest_dimension,
        "diagnosis": diagnosis,
    })

record_rows.sort(key=lambda item: item["taxonomy_strength"], reverse=True)
write_csv(TABLES / "taxonomy_record_scores.csv", record_rows)
write_csv(PROCESSED / "taxonomy_record_scores.csv", record_rows)

# ---------------------------------------------------------------------
# 2. Classification error risk
# ---------------------------------------------------------------------

error_rows: list[dict[str, object]] = []
for row in errors:
    risk_score = (
        0.30 * f(row, "severity")
        + 0.25 * f(row, "likelihood")
        + 0.20 * (1 - f(row, "detectability"))
        + 0.15 * (1 - f(row, "repair_quality"))
        + 0.10 * f(row, "governance_need")
    )
    error_rows.append({
        "error_id": row["error_id"],
        "record_id": row["record_id"],
        "idea_record": record_names[row["record_id"]],
        "error_type": row["error_type"],
        "classification_error_risk": round(risk_score, 4),
        "review_action": row["review_action"],
    })

error_rows.sort(key=lambda item: item["classification_error_risk"], reverse=True)
write_csv(TABLES / "classification_error_scores.csv", error_rows)

# ---------------------------------------------------------------------
# 3. Relationship quality
# ---------------------------------------------------------------------

relationship_rows: list[dict[str, object]] = []
for row in relationships:
    quality = (
        0.22 * f(row, "relationship_clarity")
        + 0.24 * f(row, "strategic_importance")
        + 0.18 * f(row, "evidence_support")
        + 0.16 * f(row, "governance_visibility")
        + 0.20 * f(row, "reuse_value")
    )
    relationship_rows.append({
        "relationship_id": row["relationship_id"],
        "source_record": row["source_record"],
        "source_name": record_names[row["source_record"]],
        "target_record": row["target_record"],
        "target_name": record_names[row["target_record"]],
        "relationship_type": row["relationship_type"],
        "relationship_quality_score": round(quality, 4),
        "review_action": row["review_action"],
    })

relationship_rows.sort(key=lambda item: item["relationship_quality_score"])
write_csv(TABLES / "relationship_quality_scores.csv", relationship_rows)

# ---------------------------------------------------------------------
# 4. Retrieval and reuse quality
# ---------------------------------------------------------------------

retrieval_rows: list[dict[str, object]] = []
for row in retrieval_tests:
    score = (
        0.14 * f(row, "relevance")
        + 0.13 * f(row, "context_completeness")
        + 0.14 * f(row, "classification_accuracy")
        + 0.13 * f(row, "searchability")
        + 0.15 * f(row, "decision_usefulness")
        + 0.13 * f(row, "transfer_caution")
        + 0.18 * f(row, "ethical_visibility")
    )
    retrieval_rows.append({
        "test_id": row["test_id"],
        "query_type": row["query_type"],
        "query_text": row["query_text"],
        "expected_record": row["expected_record"],
        "expected_name": record_names[row["expected_record"]],
        "retrieval_test_score": round(score, 4),
        "review_action": row["review_action"],
    })

retrieval_rows.sort(key=lambda item: item["retrieval_test_score"])
write_csv(TABLES / "retrieval_test_scores.csv", retrieval_rows)

# ---------------------------------------------------------------------
# 5. Governance and ethics
# ---------------------------------------------------------------------

governance_rows: list[dict[str, object]] = []
for row in governance_ethics:
    stewardship = (
        0.11 * f(row, "category_ownership")
        + 0.13 * f(row, "definition_quality")
        + 0.11 * f(row, "change_control")
        + 0.12 * f(row, "metadata_quality")
        + 0.10 * f(row, "review_cadence")
        + 0.10 * f(row, "user_guidance")
        + 0.08 * f(row, "ai_review")
        + 0.09 * f(row, "stakeholder_visibility")
        + 0.08 * f(row, "dissent_preservation")
        + 0.08 * f(row, "burden_visibility")
        - 0.05 * f(row, "ethical_risk")
        + 0.05
    )
    ethical_risk = (
        0.20 * f(row, "ethical_risk")
        + 0.13 * (1 - f(row, "stakeholder_visibility"))
        + 0.13 * (1 - f(row, "dissent_preservation"))
        + 0.13 * (1 - f(row, "burden_visibility"))
        + 0.11 * (1 - f(row, "definition_quality"))
        + 0.10 * (1 - f(row, "metadata_quality"))
        + 0.10 * (1 - f(row, "ai_review"))
        + 0.10 * (1 - f(row, "change_control"))
    )
    governance_rows.append({
        "governance_id": row["governance_id"],
        "taxonomy_area": row["taxonomy_area"],
        "taxonomy_stewardship_score": round(stewardship, 4),
        "ethical_classification_risk": round(ethical_risk, 4),
        "review_action": row["review_action"],
    })

governance_rows.sort(key=lambda item: item["taxonomy_stewardship_score"])
write_csv(TABLES / "governance_ethics_scores.csv", governance_rows)

summary = {
    "taxonomy_records": record_rows,
    "classification_errors": error_rows,
    "relationships": relationship_rows,
    "retrieval_tests": retrieval_rows,
    "governance_ethics": governance_rows,
}
(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

report = [
    "# Taxonomy of Strategic Ideas Diagnostic Report",
    "",
    "## Executive summary",
    "",
    "This diagnostic evaluates whether strategic idea taxonomy improves classification, comparison, retrieval, governance, learning, and accountability. It reviews idea type clarity, strategic level fit, maturity accuracy, evidence classification, strategic function clarity, relationship mapping, retrieval value, governance strength, ethical visibility, and AI classification quality.",
    "",
    "## Taxonomy record strength ranking",
    "",
]
for item in record_rows:
    report.append(
        f"- **{item['record_id']} — {item['idea_record']}**: taxonomy strength {item['taxonomy_strength']}; "
        f"taxonomy risk {item['taxonomy_risk']}; weakest dimension: {item['weakest_dimension']}; diagnosis: {item['diagnosis']}."
    )

report.extend(["", "## Classification error risks", ""])
for item in error_rows:
    report.append(
        f"- **{item['idea_record']}**: {item['error_type']} risk {item['classification_error_risk']}; action: {item['review_action']}."
    )

report.extend(["", "## Relationship quality review", ""])
for item in relationship_rows:
    report.append(
        f"- **{item['source_name']} → {item['target_name']}** ({item['relationship_type']}): relationship score {item['relationship_quality_score']}; action: {item['review_action']}."
    )

report.extend(["", "## Retrieval test review", ""])
for item in retrieval_rows:
    report.append(
        f"- **{item['query_type']}**: retrieval score {item['retrieval_test_score']}; action: {item['review_action']}."
    )

report.extend(["", "## Governance and ethics review", ""])
for item in governance_rows:
    report.append(
        f"- **{item['taxonomy_area']}**: stewardship {item['taxonomy_stewardship_score']}; ethical risk {item['ethical_classification_risk']}; action: {item['review_action']}."
    )

report.extend([
    "",
    "## Professional interpretation",
    "",
    "Strategic idea taxonomy creates value when it helps teams know what kind of idea they are evaluating, what evidence is required, what level of strategy is affected, what relationships matter, how the idea should be retrieved later, and what ethical or stakeholder implications must remain visible.",
])

(REPORTS / "taxonomy_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

print("Advanced strategic idea taxonomy diagnostics complete.")
print(f"Wrote: {TABLES / 'taxonomy_record_scores.csv'}")
print(f"Wrote: {TABLES / 'classification_error_scores.csv'}")
print(f"Wrote: {TABLES / 'relationship_quality_scores.csv'}")
print(f"Wrote: {TABLES / 'retrieval_test_scores.csv'}")
print(f"Wrote: {TABLES / 'governance_ethics_scores.csv'}")
print(f"Wrote: {REPORTS / 'taxonomy_diagnostic_report.md'}")
