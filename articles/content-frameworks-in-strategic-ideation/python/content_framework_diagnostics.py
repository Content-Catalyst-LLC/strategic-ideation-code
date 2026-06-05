#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Content Frameworks in Strategic Ideation.

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


frameworks = read_csv(RAW / "frameworks.csv")
components = read_csv(RAW / "components.csv")
links = read_csv(RAW / "framework_component_links.csv")
decisions = read_csv(RAW / "decision_support.csv")
narratives = read_csv(RAW / "narrative_coherence.csv")
governance = read_csv(RAW / "governance_ethics.csv")

framework_names = {row["framework_id"]: row["framework_name"] for row in frameworks}
component_names = {row["component_id"]: row["component_name"] for row in components}

# ---------------------------------------------------------------------
# 1. Framework strength
# ---------------------------------------------------------------------

framework_rows: list[dict[str, object]] = []

for row in frameworks:
    strength = (
        0.10 * f(row, "structure_quality")
        + 0.10 * f(row, "conceptual_clarity")
        + 0.11 * f(row, "evidence_discipline")
        + 0.10 * f(row, "assumption_visibility")
        + 0.10 * f(row, "narrative_coherence")
        + 0.12 * f(row, "decision_relevance")
        + 0.10 * f(row, "modularity")
        + 0.10 * f(row, "reuse_readiness")
        + 0.08 * f(row, "governance_strength")
        + 0.06 * f(row, "ethical_visibility")
        + 0.03 * f(row, "ai_governance")
    )
    risk = (
        0.10 * (1 - f(row, "structure_quality"))
        + 0.11 * (1 - f(row, "conceptual_clarity"))
        + 0.12 * (1 - f(row, "evidence_discipline"))
        + 0.11 * (1 - f(row, "assumption_visibility"))
        + 0.09 * (1 - f(row, "narrative_coherence"))
        + 0.12 * (1 - f(row, "decision_relevance"))
        + 0.09 * (1 - f(row, "modularity"))
        + 0.09 * (1 - f(row, "reuse_readiness"))
        + 0.08 * (1 - f(row, "governance_strength"))
        + 0.06 * (1 - f(row, "ethical_visibility"))
        + 0.03 * (1 - f(row, "ai_governance"))
    )

    if strength >= 0.74:
        diagnosis = "strong_strategic_content_framework"
    elif f(row, "evidence_discipline") < 0.55:
        diagnosis = "evidence_discipline_gap"
    elif f(row, "decision_relevance") < 0.60:
        diagnosis = "decision_relevance_gap"
    elif f(row, "governance_strength") < 0.55:
        diagnosis = "governance_gap"
    elif f(row, "ethical_visibility") < 0.55:
        diagnosis = "ethical_visibility_review_required"
    elif f(row, "ai_governance") < 0.50 and row["framework_type"] == "ai_assisted":
        diagnosis = "urgent_ai_content_governance_required"
    elif f(row, "conceptual_clarity") < 0.60:
        diagnosis = "conceptual_clarity_gap"
    else:
        diagnosis = "targeted_framework_repair"

    weakest_dimension = min(
        [
            ("structure_quality", f(row, "structure_quality")),
            ("conceptual_clarity", f(row, "conceptual_clarity")),
            ("evidence_discipline", f(row, "evidence_discipline")),
            ("assumption_visibility", f(row, "assumption_visibility")),
            ("narrative_coherence", f(row, "narrative_coherence")),
            ("decision_relevance", f(row, "decision_relevance")),
            ("modularity", f(row, "modularity")),
            ("reuse_readiness", f(row, "reuse_readiness")),
            ("governance_strength", f(row, "governance_strength")),
            ("ethical_visibility", f(row, "ethical_visibility")),
            ("ai_governance", f(row, "ai_governance")),
        ],
        key=lambda item: item[1],
    )[0]

    framework_rows.append({
        "framework_id": row["framework_id"],
        "framework_name": row["framework_name"],
        "framework_type": row["framework_type"],
        "framework_strength": round(strength, 4),
        "framework_risk": round(risk, 4),
        "weakest_dimension": weakest_dimension,
        "diagnosis": diagnosis,
        "description": row["description"],
    })

framework_rows.sort(key=lambda item: item["framework_strength"], reverse=True)
write_csv(TABLES / "framework_scores.csv", framework_rows)
write_csv(PROCESSED / "framework_scores.csv", framework_rows)

# ---------------------------------------------------------------------
# 2. Component reuse value
# ---------------------------------------------------------------------

component_rows: list[dict[str, object]] = []
for row in components:
    value = (
        0.14 * f(row, "clarity")
        + 0.16 * f(row, "requiredness")
        + 0.18 * f(row, "reuse_value")
        + 0.17 * f(row, "decision_value")
        + 0.14 * f(row, "evidence_value")
        - 0.08 * f(row, "maintenance_need")
        + 0.13 * f(row, "ethical_importance")
        + 0.06
    )
    component_rows.append({
        "component_id": row["component_id"],
        "component_name": row["component_name"],
        "component_type": row["component_type"],
        "component_reuse_score": round(value, 4),
        "recommended_action": row["review_action"],
    })

component_rows.sort(key=lambda item: item["component_reuse_score"], reverse=True)
write_csv(TABLES / "component_reuse_scores.csv", component_rows)

# ---------------------------------------------------------------------
# 3. Link quality
# ---------------------------------------------------------------------

link_rows: list[dict[str, object]] = []
for row in links:
    quality = (
        0.30 * f(row, "importance")
        + 0.28 * f(row, "implementation_quality")
        + 0.26 * f(row, "reuse_frequency")
        + 0.16
    )
    link_rows.append({
        "link_id": row["link_id"],
        "framework_id": row["framework_id"],
        "framework_name": framework_names[row["framework_id"]],
        "component_id": row["component_id"],
        "component_name": component_names[row["component_id"]],
        "relationship_type": row["relationship_type"],
        "framework_component_score": round(quality, 4),
        "recommended_action": row["review_action"],
    })

link_rows.sort(key=lambda item: item["framework_component_score"])
write_csv(TABLES / "framework_component_scores.csv", link_rows)

# ---------------------------------------------------------------------
# 4. Decision support
# ---------------------------------------------------------------------

decision_rows: list[dict[str, object]] = []
for row in decisions:
    score = (
        0.12 * f(row, "criteria_visibility")
        + 0.13 * f(row, "evidence_visibility")
        + 0.12 * f(row, "assumption_visibility")
        + 0.13 * f(row, "tradeoff_visibility")
        + 0.11 * f(row, "reversibility_visibility")
        + 0.12 * f(row, "stakeholder_visibility")
        + 0.14 * f(row, "revision_trigger_quality")
        + 0.13 * f(row, "decision_owner_clarity")
    )
    decision_rows.append({
        "decision_id": row["decision_id"],
        "framework_id": row["framework_id"],
        "framework_name": framework_names[row["framework_id"]],
        "decision_type": row["decision_type"],
        "decision_support_score": round(score, 4),
        "recommended_action": row["review_action"],
    })

decision_rows.sort(key=lambda item: item["decision_support_score"])
write_csv(TABLES / "decision_support_scores.csv", decision_rows)

# ---------------------------------------------------------------------
# 5. Narrative coherence
# ---------------------------------------------------------------------

narrative_rows: list[dict[str, object]] = []
for row in narratives:
    score = (
        0.13 * f(row, "problem_clarity")
        + 0.12 * f(row, "stakes_clarity")
        + 0.13 * f(row, "insight_quality")
        + 0.13 * f(row, "direction_clarity")
        + 0.13 * f(row, "mechanism_clarity")
        + 0.13 * f(row, "evidence_integration")
        + 0.12 * f(row, "choice_clarity")
        + 0.11 * f(row, "audience_fit")
    )
    narrative_rows.append({
        "narrative_id": row["narrative_id"],
        "framework_id": row["framework_id"],
        "framework_name": framework_names[row["framework_id"]],
        "narrative_coherence_score": round(score, 4),
        "recommended_action": row["review_action"],
    })

narrative_rows.sort(key=lambda item: item["narrative_coherence_score"])
write_csv(TABLES / "narrative_coherence_scores.csv", narrative_rows)

# ---------------------------------------------------------------------
# 6. Governance and ethics
# ---------------------------------------------------------------------

governance_rows: list[dict[str, object]] = []
for row in governance:
    stewardship = (
        0.13 * f(row, "ownership_clarity")
        + 0.13 * f(row, "version_control")
        + 0.14 * f(row, "quality_standards")
        + 0.10 * f(row, "user_training")
        + 0.11 * f(row, "review_cadence")
        + 0.10 * f(row, "exception_process")
        + 0.10 * f(row, "stakeholder_voice")
        + 0.08 * f(row, "burden_visibility")
        + 0.08 * f(row, "dissent_preservation")
        - 0.03 * f(row, "ethical_risk")
        + 0.06
    )
    ethics_risk = (
        0.20 * f(row, "ethical_risk")
        + 0.14 * (1 - f(row, "stakeholder_voice"))
        + 0.14 * (1 - f(row, "burden_visibility"))
        + 0.14 * (1 - f(row, "dissent_preservation"))
        + 0.12 * (1 - f(row, "quality_standards"))
        + 0.10 * (1 - f(row, "ownership_clarity"))
        + 0.08 * (1 - f(row, "review_cadence"))
        + 0.08 * (1 - f(row, "exception_process"))
    )
    governance_rows.append({
        "governance_id": row["governance_id"],
        "framework_id": row["framework_id"],
        "framework_name": framework_names[row["framework_id"]],
        "framework_stewardship_score": round(stewardship, 4),
        "ethical_framework_risk": round(ethics_risk, 4),
        "recommended_action": row["review_action"],
    })

governance_rows.sort(key=lambda item: item["framework_stewardship_score"])
write_csv(TABLES / "governance_ethics_scores.csv", governance_rows)

summary = {
    "frameworks": framework_rows,
    "components": component_rows,
    "framework_component_links": link_rows,
    "decision_support": decision_rows,
    "narrative_coherence": narrative_rows,
    "governance_ethics": governance_rows,
}
(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

report = [
    "# Content Frameworks in Strategic Ideation Diagnostic Report",
    "",
    "## Executive summary",
    "",
    "This diagnostic evaluates whether strategic content frameworks improve judgment rather than merely standardize presentation. It reviews structure, conceptual clarity, evidence discipline, assumption visibility, narrative coherence, decision relevance, modularity, reuse readiness, governance strength, ethical visibility, and AI governance.",
    "",
    "## Framework strength ranking",
    "",
]
for item in framework_rows:
    report.append(
        f"- **{item['framework_id']} — {item['framework_name']}**: strength {item['framework_strength']}; "
        f"risk {item['framework_risk']}; weakest dimension: {item['weakest_dimension']}; diagnosis: {item['diagnosis']}."
    )

report.extend(["", "## Highest-value reusable components", ""])
for item in component_rows:
    report.append(
        f"- **{item['component_name']}**: reuse score {item['component_reuse_score']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Framework-component repair priorities", ""])
for item in link_rows[:12]:
    report.append(
        f"- **{item['framework_name']} / {item['component_name']}**: link score {item['framework_component_score']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Decision-support review", ""])
for item in decision_rows:
    report.append(
        f"- **{item['framework_name']}** ({item['decision_type']}): decision support {item['decision_support_score']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Narrative coherence review", ""])
for item in narrative_rows:
    report.append(
        f"- **{item['framework_name']}**: narrative coherence {item['narrative_coherence_score']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Governance and ethics review", ""])
for item in governance_rows:
    report.append(
        f"- **{item['framework_name']}**: stewardship {item['framework_stewardship_score']}; ethical risk {item['ethical_framework_risk']}; action: {item['recommended_action']}."
    )

report.extend([
    "",
    "## Professional interpretation",
    "",
    "Content frameworks create value when they improve strategic judgment, not simply when they make content consistent. Strong frameworks clarify content type, conceptual hierarchy, evidence, assumptions, narrative logic, decision relevance, reuse, governance, and ethical visibility. Weak frameworks can produce attractive but unsupported strategy language, over-standardized thinking, missing dissent, or AI-generated ambiguity.",
])

(REPORTS / "content_framework_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

print("Advanced content framework diagnostics complete.")
print(f"Wrote: {TABLES / 'framework_scores.csv'}")
print(f"Wrote: {TABLES / 'component_reuse_scores.csv'}")
print(f"Wrote: {TABLES / 'framework_component_scores.csv'}")
print(f"Wrote: {TABLES / 'decision_support_scores.csv'}")
print(f"Wrote: {TABLES / 'narrative_coherence_scores.csv'}")
print(f"Wrote: {TABLES / 'governance_ethics_scores.csv'}")
print(f"Wrote: {REPORTS / 'content_framework_diagnostic_report.md'}")
