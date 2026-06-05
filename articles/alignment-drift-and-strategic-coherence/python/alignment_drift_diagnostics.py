#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Alignment Drift and Strategic Coherence.

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


contexts = read_csv(RAW / "coherence_contexts.csv")
signals = read_csv(RAW / "drift_signals.csv")
resources = read_csv(RAW / "resource_alignment.csv")
metrics = read_csv(RAW / "incentives_metrics.csv")
governance = read_csv(RAW / "governance_reviews.csv")
ethics = read_csv(RAW / "ethics_power.csv")

names = {row["context_id"]: row["context_name"] for row in contexts}

# ---------------------------------------------------------------------
# 1. Strategic coherence and drift risk
# ---------------------------------------------------------------------

coherence_rows: list[dict[str, object]] = []

for row in contexts:
    coherence = (
        0.13 * f(row, "purpose_clarity")
        + 0.12 * f(row, "priority_discipline")
        + 0.11 * f(row, "tradeoff_integrity")
        + 0.12 * f(row, "resource_alignment")
        + 0.12 * f(row, "incentive_fit")
        + 0.10 * f(row, "interpretive_consistency")
        + 0.11 * f(row, "governance_strength")
        + 0.09 * f(row, "feedback_quality")
        + 0.06 * f(row, "decision_memory")
        + 0.07 * f(row, "ethical_coherence")
        + 0.07 * f(row, "adaptive_capacity")
    )
    drift_risk = (
        0.13 * (1 - f(row, "purpose_clarity"))
        + 0.12 * (1 - f(row, "priority_discipline"))
        + 0.11 * (1 - f(row, "tradeoff_integrity"))
        + 0.12 * (1 - f(row, "resource_alignment"))
        + 0.13 * (1 - f(row, "incentive_fit"))
        + 0.10 * (1 - f(row, "interpretive_consistency"))
        + 0.11 * (1 - f(row, "governance_strength"))
        + 0.08 * (1 - f(row, "feedback_quality"))
        + 0.06 * (1 - f(row, "decision_memory"))
        + 0.07 * (1 - f(row, "ethical_coherence"))
        + 0.07 * (1 - f(row, "adaptive_capacity"))
    )

    if drift_risk >= 0.55:
        diagnosis = "high_alignment_drift_risk"
    elif f(row, "incentive_fit") < 0.45:
        diagnosis = "incentive_and_metric_review_required"
    elif f(row, "resource_alignment") < 0.45:
        diagnosis = "resource_alignment_repair_required"
    elif f(row, "ethical_coherence") < 0.45:
        diagnosis = "ethical_coherence_repair_required"
    elif coherence >= 0.74:
        diagnosis = "strong_adaptive_coherence"
    else:
        diagnosis = "targeted_coherence_repair_required"

    coherence_rows.append({
        "context_id": row["context_id"],
        "context_name": row["context_name"],
        "context_type": row["context_type"],
        "strategic_coherence_score": round(coherence, 4),
        "alignment_drift_risk": round(drift_risk, 4),
        "diagnosis": diagnosis,
        "weakest_dimension": min(
            [
                ("purpose_clarity", f(row, "purpose_clarity")),
                ("priority_discipline", f(row, "priority_discipline")),
                ("tradeoff_integrity", f(row, "tradeoff_integrity")),
                ("resource_alignment", f(row, "resource_alignment")),
                ("incentive_fit", f(row, "incentive_fit")),
                ("interpretive_consistency", f(row, "interpretive_consistency")),
                ("governance_strength", f(row, "governance_strength")),
                ("feedback_quality", f(row, "feedback_quality")),
                ("decision_memory", f(row, "decision_memory")),
                ("ethical_coherence", f(row, "ethical_coherence")),
                ("adaptive_capacity", f(row, "adaptive_capacity")),
            ],
            key=lambda item: item[1],
        )[0],
        "recommended_action": diagnosis,
        "description": row["description"],
    })

coherence_rows.sort(key=lambda item: item["strategic_coherence_score"], reverse=True)
write_csv(TABLES / "coherence_scores.csv", coherence_rows)
write_csv(PROCESSED / "coherence_scores.csv", coherence_rows)

# ---------------------------------------------------------------------
# 2. Drift signal risk
# ---------------------------------------------------------------------

signal_rows: list[dict[str, object]] = []
for row in signals:
    risk = (
        0.34 * f(row, "signal_strength")
        + 0.22 * f(row, "correction_difficulty")
        + 0.18 * f(row, "visibility")
        + 0.16 * f(row, "evidence_quality")
        + 0.10
    )
    signal_rows.append({
        "signal_id": row["signal_id"],
        "context_id": row["context_id"],
        "context_name": names[row["context_id"]],
        "signal_type": row["signal_type"],
        "signal_name": row["signal_name"],
        "drift_signal_risk": round(risk, 4),
        "recommended_action": row["review_action"],
    })

signal_rows.sort(key=lambda item: item["drift_signal_risk"], reverse=True)
write_csv(TABLES / "drift_signal_scores.csv", signal_rows)

# ---------------------------------------------------------------------
# 3. Resource alignment
# ---------------------------------------------------------------------

resource_rows: list[dict[str, object]] = []
for row in resources:
    score = (
        0.14 * f(row, "budget_alignment")
        + 0.14 * f(row, "staff_alignment")
        + 0.13 * f(row, "leadership_attention")
        + 0.12 * f(row, "technical_support")
        + 0.13 * f(row, "governance_bandwidth")
        + 0.11 * f(row, "communication_capacity")
        + 0.12 * f(row, "portfolio_focus")
        + 0.11 * f(row, "opportunity_cost_visibility")
    )
    resource_rows.append({
        "resource_id": row["resource_id"],
        "context_id": row["context_id"],
        "context_name": names[row["context_id"]],
        "resource_alignment_score": round(score, 4),
        "recommended_action": row["review_action"],
    })

resource_rows.sort(key=lambda item: item["resource_alignment_score"])
write_csv(TABLES / "resource_alignment_scores.csv", resource_rows)

# ---------------------------------------------------------------------
# 4. Incentive and metric distortion
# ---------------------------------------------------------------------

metric_rows: list[dict[str, object]] = []
for row in metrics:
    metric_integrity = (
        0.18 * f(row, "indicator_fit")
        + 0.18 * f(row, "reward_alignment")
        - 0.15 * f(row, "local_optimization_risk")
        - 0.17 * f(row, "metric_gaming_risk")
        - 0.12 * f(row, "short_termism")
        + 0.14 * f(row, "qualitative_review_strength")
        + 0.14 * f(row, "stakeholder_metric_balance")
        + 0.20
    )
    distortion_risk = (
        0.25 * f(row, "metric_gaming_risk")
        + 0.22 * f(row, "local_optimization_risk")
        + 0.18 * f(row, "short_termism")
        + 0.15 * (1 - f(row, "indicator_fit"))
        + 0.12 * (1 - f(row, "reward_alignment"))
        + 0.08 * (1 - f(row, "stakeholder_metric_balance"))
    )
    metric_rows.append({
        "metric_id": row["metric_id"],
        "context_id": row["context_id"],
        "context_name": names[row["context_id"]],
        "metric_integrity_score": round(metric_integrity, 4),
        "metric_distortion_risk": round(distortion_risk, 4),
        "recommended_action": row["review_action"],
    })

metric_rows.sort(key=lambda item: item["metric_distortion_risk"], reverse=True)
write_csv(TABLES / "incentive_metric_scores.csv", metric_rows)

# ---------------------------------------------------------------------
# 5. Governance strength
# ---------------------------------------------------------------------

governance_rows: list[dict[str, object]] = []
for row in governance:
    score = (
        0.12 * f(row, "review_cadence")
        + 0.16 * f(row, "decision_authority")
        + 0.14 * f(row, "assumption_review")
        + 0.13 * f(row, "tradeoff_review")
        + 0.13 * f(row, "stop_rule_quality")
        + 0.14 * f(row, "resource_reallocation_power")
        + 0.09 * f(row, "escalation_clarity")
        + 0.09 * f(row, "decision_memory_quality")
    )
    governance_rows.append({
        "governance_id": row["governance_id"],
        "context_id": row["context_id"],
        "context_name": names[row["context_id"]],
        "governance_strength_score": round(score, 4),
        "recommended_action": row["review_action"],
    })

governance_rows.sort(key=lambda item: item["governance_strength_score"])
write_csv(TABLES / "governance_strength_scores.csv", governance_rows)

# ---------------------------------------------------------------------
# 6. Ethics and power
# ---------------------------------------------------------------------

ethics_rows: list[dict[str, object]] = []
for row in ethics:
    power_risk = (
        0.13 * f(row, "sponsor_power")
        + 0.16 * (1 - f(row, "affected_stakeholder_voice"))
        + 0.13 * f(row, "benefit_concentration")
        + 0.16 * f(row, "burden_concentration")
        + 0.11 * (1 - f(row, "transparency"))
        + 0.10 * (1 - f(row, "redress_quality"))
        + 0.10 * (1 - f(row, "pause_authority"))
        + 0.11 * (1 - f(row, "long_term_responsibility"))
    )
    responsibility = (
        0.17 * f(row, "affected_stakeholder_voice")
        + 0.15 * f(row, "transparency")
        + 0.15 * f(row, "redress_quality")
        + 0.15 * f(row, "pause_authority")
        + 0.16 * f(row, "long_term_responsibility")
        + 0.11 * (1 - f(row, "benefit_concentration"))
        + 0.11 * (1 - f(row, "burden_concentration"))
    )
    ethics_rows.append({
        "ethics_id": row["ethics_id"],
        "context_id": row["context_id"],
        "context_name": names[row["context_id"]],
        "ethical_issue": row["ethical_issue"],
        "power_risk": round(power_risk, 4),
        "responsibility_score": round(responsibility, 4),
        "recommended_action": row["review_action"],
    })

ethics_rows.sort(key=lambda item: item["power_risk"], reverse=True)
write_csv(TABLES / "ethics_power_scores.csv", ethics_rows)

summary = {
    "coherence": coherence_rows,
    "drift_signals": signal_rows[:12],
    "resources": resource_rows,
    "metrics": metric_rows,
    "governance": governance_rows,
    "ethics": ethics_rows,
}
(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

report = [
    "# Alignment Drift and Strategic Coherence Diagnostic Report",
    "",
    "## Executive summary",
    "",
    "This diagnostic evaluates strategic coherence and alignment drift across purpose continuity, priority discipline, tradeoff integrity, resource alignment, incentive fit, interpretive consistency, governance strength, feedback quality, decision memory, ethical coherence, and adaptive capacity.",
    "",
    "## Strategic coherence ranking",
    "",
]
for item in coherence_rows:
    report.append(
        f"- **{item['context_id']} — {item['context_name']}**: coherence {item['strategic_coherence_score']}; "
        f"drift risk {item['alignment_drift_risk']}; weakest dimension: {item['weakest_dimension']}; "
        f"diagnosis: {item['diagnosis']}."
    )

report.extend(["", "## Highest drift signals", ""])
for item in signal_rows[:10]:
    report.append(
        f"- **{item['context_name']} / {item['signal_name']}**: risk {item['drift_signal_risk']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Resource alignment repair priorities", ""])
for item in resource_rows:
    report.append(
        f"- **{item['context_name']}**: resource alignment {item['resource_alignment_score']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Incentive and metric distortion review", ""])
for item in metric_rows:
    report.append(
        f"- **{item['context_name']}**: metric integrity {item['metric_integrity_score']}; distortion risk {item['metric_distortion_risk']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Governance strength review", ""])
for item in governance_rows:
    report.append(
        f"- **{item['context_name']}**: governance strength {item['governance_strength_score']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Ethics and power review", ""])
for item in ethics_rows:
    report.append(
        f"- **{item['context_name']}**: power risk {item['power_risk']}; responsibility score {item['responsibility_score']}; action: {item['recommended_action']}."
    )

report.extend([
    "",
    "## Professional interpretation",
    "",
    "Alignment drift is not merely schedule variance. It is strategic distance between intended logic and realized action. Coherence is restored by making real choices about purpose, resources, incentives, portfolio focus, governance authority, feedback, decision memory, and ethical responsibility. Adaptive coherence allows the strategy to change without quietly becoming something else.",
])

(REPORTS / "alignment_drift_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

print("Advanced alignment drift and strategic coherence diagnostics complete.")
print(f"Wrote: {TABLES / 'coherence_scores.csv'}")
print(f"Wrote: {TABLES / 'drift_signal_scores.csv'}")
print(f"Wrote: {TABLES / 'resource_alignment_scores.csv'}")
print(f"Wrote: {TABLES / 'incentive_metric_scores.csv'}")
print(f"Wrote: {TABLES / 'governance_strength_scores.csv'}")
print(f"Wrote: {TABLES / 'ethics_power_scores.csv'}")
print(f"Wrote: {REPORTS / 'alignment_drift_diagnostic_report.md'}")
