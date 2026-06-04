#!/usr/bin/env python3
"""
Advanced strategist-facing layer alignment diagnostics.

This dependency-light workflow uses only the Python standard library.

It produces:
- layer-level context diagnostics
- strategic initiative portfolio scores
- assumption-risk adjustments
- tactical translation gaps
- feedback routing recommendations
- a markdown strategist diagnostic report

The workflow is designed for strategy teams that need to distinguish:
- ideation / conceptual failures
- strategy / directional failures
- tactics / operational failures
- learning / feedback-routing failures
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


contexts = read_csv(RAW / "layer_profile_contexts.csv")
initiatives = read_csv(RAW / "strategic_initiatives.csv")
tactics = read_csv(RAW / "tactical_actions.csv")
assumptions = read_csv(RAW / "assumptions.csv")
feedback_events = read_csv(RAW / "feedback_events.csv")
criteria = read_csv(RAW / "criteria_weights.csv")

weights = {row["criterion"]: float(row["weight"]) for row in criteria}

# ---------------------------------------------------------------------
# 1. Context-level layer alignment diagnostics
# ---------------------------------------------------------------------

def diagnose_context(row: dict[str, str]) -> tuple[str, str]:
    ideation = f(row, "ideation_quality")
    strategy = f(row, "strategic_clarity")
    tactics_score = f(row, "tactical_alignment")
    feedback = f(row, "feedback_quality")
    learning = f(row, "adaptive_learning")
    memory = f(row, "decision_memory")
    ethics = f(row, "ethical_legitimacy")

    weakest = min(
        [
            ("ideation", ideation),
            ("strategy", strategy),
            ("tactics", tactics_score),
            ("feedback", feedback),
            ("learning", learning),
            ("memory", memory),
            ("ethics", ethics),
        ],
        key=lambda item: item[1],
    )

    if tactics_score >= 0.70 and ideation < 0.50:
        return "conceptual_narrowness", "Open reframing before adding more execution."
    if tactics_score >= 0.65 and strategy < 0.55:
        return "tactical_overload", "Clarify strategic choice rules before expanding activity."
    if ideation >= 0.75 and strategy < 0.55:
        return "selection_gap", "Move from possibility generation to tradeoff and choice."
    if strategy >= 0.70 and tactics_score < 0.55:
        return "translation_gap", "Convert strategy into tactical pathways, owners, and decision rights."
    if feedback < 0.55 or learning < 0.55:
        return "learning_gap", "Create feedback routing and after-action review by layer."
    if memory < 0.50:
        return "decision_memory_gap", "Record assumptions, rejected alternatives, rationale, and review triggers."
    if ethics < 0.60:
        return "legitimacy_gap", "Add stakeholder burden, voice, and accountability review."
    return weakest[0] + "_watch", "Monitor the weakest layer and protect cross-layer learning."


context_rows: list[dict[str, object]] = []

for row in contexts:
    diagnosis, recommendation = diagnose_context(row)

    layer_alignment_score = (
        0.16 * f(row, "ideation_quality")
        + 0.20 * f(row, "strategic_clarity")
        + 0.18 * f(row, "tactical_alignment")
        + 0.14 * f(row, "feedback_quality")
        + 0.14 * f(row, "adaptive_learning")
        + 0.08 * f(row, "decision_memory")
        + 0.10 * f(row, "ethical_legitimacy")
    )

    balance_penalty = max(
        [
            f(row, "ideation_quality"),
            f(row, "strategic_clarity"),
            f(row, "tactical_alignment"),
            f(row, "feedback_quality"),
            f(row, "adaptive_learning"),
        ]
    ) - min(
        [
            f(row, "ideation_quality"),
            f(row, "strategic_clarity"),
            f(row, "tactical_alignment"),
            f(row, "feedback_quality"),
            f(row, "adaptive_learning"),
        ]
    )

    adjusted_score = layer_alignment_score - 0.12 * balance_penalty

    context_rows.append(
        {
            "context_id": row["context_id"],
            "context_name": row["context_name"],
            "context_type": row["context_type"],
            "layer_alignment_score": round(layer_alignment_score, 4),
            "balance_penalty": round(balance_penalty, 4),
            "adjusted_alignment_score": round(adjusted_score, 4),
            "diagnosis": diagnosis,
            "recommendation": recommendation,
        }
    )

context_rows.sort(key=lambda item: item["adjusted_alignment_score"], reverse=True)

write_csv(
    TABLES / "layer_alignment_scores.csv",
    context_rows,
    [
        "context_id",
        "context_name",
        "context_type",
        "layer_alignment_score",
        "balance_penalty",
        "adjusted_alignment_score",
        "diagnosis",
        "recommendation",
    ],
)

# ---------------------------------------------------------------------
# 2. Initiative portfolio scoring with assumption-risk adjustment
# ---------------------------------------------------------------------

assumption_risk_by_initiative: dict[str, float] = {}

for initiative_id in {row["initiative_id"] for row in initiatives}:
    linked = [row for row in assumptions if row["initiative_id"] == initiative_id]
    if not linked:
        assumption_risk_by_initiative[initiative_id] = 0.0
        continue

    risks = []
    for item in linked:
        confidence = f(item, "confidence")
        criticality = f(item, "criticality")
        risks.append((1.0 - confidence) * criticality)

    assumption_risk_by_initiative[initiative_id] = mean(risks)


initiative_rows: list[dict[str, object]] = []

for row in initiatives:
    assumption_risk = assumption_risk_by_initiative.get(row["initiative_id"], 0.0)

    score = (
        weights["strategic_fit"] * f(row, "strategic_fit")
        + weights["implementation_feasibility"] * f(row, "implementation_feasibility")
        + weights["systems_leverage"] * f(row, "systems_leverage")
        + weights["learning_value"] * f(row, "learning_value")
        + weights["ethical_legitimacy"] * f(row, "ethical_legitimacy")
        - weights["uncertainty_penalty"] * f(row, "uncertainty")
        - weights["assumption_risk_penalty"] * assumption_risk
    )

    if score >= 0.78 and assumption_risk < 0.30:
        recommendation = "advance"
    elif score >= 0.70:
        recommendation = "prototype_or_revise"
    elif assumption_risk >= 0.40:
        recommendation = "test_assumptions_before_commitment"
    else:
        recommendation = "hold_or_reframe"

    initiative_rows.append(
        {
            "initiative_id": row["initiative_id"],
            "initiative_name": row["initiative_name"],
            "primary_layer": row["primary_layer"],
            "current_status": row["current_status"],
            "portfolio_score": round(score, 4),
            "assumption_risk": round(assumption_risk, 4),
            "uncertainty": row["uncertainty"],
            "recommendation": recommendation,
            "problem_frame": row["problem_frame"],
            "strategic_priority": row["strategic_priority"],
        }
    )

initiative_rows.sort(key=lambda item: item["portfolio_score"], reverse=True)

write_csv(
    TABLES / "initiative_portfolio_scores.csv",
    initiative_rows,
    [
        "initiative_id",
        "initiative_name",
        "primary_layer",
        "current_status",
        "portfolio_score",
        "assumption_risk",
        "uncertainty",
        "recommendation",
        "problem_frame",
        "strategic_priority",
    ],
)

write_csv(
    PROCESSED / "initiative_portfolio_scores.csv",
    initiative_rows,
    [
        "initiative_id",
        "initiative_name",
        "primary_layer",
        "current_status",
        "portfolio_score",
        "assumption_risk",
        "uncertainty",
        "recommendation",
        "problem_frame",
        "strategic_priority",
    ],
)

# ---------------------------------------------------------------------
# 3. Tactical translation gaps
# ---------------------------------------------------------------------

tactical_rows: list[dict[str, object]] = []

for row in tactics:
    alignment = f(row, "alignment_to_strategy")
    readiness = f(row, "execution_readiness")
    resource_fit = f(row, "resource_fit")
    feedback_capture = f(row, "feedback_capture")
    learning_routing = f(row, "learning_routing")
    delivery_risk = f(row, "delivery_risk")

    translation_score = (
        0.26 * alignment
        + 0.20 * readiness
        + 0.16 * resource_fit
        + 0.18 * feedback_capture
        + 0.20 * learning_routing
        - 0.12 * delivery_risk
    )

    if alignment < 0.65:
        gap = "strategic_alignment_gap"
    elif readiness < 0.60:
        gap = "execution_readiness_gap"
    elif learning_routing < 0.65:
        gap = "learning_routing_gap"
    elif delivery_risk > 0.40:
        gap = "delivery_risk_gap"
    else:
        gap = "acceptable_translation"

    tactical_rows.append(
        {
            "tactic_id": row["tactic_id"],
            "initiative_id": row["initiative_id"],
            "tactic_name": row["tactic_name"],
            "owner_group": row["owner_group"],
            "translation_score": round(translation_score, 4),
            "gap_type": gap,
            "alignment_to_strategy": alignment,
            "execution_readiness": readiness,
            "learning_routing": learning_routing,
            "delivery_risk": delivery_risk,
        }
    )

tactical_rows.sort(key=lambda item: item["translation_score"])

write_csv(
    TABLES / "tactical_translation_gaps.csv",
    tactical_rows,
    [
        "tactic_id",
        "initiative_id",
        "tactic_name",
        "owner_group",
        "translation_score",
        "gap_type",
        "alignment_to_strategy",
        "execution_readiness",
        "learning_routing",
        "delivery_risk",
    ],
)

# ---------------------------------------------------------------------
# 4. Feedback routing recommendations
# ---------------------------------------------------------------------

routing_rules = {
    "ideation": "Reopen problem framing, assumptions, boundary choices, and option architecture.",
    "strategy": "Review tradeoffs, priorities, strategic choice rules, and portfolio commitments.",
    "tactics": "Adjust execution design, owners, resources, workflows, timing, or operational constraints.",
    "learning": "Improve feedback capture, interpretation, meeting cadence, and decision-memory routines.",
    "ethics": "Conduct legitimacy, burden, voice, accountability, and affected-stakeholder review.",
}

feedback_rows: list[dict[str, object]] = []

for row in feedback_events:
    affected = row["affected_layer"]
    severity = f(row, "severity")
    signal = f(row, "signal_strength")
    priority = severity * signal

    if priority >= 0.72:
        urgency = "high"
    elif priority >= 0.50:
        urgency = "moderate"
    else:
        urgency = "monitor"

    feedback_rows.append(
        {
            "feedback_id": row["feedback_id"],
            "initiative_id": row["initiative_id"],
            "tactic_id": row["tactic_id"],
            "affected_layer": affected,
            "priority_score": round(priority, 4),
            "urgency": urgency,
            "recommended_routing": row["recommended_routing"],
            "layer_action": routing_rules.get(affected, "Review feedback and assign accountable owner."),
            "feedback_summary": row["feedback_summary"],
        }
    )

feedback_rows.sort(key=lambda item: item["priority_score"], reverse=True)

write_csv(
    TABLES / "feedback_routing_recommendations.csv",
    feedback_rows,
    [
        "feedback_id",
        "initiative_id",
        "tactic_id",
        "affected_layer",
        "priority_score",
        "urgency",
        "recommended_routing",
        "layer_action",
        "feedback_summary",
    ],
)

# ---------------------------------------------------------------------
# 5. Strategist report
# ---------------------------------------------------------------------

top_context = context_rows[0]
lowest_context = context_rows[-1]
top_initiatives = initiative_rows[:5]
highest_risk_assumptions = sorted(
    assumptions,
    key=lambda row: (1.0 - f(row, "confidence")) * f(row, "criticality"),
    reverse=True,
)[:5]
highest_priority_feedback = feedback_rows[:5]
lowest_tactics = tactical_rows[:5]

report_lines: list[str] = []

report_lines.append("# Strategist Diagnostic Report")
report_lines.append("")
report_lines.append("## Executive summary")
report_lines.append("")
report_lines.append(
    f"The strongest synthetic context is **{top_context['context_name']}** "
    f"with an adjusted alignment score of **{top_context['adjusted_alignment_score']}**."
)
report_lines.append(
    f"The weakest synthetic context is **{lowest_context['context_name']}**, "
    f"diagnosed as **{lowest_context['diagnosis']}**. Recommended response: "
    f"{lowest_context['recommendation']}"
)
report_lines.append("")
report_lines.append("## Top initiative portfolio candidates")
report_lines.append("")

for item in top_initiatives:
    report_lines.append(
        f"- **{item['initiative_id']} — {item['initiative_name']}**: "
        f"score {item['portfolio_score']}; recommendation: {item['recommendation']}; "
        f"layer: {item['primary_layer']}."
    )

report_lines.append("")
report_lines.append("## Highest-risk assumptions")
report_lines.append("")

for item in highest_risk_assumptions:
    risk = (1.0 - f(item, "confidence")) * f(item, "criticality")
    report_lines.append(
        f"- **{item['assumption_id']} ({item['initiative_id']})**: "
        f"risk {risk:.3f}; layer: {item['layer']}; test: {item['test_method']}; "
        f"assumption: {item['assumption']}"
    )

report_lines.append("")
report_lines.append("## Tactical translation gaps requiring attention")
report_lines.append("")

for item in lowest_tactics:
    report_lines.append(
        f"- **{item['tactic_id']} — {item['tactic_name']}**: "
        f"translation score {item['translation_score']}; gap: {item['gap_type']}; "
        f"owner: {item['owner_group']}."
    )

report_lines.append("")
report_lines.append("## Highest-priority feedback routing")
report_lines.append("")

for item in highest_priority_feedback:
    report_lines.append(
        f"- **{item['feedback_id']}**: priority {item['priority_score']} ({item['urgency']}); "
        f"route to **{item['affected_layer']}**; action: {item['layer_action']}"
    )

report_lines.append("")
report_lines.append("## Professional interpretation")
report_lines.append("")
report_lines.append(
    "The main strategic value of this workflow is not the numeric score itself. "
    "The value is diagnostic separation. It helps a strategist determine whether a problem "
    "belongs at the ideation layer, the strategy layer, the tactical layer, the feedback layer, "
    "or the legitimacy layer. This prevents organizations from treating every failure as an "
    "execution problem and supports more precise intervention."
)

(REPORTS / "strategist_diagnostic_report.md").write_text("\n".join(report_lines), encoding="utf-8")

# Machine-readable summary.
summary = {
    "top_context": top_context,
    "lowest_context": lowest_context,
    "top_initiatives": top_initiatives,
    "lowest_tactical_translation_scores": lowest_tactics,
    "highest_priority_feedback": highest_priority_feedback,
}

(REPORTS / "diagnostic_summary.json").write_text(
    json.dumps(summary, indent=2),
    encoding="utf-8",
)

print("Advanced layer alignment diagnostics complete.")
print(f"Wrote: {TABLES / 'layer_alignment_scores.csv'}")
print(f"Wrote: {TABLES / 'initiative_portfolio_scores.csv'}")
print(f"Wrote: {TABLES / 'tactical_translation_gaps.csv'}")
print(f"Wrote: {TABLES / 'feedback_routing_recommendations.csv'}")
print(f"Wrote: {REPORTS / 'strategist_diagnostic_report.md'}")
