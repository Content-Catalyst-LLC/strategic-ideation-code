#!/usr/bin/env python3
"""
Advanced strategist-facing analogical transfer diagnostics.

This dependency-light workflow uses only the Python standard library.

It produces:
- analogical strategy profile scores
- source-target mapping scores
- surface-distraction risk analysis
- adaptation-readiness review
- rival analogy comparison
- stakeholder legitimacy review
- transfer hypothesis register
- a markdown strategist diagnostic report

The workflow is designed for strategy teams that need to distinguish
deep structural transfer from surface resemblance, prestige borrowing,
context neglect, and power-blind imitation.
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


strategies = read_csv(RAW / "analogical_strategies.csv")
sources = read_csv(RAW / "source_domains.csv")
targets = read_csv(RAW / "target_problems.csv")
mappings = read_csv(RAW / "source_target_mappings.csv")
adaptations = read_csv(RAW / "adaptation_tests.csv")
rivals = read_csv(RAW / "rival_analogies.csv")
stakeholders = read_csv(RAW / "stakeholder_legitimacy.csv")
hypotheses = read_csv(RAW / "transfer_hypotheses.csv")

strategy_names = {row["strategy_id"]: row["strategy_name"] for row in strategies}
source_names = {row["source_id"]: row["source_name"] for row in sources}
target_names = {row["target_id"]: row["target_name"] for row in targets}
mapping_labels = {row["mapping_id"]: f"{source_names.get(row['source_id'], row['source_id'])} → {target_names.get(row['target_id'], row['target_id'])}" for row in mappings}

# ---------------------------------------------------------------------
# 1. Analogical strategy profile
# ---------------------------------------------------------------------

profile_rows: list[dict[str, object]] = []

for row in strategies:
    analogy_profile = (
        0.20 * f(row, "structural_fit")
        + 0.16 * f(row, "functional_fit")
        - 0.16 * f(row, "surface_distraction")
        + 0.16 * f(row, "adaptation_quality")
        + 0.12 * f(row, "context_sensitivity")
        + 0.08 * f(row, "stakeholder_legitimacy")
        + 0.08 * f(row, "dynamic_compatibility")
        + 0.12 * f(row, "innovation_potential")
        + 0.08 * f(row, "evidence_strength")
    )

    surface_risk = f(row, "surface_distraction") * (1 - f(row, "structural_fit"))
    transfer_readiness = (
        0.28 * f(row, "structural_fit")
        + 0.20 * f(row, "functional_fit")
        + 0.20 * f(row, "adaptation_quality")
        + 0.14 * f(row, "context_sensitivity")
        + 0.10 * f(row, "dynamic_compatibility")
        + 0.08 * f(row, "stakeholder_legitimacy")
    )

    if surface_risk >= 0.50:
        diagnosis = "surface_analogy_risk"
    elif f(row, "adaptation_quality") < 0.45:
        diagnosis = "weak_adaptation"
    elif f(row, "dynamic_compatibility") < 0.50:
        diagnosis = "dynamic_compatibility_gap"
    elif f(row, "stakeholder_legitimacy") < 0.50:
        diagnosis = "stakeholder_legitimacy_gap"
    elif analogy_profile >= 0.60:
        diagnosis = "strong_transfer_candidate"
    else:
        diagnosis = "requires_analogy_review"

    profile_rows.append(
        {
            "strategy_id": row["strategy_id"],
            "strategy_name": row["strategy_name"],
            "strategy_type": row["strategy_type"],
            "analogy_profile_score": round(analogy_profile, 4),
            "surface_distraction_risk": round(surface_risk, 4),
            "transfer_readiness": round(transfer_readiness, 4),
            "diagnosis": diagnosis,
            "source_distance": row["source_distance"],
            "structural_fit": row["structural_fit"],
            "functional_fit": row["functional_fit"],
            "surface_distraction": row["surface_distraction"],
            "adaptation_quality": row["adaptation_quality"],
            "context_sensitivity": row["context_sensitivity"],
            "stakeholder_legitimacy": row["stakeholder_legitimacy"],
            "dynamic_compatibility": row["dynamic_compatibility"],
            "innovation_potential": row["innovation_potential"],
            "evidence_strength": row["evidence_strength"],
        }
    )

profile_rows.sort(key=lambda item: item["analogy_profile_score"], reverse=True)

write_csv(
    TABLES / "analogical_strategy_profiles.csv",
    profile_rows,
    [
        "strategy_id",
        "strategy_name",
        "strategy_type",
        "analogy_profile_score",
        "surface_distraction_risk",
        "transfer_readiness",
        "diagnosis",
        "source_distance",
        "structural_fit",
        "functional_fit",
        "surface_distraction",
        "adaptation_quality",
        "context_sensitivity",
        "stakeholder_legitimacy",
        "dynamic_compatibility",
        "innovation_potential",
        "evidence_strength",
    ],
)

write_csv(
    PROCESSED / "analogical_strategy_profiles.csv",
    profile_rows,
    [
        "strategy_id",
        "strategy_name",
        "strategy_type",
        "analogy_profile_score",
        "surface_distraction_risk",
        "transfer_readiness",
        "diagnosis",
        "source_distance",
        "structural_fit",
        "functional_fit",
        "surface_distraction",
        "adaptation_quality",
        "context_sensitivity",
        "stakeholder_legitimacy",
        "dynamic_compatibility",
        "innovation_potential",
        "evidence_strength",
    ],
)

surface_rows = sorted(
    [
        {
            "strategy_id": row["strategy_id"],
            "strategy_name": row["strategy_name"],
            "surface_distraction_risk": row["surface_distraction_risk"],
            "transfer_readiness": row["transfer_readiness"],
            "diagnosis": row["diagnosis"],
            "recommended_action": "replace_surface_resemblance_with_relational_mapping"
            if float(row["surface_distraction_risk"]) >= 0.50
            else "monitor",
        }
        for row in profile_rows
    ],
    key=lambda item: float(item["surface_distraction_risk"]),
    reverse=True,
)

write_csv(
    TABLES / "surface_distraction_risk.csv",
    surface_rows,
    ["strategy_id", "strategy_name", "surface_distraction_risk", "transfer_readiness", "diagnosis", "recommended_action"],
)

# ---------------------------------------------------------------------
# 2. Source-domain quality
# ---------------------------------------------------------------------

source_rows: list[dict[str, object]] = []

for row in sources:
    source_quality = (
        0.22 * f(row, "relational_clarity")
        + 0.20 * f(row, "mechanism_visibility")
        + 0.18 * f(row, "constraint_visibility")
        + 0.16 * f(row, "failure_mode_visibility")
        - 0.12 * f(row, "prestige_pressure")
        - 0.06 * f(row, "transfer_complexity")
        + 0.12 * f(row, "source_distance")
    )

    if f(row, "prestige_pressure") >= 0.70:
        action = "audit_for_prestige_transfer"
    elif f(row, "relational_clarity") < 0.50:
        action = "clarify_relational_structure"
    elif source_quality >= 0.62:
        action = "strong_source_candidate"
    else:
        action = "source_requires_review"

    source_rows.append(
        {
            "source_id": row["source_id"],
            "source_name": row["source_name"],
            "source_domain_type": row["source_domain_type"],
            "source_quality_score": round(source_quality, 4),
            "recommended_action": action,
            "source_distance": row["source_distance"],
            "relational_clarity": row["relational_clarity"],
            "mechanism_visibility": row["mechanism_visibility"],
            "constraint_visibility": row["constraint_visibility"],
            "failure_mode_visibility": row["failure_mode_visibility"],
            "prestige_pressure": row["prestige_pressure"],
            "transfer_complexity": row["transfer_complexity"],
        }
    )

source_rows.sort(key=lambda item: item["source_quality_score"], reverse=True)

write_csv(
    TABLES / "source_domain_quality.csv",
    source_rows,
    [
        "source_id",
        "source_name",
        "source_domain_type",
        "source_quality_score",
        "recommended_action",
        "source_distance",
        "relational_clarity",
        "mechanism_visibility",
        "constraint_visibility",
        "failure_mode_visibility",
        "prestige_pressure",
        "transfer_complexity",
    ],
)

# ---------------------------------------------------------------------
# 3. Source-target mapping scores
# ---------------------------------------------------------------------

mapping_rows: list[dict[str, object]] = []

for row in mappings:
    mapping_score = (
        0.14 * f(row, "actor_correspondence")
        + 0.20 * f(row, "relation_correspondence")
        + 0.14 * f(row, "flow_correspondence")
        + 0.14 * f(row, "constraint_correspondence")
        + 0.14 * f(row, "feedback_correspondence")
        + 0.12 * f(row, "failure_mode_correspondence")
        + 0.08 * f(row, "breakpoint_visibility")
        + 0.04 * f(row, "mapping_confidence")
    )

    if f(row, "relation_correspondence") < 0.50:
        action = "repair_relational_mapping"
    elif f(row, "breakpoint_visibility") < 0.45:
        action = "define_analogy_breakpoints"
    elif mapping_score >= 0.72:
        action = "strong_mapping_candidate"
    else:
        action = "mapping_requires_review"

    mapping_rows.append(
        {
            "mapping_id": row["mapping_id"],
            "strategy_id": row["strategy_id"],
            "strategy_name": strategy_names.get(row["strategy_id"], row["strategy_id"]),
            "source_id": row["source_id"],
            "source_name": source_names.get(row["source_id"], row["source_id"]),
            "target_id": row["target_id"],
            "target_name": target_names.get(row["target_id"], row["target_id"]),
            "mapping_score": round(mapping_score, 4),
            "recommended_action": action,
            "actor_correspondence": row["actor_correspondence"],
            "relation_correspondence": row["relation_correspondence"],
            "flow_correspondence": row["flow_correspondence"],
            "constraint_correspondence": row["constraint_correspondence"],
            "feedback_correspondence": row["feedback_correspondence"],
            "failure_mode_correspondence": row["failure_mode_correspondence"],
            "breakpoint_visibility": row["breakpoint_visibility"],
            "mapping_confidence": row["mapping_confidence"],
        }
    )

mapping_rows.sort(key=lambda item: item["mapping_score"], reverse=True)

write_csv(
    TABLES / "source_target_mapping_scores.csv",
    mapping_rows,
    [
        "mapping_id",
        "strategy_id",
        "strategy_name",
        "source_id",
        "source_name",
        "target_id",
        "target_name",
        "mapping_score",
        "recommended_action",
        "actor_correspondence",
        "relation_correspondence",
        "flow_correspondence",
        "constraint_correspondence",
        "feedback_correspondence",
        "failure_mode_correspondence",
        "breakpoint_visibility",
        "mapping_confidence",
    ],
)

# ---------------------------------------------------------------------
# 4. Adaptation readiness
# ---------------------------------------------------------------------

adaptation_rows: list[dict[str, object]] = []

for row in adaptations:
    adaptation_score = (
        0.14 * f(row, "constraint_fit")
        + 0.14 * f(row, "stakeholder_fit")
        + 0.18 * f(row, "mechanism_fit")
        + 0.14 * f(row, "governance_fit")
        + 0.12 * f(row, "implementation_fit")
        + 0.12 * f(row, "evidence_fit")
        + 0.12 * f(row, "ethical_fit")
        + 0.04 * f(row, "adaptation_readiness")
    )

    if f(row, "ethical_fit") < 0.45 or f(row, "stakeholder_fit") < 0.45:
        action = "stakeholder_or_ethics_review_before_transfer"
    elif f(row, "mechanism_fit") < 0.55:
        action = "test_target_mechanism_before_transfer"
    elif adaptation_score >= 0.72:
        action = "advance_to_transfer_hypothesis"
    else:
        action = "revise_adaptation_design"

    adaptation_rows.append(
        {
            "adaptation_id": row["adaptation_id"],
            "mapping_id": row["mapping_id"],
            "mapping_label": mapping_labels.get(row["mapping_id"], row["mapping_id"]),
            "strategy_id": row["strategy_id"],
            "strategy_name": strategy_names.get(row["strategy_id"], row["strategy_id"]),
            "target_id": row["target_id"],
            "target_name": target_names.get(row["target_id"], row["target_id"]),
            "adaptation_score": round(adaptation_score, 4),
            "recommended_action": action,
            "constraint_fit": row["constraint_fit"],
            "stakeholder_fit": row["stakeholder_fit"],
            "mechanism_fit": row["mechanism_fit"],
            "governance_fit": row["governance_fit"],
            "implementation_fit": row["implementation_fit"],
            "evidence_fit": row["evidence_fit"],
            "ethical_fit": row["ethical_fit"],
            "adaptation_readiness": row["adaptation_readiness"],
        }
    )

adaptation_rows.sort(key=lambda item: item["adaptation_score"], reverse=True)

write_csv(
    TABLES / "adaptation_readiness_review.csv",
    adaptation_rows,
    [
        "adaptation_id",
        "mapping_id",
        "mapping_label",
        "strategy_id",
        "strategy_name",
        "target_id",
        "target_name",
        "adaptation_score",
        "recommended_action",
        "constraint_fit",
        "stakeholder_fit",
        "mechanism_fit",
        "governance_fit",
        "implementation_fit",
        "evidence_fit",
        "ethical_fit",
        "adaptation_readiness",
    ],
)

# ---------------------------------------------------------------------
# 5. Rival analogy comparison
# ---------------------------------------------------------------------

rival_rows: list[dict[str, object]] = []

for row in rivals:
    rival_score = (
        0.24 * f(row, "structural_fit")
        + 0.20 * f(row, "explanatory_power")
        - 0.16 * f(row, "blind_spot_risk")
        - 0.12 * f(row, "ethical_risk")
        + 0.14 * f(row, "implementation_relevance")
        + 0.10 * f(row, "novelty_value")
    )

    if f(row, "blind_spot_risk") >= 0.60:
        action = "use_only_with_breakpoint_review"
    elif f(row, "ethical_risk") >= 0.60:
        action = "ethics_review_required"
    elif rival_score >= 0.62:
        action = "strong_rival_or_primary_analogy"
    else:
        action = "secondary_or_limited_use"

    rival_rows.append(
        {
            "rival_id": row["rival_id"],
            "target_id": row["target_id"],
            "target_name": target_names.get(row["target_id"], row["target_id"]),
            "analogy_set": row["analogy_set"],
            "analogy_name": row["analogy_name"],
            "rival_analogy_score": round(rival_score, 4),
            "recommended_action": action,
            "structural_fit": row["structural_fit"],
            "explanatory_power": row["explanatory_power"],
            "blind_spot_risk": row["blind_spot_risk"],
            "ethical_risk": row["ethical_risk"],
            "implementation_relevance": row["implementation_relevance"],
            "novelty_value": row["novelty_value"],
        }
    )

rival_rows.sort(key=lambda item: item["rival_analogy_score"], reverse=True)

write_csv(
    TABLES / "rival_analogy_comparison.csv",
    rival_rows,
    [
        "rival_id",
        "target_id",
        "target_name",
        "analogy_set",
        "analogy_name",
        "rival_analogy_score",
        "recommended_action",
        "structural_fit",
        "explanatory_power",
        "blind_spot_risk",
        "ethical_risk",
        "implementation_relevance",
        "novelty_value",
    ],
)

# ---------------------------------------------------------------------
# 6. Stakeholder legitimacy review
# ---------------------------------------------------------------------

stakeholder_rows: list[dict[str, object]] = []

for row in stakeholders:
    stakeholder_score = (
        0.15 * f(row, "inclusion_level")
        + 0.16 * f(row, "burden_visibility")
        + 0.16 * f(row, "knowledge_recognition")
        + 0.14 * f(row, "interpretive_trust")
        + 0.16 * f(row, "legitimacy_signal")
        - 0.15 * f(row, "power_blindness_risk")
        + 0.08 * f(row, "review_quality")
    )

    if f(row, "power_blindness_risk") >= 0.65:
        action = "power_and_burden_review_required"
    elif f(row, "burden_visibility") < 0.45:
        action = "add_burden_visibility_review"
    elif stakeholder_score < 0.50:
        action = "stakeholder_legitimacy_review"
    else:
        action = "stakeholder_review_manageable"

    stakeholder_rows.append(
        {
            "review_id": row["review_id"],
            "strategy_id": row["strategy_id"],
            "strategy_name": strategy_names.get(row["strategy_id"], row["strategy_id"]),
            "target_id": row["target_id"],
            "target_name": target_names.get(row["target_id"], row["target_id"]),
            "stakeholder_group": row["stakeholder_group"],
            "stakeholder_legitimacy_score": round(stakeholder_score, 4),
            "recommended_action": action,
            "inclusion_level": row["inclusion_level"],
            "burden_visibility": row["burden_visibility"],
            "knowledge_recognition": row["knowledge_recognition"],
            "interpretive_trust": row["interpretive_trust"],
            "legitimacy_signal": row["legitimacy_signal"],
            "power_blindness_risk": row["power_blindness_risk"],
            "review_quality": row["review_quality"],
        }
    )

stakeholder_rows.sort(key=lambda item: item["stakeholder_legitimacy_score"])

write_csv(
    TABLES / "stakeholder_legitimacy_review.csv",
    stakeholder_rows,
    [
        "review_id",
        "strategy_id",
        "strategy_name",
        "target_id",
        "target_name",
        "stakeholder_group",
        "stakeholder_legitimacy_score",
        "recommended_action",
        "inclusion_level",
        "burden_visibility",
        "knowledge_recognition",
        "interpretive_trust",
        "legitimacy_signal",
        "power_blindness_risk",
        "review_quality",
    ],
)

# ---------------------------------------------------------------------
# 7. Transfer hypothesis register
# ---------------------------------------------------------------------

hypothesis_rows: list[dict[str, object]] = []

for row in hypotheses:
    hypothesis_score = (
        0.18 * f(row, "hypothesis_clarity")
        + 0.18 * f(row, "evidence_strength")
        + 0.18 * f(row, "testability")
        - 0.14 * f(row, "implementation_risk")
        - 0.14 * f(row, "unintended_consequence_risk")
        + 0.16 * f(row, "revision_trigger_quality")
    )

    if f(row, "unintended_consequence_risk") >= 0.65:
        action = "risk_and_second_order_effects_review"
    elif f(row, "testability") < 0.50:
        action = "convert_to_testable_transfer_hypothesis"
    elif hypothesis_score >= 0.50:
        action = "advance_to_evidence_test"
    else:
        action = "revise_or_hold_hypothesis"

    hypothesis_rows.append(
        {
            "hypothesis_id": row["hypothesis_id"],
            "mapping_id": row["mapping_id"],
            "mapping_label": mapping_labels.get(row["mapping_id"], row["mapping_id"]),
            "strategy_id": row["strategy_id"],
            "strategy_name": strategy_names.get(row["strategy_id"], row["strategy_id"]),
            "transfer_hypothesis_score": round(hypothesis_score, 4),
            "recommended_action": action,
            "hypothesis_clarity": row["hypothesis_clarity"],
            "evidence_strength": row["evidence_strength"],
            "testability": row["testability"],
            "implementation_risk": row["implementation_risk"],
            "unintended_consequence_risk": row["unintended_consequence_risk"],
            "revision_trigger_quality": row["revision_trigger_quality"],
            "recommended_next_step": row["recommended_next_step"],
            "hypothesis_statement": row["hypothesis_statement"],
        }
    )

hypothesis_rows.sort(key=lambda item: item["transfer_hypothesis_score"], reverse=True)

write_csv(
    TABLES / "transfer_hypothesis_register.csv",
    hypothesis_rows,
    [
        "hypothesis_id",
        "mapping_id",
        "mapping_label",
        "strategy_id",
        "strategy_name",
        "transfer_hypothesis_score",
        "recommended_action",
        "hypothesis_clarity",
        "evidence_strength",
        "testability",
        "implementation_risk",
        "unintended_consequence_risk",
        "revision_trigger_quality",
        "recommended_next_step",
        "hypothesis_statement",
    ],
)

# ---------------------------------------------------------------------
# 8. Strategist report
# ---------------------------------------------------------------------

weakest_profiles = sorted(profile_rows, key=lambda item: item["analogy_profile_score"])[:5]
highest_surface = surface_rows[:5]
top_sources = source_rows[:5]
weakest_mappings = sorted(mapping_rows, key=lambda item: item["mapping_score"])[:5]
top_mappings = mapping_rows[:5]
weakest_adaptations = sorted(adaptation_rows, key=lambda item: item["adaptation_score"])[:5]
top_rivals = rival_rows[:8]
weakest_stakeholders = stakeholder_rows[:5]
top_hypotheses = hypothesis_rows[:6]

report: list[str] = []

report.append("# Analogical Transfer Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic separates analogical strategy quality, source-domain quality, source-target mapping, "
    "surface-distraction risk, adaptation readiness, rival analogy comparison, stakeholder legitimacy, and "
    "transfer hypothesis quality. The purpose is to help strategists distinguish deep structural transfer "
    "from surface resemblance, prestige borrowing, context neglect, and power-blind imitation."
)
report.append("")
report.append("## Analogical strategies requiring the most review")
report.append("")

for item in weakest_profiles:
    report.append(
        f"- **{item['strategy_id']} — {item['strategy_name']}**: profile score {item['analogy_profile_score']}; "
        f"surface risk {item['surface_distraction_risk']}; transfer readiness {item['transfer_readiness']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest surface-distraction risks")
report.append("")

for item in highest_surface:
    report.append(
        f"- **{item['strategy_id']} — {item['strategy_name']}**: surface risk {item['surface_distraction_risk']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strongest source-domain candidates")
report.append("")

for item in top_sources:
    report.append(
        f"- **{item['source_id']} — {item['source_name']}**: source quality {item['source_quality_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strongest source-target mappings")
report.append("")

for item in top_mappings:
    report.append(
        f"- **{item['mapping_id']} — {item['source_name']} → {item['target_name']}**: mapping score {item['mapping_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weakest source-target mappings")
report.append("")

for item in weakest_mappings:
    report.append(
        f"- **{item['mapping_id']} — {item['source_name']} → {item['target_name']}**: mapping score {item['mapping_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Adaptation reviews requiring attention")
report.append("")

for item in weakest_adaptations:
    report.append(
        f"- **{item['adaptation_id']} — {item['mapping_label']}**: adaptation score {item['adaptation_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Rival analogy comparison")
report.append("")

for item in top_rivals:
    report.append(
        f"- **{item['target_name']} / {item['analogy_name']}**: rival score {item['rival_analogy_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weakest stakeholder legitimacy reviews")
report.append("")

for item in weakest_stakeholders:
    report.append(
        f"- **{item['review_id']} — {item['stakeholder_group']}** in **{item['target_name']}**: "
        f"legitimacy score {item['stakeholder_legitimacy_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Top transfer hypotheses")
report.append("")

for item in top_hypotheses:
    report.append(
        f"- **{item['hypothesis_id']} — {item['strategy_name']}**: hypothesis score {item['transfer_hypothesis_score']}; "
        f"action: {item['recommended_action']}; next step: {item['recommended_next_step']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "The value of this workflow is disciplined analogical reasoning. It helps a strategist ask whether "
    "a source domain contains transferable relational structure, whether the target problem is clearly defined, "
    "whether the mapping is structural rather than superficial, whether adaptation is feasible and legitimate, "
    "whether rival analogies should be considered, and what evidence would confirm or weaken the transfer."
)

(REPORTS / "analogical_transfer_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "weakest_profiles": weakest_profiles,
    "highest_surface": highest_surface,
    "top_sources": top_sources,
    "weakest_mappings": weakest_mappings,
    "top_mappings": top_mappings,
    "weakest_adaptations": weakest_adaptations,
    "top_rivals": top_rivals,
    "weakest_stakeholders": weakest_stakeholders,
    "top_hypotheses": top_hypotheses,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced analogical transfer diagnostics complete.")
print(f"Wrote: {TABLES / 'analogical_strategy_profiles.csv'}")
print(f"Wrote: {TABLES / 'source_target_mapping_scores.csv'}")
print(f"Wrote: {TABLES / 'surface_distraction_risk.csv'}")
print(f"Wrote: {TABLES / 'adaptation_readiness_review.csv'}")
print(f"Wrote: {TABLES / 'rival_analogy_comparison.csv'}")
print(f"Wrote: {TABLES / 'stakeholder_legitimacy_review.csv'}")
print(f"Wrote: {TABLES / 'transfer_hypothesis_register.csv'}")
print(f"Wrote: {REPORTS / 'analogical_transfer_diagnostic_report.md'}")
