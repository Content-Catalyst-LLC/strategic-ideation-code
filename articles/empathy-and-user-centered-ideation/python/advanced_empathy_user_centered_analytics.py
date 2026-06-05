#!/usr/bin/env python3
"""
Optional advanced analytics for Empathy and User-Centered Ideation.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- empathy profile chart
- superficiality risk chart
- journey friction chart
- unmet need chart
- reframing quality chart
- ethical empathy risk chart
- systems empathy risk chart
- idea quality simulation chart
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

contexts = pd.read_csv(RAW / "empathy_contexts.csv")
journeys = pd.read_csv(RAW / "journey_friction.csv")
needs = pd.read_csv(RAW / "unmet_needs.csv")
reframes = pd.read_csv(RAW / "problem_reframes.csv")
ethics = pd.read_csv(RAW / "ethical_empathy.csv")
systems = pd.read_csv(RAW / "systems_empathy.csv")

contexts["empathy_profile_score"] = (
    0.16 * contexts["observational_depth"]
    - 0.14 * contexts["projection_risk"]
    + 0.16 * contexts["unmet_need_visibility"]
    + 0.12 * contexts["stakeholder_breadth"]
    + 0.16 * contexts["reframing_potential"]
    + 0.10 * contexts["ethical_review"]
    + 0.10 * contexts["systems_awareness"]
    + 0.14 * contexts["decision_linkage"]
    + 0.10 * contexts["institutional_memory"]
)

contexts["superficiality_risk"] = (
    0.20 * contexts["projection_risk"]
    + 0.16 * (1 - contexts["decision_linkage"])
    + 0.14 * (1 - contexts["observational_depth"])
    + 0.12 * (1 - contexts["unmet_need_visibility"])
    + 0.12 * (1 - contexts["ethical_review"])
    + 0.10 * (1 - contexts["systems_awareness"])
    + 0.08 * (1 - contexts["stakeholder_breadth"])
    + 0.08 * (1 - contexts["institutional_memory"])
)

contexts.sort_values("empathy_profile_score", ascending=True).plot(
    kind="barh",
    x="context_name",
    y="empathy_profile_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Empathy and User-Centered Ideation Profile Scores")
plt.xlabel("Profile score")
plt.ylabel("Context")
plt.tight_layout()
plt.savefig(FIGURES / "empathy_profile_scores.png", dpi=160)
plt.close()

contexts.sort_values("superficiality_risk", ascending=True).plot(
    kind="barh",
    x="context_name",
    y="superficiality_risk",
    legend=False,
    figsize=(12, 8),
)
plt.title("Superficial Empathy and Projection Risk")
plt.xlabel("Risk")
plt.ylabel("Context")
plt.tight_layout()
plt.savefig(FIGURES / "superficiality_risk.png", dpi=160)
plt.close()

journeys["accumulated_burden_score"] = (
    0.13 * journeys["time_cost"]
    + 0.14 * journeys["cognitive_load"]
    + 0.14 * journeys["emotional_cost"]
    + 0.14 * journeys["trust_risk"]
    + 0.12 * journeys["accessibility_burden"]
    + 0.13 * journeys["uncertainty"]
    + 0.10 * journeys["workaround_dependency"]
    + 0.10 * journeys["dropoff_risk"]
)

journeys.sort_values("accumulated_burden_score", ascending=True).plot(
    kind="barh",
    x="stage_name",
    y="accumulated_burden_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Journey Friction and Accumulated Burden")
plt.xlabel("Burden")
plt.ylabel("Journey stage")
plt.tight_layout()
plt.savefig(FIGURES / "journey_friction_scores.png", dpi=160)
plt.close()

needs["unmet_need_priority"] = (
    0.10 * (1 - needs["visibility"])
    + 0.18 * needs["criticality"]
    + 0.12 * needs["frequency"]
    + 0.16 * needs["burden_intensity"]
    + 0.12 * needs["evidence_strength"]
    + 0.14 * needs["solution_fit_uncertainty"]
    + 0.18 * needs["stakeholder_sensitivity"]
)

needs.sort_values("unmet_need_priority", ascending=True).plot(
    kind="barh",
    x="need_id",
    y="unmet_need_priority",
    legend=False,
    figsize=(12, 8),
)
plt.title("Unmet Need Priority")
plt.xlabel("Priority")
plt.ylabel("Need")
plt.tight_layout()
plt.savefig(FIGURES / "unmet_need_priority.png", dpi=160)
plt.close()

reframes["reframing_quality_score"] = (
    0.14 * reframes["inquiry_influence"]
    + 0.14 * reframes["projection_reduction"]
    + 0.14 * reframes["causal_depth"]
    + 0.13 * reframes["stakeholder_evidence"]
    + 0.12 * reframes["systems_context"]
    + 0.11 * reframes["ethical_awareness"]
    + 0.12 * reframes["decision_usefulness"]
)

reframes.sort_values("reframing_quality_score", ascending=True).plot(
    kind="barh",
    x="reframe_id",
    y="reframing_quality_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Reframing Quality")
plt.xlabel("Quality")
plt.ylabel("Reframe")
plt.tight_layout()
plt.savefig(FIGURES / "reframing_quality_scores.png", dpi=160)
plt.close()

ethics["ethical_empathy_score"] = (
    0.13 * ethics["participation_quality"]
    + 0.14 * ethics["power_awareness"]
    + 0.13 * ethics["burden_visibility"]
    + 0.11 * ethics["consent_quality"]
    + 0.12 * ethics["representation_quality"]
    + 0.12 * ethics["redress_quality"]
    + 0.13 * ethics["decision_traceability"]
    + 0.12 * ethics["harm_monitoring"]
)
ethics["ethical_empathy_risk"] = 1 - ethics["ethical_empathy_score"]

ethics.sort_values("ethical_empathy_risk", ascending=True).plot(
    kind="barh",
    x="ethical_issue",
    y="ethical_empathy_risk",
    legend=False,
    figsize=(12, 9),
)
plt.title("Ethical Empathy Risk")
plt.xlabel("Risk")
plt.ylabel("Ethical issue")
plt.tight_layout()
plt.savefig(FIGURES / "ethical_empathy_risk.png", dpi=160)
plt.close()

systems["systems_empathy_risk"] = (
    0.14 * systems["feedback_risk"]
    + 0.11 * systems["delay_risk"]
    + 0.16 * systems["burden_shift_risk"]
    + 0.14 * systems["incentive_misalignment"]
    + 0.12 * systems["metric_gaming_risk"]
    + 0.12 * systems["context_dependency"]
    + 0.11 * systems["leverage_relevance"]
    - 0.10 * systems["monitoring_quality"]
)

systems.sort_values("systems_empathy_risk", ascending=True).plot(
    kind="barh",
    x="system_issue",
    y="systems_empathy_risk",
    legend=False,
    figsize=(12, 9),
)
plt.title("Systems Empathy Risk")
plt.xlabel("Risk")
plt.ylabel("System issue")
plt.tight_layout()
plt.savefig(FIGURES / "systems_empathy_risk.png", dpi=160)
plt.close()

time_steps = np.arange(1, 31)

def simulate_context(row):
    state = np.zeros(len(time_steps))
    state[0] = 0.35

    for t in range(1, len(time_steps)):
        gain = (
            0.16 * row["observational_depth"]
            + 0.18 * row["reframing_potential"]
            + 0.12 * row["systems_awareness"]
            + 0.10 * row["ethical_review"]
            + 0.16 * row["decision_linkage"]
            - 0.14 * row["projection_risk"]
        )
        drift = 0.03 * (1 - row["decision_linkage"])
        state[t] = np.clip(state[t - 1] + gain / 5 - drift, 0, 1.8)

    return state

simulation = pd.DataFrame({"time": time_steps})
for _, row in contexts.iterrows():
    simulation[row["context_name"]] = simulate_context(row)

plt.figure(figsize=(11, 7))
for col in simulation.columns[1:]:
    plt.plot(simulation["time"], simulation[col], label=col)
plt.xlabel("Time Step")
plt.ylabel("Idea Quality")
plt.title("Idea Quality from Empathic Insight")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "empathy_idea_quality_simulation.png", dpi=160)
plt.close()

contexts.to_csv(TABLES / "advanced_empathy_profile_scores.csv", index=False)
journeys.to_csv(TABLES / "advanced_journey_friction_scores.csv", index=False)
needs.to_csv(TABLES / "advanced_unmet_need_scores.csv", index=False)
reframes.to_csv(TABLES / "advanced_reframing_quality_scores.csv", index=False)
ethics.to_csv(TABLES / "advanced_ethical_empathy_scores.csv", index=False)
systems.to_csv(TABLES / "advanced_systems_empathy_scores.csv", index=False)
simulation.to_csv(TABLES / "empathy_idea_quality_simulation.csv", index=False)

print("Advanced empathy and user-centered ideation analytics complete.")
print(f"Wrote: {FIGURES / 'empathy_profile_scores.png'}")
print(f"Wrote: {FIGURES / 'superficiality_risk.png'}")
print(f"Wrote: {FIGURES / 'journey_friction_scores.png'}")
print(f"Wrote: {FIGURES / 'unmet_need_priority.png'}")
print(f"Wrote: {FIGURES / 'reframing_quality_scores.png'}")
print(f"Wrote: {FIGURES / 'ethical_empathy_risk.png'}")
print(f"Wrote: {FIGURES / 'systems_empathy_risk.png'}")
print(f"Wrote: {FIGURES / 'empathy_idea_quality_simulation.png'}")
