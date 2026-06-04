#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for abductive reasoning and strategic hypotheses.

This dependency-light workflow uses only the Python standard library.

It produces:
- hypothesis value scores
- rival hypothesis review
- evidence pathway review
- disconfirmation review
- commitment-level review
- revision trigger review
- hypothesis portfolio review
- intervention recommendations
- a markdown strategist diagnostic report

The workflow is designed for strategy teams that need to move from
observations and weak signals to testable strategic hypotheses.
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


observations = read_csv(RAW / "observations.csv")
hypotheses = read_csv(RAW / "hypotheses.csv")
evidence = read_csv(RAW / "evidence_pathways.csv")
disconfirmation = read_csv(RAW / "disconfirmation_tests.csv")
commitments = read_csv(RAW / "commitment_levels.csv")
revisions = read_csv(RAW / "revision_triggers.csv")
portfolio = read_csv(RAW / "portfolio_status.csv")
interventions = read_csv(RAW / "intervention_library.csv")

observation_names = {row["observation_id"]: row["observation_name"] for row in observations}
hypothesis_names = {row["hypothesis_id"]: row["hypothesis_name"] for row in hypotheses}

# ---------------------------------------------------------------------
# 1. Hypothesis value scoring
# ---------------------------------------------------------------------

hypothesis_rows: list[dict[str, object]] = []

for row in hypotheses:
    hypothesis_value = (
        0.16 * f(row, "explanatory_strength")
        + 0.14 * f(row, "testability")
        + 0.14 * f(row, "evidence_quality")
        + 0.16 * f(row, "strategic_relevance")
        + 0.12 * f(row, "stakeholder_visibility")
        + 0.12 * f(row, "systems_fit")
        + 0.10 * f(row, "actionability")
        + 0.06 * f(row, "reversibility")
        - 0.10 * f(row, "implementation_risk")
    )

    if hypothesis_value >= 0.72 and f(row, "evidence_quality") >= 0.65 and f(row, "reversibility") >= 0.55:
        recommended_status = "prototype_or_pilot"
    elif hypothesis_value >= 0.64:
        recommended_status = "targeted_research_or_low_risk_test"
    elif hypothesis_value >= 0.54:
        recommended_status = "monitor_and_compare"
    elif f(row, "implementation_risk") >= 0.65 and f(row, "evidence_quality") < 0.60:
        recommended_status = "avoid_major_commitment"
    else:
        recommended_status = "hold_reframe_or_archive"

    confidence_gap = max(0.0, 0.70 - f(row, "confidence_prior"))
    evidence_gap = max(0.0, 0.65 - f(row, "evidence_quality"))
    stakeholder_gap = max(0.0, 0.65 - f(row, "stakeholder_visibility"))
    systems_gap = max(0.0, 0.70 - f(row, "systems_fit"))

    hypothesis_rows.append(
        {
            "hypothesis_id": row["hypothesis_id"],
            "observation_id": row["observation_id"],
            "observation_name": observation_names.get(row["observation_id"], row["observation_id"]),
            "hypothesis_name": row["hypothesis_name"],
            "hypothesis_type": row["hypothesis_type"],
            "frame_family": row["frame_family"],
            "mechanism_family": row["mechanism_family"],
            "hypothesis_value_score": round(hypothesis_value, 4),
            "recommended_status": recommended_status,
            "confidence_gap": round(confidence_gap, 4),
            "evidence_gap": round(evidence_gap, 4),
            "stakeholder_gap": round(stakeholder_gap, 4),
            "systems_gap": round(systems_gap, 4),
            "explanatory_strength": row["explanatory_strength"],
            "testability": row["testability"],
            "evidence_quality": row["evidence_quality"],
            "strategic_relevance": row["strategic_relevance"],
            "stakeholder_visibility": row["stakeholder_visibility"],
            "systems_fit": row["systems_fit"],
            "actionability": row["actionability"],
            "implementation_risk": row["implementation_risk"],
            "reversibility": row["reversibility"],
            "confidence_prior": row["confidence_prior"],
        }
    )

hypothesis_rows.sort(key=lambda item: item["hypothesis_value_score"], reverse=True)

hypothesis_fields = [
    "hypothesis_id",
    "observation_id",
    "observation_name",
    "hypothesis_name",
    "hypothesis_type",
    "frame_family",
    "mechanism_family",
    "hypothesis_value_score",
    "recommended_status",
    "confidence_gap",
    "evidence_gap",
    "stakeholder_gap",
    "systems_gap",
    "explanatory_strength",
    "testability",
    "evidence_quality",
    "strategic_relevance",
    "stakeholder_visibility",
    "systems_fit",
    "actionability",
    "implementation_risk",
    "reversibility",
    "confidence_prior",
]

write_csv(TABLES / "hypothesis_scores.csv", hypothesis_rows, hypothesis_fields)
write_csv(PROCESSED / "hypothesis_scores.csv", hypothesis_rows, hypothesis_fields)

# Rival hypothesis review by observation.
rival_rows: list[dict[str, object]] = []
for obs in observations:
    obs_hypotheses = [h for h in hypothesis_rows if h["observation_id"] == obs["observation_id"]]
    if not obs_hypotheses:
        continue

    best = max(obs_hypotheses, key=lambda item: float(item["hypothesis_value_score"]))
    scores = [float(h["hypothesis_value_score"]) for h in obs_hypotheses]
    spread = max(scores) - min(scores) if len(scores) > 1 else 0.0
    rival_count = len(obs_hypotheses)

    if rival_count < 2:
        action = "generate_rival_hypotheses"
    elif spread < 0.08:
        action = "design_discriminating_evidence"
    elif float(best["evidence_gap"]) > 0.10:
        action = "strengthen_evidence_for_leading_hypothesis"
    else:
        action = "continue_comparative_testing"

    rival_rows.append(
        {
            "observation_id": obs["observation_id"],
            "observation_name": obs["observation_name"],
            "rival_hypothesis_count": rival_count,
            "leading_hypothesis_id": best["hypothesis_id"],
            "leading_hypothesis_name": best["hypothesis_name"],
            "leading_hypothesis_score": best["hypothesis_value_score"],
            "hypothesis_score_spread": round(spread, 4),
            "recommended_action": action,
            "signal_strength": obs["signal_strength"],
            "strategic_relevance": obs["strategic_relevance"],
            "ambiguity": obs["ambiguity"],
            "stakeholder_visibility": obs["stakeholder_visibility"],
        }
    )

write_csv(
    TABLES / "rival_hypothesis_review.csv",
    rival_rows,
    [
        "observation_id",
        "observation_name",
        "rival_hypothesis_count",
        "leading_hypothesis_id",
        "leading_hypothesis_name",
        "leading_hypothesis_score",
        "hypothesis_score_spread",
        "recommended_action",
        "signal_strength",
        "strategic_relevance",
        "ambiguity",
        "stakeholder_visibility",
    ],
)

# ---------------------------------------------------------------------
# 2. Evidence pathway review
# ---------------------------------------------------------------------

evidence_rows: list[dict[str, object]] = []

for row in evidence:
    evidence_value = (
        0.18 * f(row, "evidence_strength")
        + 0.16 * f(row, "reliability")
        + 0.18 * f(row, "discrimination_power")
        + 0.14 * f(row, "stakeholder_legitimacy")
        - 0.10 * f(row, "cost")
        - 0.08 * f(row, "time_to_learn")
    )

    if f(row, "discrimination_power") >= 0.75 and f(row, "reliability") >= 0.70:
        action = "priority_evidence_test"
    elif f(row, "stakeholder_legitimacy") < 0.50:
        action = "add_stakeholder_legitimacy_review"
    elif f(row, "cost") >= 0.55 and evidence_value < 0.45:
        action = "find_lower_cost_learning_test"
    else:
        action = "usable_evidence_pathway"

    evidence_rows.append(
        {
            "evidence_id": row["evidence_id"],
            "hypothesis_id": row["hypothesis_id"],
            "hypothesis_name": hypothesis_names.get(row["hypothesis_id"], row["hypothesis_id"]),
            "evidence_name": row["evidence_name"],
            "evidence_type": row["evidence_type"],
            "evidence_value_score": round(evidence_value, 4),
            "recommended_action": action,
            "evidence_strength": row["evidence_strength"],
            "reliability": row["reliability"],
            "cost": row["cost"],
            "time_to_learn": row["time_to_learn"],
            "discrimination_power": row["discrimination_power"],
            "stakeholder_legitimacy": row["stakeholder_legitimacy"],
            "expected_if_true": row["expected_if_true"],
            "weakens_if": row["weakens_if"],
        }
    )

evidence_rows.sort(key=lambda item: item["evidence_value_score"], reverse=True)

write_csv(
    TABLES / "evidence_pathway_review.csv",
    evidence_rows,
    [
        "evidence_id",
        "hypothesis_id",
        "hypothesis_name",
        "evidence_name",
        "evidence_type",
        "evidence_value_score",
        "recommended_action",
        "evidence_strength",
        "reliability",
        "cost",
        "time_to_learn",
        "discrimination_power",
        "stakeholder_legitimacy",
        "expected_if_true",
        "weakens_if",
    ],
)

# ---------------------------------------------------------------------
# 3. Disconfirmation review
# ---------------------------------------------------------------------

disconfirm_rows: list[dict[str, object]] = []

for row in disconfirmation:
    disconfirmation_quality = (
        0.18 * f(row, "disconfirmation_clarity")
        + 0.14 * f(row, "severity_if_disconfirmed")
        + 0.18 * f(row, "learning_value")
        - 0.08 * f(row, "political_difficulty")
        + 0.12 * f(row, "reversibility")
        + 0.14 * f(row, "decision_impact")
        + 0.14 * f(row, "revision_path_quality")
    )

    if f(row, "disconfirmation_clarity") < 0.65:
        action = "make_disconfirmation_condition_clearer"
    elif f(row, "political_difficulty") >= 0.60:
        action = "protect_disconfirming_review_from_political_pressure"
    elif disconfirmation_quality >= 0.65:
        action = "strong_disconfirmation_test"
    else:
        action = "usable_but_strengthen_revision_logic"

    disconfirm_rows.append(
        {
            "test_id": row["test_id"],
            "hypothesis_id": row["hypothesis_id"],
            "hypothesis_name": hypothesis_names.get(row["hypothesis_id"], row["hypothesis_id"]),
            "test_name": row["test_name"],
            "disconfirmation_quality_score": round(disconfirmation_quality, 4),
            "recommended_action": action,
            "disconfirmation_clarity": row["disconfirmation_clarity"],
            "severity_if_disconfirmed": row["severity_if_disconfirmed"],
            "learning_value": row["learning_value"],
            "political_difficulty": row["political_difficulty"],
            "reversibility": row["reversibility"],
            "decision_impact": row["decision_impact"],
            "revision_path_quality": row["revision_path_quality"],
        }
    )

disconfirm_rows.sort(key=lambda item: item["disconfirmation_quality_score"], reverse=True)

write_csv(
    TABLES / "disconfirmation_review.csv",
    disconfirm_rows,
    [
        "test_id",
        "hypothesis_id",
        "hypothesis_name",
        "test_name",
        "disconfirmation_quality_score",
        "recommended_action",
        "disconfirmation_clarity",
        "severity_if_disconfirmed",
        "learning_value",
        "political_difficulty",
        "reversibility",
        "decision_impact",
        "revision_path_quality",
    ],
)

# ---------------------------------------------------------------------
# 4. Commitment-level review
# ---------------------------------------------------------------------

commitment_rows: list[dict[str, object]] = []

for row in commitments:
    commitment_readiness = (
        0.16 * f(row, "commitment_reversibility")
        + 0.18 * f(row, "evidence_threshold_met")
        + 0.18 * f(row, "confidence_threshold_met")
        + 0.14 * f(row, "stakeholder_threshold_met")
        + 0.14 * f(row, "risk_threshold_met")
        - 0.12 * f(row, "commitment_cost")
    )

    if f(row, "commitment_cost") >= 0.58 and f(row, "commitment_reversibility") < 0.60:
        action = "avoid_or_stage_commitment"
    elif commitment_readiness >= 0.62:
        action = "commitment_level_reasonable"
    elif f(row, "evidence_threshold_met") < 0.60:
        action = "strengthen_evidence_before_commitment"
    else:
        action = "use_low_risk_learning_commitment"

    commitment_rows.append(
        {
            "commitment_id": row["commitment_id"],
            "hypothesis_id": row["hypothesis_id"],
            "hypothesis_name": hypothesis_names.get(row["hypothesis_id"], row["hypothesis_id"]),
            "current_commitment": row["current_commitment"],
            "commitment_readiness_score": round(commitment_readiness, 4),
            "recommended_action": action,
            "recommended_next_commitment": row["recommended_next_commitment"],
            "commitment_cost": row["commitment_cost"],
            "commitment_reversibility": row["commitment_reversibility"],
            "evidence_threshold_met": row["evidence_threshold_met"],
            "confidence_threshold_met": row["confidence_threshold_met"],
            "stakeholder_threshold_met": row["stakeholder_threshold_met"],
            "risk_threshold_met": row["risk_threshold_met"],
        }
    )

commitment_rows.sort(key=lambda item: item["commitment_readiness_score"], reverse=True)

write_csv(
    TABLES / "commitment_level_review.csv",
    commitment_rows,
    [
        "commitment_id",
        "hypothesis_id",
        "hypothesis_name",
        "current_commitment",
        "commitment_readiness_score",
        "recommended_action",
        "recommended_next_commitment",
        "commitment_cost",
        "commitment_reversibility",
        "evidence_threshold_met",
        "confidence_threshold_met",
        "stakeholder_threshold_met",
        "risk_threshold_met",
    ],
)

# ---------------------------------------------------------------------
# 5. Revision trigger review
# ---------------------------------------------------------------------

revision_rows: list[dict[str, object]] = []

for row in revisions:
    revision_quality = (
        0.18 * f(row, "trigger_clarity")
        + 0.14 * f(row, "monitoring_quality")
        + 0.18 * f(row, "reopen_value")
        - 0.10 * f(row, "revision_difficulty")
        + 0.16 * f(row, "decision_memory_quality")
    )

    if f(row, "trigger_clarity") < 0.70:
        action = "make_revision_trigger_more_observable"
    elif f(row, "decision_memory_quality") < 0.70:
        action = "strengthen_decision_memory_record"
    elif revision_quality >= 0.55:
        action = "revision_trigger_manageable"
    else:
        action = "strengthen_revision_logic"

    revision_rows.append(
        {
            "trigger_id": row["trigger_id"],
            "hypothesis_id": row["hypothesis_id"],
            "hypothesis_name": hypothesis_names.get(row["hypothesis_id"], row["hypothesis_id"]),
            "trigger_name": row["trigger_name"],
            "trigger_type": row["trigger_type"],
            "revision_quality_score": round(revision_quality, 4),
            "recommended_action": action,
            "action_if_triggered": row["action_if_triggered"],
            "trigger_clarity": row["trigger_clarity"],
            "monitoring_quality": row["monitoring_quality"],
            "reopen_value": row["reopen_value"],
            "revision_difficulty": row["revision_difficulty"],
            "decision_memory_quality": row["decision_memory_quality"],
        }
    )

revision_rows.sort(key=lambda item: item["revision_quality_score"], reverse=True)

write_csv(
    TABLES / "revision_trigger_review.csv",
    revision_rows,
    [
        "trigger_id",
        "hypothesis_id",
        "hypothesis_name",
        "trigger_name",
        "trigger_type",
        "revision_quality_score",
        "recommended_action",
        "action_if_triggered",
        "trigger_clarity",
        "monitoring_quality",
        "reopen_value",
        "revision_difficulty",
        "decision_memory_quality",
    ],
)

# ---------------------------------------------------------------------
# 6. Portfolio review
# ---------------------------------------------------------------------

portfolio_rows: list[dict[str, object]] = []

for row in portfolio:
    portfolio_value = (
        0.16 * f(row, "confidence_level")
        + 0.16 * f(row, "evidence_readiness")
        + 0.18 * f(row, "strategic_option_value")
        + 0.16 * f(row, "learning_value")
        - 0.10 * f(row, "resource_intensity")
        + 0.12 * f(row, "time_sensitivity")
        - 0.10 * f(row, "risk_exposure")
    )

    if row["portfolio_role"] == "exploratory_hypothesis" and f(row, "strategic_option_value") >= 0.80:
        action = "preserve_option_value_with_low_cost_test"
    elif f(row, "risk_exposure") >= 0.70 and f(row, "evidence_readiness") < 0.70:
        action = "stage_or_delay_major_commitment"
    elif portfolio_value >= 0.60:
        action = "active_portfolio_priority"
    else:
        action = "monitor_or_archive_with_reopen_trigger"

    portfolio_rows.append(
        {
            "portfolio_id": row["portfolio_id"],
            "hypothesis_id": row["hypothesis_id"],
            "hypothesis_name": hypothesis_names.get(row["hypothesis_id"], row["hypothesis_id"]),
            "portfolio_role": row["portfolio_role"],
            "portfolio_value_score": round(portfolio_value, 4),
            "recommended_action": action,
            "portfolio_action": row["portfolio_action"],
            "confidence_level": row["confidence_level"],
            "evidence_readiness": row["evidence_readiness"],
            "strategic_option_value": row["strategic_option_value"],
            "learning_value": row["learning_value"],
            "resource_intensity": row["resource_intensity"],
            "time_sensitivity": row["time_sensitivity"],
            "risk_exposure": row["risk_exposure"],
        }
    )

portfolio_rows.sort(key=lambda item: item["portfolio_value_score"], reverse=True)

write_csv(
    TABLES / "hypothesis_portfolio_review.csv",
    portfolio_rows,
    [
        "portfolio_id",
        "hypothesis_id",
        "hypothesis_name",
        "portfolio_role",
        "portfolio_value_score",
        "recommended_action",
        "portfolio_action",
        "confidence_level",
        "evidence_readiness",
        "strategic_option_value",
        "learning_value",
        "resource_intensity",
        "time_sensitivity",
        "risk_exposure",
    ],
)

# ---------------------------------------------------------------------
# 7. Intervention recommendations
# ---------------------------------------------------------------------

intervention_rows: list[dict[str, object]] = []

for row in interventions:
    intervention_value = (
        0.16 * f(row, "hypothesis_quality_gain")
        + 0.16 * f(row, "evidence_quality_gain")
        + 0.16 * f(row, "disconfirmation_gain")
        + 0.14 * f(row, "stakeholder_gain")
        + 0.14 * f(row, "revision_gain")
        + 0.14 * f(row, "decision_memory_gain")
        - 0.10 * f(row, "process_cost")
        - 0.08 * f(row, "implementation_complexity")
        - 0.08 * f(row, "political_safety_need")
    )

    if f(row, "political_safety_need") >= 0.45:
        action = "requires_leadership_protection"
    elif intervention_value >= 0.50:
        action = "high_value_abductive_reasoning_intervention"
    else:
        action = "supporting_intervention"

    intervention_rows.append(
        {
            "intervention_id": row["intervention_id"],
            "intervention_name": row["intervention_name"],
            "target_abductive_risk": row["target_abductive_risk"],
            "intervention_value_score": round(intervention_value, 4),
            "recommended_action": action,
            "process_cost": row["process_cost"],
            "implementation_complexity": row["implementation_complexity"],
            "hypothesis_quality_gain": row["hypothesis_quality_gain"],
            "evidence_quality_gain": row["evidence_quality_gain"],
            "disconfirmation_gain": row["disconfirmation_gain"],
            "stakeholder_gain": row["stakeholder_gain"],
            "revision_gain": row["revision_gain"],
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
        "target_abductive_risk",
        "intervention_value_score",
        "recommended_action",
        "process_cost",
        "implementation_complexity",
        "hypothesis_quality_gain",
        "evidence_quality_gain",
        "disconfirmation_gain",
        "stakeholder_gain",
        "revision_gain",
        "decision_memory_gain",
        "political_safety_need",
    ],
)

# ---------------------------------------------------------------------
# 8. Strategist report
# ---------------------------------------------------------------------

top_hypotheses = hypothesis_rows[:6]
weak_hypotheses = sorted(hypothesis_rows, key=lambda item: item["hypothesis_value_score"])[:5]
rival_needs = [row for row in rival_rows if row["recommended_action"] != "continue_comparative_testing"]
top_evidence = evidence_rows[:6]
weak_evidence = sorted(evidence_rows, key=lambda item: item["evidence_value_score"])[:5]
top_disconfirm = disconfirm_rows[:6]
commitment_risks = [row for row in commitment_rows if row["recommended_action"] != "commitment_level_reasonable"]
top_revision = revision_rows[:6]
top_portfolio = portfolio_rows[:6]
top_interventions = intervention_rows[:6]

report: list[str] = []

report.append("# Abductive Reasoning and Strategic Hypotheses Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic separates hypothesis value, rival explanation quality, evidence pathway strength, "
    "disconfirmation quality, commitment readiness, revision logic, portfolio value, and intervention priority. "
    "The purpose is to help strategists move from observations and weak signals to plausible, testable, revisable "
    "strategic hypotheses."
)
report.append("")
report.append("## Strongest strategic hypotheses")
report.append("")

for item in top_hypotheses:
    report.append(
        f"- **{item['hypothesis_id']} — {item['hypothesis_name']}**: value {item['hypothesis_value_score']}; "
        f"observation: {item['observation_name']}; status: {item['recommended_status']}."
    )

report.append("")
report.append("## Weakest or least ready hypotheses")
report.append("")

for item in weak_hypotheses:
    report.append(
        f"- **{item['hypothesis_id']} — {item['hypothesis_name']}**: value {item['hypothesis_value_score']}; "
        f"evidence gap {item['evidence_gap']}; systems gap {item['systems_gap']}; status: {item['recommended_status']}."
    )

report.append("")
report.append("## Rival hypothesis review")
report.append("")

for item in rival_rows:
    report.append(
        f"- **{item['observation_id']} — {item['observation_name']}**: {item['rival_hypothesis_count']} rival hypotheses; "
        f"leading hypothesis: {item['leading_hypothesis_name']} ({item['leading_hypothesis_score']}); "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Priority evidence pathways")
report.append("")

for item in top_evidence:
    report.append(
        f"- **{item['evidence_id']} — {item['evidence_name']}** for **{item['hypothesis_name']}**: "
        f"value {item['evidence_value_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Evidence pathways needing improvement")
report.append("")

for item in weak_evidence:
    report.append(
        f"- **{item['evidence_id']} — {item['evidence_name']}**: value {item['evidence_value_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strongest disconfirmation tests")
report.append("")

for item in top_disconfirm:
    report.append(
        f"- **{item['test_id']} — {item['test_name']}** for **{item['hypothesis_name']}**: "
        f"quality {item['disconfirmation_quality_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Commitment-level cautions")
report.append("")

for item in commitment_risks:
    report.append(
        f"- **{item['commitment_id']} — {item['hypothesis_name']}**: readiness {item['commitment_readiness_score']}; "
        f"current commitment: {item['current_commitment']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strongest revision triggers")
report.append("")

for item in top_revision:
    report.append(
        f"- **{item['trigger_id']} — {item['trigger_name']}** for **{item['hypothesis_name']}**: "
        f"revision quality {item['revision_quality_score']}; action if triggered: {item['action_if_triggered']}."
    )

report.append("")
report.append("## Highest-value hypothesis portfolio items")
report.append("")

for item in top_portfolio:
    report.append(
        f"- **{item['portfolio_id']} — {item['hypothesis_name']}** ({item['portfolio_role']}): "
        f"portfolio value {item['portfolio_value_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Highest-value abductive reasoning interventions")
report.append("")

for item in top_interventions:
    report.append(
        f"- **{item['intervention_id']} — {item['intervention_name']}**: value {item['intervention_value_score']}; "
        f"target: {item['target_abductive_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "The value of this workflow is disciplined strategic speculation. It helps teams avoid first-plausible explanations, "
    "narrative comfort, confirmation-seeking inquiry, frame lock, mechanism gaps, and overcommitment to weak hypotheses. "
    "It supports abductive reasoning as a governed learning process: infer, compare, test, revise, and preserve decision memory."
)

(REPORTS / "abductive_hypothesis_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_hypotheses": top_hypotheses,
    "weak_hypotheses": weak_hypotheses,
    "rival_review": rival_rows,
    "top_evidence": top_evidence,
    "weak_evidence": weak_evidence,
    "top_disconfirmation": top_disconfirm,
    "commitment_risks": commitment_risks,
    "top_revision_triggers": top_revision,
    "top_portfolio": top_portfolio,
    "top_interventions": top_interventions,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced abductive hypothesis diagnostics complete.")
print(f"Wrote: {TABLES / 'hypothesis_scores.csv'}")
print(f"Wrote: {TABLES / 'rival_hypothesis_review.csv'}")
print(f"Wrote: {TABLES / 'evidence_pathway_review.csv'}")
print(f"Wrote: {TABLES / 'disconfirmation_review.csv'}")
print(f"Wrote: {TABLES / 'commitment_level_review.csv'}")
print(f"Wrote: {TABLES / 'revision_trigger_review.csv'}")
print(f"Wrote: {TABLES / 'hypothesis_portfolio_review.csv'}")
print(f"Wrote: {TABLES / 'intervention_recommendations.csv'}")
print(f"Wrote: {REPORTS / 'abductive_hypothesis_diagnostic_report.md'}")
