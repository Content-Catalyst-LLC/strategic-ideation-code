#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Opportunity Recognition and Evaluation.

This dependency-light workflow uses only the Python standard library.

It produces:
- opportunity profile scores
- signal quality scores
- capability alignment scores
- timing window scores
- risk and recognition-error scores
- ethics and power scores
- learning pathway scores
- governance review scores
- decision memory scores
- a markdown strategist diagnostic report
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


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def f(row: dict[str, str], key: str) -> float:
    return float(row[key])


opportunities = read_csv(RAW / "opportunities.csv")
signal_quality = read_csv(RAW / "signal_quality.csv")
capability = read_csv(RAW / "capability_alignment.csv")
timing = read_csv(RAW / "timing_windows.csv")
risk_errors = read_csv(RAW / "risk_errors.csv")
ethics_power = read_csv(RAW / "ethics_power.csv")
learning = read_csv(RAW / "learning_pathways.csv")
governance = read_csv(RAW / "governance_review.csv")
memory = read_csv(RAW / "decision_memory.csv")

opportunity_names = {row["opportunity_id"]: row["opportunity_name"] for row in opportunities}

# ---------------------------------------------------------------------
# 1. Opportunity profile scoring
# ---------------------------------------------------------------------

profile_rows: list[dict[str, object]] = []

for row in opportunities:
    profile_score = (
        0.13 * f(row, "signal_strength")
        + 0.14 * f(row, "capability_alignment")
        + 0.12 * f(row, "desirability")
        + 0.12 * f(row, "viability")
        + 0.10 * f(row, "timing")
        + 0.12 * f(row, "learning_value")
        + 0.11 * f(row, "option_value")
        + 0.10 * f(row, "strategic_fit")
        + 0.10 * f(row, "ethical_resilience")
        - 0.14 * f(row, "risk")
    )
    confidence_adjusted = profile_score * f(row, "evidence_confidence")
    risk_adjusted_learning = f(row, "learning_value") + f(row, "option_value") - f(row, "risk")

    if f(row, "risk") >= 0.70 and f(row, "capability_alignment") < 0.50:
        diagnosis = "high_hype_or_false_positive_risk"
    elif f(row, "timing") < 0.45:
        diagnosis = "timing_not_ready"
    elif f(row, "ethical_resilience") >= 0.80:
        diagnosis = "strong_legitimacy_or_resilience_pathway"
    elif f(row, "option_value") >= 0.80:
        diagnosis = "high_option_value"
    elif profile_score >= 0.62:
        diagnosis = "strong_opportunity_candidate"
    else:
        diagnosis = "needs_more_evidence_or_reframing"

    profile_rows.append(
        {
            "opportunity_id": row["opportunity_id"],
            "opportunity_name": row["opportunity_name"],
            "opportunity_type": row["opportunity_type"],
            "profile_score": round(profile_score, 4),
            "confidence_adjusted_score": round(confidence_adjusted, 4),
            "risk_adjusted_learning": round(risk_adjusted_learning, 4),
            "diagnosis": diagnosis,
            "signal_strength": row["signal_strength"],
            "capability_alignment": row["capability_alignment"],
            "desirability": row["desirability"],
            "viability": row["viability"],
            "timing": row["timing"],
            "learning_value": row["learning_value"],
            "option_value": row["option_value"],
            "strategic_fit": row["strategic_fit"],
            "ethical_resilience": row["ethical_resilience"],
            "risk": row["risk"],
            "evidence_confidence": row["evidence_confidence"],
            "description": row["description"],
        }
    )

profile_rows.sort(key=lambda item: item["profile_score"], reverse=True)
write_csv(TABLES / "opportunity_profile_scores.csv", profile_rows, list(profile_rows[0].keys()))
write_csv(PROCESSED / "opportunity_profile_scores.csv", profile_rows, list(profile_rows[0].keys()))

# ---------------------------------------------------------------------
# 2. Signal quality scoring
# ---------------------------------------------------------------------

signal_rows: list[dict[str, object]] = []

for row in signal_quality:
    signal_quality_score = (
        0.18 * f(row, "repeatability")
        + 0.17 * f(row, "independence")
        + 0.16 * f(row, "specificity")
        + 0.16 * f(row, "trend_strength")
        + 0.17 * f(row, "stakeholder_confirmation")
        - 0.08 * f(row, "noise_level")
        - 0.08 * f(row, "hype_level")
    )
    hype_warning = (
        0.35 * f(row, "hype_level")
        + 0.25 * f(row, "noise_level")
        + 0.20 * (1 - f(row, "independence"))
        + 0.20 * (1 - f(row, "specificity"))
    )

    if hype_warning >= 0.62:
        action = "challenge_hype_and_seek_independent_evidence"
    elif signal_quality_score >= 0.62:
        action = "credible_signal_continue_evaluation"
    else:
        action = row["review_action"]

    signal_rows.append(
        {
            "signal_id": row["signal_id"],
            "opportunity_id": row["opportunity_id"],
            "opportunity_name": opportunity_names[row["opportunity_id"]],
            "signal_source": row["signal_source"],
            "signal_quality_score": round(signal_quality_score, 4),
            "hype_warning": round(hype_warning, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
        }
    )

signal_rows.sort(key=lambda item: item["signal_quality_score"], reverse=True)
write_csv(TABLES / "signal_quality_scores.csv", signal_rows, list(signal_rows[0].keys()))

# ---------------------------------------------------------------------
# 3. Capability alignment scoring
# ---------------------------------------------------------------------

capability_rows: list[dict[str, object]] = []

for row in capability:
    capability_score = (
        0.16 * f(row, "skills_fit")
        + 0.15 * f(row, "asset_fit")
        + 0.14 * f(row, "authority_fit")
        + 0.14 * f(row, "partnership_fit")
        + 0.14 * f(row, "governance_fit")
        + 0.14 * f(row, "implementation_capacity")
        + 0.13 * f(row, "credibility_fit")
        - 0.10 * f(row, "capability_gap")
    )

    if f(row, "capability_gap") >= 0.58:
        action = "do_not_scale_until_capability_gap_closes"
    elif capability_score >= 0.66:
        action = "strong_capability_fit"
    else:
        action = row["review_action"]

    capability_rows.append(
        {
            "capability_id": row["capability_id"],
            "opportunity_id": row["opportunity_id"],
            "opportunity_name": opportunity_names[row["opportunity_id"]],
            "capability_score": round(capability_score, 4),
            "capability_gap": row["capability_gap"],
            "recommended_action": action,
            "source_review_action": row["review_action"],
        }
    )

capability_rows.sort(key=lambda item: item["capability_score"], reverse=True)
write_csv(TABLES / "capability_alignment_scores.csv", capability_rows, list(capability_rows[0].keys()))

# ---------------------------------------------------------------------
# 4. Timing window scoring
# ---------------------------------------------------------------------

timing_rows: list[dict[str, object]] = []

for row in timing:
    timing_strength = (
        0.17 * f(row, "readiness")
        + 0.15 * f(row, "momentum")
        + 0.14 * f(row, "window_width")
        + 0.12 * f(row, "urgency")
        + 0.15 * f(row, "ecosystem_maturity")
        + 0.14 * f(row, "policy_timing")
        + 0.07 * f(row, "competitive_pressure")
        - 0.06 * f(row, "option_expiration_risk")
    )
    premature_pressure = (
        0.30 * (1 - f(row, "readiness"))
        + 0.22 * f(row, "competitive_pressure")
        + 0.20 * f(row, "urgency")
        + 0.16 * (1 - f(row, "ecosystem_maturity"))
        + 0.12 * f(row, "option_expiration_risk")
    )

    if f(row, "readiness") < 0.45 and premature_pressure >= 0.62:
        action = "premature_do_not_scale"
    elif timing_strength >= 0.64:
        action = "timely_or_emerging_window"
    else:
        action = row["review_action"]

    timing_rows.append(
        {
            "timing_id": row["timing_id"],
            "opportunity_id": row["opportunity_id"],
            "opportunity_name": opportunity_names[row["opportunity_id"]],
            "timing_strength": round(timing_strength, 4),
            "premature_pressure": round(premature_pressure, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
        }
    )

timing_rows.sort(key=lambda item: item["timing_strength"], reverse=True)
write_csv(TABLES / "timing_window_scores.csv", timing_rows, list(timing_rows[0].keys()))

# ---------------------------------------------------------------------
# 5. False-positive / false-negative risk scoring
# ---------------------------------------------------------------------

risk_rows: list[dict[str, object]] = []

for row in risk_errors:
    false_positive_risk = (
        0.20 * f(row, "false_positive_cost")
        + 0.16 * f(row, "implementation_risk")
        + 0.16 * f(row, "strategic_distraction")
        + 0.16 * f(row, "opportunity_cost")
        + 0.12 * f(row, "ethical_risk")
        + 0.10 * f(row, "reputational_risk")
        + 0.10 * f(row, "uncertainty_level")
    )
    missed_opportunity_risk = (
        0.40 * f(row, "false_negative_cost")
        + 0.18 * (1 - f(row, "implementation_risk"))
        + 0.14 * (1 - f(row, "ethical_risk"))
        + 0.14 * (1 - f(row, "reputational_risk"))
        + 0.14 * f(row, "uncertainty_level")
    )

    if false_positive_risk >= 0.66:
        action = "high_false_positive_review"
    elif missed_opportunity_risk >= 0.66:
        action = "protect_against_false_negative"
    else:
        action = row["review_action"]

    risk_rows.append(
        {
            "risk_id": row["risk_id"],
            "opportunity_id": row["opportunity_id"],
            "opportunity_name": opportunity_names[row["opportunity_id"]],
            "false_positive_risk": round(false_positive_risk, 4),
            "missed_opportunity_risk": round(missed_opportunity_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
        }
    )

risk_rows.sort(key=lambda item: item["false_positive_risk"], reverse=True)
write_csv(TABLES / "risk_and_error_scores.csv", risk_rows, list(risk_rows[0].keys()))

# ---------------------------------------------------------------------
# 6. Ethics and power scoring
# ---------------------------------------------------------------------

ethics_rows: list[dict[str, object]] = []

for row in ethics_power:
    power_risk = (
        0.16 * f(row, "sponsor_power")
        + 0.18 * (1 - f(row, "affected_stakeholder_voice"))
        + 0.16 * f(row, "benefit_concentration")
        + 0.18 * f(row, "burden_concentration")
        + 0.12 * (1 - f(row, "transparency"))
        + 0.10 * (1 - f(row, "redress_quality"))
        + 0.10 * (1 - f(row, "long_term_responsibility"))
    )
    responsibility_score = (
        0.18 * f(row, "affected_stakeholder_voice")
        + 0.17 * f(row, "transparency")
        + 0.17 * f(row, "redress_quality")
        + 0.18 * f(row, "long_term_responsibility")
        + 0.15 * (1 - f(row, "benefit_concentration"))
        + 0.15 * (1 - f(row, "burden_concentration"))
    )

    if power_risk >= 0.62:
        action = "urgent_ethics_and_power_review"
    elif f(row, "affected_stakeholder_voice") < 0.50:
        action = "expand_stakeholder_voice"
    else:
        action = row["review_action"]

    ethics_rows.append(
        {
            "ethics_id": row["ethics_id"],
            "opportunity_id": row["opportunity_id"],
            "opportunity_name": opportunity_names[row["opportunity_id"]],
            "ethical_issue": row["ethical_issue"],
            "power_risk": round(power_risk, 4),
            "responsibility_score": round(responsibility_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
        }
    )

ethics_rows.sort(key=lambda item: item["power_risk"], reverse=True)
write_csv(TABLES / "ethics_power_scores.csv", ethics_rows, list(ethics_rows[0].keys()))

# ---------------------------------------------------------------------
# 7. Learning pathway scoring
# ---------------------------------------------------------------------

learning_rows: list[dict[str, object]] = []

for row in learning:
    learning_pathway_score = (
        0.26 * f(row, "learning_value")
        + 0.22 * f(row, "evidence_threshold")
        + 0.18 * f(row, "stop_rule_quality")
        + 0.14 * (1 - f(row, "test_cost"))
        + 0.20
    )

    if f(row, "stop_rule_quality") < 0.58:
        action = "strengthen_stop_rule"
    elif learning_pathway_score >= 0.70:
        action = "strong_learning_pathway"
    else:
        action = row["review_action"]

    learning_rows.append(
        {
            "learning_id": row["learning_id"],
            "opportunity_id": row["opportunity_id"],
            "opportunity_name": opportunity_names[row["opportunity_id"]],
            "critical_assumption": row["critical_assumption"],
            "smallest_responsible_test": row["smallest_responsible_test"],
            "learning_pathway_score": round(learning_pathway_score, 4),
            "decision_gate": row["decision_gate"],
            "recommended_action": action,
            "source_review_action": row["review_action"],
        }
    )

learning_rows.sort(key=lambda item: item["learning_pathway_score"], reverse=True)
write_csv(TABLES / "learning_pathway_scores.csv", learning_rows, list(learning_rows[0].keys()))

# ---------------------------------------------------------------------
# 8. Governance and decision memory scoring
# ---------------------------------------------------------------------

governance_rows: list[dict[str, object]] = []

for row in governance:
    governance_score = (
        0.12 * f(row, "owner_clarity")
        + 0.12 * f(row, "review_cadence")
        + 0.14 * f(row, "evidence_standard")
        + 0.14 * f(row, "decision_gate_quality")
        + 0.13 * f(row, "stakeholder_voice")
        + 0.13 * f(row, "ethics_review")
        + 0.11 * f(row, "stop_rule_quality")
        + 0.11 * f(row, "decision_memory_quality")
    )

    if governance_score >= 0.68:
        action = "strong_opportunity_governance"
    elif f(row, "decision_gate_quality") < 0.50:
        action = "strengthen_decision_gate"
    elif f(row, "stakeholder_voice") < 0.50:
        action = "increase_stakeholder_voice"
    else:
        action = row["review_action"]

    governance_rows.append(
        {
            "governance_id": row["governance_id"],
            "opportunity_id": row["opportunity_id"],
            "opportunity_name": opportunity_names[row["opportunity_id"]],
            "governance_score": round(governance_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
        }
    )

governance_rows.sort(key=lambda item: item["governance_score"], reverse=True)
write_csv(TABLES / "governance_review_scores.csv", governance_rows, list(governance_rows[0].keys()))

memory_rows: list[dict[str, object]] = []

for row in memory:
    memory_score = (
        0.09 * f(row, "signal_record")
        + 0.09 * f(row, "capability_record")
        + 0.10 * f(row, "assumption_record")
        + 0.10 * f(row, "evidence_record")
        + 0.10 * f(row, "risk_record")
        + 0.11 * f(row, "ethics_record")
        + 0.10 * f(row, "timing_record")
        + 0.11 * f(row, "decision_gate_record")
        + 0.10 * f(row, "revision_trigger_quality")
        + 0.10 * f(row, "reuse_quality")
    )

    if memory_score >= 0.68:
        action = "strong_decision_memory"
    elif f(row, "decision_gate_record") < 0.50:
        action = "document_decision_gate"
    elif f(row, "assumption_record") < 0.50:
        action = "record_assumptions"
    else:
        action = row["review_action"]

    memory_rows.append(
        {
            "memory_id": row["memory_id"],
            "opportunity_id": row["opportunity_id"],
            "opportunity_name": opportunity_names[row["opportunity_id"]],
            "memory_practice": row["memory_practice"],
            "decision_memory_score": round(memory_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
        }
    )

memory_rows.sort(key=lambda item: item["decision_memory_score"], reverse=True)
write_csv(TABLES / "decision_memory_scores.csv", memory_rows, list(memory_rows[0].keys()))

# ---------------------------------------------------------------------
# 9. Strategist report
# ---------------------------------------------------------------------

summary = {
    "highest_profile_scores": profile_rows[:5],
    "highest_signal_quality": signal_rows[:5],
    "capability_gaps": sorted(capability_rows, key=lambda item: float(item["capability_gap"]), reverse=True)[:5],
    "timing_strength": timing_rows[:5],
    "false_positive_warnings": risk_rows[:5],
    "ethics_power_warnings": ethics_rows[:5],
    "learning_pathways": learning_rows[:5],
    "governance": governance_rows[:5],
    "decision_memory": memory_rows[:5],
}
(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

report: list[str] = []
report.append("# Opportunity Recognition and Evaluation Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic evaluates opportunities across profile strength, signal quality, capability alignment, timing, recognition-error risk, ethics and power, learning pathways, governance, and decision memory."
)
report.append("")
report.append("## Strongest opportunity profiles")
report.append("")
for item in profile_rows[:6]:
    report.append(
        f"- **{item['opportunity_id']} — {item['opportunity_name']}**: profile {item['profile_score']}; "
        f"confidence-adjusted {item['confidence_adjusted_score']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Signal quality")
report.append("")
for item in signal_rows[:6]:
    report.append(
        f"- **{item['opportunity_name']}**: signal quality {item['signal_quality_score']}; "
        f"hype warning {item['hype_warning']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Capability alignment")
report.append("")
for item in capability_rows[:6]:
    report.append(
        f"- **{item['opportunity_name']}**: capability score {item['capability_score']}; "
        f"gap {item['capability_gap']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Timing windows")
report.append("")
for item in timing_rows[:6]:
    report.append(
        f"- **{item['opportunity_name']}**: timing strength {item['timing_strength']}; "
        f"premature pressure {item['premature_pressure']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## False-positive and missed-opportunity risks")
report.append("")
for item in risk_rows[:6]:
    report.append(
        f"- **{item['opportunity_name']}**: false-positive risk {item['false_positive_risk']}; "
        f"missed-opportunity risk {item['missed_opportunity_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Ethics and power")
report.append("")
for item in ethics_rows[:6]:
    report.append(
        f"- **{item['opportunity_name']}**: power risk {item['power_risk']}; "
        f"responsibility score {item['responsibility_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Learning pathways")
report.append("")
for item in learning_rows[:6]:
    report.append(
        f"- **{item['opportunity_name']}**: test `{item['smallest_responsible_test']}`; "
        f"learning pathway score {item['learning_pathway_score']}; gate: {item['decision_gate']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Governance")
report.append("")
for item in governance_rows[:6]:
    report.append(
        f"- **{item['opportunity_name']}**: governance score {item['governance_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Decision memory")
report.append("")
for item in memory_rows[:6]:
    report.append(
        f"- **{item['opportunity_name']}**: memory score {item['decision_memory_score']}; "
        f"practice: {item['memory_practice']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "Opportunity recognition becomes strategic when teams separate signal from story, capability from aspiration, timing from urgency, and value creation from ethical responsibility. The strongest opportunity systems protect learning, test assumptions, stage commitment, preserve decision memory, and avoid confusing attractive possibility with strategic readiness."
)

(REPORTS / "opportunity_recognition_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

print("Advanced opportunity recognition diagnostics complete.")
print(f"Wrote: {TABLES / 'opportunity_profile_scores.csv'}")
print(f"Wrote: {TABLES / 'signal_quality_scores.csv'}")
print(f"Wrote: {TABLES / 'capability_alignment_scores.csv'}")
print(f"Wrote: {TABLES / 'timing_window_scores.csv'}")
print(f"Wrote: {TABLES / 'risk_and_error_scores.csv'}")
print(f"Wrote: {TABLES / 'ethics_power_scores.csv'}")
print(f"Wrote: {TABLES / 'learning_pathway_scores.csv'}")
print(f"Wrote: {TABLES / 'governance_review_scores.csv'}")
print(f"Wrote: {TABLES / 'decision_memory_scores.csv'}")
print(f"Wrote: {REPORTS / 'opportunity_recognition_diagnostic_report.md'}")
