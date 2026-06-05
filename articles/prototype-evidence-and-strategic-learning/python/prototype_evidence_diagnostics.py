#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Prototype Evidence and Strategic Learning.

This dependency-light workflow uses only the Python standard library.

It produces:
- prototype system profile scores
- assumption-to-evidence scores
- evidence-quality scores
- behavioral observation scores
- context-realism scores
- systems-impact scores
- ethical prototype governance review
- decision-rule scores
- learning-memory scores
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


systems = read_csv(RAW / "prototype_systems.csv")
assumptions = read_csv(RAW / "assumptions.csv")
evidence_records = read_csv(RAW / "evidence_records.csv")
behavior = read_csv(RAW / "behavioral_observations.csv")
context = read_csv(RAW / "context_reviews.csv")
systems_effects = read_csv(RAW / "systems_effects.csv")
ethics = read_csv(RAW / "ethical_reviews.csv")
decisions = read_csv(RAW / "decision_rules.csv")
memory = read_csv(RAW / "learning_memory.csv")

system_names = {row["system_id"]: row["system_name"] for row in systems}

# ---------------------------------------------------------------------
# 1. Prototype learning profile
# ---------------------------------------------------------------------

profile_rows: list[dict[str, object]] = []

for row in systems:
    learning_quality = (
        0.13 * f(row, "assumption_clarity")
        + 0.13 * f(row, "learning_target_fit")
        + 0.15 * f(row, "evidence_quality")
        + 0.13 * f(row, "behavioral_grounding")
        + 0.11 * f(row, "context_realism")
        + 0.11 * f(row, "systems_awareness")
        + 0.11 * f(row, "decision_linkage")
        + 0.07 * f(row, "ethical_review")
        + 0.06 * f(row, "learning_memory")
    )

    validation_theater_risk = (
        0.17 * (1 - f(row, "assumption_clarity"))
        + 0.16 * (1 - f(row, "evidence_quality"))
        + 0.14 * (1 - f(row, "behavioral_grounding"))
        + 0.13 * (1 - f(row, "decision_linkage"))
        + 0.12 * (1 - f(row, "learning_memory"))
        + 0.11 * (1 - f(row, "systems_awareness"))
        + 0.09 * (1 - f(row, "ethical_review"))
        + 0.08 * (1 - f(row, "context_realism"))
    )

    if learning_quality >= 0.72:
        diagnosis = "strong_prototype_learning_system"
    elif validation_theater_risk >= 0.68:
        diagnosis = "high_validation_theater_risk"
    elif f(row, "behavioral_grounding") < 0.36:
        diagnosis = "evidence_lacks_behavioral_grounding"
    elif f(row, "decision_linkage") < 0.40:
        diagnosis = "prototype_evidence_not_linked_to_decisions"
    else:
        diagnosis = "developing_prototype_learning_capability"

    profile_rows.append(
        {
            "system_id": row["system_id"],
            "system_name": row["system_name"],
            "organization_type": row["organization_type"],
            "domain": row["domain"],
            "prototype_learning_quality": round(learning_quality, 4),
            "validation_theater_risk": round(validation_theater_risk, 4),
            "diagnosis": diagnosis,
            "assumption_clarity": row["assumption_clarity"],
            "learning_target_fit": row["learning_target_fit"],
            "evidence_quality": row["evidence_quality"],
            "behavioral_grounding": row["behavioral_grounding"],
            "context_realism": row["context_realism"],
            "systems_awareness": row["systems_awareness"],
            "decision_linkage": row["decision_linkage"],
            "ethical_review": row["ethical_review"],
            "learning_memory": row["learning_memory"],
            "description": row["description"],
        }
    )

profile_rows.sort(key=lambda item: item["prototype_learning_quality"], reverse=True)
write_csv(TABLES / "prototype_system_profile_scores.csv", profile_rows, list(profile_rows[0].keys()))
write_csv(PROCESSED / "prototype_system_profile_scores.csv", profile_rows, list(profile_rows[0].keys()))

# ---------------------------------------------------------------------
# 2. Assumption-to-evidence mapping
# ---------------------------------------------------------------------

assumption_rows: list[dict[str, object]] = []

for row in assumptions:
    criticality = 0.50 * f(row, "uncertainty") + 0.50 * f(row, "consequence")
    test_design_score = (
        0.22 * f(row, "explicitness")
        + 0.24 * f(row, "testability")
        + 0.22 * f(row, "learning_target_clarity")
        + 0.17 * f(row, "evidence_standard_defined")
        + 0.15 * f(row, "decision_rule_defined")
    )

    strategic_priority = criticality * (1 - test_design_score)

    if strategic_priority >= 0.40:
        action = "critical_assumption_needs_better_test_design"
    elif test_design_score >= 0.72:
        action = "strong_assumption_to_evidence_link"
    elif f(row, "testability") < 0.45:
        action = "make_assumption_testable"
    elif f(row, "evidence_standard_defined") < 0.45:
        action = "define_evidence_standard"
    else:
        action = "strengthen_learning_target_and_decision_rule"

    assumption_rows.append(
        {
            "assumption_id": row["assumption_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "assumption": row["assumption"],
            "assumption_type": row["assumption_type"],
            "criticality": round(criticality, 4),
            "test_design_score": round(test_design_score, 4),
            "strategic_priority_gap": round(strategic_priority, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "uncertainty": row["uncertainty"],
            "consequence": row["consequence"],
            "explicitness": row["explicitness"],
            "testability": row["testability"],
            "learning_target_clarity": row["learning_target_clarity"],
            "evidence_standard_defined": row["evidence_standard_defined"],
            "decision_rule_defined": row["decision_rule_defined"],
        }
    )

assumption_rows.sort(key=lambda item: item["strategic_priority_gap"], reverse=True)
write_csv(TABLES / "assumption_evidence_scores.csv", assumption_rows, list(assumption_rows[0].keys()))

# ---------------------------------------------------------------------
# 3. Evidence quality scoring
# ---------------------------------------------------------------------

evidence_rows: list[dict[str, object]] = []

for row in evidence_records:
    quality = (
        0.14 * f(row, "relevance")
        + 0.15 * f(row, "validity")
        + 0.13 * f(row, "context_realism")
        + 0.14 * f(row, "behavioral_richness")
        + 0.12 * f(row, "sample_fit")
        + 0.13 * f(row, "interpretability")
        + 0.11 * f(row, "decision_usefulness")
        + 0.08 * f(row, "limitation_clarity")
    )

    overgeneralization_risk = (
        0.18 * (1 - f(row, "context_realism"))
        + 0.16 * (1 - f(row, "sample_fit"))
        + 0.16 * (1 - f(row, "behavioral_richness"))
        + 0.14 * (1 - f(row, "limitation_clarity"))
        + 0.12 * (1 - f(row, "validity"))
        + 0.12 * (1 - f(row, "decision_usefulness"))
        + 0.12 * (1 - f(row, "interpretability"))
    )

    if quality >= 0.72:
        action = "strong_evidence_quality"
    elif overgeneralization_risk >= 0.65:
        action = "high_overgeneralization_risk"
    elif f(row, "behavioral_richness") < 0.40:
        action = "add_behavioral_evidence"
    elif f(row, "limitation_clarity") < 0.40:
        action = "document_evidence_limits"
    else:
        action = "strengthen_evidence_quality"

    evidence_rows.append(
        {
            "evidence_id": row["evidence_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "prototype_type": row["prototype_type"],
            "evidence_type": row["evidence_type"],
            "evidence_quality_score": round(quality, 4),
            "overgeneralization_risk": round(overgeneralization_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "relevance": row["relevance"],
            "validity": row["validity"],
            "context_realism": row["context_realism"],
            "behavioral_richness": row["behavioral_richness"],
            "sample_fit": row["sample_fit"],
            "interpretability": row["interpretability"],
            "decision_usefulness": row["decision_usefulness"],
            "limitation_clarity": row["limitation_clarity"],
        }
    )

evidence_rows.sort(key=lambda item: item["evidence_quality_score"], reverse=True)
write_csv(TABLES / "evidence_quality_scores.csv", evidence_rows, list(evidence_rows[0].keys()))

# ---------------------------------------------------------------------
# 4. Behavioral observation scoring
# ---------------------------------------------------------------------

behavior_rows: list[dict[str, object]] = []

for row in behavior:
    behavior_score = (
        0.20 * f(row, "behavior_signal_strength")
        + 0.16 * f(row, "preference_behavior_alignment")
        - 0.10 * f(row, "hesitation_signal")
        + 0.12 * f(row, "workaround_signal")
        - 0.14 * f(row, "abandonment_signal")
        + 0.18 * f(row, "commitment_signal")
        - 0.10 * f(row, "burden_signal")
    )

    concern_score = (
        0.18 * f(row, "hesitation_signal")
        + 0.18 * f(row, "workaround_signal")
        + 0.20 * f(row, "abandonment_signal")
        + 0.18 * f(row, "burden_signal")
        + 0.14 * (1 - f(row, "preference_behavior_alignment"))
        + 0.12 * (1 - f(row, "commitment_signal"))
    )

    if concern_score >= 0.62:
        action = "behavioral_concern_requires_revision"
    elif behavior_score >= 0.55:
        action = "behavior_supports_learning_target"
    elif f(row, "commitment_signal") < 0.35:
        action = "test_real_commitment"
    elif f(row, "burden_signal") >= 0.70:
        action = "review_hidden_burden"
    else:
        action = "interpret_behavior_with_context"

    behavior_rows.append(
        {
            "observation_id": row["observation_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "observed_behavior": row["observed_behavior"],
            "stated_feedback": row["stated_feedback"],
            "behavioral_support_score": round(behavior_score, 4),
            "behavioral_concern_score": round(concern_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "behavior_signal_strength": row["behavior_signal_strength"],
            "preference_behavior_alignment": row["preference_behavior_alignment"],
            "hesitation_signal": row["hesitation_signal"],
            "workaround_signal": row["workaround_signal"],
            "abandonment_signal": row["abandonment_signal"],
            "commitment_signal": row["commitment_signal"],
            "burden_signal": row["burden_signal"],
        }
    )

behavior_rows.sort(key=lambda item: item["behavioral_concern_score"], reverse=True)
write_csv(TABLES / "behavioral_observation_scores.csv", behavior_rows, list(behavior_rows[0].keys()))

# ---------------------------------------------------------------------
# 5. Context realism scoring
# ---------------------------------------------------------------------

context_rows: list[dict[str, object]] = []

for row in context:
    realism_score = (
        0.16 * f(row, "realism_of_setting")
        + 0.13 * f(row, "realism_of_incentives")
        + 0.13 * f(row, "realism_of_support")
        + 0.15 * f(row, "realism_of_constraints")
        + 0.14 * f(row, "participant_fit")
        + 0.15 * f(row, "scale_similarity")
        + 0.14 * f(row, "time_horizon_fit")
    )

    if realism_score >= 0.72:
        action = "strong_context_realism"
    elif f(row, "scale_similarity") < 0.40:
        action = "do_not_generalize_to_scale"
    elif f(row, "time_horizon_fit") < 0.40:
        action = "extend_time_horizon"
    elif f(row, "realism_of_constraints") < 0.40:
        action = "test_under_real_constraints"
    else:
        action = "improve_context_realism"

    context_rows.append(
        {
            "context_id": row["context_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "test_context": row["test_context"],
            "context_realism_score": round(realism_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "realism_of_setting": row["realism_of_setting"],
            "realism_of_incentives": row["realism_of_incentives"],
            "realism_of_support": row["realism_of_support"],
            "realism_of_constraints": row["realism_of_constraints"],
            "participant_fit": row["participant_fit"],
            "scale_similarity": row["scale_similarity"],
            "time_horizon_fit": row["time_horizon_fit"],
        }
    )

context_rows.sort(key=lambda item: item["context_realism_score"], reverse=True)
write_csv(TABLES / "context_realism_scores.csv", context_rows, list(context_rows[0].keys()))

# ---------------------------------------------------------------------
# 6. Systems impact scoring
# ---------------------------------------------------------------------

impact_rows: list[dict[str, object]] = []

for row in systems_effects:
    systems_risk = (
        0.14 * f(row, "feedback_loop_risk")
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
            "effect_id": row["effect_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "system_issue": row["system_issue"],
            "systems_impact_risk": round(systems_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "feedback_loop_risk": row["feedback_loop_risk"],
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
# 7. Ethical prototype governance
# ---------------------------------------------------------------------

ethics_rows: list[dict[str, object]] = []

for row in ethics:
    governance_score = (
        0.13 * f(row, "consent_quality")
        + 0.13 * f(row, "privacy_protection")
        + 0.14 * f(row, "accessibility_review")
        + 0.13 * f(row, "burden_review")
        + 0.13 * f(row, "representation_quality")
        + 0.10 * f(row, "redress_path")
        + 0.12 * f(row, "expectation_management")
        + 0.12 * f(row, "accountability_quality")
    )

    governance_risk = 1 - governance_score

    if governance_score >= 0.78:
        action = "strong_ethical_prototype_governance"
    elif f(row, "expectation_management") < 0.45:
        action = "clarify_prototype_status_and_expectations"
    elif f(row, "accessibility_review") < 0.45:
        action = "add_accessibility_review"
    elif f(row, "redress_path") < 0.45:
        action = "define_redress_path"
    else:
        action = "strengthen_ethics_governance"

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
            "consent_quality": row["consent_quality"],
            "privacy_protection": row["privacy_protection"],
            "accessibility_review": row["accessibility_review"],
            "burden_review": row["burden_review"],
            "representation_quality": row["representation_quality"],
            "redress_path": row["redress_path"],
            "expectation_management": row["expectation_management"],
            "accountability_quality": row["accountability_quality"],
        }
    )

ethics_rows.sort(key=lambda item: item["ethical_governance_risk"], reverse=True)
write_csv(TABLES / "ethical_prototype_governance.csv", ethics_rows, list(ethics_rows[0].keys()))

# ---------------------------------------------------------------------
# 8. Decision rule scoring
# ---------------------------------------------------------------------

decision_rows: list[dict[str, object]] = []

for row in decisions:
    decision_score = (
        0.16 * f(row, "evidence_to_decision_clarity")
        + 0.14 * f(row, "threshold_defined")
        + 0.13 * f(row, "stop_rule_quality")
        + 0.13 * f(row, "revise_rule_quality")
        + 0.13 * f(row, "scale_rule_quality")
        + 0.14 * f(row, "resource_connection")
        + 0.17 * f(row, "authority_connection")
    )

    if decision_score >= 0.72:
        action = "strong_decision_rule"
    elif f(row, "evidence_to_decision_clarity") < 0.45:
        action = "connect_evidence_to_decision"
    elif f(row, "stop_rule_quality") < 0.45:
        action = "define_stop_rule"
    elif f(row, "scale_rule_quality") < 0.45:
        action = "define_scale_rule"
    else:
        action = "strengthen_decision_rule"

    decision_rows.append(
        {
            "decision_id": row["decision_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "decision_context": row["decision_context"],
            "decision_rule_score": round(decision_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "evidence_to_decision_clarity": row["evidence_to_decision_clarity"],
            "threshold_defined": row["threshold_defined"],
            "stop_rule_quality": row["stop_rule_quality"],
            "revise_rule_quality": row["revise_rule_quality"],
            "scale_rule_quality": row["scale_rule_quality"],
            "resource_connection": row["resource_connection"],
            "authority_connection": row["authority_connection"],
        }
    )

decision_rows.sort(key=lambda item: item["decision_rule_score"], reverse=True)
write_csv(TABLES / "decision_rule_scores.csv", decision_rows, list(decision_rows[0].keys()))

# ---------------------------------------------------------------------
# 9. Learning memory scoring
# ---------------------------------------------------------------------

memory_rows: list[dict[str, object]] = []

for row in memory:
    memory_score = (
        0.12 * f(row, "assumption_record_quality")
        + 0.12 * f(row, "prototype_description_quality")
        + 0.14 * f(row, "evidence_record_quality")
        + 0.14 * f(row, "interpretation_quality")
        + 0.14 * f(row, "decision_rationale_quality")
        + 0.12 * f(row, "limitation_record_quality")
        + 0.11 * f(row, "remaining_uncertainty_quality")
        + 0.11 * f(row, "reuse_quality")
    )

    if memory_score >= 0.72:
        action = "strong_learning_memory"
    elif f(row, "decision_rationale_quality") < 0.45:
        action = "document_decision_rationale"
    elif f(row, "limitation_record_quality") < 0.45:
        action = "document_evidence_limits"
    elif f(row, "remaining_uncertainty_quality") < 0.45:
        action = "document_remaining_uncertainty"
    else:
        action = "strengthen_learning_memory"

    memory_rows.append(
        {
            "memory_id": row["memory_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "memory_practice": row["memory_practice"],
            "learning_memory_score": round(memory_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "assumption_record_quality": row["assumption_record_quality"],
            "prototype_description_quality": row["prototype_description_quality"],
            "evidence_record_quality": row["evidence_record_quality"],
            "interpretation_quality": row["interpretation_quality"],
            "decision_rationale_quality": row["decision_rationale_quality"],
            "limitation_record_quality": row["limitation_record_quality"],
            "remaining_uncertainty_quality": row["remaining_uncertainty_quality"],
            "reuse_quality": row["reuse_quality"],
        }
    )

memory_rows.sort(key=lambda item: item["learning_memory_score"], reverse=True)
write_csv(TABLES / "learning_memory_scores.csv", memory_rows, list(memory_rows[0].keys()))

# ---------------------------------------------------------------------
# 10. Strategist report
# ---------------------------------------------------------------------

top_profiles = profile_rows[:5]
highest_theater = sorted(profile_rows, key=lambda item: item["validation_theater_risk"], reverse=True)[:5]
critical_assumptions = assumption_rows[:6]
top_evidence = evidence_rows[:6]
weak_evidence = sorted(evidence_rows, key=lambda item: item["evidence_quality_score"])[:4]
behavior_concerns = behavior_rows[:6]
top_context = context_rows[:6]
systems_risks = impact_rows[:6]
ethics_risks = ethics_rows[:6]
top_decisions = decision_rows[:6]
low_decisions = sorted(decision_rows, key=lambda item: item["decision_rule_score"])[:4]
top_memory = memory_rows[:6]
low_memory = sorted(memory_rows, key=lambda item: item["learning_memory_score"])[:4]

report: list[str] = []
report.append("# Prototype Evidence and Strategic Learning Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic evaluates prototypes as strategic learning instruments. It assesses assumption clarity, learning-target fit, evidence quality, "
    "behavioral grounding, context realism, systems awareness, ethical governance, decision rules, validation-theater risk, overgeneralization risk, and learning memory."
)

report.append("")
report.append("## Strongest prototype learning systems")
report.append("")
for item in top_profiles:
    report.append(
        f"- **{item['system_id']} — {item['system_name']}**: learning quality {item['prototype_learning_quality']}; "
        f"validation-theater risk {item['validation_theater_risk']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest validation-theater risks")
report.append("")
for item in highest_theater:
    report.append(
        f"- **{item['system_id']} — {item['system_name']}**: validation-theater risk {item['validation_theater_risk']}; "
        f"diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Critical assumptions needing stronger test design")
report.append("")
for item in critical_assumptions:
    report.append(
        f"- **{item['assumption_id']} — {item['assumption']}**: criticality {item['criticality']}; "
        f"test design {item['test_design_score']}; priority gap {item['strategic_priority_gap']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strongest evidence records")
report.append("")
for item in top_evidence:
    report.append(
        f"- **{item['evidence_id']} — {item['prototype_type']} / {item['evidence_type']}**: "
        f"quality {item['evidence_quality_score']}; overgeneralization risk {item['overgeneralization_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weak evidence warnings")
report.append("")
for item in weak_evidence:
    report.append(
        f"- **{item['evidence_id']} — {item['prototype_type']} / {item['evidence_type']}**: "
        f"quality {item['evidence_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Behavioral observation concerns")
report.append("")
for item in behavior_concerns:
    report.append(
        f"- **{item['observation_id']} — {item['observed_behavior']}**: "
        f"concern {item['behavioral_concern_score']}; support {item['behavioral_support_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Context realism")
report.append("")
for item in top_context:
    report.append(
        f"- **{item['context_id']} — {item['test_context']}**: "
        f"context realism {item['context_realism_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Systems impact risks")
report.append("")
for item in systems_risks:
    report.append(
        f"- **{item['effect_id']} — {item['system_issue']}**: "
        f"systems risk {item['systems_impact_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Ethical prototype governance risks")
report.append("")
for item in ethics_risks:
    report.append(
        f"- **{item['ethics_id']} — {item['ethical_issue']}**: "
        f"governance risk {item['ethical_governance_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strong decision rules")
report.append("")
for item in top_decisions:
    report.append(
        f"- **{item['decision_id']} — {item['decision_context']}**: "
        f"decision rule score {item['decision_rule_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weak decision-rule warnings")
report.append("")
for item in low_decisions:
    report.append(
        f"- **{item['decision_id']} — {item['decision_context']}**: "
        f"decision rule score {item['decision_rule_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Learning memory")
report.append("")
for item in top_memory:
    report.append(
        f"- **{item['memory_id']} — {item['memory_practice']}**: "
        f"memory score {item['learning_memory_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Low learning-memory warnings")
report.append("")
for item in low_memory:
    report.append(
        f"- **{item['memory_id']} — {item['memory_practice']}**: "
        f"memory score {item['learning_memory_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "Prototype evidence strengthens strategy when prototypes are tied to critical assumptions, evidence standards are defined before testing, behavior is observed, "
    "context is realistic, systems effects are interpreted, ethics are governed, and decision rules change action. Prototype evidence becomes weak when prototypes are "
    "used primarily to persuade, validate, or accelerate commitment without documenting what was learned and what uncertainty remains."
)

(REPORTS / "prototype_evidence_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_profiles": top_profiles,
    "highest_theater": highest_theater,
    "critical_assumptions": critical_assumptions,
    "top_evidence": top_evidence,
    "weak_evidence": weak_evidence,
    "behavior_concerns": behavior_concerns,
    "top_context": top_context,
    "systems_risks": systems_risks,
    "ethics_risks": ethics_risks,
    "top_decisions": top_decisions,
    "low_decisions": low_decisions,
    "top_memory": top_memory,
    "low_memory": low_memory,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced prototype evidence and strategic learning diagnostics complete.")
print(f"Wrote: {TABLES / 'prototype_system_profile_scores.csv'}")
print(f"Wrote: {TABLES / 'assumption_evidence_scores.csv'}")
print(f"Wrote: {TABLES / 'evidence_quality_scores.csv'}")
print(f"Wrote: {TABLES / 'behavioral_observation_scores.csv'}")
print(f"Wrote: {TABLES / 'context_realism_scores.csv'}")
print(f"Wrote: {TABLES / 'systems_impact_scores.csv'}")
print(f"Wrote: {TABLES / 'ethical_prototype_governance.csv'}")
print(f"Wrote: {TABLES / 'decision_rule_scores.csv'}")
print(f"Wrote: {TABLES / 'learning_memory_scores.csv'}")
print(f"Wrote: {REPORTS / 'prototype_evidence_diagnostic_report.md'}")
