#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Institutional Memory and Idea Systems.

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


memory_systems = read_csv(RAW / "memory_systems.csv")
idea_lifecycle = read_csv(RAW / "idea_lifecycle.csv")
decision_memory = read_csv(RAW / "decision_memory.csv")
retrieval_tests = read_csv(RAW / "retrieval_tests.csv")
learning_updates = read_csv(RAW / "learning_updates.csv")
stewardship_ethics = read_csv(RAW / "stewardship_ethics.csv")

system_names = {row["system_id"]: row["system_area"] for row in memory_systems}
idea_names = {row["idea_id"]: row["idea_title"] for row in idea_lifecycle}

# ---------------------------------------------------------------------
# 1. Memory system strength
# ---------------------------------------------------------------------

memory_rows: list[dict[str, object]] = []
for row in memory_systems:
    strength = (
        0.09 * f(row, "capture_quality")
        + 0.11 * f(row, "metadata_completeness")
        + 0.11 * f(row, "context_preservation")
        + 0.13 * f(row, "decision_memory")
        + 0.12 * f(row, "learning_integration")
        + 0.12 * f(row, "retrieval_readiness")
        + 0.10 * f(row, "reuse_potential")
        + 0.08 * f(row, "stewardship_quality")
        + 0.06 * f(row, "continuity_resilience")
        + 0.05 * f(row, "ethical_memory")
        + 0.03 * f(row, "ai_governance")
    )
    failure_risk = (
        0.09 * (1 - f(row, "capture_quality"))
        + 0.11 * (1 - f(row, "metadata_completeness"))
        + 0.11 * (1 - f(row, "context_preservation"))
        + 0.13 * (1 - f(row, "decision_memory"))
        + 0.12 * (1 - f(row, "learning_integration"))
        + 0.12 * (1 - f(row, "retrieval_readiness"))
        + 0.09 * (1 - f(row, "reuse_potential"))
        + 0.08 * (1 - f(row, "stewardship_quality"))
        + 0.07 * (1 - f(row, "continuity_resilience"))
        + 0.05 * (1 - f(row, "ethical_memory"))
        + 0.03 * (1 - f(row, "ai_governance"))
    )

    if strength >= 0.74:
        diagnosis = "strong_institutional_idea_memory"
    elif f(row, "decision_memory") < 0.55:
        diagnosis = "decision_memory_gap"
    elif f(row, "learning_integration") < 0.55:
        diagnosis = "learning_integration_gap"
    elif f(row, "retrieval_readiness") < 0.60:
        diagnosis = "retrieval_gap"
    elif f(row, "stewardship_quality") < 0.55:
        diagnosis = "stewardship_gap"
    elif f(row, "ethical_memory") < 0.55:
        diagnosis = "ethical_memory_review_required"
    elif f(row, "continuity_resilience") < 0.55:
        diagnosis = "continuity_risk"
    elif row["system_type"] == "ai_memory" and f(row, "ai_governance") < 0.45:
        diagnosis = "urgent_ai_memory_governance_required"
    else:
        diagnosis = "targeted_memory_repair"

    weakest_dimension = min(
        [
            ("capture_quality", f(row, "capture_quality")),
            ("metadata_completeness", f(row, "metadata_completeness")),
            ("context_preservation", f(row, "context_preservation")),
            ("decision_memory", f(row, "decision_memory")),
            ("learning_integration", f(row, "learning_integration")),
            ("retrieval_readiness", f(row, "retrieval_readiness")),
            ("reuse_potential", f(row, "reuse_potential")),
            ("stewardship_quality", f(row, "stewardship_quality")),
            ("continuity_resilience", f(row, "continuity_resilience")),
            ("ethical_memory", f(row, "ethical_memory")),
            ("ai_governance", f(row, "ai_governance")),
        ],
        key=lambda item: item[1],
    )[0]

    memory_rows.append({
        "system_id": row["system_id"],
        "system_area": row["system_area"],
        "system_type": row["system_type"],
        "memory_strength": round(strength, 4),
        "memory_failure_risk": round(failure_risk, 4),
        "weakest_dimension": weakest_dimension,
        "diagnosis": diagnosis,
        "description": row["description"],
    })

memory_rows.sort(key=lambda item: item["memory_strength"], reverse=True)
write_csv(TABLES / "memory_system_scores.csv", memory_rows)
write_csv(PROCESSED / "memory_system_scores.csv", memory_rows)

# ---------------------------------------------------------------------
# 2. Idea lifecycle quality
# ---------------------------------------------------------------------

lifecycle_rows: list[dict[str, object]] = []
for row in idea_lifecycle:
    score = (
        0.11 * f(row, "source_quality")
        + 0.13 * f(row, "problem_clarity")
        + 0.12 * f(row, "mechanism_clarity")
        + 0.13 * f(row, "evidence_level")
        + 0.12 * f(row, "assumption_quality")
        + 0.13 * f(row, "decision_status_quality")
        + 0.13 * f(row, "learning_update_quality")
        + 0.13 * f(row, "reuse_condition_quality")
    )
    lifecycle_rows.append({
        "idea_id": row["idea_id"],
        "idea_title": row["idea_title"],
        "lifecycle_stage": row["lifecycle_stage"],
        "lifecycle_quality_score": round(score, 4),
        "recommended_action": row["review_action"],
    })

lifecycle_rows.sort(key=lambda item: item["lifecycle_quality_score"])
write_csv(TABLES / "idea_lifecycle_scores.csv", lifecycle_rows)

# ---------------------------------------------------------------------
# 3. Decision memory quality
# ---------------------------------------------------------------------

decision_rows: list[dict[str, object]] = []
for row in decision_memory:
    score = (
        0.13 * f(row, "rationale_quality")
        + 0.13 * f(row, "evidence_quality")
        + 0.12 * f(row, "assumption_visibility")
        + 0.11 * f(row, "alternative_visibility")
        + 0.12 * f(row, "tradeoff_visibility")
        + 0.12 * f(row, "dissent_preservation")
        + 0.10 * f(row, "owner_clarity")
        + 0.13 * f(row, "revision_trigger_quality")
        + 0.14 * f(row, "traceability_quality")
    )
    decision_rows.append({
        "decision_id": row["decision_id"],
        "idea_id": row["idea_id"],
        "idea_title": idea_names[row["idea_id"]],
        "decision_type": row["decision_type"],
        "decision_memory_score": round(score, 4),
        "recommended_action": row["review_action"],
    })

decision_rows.sort(key=lambda item: item["decision_memory_score"])
write_csv(TABLES / "decision_memory_scores.csv", decision_rows)

# ---------------------------------------------------------------------
# 4. Retrieval and reuse
# ---------------------------------------------------------------------

retrieval_rows: list[dict[str, object]] = []
for row in retrieval_tests:
    score = (
        0.15 * f(row, "relevance")
        + 0.15 * f(row, "context_completeness")
        + 0.15 * f(row, "trustworthiness")
        + 0.13 * f(row, "timing_usefulness")
        + 0.13 * f(row, "searchability")
        + 0.15 * f(row, "reuse_potential")
        + 0.14 * f(row, "transfer_caution_quality")
    )
    retrieval_rows.append({
        "test_id": row["test_id"],
        "query_type": row["query_type"],
        "query_text": row["query_text"],
        "expected_record": row["expected_record"],
        "retrieval_reuse_score": round(score, 4),
        "recommended_action": row["review_action"],
    })

retrieval_rows.sort(key=lambda item: item["retrieval_reuse_score"])
write_csv(TABLES / "retrieval_reuse_scores.csv", retrieval_rows)

# ---------------------------------------------------------------------
# 5. Learning update quality
# ---------------------------------------------------------------------

learning_rows: list[dict[str, object]] = []
for row in learning_updates:
    score = (
        0.15 * f(row, "evidence_quality")
        + 0.14 * f(row, "interpretation_quality")
        + 0.14 * f(row, "assumption_update_quality")
        + 0.14 * f(row, "decision_update_quality")
        + 0.14 * f(row, "stakeholder_update_quality")
        + 0.14 * f(row, "reuse_tag_quality")
        + 0.15 * f(row, "followup_quality")
    )
    learning_rows.append({
        "learning_id": row["learning_id"],
        "idea_id": row["idea_id"],
        "idea_title": idea_names[row["idea_id"]],
        "learning_source": row["learning_source"],
        "learning_update_score": round(score, 4),
        "recommended_action": row["review_action"],
    })

learning_rows.sort(key=lambda item: item["learning_update_score"])
write_csv(TABLES / "learning_update_scores.csv", learning_rows)

# ---------------------------------------------------------------------
# 6. Stewardship and ethical memory
# ---------------------------------------------------------------------

stewardship_rows: list[dict[str, object]] = []
for row in stewardship_ethics:
    stewardship_score = (
        0.12 * f(row, "ownership_clarity")
        + 0.12 * f(row, "lifecycle_governance")
        + 0.13 * f(row, "metadata_stewardship")
        + 0.12 * f(row, "repository_curation")
        + 0.10 * f(row, "access_governance")
        + 0.12 * f(row, "continuity_planning")
        + 0.10 * f(row, "stakeholder_memory")
        + 0.10 * f(row, "dissent_preservation")
        - 0.04 * f(row, "privacy_sensitivity")
        - 0.05 * f(row, "ethical_risk")
        + 0.08
    )
    ethical_risk = (
        0.20 * f(row, "ethical_risk")
        + 0.14 * f(row, "privacy_sensitivity")
        + 0.14 * (1 - f(row, "stakeholder_memory"))
        + 0.14 * (1 - f(row, "dissent_preservation"))
        + 0.12 * (1 - f(row, "access_governance"))
        + 0.10 * (1 - f(row, "metadata_stewardship"))
        + 0.08 * (1 - f(row, "continuity_planning"))
        + 0.08 * (1 - f(row, "repository_curation"))
    )
    stewardship_rows.append({
        "stewardship_id": row["stewardship_id"],
        "system_id": row["system_id"],
        "system_area": system_names[row["system_id"]],
        "stewardship_score": round(stewardship_score, 4),
        "ethical_memory_risk": round(ethical_risk, 4),
        "recommended_action": row["review_action"],
    })

stewardship_rows.sort(key=lambda item: item["stewardship_score"])
write_csv(TABLES / "stewardship_ethics_scores.csv", stewardship_rows)

summary = {
    "memory_systems": memory_rows,
    "idea_lifecycle": lifecycle_rows,
    "decision_memory": decision_rows,
    "retrieval_reuse": retrieval_rows,
    "learning_updates": learning_rows,
    "stewardship_ethics": stewardship_rows,
}
(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

report = [
    "# Institutional Memory and Idea Systems Diagnostic Report",
    "",
    "## Executive summary",
    "",
    "This diagnostic evaluates whether strategic ideas are preserved as reusable institutional intelligence rather than scattered records. It reviews capture quality, metadata completeness, context preservation, decision memory, learning integration, retrieval readiness, reuse potential, stewardship, continuity resilience, ethical memory, and AI memory governance.",
    "",
    "## Institutional memory strength ranking",
    "",
]
for item in memory_rows:
    report.append(
        f"- **{item['system_id']} — {item['system_area']}**: memory strength {item['memory_strength']}; "
        f"failure risk {item['memory_failure_risk']}; weakest dimension: {item['weakest_dimension']}; diagnosis: {item['diagnosis']}."
    )

report.extend(["", "## Idea lifecycle repair priorities", ""])
for item in lifecycle_rows:
    report.append(
        f"- **{item['idea_title']}** ({item['lifecycle_stage']}): lifecycle score {item['lifecycle_quality_score']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Decision-memory review", ""])
for item in decision_rows:
    report.append(
        f"- **{item['idea_title']}** ({item['decision_type']}): decision-memory score {item['decision_memory_score']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Retrieval and reuse review", ""])
for item in retrieval_rows:
    report.append(
        f"- **{item['query_type']}**: retrieval/reuse score {item['retrieval_reuse_score']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Learning update review", ""])
for item in learning_rows:
    report.append(
        f"- **{item['idea_title']} / {item['learning_source']}**: learning update score {item['learning_update_score']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Stewardship and ethical memory review", ""])
for item in stewardship_rows:
    report.append(
        f"- **{item['system_area']}**: stewardship {item['stewardship_score']}; ethical memory risk {item['ethical_memory_risk']}; action: {item['recommended_action']}."
    )

report.extend([
    "",
    "## Professional interpretation",
    "",
    "Institutional memory is strategic when it preserves ideas, evidence, assumptions, decisions, lessons, stakeholder concerns, reuse conditions, and revision triggers in a form that future teams can find, trust, interpret, and apply. Weak idea systems create strategic repetition, memory loss, undocumented drift, and rediscovery cycles. Strong idea systems build cumulative strategic intelligence.",
])

(REPORTS / "institutional_memory_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

print("Advanced institutional memory diagnostics complete.")
print(f"Wrote: {TABLES / 'memory_system_scores.csv'}")
print(f"Wrote: {TABLES / 'idea_lifecycle_scores.csv'}")
print(f"Wrote: {TABLES / 'decision_memory_scores.csv'}")
print(f"Wrote: {TABLES / 'retrieval_reuse_scores.csv'}")
print(f"Wrote: {TABLES / 'learning_update_scores.csv'}")
print(f"Wrote: {TABLES / 'stewardship_ethics_scores.csv'}")
print(f"Wrote: {REPORTS / 'institutional_memory_diagnostic_report.md'}")
