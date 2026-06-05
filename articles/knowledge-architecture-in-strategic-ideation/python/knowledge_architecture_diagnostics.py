#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Knowledge Architecture in Strategic Ideation.

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


ideas = read_csv(RAW / "idea_records.csv")
relationships = read_csv(RAW / "relationships.csv")
evidence = read_csv(RAW / "evidence_assumptions.csv")
retrieval = read_csv(RAW / "retrieval_tests.csv")
stewardship = read_csv(RAW / "stewardship_ethics.csv")

idea_names = {row["idea_id"]: row["idea_title"] for row in ideas}

# ---------------------------------------------------------------------
# 1. Idea architecture strength
# ---------------------------------------------------------------------

idea_rows: list[dict[str, object]] = []

for row in ideas:
    strength = (
        0.11 * f(row, "taxonomy_quality")
        + 0.12 * f(row, "metadata_completeness")
        + 0.11 * f(row, "semantic_clarity")
        + 0.12 * f(row, "evidence_linkage")
        + 0.11 * f(row, "assumption_clarity")
        + 0.11 * f(row, "relationship_mapping")
        + 0.12 * f(row, "retrieval_readiness")
        + 0.09 * f(row, "decision_memory")
        + 0.07 * f(row, "stewardship_quality")
        + 0.04 * f(row, "ethical_representation")
    )
    risk = (
        0.11 * (1 - f(row, "taxonomy_quality"))
        + 0.12 * (1 - f(row, "metadata_completeness"))
        + 0.12 * (1 - f(row, "semantic_clarity"))
        + 0.13 * (1 - f(row, "evidence_linkage"))
        + 0.12 * (1 - f(row, "assumption_clarity"))
        + 0.10 * (1 - f(row, "relationship_mapping"))
        + 0.12 * (1 - f(row, "retrieval_readiness"))
        + 0.09 * (1 - f(row, "decision_memory"))
        + 0.06 * (1 - f(row, "stewardship_quality"))
        + 0.03 * (1 - f(row, "ethical_representation"))
    )

    if strength >= 0.74:
        diagnosis = "strong_strategic_knowledge_architecture"
    elif f(row, "evidence_linkage") < 0.55:
        diagnosis = "evidence_linkage_gap"
    elif f(row, "metadata_completeness") < 0.60:
        diagnosis = "metadata_quality_gap"
    elif f(row, "retrieval_readiness") < 0.60:
        diagnosis = "retrieval_and_reuse_gap"
    elif f(row, "decision_memory") < 0.55:
        diagnosis = "decision_memory_gap"
    elif f(row, "ethical_representation") < 0.55:
        diagnosis = "ethical_representation_review_required"
    else:
        diagnosis = "targeted_architecture_repair"

    idea_rows.append({
        "idea_id": row["idea_id"],
        "idea_title": row["idea_title"],
        "domain": row["domain"],
        "strategic_function": row["strategic_function"],
        "maturity": row["maturity"],
        "evidence_level": row["evidence_level"],
        "decision_status": row["decision_status"],
        "architecture_strength": round(strength, 4),
        "architecture_risk": round(risk, 4),
        "weakest_dimension": min(
            [
                ("taxonomy_quality", f(row, "taxonomy_quality")),
                ("metadata_completeness", f(row, "metadata_completeness")),
                ("semantic_clarity", f(row, "semantic_clarity")),
                ("evidence_linkage", f(row, "evidence_linkage")),
                ("assumption_clarity", f(row, "assumption_clarity")),
                ("relationship_mapping", f(row, "relationship_mapping")),
                ("retrieval_readiness", f(row, "retrieval_readiness")),
                ("decision_memory", f(row, "decision_memory")),
                ("stewardship_quality", f(row, "stewardship_quality")),
                ("ethical_representation", f(row, "ethical_representation")),
            ],
            key=lambda item: item[1],
        )[0],
        "diagnosis": diagnosis,
        "description": row["description"],
    })

idea_rows.sort(key=lambda item: item["architecture_strength"], reverse=True)
write_csv(TABLES / "idea_architecture_scores.csv", idea_rows)
write_csv(PROCESSED / "idea_architecture_scores.csv", idea_rows)

# ---------------------------------------------------------------------
# 2. Evidence and assumption quality
# ---------------------------------------------------------------------

evidence_rows: list[dict[str, object]] = []
for row in evidence:
    quality = (
        0.17 * f(row, "source_quality")
        + 0.18 * f(row, "confidence_level")
        + 0.13 * f(row, "review_frequency")
        - 0.12 * f(row, "uncertainty_level")
        + 0.12 * f(row, "counterevidence_visibility")
        + 0.14 * f(row, "owner_clarity")
        + 0.16 * f(row, "revision_trigger_quality")
        + 0.12
    )
    evidence_rows.append({
        "record_id": row["record_id"],
        "idea_id": row["idea_id"],
        "idea_title": idea_names[row["idea_id"]],
        "knowledge_type": row["knowledge_type"],
        "item_name": row["item_name"],
        "evidence_assumption_score": round(quality, 4),
        "recommended_action": row["review_action"],
    })

evidence_rows.sort(key=lambda item: item["evidence_assumption_score"])
write_csv(TABLES / "evidence_assumption_scores.csv", evidence_rows)

# ---------------------------------------------------------------------
# 3. Relationship mapping quality
# ---------------------------------------------------------------------

relationship_rows: list[dict[str, object]] = []
for row in relationships:
    score = (
        0.26 * f(row, "relationship_strength")
        + 0.24 * f(row, "relationship_confidence")
        + 0.28 * f(row, "strategic_value")
        - 0.12 * f(row, "maintenance_need")
        + 0.10
    )
    relationship_rows.append({
        "relationship_id": row["relationship_id"],
        "source_id": row["source_id"],
        "source_title": idea_names.get(row["source_id"], row["source_id"]),
        "target_id": row["target_id"],
        "target_title": idea_names.get(row["target_id"], row["target_id"]),
        "relationship_type": row["relationship_type"],
        "relationship_mapping_score": round(score, 4),
        "recommended_action": row["review_action"],
    })

relationship_rows.sort(key=lambda item: item["relationship_mapping_score"], reverse=True)
write_csv(TABLES / "relationship_mapping_scores.csv", relationship_rows)

# ---------------------------------------------------------------------
# 4. Retrieval and reuse
# ---------------------------------------------------------------------

retrieval_rows: list[dict[str, object]] = []
for row in retrieval:
    score = (
        0.16 * f(row, "relevance")
        + 0.15 * f(row, "context_completeness")
        + 0.16 * f(row, "trustworthiness")
        + 0.14 * f(row, "usability")
        + 0.14 * f(row, "searchability")
        + 0.15 * f(row, "reuse_potential")
        + 0.10
    )
    retrieval_rows.append({
        "test_id": row["test_id"],
        "query_type": row["query_type"],
        "query_text": row["query_text"],
        "expected_idea_id": row["expected_idea_id"],
        "expected_idea_title": idea_names[row["expected_idea_id"]],
        "retrieval_reuse_score": round(score, 4),
        "recommended_action": row["review_action"],
    })

retrieval_rows.sort(key=lambda item: item["retrieval_reuse_score"])
write_csv(TABLES / "retrieval_reuse_scores.csv", retrieval_rows)

# ---------------------------------------------------------------------
# 5. Stewardship and ethics
# ---------------------------------------------------------------------

stewardship_rows: list[dict[str, object]] = []
for row in stewardship:
    stewardship_score = (
        0.13 * f(row, "taxonomy_stewardship")
        + 0.13 * f(row, "metadata_stewardship")
        + 0.13 * f(row, "evidence_standard_quality")
        + 0.13 * f(row, "repository_curation")
        + 0.11 * f(row, "access_governance")
        - 0.07 * f(row, "privacy_sensitivity")
        + 0.13 * f(row, "stakeholder_representation")
        + 0.12 * f(row, "dissent_preservation")
        - 0.05 * f(row, "ethical_risk")
        + 0.04
    )
    ethics_risk = (
        0.22 * f(row, "ethical_risk")
        + 0.14 * f(row, "privacy_sensitivity")
        + 0.16 * (1 - f(row, "stakeholder_representation"))
        + 0.14 * (1 - f(row, "dissent_preservation"))
        + 0.12 * (1 - f(row, "access_governance"))
        + 0.10 * (1 - f(row, "evidence_standard_quality"))
        + 0.12 * (1 - f(row, "repository_curation"))
    )
    stewardship_rows.append({
        "stewardship_id": row["stewardship_id"],
        "idea_id": row["idea_id"],
        "idea_title": idea_names[row["idea_id"]],
        "stewardship_score": round(stewardship_score, 4),
        "ethical_knowledge_risk": round(ethics_risk, 4),
        "recommended_action": row["review_action"],
    })

stewardship_rows.sort(key=lambda item: item["stewardship_score"])
write_csv(TABLES / "stewardship_ethics_scores.csv", stewardship_rows)

summary = {
    "idea_architecture": idea_rows,
    "evidence_assumptions": evidence_rows,
    "relationships": relationship_rows,
    "retrieval_reuse": retrieval_rows,
    "stewardship_ethics": stewardship_rows,
}
(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

report = [
    "# Knowledge Architecture in Strategic Ideation Diagnostic Report",
    "",
    "## Executive summary",
    "",
    "This diagnostic evaluates whether strategic ideas are structured as reusable knowledge objects. It reviews taxonomy quality, metadata completeness, semantic clarity, evidence linkage, assumption clarity, relationship mapping, retrieval readiness, decision memory, stewardship quality, and ethical representation.",
    "",
    "## Strategic idea architecture ranking",
    "",
]
for item in idea_rows:
    report.append(
        f"- **{item['idea_id']} — {item['idea_title']}**: architecture strength {item['architecture_strength']}; "
        f"risk {item['architecture_risk']}; weakest dimension: {item['weakest_dimension']}; diagnosis: {item['diagnosis']}."
    )

report.extend(["", "## Evidence and assumption repair priorities", ""])
for item in evidence_rows:
    report.append(
        f"- **{item['idea_title']} / {item['item_name']}**: score {item['evidence_assumption_score']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Relationship mapping review", ""])
for item in relationship_rows:
    report.append(
        f"- **{item['source_title']} → {item['target_title']}** ({item['relationship_type']}): score {item['relationship_mapping_score']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Retrieval and reuse review", ""])
for item in retrieval_rows:
    report.append(
        f"- **{item['query_type']}** for {item['expected_idea_title']}: retrieval/reuse score {item['retrieval_reuse_score']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Stewardship and ethics review", ""])
for item in stewardship_rows:
    report.append(
        f"- **{item['idea_title']}**: stewardship {item['stewardship_score']}; ethical knowledge risk {item['ethical_knowledge_risk']}; action: {item['recommended_action']}."
    )

report.extend([
    "",
    "## Professional interpretation",
    "",
    "Knowledge architecture turns strategic ideas into organized, traceable, reusable intelligence. Weak architecture produces idea clutter, memory loss, ambiguous language, unsupported claims, and retrieval failure. Strong architecture links ideas to metadata, evidence, assumptions, decisions, relationships, lessons, governance, and ethical representation.",
])

(REPORTS / "knowledge_architecture_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

print("Advanced knowledge architecture diagnostics complete.")
print(f"Wrote: {TABLES / 'idea_architecture_scores.csv'}")
print(f"Wrote: {TABLES / 'evidence_assumption_scores.csv'}")
print(f"Wrote: {TABLES / 'relationship_mapping_scores.csv'}")
print(f"Wrote: {TABLES / 'retrieval_reuse_scores.csv'}")
print(f"Wrote: {TABLES / 'stewardship_ethics_scores.csv'}")
print(f"Wrote: {REPORTS / 'knowledge_architecture_diagnostic_report.md'}")
