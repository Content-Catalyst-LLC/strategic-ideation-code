#!/usr/bin/env python3
"""
Optional advanced analytics for Feedback Loops in Design Thinking.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- feedback profile chart
- noisy churn risk chart
- signal quality chart
- interpretation capacity chart
- adjustment pathway chart
- ethical governance chart
- iterative design improvement simulation
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
TABLES = ROOT / "outputs" / "tables"
FIGURES = ROOT / "outputs" / "figures"

FIGURES.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)

try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError as exc:
    print("Missing optional advanced analytics dependencies.")
    print("Run:")
    print("  python3 -m venv .venv")
    print("  source .venv/bin/activate")
    print("  pip install -r python/requirements-advanced.txt")
    raise SystemExit(1) from exc

systems = pd.read_csv(RAW / "feedback_systems.csv")
signals = pd.read_csv(RAW / "signals.csv")
interpretations = pd.read_csv(RAW / "interpretation_capacity.csv")
adjustments = pd.read_csv(RAW / "adjustment_pathways.csv")
ethics = pd.read_csv(RAW / "ethical_governance.csv")

systems["feedback_profile_score"] = (
    0.13 * systems["signal_quality"]
    + 0.13 * systems["interpretation_capacity"]
    + 0.10 * systems["adjustment_speed"]
    + 0.13 * systems["user_insight_depth"]
    + 0.10 * systems["stability"]
    + 0.11 * systems["ethical_integrity"]
    + 0.10 * systems["systems_awareness"]
    + 0.10 * systems["decision_linkage"]
    + 0.10 * systems["learning_memory"]
)

systems["noisy_churn_risk"] = (
    0.16 * systems["adjustment_speed"]
    + 0.15 * (1 - systems["signal_quality"])
    + 0.15 * (1 - systems["interpretation_capacity"])
    + 0.13 * (1 - systems["stability"])
    + 0.12 * (1 - systems["systems_awareness"])
    + 0.12 * (1 - systems["ethical_integrity"])
    + 0.10 * (1 - systems["decision_linkage"])
    + 0.07 * (1 - systems["learning_memory"])
)

systems.sort_values("feedback_profile_score", ascending=True).plot(
    kind="barh",
    x="system_name",
    y="feedback_profile_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Feedback-Loop Design Profile")
plt.xlabel("Profile score")
plt.ylabel("System")
plt.tight_layout()
plt.savefig(FIGURES / "feedback_profile_scores.png", dpi=160)
plt.close()

systems.sort_values("noisy_churn_risk", ascending=True).plot(
    kind="barh",
    x="system_name",
    y="noisy_churn_risk",
    legend=False,
    figsize=(12, 8),
)
plt.title("Noisy Churn Risk")
plt.xlabel("Risk")
plt.ylabel("System")
plt.tight_layout()
plt.savefig(FIGURES / "noisy_churn_risk.png", dpi=160)
plt.close()

signals["signal_quality_score"] = (
    0.15 * signals["relevance"]
    + 0.13 * signals["timeliness"]
    + 0.14 * signals["reliability"]
    + 0.14 * signals["representativeness"]
    + 0.13 * signals["interpretability"]
    + 0.14 * signals["behavioral_richness"]
    - 0.13 * signals["bias_risk"]
)

signals.sort_values("signal_quality_score", ascending=True).plot(
    kind="barh",
    x="signal_source",
    y="signal_quality_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Signal Quality Scores")
plt.xlabel("Signal quality")
plt.ylabel("Signal source")
plt.tight_layout()
plt.savefig(FIGURES / "signal_quality_scores.png", dpi=160)
plt.close()

interpretations["interpretation_capacity_score"] = (
    0.14 * interpretations["contextual_understanding"]
    + 0.13 * interpretations["domain_expertise"]
    + 0.15 * interpretations["user_research_capacity"]
    + 0.15 * interpretations["systems_thinking_capacity"]
    + 0.13 * interpretations["bias_review"]
    + 0.15 * interpretations["triangulation_quality"]
    + 0.15 * interpretations["decision_relevance"]
)

interpretations.sort_values("interpretation_capacity_score", ascending=True).plot(
    kind="barh",
    x="interpretation_practice",
    y="interpretation_capacity_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Interpretation Capacity Scores")
plt.xlabel("Interpretation capacity")
plt.ylabel("Interpretation practice")
plt.tight_layout()
plt.savefig(FIGURES / "interpretation_capacity_scores.png", dpi=160)
plt.close()

adjustments["adjustment_pathway_score"] = (
    0.15 * adjustments["decision_authority"]
    + 0.12 * adjustments["resource_availability"]
    + 0.14 * adjustments["revision_trigger_quality"]
    + 0.10 * adjustments["implementation_speed"]
    + 0.14 * adjustments["change_traceability"]
    + 0.13 * adjustments["stability_protection"]
    + 0.12 * adjustments["communication_quality"]
)

adjustments.sort_values("adjustment_pathway_score", ascending=True).plot(
    kind="barh",
    x="adjustment_pathway",
    y="adjustment_pathway_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Adjustment Pathway Scores")
plt.xlabel("Adjustment pathway score")
plt.ylabel("Adjustment pathway")
plt.tight_layout()
plt.savefig(FIGURES / "adjustment_pathway_scores.png", dpi=160)
plt.close()

ethics["ethical_governance_score"] = (
    0.14 * ethics["privacy_protection"]
    + 0.13 * ethics["consent_quality"]
    + 0.14 * ethics["accessibility_review"]
    + 0.13 * ethics["burden_review"]
    + 0.13 * ethics["representation_quality"]
    + 0.10 * ethics["redress_path"]
    + 0.12 * ethics["accountability_quality"]
    + 0.11 * ethics["governance_traceability"]
)

ethics["ethical_governance_risk"] = 1 - ethics["ethical_governance_score"]

ethics.sort_values("ethical_governance_risk", ascending=True).plot(
    kind="barh",
    x="ethical_issue",
    y="ethical_governance_risk",
    legend=False,
    figsize=(12, 9),
)
plt.title("Ethical Feedback Governance Risk")
plt.xlabel("Risk")
plt.ylabel("Ethical issue")
plt.tight_layout()
plt.savefig(FIGURES / "ethical_governance_risk.png", dpi=160)
plt.close()

time_steps = np.arange(1, 41)

def simulate_system(row):
    state = np.zeros(len(time_steps))
    state[0] = 0.30
    for t in range(1, len(time_steps)):
        learning_gain = (
            0.12 * row["signal_quality"]
            + 0.12 * row["interpretation_capacity"]
            + 0.08 * row["adjustment_speed"]
            + 0.12 * row["user_insight_depth"]
            + 0.09 * row["systems_awareness"]
            + 0.08 * row["ethical_integrity"]
            + 0.10 * row["decision_linkage"]
            + 0.08 * row["learning_memory"]
        )
        churn_penalty = 0.06 * row["adjustment_speed"] * (1 - row["interpretation_capacity"])
        ethics_penalty = 0.04 * (1 - row["ethical_integrity"])
        decision_drift = 0.05 * (1 - row["decision_linkage"])
        disturbance = 0.10 * (1 - row["stability"]) * np.sin(t / 4)
        state[t] = state[t - 1] + learning_gain / 5 - churn_penalty / 5 - ethics_penalty / 5 - decision_drift / 5 + disturbance / 10
        state[t] = np.clip(state[t], 0, 1.8)
    return state

simulation = pd.DataFrame({"time": time_steps})
for _, row in systems.iterrows():
    simulation[row["system_name"]] = simulate_system(row)

plt.figure(figsize=(11, 7))
for col in simulation.columns[1:]:
    plt.plot(simulation["time"], simulation[col], label=col)
plt.xlabel("Time Step")
plt.ylabel("Design Performance")
plt.title("Iterative Design Improvement Through Feedback")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "iterative_design_improvement.png", dpi=160)
plt.close()

systems.to_csv(TABLES / "advanced_feedback_system_profile_scores.csv", index=False)
signals.to_csv(TABLES / "advanced_signal_quality_scores.csv", index=False)
interpretations.to_csv(TABLES / "advanced_interpretation_capacity_scores.csv", index=False)
adjustments.to_csv(TABLES / "advanced_adjustment_pathway_scores.csv", index=False)
ethics.to_csv(TABLES / "advanced_ethical_governance_scores.csv", index=False)
simulation.to_csv(TABLES / "iterative_design_improvement_simulation.csv", index=False)

print("Advanced feedback-loop analytics complete.")
print(f"Wrote: {FIGURES / 'feedback_profile_scores.png'}")
print(f"Wrote: {FIGURES / 'noisy_churn_risk.png'}")
print(f"Wrote: {FIGURES / 'signal_quality_scores.png'}")
print(f"Wrote: {FIGURES / 'interpretation_capacity_scores.png'}")
print(f"Wrote: {FIGURES / 'adjustment_pathway_scores.png'}")
print(f"Wrote: {FIGURES / 'ethical_governance_risk.png'}")
print(f"Wrote: {FIGURES / 'iterative_design_improvement.png'}")
