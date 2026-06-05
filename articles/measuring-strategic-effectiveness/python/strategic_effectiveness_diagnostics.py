#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Measuring Strategic Effectiveness.

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


strategies = read_csv(RAW / "strategies.csv")
indicator_quality = read_csv(RAW / "indicator_quality.csv")
evidence_confidence = read_csv(RAW / "evidence_confidence.csv")
feedback_learning = read_csv(RAW / "feedback_learning.csv")
ethics_power = read_csv(RAW / "ethics_power.csv")

names = {row["strategy_id"]: row["strategy_name"] for row in strategies}

effectiveness_rows: list[dict[str, object]] = []
for row in strategies:
    effectiveness = (
        0.18 * f(row, "performance")
        + 0.14 * f(row, "alignment")
        + 0.15 * f(row, "resilience")
        + 0.15 * f(row, "adaptability")
        + 0.13 * f(row, "impact")
        + 0.10 * f(row, "learning_value")
        + 0.06 * f(row, "evidence_confidence")
        + 0.06 * f(row, "ethical_resilience")
        - 0.05 * f(row, "measurement_burden")
        + 0.08 * f(row, "strategic_fit")
    )
    confidence_adjusted = effectiveness * f(row, "evidence_confidence")
    fragility = (
        0.22 * f(row, "performance")
        + 0.18 * (1 - f(row, "resilience"))
        + 0.18 * (1 - f(row, "adaptability"))
        + 0.14 * (1 - f(row, "alignment"))
        + 0.12 * (1 - f(row, "ethical_resilience"))
        + 0.10 * f(row, "measurement_burden")
        + 0.06 * (1 - f(row, "learning_value"))
    )

    if f(row, "performance") >= 0.80 and (f(row, "resilience") < 0.45 or f(row, "adaptability") < 0.45):
        diagnosis = "high_performance_fragility_review"
    elif f(row, "measurement_burden") >= 0.70:
        diagnosis = "metric_burden_and_gaming_review"
    elif effectiveness >= 0.70:
        diagnosis = "strong_effectiveness_profile"
    elif f(row, "learning_value") >= 0.80:
        diagnosis = "protect_as_learning_strategy"
    else:
        diagnosis = "measurement_and_strategy_review_required"

    effectiveness_rows.append({
        "strategy_id": row["strategy_id"],
        "strategy_name": row["strategy_name"],
        "strategy_type": row["strategy_type"],
        "strategic_effectiveness_score": round(effectiveness, 4),
        "confidence_adjusted_effectiveness": round(confidence_adjusted, 4),
        "fragility_warning_score": round(fragility, 4),
        "diagnosis": diagnosis,
        "weakest_dimension": min(
            [
                ("performance", f(row, "performance")),
                ("alignment", f(row, "alignment")),
                ("resilience", f(row, "resilience")),
                ("adaptability", f(row, "adaptability")),
                ("impact", f(row, "impact")),
                ("learning_value", f(row, "learning_value")),
                ("ethical_resilience", f(row, "ethical_resilience")),
            ],
            key=lambda item: item[1],
        )[0],
        "recommended_action": diagnosis,
    })

effectiveness_rows.sort(key=lambda item: item["strategic_effectiveness_score"], reverse=True)
write_csv(TABLES / "strategic_effectiveness_scores.csv", effectiveness_rows)
write_csv(PROCESSED / "strategic_effectiveness_scores.csv", effectiveness_rows)

indicator_rows: list[dict[str, object]] = []
for row in indicator_quality:
    score = (
        0.16 * f(row, "leading_indicator_quality")
        + 0.14 * f(row, "lagging_indicator_quality")
        + 0.16 * f(row, "balance_quality")
        + 0.14 * f(row, "data_reliability")
        + 0.10 * f(row, "timeliness")
        + 0.12 * f(row, "interpretability")
        - 0.10 * f(row, "behavioral_incentive_risk")
        - 0.08 * f(row, "coverage_gap")
        + 0.10
    )
    metric_risk = (
        0.40 * f(row, "behavioral_incentive_risk")
        + 0.30 * f(row, "coverage_gap")
        + 0.15 * (1 - f(row, "balance_quality"))
        + 0.15 * (1 - f(row, "leading_indicator_quality"))
    )
    indicator_rows.append({
        "indicator_id": row["indicator_id"],
        "strategy_id": row["strategy_id"],
        "strategy_name": names[row["strategy_id"]],
        "indicator_quality_score": round(score, 4),
        "metric_distortion_risk": round(metric_risk, 4),
        "recommended_action": row["review_action"],
    })

indicator_rows.sort(key=lambda item: item["indicator_quality_score"], reverse=True)
write_csv(TABLES / "indicator_quality_scores.csv", indicator_rows)

evidence_rows: list[dict[str, object]] = []
for row in evidence_confidence:
    score = (
        0.14 * f(row, "baseline_quality")
        + 0.14 * f(row, "comparison_quality")
        + 0.16 * f(row, "causal_plausibility")
        + 0.13 * f(row, "data_completeness")
        + 0.13 * f(row, "stakeholder_evidence")
        + 0.12 * f(row, "qualitative_depth")
        + 0.10 * f(row, "uncertainty_tracking")
        + 0.08 * f(row, "decision_use")
    )
    evidence_rows.append({
        "evidence_id": row["evidence_id"],
        "strategy_id": row["strategy_id"],
        "strategy_name": names[row["strategy_id"]],
        "evidence_confidence_score": round(score, 4),
        "recommended_action": row["review_action"],
    })

evidence_rows.sort(key=lambda item: item["evidence_confidence_score"], reverse=True)
write_csv(TABLES / "evidence_confidence_scores.csv", evidence_rows)

feedback_rows: list[dict[str, object]] = []
for row in feedback_learning:
    score = (
        0.12 * f(row, "feedback_frequency")
        + 0.14 * f(row, "assumption_review")
        + 0.14 * f(row, "revision_trigger_quality")
        + 0.13 * f(row, "after_action_learning")
        + 0.13 * f(row, "drift_detection")
        + 0.12 * f(row, "adaptation_authority")
        + 0.11 * f(row, "decision_memory_quality")
        + 0.11 * f(row, "learning_culture")
    )
    feedback_rows.append({
        "feedback_id": row["feedback_id"],
        "strategy_id": row["strategy_id"],
        "strategy_name": names[row["strategy_id"]],
        "feedback_learning_score": round(score, 4),
        "recommended_action": row["review_action"],
    })

feedback_rows.sort(key=lambda item: item["feedback_learning_score"], reverse=True)
write_csv(TABLES / "feedback_learning_scores.csv", feedback_rows)

ethics_rows: list[dict[str, object]] = []
for row in ethics_power:
    power_risk = (
        0.16 * f(row, "sponsor_power")
        + 0.18 * (1 - f(row, "affected_stakeholder_voice"))
        + 0.16 * f(row, "benefit_concentration")
        + 0.18 * f(row, "burden_concentration")
        + 0.12 * (1 - f(row, "measurement_transparency"))
        + 0.10 * (1 - f(row, "redress_quality"))
        + 0.10 * (1 - f(row, "long_term_responsibility"))
    )
    responsibility = (
        0.18 * f(row, "affected_stakeholder_voice")
        + 0.17 * f(row, "measurement_transparency")
        + 0.17 * f(row, "redress_quality")
        + 0.18 * f(row, "long_term_responsibility")
        + 0.15 * (1 - f(row, "benefit_concentration"))
        + 0.15 * (1 - f(row, "burden_concentration"))
    )
    ethics_rows.append({
        "ethics_id": row["ethics_id"],
        "strategy_id": row["strategy_id"],
        "strategy_name": names[row["strategy_id"]],
        "ethical_issue": row["ethical_issue"],
        "power_risk": round(power_risk, 4),
        "responsibility_score": round(responsibility, 4),
        "recommended_action": row["review_action"],
    })

ethics_rows.sort(key=lambda item: item["power_risk"], reverse=True)
write_csv(TABLES / "ethics_power_scores.csv", ethics_rows)

summary = {
    "effectiveness_profiles": effectiveness_rows,
    "indicator_quality": indicator_rows,
    "evidence_confidence": evidence_rows,
    "feedback_learning": feedback_rows,
    "ethics_power": ethics_rows,
}
(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

report = [
    "# Strategic Effectiveness Diagnostic Report",
    "",
    "## Executive summary",
    "",
    "This diagnostic evaluates strategies across performance, alignment, resilience, adaptability, impact, learning, evidence confidence, ethics, indicator quality, feedback, and measurement distortion risk.",
    "",
    "## Strategic effectiveness profiles",
    "",
]
for item in effectiveness_rows:
    report.append(
        f"- **{item['strategy_id']} — {item['strategy_name']}**: effectiveness {item['strategic_effectiveness_score']}; "
        f"confidence-adjusted {item['confidence_adjusted_effectiveness']}; fragility warning {item['fragility_warning_score']}; "
        f"weakest dimension: {item['weakest_dimension']}; diagnosis: {item['diagnosis']}."
    )

report.extend(["", "## Indicator quality and metric risk", ""])
for item in indicator_rows:
    report.append(
        f"- **{item['strategy_name']}**: indicator quality {item['indicator_quality_score']}; "
        f"metric distortion risk {item['metric_distortion_risk']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Evidence confidence", ""])
for item in evidence_rows:
    report.append(
        f"- **{item['strategy_name']}**: evidence confidence {item['evidence_confidence_score']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Feedback and learning", ""])
for item in feedback_rows:
    report.append(
        f"- **{item['strategy_name']}**: feedback-learning score {item['feedback_learning_score']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Ethics and power", ""])
for item in ethics_rows:
    report.append(
        f"- **{item['strategy_name']}**: power risk {item['power_risk']}; responsibility score {item['responsibility_score']}; action: {item['recommended_action']}."
    )

report.extend([
    "",
    "## Professional interpretation",
    "",
    "Strategic effectiveness should not be interpreted from performance alone. Strong measurement systems combine leading and lagging indicators, evidence-confidence review, qualitative stakeholder evidence, feedback loops, causal reasoning, ethics review, and decision pathways that convert measurement into learning and strategic revision.",
])

(REPORTS / "strategic_effectiveness_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

print("Advanced strategic effectiveness diagnostics complete.")
print(f"Wrote: {TABLES / 'strategic_effectiveness_scores.csv'}")
print(f"Wrote: {TABLES / 'indicator_quality_scores.csv'}")
print(f"Wrote: {TABLES / 'evidence_confidence_scores.csv'}")
print(f"Wrote: {TABLES / 'feedback_learning_scores.csv'}")
print(f"Wrote: {TABLES / 'ethics_power_scores.csv'}")
print(f"Wrote: {REPORTS / 'strategic_effectiveness_diagnostic_report.md'}")
