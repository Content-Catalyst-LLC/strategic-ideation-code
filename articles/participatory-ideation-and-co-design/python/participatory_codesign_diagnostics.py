#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Participatory Ideation and Co-Design.

This dependency-light workflow uses only the Python standard library.

It produces:
- participation system profile scores
- stakeholder representation scores
- influence boundary scores
- accessibility support scores
- reciprocity and extraction-risk scores
- power-risk scores
- knowledge integration scores
- conflict and tradeoff scores
- decision traceability scores
- accountability scores
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


systems = read_csv(RAW / "participation_systems.csv")
stakeholders = read_csv(RAW / "stakeholders.csv")
boundaries = read_csv(RAW / "influence_boundaries.csv")
access = read_csv(RAW / "accessibility_supports.csv")
reciprocity = read_csv(RAW / "reciprocity.csv")
power = read_csv(RAW / "power_risks.csv")
knowledge = read_csv(RAW / "knowledge_integration.csv")
conflicts = read_csv(RAW / "conflict_tradeoffs.csv")
decisions = read_csv(RAW / "decision_traceability.csv")
accountability = read_csv(RAW / "accountability.csv")

system_names = {row["system_id"]: row["system_name"] for row in systems}

# ---------------------------------------------------------------------
# 1. Participation system profile
# ---------------------------------------------------------------------

profile_rows: list[dict[str, object]] = []

for row in systems:
    quality = (
        0.13 * f(row, "representation")
        + 0.15 * f(row, "influence")
        + 0.11 * f(row, "accessibility")
        + 0.11 * f(row, "reciprocity")
        + 0.13 * f(row, "power_awareness")
        + 0.12 * f(row, "knowledge_integration")
        + 0.11 * f(row, "decision_linkage")
        + 0.10 * f(row, "accountability")
        + 0.04 * f(row, "learning_memory")
    )

    tokenism_risk = (
        0.16 * (1 - f(row, "influence"))
        + 0.14 * (1 - f(row, "decision_linkage"))
        + 0.14 * (1 - f(row, "accountability"))
        + 0.13 * (1 - f(row, "reciprocity"))
        + 0.13 * (1 - f(row, "power_awareness"))
        + 0.11 * (1 - f(row, "representation"))
        + 0.10 * (1 - f(row, "accessibility"))
        + 0.09 * (1 - f(row, "learning_memory"))
    )

    if quality >= 0.72:
        diagnosis = "strong_participatory_codesign_system"
    elif tokenism_risk >= 0.68:
        diagnosis = "high_tokenism_or_extractive_participation_risk"
    elif f(row, "influence") < 0.36:
        diagnosis = "participation_has_low_decision_influence"
    elif f(row, "accountability") < 0.36:
        diagnosis = "weak_close_the_loop_accountability"
    else:
        diagnosis = "developing_participatory_capability"

    profile_rows.append(
        {
            "system_id": row["system_id"],
            "system_name": row["system_name"],
            "organization_type": row["organization_type"],
            "domain": row["domain"],
            "participation_quality_score": round(quality, 4),
            "tokenism_extraction_risk": round(tokenism_risk, 4),
            "diagnosis": diagnosis,
            "representation": row["representation"],
            "influence": row["influence"],
            "accessibility": row["accessibility"],
            "reciprocity": row["reciprocity"],
            "power_awareness": row["power_awareness"],
            "knowledge_integration": row["knowledge_integration"],
            "decision_linkage": row["decision_linkage"],
            "accountability": row["accountability"],
            "learning_memory": row["learning_memory"],
            "description": row["description"],
        }
    )

profile_rows.sort(key=lambda item: item["participation_quality_score"], reverse=True)
profile_fields = list(profile_rows[0].keys())
write_csv(TABLES / "participation_system_profile_scores.csv", profile_rows, profile_fields)
write_csv(PROCESSED / "participation_system_profile_scores.csv", profile_rows, profile_fields)

# ---------------------------------------------------------------------
# 2. Stakeholder representation scoring
# ---------------------------------------------------------------------

stakeholder_rows: list[dict[str, object]] = []

for row in stakeholders:
    representation_need = (
        0.20 * f(row, "affectedness")
        + 0.11 * (1 - f(row, "decision_power"))
        + 0.12 * f(row, "implementation_role")
        + 0.18 * f(row, "knowledge_value")
        + 0.16 * f(row, "usual_exclusion_risk")
    )

    representation_score = (
        0.55 * f(row, "participation_depth")
        + 0.45 * f(row, "representation_quality")
    )

    gap = representation_need - representation_score

    if gap >= 0.25:
        action = "representation_gap_requires_action"
    elif f(row, "usual_exclusion_risk") >= 0.50 and f(row, "participation_depth") < 0.55:
        action = "targeted_inclusion_needed"
    elif representation_score >= 0.72:
        action = "strong_representation"
    else:
        action = "improve_participation_depth"

    stakeholder_rows.append(
        {
            "stakeholder_id": row["stakeholder_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "stakeholder_group": row["stakeholder_group"],
            "stakeholder_type": row["stakeholder_type"],
            "representation_need": round(representation_need, 4),
            "representation_score": round(representation_score, 4),
            "representation_gap": round(gap, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "affectedness": row["affectedness"],
            "decision_power": row["decision_power"],
            "implementation_role": row["implementation_role"],
            "knowledge_value": row["knowledge_value"],
            "usual_exclusion_risk": row["usual_exclusion_risk"],
            "participation_depth": row["participation_depth"],
            "representation_quality": row["representation_quality"],
        }
    )

stakeholder_rows.sort(key=lambda item: item["representation_gap"], reverse=True)
write_csv(TABLES / "stakeholder_representation_scores.csv", stakeholder_rows, list(stakeholder_rows[0].keys()))

# ---------------------------------------------------------------------
# 3. Influence-boundary scoring
# ---------------------------------------------------------------------

boundary_rows: list[dict[str, object]] = []

for row in boundaries:
    influence_score = (
        0.16 * f(row, "problem_frame_open")
        + 0.14 * f(row, "idea_generation_open")
        + 0.14 * f(row, "prototype_open")
        + 0.13 * f(row, "evaluation_criteria_open")
        + 0.11 * f(row, "implementation_open")
        + 0.10 * f(row, "governance_open")
        + 0.11 * f(row, "constraint_transparency")
        + 0.11 * f(row, "decision_authority_clarity")
    )

    if influence_score >= 0.70:
        action = "strong_influence_boundary"
    elif f(row, "constraint_transparency") < 0.45:
        action = "clarify_constraints"
    elif f(row, "decision_authority_clarity") < 0.45:
        action = "clarify_decision_authority"
    elif f(row, "problem_frame_open") < 0.40:
        action = "invite_earlier_problem_framing"
    else:
        action = "increase_participant_influence"

    boundary_rows.append(
        {
            "boundary_id": row["boundary_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "participation_purpose": row["participation_purpose"],
            "influence_boundary_score": round(influence_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "problem_frame_open": row["problem_frame_open"],
            "idea_generation_open": row["idea_generation_open"],
            "prototype_open": row["prototype_open"],
            "evaluation_criteria_open": row["evaluation_criteria_open"],
            "implementation_open": row["implementation_open"],
            "governance_open": row["governance_open"],
            "constraint_transparency": row["constraint_transparency"],
            "decision_authority_clarity": row["decision_authority_clarity"],
        }
    )

boundary_rows.sort(key=lambda item: item["influence_boundary_score"], reverse=True)
write_csv(TABLES / "influence_boundary_scores.csv", boundary_rows, list(boundary_rows[0].keys()))

# ---------------------------------------------------------------------
# 4. Accessibility support scoring
# ---------------------------------------------------------------------

access_rows: list[dict[str, object]] = []

for row in access:
    access_score = (
        0.13 * f(row, "language_access")
        + 0.14 * f(row, "disability_access")
        + 0.12 * f(row, "schedule_flexibility")
        + 0.11 * f(row, "technology_access")
        + 0.13 * f(row, "compensation_support")
        + 0.12 * f(row, "care_transport_support")
        + 0.13 * f(row, "psychological_safety")
        + 0.12 * f(row, "cultural_fit")
    )

    if access_score >= 0.72:
        action = "strong_access_support"
    elif f(row, "compensation_support") < 0.35:
        action = "add_compensation_or_reciprocity_support"
    elif f(row, "disability_access") < 0.45:
        action = "add_disability_access_review"
    elif f(row, "care_transport_support") < 0.35:
        action = "add_care_transport_support"
    else:
        action = "strengthen_access_plan"

    access_rows.append(
        {
            "access_id": row["access_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "access_design": row["access_design"],
            "accessibility_support_score": round(access_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "language_access": row["language_access"],
            "disability_access": row["disability_access"],
            "schedule_flexibility": row["schedule_flexibility"],
            "technology_access": row["technology_access"],
            "compensation_support": row["compensation_support"],
            "care_transport_support": row["care_transport_support"],
            "psychological_safety": row["psychological_safety"],
            "cultural_fit": row["cultural_fit"],
        }
    )

access_rows.sort(key=lambda item: item["accessibility_support_score"], reverse=True)
write_csv(TABLES / "accessibility_support_scores.csv", access_rows, list(access_rows[0].keys()))

# ---------------------------------------------------------------------
# 5. Reciprocity and extraction risk
# ---------------------------------------------------------------------

reciprocity_rows: list[dict[str, object]] = []

for row in reciprocity:
    reciprocity_score = (
        0.16 * f(row, "compensation_quality")
        + 0.12 * f(row, "credit_quality")
        + 0.16 * f(row, "feedback_return_quality")
        + 0.12 * f(row, "capacity_building")
        + 0.15 * f(row, "benefit_to_participants")
        + 0.14 * f(row, "ongoing_relationship")
        - 0.15 * f(row, "extraction_risk_context")
    )

    extraction_risk = (
        0.25 * f(row, "participant_labor")
        + 0.18 * f(row, "extraction_risk_context")
        + 0.14 * (1 - f(row, "compensation_quality"))
        + 0.13 * (1 - f(row, "feedback_return_quality"))
        + 0.12 * (1 - f(row, "benefit_to_participants"))
        + 0.10 * (1 - f(row, "ongoing_relationship"))
        + 0.08 * (1 - f(row, "credit_quality"))
    )

    if extraction_risk >= 0.62:
        action = "high_extraction_risk"
    elif reciprocity_score >= 0.62:
        action = "strong_reciprocity"
    elif f(row, "feedback_return_quality") < 0.35:
        action = "close_loop_with_participants"
    elif f(row, "compensation_quality") < 0.35:
        action = "improve_compensation_or_support"
    else:
        action = "strengthen_reciprocity"

    reciprocity_rows.append(
        {
            "reciprocity_id": row["reciprocity_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "reciprocity_score": round(reciprocity_score, 4),
            "extraction_risk": round(extraction_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "participant_labor": row["participant_labor"],
            "compensation_quality": row["compensation_quality"],
            "credit_quality": row["credit_quality"],
            "feedback_return_quality": row["feedback_return_quality"],
            "capacity_building": row["capacity_building"],
            "benefit_to_participants": row["benefit_to_participants"],
            "ongoing_relationship": row["ongoing_relationship"],
            "extraction_risk_context": row["extraction_risk_context"],
        }
    )

reciprocity_rows.sort(key=lambda item: item["extraction_risk"], reverse=True)
write_csv(TABLES / "reciprocity_scores.csv", reciprocity_rows, list(reciprocity_rows[0].keys()))

# ---------------------------------------------------------------------
# 6. Power-risk scoring
# ---------------------------------------------------------------------

power_rows: list[dict[str, object]] = []

for row in power:
    raw_power_risk = (
        0.13 * f(row, "invitation_bias")
        + 0.15 * f(row, "framing_control")
        + 0.11 * f(row, "language_barrier")
        + 0.13 * f(row, "dominant_voice_risk")
        + 0.16 * f(row, "interpretive_capture")
        + 0.16 * f(row, "decision_capture")
        + 0.10 * f(row, "participant_risk")
        - 0.06 * f(row, "mitigation_quality")
    )

    if raw_power_risk >= 0.62:
        action = "high_power_risk_requires_mitigation"
    elif f(row, "interpretive_capture") >= 0.65:
        action = "add_participant_synthesis_review"
    elif f(row, "decision_capture") >= 0.65:
        action = "clarify_decision_power"
    elif f(row, "mitigation_quality") < 0.40:
        action = "add_power_mitigation"
    else:
        action = "monitor_power_dynamics"

    power_rows.append(
        {
            "power_id": row["power_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "power_issue": row["power_issue"],
            "power_risk_score": round(raw_power_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "invitation_bias": row["invitation_bias"],
            "framing_control": row["framing_control"],
            "language_barrier": row["language_barrier"],
            "dominant_voice_risk": row["dominant_voice_risk"],
            "interpretive_capture": row["interpretive_capture"],
            "decision_capture": row["decision_capture"],
            "participant_risk": row["participant_risk"],
            "mitigation_quality": row["mitigation_quality"],
        }
    )

power_rows.sort(key=lambda item: item["power_risk_score"], reverse=True)
write_csv(TABLES / "power_risk_scores.csv", power_rows, list(power_rows[0].keys()))

# ---------------------------------------------------------------------
# 7. Knowledge integration scoring
# ---------------------------------------------------------------------

knowledge_rows: list[dict[str, object]] = []

for row in knowledge:
    integration_score = (
        0.15 * f(row, "lived_experience_integration")
        + 0.12 * f(row, "technical_expertise_integration")
        + 0.13 * f(row, "operational_knowledge_integration")
        + 0.14 * f(row, "systems_analysis_integration")
        + 0.13 * f(row, "evidence_quality")
        + 0.14 * f(row, "conflict_visibility")
        + 0.19 * f(row, "synthesis_traceability")
    )

    if integration_score >= 0.72:
        action = "strong_knowledge_integration"
    elif f(row, "synthesis_traceability") < 0.45:
        action = "make_synthesis_traceable"
    elif f(row, "conflict_visibility") < 0.45:
        action = "document_conflict_and_tradeoffs"
    elif f(row, "lived_experience_integration") < 0.45:
        action = "strengthen_lived_experience_integration"
    else:
        action = "improve_knowledge_integration"

    knowledge_rows.append(
        {
            "knowledge_id": row["knowledge_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "integration_practice": row["integration_practice"],
            "knowledge_integration_score": round(integration_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "lived_experience_integration": row["lived_experience_integration"],
            "technical_expertise_integration": row["technical_expertise_integration"],
            "operational_knowledge_integration": row["operational_knowledge_integration"],
            "systems_analysis_integration": row["systems_analysis_integration"],
            "evidence_quality": row["evidence_quality"],
            "conflict_visibility": row["conflict_visibility"],
            "synthesis_traceability": row["synthesis_traceability"],
        }
    )

knowledge_rows.sort(key=lambda item: item["knowledge_integration_score"], reverse=True)
write_csv(TABLES / "knowledge_integration_scores.csv", knowledge_rows, list(knowledge_rows[0].keys()))

# ---------------------------------------------------------------------
# 8. Conflict and tradeoff scoring
# ---------------------------------------------------------------------

conflict_rows: list[dict[str, object]] = []

for row in conflicts:
    conflict_handling_score = (
        0.16 * f(row, "conflict_visibility")
        + 0.15 * f(row, "tradeoff_clarity")
        + 0.15 * f(row, "dissent_documentation")
        + 0.14 * f(row, "burden_shift_review")
        + 0.14 * f(row, "value_tension_review")
        + 0.13 * f(row, "resolution_transparency")
        + 0.13 * f(row, "followup_quality")
    )

    if conflict_handling_score >= 0.70:
        action = "strong_conflict_tradeoff_handling"
    elif f(row, "dissent_documentation") < 0.40:
        action = "document_dissent"
    elif f(row, "burden_shift_review") < 0.45:
        action = "review_burden_shifts"
    elif f(row, "resolution_transparency") < 0.45:
        action = "make_resolution_transparent"
    else:
        action = "strengthen_conflict_handling"

    conflict_rows.append(
        {
            "conflict_id": row["conflict_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "conflict_type": row["conflict_type"],
            "conflict_tradeoff_score": round(conflict_handling_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "conflict_visibility": row["conflict_visibility"],
            "tradeoff_clarity": row["tradeoff_clarity"],
            "dissent_documentation": row["dissent_documentation"],
            "burden_shift_review": row["burden_shift_review"],
            "value_tension_review": row["value_tension_review"],
            "resolution_transparency": row["resolution_transparency"],
            "followup_quality": row["followup_quality"],
        }
    )

conflict_rows.sort(key=lambda item: item["conflict_tradeoff_score"], reverse=True)
write_csv(TABLES / "conflict_tradeoff_scores.csv", conflict_rows, list(conflict_rows[0].keys()))

# ---------------------------------------------------------------------
# 9. Decision traceability scoring
# ---------------------------------------------------------------------

decision_rows: list[dict[str, object]] = []

for row in decisions:
    decision_score = (
        0.16 * f(row, "input_to_decision_clarity")
        + 0.14 * f(row, "authority_connection")
        + 0.11 * f(row, "resource_connection")
        + 0.13 * f(row, "revision_trigger_quality")
        + 0.13 * f(row, "implementation_path_quality")
        + 0.15 * f(row, "participant_review_quality")
        + 0.18 * f(row, "decision_rationale_quality")
    )

    if decision_score >= 0.72:
        action = "strong_decision_traceability"
    elif f(row, "input_to_decision_clarity") < 0.40:
        action = "show_how_input_changed_decisions"
    elif f(row, "participant_review_quality") < 0.40:
        action = "add_participant_review"
    elif f(row, "decision_rationale_quality") < 0.40:
        action = "document_decision_rationale"
    else:
        action = "strengthen_decision_traceability"

    decision_rows.append(
        {
            "decision_id": row["decision_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "decision_type": row["decision_type"],
            "decision_traceability_score": round(decision_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "input_to_decision_clarity": row["input_to_decision_clarity"],
            "authority_connection": row["authority_connection"],
            "resource_connection": row["resource_connection"],
            "revision_trigger_quality": row["revision_trigger_quality"],
            "implementation_path_quality": row["implementation_path_quality"],
            "participant_review_quality": row["participant_review_quality"],
            "decision_rationale_quality": row["decision_rationale_quality"],
        }
    )

decision_rows.sort(key=lambda item: item["decision_traceability_score"], reverse=True)
write_csv(TABLES / "decision_traceability_scores.csv", decision_rows, list(decision_rows[0].keys()))

# ---------------------------------------------------------------------
# 10. Accountability scoring
# ---------------------------------------------------------------------

accountability_rows: list[dict[str, object]] = []

for row in accountability:
    accountability_score = (
        0.16 * f(row, "close_loop_quality")
        + 0.13 * f(row, "public_response_quality")
        + 0.12 * f(row, "participant_challenge_path")
        + 0.13 * f(row, "implementation_monitoring")
        + 0.13 * f(row, "ongoing_governance")
        + 0.16 * f(row, "learning_memory_quality")
        + 0.17 * f(row, "trust_repair_quality")
    )

    if accountability_score >= 0.72:
        action = "strong_accountability"
    elif f(row, "close_loop_quality") < 0.40:
        action = "close_the_loop_with_participants"
    elif f(row, "participant_challenge_path") < 0.35:
        action = "create_participant_challenge_path"
    elif f(row, "implementation_monitoring") < 0.40:
        action = "add_implementation_monitoring"
    else:
        action = "strengthen_accountability"

    accountability_rows.append(
        {
            "accountability_id": row["accountability_id"],
            "system_id": row["system_id"],
            "system_name": system_names.get(row["system_id"], row["system_id"]),
            "accountability_practice": row["accountability_practice"],
            "accountability_score": round(accountability_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "close_loop_quality": row["close_loop_quality"],
            "public_response_quality": row["public_response_quality"],
            "participant_challenge_path": row["participant_challenge_path"],
            "implementation_monitoring": row["implementation_monitoring"],
            "ongoing_governance": row["ongoing_governance"],
            "learning_memory_quality": row["learning_memory_quality"],
            "trust_repair_quality": row["trust_repair_quality"],
        }
    )

accountability_rows.sort(key=lambda item: item["accountability_score"], reverse=True)
write_csv(TABLES / "accountability_scores.csv", accountability_rows, list(accountability_rows[0].keys()))

# ---------------------------------------------------------------------
# 11. Strategist report
# ---------------------------------------------------------------------

top_profiles = profile_rows[:5]
highest_tokenism = sorted(profile_rows, key=lambda item: item["tokenism_extraction_risk"], reverse=True)[:5]
representation_gaps = stakeholder_rows[:6]
top_boundaries = boundary_rows[:6]
low_boundaries = sorted(boundary_rows, key=lambda item: item["influence_boundary_score"])[:4]
top_access = access_rows[:6]
high_extraction = reciprocity_rows[:6]
high_power = power_rows[:6]
top_knowledge = knowledge_rows[:6]
top_conflicts = conflict_rows[:6]
top_decisions = decision_rows[:6]
top_accountability = accountability_rows[:6]
low_accountability = sorted(accountability_rows, key=lambda item: item["accountability_score"])[:4]

report: list[str] = []
report.append("# Participatory Ideation and Co-Design Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic evaluates participation as a strategic capability. It assesses representation, influence boundaries, accessibility, reciprocity, "
    "power risk, knowledge integration, conflict and tradeoff handling, decision traceability, accountability, tokenism risk, extraction risk, and learning memory."
)

report.append("")
report.append("## Strongest participatory systems")
report.append("")
for item in top_profiles:
    report.append(
        f"- **{item['system_id']} — {item['system_name']}**: quality {item['participation_quality_score']}; "
        f"tokenism/extraction risk {item['tokenism_extraction_risk']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest tokenism or extraction risks")
report.append("")
for item in highest_tokenism:
    report.append(
        f"- **{item['system_id']} — {item['system_name']}**: tokenism/extraction risk {item['tokenism_extraction_risk']}; "
        f"diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Representation gaps")
report.append("")
for item in representation_gaps:
    report.append(
        f"- **{item['stakeholder_id']} — {item['stakeholder_group']}**: "
        f"need {item['representation_need']}; score {item['representation_score']}; gap {item['representation_gap']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strong influence boundaries")
report.append("")
for item in top_boundaries:
    report.append(
        f"- **{item['boundary_id']} — {item['participation_purpose']}**: "
        f"influence score {item['influence_boundary_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weak influence boundary warnings")
report.append("")
for item in low_boundaries:
    report.append(
        f"- **{item['boundary_id']} — {item['participation_purpose']}**: "
        f"influence score {item['influence_boundary_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Accessibility support")
report.append("")
for item in top_access:
    report.append(
        f"- **{item['access_id']} — {item['access_design']}**: "
        f"accessibility score {item['accessibility_support_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Reciprocity and extraction risk")
report.append("")
for item in high_extraction:
    report.append(
        f"- **{item['reciprocity_id']} — {item['system_name']}**: "
        f"extraction risk {item['extraction_risk']}; reciprocity score {item['reciprocity_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Power risks")
report.append("")
for item in high_power:
    report.append(
        f"- **{item['power_id']} — {item['power_issue']}**: "
        f"power risk {item['power_risk_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Knowledge integration")
report.append("")
for item in top_knowledge:
    report.append(
        f"- **{item['knowledge_id']} — {item['integration_practice']}**: "
        f"integration score {item['knowledge_integration_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Conflict and tradeoff handling")
report.append("")
for item in top_conflicts:
    report.append(
        f"- **{item['conflict_id']} — {item['conflict_type']}**: "
        f"conflict/tradeoff score {item['conflict_tradeoff_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Decision traceability")
report.append("")
for item in top_decisions:
    report.append(
        f"- **{item['decision_id']} — {item['decision_type']}**: "
        f"traceability score {item['decision_traceability_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Accountability")
report.append("")
for item in top_accountability:
    report.append(
        f"- **{item['accountability_id']} — {item['accountability_practice']}**: "
        f"accountability score {item['accountability_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Low-accountability warnings")
report.append("")
for item in low_accountability:
    report.append(
        f"- **{item['accountability_id']} — {item['accountability_practice']}**: "
        f"accountability score {item['accountability_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "Participatory ideation strengthens strategy when affected stakeholders are meaningfully represented, participation begins early enough to shape framing, "
    "influence boundaries are transparent, access is designed, participant labor is reciprocated, power risks are mitigated, conflict is documented, and decisions "
    "are traceable. Participation becomes weak or harmful when it is late, symbolic, extractive, inaccessible, or disconnected from accountability."
)

(REPORTS / "participatory_codesign_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_profiles": top_profiles,
    "highest_tokenism": highest_tokenism,
    "representation_gaps": representation_gaps,
    "top_boundaries": top_boundaries,
    "low_boundaries": low_boundaries,
    "top_access": top_access,
    "high_extraction": high_extraction,
    "high_power": high_power,
    "top_knowledge": top_knowledge,
    "top_conflicts": top_conflicts,
    "top_decisions": top_decisions,
    "top_accountability": top_accountability,
    "low_accountability": low_accountability,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced participatory ideation and co-design diagnostics complete.")
print(f"Wrote: {TABLES / 'participation_system_profile_scores.csv'}")
print(f"Wrote: {TABLES / 'stakeholder_representation_scores.csv'}")
print(f"Wrote: {TABLES / 'influence_boundary_scores.csv'}")
print(f"Wrote: {TABLES / 'accessibility_support_scores.csv'}")
print(f"Wrote: {TABLES / 'reciprocity_scores.csv'}")
print(f"Wrote: {TABLES / 'power_risk_scores.csv'}")
print(f"Wrote: {TABLES / 'knowledge_integration_scores.csv'}")
print(f"Wrote: {TABLES / 'conflict_tradeoff_scores.csv'}")
print(f"Wrote: {TABLES / 'decision_traceability_scores.csv'}")
print(f"Wrote: {TABLES / 'accountability_scores.csv'}")
print(f"Wrote: {REPORTS / 'participatory_codesign_diagnostic_report.md'}")
