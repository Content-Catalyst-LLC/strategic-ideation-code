#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Feedback Loops in Design Thinking.

This dependency-light workflow uses only the Python standard library.

It produces:
- feedback system profile scores
- signal quality scores
- interpretation capacity scores
- adjustment pathway scores
- user feedback scores
- temporal learning scores
- systems impact scores
- ethical feedback governance review
- decision linkage scores
- feedback memory scores
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


systems = read_csv(RAW / "feedback_systems.csv")
signals = read_csv(RAW / "signals.csv")
interpretations = read_csv(RAW / "interpretation_capacity.csv")
adjustments = read_csv(RAW / "adjustment_pathways.csv")
user_feedback = read_csv(RAW / "user_feedback.csv")
temporal = read_csv(RAW / "temporal_learning.csv")
impacts = read_csv(RAW / "systems_impact.csv")
ethics = read_csv(RAW / "ethical_governance.csv")
decisions = read_csv(RAW / "decision_linkage.csv")
memory = read_csv(RAW / "feedback_memory.csv")

system_names = {row["system_id"]: row["system_name"] for row in systems}

# ---------------------------------------------------------------------
# 1. Feedback system profile
# ---------------------------------------------------------------------

profile_rows: list[dict[str, object]] = []

for row in systems:
    profile = (
        0.13 * f(row, "signal_quality")
        + 0.13 * f(row, "interpretation_capacity")
        + 0.10 * f(row, "adjustment_speed")
        + 0.13 * f(row, "user_insight_depth")
        + 0.10 * f(row, "stability")
        + 0.11 * f(row, "ethical_integrity")
        + 0.10 * f(row, "systems_awareness")
        + 0.10 * f(row, "decision_linkage")
        + 0.10 * f(row, "learning_memory")
    )

    noisy_churn_risk = (
        0.16 * f(row, "adjustment_speed")
        + 0.15 * (1 - f(row, "signal_quality"))
        + 0.15 * (1 - f(row, "interpretation_capacity"))
        + 0.13 * (1 - f(row, "stability"))
        + 0.12 * (1 - f(row, "systems_awareness"))
        + 0.12 * (1 - f(row, "ethical_integrity"))
        + 0.10 * (1 - f(row, "decision_linkage"))
        + 0.07 * (1 - f(row, "learning_memory"))
    )

    if profile >= 0.68:
        diagnosis = "strong_feedback_learning_system"
    elif noisy_churn_risk >= 0.64:
        diagnosis = "high_noisy_churn_or_feedback_theater_risk"
    elif f(row, "decision_linkage") < 0.40:
        diagnosis = "feedback_not_linked_to_decisions"
    elif f(row, "ethical_integrity") < 0.45:
        diagnosis = "ethical_feedback_governance_gap"
    else:
        diagnosis = "developing_feedback_capability"

    profile_rows.append(
        {
            "system_id": row["system_id"],
            "system_name": row["system_name"],
            "organization_type": row["organization_type"],
            "domain": row["domain"],
            "feedback_profile_score": round(profile, 4),
            "noisy_churn_risk": round(noisy_churn_risk, 4),
            "diagnosis": diagnosis,
            "signal_quality": row["signal_quality"],
            "interpretation_capacity": row["interpretation_capacity"],
            "adjustment_speed": row["adjustment_speed"],
            "user_insight_depth": row["user_insight_depth"],
            "stability": row["stability"],
            "ethical_integrity": row["ethical_integrity"],
            "systems_awareness": row["systems_awareness"],
            "decision_linkage": row["decision_linkage"],
            "learning_memory": row["learning_memory"],
            "description": row["description"],
        }
    )

profile_rows.sort(key=lambda item: item["feedback_profile_score"], reverse=True)

profile_fields = [
    "system_id",
    "system_name",
    "organization_type",
    "domain",
    "feedback_profile_score",
    "noisy_churn_risk",
    "diagnosis",
    "signal_quality",
    "interpretation_capacity",
    "adjustment_speed",
    "user_insight_depth",
    "stability",
    "ethical_integrity",
    "systems_awareness",
    "decision_linkage",
    "learning_memory",
    "description",
]
write_csv(TABLES / "feedback_system_profile_scores.csv", profile_rows, profile_fields)
write_csv(PROCESSED / "feedback_system_profile_scores.csv", profile_rows, profile_fields)

# ---------------------------------------------------------------------
# 2. Signal quality scoring
# ---------------------------------------------------------------------

signal_rows: list[dict[str, object]] = []

for row in signals:
    signal_quality = (
        0.15 * f(row, "relevance")
        + 0.13 * f(row, "timeliness")
        + 0.14 * f(row, "reliability")
        + 0.14 * f(row, "representativeness")
        + 0.13 * f(row, "interpretability")
        + 0.14 * f(row, "behavioral_richness")
        - 0.13 * f(row, "bias_risk")
    )

    if signal_quality >= 0.66:
        action = "strong_signal_for_learning"
    elif f(row, "bias_risk") >= 0.65:
        action = "bias_review_required"
    elif f(row, "behavioral_richness") < 0.40:
        action = "add_behavioral_evidence"
    elif f(row, "representativeness") < 0.40:
        action = "improve_representation"
    else:
        action = "triangulate_signal"

    signal_rows.append(
        {
            "signal_id": row["signal_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "signal_source": row["signal_source"],
            "signal_type": row["signal_type"],
            "signal_quality_score": round(signal_quality, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "relevance": row["relevance"],
            "timeliness": row["timeliness"],
            "reliability": row["reliability"],
            "representativeness": row["representativeness"],
            "interpretability": row["interpretability"],
            "behavioral_richness": row["behavioral_richness"],
            "bias_risk": row["bias_risk"],
        }
    )

signal_rows.sort(key=lambda item: item["signal_quality_score"], reverse=True)
write_csv(TABLES / "signal_quality_scores.csv", signal_rows, list(signal_rows[0].keys()))

# ---------------------------------------------------------------------
# 3. Interpretation capacity scoring
# ---------------------------------------------------------------------

interpretation_rows: list[dict[str, object]] = []

for row in interpretations:
    interpretation_score = (
        0.14 * f(row, "contextual_understanding")
        + 0.13 * f(row, "domain_expertise")
        + 0.15 * f(row, "user_research_capacity")
        + 0.15 * f(row, "systems_thinking_capacity")
        + 0.13 * f(row, "bias_review")
        + 0.15 * f(row, "triangulation_quality")
        + 0.15 * f(row, "decision_relevance")
    )

    if interpretation_score >= 0.72:
        action = "strong_interpretation_capacity"
    elif f(row, "systems_thinking_capacity") < 0.45:
        action = "add_systems_interpretation"
    elif f(row, "bias_review") < 0.45:
        action = "add_bias_review"
    elif f(row, "user_research_capacity") < 0.45:
        action = "add_user_research_capacity"
    else:
        action = "strengthen_interpretation_protocol"

    interpretation_rows.append(
        {
            "interpretation_id": row["interpretation_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "interpretation_practice": row["interpretation_practice"],
            "interpretation_capacity_score": round(interpretation_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "contextual_understanding": row["contextual_understanding"],
            "domain_expertise": row["domain_expertise"],
            "user_research_capacity": row["user_research_capacity"],
            "systems_thinking_capacity": row["systems_thinking_capacity"],
            "bias_review": row["bias_review"],
            "triangulation_quality": row["triangulation_quality"],
            "decision_relevance": row["decision_relevance"],
        }
    )

interpretation_rows.sort(key=lambda item: item["interpretation_capacity_score"], reverse=True)
write_csv(TABLES / "interpretation_capacity_scores.csv", interpretation_rows, list(interpretation_rows[0].keys()))

# ---------------------------------------------------------------------
# 4. Adjustment pathway scoring
# ---------------------------------------------------------------------

adjustment_rows: list[dict[str, object]] = []

for row in adjustments:
    adjustment_score = (
        0.15 * f(row, "decision_authority")
        + 0.12 * f(row, "resource_availability")
        + 0.14 * f(row, "revision_trigger_quality")
        + 0.10 * f(row, "implementation_speed")
        + 0.14 * f(row, "change_traceability")
        + 0.13 * f(row, "stability_protection")
        + 0.12 * f(row, "communication_quality")
    )

    overreaction_risk = (
        0.22 * f(row, "implementation_speed")
        + 0.20 * (1 - f(row, "revision_trigger_quality"))
        + 0.20 * (1 - f(row, "stability_protection"))
        + 0.18 * (1 - f(row, "change_traceability"))
        + 0.20 * (1 - f(row, "decision_authority"))
    )

    if adjustment_score >= 0.70:
        action = "strong_adjustment_pathway"
    elif f(row, "decision_authority") < 0.45:
        action = "connect_to_decision_authority"
    elif f(row, "revision_trigger_quality") < 0.45:
        action = "define_revision_triggers"
    elif overreaction_risk >= 0.68:
        action = "add_stability_and_threshold_rules"
    else:
        action = "strengthen_adjustment_pathway"

    adjustment_rows.append(
        {
            "adjustment_id": row["adjustment_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "adjustment_pathway": row["adjustment_pathway"],
            "adjustment_pathway_score": round(adjustment_score, 4),
            "overreaction_risk": round(overreaction_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "decision_authority": row["decision_authority"],
            "resource_availability": row["resource_availability"],
            "revision_trigger_quality": row["revision_trigger_quality"],
            "implementation_speed": row["implementation_speed"],
            "change_traceability": row["change_traceability"],
            "stability_protection": row["stability_protection"],
            "communication_quality": row["communication_quality"],
        }
    )

adjustment_rows.sort(key=lambda item: item["adjustment_pathway_score"], reverse=True)
write_csv(TABLES / "adjustment_pathway_scores.csv", adjustment_rows, list(adjustment_rows[0].keys()))

# ---------------------------------------------------------------------
# 5. User feedback scoring
# ---------------------------------------------------------------------

user_feedback_rows: list[dict[str, object]] = []

for row in user_feedback:
    feedback_score = (
        0.18 * f(row, "behavioral_signal_strength")
        + 0.14 * f(row, "preference_behavior_alignment")
        + 0.13 * f(row, "nonuser_inclusion")
        + 0.15 * f(row, "accessibility_signal")
        + 0.15 * f(row, "trust_signal")
        + 0.11 * f(row, "workaround_signal")
    )

    if feedback_score >= 0.66:
        action = "strong_user_feedback_signal"
    elif f(row, "nonuser_inclusion") < 0.25:
        action = "include_nonusers_and_abandoners"
    elif f(row, "behavioral_signal_strength") < 0.45:
        action = "observe_behavior_not_only_feedback"
    elif f(row, "accessibility_signal") < 0.45:
        action = "add_accessibility_feedback"
    else:
        action = "strengthen_user_feedback_system"

    user_feedback_rows.append(
        {
            "feedback_id": row["feedback_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "user_group": row["user_group"],
            "observed_behavior": row["observed_behavior"],
            "stated_feedback": row["stated_feedback"],
            "user_feedback_score": round(feedback_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "behavioral_signal_strength": row["behavioral_signal_strength"],
            "preference_behavior_alignment": row["preference_behavior_alignment"],
            "nonuser_inclusion": row["nonuser_inclusion"],
            "accessibility_signal": row["accessibility_signal"],
            "trust_signal": row["trust_signal"],
            "workaround_signal": row["workaround_signal"],
        }
    )

user_feedback_rows.sort(key=lambda item: item["user_feedback_score"], reverse=True)
write_csv(TABLES / "user_feedback_scores.csv", user_feedback_rows, list(user_feedback_rows[0].keys()))

# ---------------------------------------------------------------------
# 6. Temporal learning scoring
# ---------------------------------------------------------------------

temporal_rows: list[dict[str, object]] = []

for row in temporal:
    temporal_score = (
        0.12 * f(row, "early_signal_quality")
        + 0.15 * f(row, "delayed_outcome_tracking")
        + 0.15 * f(row, "pattern_detection")
        + 0.14 * f(row, "drift_detection")
        + 0.14 * f(row, "learning_cadence_quality")
        - 0.12 * f(row, "overreaction_risk")
        + 0.14 * f(row, "revision_timing_quality")
    )

    if temporal_score >= 0.64:
        action = "strong_temporal_learning"
    elif f(row, "delayed_outcome_tracking") < 0.45:
        action = "add_delayed_outcome_tracking"
    elif f(row, "overreaction_risk") >= 0.75:
        action = "reduce_noise_driven_churn"
    elif f(row, "drift_detection") < 0.45:
        action = "add_drift_detection"
    else:
        action = "strengthen_temporal_learning"

    temporal_rows.append(
        {
            "temporal_id": row["temporal_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "temporal_issue": row["temporal_issue"],
            "temporal_learning_score": round(temporal_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "early_signal_quality": row["early_signal_quality"],
            "delayed_outcome_tracking": row["delayed_outcome_tracking"],
            "pattern_detection": row["pattern_detection"],
            "drift_detection": row["drift_detection"],
            "learning_cadence_quality": row["learning_cadence_quality"],
            "overreaction_risk": row["overreaction_risk"],
            "revision_timing_quality": row["revision_timing_quality"],
        }
    )

temporal_rows.sort(key=lambda item: item["temporal_learning_score"], reverse=True)
write_csv(TABLES / "temporal_learning_scores.csv", temporal_rows, list(temporal_rows[0].keys()))

# ---------------------------------------------------------------------
# 7. Systems impact scoring
# ---------------------------------------------------------------------

impact_rows: list[dict[str, object]] = []

for row in impacts:
    systems_risk = (
        0.14 * f(row, "feedback_risk")
        + 0.12 * f(row, "delay_risk")
        + 0.16 * f(row, "burden_shift_risk")
        + 0.16 * f(row, "capacity_risk")
        + 0.12 * f(row, "incentive_risk")
        + 0.14 * f(row, "scale_uncertainty")
        - 0.16 * f(row, "monitoring_quality")
    )

    if systems_risk >= 0.58:
        action = "systems_impact_review_required"
    elif f(row, "burden_shift_risk") >= 0.70:
        action = "burden_shift_review_required"
    elif f(row, "capacity_risk") >= 0.70:
        action = "capacity_review_required"
    elif f(row, "monitoring_quality") < 0.40:
        action = "improve_system_monitoring"
    else:
        action = "monitor_system_effects"

    impact_rows.append(
        {
            "impact_id": row["impact_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "system_issue": row["system_issue"],
            "systems_impact_risk": round(systems_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "feedback_risk": row["feedback_risk"],
            "delay_risk": row["delay_risk"],
            "burden_shift_risk": row["burden_shift_risk"],
            "capacity_risk": row["capacity_risk"],
            "incentive_risk": row["incentive_risk"],
            "scale_uncertainty": row["scale_uncertainty"],
            "monitoring_quality": row["monitoring_quality"],
        }
    )

impact_rows.sort(key=lambda item: item["systems_impact_risk"], reverse=True)
write_csv(TABLES / "systems_impact_scores.csv", impact_rows, list(impact_rows[0].keys()))

# ---------------------------------------------------------------------
# 8. Ethical feedback governance
# ---------------------------------------------------------------------

ethics_rows: list[dict[str, object]] = []

for row in ethics:
    governance_score = (
        0.14 * f(row, "privacy_protection")
        + 0.13 * f(row, "consent_quality")
        + 0.14 * f(row, "accessibility_review")
        + 0.13 * f(row, "burden_review")
        + 0.13 * f(row, "representation_quality")
        + 0.10 * f(row, "redress_path")
        + 0.12 * f(row, "accountability_quality")
        + 0.11 * f(row, "governance_traceability")
    )

    governance_risk = 1 - governance_score

    if governance_score >= 0.78:
        action = "strong_ethical_feedback_governance"
    elif f(row, "accessibility_review") < 0.45:
        action = "add_accessibility_review"
    elif f(row, "representation_quality") < 0.45:
        action = "fix_representation"
    elif f(row, "redress_path") < 0.45:
        action = "define_redress_path"
    elif f(row, "accountability_quality") < 0.45:
        action = "add_accountability_response"
    else:
        action = "strengthen_feedback_governance"

    ethics_rows.append(
        {
            "ethics_id": row["ethics_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "ethical_issue": row["ethical_issue"],
            "ethical_governance_score": round(governance_score, 4),
            "ethical_governance_risk": round(governance_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "privacy_protection": row["privacy_protection"],
            "consent_quality": row["consent_quality"],
            "accessibility_review": row["accessibility_review"],
            "burden_review": row["burden_review"],
            "representation_quality": row["representation_quality"],
            "redress_path": row["redress_path"],
            "accountability_quality": row["accountability_quality"],
            "governance_traceability": row["governance_traceability"],
        }
    )

ethics_rows.sort(key=lambda item: item["ethical_governance_risk"], reverse=True)
write_csv(TABLES / "ethical_feedback_governance.csv", ethics_rows, list(ethics_rows[0].keys()))

# ---------------------------------------------------------------------
# 9. Decision linkage scoring
# ---------------------------------------------------------------------

decision_rows: list[dict[str, object]] = []

for row in decisions:
    decision_score = (
        0.14 * f(row, "evidence_to_decision_clarity")
        + 0.14 * f(row, "authority_connection")
        + 0.11 * f(row, "resource_connection")
        + 0.13 * f(row, "revision_trigger_quality")
        + 0.11 * f(row, "stop_rule_quality")
        + 0.10 * f(row, "scale_rule_quality")
        + 0.13 * f(row, "learning_record_quality")
        + 0.14 * f(row, "implementation_path_quality")
    )

    if decision_score >= 0.72:
        action = "strong_feedback_to_decision_linkage"
    elif f(row, "authority_connection") < 0.45:
        action = "connect_to_decision_authority"
    elif f(row, "revision_trigger_quality") < 0.45:
        action = "define_revision_trigger"
    elif f(row, "learning_record_quality") < 0.45:
        action = "archive_decision_learning"
    else:
        action = "strengthen_decision_linkage"

    decision_rows.append(
        {
            "decision_id": row["decision_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "decision_type": row["decision_type"],
            "decision_linkage_score": round(decision_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "evidence_to_decision_clarity": row["evidence_to_decision_clarity"],
            "authority_connection": row["authority_connection"],
            "resource_connection": row["resource_connection"],
            "revision_trigger_quality": row["revision_trigger_quality"],
            "stop_rule_quality": row["stop_rule_quality"],
            "scale_rule_quality": row["scale_rule_quality"],
            "learning_record_quality": row["learning_record_quality"],
            "implementation_path_quality": row["implementation_path_quality"],
        }
    )

decision_rows.sort(key=lambda item: item["decision_linkage_score"], reverse=True)
write_csv(TABLES / "decision_linkage_scores.csv", decision_rows, list(decision_rows[0].keys()))

# ---------------------------------------------------------------------
# 10. Feedback memory scoring
# ---------------------------------------------------------------------

memory_rows: list[dict[str, object]] = []

for row in memory:
    memory_score = (
        0.13 * f(row, "signal_archive_quality")
        + 0.14 * f(row, "interpretation_record_quality")
        + 0.14 * f(row, "change_record_quality")
        + 0.14 * f(row, "decision_rationale_quality")
        + 0.13 * f(row, "remaining_uncertainty_record")
        + 0.14 * f(row, "accessibility_of_learning")
        + 0.14 * f(row, "reuse_quality")
    )

    if memory_score >= 0.72:
        action = "strong_feedback_memory"
    elif f(row, "decision_rationale_quality") < 0.45:
        action = "document_decision_rationale"
    elif f(row, "change_record_quality") < 0.45:
        action = "document_what_changed"
    elif f(row, "reuse_quality") < 0.45:
        action = "make_learning_reusable"
    else:
        action = "strengthen_feedback_memory"

    memory_rows.append(
        {
            "memory_id": row["memory_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "memory_practice": row["memory_practice"],
            "feedback_memory_score": round(memory_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "signal_archive_quality": row["signal_archive_quality"],
            "interpretation_record_quality": row["interpretation_record_quality"],
            "change_record_quality": row["change_record_quality"],
            "decision_rationale_quality": row["decision_rationale_quality"],
            "remaining_uncertainty_record": row["remaining_uncertainty_record"],
            "accessibility_of_learning": row["accessibility_of_learning"],
            "reuse_quality": row["reuse_quality"],
        }
    )

memory_rows.sort(key=lambda item: item["feedback_memory_score"], reverse=True)
write_csv(TABLES / "feedback_memory_scores.csv", memory_rows, list(memory_rows[0].keys()))

# ---------------------------------------------------------------------
# 11. Strategist report
# ---------------------------------------------------------------------

top_profiles = profile_rows[:5]
highest_churn = sorted(profile_rows, key=lambda item: item["noisy_churn_risk"], reverse=True)[:5]
top_signals = signal_rows[:6]
low_signals = sorted(signal_rows, key=lambda item: item["signal_quality_score"])[:4]
top_interpretation = interpretation_rows[:6]
top_adjustments = adjustment_rows[:6]
top_user_feedback = user_feedback_rows[:6]
top_temporal = temporal_rows[:6]
systems_risks = impact_rows[:6]
ethics_risks = ethics_rows[:6]
top_decisions = decision_rows[:6]
top_memory = memory_rows[:6]

report: list[str] = []
report.append("# Feedback Loops in Design Thinking Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic evaluates feedback loops as strategic learning systems. It assesses signal quality, interpretation capacity, adjustment pathways, "
    "user grounding, temporal learning, systems impact, ethical governance, decision linkage, noisy-churn risk, and feedback memory."
)

report.append("")
report.append("## Strongest feedback systems")
report.append("")
for item in top_profiles:
    report.append(
        f"- **{item['system_id']} — {item['system_name']}**: profile {item['feedback_profile_score']}; "
        f"noisy churn risk {item['noisy_churn_risk']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest noisy-churn or feedback-theater risks")
report.append("")
for item in highest_churn:
    report.append(
        f"- **{item['system_id']} — {item['system_name']}**: noisy churn risk {item['noisy_churn_risk']}; "
        f"diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Strongest signals")
report.append("")
for item in top_signals:
    report.append(
        f"- **{item['signal_id']} — {item['signal_source']}**: "
        f"signal quality {item['signal_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weak signal warnings")
report.append("")
for item in low_signals:
    report.append(
        f"- **{item['signal_id']} — {item['signal_source']}**: "
        f"signal quality {item['signal_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Interpretation capacity")
report.append("")
for item in top_interpretation:
    report.append(
        f"- **{item['interpretation_id']} — {item['interpretation_practice']}**: "
        f"interpretation score {item['interpretation_capacity_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Adjustment pathways")
report.append("")
for item in top_adjustments:
    report.append(
        f"- **{item['adjustment_id']} — {item['adjustment_pathway']}**: "
        f"adjustment score {item['adjustment_pathway_score']}; overreaction risk {item['overreaction_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## User feedback signals")
report.append("")
for item in top_user_feedback:
    report.append(
        f"- **{item['feedback_id']} — {item['user_group']}**: "
        f"user feedback score {item['user_feedback_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Temporal learning")
report.append("")
for item in top_temporal:
    report.append(
        f"- **{item['temporal_id']} — {item['temporal_issue']}**: "
        f"temporal learning {item['temporal_learning_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Systems impact risks")
report.append("")
for item in systems_risks:
    report.append(
        f"- **{item['impact_id']} — {item['system_issue']}**: "
        f"systems risk {item['systems_impact_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Ethical feedback governance risks")
report.append("")
for item in ethics_risks:
    report.append(
        f"- **{item['ethics_id']} — {item['ethical_issue']}**: "
        f"governance risk {item['ethical_governance_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Decision linkage")
report.append("")
for item in top_decisions:
    report.append(
        f"- **{item['decision_id']} — {item['decision_type']}**: "
        f"decision linkage {item['decision_linkage_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Feedback memory")
report.append("")
for item in top_memory:
    report.append(
        f"- **{item['memory_id']} — {item['memory_practice']}**: "
        f"memory score {item['feedback_memory_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "Feedback loops strengthen design thinking when meaningful signals are interpreted well, connected to decision authority, governed ethically, "
    "interpreted systemically, adjusted responsibly, and preserved as institutional memory. Fast feedback without interpretation can create noisy churn; "
    "feedback collection without decision linkage can become performative."
)

(REPORTS / "feedback_loop_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_profiles": top_profiles,
    "highest_churn": highest_churn,
    "top_signals": top_signals,
    "low_signals": low_signals,
    "top_interpretation": top_interpretation,
    "top_adjustments": top_adjustments,
    "top_user_feedback": top_user_feedback,
    "top_temporal": top_temporal,
    "systems_risks": systems_risks,
    "ethics_risks": ethics_risks,
    "top_decisions": top_decisions,
    "top_memory": top_memory,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced feedback-loop diagnostics complete.")
print(f"Wrote: {TABLES / 'feedback_system_profile_scores.csv'}")
print(f"Wrote: {TABLES / 'signal_quality_scores.csv'}")
print(f"Wrote: {TABLES / 'interpretation_capacity_scores.csv'}")
print(f"Wrote: {TABLES / 'adjustment_pathway_scores.csv'}")
print(f"Wrote: {TABLES / 'user_feedback_scores.csv'}")
print(f"Wrote: {TABLES / 'temporal_learning_scores.csv'}")
print(f"Wrote: {TABLES / 'systems_impact_scores.csv'}")
print(f"Wrote: {TABLES / 'ethical_feedback_governance.csv'}")
print(f"Wrote: {TABLES / 'decision_linkage_scores.csv'}")
print(f"Wrote: {TABLES / 'feedback_memory_scores.csv'}")
print(f"Wrote: {REPORTS / 'feedback_loop_diagnostic_report.md'}")
