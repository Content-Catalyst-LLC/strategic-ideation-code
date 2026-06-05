#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Strategy Implementation and Alignment.

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


profiles = read_csv(RAW / "implementation_profiles.csv")
dimensions = read_csv(RAW / "alignment_dimensions.csv")
ethics = read_csv(RAW / "ethics_power.csv")

names = {row["organization_id"]: row["organization_name"] for row in profiles}

profile_rows: list[dict[str, object]] = []
for row in profiles:
    score = (
        0.12 * f(row, "goal_clarity")
        + 0.15 * f(row, "coordination_quality")
        + 0.12 * f(row, "structural_support")
        + 0.12 * f(row, "cultural_support")
        + 0.13 * f(row, "incentive_alignment")
        + 0.12 * f(row, "resource_sufficiency")
        + 0.11 * f(row, "communication_quality")
        + 0.10 * f(row, "accountability_strength")
        + 0.10 * f(row, "adaptive_execution")
        + 0.08 * f(row, "external_alignment")
        + 0.05 * f(row, "ethical_resilience")
    )
    drift = (
        0.16 * (1 - f(row, "coordination_quality"))
        + 0.14 * (1 - f(row, "cultural_support"))
        + 0.14 * (1 - f(row, "incentive_alignment"))
        + 0.12 * (1 - f(row, "communication_quality"))
        + 0.12 * (1 - f(row, "adaptive_execution"))
        + 0.10 * (1 - f(row, "external_alignment"))
        + 0.10 * (1 - f(row, "accountability_strength"))
        + 0.06 * (1 - f(row, "ethical_resilience"))
        + 0.06 * (1 - f(row, "structural_support"))
    )
    if drift >= 0.58:
        diagnosis = "high_alignment_drift_risk"
    elif f(row, "incentive_alignment") < 0.45:
        diagnosis = "incentive_misalignment"
    elif f(row, "adaptive_execution") < 0.45:
        diagnosis = "low_adaptive_execution"
    elif score >= 0.72:
        diagnosis = "strong_implementation_system"
    elif score >= 0.62:
        diagnosis = "targeted_alignment_repair_needed"
    else:
        diagnosis = "implementation_gap_review_required"

    profile_rows.append({
        "organization_id": row["organization_id"],
        "organization_name": row["organization_name"],
        "organization_type": row["organization_type"],
        "implementation_profile_score": round(score, 4),
        "alignment_drift_risk": round(drift, 4),
        "diagnosis": diagnosis,
        "weakest_core_condition": min(
            [
                ("coordination", f(row, "coordination_quality")),
                ("structure", f(row, "structural_support")),
                ("culture", f(row, "cultural_support")),
                ("incentives", f(row, "incentive_alignment")),
                ("resources", f(row, "resource_sufficiency")),
                ("communication", f(row, "communication_quality")),
                ("accountability", f(row, "accountability_strength")),
                ("adaptation", f(row, "adaptive_execution")),
            ],
            key=lambda item: item[1]
        )[0],
        "recommended_action": diagnosis,
    })

profile_rows.sort(key=lambda item: item["implementation_profile_score"], reverse=True)
write_csv(TABLES / "implementation_profile_scores.csv", profile_rows)
write_csv(PROCESSED / "implementation_profile_scores.csv", profile_rows)

dimension_rows: list[dict[str, object]] = []
dimension_cols = ["translation", "structure", "culture", "incentives", "resources", "coordination", "feedback", "leadership", "governance", "decision_memory", "ethics"]
for row in dimensions:
    scores = {col: f(row, col) for col in dimension_cols}
    avg = sum(scores.values()) / len(scores)
    spread = max(scores.values()) - min(scores.values())
    weakest = min(scores, key=scores.get)
    strongest = max(scores, key=scores.get)
    drift_index = (1 - avg) * 0.65 + spread * 0.35
    dimension_rows.append({
        "dimension_id": row["dimension_id"],
        "organization_id": row["organization_id"],
        "organization_name": names[row["organization_id"]],
        "alignment_system_score": round(avg, 4),
        "alignment_spread": round(spread, 4),
        "alignment_drift_index": round(drift_index, 4),
        "weakest_dimension": weakest,
        "strongest_dimension": strongest,
        "recommended_action": row["review_action"],
    })

dimension_rows.sort(key=lambda item: item["alignment_drift_index"], reverse=True)
write_csv(TABLES / "alignment_dimension_scores.csv", dimension_rows)

ethics_rows: list[dict[str, object]] = []
for row in ethics:
    power_risk = (
        0.16 * f(row, "sponsor_power")
        + 0.18 * (1 - f(row, "affected_stakeholder_voice"))
        + 0.16 * f(row, "benefit_concentration")
        + 0.18 * f(row, "burden_concentration")
        + 0.12 * (1 - f(row, "transparency"))
        + 0.10 * (1 - f(row, "redress_quality"))
        + 0.10 * (1 - f(row, "long_term_responsibility"))
    )
    responsibility = (
        0.18 * f(row, "affected_stakeholder_voice")
        + 0.17 * f(row, "transparency")
        + 0.17 * f(row, "redress_quality")
        + 0.18 * f(row, "long_term_responsibility")
        + 0.15 * (1 - f(row, "benefit_concentration"))
        + 0.15 * (1 - f(row, "burden_concentration"))
    )
    ethics_rows.append({
        "ethics_id": row["ethics_id"],
        "organization_id": row["organization_id"],
        "organization_name": names[row["organization_id"]],
        "ethical_issue": row["ethical_issue"],
        "power_risk": round(power_risk, 4),
        "responsibility_score": round(responsibility, 4),
        "recommended_action": row["review_action"],
    })

ethics_rows.sort(key=lambda item: item["power_risk"], reverse=True)
write_csv(TABLES / "ethics_power_scores.csv", ethics_rows)

summary = {
    "implementation_profiles": profile_rows,
    "alignment_dimensions": dimension_rows,
    "ethics_power": ethics_rows,
}
(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

report = [
    "# Strategy Implementation and Alignment Diagnostic Report",
    "",
    "## Executive summary",
    "",
    "This diagnostic evaluates implementation systems across goal clarity, coordination, structure, culture, incentives, resources, communication, accountability, adaptive execution, external alignment, ethics, and alignment drift.",
    "",
    "## Implementation profile ranking",
    "",
]
for item in profile_rows:
    report.append(
        f"- **{item['organization_id']} — {item['organization_name']}**: "
        f"profile {item['implementation_profile_score']}; drift risk {item['alignment_drift_risk']}; "
        f"weakest condition: {item['weakest_core_condition']}; diagnosis: {item['diagnosis']}."
    )

report.extend(["", "## Alignment drift and dimension review", ""])
for item in dimension_rows:
    report.append(
        f"- **{item['organization_name']}**: alignment score {item['alignment_system_score']}; "
        f"drift index {item['alignment_drift_index']}; weakest dimension: {item['weakest_dimension']}; "
        f"action: {item['recommended_action']}."
    )

report.extend(["", "## Ethics and power review", ""])
for item in ethics_rows:
    report.append(
        f"- **{item['organization_name']}**: power risk {item['power_risk']}; "
        f"responsibility score {item['responsibility_score']}; action: {item['recommended_action']}."
    )

report.extend([
    "",
    "## Professional interpretation",
    "",
    "Implementation becomes strategic when intent is translated into work, structures support coordination, incentives reinforce desired behavior, resources match priorities, culture supports action, feedback loops detect drift, and governance protects both accountability and learning. Alignment should create coherence without becoming rigidity.",
])

(REPORTS / "implementation_alignment_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

print("Advanced implementation and alignment diagnostics complete.")
print(f"Wrote: {TABLES / 'implementation_profile_scores.csv'}")
print(f"Wrote: {TABLES / 'alignment_dimension_scores.csv'}")
print(f"Wrote: {TABLES / 'ethics_power_scores.csv'}")
print(f"Wrote: {REPORTS / 'implementation_alignment_diagnostic_report.md'}")
