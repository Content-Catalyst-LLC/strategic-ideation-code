#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Learning Loops in Strategic Execution.

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


contexts = read_csv(RAW / "learning_contexts.csv")
feedback = read_csv(RAW / "feedback_quality.csv")
assumptions = read_csv(RAW / "assumption_reviews.csv")
governance = read_csv(RAW / "governance_learning.csv")
scaling = read_csv(RAW / "knowledge_scaling.csv")
ethics = read_csv(RAW / "ethics_power.csv")

names = {row["context_id"]: row["context_name"] for row in contexts}

# ---------------------------------------------------------------------
# 1. Learning loop strength and learning failure risk
# ---------------------------------------------------------------------

learning_rows: list[dict[str, object]] = []

for row in contexts:
    strength = (
        0.12 * f(row, "feedback_quality")
        + 0.12 * f(row, "assumption_review")
        + 0.11 * f(row, "interpretation_discipline")
        + 0.13 * f(row, "decision_authority")
        + 0.13 * f(row, "learning_closure")
        + 0.10 * f(row, "decision_memory")
        + 0.08 * f(row, "psychological_safety")
        + 0.08 * f(row, "knowledge_scaling")
        + 0.08 * f(row, "ethical_learning")
        + 0.07 * f(row, "strategic_coherence")
        + 0.08 * f(row, "adaptive_capacity")
    )
    failure_risk = (
        0.11 * (1 - f(row, "feedback_quality"))
        + 0.12 * (1 - f(row, "assumption_review"))
        + 0.10 * (1 - f(row, "interpretation_discipline"))
        + 0.14 * (1 - f(row, "decision_authority"))
        + 0.14 * (1 - f(row, "learning_closure"))
        + 0.11 * (1 - f(row, "decision_memory"))
        + 0.08 * (1 - f(row, "psychological_safety"))
        + 0.08 * (1 - f(row, "knowledge_scaling"))
        + 0.08 * (1 - f(row, "ethical_learning"))
        + 0.07 * (1 - f(row, "strategic_coherence"))
        + 0.07 * (1 - f(row, "adaptive_capacity"))
    )

    if strength >= 0.74:
        diagnosis = "strong_adaptive_learning_system"
    elif f(row, "decision_authority") < 0.45:
        diagnosis = "governance_authority_gap"
    elif f(row, "learning_closure") < 0.45:
        diagnosis = "feedback_not_changing_action"
    elif f(row, "decision_memory") < 0.40:
        diagnosis = "institutional_memory_gap"
    elif f(row, "ethical_learning") < 0.45:
        diagnosis = "ethical_learning_review_required"
    elif f(row, "assumption_review") < 0.45:
        diagnosis = "assumption_review_gap"
    else:
        diagnosis = "targeted_learning_loop_repair"

    learning_rows.append({
        "context_id": row["context_id"],
        "context_name": row["context_name"],
        "context_type": row["context_type"],
        "learning_loop_strength": round(strength, 4),
        "learning_failure_risk": round(failure_risk, 4),
        "diagnosis": diagnosis,
        "weakest_dimension": min(
            [
                ("feedback_quality", f(row, "feedback_quality")),
                ("assumption_review", f(row, "assumption_review")),
                ("interpretation_discipline", f(row, "interpretation_discipline")),
                ("decision_authority", f(row, "decision_authority")),
                ("learning_closure", f(row, "learning_closure")),
                ("decision_memory", f(row, "decision_memory")),
                ("psychological_safety", f(row, "psychological_safety")),
                ("knowledge_scaling", f(row, "knowledge_scaling")),
                ("ethical_learning", f(row, "ethical_learning")),
                ("strategic_coherence", f(row, "strategic_coherence")),
                ("adaptive_capacity", f(row, "adaptive_capacity")),
            ],
            key=lambda item: item[1],
        )[0],
        "recommended_action": diagnosis,
        "description": row["description"],
    })

learning_rows.sort(key=lambda item: item["learning_loop_strength"], reverse=True)
write_csv(TABLES / "learning_loop_scores.csv", learning_rows)
write_csv(PROCESSED / "learning_loop_scores.csv", learning_rows)

# ---------------------------------------------------------------------
# 2. Feedback quality
# ---------------------------------------------------------------------

feedback_rows: list[dict[str, object]] = []
for row in feedback:
    quality = (
        0.16 * f(row, "reliability")
        + 0.15 * f(row, "timeliness")
        + 0.16 * f(row, "contextual_relevance")
        + 0.16 * f(row, "validity")
        + 0.13 * f(row, "triangulation")
        + 0.13 * f(row, "stakeholder_coverage")
        - 0.11 * f(row, "noise_risk")
        + 0.11
    )
    feedback_rows.append({
        "feedback_id": row["feedback_id"],
        "context_id": row["context_id"],
        "context_name": names[row["context_id"]],
        "source_type": row["source_type"],
        "feedback_quality_score": round(quality, 4),
        "recommended_action": row["review_action"],
    })

feedback_rows.sort(key=lambda item: item["feedback_quality_score"], reverse=True)
write_csv(TABLES / "feedback_quality_scores.csv", feedback_rows)

# ---------------------------------------------------------------------
# 3. Assumption review
# ---------------------------------------------------------------------

assumption_rows: list[dict[str, object]] = []
for row in assumptions:
    score = (
        0.16 * f(row, "explicitness")
        + 0.18 * f(row, "evidence_linkage")
        + 0.15 * f(row, "review_frequency")
        + 0.14 * f(row, "failure_visibility")
        + 0.20 * f(row, "revision_trigger_quality")
        + 0.17 * f(row, "owner_clarity")
    )
    assumption_rows.append({
        "assumption_id": row["assumption_id"],
        "context_id": row["context_id"],
        "context_name": names[row["context_id"]],
        "assumption_type": row["assumption_type"],
        "assumption_name": row["assumption_name"],
        "assumption_review_score": round(score, 4),
        "recommended_action": row["review_action"],
    })

assumption_rows.sort(key=lambda item: item["assumption_review_score"])
write_csv(TABLES / "assumption_review_scores.csv", assumption_rows)

# ---------------------------------------------------------------------
# 4. Governance learning authority
# ---------------------------------------------------------------------

governance_rows: list[dict[str, object]] = []
for row in governance:
    score = (
        0.11 * f(row, "review_cadence")
        + 0.16 * f(row, "decision_authority")
        + 0.14 * f(row, "resource_reallocation_power")
        + 0.15 * f(row, "revision_trigger_quality")
        + 0.13 * f(row, "stop_rule_quality")
        + 0.10 * f(row, "escalation_clarity")
        + 0.10 * f(row, "lesson_owner_clarity")
        + 0.11 * f(row, "follow_up_discipline")
    )
    governance_rows.append({
        "governance_id": row["governance_id"],
        "context_id": row["context_id"],
        "context_name": names[row["context_id"]],
        "governance_learning_score": round(score, 4),
        "recommended_action": row["review_action"],
    })

governance_rows.sort(key=lambda item: item["governance_learning_score"])
write_csv(TABLES / "governance_learning_scores.csv", governance_rows)

# ---------------------------------------------------------------------
# 5. Knowledge scaling
# ---------------------------------------------------------------------

scaling_rows: list[dict[str, object]] = []
for row in scaling:
    score = (
        0.13 * f(row, "template_quality")
        + 0.13 * f(row, "metadata_quality")
        + 0.13 * f(row, "repository_usability")
        + 0.14 * f(row, "cross_team_reuse")
        + 0.13 * f(row, "portfolio_synthesis")
        + 0.11 * f(row, "onboarding_reuse")
        + 0.12 * f(row, "searchability")
        + 0.11 * f(row, "stewardship")
    )
    scaling_rows.append({
        "scaling_id": row["scaling_id"],
        "context_id": row["context_id"],
        "context_name": names[row["context_id"]],
        "knowledge_scaling_score": round(score, 4),
        "recommended_action": row["review_action"],
    })

scaling_rows.sort(key=lambda item: item["knowledge_scaling_score"])
write_csv(TABLES / "knowledge_scaling_scores.csv", scaling_rows)

# ---------------------------------------------------------------------
# 6. Ethics and power in learning
# ---------------------------------------------------------------------

ethics_rows: list[dict[str, object]] = []
for row in ethics:
    power_risk = (
        0.13 * f(row, "sponsor_power")
        + 0.14 * (1 - f(row, "affected_stakeholder_voice"))
        + 0.13 * (1 - f(row, "frontline_voice"))
        + 0.14 * (1 - f(row, "burden_visibility"))
        + 0.14 * (1 - f(row, "interpretive_power_balance"))
        + 0.11 * (1 - f(row, "redress_quality"))
        + 0.11 * (1 - f(row, "pause_authority"))
        + 0.10 * (1 - f(row, "lesson_return"))
    )
    responsibility = (
        0.15 * f(row, "affected_stakeholder_voice")
        + 0.15 * f(row, "frontline_voice")
        + 0.14 * f(row, "burden_visibility")
        + 0.14 * f(row, "interpretive_power_balance")
        + 0.13 * f(row, "redress_quality")
        + 0.13 * f(row, "pause_authority")
        + 0.11 * f(row, "lesson_return")
        + 0.05 * (1 - f(row, "sponsor_power"))
    )
    ethics_rows.append({
        "ethics_id": row["ethics_id"],
        "context_id": row["context_id"],
        "context_name": names[row["context_id"]],
        "ethical_issue": row["ethical_issue"],
        "learning_power_risk": round(power_risk, 4),
        "responsible_learning_score": round(responsibility, 4),
        "recommended_action": row["review_action"],
    })

ethics_rows.sort(key=lambda item: item["learning_power_risk"], reverse=True)
write_csv(TABLES / "ethics_power_scores.csv", ethics_rows)

summary = {
    "learning_loops": learning_rows,
    "feedback_quality": feedback_rows,
    "assumption_review": assumption_rows,
    "governance_learning": governance_rows,
    "knowledge_scaling": scaling_rows,
    "ethics_power": ethics_rows,
}
(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

report = [
    "# Learning Loops in Strategic Execution Diagnostic Report",
    "",
    "## Executive summary",
    "",
    "This diagnostic evaluates whether execution evidence becomes strategic learning. It reviews feedback quality, assumption review, interpretation discipline, decision authority, learning closure, decision memory, psychological safety, knowledge scaling, ethical learning, strategic coherence, and adaptive capacity.",
    "",
    "## Learning loop strength ranking",
    "",
]
for item in learning_rows:
    report.append(
        f"- **{item['context_id']} — {item['context_name']}**: loop strength {item['learning_loop_strength']}; "
        f"failure risk {item['learning_failure_risk']}; weakest dimension: {item['weakest_dimension']}; "
        f"diagnosis: {item['diagnosis']}."
    )

report.extend(["", "## Feedback quality", ""])
for item in feedback_rows:
    report.append(
        f"- **{item['context_name']} / {item['source_type']}**: feedback quality {item['feedback_quality_score']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Assumption review repair priorities", ""])
for item in assumption_rows:
    report.append(
        f"- **{item['context_name']} / {item['assumption_name']}**: assumption review score {item['assumption_review_score']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Governance learning authority", ""])
for item in governance_rows:
    report.append(
        f"- **{item['context_name']}**: governance learning score {item['governance_learning_score']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Knowledge scaling", ""])
for item in scaling_rows:
    report.append(
        f"- **{item['context_name']}**: knowledge scaling score {item['knowledge_scaling_score']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Ethics and power in learning", ""])
for item in ethics_rows:
    report.append(
        f"- **{item['context_name']}**: learning power risk {item['learning_power_risk']}; responsible learning score {item['responsible_learning_score']}; action: {item['recommended_action']}."
    )

report.extend([
    "",
    "## Professional interpretation",
    "",
    "A learning loop is closed only when evidence changes judgment, decision, action, or memory. Feedback without authority, memory, candor, knowledge scaling, and ethical inclusion creates learning debt. Strong strategic execution systems convert implementation evidence into adaptive coherence rather than drift, rigid persistence, or reporting theater.",
])

(REPORTS / "learning_loop_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

print("Advanced learning loop diagnostics complete.")
print(f"Wrote: {TABLES / 'learning_loop_scores.csv'}")
print(f"Wrote: {TABLES / 'feedback_quality_scores.csv'}")
print(f"Wrote: {TABLES / 'assumption_review_scores.csv'}")
print(f"Wrote: {TABLES / 'governance_learning_scores.csv'}")
print(f"Wrote: {TABLES / 'knowledge_scaling_scores.csv'}")
print(f"Wrote: {TABLES / 'ethics_power_scores.csv'}")
print(f"Wrote: {REPORTS / 'learning_loop_diagnostic_report.md'}")
