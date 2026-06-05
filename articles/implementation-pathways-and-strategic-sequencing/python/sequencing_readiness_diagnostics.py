#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Implementation Pathways and Strategic Sequencing.

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


pathways = read_csv(RAW / "pathways.csv")
dependencies = read_csv(RAW / "dependencies.csv")
capacity = read_csv(RAW / "capacity_load.csv")
timing = read_csv(RAW / "timing_windows.csv")
lockin = read_csv(RAW / "reversibility_lockin.csv")
ethics = read_csv(RAW / "ethics_power.csv")

names = {row["pathway_id"]: row["pathway_name"] for row in pathways}

# ---------------------------------------------------------------------
# 1. Pathway readiness
# ---------------------------------------------------------------------

readiness_rows: list[dict[str, object]] = []

for row in pathways:
    readiness = (
        0.15 * f(row, "capability_readiness")
        + 0.14 * f(row, "evidence_strength")
        + 0.14 * f(row, "governance_readiness")
        + 0.13 * f(row, "legitimacy")
        - 0.10 * f(row, "dependency_load")
        + 0.09 * f(row, "reversibility")
        - 0.09 * f(row, "capacity_demand")
        + 0.07 * f(row, "timing_urgency")
        + 0.11 * f(row, "ethical_resilience")
        + 0.09 * f(row, "feedback_strength")
        + 0.10 * f(row, "strategic_fit")
    )
    premature_risk = (
        0.22 * f(row, "dependency_load")
        + 0.20 * f(row, "capacity_demand")
        + 0.16 * (1 - f(row, "evidence_strength"))
        + 0.14 * (1 - f(row, "governance_readiness"))
        + 0.12 * (1 - f(row, "reversibility"))
        + 0.10 * (1 - f(row, "ethical_resilience"))
        + 0.06 * (1 - f(row, "feedback_strength"))
    )

    if premature_risk >= 0.62:
        diagnosis = "stage_or_delay_before_scaling"
    elif readiness >= 0.62 and f(row, "timing_urgency") >= 0.75:
        diagnosis = "advance_with_controls"
    elif readiness >= 0.62:
        diagnosis = "advance_to_next_stage"
    elif f(row, "evidence_strength") < 0.55:
        diagnosis = "test_before_commitment"
    elif f(row, "governance_readiness") < 0.55:
        diagnosis = "build_governance_first"
    else:
        diagnosis = "build_readiness_first"

    readiness_rows.append({
        "pathway_id": row["pathway_id"],
        "pathway_name": row["pathway_name"],
        "pathway_type": row["pathway_type"],
        "sequencing_readiness_score": round(readiness, 4),
        "premature_commitment_risk": round(premature_risk, 4),
        "diagnosis": diagnosis,
        "weakest_dimension": min(
            [
                ("capability", f(row, "capability_readiness")),
                ("evidence", f(row, "evidence_strength")),
                ("governance", f(row, "governance_readiness")),
                ("legitimacy", f(row, "legitimacy")),
                ("reversibility", f(row, "reversibility")),
                ("ethical_resilience", f(row, "ethical_resilience")),
                ("feedback", f(row, "feedback_strength")),
                ("strategic_fit", f(row, "strategic_fit")),
            ],
            key=lambda item: item[1],
        )[0],
        "recommended_action": diagnosis,
        "description": row["description"],
    })

readiness_rows.sort(key=lambda item: item["sequencing_readiness_score"], reverse=True)
write_csv(TABLES / "pathway_readiness_scores.csv", readiness_rows)
write_csv(PROCESSED / "pathway_readiness_scores.csv", readiness_rows)

# ---------------------------------------------------------------------
# 2. Dependency risk
# ---------------------------------------------------------------------

dependency_rows: list[dict[str, object]] = []
for row in dependencies:
    dependency_risk = (
        0.38 * f(row, "dependency_strength")
        + 0.30 * f(row, "bottleneck_risk")
        + 0.20 * (1 - f(row, "readiness_level"))
        + 0.12 * (1 - f(row, "owner_clarity"))
    )
    dependency_rows.append({
        "dependency_id": row["dependency_id"],
        "pathway_id": row["pathway_id"],
        "pathway_name": names[row["pathway_id"]],
        "dependency_type": row["dependency_type"],
        "dependency_name": row["dependency_name"],
        "dependency_risk_score": round(dependency_risk, 4),
        "recommended_action": row["review_action"],
    })

dependency_rows.sort(key=lambda item: item["dependency_risk_score"], reverse=True)
write_csv(TABLES / "dependency_risk_scores.csv", dependency_rows)

# ---------------------------------------------------------------------
# 3. Capacity load
# ---------------------------------------------------------------------

capacity_rows: list[dict[str, object]] = []
for row in capacity:
    load = (
        0.12 * f(row, "budget_load")
        + 0.14 * f(row, "staff_load")
        + 0.14 * f(row, "technical_load")
        + 0.13 * f(row, "governance_load")
        + 0.12 * f(row, "leadership_attention_load")
        + 0.12 * f(row, "stakeholder_participation_load")
        + 0.11 * f(row, "operational_disruption")
        + 0.12 * (1 - f(row, "absorptive_capacity"))
    )
    if load >= 0.68:
        action = "reduce_scope_or_resequence"
    elif f(row, "absorptive_capacity") < 0.55:
        action = "build_absorptive_capacity"
    else:
        action = row["review_action"]

    capacity_rows.append({
        "capacity_id": row["capacity_id"],
        "pathway_id": row["pathway_id"],
        "pathway_name": names[row["pathway_id"]],
        "capacity_load_score": round(load, 4),
        "absorptive_capacity": row["absorptive_capacity"],
        "recommended_action": action,
        "source_review_action": row["review_action"],
    })

capacity_rows.sort(key=lambda item: item["capacity_load_score"], reverse=True)
write_csv(TABLES / "capacity_load_scores.csv", capacity_rows)

# ---------------------------------------------------------------------
# 4. Timing windows
# ---------------------------------------------------------------------

timing_rows: list[dict[str, object]] = []
for row in timing:
    timing_value = (
        0.20 * f(row, "external_window_strength")
        + 0.18 * f(row, "internal_readiness")
        + 0.16 * f(row, "urgency_quality")
        + 0.14 * f(row, "delay_cost")
        - 0.16 * f(row, "premature_action_risk")
        + 0.10 * f(row, "option_value")
        + 0.06 * f(row, "window_stability")
    )
    urgency_trap = (
        0.45 * f(row, "premature_action_risk")
        + 0.25 * (1 - f(row, "internal_readiness"))
        + 0.15 * f(row, "delay_cost")
        + 0.15 * (1 - f(row, "urgency_quality"))
    )
    timing_rows.append({
        "timing_id": row["timing_id"],
        "pathway_id": row["pathway_id"],
        "pathway_name": names[row["pathway_id"]],
        "timing_window_score": round(timing_value, 4),
        "urgency_trap_risk": round(urgency_trap, 4),
        "recommended_action": row["review_action"],
    })

timing_rows.sort(key=lambda item: item["timing_window_score"], reverse=True)
write_csv(TABLES / "timing_window_scores.csv", timing_rows)

# ---------------------------------------------------------------------
# 5. Reversibility and lock-in
# ---------------------------------------------------------------------

lockin_rows: list[dict[str, object]] = []
for row in lockin:
    lockin_risk = (
        0.16 * f(row, "technical_lockin")
        + 0.15 * f(row, "institutional_lockin")
        + 0.14 * f(row, "political_lockin")
        + 0.12 * f(row, "metric_lockin")
        + 0.13 * f(row, "resource_lockin")
        + 0.12 * f(row, "narrative_lockin")
        + 0.10 * (1 - f(row, "modularity"))
        + 0.08 * (1 - f(row, "exit_rule_quality"))
    )
    reversibility_score = (
        0.45 * f(row, "modularity")
        + 0.35 * f(row, "exit_rule_quality")
        + 0.20 * (1 - lockin_risk)
    )
    lockin_rows.append({
        "lockin_id": row["lockin_id"],
        "pathway_id": row["pathway_id"],
        "pathway_name": names[row["pathway_id"]],
        "lockin_risk_score": round(lockin_risk, 4),
        "reversibility_score": round(reversibility_score, 4),
        "recommended_action": row["review_action"],
    })

lockin_rows.sort(key=lambda item: item["lockin_risk_score"], reverse=True)
write_csv(TABLES / "reversibility_lockin_scores.csv", lockin_rows)

# ---------------------------------------------------------------------
# 6. Ethics and power
# ---------------------------------------------------------------------

ethics_rows: list[dict[str, object]] = []
for row in ethics:
    power_risk = (
        0.13 * f(row, "sponsor_power")
        + 0.15 * (1 - f(row, "affected_stakeholder_voice"))
        + 0.13 * f(row, "benefit_concentration")
        + 0.15 * f(row, "burden_concentration")
        + 0.11 * (1 - f(row, "sequencing_transparency"))
        + 0.10 * (1 - f(row, "redress_quality"))
        + 0.11 * (1 - f(row, "pause_authority"))
        + 0.12 * (1 - f(row, "long_term_responsibility"))
    )
    responsibility = (
        0.16 * f(row, "affected_stakeholder_voice")
        + 0.14 * f(row, "sequencing_transparency")
        + 0.14 * f(row, "redress_quality")
        + 0.14 * f(row, "pause_authority")
        + 0.16 * f(row, "long_term_responsibility")
        + 0.13 * (1 - f(row, "benefit_concentration"))
        + 0.13 * (1 - f(row, "burden_concentration"))
    )
    ethics_rows.append({
        "ethics_id": row["ethics_id"],
        "pathway_id": row["pathway_id"],
        "pathway_name": names[row["pathway_id"]],
        "ethical_issue": row["ethical_issue"],
        "power_risk": round(power_risk, 4),
        "responsibility_score": round(responsibility, 4),
        "recommended_action": row["review_action"],
    })

ethics_rows.sort(key=lambda item: item["power_risk"], reverse=True)
write_csv(TABLES / "ethics_power_scores.csv", ethics_rows)

summary = {
    "pathway_readiness": readiness_rows,
    "dependency_risk": dependency_rows[:12],
    "capacity_load": capacity_rows,
    "timing_windows": timing_rows,
    "reversibility_lockin": lockin_rows,
    "ethics_power": ethics_rows,
}
(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

report = [
    "# Implementation Pathways and Strategic Sequencing Diagnostic Report",
    "",
    "## Executive summary",
    "",
    "This diagnostic evaluates implementation pathways across readiness, evidence, governance, legitimacy, dependency load, reversibility, capacity demand, timing urgency, ethics, feedback strength, strategic fit, lock-in risk, and resequencing conditions.",
    "",
    "## Pathway readiness ranking",
    "",
]
for item in readiness_rows:
    report.append(
        f"- **{item['pathway_id']} — {item['pathway_name']}**: readiness {item['sequencing_readiness_score']}; "
        f"premature commitment risk {item['premature_commitment_risk']}; weakest dimension: {item['weakest_dimension']}; "
        f"diagnosis: {item['diagnosis']}."
    )

report.extend(["", "## Highest dependency risks", ""])
for item in dependency_rows[:10]:
    report.append(
        f"- **{item['pathway_name']} / {item['dependency_name']}**: risk {item['dependency_risk_score']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Capacity load review", ""])
for item in capacity_rows:
    report.append(
        f"- **{item['pathway_name']}**: capacity load {item['capacity_load_score']}; absorptive capacity {item['absorptive_capacity']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Timing window review", ""])
for item in timing_rows:
    report.append(
        f"- **{item['pathway_name']}**: timing score {item['timing_window_score']}; urgency trap risk {item['urgency_trap_risk']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Reversibility and lock-in review", ""])
for item in lockin_rows:
    report.append(
        f"- **{item['pathway_name']}**: lock-in risk {item['lockin_risk_score']}; reversibility {item['reversibility_score']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Ethics and power review", ""])
for item in ethics_rows:
    report.append(
        f"- **{item['pathway_name']}**: power risk {item['power_risk']}; responsibility score {item['responsibility_score']}; action: {item['recommended_action']}."
    )

report.extend([
    "",
    "## Professional interpretation",
    "",
    "Implementation pathways should advance only when readiness, dependency logic, capability, governance, legitimacy, capacity, reversibility, timing, feedback, and ethics support the next commitment. Strong sequencing does not merely create a timeline. It protects strategy from premature scaling, hidden lock-in, implementation overload, urgency traps, and ethically weak ordering of action.",
])

(REPORTS / "sequencing_readiness_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

print("Advanced implementation pathway and sequencing diagnostics complete.")
print(f"Wrote: {TABLES / 'pathway_readiness_scores.csv'}")
print(f"Wrote: {TABLES / 'dependency_risk_scores.csv'}")
print(f"Wrote: {TABLES / 'capacity_load_scores.csv'}")
print(f"Wrote: {TABLES / 'timing_window_scores.csv'}")
print(f"Wrote: {TABLES / 'reversibility_lockin_scores.csv'}")
print(f"Wrote: {TABLES / 'ethics_power_scores.csv'}")
print(f"Wrote: {REPORTS / 'sequencing_readiness_diagnostic_report.md'}")
