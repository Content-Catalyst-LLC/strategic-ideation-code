#!/usr/bin/env python3
"""
Advanced strategist-facing strategic narrative diagnostics.

This dependency-light workflow uses only the Python standard library.

It produces:
- narrative coherence scores
- direction-logic alignment review
- narrative-performance gap analysis
- role-alignment register
- stakeholder interpretation risk
- narrative drift register
- narrative governance actions
- a markdown strategist diagnostic report

The workflow is designed for strategy teams that need to test whether
the story guiding direction is coherent, truthful, accountable, and actionable.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean

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


def bool_text(value: str) -> bool:
    return value.strip().lower() == "true"


profiles = read_csv(RAW / "narrative_profiles.csv")
elements = read_csv(RAW / "narrative_elements.csv")
logic = read_csv(RAW / "direction_logic.csv")
performance = read_csv(RAW / "performance_evidence.csv")
roles = read_csv(RAW / "role_alignment.csv")
stakeholders = read_csv(RAW / "stakeholder_interpretations.csv")
drifts = read_csv(RAW / "narrative_drift_events.csv")
governance = read_csv(RAW / "narrative_governance.csv")

narrative_names = {row["narrative_id"]: row["narrative_name"] for row in profiles}

# ---------------------------------------------------------------------
# 1. Narrative coherence scores
# ---------------------------------------------------------------------

coherence_rows: list[dict[str, object]] = []

for row in profiles:
    coherence_score = (
        0.14 * f(row, "diagnosis_clarity")
        + 0.12 * f(row, "purpose_clarity")
        + 0.14 * f(row, "choice_clarity")
        + 0.12 * f(row, "sequencing_logic")
        + 0.11 * f(row, "role_clarity")
        + 0.10 * f(row, "future_credibility")
        + 0.11 * f(row, "accountability_strength")
        + 0.08 * f(row, "evidence_grounding")
        + 0.05 * f(row, "stakeholder_visibility")
        + 0.03 * f(row, "ethical_visibility")
    )

    drift_risk = 1 - coherence_score

    if f(row, "choice_clarity") < 0.40:
        diagnosis = "weak_choice_logic"
    elif f(row, "sequencing_logic") < 0.40:
        diagnosis = "weak_pathway_logic"
    elif f(row, "accountability_strength") < 0.40:
        diagnosis = "narrative_performance_gap_risk"
    elif f(row, "stakeholder_visibility") < 0.45 or f(row, "ethical_visibility") < 0.45:
        diagnosis = "stakeholder_or_ethics_visibility_gap"
    elif coherence_score >= 0.72:
        diagnosis = "strong_directional_narrative"
    else:
        diagnosis = "requires_narrative_review"

    coherence_rows.append(
        {
            "narrative_id": row["narrative_id"],
            "narrative_name": row["narrative_name"],
            "narrative_type": row["narrative_type"],
            "narrative_coherence_score": round(coherence_score, 4),
            "drift_risk": round(drift_risk, 4),
            "diagnosis": diagnosis,
            "diagnosis_clarity": row["diagnosis_clarity"],
            "purpose_clarity": row["purpose_clarity"],
            "choice_clarity": row["choice_clarity"],
            "sequencing_logic": row["sequencing_logic"],
            "role_clarity": row["role_clarity"],
            "future_credibility": row["future_credibility"],
            "accountability_strength": row["accountability_strength"],
            "evidence_grounding": row["evidence_grounding"],
            "stakeholder_visibility": row["stakeholder_visibility"],
            "ethical_visibility": row["ethical_visibility"],
        }
    )

coherence_rows.sort(key=lambda item: item["narrative_coherence_score"], reverse=True)

write_csv(
    TABLES / "narrative_coherence_scores.csv",
    coherence_rows,
    [
        "narrative_id",
        "narrative_name",
        "narrative_type",
        "narrative_coherence_score",
        "drift_risk",
        "diagnosis",
        "diagnosis_clarity",
        "purpose_clarity",
        "choice_clarity",
        "sequencing_logic",
        "role_clarity",
        "future_credibility",
        "accountability_strength",
        "evidence_grounding",
        "stakeholder_visibility",
        "ethical_visibility",
    ],
)

write_csv(
    PROCESSED / "narrative_coherence_scores.csv",
    coherence_rows,
    [
        "narrative_id",
        "narrative_name",
        "narrative_type",
        "narrative_coherence_score",
        "drift_risk",
        "diagnosis",
        "diagnosis_clarity",
        "purpose_clarity",
        "choice_clarity",
        "sequencing_logic",
        "role_clarity",
        "future_credibility",
        "accountability_strength",
        "evidence_grounding",
        "stakeholder_visibility",
        "ethical_visibility",
    ],
)

# ---------------------------------------------------------------------
# 2. Narrative element quality
# ---------------------------------------------------------------------

element_rows: list[dict[str, object]] = []

for row in elements:
    element_score = (
        0.30 * f(row, "element_quality")
        + 0.24 * f(row, "internal_alignment")
        + 0.22 * f(row, "evidence_support")
        - 0.12 * f(row, "contestation_level")
        - 0.12 * f(row, "revision_need")
    )

    if f(row, "revision_need") >= 0.75:
        action = "urgent_element_revision"
    elif element_score < 0.40:
        action = "element_review_needed"
    else:
        action = "element_manageable"

    element_rows.append(
        {
            "element_id": row["element_id"],
            "narrative_id": row["narrative_id"],
            "narrative_name": narrative_names.get(row["narrative_id"], row["narrative_id"]),
            "element_type": row["element_type"],
            "element_score": round(element_score, 4),
            "recommended_action": action,
            "element_quality": row["element_quality"],
            "internal_alignment": row["internal_alignment"],
            "evidence_support": row["evidence_support"],
            "contestation_level": row["contestation_level"],
            "revision_need": row["revision_need"],
            "element_statement": row["element_statement"],
        }
    )

element_rows.sort(key=lambda item: item["element_score"])

write_csv(
    TABLES / "narrative_element_quality.csv",
    element_rows,
    [
        "element_id",
        "narrative_id",
        "narrative_name",
        "element_type",
        "element_score",
        "recommended_action",
        "element_quality",
        "internal_alignment",
        "evidence_support",
        "contestation_level",
        "revision_need",
        "element_statement",
    ],
)

# ---------------------------------------------------------------------
# 3. Direction-logic alignment
# ---------------------------------------------------------------------

logic_rows: list[dict[str, object]] = []

for row in logic:
    logic_score = (
        0.30 * f(row, "alignment_score")
        + 0.22 * f(row, "dependency_clarity")
        + 0.20 * f(row, "tradeoff_visibility")
        + 0.16 * f(row, "strategic_importance")
        - 0.18 * f(row, "logic_gap")
    )

    if f(row, "logic_gap") >= 0.70:
        action = "repair_direction_logic"
    elif f(row, "tradeoff_visibility") < 0.40:
        action = "make_tradeoffs_explicit"
    else:
        action = "logic_manageable"

    logic_rows.append(
        {
            "logic_id": row["logic_id"],
            "narrative_id": row["narrative_id"],
            "narrative_name": narrative_names.get(row["narrative_id"], row["narrative_id"]),
            "alignment_pair": row["alignment_pair"],
            "direction_logic_score": round(logic_score, 4),
            "recommended_action": action,
            "alignment_score": row["alignment_score"],
            "dependency_clarity": row["dependency_clarity"],
            "tradeoff_visibility": row["tradeoff_visibility"],
            "strategic_importance": row["strategic_importance"],
            "logic_gap": row["logic_gap"],
        }
    )

logic_rows.sort(key=lambda item: item["direction_logic_score"])

write_csv(
    TABLES / "direction_logic_alignment.csv",
    logic_rows,
    [
        "logic_id",
        "narrative_id",
        "narrative_name",
        "alignment_pair",
        "direction_logic_score",
        "recommended_action",
        "alignment_score",
        "dependency_clarity",
        "tradeoff_visibility",
        "strategic_importance",
        "logic_gap",
    ],
)

# ---------------------------------------------------------------------
# 4. Narrative-performance gap
# ---------------------------------------------------------------------

performance_rows: list[dict[str, object]] = []

for row in performance:
    gap_score = (
        0.26 * (1 - f(row, "evidence_strength"))
        + 0.28 * (1 - f(row, "action_alignment"))
        + 0.26 * f(row, "contradiction_risk")
        + 0.12 * f(row, "stakeholder_signal")
        + 0.08 * (1.0 if bool_text(row["revision_required"]) else 0.0)
    )

    if gap_score >= 0.66:
        action = "urgent_narrative_performance_audit"
    elif bool_text(row["revision_required"]):
        action = "scheduled_revision_review"
    else:
        action = "monitor"

    performance_rows.append(
        {
            "evidence_id": row["evidence_id"],
            "narrative_id": row["narrative_id"],
            "narrative_name": narrative_names.get(row["narrative_id"], row["narrative_id"]),
            "evidence_type": row["evidence_type"],
            "narrative_performance_gap": round(gap_score, 4),
            "recommended_action": action,
            "evidence_strength": row["evidence_strength"],
            "action_alignment": row["action_alignment"],
            "contradiction_risk": row["contradiction_risk"],
            "stakeholder_signal": row["stakeholder_signal"],
            "revision_required": row["revision_required"],
            "claim_tested": row["claim_tested"],
        }
    )

performance_rows.sort(key=lambda item: item["narrative_performance_gap"], reverse=True)

write_csv(
    TABLES / "narrative_performance_gap.csv",
    performance_rows,
    [
        "evidence_id",
        "narrative_id",
        "narrative_name",
        "evidence_type",
        "narrative_performance_gap",
        "recommended_action",
        "evidence_strength",
        "action_alignment",
        "contradiction_risk",
        "stakeholder_signal",
        "revision_required",
        "claim_tested",
    ],
)

# ---------------------------------------------------------------------
# 5. Role-alignment register
# ---------------------------------------------------------------------

role_rows: list[dict[str, object]] = []

for row in roles:
    role_score = (
        0.22 * f(row, "role_clarity")
        + 0.20 * f(row, "contribution_clarity")
        + 0.18 * f(row, "decision_authority_clarity")
        + 0.18 * f(row, "feedback_channel_quality")
        + 0.14 * f(row, "commitment_level")
        - 0.18 * f(row, "misalignment_risk")
    )

    if f(row, "misalignment_risk") >= 0.70:
        action = "repair_role_logic"
    elif f(row, "decision_authority_clarity") < 0.45:
        action = "clarify_decision_authority"
    else:
        action = "role_alignment_manageable"

    role_rows.append(
        {
            "role_id": row["role_id"],
            "narrative_id": row["narrative_id"],
            "narrative_name": narrative_names.get(row["narrative_id"], row["narrative_id"]),
            "actor_group": row["actor_group"],
            "role_alignment_score": round(role_score, 4),
            "recommended_action": action,
            "role_clarity": row["role_clarity"],
            "contribution_clarity": row["contribution_clarity"],
            "decision_authority_clarity": row["decision_authority_clarity"],
            "feedback_channel_quality": row["feedback_channel_quality"],
            "commitment_level": row["commitment_level"],
            "misalignment_risk": row["misalignment_risk"],
        }
    )

role_rows.sort(key=lambda item: item["role_alignment_score"])

write_csv(
    TABLES / "role_alignment_register.csv",
    role_rows,
    [
        "role_id",
        "narrative_id",
        "narrative_name",
        "actor_group",
        "role_alignment_score",
        "recommended_action",
        "role_clarity",
        "contribution_clarity",
        "decision_authority_clarity",
        "feedback_channel_quality",
        "commitment_level",
        "misalignment_risk",
    ],
)

# ---------------------------------------------------------------------
# 6. Stakeholder interpretation risk
# ---------------------------------------------------------------------

stakeholder_rows: list[dict[str, object]] = []

for row in stakeholders:
    interpretation_risk = (
        0.18 * (1 - f(row, "understanding_quality"))
        + 0.20 * (1 - f(row, "trust_in_narrative"))
        + 0.18 * (1 - f(row, "perceived_truthfulness"))
        + 0.14 * (1 - f(row, "perceived_inclusion"))
        + 0.14 * (1 - f(row, "perceived_burden_visibility"))
        + 0.16 * f(row, "contestation_level")
    )

    if interpretation_risk >= 0.64:
        action = "stakeholder_narrative_review"
    elif f(row, "perceived_burden_visibility") < 0.45:
        action = "add_burden_visibility_review"
    else:
        action = "interpretation_manageable"

    stakeholder_rows.append(
        {
            "interpretation_id": row["interpretation_id"],
            "narrative_id": row["narrative_id"],
            "narrative_name": narrative_names.get(row["narrative_id"], row["narrative_id"]),
            "stakeholder_group": row["stakeholder_group"],
            "stakeholder_interpretation_risk": round(interpretation_risk, 4),
            "recommended_action": action,
            "understanding_quality": row["understanding_quality"],
            "trust_in_narrative": row["trust_in_narrative"],
            "perceived_truthfulness": row["perceived_truthfulness"],
            "perceived_inclusion": row["perceived_inclusion"],
            "perceived_burden_visibility": row["perceived_burden_visibility"],
            "contestation_level": row["contestation_level"],
        }
    )

stakeholder_rows.sort(key=lambda item: item["stakeholder_interpretation_risk"], reverse=True)

write_csv(
    TABLES / "stakeholder_interpretation_risk.csv",
    stakeholder_rows,
    [
        "interpretation_id",
        "narrative_id",
        "narrative_name",
        "stakeholder_group",
        "stakeholder_interpretation_risk",
        "recommended_action",
        "understanding_quality",
        "trust_in_narrative",
        "perceived_truthfulness",
        "perceived_inclusion",
        "perceived_burden_visibility",
        "contestation_level",
    ],
)

# ---------------------------------------------------------------------
# 7. Narrative drift register
# ---------------------------------------------------------------------

drift_rows: list[dict[str, object]] = []

for row in drifts:
    drift_priority = (
        0.34 * f(row, "drift_severity")
        + 0.34 * f(row, "strategic_exposure")
        + 0.18 * f(row, "detection_confidence")
        + 0.14 * (1.0 if row["drift_type"] in ("slogan_substitution", "fragmentation", "ethical_blindness", "heroic_brittleness") else 0.65)
    )

    if drift_priority >= 0.78:
        urgency = "urgent_narrative_repair"
    elif drift_priority >= 0.62:
        urgency = "scheduled_narrative_review"
    else:
        urgency = "monitor"

    drift_rows.append(
        {
            "drift_id": row["drift_id"],
            "narrative_id": row["narrative_id"],
            "narrative_name": narrative_names.get(row["narrative_id"], row["narrative_id"]),
            "drift_type": row["drift_type"],
            "drift_priority": round(drift_priority, 4),
            "urgency": urgency,
            "drift_severity": row["drift_severity"],
            "strategic_exposure": row["strategic_exposure"],
            "detection_confidence": row["detection_confidence"],
            "recommended_response": row["recommended_response"],
            "drift_description": row["drift_description"],
        }
    )

drift_rows.sort(key=lambda item: item["drift_priority"], reverse=True)

write_csv(
    TABLES / "narrative_drift_register.csv",
    drift_rows,
    [
        "drift_id",
        "narrative_id",
        "narrative_name",
        "drift_type",
        "drift_priority",
        "urgency",
        "drift_severity",
        "strategic_exposure",
        "detection_confidence",
        "recommended_response",
        "drift_description",
    ],
)

# ---------------------------------------------------------------------
# 8. Narrative governance actions
# ---------------------------------------------------------------------

governance_rows: list[dict[str, object]] = []

for row in governance:
    governance_strength = (
        0.14 * f(row, "diagnosis_owner")
        + 0.14 * f(row, "choice_owner")
        + 0.18 * f(row, "evidence_review_quality")
        + 0.18 * f(row, "stakeholder_review_quality")
        + 0.18 * f(row, "performance_gap_review")
        + 0.18 * f(row, "revision_trigger_quality")
        - 0.16 * f(row, "governance_risk")
    )

    if governance_strength < 0.35:
        action = "establish_narrative_governance"
    elif f(row, "performance_gap_review") < 0.45:
        action = "add_narrative_performance_gap_review"
    elif f(row, "stakeholder_review_quality") < 0.45:
        action = "add_stakeholder_narrative_review"
    else:
        action = "governance_manageable"

    governance_rows.append(
        {
            "governance_id": row["governance_id"],
            "narrative_id": row["narrative_id"],
            "narrative_name": narrative_names.get(row["narrative_id"], row["narrative_id"]),
            "owner_group": row["owner_group"],
            "review_cadence": row["review_cadence"],
            "governance_strength": round(governance_strength, 4),
            "recommended_action": action,
            "diagnosis_owner": row["diagnosis_owner"],
            "choice_owner": row["choice_owner"],
            "evidence_review_quality": row["evidence_review_quality"],
            "stakeholder_review_quality": row["stakeholder_review_quality"],
            "performance_gap_review": row["performance_gap_review"],
            "revision_trigger_quality": row["revision_trigger_quality"],
            "governance_risk": row["governance_risk"],
        }
    )

governance_rows.sort(key=lambda item: item["governance_strength"])

write_csv(
    TABLES / "narrative_governance_actions.csv",
    governance_rows,
    [
        "governance_id",
        "narrative_id",
        "narrative_name",
        "owner_group",
        "review_cadence",
        "governance_strength",
        "recommended_action",
        "diagnosis_owner",
        "choice_owner",
        "evidence_review_quality",
        "stakeholder_review_quality",
        "performance_gap_review",
        "revision_trigger_quality",
        "governance_risk",
    ],
)

# ---------------------------------------------------------------------
# 9. Strategist report
# ---------------------------------------------------------------------

weakest_narratives = sorted(coherence_rows, key=lambda item: item["narrative_coherence_score"])[:5]
weakest_elements = element_rows[:5]
weakest_logic = logic_rows[:5]
highest_gap = performance_rows[:6]
weakest_roles = role_rows[:5]
highest_stakeholder_risk = stakeholder_rows[:5]
highest_drift = drift_rows[:5]
weakest_governance = governance_rows[:5]

report: list[str] = []

report.append("# Strategic Narrative Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic separates narrative coherence, element quality, direction logic, performance gaps, "
    "role alignment, stakeholder interpretation, narrative drift, and governance maturity. "
    "The purpose is to help strategists identify when the problem is not communication, but weak direction logic."
)
report.append("")
report.append("## Narratives requiring the most review")
report.append("")

for item in weakest_narratives:
    report.append(
        f"- **{item['narrative_id']} — {item['narrative_name']}**: coherence score {item['narrative_coherence_score']}; "
        f"drift risk {item['drift_risk']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Weakest narrative elements")
report.append("")

for item in weakest_elements:
    report.append(
        f"- **{item['element_id']} ({item['narrative_name']})**: {item['element_type']} score {item['element_score']}; "
        f"action: {item['recommended_action']}; statement: {item['element_statement']}"
    )

report.append("")
report.append("## Weakest direction-logic links")
report.append("")

for item in weakest_logic:
    report.append(
        f"- **{item['logic_id']} ({item['narrative_name']})**: {item['alignment_pair']} score {item['direction_logic_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest narrative-performance gaps")
report.append("")

for item in highest_gap:
    report.append(
        f"- **{item['evidence_id']} ({item['narrative_name']})**: gap {item['narrative_performance_gap']}; "
        f"action: {item['recommended_action']}; claim tested: {item['claim_tested']}"
    )

report.append("")
report.append("## Role-alignment concerns")
report.append("")

for item in weakest_roles:
    report.append(
        f"- **{item['role_id']} ({item['narrative_name']})**: actor group {item['actor_group']}; "
        f"score {item['role_alignment_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Stakeholder interpretation concerns")
report.append("")

for item in highest_stakeholder_risk:
    report.append(
        f"- **{item['interpretation_id']} ({item['narrative_name']})**: group {item['stakeholder_group']}; "
        f"risk {item['stakeholder_interpretation_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest narrative drift priorities")
report.append("")

for item in highest_drift:
    report.append(
        f"- **{item['drift_id']} ({item['narrative_name']})**: drift type {item['drift_type']}; "
        f"priority {item['drift_priority']}; response: {item['recommended_response']}."
    )

report.append("")
report.append("## Weakest governance areas")
report.append("")

for item in weakest_governance:
    report.append(
        f"- **{item['governance_id']} ({item['narrative_name']})**: governance strength {item['governance_strength']}; "
        f"owner group: {item['owner_group']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "The value of this workflow is disciplined direction review. It helps a strategist ask whether the "
    "narrative has a clear diagnosis, purpose, choice, sequence, role logic, future state, evidence base, "
    "and accountability mechanism. It also tests whether action confirms or contradicts the story being told."
)

(REPORTS / "strategic_narrative_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "weakest_narratives": weakest_narratives,
    "weakest_elements": weakest_elements,
    "weakest_logic": weakest_logic,
    "highest_gap": highest_gap,
    "weakest_roles": weakest_roles,
    "highest_stakeholder_risk": highest_stakeholder_risk,
    "highest_drift": highest_drift,
    "weakest_governance": weakest_governance,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced strategic narrative diagnostics complete.")
print(f"Wrote: {TABLES / 'narrative_coherence_scores.csv'}")
print(f"Wrote: {TABLES / 'direction_logic_alignment.csv'}")
print(f"Wrote: {TABLES / 'narrative_performance_gap.csv'}")
print(f"Wrote: {TABLES / 'role_alignment_register.csv'}")
print(f"Wrote: {TABLES / 'stakeholder_interpretation_risk.csv'}")
print(f"Wrote: {TABLES / 'narrative_drift_register.csv'}")
print(f"Wrote: {TABLES / 'narrative_governance_actions.csv'}")
print(f"Wrote: {REPORTS / 'strategic_narrative_diagnostic_report.md'}")
