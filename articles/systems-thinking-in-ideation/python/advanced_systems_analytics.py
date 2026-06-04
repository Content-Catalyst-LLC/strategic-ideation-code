#!/usr/bin/env python3
"""
Optional advanced analytics for systems thinking in ideation.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- systems-ideation score chart
- symptom-focus risk chart
- leverage-point score chart
- boundary quality chart
- unintended-consequence risk chart
- learning-loop quality chart
- structural intervention simulation chart
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

systems = pd.read_csv(RAW / "systems_profiles.csv")
leverage = pd.read_csv(RAW / "leverage_points.csv")
boundaries = pd.read_csv(RAW / "boundary_reviews.csv")
consequences = pd.read_csv(RAW / "unintended_consequences.csv")
learning = pd.read_csv(RAW / "learning_loops.csv")
portfolio = pd.read_csv(RAW / "intervention_portfolio.csv")

systems["systems_ideation_score"] = (
    0.14 * systems["feedback_awareness"]
    + 0.14 * systems["leverage_sensitivity"]
    + 0.13 * systems["root_cause_depth"]
    + 0.12 * systems["stakeholder_visibility"]
    + 0.12 * systems["boundary_quality"]
    + 0.10 * systems["stock_flow_awareness"]
    + 0.10 * systems["delay_awareness"]
    + 0.13 * systems["adaptive_learning"]
    - 0.10 * systems["unintended_consequence_risk"]
    - 0.08 * systems["local_optimization_risk"]
)

systems["symptom_focus_risk"] = (
    (1.0 - systems["root_cause_depth"]) * 0.30
    + (1.0 - systems["leverage_sensitivity"]) * 0.25
    + systems["local_optimization_risk"] * 0.25
    + systems["unintended_consequence_risk"] * 0.20
)

systems.sort_values("systems_ideation_score", ascending=True).plot(
    kind="barh",
    x="system_name",
    y="systems_ideation_score",
    legend=False,
    figsize=(12, 9),
)
plt.title("Systems-Ideation Scores")
plt.xlabel("Systems-ideation score")
plt.ylabel("System")
plt.tight_layout()
plt.savefig(FIGURES / "systems_ideation_scores.png", dpi=160)
plt.close()

systems.sort_values("symptom_focus_risk", ascending=True).plot(
    kind="barh",
    x="system_name",
    y="symptom_focus_risk",
    legend=False,
    figsize=(12, 9),
)
plt.title("Symptom-Focus Risk")
plt.xlabel("Risk score")
plt.ylabel("System")
plt.tight_layout()
plt.savefig(FIGURES / "symptom_focus_risk.png", dpi=160)
plt.close()

leverage["leverage_value_score"] = (
    0.22 * leverage["leverage_depth"]
    + 0.12 * leverage["implementation_feasibility"]
    + 0.12 * leverage["evidence_quality"]
    + 0.12 * leverage["stakeholder_legitimacy"]
    + 0.08 * leverage["reversibility"]
    + 0.16 * leverage["system_sensitivity"]
    - 0.10 * leverage["risk_exposure"]
    - 0.08 * leverage["time_to_effect"]
)

leverage.sort_values("leverage_value_score", ascending=True).plot(
    kind="barh",
    x="intervention_name",
    y="leverage_value_score",
    legend=False,
    figsize=(12, 9),
)
plt.title("Leverage-Point Value Scores")
plt.xlabel("Leverage score")
plt.ylabel("Intervention")
plt.tight_layout()
plt.savefig(FIGURES / "leverage_point_scores.png", dpi=160)
plt.close()

boundaries["boundary_quality_score"] = (
    0.16 * boundaries["stakeholder_inclusion"]
    + 0.14 * boundaries["downstream_effect_visibility"]
    + 0.14 * boundaries["externality_visibility"]
    + 0.14 * boundaries["implementation_visibility"]
    + 0.14 * boundaries["ecological_or_social_context"]
    + 0.14 * boundaries["hidden_dependency_visibility"]
    - 0.12 * boundaries["boundary_risk"]
)

boundaries.sort_values("boundary_quality_score", ascending=True).plot(
    kind="barh",
    x="boundary_name",
    y="boundary_quality_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Boundary Quality Scores")
plt.xlabel("Boundary quality score")
plt.ylabel("Boundary")
plt.tight_layout()
plt.savefig(FIGURES / "boundary_quality_scores.png", dpi=160)
plt.close()

consequences["consequence_risk_score"] = (
    0.20 * consequences["likelihood"]
    + 0.20 * consequences["severity"]
    + 0.16 * consequences["stakeholder_burden"]
    + 0.12 * consequences["delay_length"]
    - 0.12 * consequences["detectability"]
    - 0.10 * consequences["reversibility"]
    - 0.10 * consequences["mitigation_quality"]
)

consequences.sort_values("consequence_risk_score", ascending=True).plot(
    kind="barh",
    x="intervention_name",
    y="consequence_risk_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Unintended-Consequence Risk Scores")
plt.xlabel("Risk score")
plt.ylabel("Intervention")
plt.tight_layout()
plt.savefig(FIGURES / "unintended_consequence_risk_scores.png", dpi=160)
plt.close()

learning["learning_quality_score"] = (
    0.16 * learning["feedback_quality"]
    + 0.16 * learning["revision_trigger_clarity"]
    + 0.16 * learning["decision_memory_quality"]
    + 0.14 * learning["stakeholder_learning_visibility"]
    + 0.14 * learning["implementation_signal_quality"]
    + 0.14 * learning["governance_response_capacity"]
    + 0.08 * learning["cycle_time"]
    - 0.10 * learning["learning_risk"]
)

learning.sort_values("learning_quality_score", ascending=True).plot(
    kind="barh",
    x="learning_loop_name",
    y="learning_quality_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Learning-Loop Quality Scores")
plt.xlabel("Learning-loop quality")
plt.ylabel("Learning loop")
plt.tight_layout()
plt.savefig(FIGURES / "learning_loop_quality_scores.png", dpi=160)
plt.close()

# Structural intervention simulation.
time_steps = np.arange(1, 31)

def simulate_system(feedback, leverage_sensitivity, boundary, stakeholder, learning_capacity, risk, initial_state=0.30):
    state = np.zeros(len(time_steps))
    state[0] = initial_state

    for t in range(1, len(time_steps)):
        gain = (
            0.16 * feedback
            + 0.18 * leverage_sensitivity
            + 0.12 * boundary
            + 0.12 * stakeholder
            + 0.16 * learning_capacity
        )
        drag = 0.14 * risk
        adaptive_gain = 0.01 * feedback * learning_capacity * np.log1p(t)
        state[t] = state[t - 1] + gain / 5 - drag / 6 + adaptive_gain
        state[t] = np.clip(state[t], 0, 1.8)

    return state

simulation = pd.DataFrame({"time": time_steps})

for _, row in systems.iterrows():
    if row["system_id"] in {"SYS001", "SYS002", "SYS003", "SYS005", "SYS006"}:
        simulation[row["system_name"]] = simulate_system(
            feedback=row["feedback_awareness"],
            leverage_sensitivity=row["leverage_sensitivity"],
            boundary=row["boundary_quality"],
            stakeholder=row["stakeholder_visibility"],
            learning_capacity=row["adaptive_learning"],
            risk=row["unintended_consequence_risk"],
        )

plt.figure(figsize=(11, 7))
for col in simulation.columns[1:]:
    plt.plot(simulation["time"], simulation[col], label=col)
plt.xlabel("Ideation Cycle")
plt.ylabel("Intervention Quality")
plt.title("Structural Intervention Quality Over Time")
plt.legend()
plt.tight_layout()
plt.savefig(FIGURES / "structural_intervention_simulation.png", dpi=160)
plt.close()

systems.to_csv(TABLES / "advanced_systems_ideation_scores.csv", index=False)
leverage.to_csv(TABLES / "advanced_leverage_point_scores.csv", index=False)
boundaries.to_csv(TABLES / "advanced_boundary_quality_scores.csv", index=False)
consequences.to_csv(TABLES / "advanced_unintended_consequence_scores.csv", index=False)
learning.to_csv(TABLES / "advanced_learning_loop_scores.csv", index=False)
portfolio.to_csv(TABLES / "advanced_intervention_portfolio.csv", index=False)
simulation.to_csv(TABLES / "advanced_structural_intervention_simulation.csv", index=False)

print("Advanced systems analytics complete.")
print(f"Wrote: {FIGURES / 'systems_ideation_scores.png'}")
print(f"Wrote: {FIGURES / 'symptom_focus_risk.png'}")
print(f"Wrote: {FIGURES / 'leverage_point_scores.png'}")
print(f"Wrote: {FIGURES / 'boundary_quality_scores.png'}")
print(f"Wrote: {FIGURES / 'unintended_consequence_risk_scores.png'}")
print(f"Wrote: {FIGURES / 'learning_loop_quality_scores.png'}")
print(f"Wrote: {FIGURES / 'structural_intervention_simulation.png'}")
