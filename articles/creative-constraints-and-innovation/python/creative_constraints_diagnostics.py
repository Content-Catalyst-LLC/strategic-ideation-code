#!/usr/bin/env python3
"""
Advanced strategist-facing creative constraint diagnostics.

This dependency-light workflow uses only the Python standard library.

It produces:
- constraint context profile scores
- real vs assumed constraint classification
- rigidity and diffusion risk analysis
- constraint function map
- innovation option scores
- stakeholder constraint review
- dynamic constraint register
- capability and learning review
- a markdown strategist diagnostic report

The workflow is designed for strategy teams that need to distinguish
productive structure from unnecessary restriction, hidden power, or avoidable harm.
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


def bool_text(value: str) -> bool:
    return value.strip().lower() == "true"


contexts = read_csv(RAW / "constraint_contexts.csv")
constraints = read_csv(RAW / "constraint_register.csv")
functions = read_csv(RAW / "constraint_function_map.csv")
options = read_csv(RAW / "innovation_options.csv")
stakeholders = read_csv(RAW / "stakeholder_constraint_review.csv")
dynamics = read_csv(RAW / "dynamic_constraints.csv")
capabilities = read_csv(RAW / "capability_learning.csv")

context_names = {row["context_id"]: row["context_name"] for row in contexts}
constraint_names = {row["constraint_id"]: row["constraint_name"] for row in constraints}

# ---------------------------------------------------------------------
# 1. Constraint context profiles
# ---------------------------------------------------------------------

profile_rows: list[dict[str, object]] = []

for row in contexts:
    rigidity_pressure = (
        0.24 * f(row, "resource_pressure")
        + 0.25 * f(row, "technical_rigidity")
        + 0.27 * f(row, "institutional_rigidity")
        + 0.24 * f(row, "ecological_boundary_pressure")
    )

    productive_constraint_profile = (
        -0.10 * f(row, "resource_pressure")
        -0.10 * f(row, "technical_rigidity")
        -0.10 * f(row, "institutional_rigidity")
        + 0.12 * f(row, "ecological_boundary_pressure")
        + 0.16 * f(row, "ethical_constraint_visibility")
        + 0.16 * f(row, "search_focus")
        + 0.16 * f(row, "adaptive_opportunity")
        + 0.14 * f(row, "stakeholder_legitimacy")
        + 0.14 * f(row, "learning_capacity")
        + 0.12 * f(row, "implementation_readiness")
    )

    rigidity_risk = rigidity_pressure * (1 - f(row, "learning_capacity"))
    diffusion_risk = (1 - f(row, "search_focus")) * f(row, "adaptive_opportunity")
    legitimacy_gap = max(0.0, 0.65 - f(row, "stakeholder_legitimacy"))

    if diffusion_risk >= 0.42:
        diagnosis = "under_constrained_diffusion_risk"
    elif rigidity_risk >= 0.42:
        diagnosis = "over_constrained_rigidity_risk"
    elif legitimacy_gap >= 0.25:
        diagnosis = "stakeholder_legitimacy_gap"
    elif productive_constraint_profile >= 0.42:
        diagnosis = "productive_constraint_profile"
    else:
        diagnosis = "requires_constraint_review"

    profile_rows.append(
        {
            "context_id": row["context_id"],
            "context_name": row["context_name"],
            "context_type": row["context_type"],
            "productive_constraint_profile": round(productive_constraint_profile, 4),
            "rigidity_pressure": round(rigidity_pressure, 4),
            "rigidity_risk": round(rigidity_risk, 4),
            "diffusion_risk": round(diffusion_risk, 4),
            "legitimacy_gap": round(legitimacy_gap, 4),
            "diagnosis": diagnosis,
            "resource_pressure": row["resource_pressure"],
            "technical_rigidity": row["technical_rigidity"],
            "institutional_rigidity": row["institutional_rigidity"],
            "ecological_boundary_pressure": row["ecological_boundary_pressure"],
            "ethical_constraint_visibility": row["ethical_constraint_visibility"],
            "search_focus": row["search_focus"],
            "adaptive_opportunity": row["adaptive_opportunity"],
            "stakeholder_legitimacy": row["stakeholder_legitimacy"],
            "learning_capacity": row["learning_capacity"],
            "implementation_readiness": row["implementation_readiness"],
        }
    )

profile_rows.sort(key=lambda item: item["productive_constraint_profile"], reverse=True)

write_csv(
    TABLES / "constraint_context_profiles.csv",
    profile_rows,
    [
        "context_id",
        "context_name",
        "context_type",
        "productive_constraint_profile",
        "rigidity_pressure",
        "rigidity_risk",
        "diffusion_risk",
        "legitimacy_gap",
        "diagnosis",
        "resource_pressure",
        "technical_rigidity",
        "institutional_rigidity",
        "ecological_boundary_pressure",
        "ethical_constraint_visibility",
        "search_focus",
        "adaptive_opportunity",
        "stakeholder_legitimacy",
        "learning_capacity",
        "implementation_readiness",
    ],
)

write_csv(
    PROCESSED / "constraint_context_profiles.csv",
    profile_rows,
    [
        "context_id",
        "context_name",
        "context_type",
        "productive_constraint_profile",
        "rigidity_pressure",
        "rigidity_risk",
        "diffusion_risk",
        "legitimacy_gap",
        "diagnosis",
        "resource_pressure",
        "technical_rigidity",
        "institutional_rigidity",
        "ecological_boundary_pressure",
        "ethical_constraint_visibility",
        "search_focus",
        "adaptive_opportunity",
        "stakeholder_legitimacy",
        "learning_capacity",
        "implementation_readiness",
    ],
)

risk_rows = sorted(
    [
        {
            "context_id": item["context_id"],
            "context_name": item["context_name"],
            "rigidity_risk": item["rigidity_risk"],
            "diffusion_risk": item["diffusion_risk"],
            "legitimacy_gap": item["legitimacy_gap"],
            "diagnosis": item["diagnosis"],
        }
        for item in profile_rows
    ],
    key=lambda item: max(float(item["rigidity_risk"]), float(item["diffusion_risk"]), float(item["legitimacy_gap"])),
    reverse=True,
)

write_csv(
    TABLES / "rigidity_and_diffusion_risk.csv",
    risk_rows,
    ["context_id", "context_name", "rigidity_risk", "diffusion_risk", "legitimacy_gap", "diagnosis"],
)

# ---------------------------------------------------------------------
# 2. Constraint classification review
# ---------------------------------------------------------------------

constraint_rows: list[dict[str, object]] = []

for row in constraints:
    real = bool_text(row["is_real_constraint"])

    if real:
        respect_priority = f(row, "certainty") * f(row, "strategic_importance") * (1 - 0.35 * f(row, "redesign_potential"))
        classification = "real_constraint"
    else:
        respect_priority = f(row, "strategic_importance") * f(row, "redesign_potential") * (1 - f(row, "evidence_quality") + 0.25)
        classification = "assumed_or_political_constraint"

    if not real and respect_priority >= 0.55:
        action = "challenge_before_convergence"
    elif real and row["constraint_type"] in ("ethical", "ecological"):
        action = "treat_as_design_requirement"
    elif real and respect_priority >= 0.55:
        action = "respect_and_design_around"
    elif f(row, "burden_visibility") < 0.45:
        action = "add_burden_visibility_review"
    else:
        action = "monitor_or_sequence"

    constraint_rows.append(
        {
            "constraint_id": row["constraint_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "constraint_name": row["constraint_name"],
            "constraint_type": row["constraint_type"],
            "classification": classification,
            "constraint_priority": round(respect_priority, 4),
            "recommended_action": action,
            "certainty": row["certainty"],
            "strategic_importance": row["strategic_importance"],
            "redesign_potential": row["redesign_potential"],
            "evidence_quality": row["evidence_quality"],
            "burden_visibility": row["burden_visibility"],
            "notes": row["notes"],
        }
    )

constraint_rows.sort(key=lambda item: item["constraint_priority"], reverse=True)

write_csv(
    TABLES / "constraint_classification_review.csv",
    constraint_rows,
    [
        "constraint_id",
        "context_id",
        "context_name",
        "constraint_name",
        "constraint_type",
        "classification",
        "constraint_priority",
        "recommended_action",
        "certainty",
        "strategic_importance",
        "redesign_potential",
        "evidence_quality",
        "burden_visibility",
        "notes",
    ],
)

# ---------------------------------------------------------------------
# 3. Constraint function map
# ---------------------------------------------------------------------

function_rows: list[dict[str, object]] = []

for row in functions:
    generative_value = (
        0.18 * f(row, "focus_value")
        + 0.16 * f(row, "tradeoff_visibility")
        + 0.18 * f(row, "recombination_pressure")
        + 0.16 * f(row, "legitimacy_protection")
        + 0.16 * f(row, "learning_value")
        + 0.10 * f(row, "capability_requirement")
        - 0.16 * f(row, "suppression_risk")
    )

    if f(row, "suppression_risk") >= 0.75:
        action = "review_for_unnecessary_restriction"
    elif f(row, "legitimacy_protection") >= 0.80:
        action = "preserve_as_legitimacy_condition"
    elif generative_value >= 0.55:
        action = "use_as_design_parameter"
    else:
        action = "reframe_or_reduce_constraint"

    function_rows.append(
        {
            "function_id": row["function_id"],
            "constraint_id": row["constraint_id"],
            "constraint_name": constraint_names.get(row["constraint_id"], row["constraint_id"]),
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "generative_constraint_value": round(generative_value, 4),
            "recommended_action": action,
            "focus_value": row["focus_value"],
            "tradeoff_visibility": row["tradeoff_visibility"],
            "recombination_pressure": row["recombination_pressure"],
            "legitimacy_protection": row["legitimacy_protection"],
            "learning_value": row["learning_value"],
            "suppression_risk": row["suppression_risk"],
            "capability_requirement": row["capability_requirement"],
        }
    )

function_rows.sort(key=lambda item: item["generative_constraint_value"], reverse=True)

write_csv(
    TABLES / "constraint_function_map.csv",
    function_rows,
    [
        "function_id",
        "constraint_id",
        "constraint_name",
        "context_id",
        "context_name",
        "generative_constraint_value",
        "recommended_action",
        "focus_value",
        "tradeoff_visibility",
        "recombination_pressure",
        "legitimacy_protection",
        "learning_value",
        "suppression_risk",
        "capability_requirement",
    ],
)

# ---------------------------------------------------------------------
# 4. Innovation option scores
# ---------------------------------------------------------------------

option_rows: list[dict[str, object]] = []

for row in options:
    option_score = (
        0.12 * f(row, "novelty")
        + 0.16 * f(row, "strategic_fit")
        + 0.14 * f(row, "constraint_fit")
        + 0.14 * f(row, "adaptive_value")
        + 0.12 * f(row, "stakeholder_value")
        + 0.12 * f(row, "ecological_responsibility")
        + 0.12 * f(row, "ethical_legitimacy")
        + 0.10 * f(row, "implementation_readiness")
        - 0.08 * f(row, "assumption_burden")
    )

    if option_score >= 0.72:
        recommendation = "advance_to_evidence_gate"
    elif f(row, "ethical_legitimacy") < 0.40 or f(row, "stakeholder_value") < 0.40:
        recommendation = "stakeholder_or_ethics_review_before_advancing"
    elif f(row, "assumption_burden") >= 0.55:
        recommendation = "assumption_mapping_required"
    elif option_score >= 0.58:
        recommendation = "revise_and_retest"
    else:
        recommendation = "hold_or_reframe"

    option_rows.append(
        {
            "option_id": row["option_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "option_name": row["option_name"],
            "innovation_option_score": round(option_score, 4),
            "recommendation": recommendation,
            "novelty": row["novelty"],
            "strategic_fit": row["strategic_fit"],
            "constraint_fit": row["constraint_fit"],
            "adaptive_value": row["adaptive_value"],
            "stakeholder_value": row["stakeholder_value"],
            "ecological_responsibility": row["ecological_responsibility"],
            "ethical_legitimacy": row["ethical_legitimacy"],
            "implementation_readiness": row["implementation_readiness"],
            "assumption_burden": row["assumption_burden"],
        }
    )

option_rows.sort(key=lambda item: item["innovation_option_score"], reverse=True)

write_csv(
    TABLES / "innovation_option_scores.csv",
    option_rows,
    [
        "option_id",
        "context_id",
        "context_name",
        "option_name",
        "innovation_option_score",
        "recommendation",
        "novelty",
        "strategic_fit",
        "constraint_fit",
        "adaptive_value",
        "stakeholder_value",
        "ecological_responsibility",
        "ethical_legitimacy",
        "implementation_readiness",
        "assumption_burden",
    ],
)

# ---------------------------------------------------------------------
# 5. Stakeholder constraint review
# ---------------------------------------------------------------------

stakeholder_rows: list[dict[str, object]] = []

for row in stakeholders:
    stakeholder_score = (
        0.16 * f(row, "inclusion_level")
        + 0.18 * f(row, "influence_on_constraint_definition")
        + 0.16 * f(row, "burden_visibility")
        + 0.16 * f(row, "knowledge_recognition")
        + 0.12 * f(row, "trust_signal")
        + 0.14 * f(row, "legitimacy_signal")
        + 0.08 * f(row, "review_quality")
    )

    if f(row, "influence_on_constraint_definition") < 0.30:
        action = "include_stakeholders_before_constraint_lock_in"
    elif f(row, "burden_visibility") < 0.40:
        action = "add_burden_visibility_review"
    elif stakeholder_score < 0.55:
        action = "stakeholder_constraint_review"
    else:
        action = "stakeholder_review_manageable"

    stakeholder_rows.append(
        {
            "review_id": row["review_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "stakeholder_group": row["stakeholder_group"],
            "stakeholder_constraint_score": round(stakeholder_score, 4),
            "recommended_action": action,
            "inclusion_level": row["inclusion_level"],
            "influence_on_constraint_definition": row["influence_on_constraint_definition"],
            "burden_visibility": row["burden_visibility"],
            "knowledge_recognition": row["knowledge_recognition"],
            "trust_signal": row["trust_signal"],
            "legitimacy_signal": row["legitimacy_signal"],
            "review_quality": row["review_quality"],
        }
    )

stakeholder_rows.sort(key=lambda item: item["stakeholder_constraint_score"])

write_csv(
    TABLES / "stakeholder_constraint_review.csv",
    stakeholder_rows,
    [
        "review_id",
        "context_id",
        "context_name",
        "stakeholder_group",
        "stakeholder_constraint_score",
        "recommended_action",
        "inclusion_level",
        "influence_on_constraint_definition",
        "burden_visibility",
        "knowledge_recognition",
        "trust_signal",
        "legitimacy_signal",
        "review_quality",
    ],
)

# ---------------------------------------------------------------------
# 6. Dynamic constraint register
# ---------------------------------------------------------------------

dynamic_rows: list[dict[str, object]] = []

for row in dynamics:
    dynamic_priority = (
        0.26 * f(row, "change_likelihood")
        + 0.30 * f(row, "strategic_exposure")
        + 0.18 * f(row, "detection_confidence")
        + 0.18 * (1 - f(row, "adaptation_readiness"))
        + 0.08 * (1.0 if row["change_direction"] in ("tightening", "politically_contested") else 0.65)
    )

    if dynamic_priority >= 0.72:
        action = "urgent_dynamic_constraint_review"
    elif f(row, "adaptation_readiness") < 0.45:
        action = "build_adaptation_capacity"
    else:
        action = "monitor_and_update_assumptions"

    dynamic_rows.append(
        {
            "dynamic_id": row["dynamic_id"],
            "constraint_id": row["constraint_id"],
            "constraint_name": constraint_names.get(row["constraint_id"], row["constraint_id"]),
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "change_direction": row["change_direction"],
            "dynamic_priority": round(dynamic_priority, 4),
            "recommended_action": action,
            "change_likelihood": row["change_likelihood"],
            "strategic_exposure": row["strategic_exposure"],
            "detection_confidence": row["detection_confidence"],
            "adaptation_readiness": row["adaptation_readiness"],
            "recommended_response": row["recommended_response"],
        }
    )

dynamic_rows.sort(key=lambda item: item["dynamic_priority"], reverse=True)

write_csv(
    TABLES / "dynamic_constraint_register.csv",
    dynamic_rows,
    [
        "dynamic_id",
        "constraint_id",
        "constraint_name",
        "context_id",
        "context_name",
        "change_direction",
        "dynamic_priority",
        "recommended_action",
        "change_likelihood",
        "strategic_exposure",
        "detection_confidence",
        "adaptation_readiness",
        "recommended_response",
    ],
)

# ---------------------------------------------------------------------
# 7. Capability and learning review
# ---------------------------------------------------------------------

capability_rows: list[dict[str, object]] = []

for row in capabilities:
    learning_score = (
        0.16 * f(row, "interpretive_flexibility")
        + 0.14 * f(row, "technical_capacity")
        + 0.16 * f(row, "process_discipline")
        + 0.14 * f(row, "decision_memory")
        + 0.14 * f(row, "stakeholder_learning")
        + 0.12 * f(row, "prototype_capacity")
        + 0.14 * f(row, "revision_capacity")
        - 0.10 * f(row, "burnout_risk")
    )

    if f(row, "burnout_risk") >= 0.65:
        action = "distinguish_creative_constraint_from_harmful_strain"
    elif f(row, "decision_memory") < 0.45:
        action = "create_decision_memory_system"
    elif f(row, "revision_capacity") < 0.45:
        action = "build_revision_pathways"
    elif learning_score < 0.55:
        action = "strengthen_learning_architecture"
    else:
        action = "learning_capacity_manageable"

    capability_rows.append(
        {
            "capability_id": row["capability_id"],
            "context_id": row["context_id"],
            "context_name": context_names.get(row["context_id"], row["context_id"]),
            "capability_name": row["capability_name"],
            "constraint_learning_score": round(learning_score, 4),
            "recommended_action": action,
            "interpretive_flexibility": row["interpretive_flexibility"],
            "technical_capacity": row["technical_capacity"],
            "process_discipline": row["process_discipline"],
            "decision_memory": row["decision_memory"],
            "stakeholder_learning": row["stakeholder_learning"],
            "prototype_capacity": row["prototype_capacity"],
            "revision_capacity": row["revision_capacity"],
            "burnout_risk": row["burnout_risk"],
        }
    )

capability_rows.sort(key=lambda item: item["constraint_learning_score"], reverse=True)

write_csv(
    TABLES / "capability_learning_review.csv",
    capability_rows,
    [
        "capability_id",
        "context_id",
        "context_name",
        "capability_name",
        "constraint_learning_score",
        "recommended_action",
        "interpretive_flexibility",
        "technical_capacity",
        "process_discipline",
        "decision_memory",
        "stakeholder_learning",
        "prototype_capacity",
        "revision_capacity",
        "burnout_risk",
    ],
)

# ---------------------------------------------------------------------
# 8. Strategist report
# ---------------------------------------------------------------------

weakest_profiles = sorted(profile_rows, key=lambda item: item["productive_constraint_profile"])[:5]
highest_risks = risk_rows[:5]
highest_constraints = constraint_rows[:6]
top_function_values = function_rows[:5]
top_options = option_rows[:6]
weakest_stakeholders = stakeholder_rows[:5]
highest_dynamic = dynamic_rows[:5]
top_capabilities = capability_rows[:5]
weakest_capabilities = sorted(capability_rows, key=lambda item: item["constraint_learning_score"])[:5]

report: list[str] = []

report.append("# Creative Constraints Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic separates constraint context profiles, real-versus-assumed constraints, "
    "rigidity risk, diffusion risk, constraint function, innovation option quality, stakeholder legitimacy, "
    "dynamic constraint change, and learning capacity. The purpose is to help strategists determine whether "
    "constraints are focusing innovation, suppressing it, protecting legitimacy, or hiding assumptions."
)
report.append("")
report.append("## Contexts requiring the most constraint review")
report.append("")

for item in weakest_profiles:
    report.append(
        f"- **{item['context_id']} — {item['context_name']}**: productive constraint profile {item['productive_constraint_profile']}; "
        f"diagnosis: {item['diagnosis']}; rigidity risk {item['rigidity_risk']}; diffusion risk {item['diffusion_risk']}."
    )

report.append("")
report.append("## Highest rigidity, diffusion, or legitimacy risks")
report.append("")

for item in highest_risks:
    report.append(
        f"- **{item['context_id']} — {item['context_name']}**: rigidity {item['rigidity_risk']}; "
        f"diffusion {item['diffusion_risk']}; legitimacy gap {item['legitimacy_gap']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest-priority constraint classifications")
report.append("")

for item in highest_constraints:
    report.append(
        f"- **{item['constraint_id']} — {item['constraint_name']}**: {item['classification']}; "
        f"priority {item['constraint_priority']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Most generative constraint functions")
report.append("")

for item in top_function_values:
    report.append(
        f"- **{item['constraint_id']} — {item['constraint_name']}**: generative value {item['generative_constraint_value']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Top innovation options")
report.append("")

for item in top_options:
    report.append(
        f"- **{item['option_id']} — {item['option_name']}**: score {item['innovation_option_score']}; "
        f"recommendation: {item['recommendation']}."
    )

report.append("")
report.append("## Weakest stakeholder constraint reviews")
report.append("")

for item in weakest_stakeholders:
    report.append(
        f"- **{item['review_id']} — {item['stakeholder_group']}** in **{item['context_name']}**: "
        f"score {item['stakeholder_constraint_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest dynamic constraint priorities")
report.append("")

for item in highest_dynamic:
    report.append(
        f"- **{item['dynamic_id']} — {item['constraint_name']}**: change {item['change_direction']}; "
        f"priority {item['dynamic_priority']}; response: {item['recommended_response']}."
    )

report.append("")
report.append("## Strongest learning capabilities")
report.append("")

for item in top_capabilities:
    report.append(
        f"- **{item['capability_id']} — {item['capability_name']}**: learning score {item['constraint_learning_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weakest learning capabilities")
report.append("")

for item in weakest_capabilities:
    report.append(
        f"- **{item['capability_id']} — {item['capability_name']}**: learning score {item['constraint_learning_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "The value of this workflow is disciplined constraint reasoning. It helps a strategist ask whether "
    "a boundary is real, assumed, ethical, ecological, political, temporary, or redesignable; whether it "
    "focuses or suppresses creativity; whether stakeholders experience it as legitimate; and whether the "
    "organization has enough capability to transform constraint into learning rather than strain."
)

(REPORTS / "creative_constraints_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "weakest_profiles": weakest_profiles,
    "highest_risks": highest_risks,
    "highest_constraints": highest_constraints,
    "top_function_values": top_function_values,
    "top_options": top_options,
    "weakest_stakeholders": weakest_stakeholders,
    "highest_dynamic": highest_dynamic,
    "top_capabilities": top_capabilities,
    "weakest_capabilities": weakest_capabilities,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced creative constraints diagnostics complete.")
print(f"Wrote: {TABLES / 'constraint_context_profiles.csv'}")
print(f"Wrote: {TABLES / 'constraint_classification_review.csv'}")
print(f"Wrote: {TABLES / 'rigidity_and_diffusion_risk.csv'}")
print(f"Wrote: {TABLES / 'constraint_function_map.csv'}")
print(f"Wrote: {TABLES / 'stakeholder_constraint_review.csv'}")
print(f"Wrote: {TABLES / 'dynamic_constraint_register.csv'}")
print(f"Wrote: {TABLES / 'capability_learning_review.csv'}")
print(f"Wrote: {REPORTS / 'creative_constraints_diagnostic_report.md'}")
