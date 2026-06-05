#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Prototyping and Rapid Experimentation.

This dependency-light workflow uses only the Python standard library.

It produces:
- experimentation profile scores
- assumption priority scores
- prototype fit scores
- experiment quality scores
- evidence quality scores
- user validation scores
- iteration learning scores
- systems impact scores
- ethical governance review
- decision linkage scores
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


systems = read_csv(RAW / "experimentation_systems.csv")
assumptions = read_csv(RAW / "assumptions.csv")
prototypes = read_csv(RAW / "prototypes.csv")
experiments = read_csv(RAW / "experiments.csv")
evidence = read_csv(RAW / "evidence.csv")
validations = read_csv(RAW / "user_validation.csv")
iterations = read_csv(RAW / "iterations.csv")
impacts = read_csv(RAW / "systems_impact.csv")
ethics = read_csv(RAW / "ethical_governance.csv")
decisions = read_csv(RAW / "decision_linkage.csv")

system_names = {row["system_id"]: row["system_name"] for row in systems}
prototype_names = {row["prototype_id"]: row["prototype_name"] for row in prototypes}
experiment_names = {row["experiment_id"]: row["hypothesis"] for row in experiments}

# ---------------------------------------------------------------------
# 1. Experimentation system profile
# ---------------------------------------------------------------------

profile_rows: list[dict[str, object]] = []

for row in systems:
    profile = (
        0.10 * f(row, "speed")
        + 0.09 * f(row, "cost_efficiency")
        + 0.15 * f(row, "insight_depth")
        + 0.12 * f(row, "user_validation")
        + 0.12 * f(row, "assumption_criticality")
        + 0.14 * f(row, "evidence_quality")
        + 0.10 * f(row, "systems_awareness")
        + 0.08 * f(row, "ethical_review")
        + 0.10 * f(row, "decision_linkage")
        + 0.10 * f(row, "learning_memory")
    )

    superficial_testing_risk = (
        0.14 * f(row, "speed")
        + 0.16 * (1 - f(row, "insight_depth"))
        + 0.15 * (1 - f(row, "evidence_quality"))
        + 0.13 * (1 - f(row, "systems_awareness"))
        + 0.13 * (1 - f(row, "ethical_review"))
        + 0.13 * (1 - f(row, "decision_linkage"))
        + 0.09 * (1 - f(row, "assumption_criticality"))
        + 0.07 * (1 - f(row, "learning_memory"))
    )

    if profile >= 0.66:
        diagnosis = "strong_experimentation_learning_system"
    elif superficial_testing_risk >= 0.62:
        diagnosis = "high_superficial_testing_or_prototype_theater_risk"
    elif f(row, "decision_linkage") < 0.42:
        diagnosis = "learning_not_linked_to_decisions"
    elif f(row, "evidence_quality") < 0.45:
        diagnosis = "weak_evidence_quality"
    else:
        diagnosis = "developing_experimentation_capability"

    profile_rows.append(
        {
            "system_id": row["system_id"],
            "system_name": row["system_name"],
            "organization_type": row["organization_type"],
            "domain": row["domain"],
            "experimentation_profile_score": round(profile, 4),
            "superficial_testing_risk": round(superficial_testing_risk, 4),
            "diagnosis": diagnosis,
            "speed": row["speed"],
            "cost_efficiency": row["cost_efficiency"],
            "insight_depth": row["insight_depth"],
            "user_validation": row["user_validation"],
            "assumption_criticality": row["assumption_criticality"],
            "evidence_quality": row["evidence_quality"],
            "systems_awareness": row["systems_awareness"],
            "ethical_review": row["ethical_review"],
            "decision_linkage": row["decision_linkage"],
            "learning_memory": row["learning_memory"],
            "description": row["description"],
        }
    )

profile_rows.sort(key=lambda item: item["experimentation_profile_score"], reverse=True)

profile_fields = [
    "system_id",
    "system_name",
    "organization_type",
    "domain",
    "experimentation_profile_score",
    "superficial_testing_risk",
    "diagnosis",
    "speed",
    "cost_efficiency",
    "insight_depth",
    "user_validation",
    "assumption_criticality",
    "evidence_quality",
    "systems_awareness",
    "ethical_review",
    "decision_linkage",
    "learning_memory",
    "description",
]
write_csv(TABLES / "experimentation_profile_scores.csv", profile_rows, profile_fields)
write_csv(PROCESSED / "experimentation_profile_scores.csv", profile_rows, profile_fields)

# ---------------------------------------------------------------------
# 2. Assumption priority scoring
# ---------------------------------------------------------------------

assumption_rows: list[dict[str, object]] = []

for row in assumptions:
    assumption_priority = (
        0.16 * f(row, "uncertainty")
        + 0.17 * f(row, "strategic_significance")
        + 0.13 * f(row, "reversibility_risk")
        + 0.14 * f(row, "cost_of_error")
        + 0.13 * f(row, "evidence_gap")
        + 0.14 * f(row, "stakeholder_sensitivity")
        + 0.08 * f(row, "testing_feasibility")
    )

    if assumption_priority >= 0.72:
        action = "test_before_commitment"
    elif f(row, "evidence_gap") >= 0.75:
        action = "generate_evidence"
    elif f(row, "stakeholder_sensitivity") >= 0.85:
        action = "ethical_and_stakeholder_review_required"
    elif f(row, "testing_feasibility") < 0.50:
        action = "design_indirect_or_simulated_test"
    else:
        action = "include_in_assumption_map"

    assumption_rows.append(
        {
            "assumption_id": row["assumption_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "assumption_statement": row["assumption_statement"],
            "assumption_type": row["assumption_type"],
            "assumption_priority_score": round(assumption_priority, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "uncertainty": row["uncertainty"],
            "strategic_significance": row["strategic_significance"],
            "reversibility_risk": row["reversibility_risk"],
            "cost_of_error": row["cost_of_error"],
            "evidence_gap": row["evidence_gap"],
            "stakeholder_sensitivity": row["stakeholder_sensitivity"],
            "testing_feasibility": row["testing_feasibility"],
        }
    )

assumption_rows.sort(key=lambda item: item["assumption_priority_score"], reverse=True)
write_csv(TABLES / "assumption_priority_scores.csv", assumption_rows, list(assumption_rows[0].keys()))

# ---------------------------------------------------------------------
# 3. Prototype fit scoring
# ---------------------------------------------------------------------

prototype_rows: list[dict[str, object]] = []

for row in prototypes:
    prototype_fit = (
        0.20 * f(row, "learning_fit")
        - 0.10 * f(row, "cost_to_build")
        + 0.12 * f(row, "speed_to_test")
        + 0.13 * f(row, "reversibility")
        + 0.14 * f(row, "user_context_realism")
        + 0.13 * f(row, "operational_realism")
        + 0.12 * f(row, "systems_visibility")
        + 0.06 * (1 - abs(f(row, "fidelity") - f(row, "learning_fit")))
    )

    if prototype_fit >= 0.66:
        action = "good_fit_for_learning_target"
    elif f(row, "learning_fit") < 0.50:
        action = "refocus_prototype_on_learning_target"
    elif f(row, "cost_to_build") > 0.68 and f(row, "reversibility") < 0.45:
        action = "reduce_fidelity_before_testing"
    elif f(row, "systems_visibility") < 0.35:
        action = "add_systems_interpretation_layer"
    else:
        action = "revise_prototype_fit"

    prototype_rows.append(
        {
            "prototype_id": row["prototype_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "prototype_name": row["prototype_name"],
            "prototype_type": row["prototype_type"],
            "learning_target": row["learning_target"],
            "prototype_fit_score": round(prototype_fit, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "fidelity": row["fidelity"],
            "learning_fit": row["learning_fit"],
            "cost_to_build": row["cost_to_build"],
            "speed_to_test": row["speed_to_test"],
            "reversibility": row["reversibility"],
            "user_context_realism": row["user_context_realism"],
            "operational_realism": row["operational_realism"],
            "systems_visibility": row["systems_visibility"],
        }
    )

prototype_rows.sort(key=lambda item: item["prototype_fit_score"], reverse=True)
write_csv(TABLES / "prototype_fit_scores.csv", prototype_rows, list(prototype_rows[0].keys()))

# ---------------------------------------------------------------------
# 4. Experiment quality scoring
# ---------------------------------------------------------------------

experiment_rows: list[dict[str, object]] = []

for row in experiments:
    experiment_quality = (
        0.15 * f(row, "learning_target_clarity")
        + 0.12 * f(row, "test_condition_quality")
        + 0.15 * f(row, "evidence_standard_quality")
        + 0.12 * f(row, "participant_fit")
        + 0.13 * f(row, "risk_boundary_quality")
        + 0.11 * f(row, "interpretation_limit_clarity")
        + 0.14 * f(row, "decision_rule_quality")
        + 0.08 * f(row, "repeatability")
    )

    if experiment_quality >= 0.74:
        action = "strong_experiment_design"
    elif f(row, "learning_target_clarity") < 0.50:
        action = "clarify_learning_target"
    elif f(row, "evidence_standard_quality") < 0.50:
        action = "define_evidence_standard"
    elif f(row, "decision_rule_quality") < 0.50:
        action = "define_decision_rule"
    elif f(row, "risk_boundary_quality") < 0.50:
        action = "add_risk_boundary"
    else:
        action = "strengthen_experiment_design"

    experiment_rows.append(
        {
            "experiment_id": row["experiment_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "prototype_id": row["prototype_id"],
            "prototype_name": prototype_names.get(row["prototype_id"], row["prototype_id"]),
            "hypothesis": row["hypothesis"],
            "experiment_quality_score": round(experiment_quality, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "learning_target_clarity": row["learning_target_clarity"],
            "test_condition_quality": row["test_condition_quality"],
            "evidence_standard_quality": row["evidence_standard_quality"],
            "participant_fit": row["participant_fit"],
            "risk_boundary_quality": row["risk_boundary_quality"],
            "interpretation_limit_clarity": row["interpretation_limit_clarity"],
            "decision_rule_quality": row["decision_rule_quality"],
            "repeatability": row["repeatability"],
        }
    )

experiment_rows.sort(key=lambda item: item["experiment_quality_score"], reverse=True)
write_csv(TABLES / "experiment_quality_scores.csv", experiment_rows, list(experiment_rows[0].keys()))

# ---------------------------------------------------------------------
# 5. Evidence quality scoring
# ---------------------------------------------------------------------

evidence_rows: list[dict[str, object]] = []

for row in evidence:
    evidence_quality = (
        0.16 * f(row, "relevance")
        + 0.15 * f(row, "validity")
        + 0.13 * f(row, "contextual_realism")
        + 0.14 * f(row, "behavioral_richness")
        + 0.13 * f(row, "interpretability")
        + 0.16 * f(row, "decision_usefulness")
        - 0.13 * f(row, "limitation_severity")
    )

    if evidence_quality >= 0.68:
        action = "decision_relevant_evidence"
    elif f(row, "behavioral_richness") < 0.35:
        action = "add_behavioral_evidence"
    elif f(row, "limitation_severity") >= 0.65:
        action = "do_not_overgeneralize"
    elif f(row, "decision_usefulness") < 0.45:
        action = "connect_evidence_to_decision"
    else:
        action = "strengthen_evidence_quality"

    evidence_rows.append(
        {
            "evidence_id": row["evidence_id"],
            "experiment_id": row["experiment_id"],
            "hypothesis": experiment_names.get(row["experiment_id"], row["experiment_id"]),
            "evidence_type": row["evidence_type"],
            "evidence_quality_score": round(evidence_quality, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "relevance": row["relevance"],
            "validity": row["validity"],
            "contextual_realism": row["contextual_realism"],
            "behavioral_richness": row["behavioral_richness"],
            "interpretability": row["interpretability"],
            "decision_usefulness": row["decision_usefulness"],
            "limitation_severity": row["limitation_severity"],
        }
    )

evidence_rows.sort(key=lambda item: item["evidence_quality_score"], reverse=True)
write_csv(TABLES / "evidence_quality_scores.csv", evidence_rows, list(evidence_rows[0].keys()))

# ---------------------------------------------------------------------
# 6. User validation scoring
# ---------------------------------------------------------------------

validation_rows: list[dict[str, object]] = []

for row in validations:
    validation_quality = (
        0.18 * f(row, "behavioral_signal_strength")
        + 0.14 * f(row, "preference_behavior_alignment")
        + 0.13 * f(row, "nonuser_inclusion")
        + 0.13 * f(row, "accessibility_signal")
        + 0.14 * f(row, "trust_signal")
        + 0.10 * f(row, "workaround_signal")
    )

    if validation_quality >= 0.66:
        action = "strong_user_validation_signal"
    elif f(row, "nonuser_inclusion") < 0.25:
        action = "include_nonusers_or_skeptics"
    elif f(row, "behavioral_signal_strength") < 0.45:
        action = "observe_behavior_not_only_feedback"
    elif f(row, "accessibility_signal") < 0.45:
        action = "add_accessibility_testing"
    else:
        action = "strengthen_user_validation"

    validation_rows.append(
        {
            "validation_id": row["validation_id"],
            "experiment_id": row["experiment_id"],
            "hypothesis": experiment_names.get(row["experiment_id"], row["experiment_id"]),
            "user_group": row["user_group"],
            "observed_behavior": row["observed_behavior"],
            "stated_feedback": row["stated_feedback"],
            "user_validation_score": round(validation_quality, 4),
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

validation_rows.sort(key=lambda item: item["user_validation_score"], reverse=True)
write_csv(TABLES / "user_validation_scores.csv", validation_rows, list(validation_rows[0].keys()))

# ---------------------------------------------------------------------
# 7. Iteration learning scoring
# ---------------------------------------------------------------------

iteration_rows: list[dict[str, object]] = []

for row in iterations:
    iteration_score = (
        0.16 * f(row, "learning_quality")
        + 0.14 * f(row, "change_traceability")
        + 0.14 * f(row, "assumption_revision")
        + 0.12 * f(row, "prototype_revision_quality")
        - 0.12 * f(row, "remaining_uncertainty")
        + 0.14 * f(row, "decision_memory_quality")
        + 0.14 * f(row, "next_test_clarity")
    )

    if iteration_score >= 0.62:
        action = "strong_iteration_learning"
    elif f(row, "change_traceability") < 0.40:
        action = "document_what_changed_and_why"
    elif f(row, "decision_memory_quality") < 0.40:
        action = "archive_learning_record"
    elif f(row, "remaining_uncertainty") >= 0.75:
        action = "redesign_test_for_remaining_uncertainty"
    else:
        action = "strengthen_iteration_discipline"

    iteration_rows.append(
        {
            "iteration_id": row["iteration_id"],
            "experiment_id": row["experiment_id"],
            "hypothesis": experiment_names.get(row["experiment_id"], row["experiment_id"]),
            "iteration_number": row["iteration_number"],
            "iteration_learning_score": round(iteration_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "learning_quality": row["learning_quality"],
            "change_traceability": row["change_traceability"],
            "assumption_revision": row["assumption_revision"],
            "prototype_revision_quality": row["prototype_revision_quality"],
            "remaining_uncertainty": row["remaining_uncertainty"],
            "decision_memory_quality": row["decision_memory_quality"],
            "next_test_clarity": row["next_test_clarity"],
        }
    )

iteration_rows.sort(key=lambda item: item["iteration_learning_score"], reverse=True)
write_csv(TABLES / "iteration_learning_scores.csv", iteration_rows, list(iteration_rows[0].keys()))

# ---------------------------------------------------------------------
# 8. Systems impact scoring
# ---------------------------------------------------------------------

impact_rows: list[dict[str, object]] = []

for row in impacts:
    systems_risk = (
        0.14 * f(row, "feedback_risk")
        + 0.12 * f(row, "delay_risk")
        + 0.16 * f(row, "burden_shift_risk")
        + 0.16 * f(row, "capacity_risk")
        + 0.12 * f(row, "incentive_risk")
        + 0.15 * f(row, "scale_uncertainty")
        - 0.15 * f(row, "monitoring_quality")
    )

    if systems_risk >= 0.58:
        action = "systems_impact_review_required"
    elif f(row, "burden_shift_risk") >= 0.70:
        action = "burden_shift_review_required"
    elif f(row, "capacity_risk") >= 0.80:
        action = "capacity_stress_test_required"
    elif f(row, "scale_uncertainty") >= 0.75:
        action = "scale_readiness_review_required"
    else:
        action = "monitor_system_effects"

    impact_rows.append(
        {
            "impact_id": row["impact_id"],
            "experiment_id": row["experiment_id"],
            "hypothesis": experiment_names.get(row["experiment_id"], row["experiment_id"]),
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
# 9. Ethical governance scoring
# ---------------------------------------------------------------------

ethics_rows: list[dict[str, object]] = []

for row in ethics:
    governance_score = (
        0.14 * f(row, "participant_risk_review")
        + 0.13 * f(row, "consent_quality")
        + 0.13 * f(row, "privacy_protection")
        + 0.14 * f(row, "accessibility_review")
        + 0.13 * f(row, "burden_review")
        + 0.12 * f(row, "representation_quality")
        + 0.10 * f(row, "redress_path")
        + 0.11 * f(row, "governance_traceability")
    )

    governance_risk = 1 - governance_score

    if governance_score >= 0.78:
        action = "strong_ethical_governance"
    elif f(row, "representation_quality") < 0.40:
        action = "fix_representation"
    elif f(row, "accessibility_review") < 0.45:
        action = "add_accessibility_review"
    elif f(row, "redress_path") < 0.45:
        action = "define_redress_path"
    elif f(row, "governance_traceability") < 0.45:
        action = "add_governance_traceability"
    else:
        action = "strengthen_governance"

    ethics_rows.append(
        {
            "ethics_id": row["ethics_id"],
            "experiment_id": row["experiment_id"],
            "hypothesis": experiment_names.get(row["experiment_id"], row["experiment_id"]),
            "ethical_issue": row["ethical_issue"],
            "ethical_governance_score": round(governance_score, 4),
            "ethical_governance_risk": round(governance_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "participant_risk_review": row["participant_risk_review"],
            "consent_quality": row["consent_quality"],
            "privacy_protection": row["privacy_protection"],
            "accessibility_review": row["accessibility_review"],
            "burden_review": row["burden_review"],
            "representation_quality": row["representation_quality"],
            "redress_path": row["redress_path"],
            "governance_traceability": row["governance_traceability"],
        }
    )

ethics_rows.sort(key=lambda item: item["ethical_governance_risk"], reverse=True)
write_csv(TABLES / "ethical_governance_review.csv", ethics_rows, list(ethics_rows[0].keys()))

# ---------------------------------------------------------------------
# 10. Decision linkage scoring
# ---------------------------------------------------------------------

decision_rows: list[dict[str, object]] = []

for row in decisions:
    decision_score = (
        0.14 * f(row, "evidence_to_decision_clarity")
        + 0.14 * f(row, "authority_connection")
        + 0.11 * f(row, "resource_connection")
        + 0.12 * f(row, "stop_rule_quality")
        + 0.12 * f(row, "scale_rule_quality")
        + 0.13 * f(row, "revision_trigger_quality")
        + 0.12 * f(row, "learning_record_quality")
        + 0.12 * f(row, "implementation_path_quality")
    )

    if decision_score >= 0.72:
        action = "strong_evidence_to_decision_linkage"
    elif f(row, "authority_connection") < 0.45:
        action = "connect_to_decision_authority"
    elif f(row, "stop_rule_quality") < 0.45:
        action = "define_stop_rule"
    elif f(row, "scale_rule_quality") < 0.45:
        action = "define_scale_rule"
    elif f(row, "learning_record_quality") < 0.45:
        action = "archive_decision_learning_record"
    else:
        action = "strengthen_decision_linkage"

    decision_rows.append(
        {
            "decision_id": row["decision_id"],
            "experiment_id": row["experiment_id"],
            "hypothesis": experiment_names.get(row["experiment_id"], row["experiment_id"]),
            "decision_type": row["decision_type"],
            "decision_linkage_score": round(decision_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "evidence_to_decision_clarity": row["evidence_to_decision_clarity"],
            "authority_connection": row["authority_connection"],
            "resource_connection": row["resource_connection"],
            "stop_rule_quality": row["stop_rule_quality"],
            "scale_rule_quality": row["scale_rule_quality"],
            "revision_trigger_quality": row["revision_trigger_quality"],
            "learning_record_quality": row["learning_record_quality"],
            "implementation_path_quality": row["implementation_path_quality"],
        }
    )

decision_rows.sort(key=lambda item: item["decision_linkage_score"], reverse=True)
write_csv(TABLES / "decision_linkage_scores.csv", decision_rows, list(decision_rows[0].keys()))

# ---------------------------------------------------------------------
# 11. Strategist report
# ---------------------------------------------------------------------

top_profiles = profile_rows[:5]
high_superficial = sorted(profile_rows, key=lambda item: item["superficial_testing_risk"], reverse=True)[:5]
top_assumptions = assumption_rows[:6]
top_prototypes = prototype_rows[:6]
top_experiments = experiment_rows[:6]
top_evidence = evidence_rows[:6]
low_evidence = sorted(evidence_rows, key=lambda item: item["evidence_quality_score"])[:4]
top_validation = validation_rows[:6]
top_iterations = iteration_rows[:6]
system_risks = impact_rows[:6]
ethics_risks = ethics_rows[:6]
top_decisions = decision_rows[:6]

report: list[str] = []
report.append("# Prototyping and Rapid Experimentation Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic evaluates prototypes and experiments as strategic learning systems. It assesses assumption criticality, prototype fit, experiment design, "
    "evidence quality, user validation, iteration discipline, systems impact, ethical governance, decision linkage, and learning memory."
)

report.append("")
report.append("## Strongest experimentation systems")
report.append("")
for item in top_profiles:
    report.append(
        f"- **{item['system_id']} — {item['system_name']}**: profile {item['experimentation_profile_score']}; "
        f"superficial testing risk {item['superficial_testing_risk']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest superficial testing risks")
report.append("")
for item in high_superficial:
    report.append(
        f"- **{item['system_id']} — {item['system_name']}**: superficial testing risk {item['superficial_testing_risk']}; "
        f"diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest priority assumptions")
report.append("")
for item in top_assumptions:
    report.append(
        f"- **{item['assumption_id']} — {item['assumption_statement']}**: "
        f"priority {item['assumption_priority_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Best prototype fit")
report.append("")
for item in top_prototypes:
    report.append(
        f"- **{item['prototype_id']} — {item['prototype_name']}**: "
        f"fit {item['prototype_fit_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strong experiment designs")
report.append("")
for item in top_experiments:
    report.append(
        f"- **{item['experiment_id']} — {item['hypothesis']}**: "
        f"quality {item['experiment_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strong evidence")
report.append("")
for item in top_evidence:
    report.append(
        f"- **{item['evidence_id']} — {item['evidence_type']}**: "
        f"evidence quality {item['evidence_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weak evidence warnings")
report.append("")
for item in low_evidence:
    report.append(
        f"- **{item['evidence_id']} — {item['evidence_type']}**: "
        f"evidence quality {item['evidence_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## User validation signals")
report.append("")
for item in top_validation:
    report.append(
        f"- **{item['validation_id']} — {item['user_group']}**: "
        f"validation {item['user_validation_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Iteration learning")
report.append("")
for item in top_iterations:
    report.append(
        f"- **{item['iteration_id']} — experiment {item['experiment_id']}**: "
        f"iteration learning {item['iteration_learning_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Systems impact risks")
report.append("")
for item in system_risks:
    report.append(
        f"- **{item['impact_id']} — {item['system_issue']}**: "
        f"systems risk {item['systems_impact_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Ethical governance risks")
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
report.append("## Professional interpretation")
report.append("")
report.append(
    "Prototyping strengthens strategic ideation when it tests critical assumptions, uses the lowest useful fidelity, produces interpretable evidence, "
    "observes behavior rather than opinion alone, accounts for systems effects, protects participants, documents iteration, and links learning to decisions."
)

(REPORTS / "prototyping_experimentation_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_profiles": top_profiles,
    "high_superficial": high_superficial,
    "top_assumptions": top_assumptions,
    "top_prototypes": top_prototypes,
    "top_experiments": top_experiments,
    "top_evidence": top_evidence,
    "low_evidence": low_evidence,
    "top_validation": top_validation,
    "top_iterations": top_iterations,
    "system_risks": system_risks,
    "ethics_risks": ethics_risks,
    "top_decisions": top_decisions,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced prototyping and rapid experimentation diagnostics complete.")
print(f"Wrote: {TABLES / 'experimentation_profile_scores.csv'}")
print(f"Wrote: {TABLES / 'assumption_priority_scores.csv'}")
print(f"Wrote: {TABLES / 'prototype_fit_scores.csv'}")
print(f"Wrote: {TABLES / 'experiment_quality_scores.csv'}")
print(f"Wrote: {TABLES / 'evidence_quality_scores.csv'}")
print(f"Wrote: {TABLES / 'user_validation_scores.csv'}")
print(f"Wrote: {TABLES / 'iteration_learning_scores.csv'}")
print(f"Wrote: {TABLES / 'systems_impact_scores.csv'}")
print(f"Wrote: {TABLES / 'ethical_governance_review.csv'}")
print(f"Wrote: {TABLES / 'decision_linkage_scores.csv'}")
print(f"Wrote: {REPORTS / 'prototyping_experimentation_diagnostic_report.md'}")
