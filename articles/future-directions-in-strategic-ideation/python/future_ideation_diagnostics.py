#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Future Directions in Strategic Ideation.

Uses only Python standard library.
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


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def f(row: dict[str, str], key: str) -> float:
    return float(row[key])


ideas = read_csv(RAW / "future_ideas.csv")
scenarios = read_csv(RAW / "scenario_options.csv")
ai = read_csv(RAW / "ai_governance.csv")
ci = read_csv(RAW / "collective_intelligence.csv")
learning = read_csv(RAW / "learning_memory.csv")

idea_names = {row["idea_id"]: row["idea"] for row in ideas}

# ---------------------------------------------------------------------
# 1. Future-ready idea score
# ---------------------------------------------------------------------

idea_rows: list[dict[str, object]] = []
for row in ideas:
    future_ready_score = (
        0.10 * f(row, "problem_frame_quality")
        + 0.10 * f(row, "evidence_quality")
        + 0.10 * f(row, "adaptability")
        + 0.11 * f(row, "scenario_robustness")
        + 0.10 * f(row, "stakeholder_legitimacy")
        + 0.09 * f(row, "implementation_readiness")
        + 0.10 * f(row, "ethical_visibility")
        + 0.11 * f(row, "learning_design")
        + 0.08 * f(row, "option_value")
        + 0.06 * f(row, "ai_governance")
        + 0.05 * f(row, "systems_responsibility")
    )
    future_risk = (
        0.10 * (1 - f(row, "problem_frame_quality"))
        + 0.10 * (1 - f(row, "evidence_quality"))
        + 0.10 * (1 - f(row, "adaptability"))
        + 0.12 * (1 - f(row, "scenario_robustness"))
        + 0.12 * (1 - f(row, "stakeholder_legitimacy"))
        + 0.10 * (1 - f(row, "implementation_readiness"))
        + 0.11 * (1 - f(row, "ethical_visibility"))
        + 0.10 * (1 - f(row, "learning_design"))
        + 0.07 * (1 - f(row, "option_value"))
        + 0.08 * (1 - f(row, "ai_governance"))
        + 0.10 * (1 - f(row, "systems_responsibility"))
    )

    if future_ready_score > 0.78:
        diagnosis = "future_ready_candidate"
    elif f(row, "scenario_robustness") < 0.55:
        diagnosis = "scenario_fragility"
    elif f(row, "stakeholder_legitimacy") < 0.55:
        diagnosis = "legitimacy_gap"
    elif f(row, "ethical_visibility") < 0.55:
        diagnosis = "ethical_visibility_gap"
    elif f(row, "learning_design") < 0.55:
        diagnosis = "weak_learning_design"
    elif f(row, "ai_governance") < 0.45:
        diagnosis = "ai_governance_risk"
    elif f(row, "implementation_readiness") < 0.55:
        diagnosis = "implementation_readiness_gap"
    else:
        diagnosis = "targeted_repair_before_advancement"

    weakest_dimension = min(
        [
            ("problem_frame_quality", f(row, "problem_frame_quality")),
            ("evidence_quality", f(row, "evidence_quality")),
            ("adaptability", f(row, "adaptability")),
            ("scenario_robustness", f(row, "scenario_robustness")),
            ("stakeholder_legitimacy", f(row, "stakeholder_legitimacy")),
            ("implementation_readiness", f(row, "implementation_readiness")),
            ("ethical_visibility", f(row, "ethical_visibility")),
            ("learning_design", f(row, "learning_design")),
            ("option_value", f(row, "option_value")),
            ("ai_governance", f(row, "ai_governance")),
            ("systems_responsibility", f(row, "systems_responsibility")),
        ],
        key=lambda item: item[1],
    )[0]

    idea_rows.append({
        "idea_id": row["idea_id"],
        "idea": row["idea"],
        "idea_type": row["idea_type"],
        "future_ready_score": round(future_ready_score, 4),
        "future_risk": round(future_risk, 4),
        "weakest_dimension": weakest_dimension,
        "diagnosis": diagnosis,
        "description": row["description"],
    })

idea_rows.sort(key=lambda item: item["future_ready_score"], reverse=True)
write_csv(TABLES / "future_ready_idea_scores.csv", idea_rows)
write_csv(PROCESSED / "future_ready_idea_scores.csv", idea_rows)

# ---------------------------------------------------------------------
# 2. Scenario and option value review
# ---------------------------------------------------------------------

scenario_rows: list[dict[str, object]] = []
for row in scenarios:
    scenario_option_score = (
        0.20 * f(row, "scenario_performance")
        + 0.18 * f(row, "adaptation_capacity")
        + 0.18 * f(row, "option_preservation")
        + 0.14 * (1 - f(row, "lock_in_risk"))
        + 0.15 * f(row, "learning_value")
        + 0.15 * f(row, "resilience_contribution")
    )
    scenario_risk = (
        0.20 * (1 - f(row, "scenario_performance"))
        + 0.18 * (1 - f(row, "adaptation_capacity"))
        + 0.16 * (1 - f(row, "option_preservation"))
        + 0.18 * f(row, "lock_in_risk")
        + 0.14 * (1 - f(row, "learning_value"))
        + 0.14 * (1 - f(row, "resilience_contribution"))
    )
    scenario_rows.append({
        "scenario_option_id": row["scenario_option_id"],
        "idea_id": row["idea_id"],
        "idea": idea_names[row["idea_id"]],
        "scenario": row["scenario"],
        "scenario_option_score": round(scenario_option_score, 4),
        "scenario_risk": round(scenario_risk, 4),
        "review_action": row["review_action"],
    })

scenario_rows.sort(key=lambda item: item["scenario_option_score"], reverse=True)
write_csv(TABLES / "scenario_option_scores.csv", scenario_rows)

# ---------------------------------------------------------------------
# 3. AI governance review
# ---------------------------------------------------------------------

ai_rows: list[dict[str, object]] = []
for row in ai:
    ai_governance_score = (
        0.13 * f(row, "disclosure_quality")
        + 0.14 * f(row, "source_traceability")
        + 0.14 * f(row, "human_review")
        + 0.13 * f(row, "bias_review")
        + 0.13 * f(row, "stakeholder_review")
        + 0.13 * f(row, "uncertainty_preservation")
        + 0.12 * f(row, "accountability_clarity")
        + 0.08 * (1 - f(row, "fluency_risk"))
    )
    ai_risk = (
        0.22 * f(row, "fluency_risk")
        + 0.12 * (1 - f(row, "disclosure_quality"))
        + 0.14 * (1 - f(row, "source_traceability"))
        + 0.12 * (1 - f(row, "human_review"))
        + 0.12 * (1 - f(row, "bias_review"))
        + 0.10 * (1 - f(row, "stakeholder_review"))
        + 0.10 * (1 - f(row, "uncertainty_preservation"))
        + 0.08 * (1 - f(row, "accountability_clarity"))
    )
    ai_rows.append({
        "ai_id": row["ai_id"],
        "idea_id": row["idea_id"],
        "idea": idea_names[row["idea_id"]],
        "ai_use_case": row["ai_use_case"],
        "ai_governance_score": round(ai_governance_score, 4),
        "ai_risk": round(ai_risk, 4),
        "review_action": row["review_action"],
    })

ai_rows.sort(key=lambda item: item["ai_risk"], reverse=True)
write_csv(TABLES / "ai_governance_scores.csv", ai_rows)

# ---------------------------------------------------------------------
# 4. Collective intelligence review
# ---------------------------------------------------------------------

ci_rows: list[dict[str, object]] = []
for row in ci:
    collective_score = (
        0.10 * f(row, "executive_alignment")
        + 0.13 * f(row, "frontline_voice")
        + 0.15 * f(row, "stakeholder_voice")
        + 0.12 * f(row, "technical_expertise")
        + 0.12 * f(row, "analytical_support")
        + 0.14 * f(row, "dissent_protection")
        + 0.12 * f(row, "synthesis_quality")
        + 0.12 * f(row, "participation_influence")
    )
    participation_gap = max(0.0, f(row, "stakeholder_voice") - f(row, "participation_influence"))
    ci_rows.append({
        "ci_id": row["ci_id"],
        "idea_id": row["idea_id"],
        "idea": idea_names[row["idea_id"]],
        "knowledge_source": row["knowledge_source"],
        "collective_intelligence_score": round(collective_score, 4),
        "participation_gap": round(participation_gap, 4),
        "review_action": row["review_action"],
    })

ci_rows.sort(key=lambda item: item["collective_intelligence_score"], reverse=True)
write_csv(TABLES / "collective_intelligence_scores.csv", ci_rows)

# ---------------------------------------------------------------------
# 5. Learning memory review
# ---------------------------------------------------------------------

learning_rows: list[dict[str, object]] = []
for row in learning:
    learning_memory_score = (
        0.13 * f(row, "idea_metadata_quality")
        + 0.14 * f(row, "decision_memory_quality")
        + 0.13 * f(row, "retrieval_quality")
        + 0.12 * f(row, "experiment_design")
        + 0.12 * f(row, "stop_rule_quality")
        + 0.12 * f(row, "revision_trigger_quality")
        + 0.12 * f(row, "outcome_learning")
        + 0.12 * f(row, "knowledge_reuse_value")
    )
    learning_risk = (
        0.13 * (1 - f(row, "idea_metadata_quality"))
        + 0.14 * (1 - f(row, "decision_memory_quality"))
        + 0.13 * (1 - f(row, "retrieval_quality"))
        + 0.12 * (1 - f(row, "experiment_design"))
        + 0.12 * (1 - f(row, "stop_rule_quality"))
        + 0.12 * (1 - f(row, "revision_trigger_quality"))
        + 0.12 * (1 - f(row, "outcome_learning"))
        + 0.12 * (1 - f(row, "knowledge_reuse_value"))
    )
    learning_rows.append({
        "lm_id": row["lm_id"],
        "idea_id": row["idea_id"],
        "idea": idea_names[row["idea_id"]],
        "learning_memory_score": round(learning_memory_score, 4),
        "learning_memory_risk": round(learning_risk, 4),
        "review_action": row["review_action"],
    })

learning_rows.sort(key=lambda item: item["learning_memory_score"], reverse=True)
write_csv(TABLES / "learning_memory_scores.csv", learning_rows)

summary = {
    "future_ready_ideas": idea_rows,
    "scenario_options": scenario_rows,
    "ai_governance": ai_rows,
    "collective_intelligence": ci_rows,
    "learning_memory": learning_rows,
}
(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

report = [
    "# Future Directions in Strategic Ideation Diagnostic Report",
    "",
    "## Executive summary",
    "",
    "This diagnostic evaluates future-ready strategic ideas across problem-frame quality, evidence, adaptability, scenario robustness, stakeholder legitimacy, implementation readiness, ethical visibility, learning design, option value, AI governance, systems responsibility, collective intelligence, and institutional memory.",
    "",
    "## Future-ready idea ranking",
    "",
]
for item in idea_rows:
    report.append(
        f"- **{item['idea_id']} — {item['idea']}**: future-ready score {item['future_ready_score']}; "
        f"future risk {item['future_risk']}; weakest dimension: {item['weakest_dimension']}; diagnosis: {item['diagnosis']}."
    )

report.extend(["", "## Scenario and option review", ""])
for item in scenario_rows:
    report.append(
        f"- **{item['idea']}** in **{item['scenario']}**: scenario-option score {item['scenario_option_score']}; "
        f"scenario risk {item['scenario_risk']}; action: {item['review_action']}."
    )

report.extend(["", "## AI governance review", ""])
for item in ai_rows:
    report.append(
        f"- **{item['idea']}** ({item['ai_use_case']}): AI governance score {item['ai_governance_score']}; "
        f"AI risk {item['ai_risk']}; action: {item['review_action']}."
    )

report.extend(["", "## Collective intelligence review", ""])
for item in ci_rows:
    report.append(
        f"- **{item['idea']}** ({item['knowledge_source']}): collective intelligence score {item['collective_intelligence_score']}; "
        f"participation gap {item['participation_gap']}; action: {item['review_action']}."
    )

report.extend(["", "## Learning memory review", ""])
for item in learning_rows:
    report.append(
        f"- **{item['idea']}**: learning memory score {item['learning_memory_score']}; "
        f"learning memory risk {item['learning_memory_risk']}; action: {item['review_action']}."
    )

report.extend([
    "",
    "## Professional interpretation",
    "",
    "Future-ready strategic ideation is not merely faster idea generation. It is a disciplined system for framing problems, governing AI, testing ideas across scenarios, preserving options, including stakeholders, making ethics visible, designing experiments, and preserving decision memory.",
])

(REPORTS / "future_ideation_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

print("Advanced future strategic ideation diagnostics complete.")
print(f"Wrote: {TABLES / 'future_ready_idea_scores.csv'}")
print(f"Wrote: {TABLES / 'scenario_option_scores.csv'}")
print(f"Wrote: {TABLES / 'ai_governance_scores.csv'}")
print(f"Wrote: {TABLES / 'collective_intelligence_scores.csv'}")
print(f"Wrote: {TABLES / 'learning_memory_scores.csv'}")
print(f"Wrote: {REPORTS / 'future_ideation_diagnostic_report.md'}")
