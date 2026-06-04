#!/usr/bin/env python3
"""
Advanced strategist-facing heuristics diagnostics for strategic ideation.

This dependency-light workflow uses only the Python standard library.

It produces:
- heuristic context profile scores
- premature closure and recognition trap risk analysis
- search-breadth scores
- heuristic use review
- institutional shortcut audit
- complexity-fit review
- stopping-rule governance review
- intervention recommendations
- a markdown strategist diagnostic report

The workflow is designed for strategy teams that need to diagnose which
shortcuts are governing ideation before options are formally evaluated.
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


contexts = read_csv(RAW / "heuristic_contexts.csv")
uses = read_csv(RAW / "heuristic_use_cases.csv")
ideas = read_csv(RAW / "idea_search_inventory.csv")
shortcuts = read_csv(RAW / "institutional_shortcuts.csv")
complexity = read_csv(RAW / "complexity_fit.csv")
stopping_rules = read_csv(RAW / "stopping_rules.csv")
interventions = read_csv(RAW / "intervention_library.csv")

context_names = {row["context_id"]: row["context_name"] for row in contexts}

# ---------------------------------------------------------------------
# 1. Heuristic context profiles
# ---------------------------------------------------------------------

profile_rows: list[dict[str, object]] = []

for row in contexts:
    closure_pressure = f(row, "anchoring_intensity") * f(row, "satisficing_tendency")
    recognition_trap_risk = f(row, "recognition_comfort") * (1 - f(row, "exploratory_diversity"))
    institutional_autopilot_risk = f(row, "default_gravity") * (1 - f(row, "decision_memory_quality"))
    social_proof_risk = f(row, "social_proof_pressure") * (1 - f(row, "source_domain_diversity"))
    complexity_check_gap = max(0.0, 0.70 - f(row, "systems_check_quality"))
    stakeholder_gap = max(0.0, 0.60 - f(row, "stakeholder_variation"))

    heuristic_profile = (
        -0.11 * f(row, "availability_dependence")
        -0.11 * f(row, "anchoring_intensity")
        -0.10 * f(row, "recognition_comfort")
        -0.11 * f(row, "satisficing_tendency")
        -0.07 * f(row, "affect_pressure")
        -0.08 * f(row, "default_gravity")
        -0.06 * f(row, "social_proof_pressure")
        + 0.17 * f(row, "exploratory_diversity")
        + 0.13 * f(row, "stakeholder_variation")
        + 0.13 * f(row, "source_domain_diversity")
        + 0.14 * f(row, "systems_check_quality")
        + 0.07 * f(row, "political_safety")
        + 0.08 * f(row, "decision_memory_quality")
    )

    if closure_pressure >= 0.55:
        diagnosis = "premature_closure_risk"
    elif recognition_trap_risk >= 0.50:
        diagnosis = "recognition_trap_risk"
    elif institutional_autopilot_risk >= 0.50:
        diagnosis = "institutional_autopilot_risk"
    elif social_proof_risk >= 0.45:
        diagnosis = "social_proof_local_search_risk"
    elif stakeholder_gap >= 0.25:
        diagnosis = "stakeholder_visibility_gap"
    elif complexity_check_gap >= 0.25:
        diagnosis = "systems_check_gap"
    elif heuristic_profile >= 0.20:
        diagnosis = "stronger_heuristic_ecology"
    else:
        diagnosis = "requires_heuristic_review"

    profile_rows.append(
        {
            "context_id": row["context_id"],
            "context_name": row["context_name"],
            "context_type": row["context_type"],
            "heuristic_profile_score": round(heuristic_profile, 4),
            "closure_pressure": round(closure_pressure, 4),
            "recognition_trap_risk": round(recognition_trap_risk, 4),
            "institutional_autopilot_risk": round(institutional_autopilot_risk, 4),
            "social_proof_risk": round(social_proof_risk, 4),
            "complexity_check_gap": round(complexity_check_gap, 4),
            "stakeholder_gap": round(stakeholder_gap, 4),
            "diagnosis": diagnosis,
            "availability_dependence": row["availability_dependence"],
            "anchoring_intensity": row["anchoring_intensity"],
            "recognition_comfort": row["recognition_comfort"],
            "satisficing_tendency": row["satisficing_tendency"],
            "affect_pressure": row["affect_pressure"],
            "default_gravity": row["default_gravity"],
            "social_proof_pressure": row["social_proof_pressure"],
            "exploratory_diversity": row["exploratory_diversity"],
            "stakeholder_variation": row["stakeholder_variation"],
            "source_domain_diversity": row["source_domain_diversity"],
            "systems_check_quality": row["systems_check_quality"],
            "political_safety": row["political_safety"],
            "decision_memory_quality": row["decision_memory_quality"],
        }
    )

profile_rows.sort(key=lambda item: item["heuristic_profile_score"], reverse=True)

profile_fields = [
    "context_id",
    "context_name",
    "context_type",
    "heuristic_profile_score",
    "closure_pressure",
    "recognition_trap_risk",
    "institutional_autopilot_risk",
    "social_proof_risk",
    "complexity_check_gap",
    "stakeholder_gap",
    "diagnosis",
    "availability_dependence",
    "anchoring_intensity",
    "recognition_comfort",
    "satisficing_tendency",
    "affect_pressure",
    "default_gravity",
    "social_proof_pressure",
    "exploratory_diversity",
    "stakeholder_variation",
    "source_domain_diversity",
    "systems_check_quality",
    "political_safety",
    "decision_memory_quality",
]

write_csv(TABLES / "heuristic_context_profiles.csv", profile_rows, profile_fields)
write_csv(PROCESSED / "heuristic_context_profiles.csv", profile_rows, profile_fields)

risk_rows = sorted(
    [
        {
            "context_id": row["context_id"],
            "context_name": row["context_name"],
            "closure_pressure": row["closure_pressure"],
            "recognition_trap_risk": row["recognition_trap_risk"],
            "institutional_autopilot_risk": row["institutional_autopilot_risk"],
            "social_proof_risk": row["social_proof_risk"],
            "complexity_check_gap": row["complexity_check_gap"],
            "stakeholder_gap": row["stakeholder_gap"],
            "diagnosis": row["diagnosis"],
        }
        for row in profile_rows
    ],
    key=lambda item: max(
        float(item["closure_pressure"]),
        float(item["recognition_trap_risk"]),
        float(item["institutional_autopilot_risk"]),
        float(item["social_proof_risk"]),
        float(item["complexity_check_gap"]),
        float(item["stakeholder_gap"]),
    ),
    reverse=True,
)

write_csv(
    TABLES / "premature_closure_risk.csv",
    risk_rows,
    [
        "context_id",
        "context_name",
        "closure_pressure",
        "recognition_trap_risk",
        "institutional_autopilot_risk",
        "social_proof_risk",
        "complexity_check_gap",
        "stakeholder_gap",
        "diagnosis",
    ],
)

# ---------------------------------------------------------------------
# 2. Heuristic use review
# ---------------------------------------------------------------------

use_rows: list[dict[str, object]] = []

for row in uses:
    heuristic_value = (
        0.12 * f(row, "search_speed_gain")
        - 0.12 * f(row, "search_depth_loss")
        + 0.16 * f(row, "strategic_relevance")
        + 0.16 * f(row, "fit_to_context")
        - 0.14 * f(row, "misuse_risk")
        + 0.12 * f(row, "stakeholder_visibility")
        + 0.14 * f(row, "systems_fit")
        + 0.14 * f(row, "evidence_pathway")
    )

    if f(row, "misuse_risk") >= 0.75:
        action = "high_misuse_risk_review_required"
    elif f(row, "search_depth_loss") >= 0.70:
        action = "pair_with_divergence_or_reframing"
    elif f(row, "systems_fit") < 0.40:
        action = "systems_fit_review_before_use"
    elif heuristic_value >= 0.45:
        action = "use_deliberately_with_governance"
    else:
        action = "revise_or_replace_heuristic"

    use_rows.append(
        {
            "heuristic_id": row["heuristic_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "heuristic_name": row["heuristic_name"],
            "heuristic_family": row["heuristic_family"],
            "use_phase": row["use_phase"],
            "heuristic_value_score": round(heuristic_value, 4),
            "recommended_action": action,
            "search_speed_gain": row["search_speed_gain"],
            "search_depth_loss": row["search_depth_loss"],
            "strategic_relevance": row["strategic_relevance"],
            "fit_to_context": row["fit_to_context"],
            "misuse_risk": row["misuse_risk"],
            "stakeholder_visibility": row["stakeholder_visibility"],
            "systems_fit": row["systems_fit"],
            "evidence_pathway": row["evidence_pathway"],
        }
    )

use_rows.sort(key=lambda item: item["heuristic_value_score"], reverse=True)

write_csv(
    TABLES / "heuristic_use_review.csv",
    use_rows,
    [
        "heuristic_id",
        "context_id",
        "context_name",
        "heuristic_name",
        "heuristic_family",
        "use_phase",
        "heuristic_value_score",
        "recommended_action",
        "search_speed_gain",
        "search_depth_loss",
        "strategic_relevance",
        "fit_to_context",
        "misuse_risk",
        "stakeholder_visibility",
        "systems_fit",
        "evidence_pathway",
    ],
)

# ---------------------------------------------------------------------
# 3. Search-breadth scores
# ---------------------------------------------------------------------

idea_rows: list[dict[str, object]] = []

for row in ideas:
    breadth_score = (
        0.12 * f(row, "stakeholder_visibility")
        + 0.12 * f(row, "novelty_level")
        + 0.12 * f(row, "evidence_pathway")
        + 0.14 * f(row, "strategic_relevance")
        + 0.10 * f(row, "implementation_pathway")
        + 0.16 * f(row, "search_breadth")
        - 0.12 * f(row, "closure_pressure")
        - 0.08 * f(row, "assumption_burden")
    )

    if f(row, "closure_pressure") >= 0.80:
        action = "premature_closure_check"
    elif f(row, "search_breadth") < 0.35:
        action = "expand_search_before_evaluation"
    elif f(row, "stakeholder_visibility") < 0.40:
        action = "add_stakeholder_visibility_review"
    elif breadth_score >= 0.45:
        action = "strong_search_breadth_contributor"
    else:
        action = "revise_or_defer"

    idea_rows.append(
        {
            "idea_id": row["idea_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "idea_name": row["idea_name"],
            "dominant_heuristic": row["dominant_heuristic"],
            "frame_family": row["frame_family"],
            "source_domain": row["source_domain"],
            "search_breadth_score": round(breadth_score, 4),
            "recommended_action": action,
            "stakeholder_visibility": row["stakeholder_visibility"],
            "novelty_level": row["novelty_level"],
            "evidence_pathway": row["evidence_pathway"],
            "strategic_relevance": row["strategic_relevance"],
            "implementation_pathway": row["implementation_pathway"],
            "system_level": row["system_level"],
            "search_breadth": row["search_breadth"],
            "closure_pressure": row["closure_pressure"],
            "assumption_burden": row["assumption_burden"],
        }
    )

idea_rows.sort(key=lambda item: item["search_breadth_score"], reverse=True)

write_csv(
    TABLES / "search_breadth_scores.csv",
    idea_rows,
    [
        "idea_id",
        "context_id",
        "context_name",
        "idea_name",
        "dominant_heuristic",
        "frame_family",
        "source_domain",
        "search_breadth_score",
        "recommended_action",
        "stakeholder_visibility",
        "novelty_level",
        "evidence_pathway",
        "strategic_relevance",
        "implementation_pathway",
        "system_level",
        "search_breadth",
        "closure_pressure",
        "assumption_burden",
    ],
)

# ---------------------------------------------------------------------
# 4. Institutional shortcut audit
# ---------------------------------------------------------------------

shortcut_rows: list[dict[str, object]] = []

for row in shortcuts:
    shortcut_risk = (
        0.16 * f(row, "search_narrowing_risk")
        + 0.14 * f(row, "metric_lock_in")
        + 0.14 * f(row, "template_dependency")
        + 0.14 * f(row, "leadership_preference_pressure")
        + 0.14 * f(row, "stakeholder_exclusion")
        + 0.14 * f(row, "revision_difficulty")
        + 0.14 * f(row, "strategic_obsolescence_risk")
        - 0.08 * f(row, "coordination_benefit")
    )

    if f(row, "strategic_obsolescence_risk") >= 0.70:
        action = "revalidate_shortcut_against_current_strategy"
    elif f(row, "stakeholder_exclusion") >= 0.65:
        action = "stakeholder_visibility_review_required"
    elif shortcut_risk >= 0.55:
        action = "institutional_shortcut_audit_required"
    else:
        action = "shortcut_manageable_with_monitoring"

    shortcut_rows.append(
        {
            "shortcut_id": row["shortcut_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "shortcut_name": row["shortcut_name"],
            "shortcut_type": row["shortcut_type"],
            "institutional_shortcut_risk": round(shortcut_risk, 4),
            "recommended_action": action,
            "coordination_benefit": row["coordination_benefit"],
            "search_narrowing_risk": row["search_narrowing_risk"],
            "metric_lock_in": row["metric_lock_in"],
            "template_dependency": row["template_dependency"],
            "leadership_preference_pressure": row["leadership_preference_pressure"],
            "stakeholder_exclusion": row["stakeholder_exclusion"],
            "revision_difficulty": row["revision_difficulty"],
            "strategic_obsolescence_risk": row["strategic_obsolescence_risk"],
        }
    )

shortcut_rows.sort(key=lambda item: item["institutional_shortcut_risk"], reverse=True)

write_csv(
    TABLES / "institutional_shortcut_audit.csv",
    shortcut_rows,
    [
        "shortcut_id",
        "context_id",
        "context_name",
        "shortcut_name",
        "shortcut_type",
        "institutional_shortcut_risk",
        "recommended_action",
        "coordination_benefit",
        "search_narrowing_risk",
        "metric_lock_in",
        "template_dependency",
        "leadership_preference_pressure",
        "stakeholder_exclusion",
        "revision_difficulty",
        "strategic_obsolescence_risk",
    ],
)

# ---------------------------------------------------------------------
# 5. Complexity-fit review
# ---------------------------------------------------------------------

complexity_rows: list[dict[str, object]] = []

for row in complexity:
    fit_score = (
        0.16 * f(row, "feedback_awareness")
        + 0.14 * f(row, "delay_awareness")
        + 0.16 * f(row, "second_order_review")
        + 0.14 * f(row, "adaptation_review")
        + 0.14 * f(row, "boundary_quality")
        + 0.16 * f(row, "robustness_across_scenarios")
        - 0.10 * f(row, "complexity_mismatch_risk")
    )

    if f(row, "complexity_mismatch_risk") >= 0.75:
        action = "replace_simple_heuristic_with_systems_review"
    elif f(row, "second_order_review") < 0.35:
        action = "add_second_order_effects_review"
    elif f(row, "feedback_awareness") < 0.40:
        action = "map_feedback_before_convergence"
    elif fit_score >= 0.55:
        action = "complexity_fit_manageable"
    else:
        action = "strengthen_complexity_fit"

    complexity_rows.append(
        {
            "fit_id": row["fit_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "heuristic_name": row["heuristic_name"],
            "assumed_environment": row["assumed_environment"],
            "actual_environment": row["actual_environment"],
            "complexity_fit_score": round(fit_score, 4),
            "recommended_action": action,
            "feedback_awareness": row["feedback_awareness"],
            "delay_awareness": row["delay_awareness"],
            "second_order_review": row["second_order_review"],
            "adaptation_review": row["adaptation_review"],
            "boundary_quality": row["boundary_quality"],
            "robustness_across_scenarios": row["robustness_across_scenarios"],
            "complexity_mismatch_risk": row["complexity_mismatch_risk"],
        }
    )

complexity_rows.sort(key=lambda item: item["complexity_fit_score"])

write_csv(
    TABLES / "complexity_fit_review.csv",
    complexity_rows,
    [
        "fit_id",
        "context_id",
        "context_name",
        "heuristic_name",
        "assumed_environment",
        "actual_environment",
        "complexity_fit_score",
        "recommended_action",
        "feedback_awareness",
        "delay_awareness",
        "second_order_review",
        "adaptation_review",
        "boundary_quality",
        "robustness_across_scenarios",
        "complexity_mismatch_risk",
    ],
)

# ---------------------------------------------------------------------
# 6. Stopping-rule governance
# ---------------------------------------------------------------------

stopping_rows: list[dict[str, object]] = []

for row in stopping_rules:
    closure_quality = (
        0.14 * f(row, "option_diversity_requirement")
        + 0.14 * f(row, "stakeholder_coverage_requirement")
        + 0.14 * f(row, "source_domain_requirement")
        + 0.16 * f(row, "systems_review_requirement")
        + 0.14 * f(row, "evidence_threshold")
        - 0.10 * f(row, "political_pressure")
        + 0.14 * f(row, "closure_quality")
        + 0.14 * f(row, "reopen_trigger_quality")
    )

    if f(row, "political_pressure") >= 0.75 and f(row, "option_diversity_requirement") < 0.40:
        action = "political_premature_closure_risk"
    elif f(row, "systems_review_requirement") < 0.40:
        action = "add_systems_review_before_closure"
    elif f(row, "reopen_trigger_quality") < 0.40:
        action = "define_reopen_trigger"
    elif closure_quality >= 0.60:
        action = "stopping_rule_manageable"
    else:
        action = "strengthen_stopping_rule"

    stopping_rows.append(
        {
            "rule_id": row["rule_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "rule_name": row["rule_name"],
            "closure_trigger": row["closure_trigger"],
            "stopping_rule_quality_score": round(closure_quality, 4),
            "recommended_action": action,
            "option_diversity_requirement": row["option_diversity_requirement"],
            "stakeholder_coverage_requirement": row["stakeholder_coverage_requirement"],
            "source_domain_requirement": row["source_domain_requirement"],
            "systems_review_requirement": row["systems_review_requirement"],
            "evidence_threshold": row["evidence_threshold"],
            "political_pressure": row["political_pressure"],
            "closure_quality": row["closure_quality"],
            "reopen_trigger_quality": row["reopen_trigger_quality"],
        }
    )

stopping_rows.sort(key=lambda item: item["stopping_rule_quality_score"])

write_csv(
    TABLES / "stopping_rule_review.csv",
    stopping_rows,
    [
        "rule_id",
        "context_id",
        "context_name",
        "rule_name",
        "closure_trigger",
        "stopping_rule_quality_score",
        "recommended_action",
        "option_diversity_requirement",
        "stakeholder_coverage_requirement",
        "source_domain_requirement",
        "systems_review_requirement",
        "evidence_threshold",
        "political_pressure",
        "closure_quality",
        "reopen_trigger_quality",
    ],
)

# ---------------------------------------------------------------------
# 7. Intervention recommendations
# ---------------------------------------------------------------------

intervention_rows: list[dict[str, object]] = []

for row in interventions:
    intervention_value = (
        0.18 * f(row, "search_breadth_gain")
        + 0.14 * f(row, "stakeholder_gain")
        + 0.16 * f(row, "systems_fit_gain")
        + 0.16 * f(row, "closure_quality_gain")
        + 0.16 * f(row, "decision_memory_gain")
        - 0.10 * f(row, "process_cost")
        - 0.08 * f(row, "implementation_complexity")
        - 0.08 * f(row, "political_safety_need")
    )

    if f(row, "political_safety_need") >= 0.50:
        action = "requires_leadership_protection"
    elif intervention_value >= 0.45:
        action = "high_value_heuristic_intervention"
    else:
        action = "supporting_intervention"

    intervention_rows.append(
        {
            "intervention_id": row["intervention_id"],
            "intervention_name": row["intervention_name"],
            "target_heuristic_risk": row["target_heuristic_risk"],
            "intervention_value_score": round(intervention_value, 4),
            "recommended_action": action,
            "process_cost": row["process_cost"],
            "implementation_complexity": row["implementation_complexity"],
            "search_breadth_gain": row["search_breadth_gain"],
            "stakeholder_gain": row["stakeholder_gain"],
            "systems_fit_gain": row["systems_fit_gain"],
            "closure_quality_gain": row["closure_quality_gain"],
            "decision_memory_gain": row["decision_memory_gain"],
            "political_safety_need": row["political_safety_need"],
        }
    )

intervention_rows.sort(key=lambda item: item["intervention_value_score"], reverse=True)

write_csv(
    TABLES / "intervention_recommendations.csv",
    intervention_rows,
    [
        "intervention_id",
        "intervention_name",
        "target_heuristic_risk",
        "intervention_value_score",
        "recommended_action",
        "process_cost",
        "implementation_complexity",
        "search_breadth_gain",
        "stakeholder_gain",
        "systems_fit_gain",
        "closure_quality_gain",
        "decision_memory_gain",
        "political_safety_need",
    ],
)

# ---------------------------------------------------------------------
# 8. Strategist report
# ---------------------------------------------------------------------

weakest_profiles = sorted(profile_rows, key=lambda item: item["heuristic_profile_score"])[:5]
highest_risks = risk_rows[:5]
top_uses = use_rows[:6]
weak_uses = sorted(use_rows, key=lambda item: item["heuristic_value_score"])[:5]
top_ideas = idea_rows[:6]
weak_ideas = sorted(idea_rows, key=lambda item: item["search_breadth_score"])[:5]
highest_shortcuts = shortcut_rows[:5]
weak_complexity = complexity_rows[:5]
weak_stopping = stopping_rows[:5]
top_interventions = intervention_rows[:6]

report: list[str] = []

report.append("# Heuristics in Strategic Ideation Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic separates heuristic profile quality, closure pressure, recognition-trap risk, institutional autopilot, "
    "social-proof local search, complexity-check gaps, stakeholder gaps, search breadth, heuristic misuse risk, institutional "
    "shortcut risk, complexity fit, stopping-rule governance, and intervention value. The purpose is to help strategists "
    "diagnose which shortcuts are governing ideation before formal evaluation begins."
)
report.append("")
report.append("## Contexts requiring the most heuristic review")
report.append("")

for item in weakest_profiles:
    report.append(
        f"- **{item['context_id']} — {item['context_name']}**: heuristic profile {item['heuristic_profile_score']}; "
        f"closure pressure {item['closure_pressure']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest closure, recognition, institutional, or complexity risks")
report.append("")

for item in highest_risks:
    report.append(
        f"- **{item['context_id']} — {item['context_name']}**: closure {item['closure_pressure']}; "
        f"recognition trap {item['recognition_trap_risk']}; institutional autopilot {item['institutional_autopilot_risk']}; "
        f"social proof {item['social_proof_risk']}; complexity gap {item['complexity_check_gap']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Strongest deliberate heuristic uses")
report.append("")

for item in top_uses:
    report.append(
        f"- **{item['heuristic_id']} — {item['heuristic_name']}** ({item['heuristic_family']}): "
        f"value {item['heuristic_value_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Heuristics needing replacement or governance")
report.append("")

for item in weak_uses:
    report.append(
        f"- **{item['heuristic_id']} — {item['heuristic_name']}**: value {item['heuristic_value_score']}; "
        f"misuse risk {item['misuse_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strongest search-breadth contributors")
report.append("")

for item in top_ideas:
    report.append(
        f"- **{item['idea_id']} — {item['idea_name']}**: search breadth score {item['search_breadth_score']}; "
        f"dominant heuristic: {item['dominant_heuristic']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weakest search-breadth contributors")
report.append("")

for item in weak_ideas:
    report.append(
        f"- **{item['idea_id']} — {item['idea_name']}**: search breadth score {item['search_breadth_score']}; "
        f"closure pressure {item['closure_pressure']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest institutional shortcut risks")
report.append("")

for item in highest_shortcuts:
    report.append(
        f"- **{item['shortcut_id']} — {item['shortcut_name']}**: risk {item['institutional_shortcut_risk']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weakest complexity-fit reviews")
report.append("")

for item in weak_complexity:
    report.append(
        f"- **{item['fit_id']} — {item['heuristic_name']}** in **{item['context_name']}**: "
        f"complexity fit {item['complexity_fit_score']}; mismatch risk {item['complexity_mismatch_risk']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weakest stopping-rule governance")
report.append("")

for item in weak_stopping:
    report.append(
        f"- **{item['rule_id']} — {item['rule_name']}**: stopping-rule quality {item['stopping_rule_quality_score']}; "
        f"trigger: {item['closure_trigger']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest-value heuristic interventions")
report.append("")

for item in top_interventions:
    report.append(
        f"- **{item['intervention_id']} — {item['intervention_name']}**: value {item['intervention_value_score']}; "
        f"target: {item['target_heuristic_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "The value of this workflow is heuristic-aware ideation design. It helps a strategist ask which shortcuts "
    "generated the option space, when speed became premature closure, when recognition became a trap, when institutional "
    "routines defined what counted as realistic, whether heuristics fit system complexity, and how intervention design "
    "can create a richer heuristic ecology."
)

(REPORTS / "heuristics_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "weakest_profiles": weakest_profiles,
    "highest_risks": highest_risks,
    "top_uses": top_uses,
    "weak_uses": weak_uses,
    "top_ideas": top_ideas,
    "weak_ideas": weak_ideas,
    "highest_shortcuts": highest_shortcuts,
    "weak_complexity": weak_complexity,
    "weak_stopping": weak_stopping,
    "top_interventions": top_interventions,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced heuristics diagnostics complete.")
print(f"Wrote: {TABLES / 'heuristic_context_profiles.csv'}")
print(f"Wrote: {TABLES / 'premature_closure_risk.csv'}")
print(f"Wrote: {TABLES / 'heuristic_use_review.csv'}")
print(f"Wrote: {TABLES / 'search_breadth_scores.csv'}")
print(f"Wrote: {TABLES / 'institutional_shortcut_audit.csv'}")
print(f"Wrote: {TABLES / 'complexity_fit_review.csv'}")
print(f"Wrote: {TABLES / 'stopping_rule_review.csv'}")
print(f"Wrote: {TABLES / 'intervention_recommendations.csv'}")
print(f"Wrote: {REPORTS / 'heuristics_diagnostic_report.md'}")
