#!/usr/bin/env python3
"""
Advanced strategist-facing lateral thinking diagnostics.

This dependency-light workflow uses only the Python standard library.

It produces:
- lateral context profile scores
- frame-rigidity risk analysis
- dominant-frame and assumption-disruption review
- lateral-move scoring
- reframed problem quality review
- convergence-integration review
- stakeholder legitimacy and political-safety review
- a markdown strategist diagnostic report

The workflow is designed for strategy teams that need to turn frame disruption
into better problem representations, testable options, and decision memory.
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


contexts = read_csv(RAW / "lateral_contexts.csv")
frames = read_csv(RAW / "dominant_frames.csv")
assumptions = read_csv(RAW / "assumption_register.csv")
moves = read_csv(RAW / "lateral_moves.csv")
reframes = read_csv(RAW / "reframed_problems.csv")
integrations = read_csv(RAW / "convergence_integration.csv")
stakeholders = read_csv(RAW / "stakeholder_legitimacy.csv")

context_names = {row["context_id"]: row["context_name"] for row in contexts}
frame_names = {row["frame_id"]: row["frame_name"] for row in frames}
move_names = {row["move_id"]: row["move_name"] for row in moves}
reframe_names = {row["reframe_id"]: row["reframed_problem"] for row in reframes}

# ---------------------------------------------------------------------
# 1. Lateral context profile
# ---------------------------------------------------------------------

profile_rows: list[dict[str, object]] = []

for row in contexts:
    lateral_profile = (
        -0.14 * f(row, "frame_rigidity")
        + 0.14 * f(row, "provocation_strength")
        + 0.12 * f(row, "analogical_distance")
        + 0.09 * f(row, "random_entry_capacity")
        + 0.10 * f(row, "reversal_capacity")
        + 0.10 * f(row, "challenge_quality")
        + 0.14 * f(row, "convergence_discipline")
        + 0.12 * f(row, "systems_integration")
        + 0.08 * f(row, "stakeholder_legitimacy")
        + 0.07 * f(row, "political_safety")
        + 0.14 * f(row, "transformational_potential")
    )

    rigidity_risk = f(row, "frame_rigidity") * (1 - f(row, "provocation_strength"))
    drift_risk = f(row, "transformational_potential") * (1 - f(row, "convergence_discipline"))
    legitimacy_gap = max(0.0, 0.60 - f(row, "stakeholder_legitimacy"))
    political_safety_gap = max(0.0, 0.55 - f(row, "political_safety"))

    if rigidity_risk >= 0.55:
        diagnosis = "frame_rigidity_risk"
    elif drift_risk >= 0.45:
        diagnosis = "unintegrated_novelty_risk"
    elif legitimacy_gap >= 0.20:
        diagnosis = "stakeholder_legitimacy_gap"
    elif political_safety_gap >= 0.25:
        diagnosis = "political_safety_gap"
    elif lateral_profile >= 0.50:
        diagnosis = "strong_lateral_system"
    else:
        diagnosis = "requires_lateral_process_review"

    profile_rows.append(
        {
            "context_id": row["context_id"],
            "context_name": row["context_name"],
            "context_type": row["context_type"],
            "lateral_profile_score": round(lateral_profile, 4),
            "frame_rigidity_risk": round(rigidity_risk, 4),
            "drift_risk": round(drift_risk, 4),
            "legitimacy_gap": round(legitimacy_gap, 4),
            "political_safety_gap": round(political_safety_gap, 4),
            "diagnosis": diagnosis,
            "frame_rigidity": row["frame_rigidity"],
            "provocation_strength": row["provocation_strength"],
            "analogical_distance": row["analogical_distance"],
            "random_entry_capacity": row["random_entry_capacity"],
            "reversal_capacity": row["reversal_capacity"],
            "challenge_quality": row["challenge_quality"],
            "convergence_discipline": row["convergence_discipline"],
            "systems_integration": row["systems_integration"],
            "stakeholder_legitimacy": row["stakeholder_legitimacy"],
            "political_safety": row["political_safety"],
            "transformational_potential": row["transformational_potential"],
        }
    )

profile_rows.sort(key=lambda item: item["lateral_profile_score"], reverse=True)

profile_fields = [
    "context_id",
    "context_name",
    "context_type",
    "lateral_profile_score",
    "frame_rigidity_risk",
    "drift_risk",
    "legitimacy_gap",
    "political_safety_gap",
    "diagnosis",
    "frame_rigidity",
    "provocation_strength",
    "analogical_distance",
    "random_entry_capacity",
    "reversal_capacity",
    "challenge_quality",
    "convergence_discipline",
    "systems_integration",
    "stakeholder_legitimacy",
    "political_safety",
    "transformational_potential",
]

write_csv(TABLES / "lateral_context_profiles.csv", profile_rows, profile_fields)
write_csv(PROCESSED / "lateral_context_profiles.csv", profile_rows, profile_fields)

risk_rows = sorted(
    [
        {
            "context_id": row["context_id"],
            "context_name": row["context_name"],
            "frame_rigidity_risk": row["frame_rigidity_risk"],
            "drift_risk": row["drift_risk"],
            "legitimacy_gap": row["legitimacy_gap"],
            "political_safety_gap": row["political_safety_gap"],
            "diagnosis": row["diagnosis"],
        }
        for row in profile_rows
    ],
    key=lambda item: max(
        float(item["frame_rigidity_risk"]),
        float(item["drift_risk"]),
        float(item["legitimacy_gap"]),
        float(item["political_safety_gap"]),
    ),
    reverse=True,
)

write_csv(
    TABLES / "frame_rigidity_risk.csv",
    risk_rows,
    ["context_id", "context_name", "frame_rigidity_risk", "drift_risk", "legitimacy_gap", "political_safety_gap", "diagnosis"],
)

# ---------------------------------------------------------------------
# 2. Dominant frame review
# ---------------------------------------------------------------------

frame_rows: list[dict[str, object]] = []

for row in frames:
    frame_quality = (
        0.18 * f(row, "problem_clarity")
        + 0.18 * f(row, "assumption_visibility")
        - 0.16 * f(row, "metric_lock_in")
        - 0.16 * f(row, "category_rigidity")
        - 0.14 * f(row, "stakeholder_exclusion")
        + 0.18 * f(row, "system_boundary_quality")
        - 0.10 * f(row, "frame_obsolescence_risk")
    )

    if f(row, "frame_obsolescence_risk") >= 0.70:
        action = "reframe_before_optimization"
    elif f(row, "metric_lock_in") >= 0.75:
        action = "audit_metric_lock_in"
    elif f(row, "stakeholder_exclusion") >= 0.65:
        action = "include_excluded_stakeholders_before_reframing"
    elif frame_quality < 0.25:
        action = "dominant_frame_review_required"
    else:
        action = "frame_manageable"

    frame_rows.append(
        {
            "frame_id": row["frame_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "frame_name": row["frame_name"],
            "frame_origin": row["frame_origin"],
            "frame_quality_score": round(frame_quality, 4),
            "recommended_action": action,
            "problem_clarity": row["problem_clarity"],
            "assumption_visibility": row["assumption_visibility"],
            "metric_lock_in": row["metric_lock_in"],
            "category_rigidity": row["category_rigidity"],
            "stakeholder_exclusion": row["stakeholder_exclusion"],
            "system_boundary_quality": row["system_boundary_quality"],
            "frame_obsolescence_risk": row["frame_obsolescence_risk"],
        }
    )

frame_rows.sort(key=lambda item: item["frame_quality_score"])

write_csv(
    TABLES / "dominant_frame_review.csv",
    frame_rows,
    [
        "frame_id",
        "context_id",
        "context_name",
        "frame_name",
        "frame_origin",
        "frame_quality_score",
        "recommended_action",
        "problem_clarity",
        "assumption_visibility",
        "metric_lock_in",
        "category_rigidity",
        "stakeholder_exclusion",
        "system_boundary_quality",
        "frame_obsolescence_risk",
    ],
)

# ---------------------------------------------------------------------
# 3. Assumption disruption review
# ---------------------------------------------------------------------

assumption_rows: list[dict[str, object]] = []

for row in assumptions:
    challenge_priority = (
        0.24 * f(row, "strategic_importance")
        + 0.24 * f(row, "challenge_potential")
        + 0.18 * (1 - f(row, "evidence_strength"))
        + 0.16 * f(row, "power_protection_risk")
        + 0.10 * (1 - f(row, "stakeholder_burden_visibility"))
        + 0.08 * (1.0 if row["revision_priority"] == "high" else 0.55)
    )

    if f(row, "power_protection_risk") >= 0.70:
        action = "power_assumption_review"
    elif f(row, "evidence_strength") < 0.35:
        action = "test_or_challenge_assumption"
    elif challenge_priority >= 0.70:
        action = "priority_lateral_challenge"
    else:
        action = "monitor_assumption"

    assumption_rows.append(
        {
            "assumption_id": row["assumption_id"],
            "frame_id": row["frame_id"],
            "frame_name": frame_names.get(row["frame_id"], row["frame_id"]),
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "assumption_text": row["assumption_text"],
            "assumption_type": row["assumption_type"],
            "challenge_priority": round(challenge_priority, 4),
            "recommended_action": action,
            "evidence_strength": row["evidence_strength"],
            "strategic_importance": row["strategic_importance"],
            "challenge_potential": row["challenge_potential"],
            "stakeholder_burden_visibility": row["stakeholder_burden_visibility"],
            "power_protection_risk": row["power_protection_risk"],
            "revision_priority": row["revision_priority"],
        }
    )

assumption_rows.sort(key=lambda item: item["challenge_priority"], reverse=True)

write_csv(
    TABLES / "assumption_disruption_review.csv",
    assumption_rows,
    [
        "assumption_id",
        "frame_id",
        "frame_name",
        "context_id",
        "context_name",
        "assumption_text",
        "assumption_type",
        "challenge_priority",
        "recommended_action",
        "evidence_strength",
        "strategic_importance",
        "challenge_potential",
        "stakeholder_burden_visibility",
        "power_protection_risk",
        "revision_priority",
    ],
)

# ---------------------------------------------------------------------
# 4. Lateral move scoring
# ---------------------------------------------------------------------

move_rows: list[dict[str, object]] = []

for row in moves:
    move_score = (
        0.16 * f(row, "frame_disruption")
        + 0.18 * f(row, "strategic_relevance")
        + 0.16 * f(row, "reconstruction_quality")
        + 0.12 * f(row, "evidence_pathway")
        + 0.12 * f(row, "stakeholder_fit")
        + 0.12 * f(row, "systems_fit")
        + 0.10 * f(row, "novelty_value")
        - 0.14 * f(row, "drift_risk")
    )

    if f(row, "drift_risk") >= 0.70:
        action = "high_drift_risk_reconstruction_required"
    elif f(row, "reconstruction_quality") < 0.45:
        action = "reconstruct_before_evaluation"
    elif f(row, "stakeholder_fit") < 0.40:
        action = "stakeholder_review_before_advancing"
    elif move_score >= 0.62:
        action = "advance_to_reframe_review"
    else:
        action = "revise_or_hold_lateral_move"

    move_rows.append(
        {
            "move_id": row["move_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "frame_id": row["frame_id"],
            "frame_name": frame_names.get(row["frame_id"], row["frame_id"]),
            "technique": row["technique"],
            "move_name": row["move_name"],
            "lateral_move_score": round(move_score, 4),
            "recommended_action": action,
            "frame_disruption": row["frame_disruption"],
            "strategic_relevance": row["strategic_relevance"],
            "reconstruction_quality": row["reconstruction_quality"],
            "evidence_pathway": row["evidence_pathway"],
            "stakeholder_fit": row["stakeholder_fit"],
            "systems_fit": row["systems_fit"],
            "novelty_value": row["novelty_value"],
            "drift_risk": row["drift_risk"],
        }
    )

move_rows.sort(key=lambda item: item["lateral_move_score"], reverse=True)

write_csv(
    TABLES / "lateral_move_scores.csv",
    move_rows,
    [
        "move_id",
        "context_id",
        "context_name",
        "frame_id",
        "frame_name",
        "technique",
        "move_name",
        "lateral_move_score",
        "recommended_action",
        "frame_disruption",
        "strategic_relevance",
        "reconstruction_quality",
        "evidence_pathway",
        "stakeholder_fit",
        "systems_fit",
        "novelty_value",
        "drift_risk",
    ],
)

# ---------------------------------------------------------------------
# 5. Reframed problem quality
# ---------------------------------------------------------------------

reframe_rows: list[dict[str, object]] = []

for row in reframes:
    reframe_score = (
        0.16 * f(row, "problem_clarity")
        + 0.18 * f(row, "structural_shift")
        + 0.14 * f(row, "stakeholder_visibility")
        + 0.16 * f(row, "systems_alignment")
        + 0.14 * f(row, "decision_value")
        + 0.12 * f(row, "testability")
        + 0.10 * f(row, "implementation_pathway_quality")
    )

    if f(row, "testability") < 0.45:
        action = "convert_to_testable_hypothesis"
    elif f(row, "stakeholder_visibility") < 0.45:
        action = "add_stakeholder_visibility_review"
    elif reframe_score >= 0.72:
        action = "advance_to_convergence_integration"
    elif reframe_score >= 0.58:
        action = "revise_and_retest_reframe"
    else:
        action = "hold_or_reconstruct_reframe"

    reframe_rows.append(
        {
            "reframe_id": row["reframe_id"],
            "move_id": row["move_id"],
            "move_name": move_names.get(row["move_id"], row["move_id"]),
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "reframed_problem": row["reframed_problem"],
            "reframe_quality_score": round(reframe_score, 4),
            "recommended_action": action,
            "problem_clarity": row["problem_clarity"],
            "structural_shift": row["structural_shift"],
            "stakeholder_visibility": row["stakeholder_visibility"],
            "systems_alignment": row["systems_alignment"],
            "decision_value": row["decision_value"],
            "testability": row["testability"],
            "implementation_pathway_quality": row["implementation_pathway_quality"],
        }
    )

reframe_rows.sort(key=lambda item: item["reframe_quality_score"], reverse=True)

write_csv(
    TABLES / "reframed_problem_scores.csv",
    reframe_rows,
    [
        "reframe_id",
        "move_id",
        "move_name",
        "context_id",
        "context_name",
        "reframed_problem",
        "reframe_quality_score",
        "recommended_action",
        "problem_clarity",
        "structural_shift",
        "stakeholder_visibility",
        "systems_alignment",
        "decision_value",
        "testability",
        "implementation_pathway_quality",
    ],
)

# ---------------------------------------------------------------------
# 6. Convergence integration
# ---------------------------------------------------------------------

integration_rows: list[dict[str, object]] = []

for row in integrations:
    integration_score = (
        0.14 * f(row, "criteria_clarity")
        + 0.14 * f(row, "evidence_readiness")
        + 0.14 * f(row, "prototype_readiness")
        + 0.14 * f(row, "risk_review_quality")
        + 0.14 * f(row, "stakeholder_review_quality")
        + 0.14 * f(row, "systems_review_quality")
        + 0.12 * f(row, "implementation_readiness")
        + 0.10 * f(row, "decision_memory_quality")
    )

    if f(row, "prototype_readiness") < 0.45:
        action = "define_prototype_or_evidence_test"
    elif f(row, "systems_review_quality") < 0.45:
        action = "systems_review_before_selection"
    elif integration_score >= 0.72:
        action = "ready_for_evidence_gate"
    else:
        action = "strengthen_convergence_integration"

    integration_rows.append(
        {
            "integration_id": row["integration_id"],
            "reframe_id": row["reframe_id"],
            "reframed_problem": reframe_names.get(row["reframe_id"], row["reframe_id"]),
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "convergence_integration_score": round(integration_score, 4),
            "recommended_action": action,
            "criteria_clarity": row["criteria_clarity"],
            "evidence_readiness": row["evidence_readiness"],
            "prototype_readiness": row["prototype_readiness"],
            "risk_review_quality": row["risk_review_quality"],
            "stakeholder_review_quality": row["stakeholder_review_quality"],
            "systems_review_quality": row["systems_review_quality"],
            "implementation_readiness": row["implementation_readiness"],
            "decision_memory_quality": row["decision_memory_quality"],
        }
    )

integration_rows.sort(key=lambda item: item["convergence_integration_score"], reverse=True)

write_csv(
    TABLES / "convergence_integration_review.csv",
    integration_rows,
    [
        "integration_id",
        "reframe_id",
        "reframed_problem",
        "context_id",
        "context_name",
        "convergence_integration_score",
        "recommended_action",
        "criteria_clarity",
        "evidence_readiness",
        "prototype_readiness",
        "risk_review_quality",
        "stakeholder_review_quality",
        "systems_review_quality",
        "implementation_readiness",
        "decision_memory_quality",
    ],
)

# ---------------------------------------------------------------------
# 7. Stakeholder legitimacy and political safety
# ---------------------------------------------------------------------

stakeholder_rows: list[dict[str, object]] = []

for row in stakeholders:
    stakeholder_score = (
        0.14 * f(row, "inclusion_level")
        + 0.16 * f(row, "burden_visibility")
        + 0.16 * f(row, "knowledge_recognition")
        + 0.14 * f(row, "interpretive_trust")
        + 0.14 * f(row, "political_safety")
        + 0.16 * f(row, "legitimacy_signal")
        - 0.10 * f(row, "power_challenge_risk")
    )

    if f(row, "political_safety") < 0.35:
        action = "protect_constructive_dissent"
    elif f(row, "burden_visibility") < 0.40:
        action = "add_burden_visibility_review"
    elif stakeholder_score < 0.50:
        action = "stakeholder_legitimacy_review"
    else:
        action = "stakeholder_review_manageable"

    stakeholder_rows.append(
        {
            "review_id": row["review_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "reframe_id": row["reframe_id"],
            "reframed_problem": reframe_names.get(row["reframe_id"], row["reframe_id"]),
            "stakeholder_group": row["stakeholder_group"],
            "stakeholder_legitimacy_score": round(stakeholder_score, 4),
            "recommended_action": action,
            "inclusion_level": row["inclusion_level"],
            "burden_visibility": row["burden_visibility"],
            "knowledge_recognition": row["knowledge_recognition"],
            "interpretive_trust": row["interpretive_trust"],
            "political_safety": row["political_safety"],
            "legitimacy_signal": row["legitimacy_signal"],
            "power_challenge_risk": row["power_challenge_risk"],
        }
    )

stakeholder_rows.sort(key=lambda item: item["stakeholder_legitimacy_score"])

write_csv(
    TABLES / "stakeholder_legitimacy_review.csv",
    stakeholder_rows,
    [
        "review_id",
        "context_id",
        "context_name",
        "reframe_id",
        "reframed_problem",
        "stakeholder_group",
        "stakeholder_legitimacy_score",
        "recommended_action",
        "inclusion_level",
        "burden_visibility",
        "knowledge_recognition",
        "interpretive_trust",
        "political_safety",
        "legitimacy_signal",
        "power_challenge_risk",
    ],
)

# ---------------------------------------------------------------------
# 8. Strategist report
# ---------------------------------------------------------------------

weakest_profiles = sorted(profile_rows, key=lambda item: item["lateral_profile_score"])[:5]
highest_risks = risk_rows[:5]
weakest_frames = frame_rows[:5]
highest_assumptions = assumption_rows[:6]
top_moves = move_rows[:6]
weak_moves = sorted(move_rows, key=lambda item: item["lateral_move_score"])[:5]
top_reframes = reframe_rows[:6]
weak_integrations = sorted(integration_rows, key=lambda item: item["convergence_integration_score"])[:5]
weak_stakeholders = stakeholder_rows[:5]

report: list[str] = []

report.append("# Lateral Thinking Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic separates frame rigidity, provocation strength, analogical distance, random-entry capacity, "
    "reversal capacity, challenge quality, convergence discipline, systems integration, stakeholder legitimacy, "
    "political safety, and transformational potential. The purpose is to help strategists convert frame disruption "
    "into better problem representations, testable options, and responsible decision memory."
)
report.append("")
report.append("## Contexts requiring the most lateral-process review")
report.append("")

for item in weakest_profiles:
    report.append(
        f"- **{item['context_id']} — {item['context_name']}**: lateral profile {item['lateral_profile_score']}; "
        f"diagnosis: {item['diagnosis']}; rigidity risk {item['frame_rigidity_risk']}; drift risk {item['drift_risk']}."
    )

report.append("")
report.append("## Highest frame, drift, legitimacy, or political-safety risks")
report.append("")

for item in highest_risks:
    report.append(
        f"- **{item['context_id']} — {item['context_name']}**: frame rigidity {item['frame_rigidity_risk']}; "
        f"drift {item['drift_risk']}; legitimacy gap {item['legitimacy_gap']}; political safety gap {item['political_safety_gap']}; "
        f"diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Weakest dominant frames")
report.append("")

for item in weakest_frames:
    report.append(
        f"- **{item['frame_id']} — {item['frame_name']}** in **{item['context_name']}**: "
        f"frame quality {item['frame_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest-priority assumptions to challenge")
report.append("")

for item in highest_assumptions:
    report.append(
        f"- **{item['assumption_id']} — {item['assumption_text']}**: priority {item['challenge_priority']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strongest lateral moves")
report.append("")

for item in top_moves:
    report.append(
        f"- **{item['move_id']} — {item['move_name']}** ({item['technique']}): score {item['lateral_move_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Lateral moves needing reconstruction")
report.append("")

for item in weak_moves:
    report.append(
        f"- **{item['move_id']} — {item['move_name']}**: score {item['lateral_move_score']}; "
        f"drift risk {item['drift_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strongest reframed problems")
report.append("")

for item in top_reframes:
    report.append(
        f"- **{item['reframe_id']} — {item['reframed_problem']}**: score {item['reframe_quality_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Convergence integration gaps")
report.append("")

for item in weak_integrations:
    report.append(
        f"- **{item['integration_id']} — {item['reframed_problem']}**: integration score {item['convergence_integration_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weakest stakeholder legitimacy and political safety reviews")
report.append("")

for item in weak_stakeholders:
    report.append(
        f"- **{item['review_id']} — {item['stakeholder_group']}** in **{item['context_name']}**: "
        f"legitimacy score {item['stakeholder_legitimacy_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "The value of this workflow is disciplined frame disruption. It helps a strategist ask what frame is governing "
    "the search, which assumptions deserve challenge, which lateral moves are strategically relevant, whether reframes "
    "can be tested, whether convergence is mature enough, whether stakeholders recognize the reframe as legitimate, "
    "and whether political safety exists for constructive challenge."
)

(REPORTS / "lateral_thinking_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "weakest_profiles": weakest_profiles,
    "highest_risks": highest_risks,
    "weakest_frames": weakest_frames,
    "highest_assumptions": highest_assumptions,
    "top_moves": top_moves,
    "weak_moves": weak_moves,
    "top_reframes": top_reframes,
    "weak_integrations": weak_integrations,
    "weak_stakeholders": weak_stakeholders,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced lateral thinking diagnostics complete.")
print(f"Wrote: {TABLES / 'lateral_context_profiles.csv'}")
print(f"Wrote: {TABLES / 'frame_rigidity_risk.csv'}")
print(f"Wrote: {TABLES / 'dominant_frame_review.csv'}")
print(f"Wrote: {TABLES / 'assumption_disruption_review.csv'}")
print(f"Wrote: {TABLES / 'lateral_move_scores.csv'}")
print(f"Wrote: {TABLES / 'reframed_problem_scores.csv'}")
print(f"Wrote: {TABLES / 'convergence_integration_review.csv'}")
print(f"Wrote: {TABLES / 'stakeholder_legitimacy_review.csv'}")
print(f"Wrote: {REPORTS / 'lateral_thinking_diagnostic_report.md'}")
