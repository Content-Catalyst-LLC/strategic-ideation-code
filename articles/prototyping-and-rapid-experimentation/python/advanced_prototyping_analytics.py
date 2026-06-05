#!/usr/bin/env python3
"""
Optional advanced analytics for Prototyping and Rapid Experimentation.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- experimentation profile chart
- superficial testing risk chart
- assumption priority chart
- prototype fit chart
- experiment quality chart
- evidence quality chart
- systems impact chart
- iterative strategic learning simulation
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

systems = pd.read_csv(RAW / "experimentation_systems.csv")
assumptions = pd.read_csv(RAW / "assumptions.csv")
prototypes = pd.read_csv(RAW / "prototypes.csv")
experiments = pd.read_csv(RAW / "experiments.csv")
evidence = pd.read_csv(RAW / "evidence.csv")
impacts = pd.read_csv(RAW / "systems_impact.csv")

systems["experimentation_profile_score"] = (
    0.10 * systems["speed"]
    + 0.09 * systems["cost_efficiency"]
    + 0.15 * systems["insight_depth"]
    + 0.12 * systems["user_validation"]
    + 0.12 * systems["assumption_criticality"]
    + 0.14 * systems["evidence_quality"]
    + 0.10 * systems["systems_awareness"]
    + 0.08 * systems["ethical_review"]
    + 0.10 * systems["decision_linkage"]
    + 0.10 * systems["learning_memory"]
)

systems["superficial_testing_risk"] = (
    0.14 * systems["speed"]
    + 0.16 * (1 - systems["insight_depth"])
    + 0.15 * (1 - systems["evidence_quality"])
    + 0.13 * (1 - systems["systems_awareness"])
    + 0.13 * (1 - systems["ethical_review"])
    + 0.13 * (1 - systems["decision_linkage"])
    + 0.09 * (1 - systems["assumption_criticality"])
    + 0.07 * (1 - systems["learning_memory"])
)

systems.sort_values("experimentation_profile_score", ascending=True).plot(
    kind="barh",
    x="system_name",
    y="experimentation_profile_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Experimentation Learning Profile")
plt.xlabel("Profile score")
plt.ylabel("System")
plt.tight_layout()
plt.savefig(FIGURES / "experimentation_profile_scores.png", dpi=160)
plt.close()

systems.sort_values("superficial_testing_risk", ascending=True).plot(
    kind="barh",
    x="system_name",
    y="superficial_testing_risk",
    legend=False,
    figsize=(12, 8),
)
plt.title("Superficial Testing Risk")
plt.xlabel("Risk")
plt.ylabel("System")
plt.tight_layout()
plt.savefig(FIGURES / "superficial_testing_risk.png", dpi=160)
plt.close()

assumptions["assumption_priority_score"] = (
    0.16 * assumptions["uncertainty"]
    + 0.17 * assumptions["strategic_significance"]
    + 0.13 * assumptions["reversibility_risk"]
    + 0.14 * assumptions["cost_of_error"]
    + 0.13 * assumptions["evidence_gap"]
    + 0.14 * assumptions["stakeholder_sensitivity"]
    + 0.08 * assumptions["testing_feasibility"]
)

assumptions.sort_values("assumption_priority_score", ascending=True).plot(
    kind="barh",
    x="assumption_id",
    y="assumption_priority_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Assumption Priority Scores")
plt.xlabel("Priority")
plt.ylabel("Assumption")
plt.tight_layout()
plt.savefig(FIGURES / "assumption_priority_scores.png", dpi=160)
plt.close()

prototypes["prototype_fit_score"] = (
    0.20 * prototypes["learning_fit"]
    - 0.10 * prototypes["cost_to_build"]
    + 0.12 * prototypes["speed_to_test"]
    + 0.13 * prototypes["reversibility"]
    + 0.14 * prototypes["user_context_realism"]
    + 0.13 * prototypes["operational_realism"]
    + 0.12 * prototypes["systems_visibility"]
    + 0.06 * (1 - (prototypes["fidelity"] - prototypes["learning_fit"]).abs())
)

prototypes.sort_values("prototype_fit_score", ascending=True).plot(
    kind="barh",
    x="prototype_name",
    y="prototype_fit_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Prototype Fit Scores")
plt.xlabel("Fit")
plt.ylabel("Prototype")
plt.tight_layout()
plt.savefig(FIGURES / "prototype_fit_scores.png", dpi=160)
plt.close()

experiments["experiment_quality_score"] = (
    0.15 * experiments["learning_target_clarity"]
    + 0.12 * experiments["test_condition_quality"]
    + 0.15 * experiments["evidence_standard_quality"]
    + 0.12 * experiments["participant_fit"]
    + 0.13 * experiments["risk_boundary_quality"]
    + 0.11 * experiments["interpretation_limit_clarity"]
    + 0.14 * experiments["decision_rule_quality"]
    + 0.08 * experiments["repeatability"]
)

experiments.sort_values("experiment_quality_score", ascending=True).plot(
    kind="barh",
    x="experiment_id",
    y="experiment_quality_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Experiment Quality Scores")
plt.xlabel("Quality")
plt.ylabel("Experiment")
plt.tight_layout()
plt.savefig(FIGURES / "experiment_quality_scores.png", dpi=160)
plt.close()

evidence["evidence_quality_score"] = (
    0.16 * evidence["relevance"]
    + 0.15 * evidence["validity"]
    + 0.13 * evidence["contextual_realism"]
    + 0.14 * evidence["behavioral_richness"]
    + 0.13 * evidence["interpretability"]
    + 0.16 * evidence["decision_usefulness"]
    - 0.13 * evidence["limitation_severity"]
)

evidence.sort_values("evidence_quality_score", ascending=True).plot(
    kind="barh",
    x="evidence_type",
    y="evidence_quality_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Evidence Quality Scores")
plt.xlabel("Quality")
plt.ylabel("Evidence type")
plt.tight_layout()
plt.savefig(FIGURES / "evidence_quality_scores.png", dpi=160)
plt.close()

impacts["systems_impact_risk"] = (
    0.14 * impacts["feedback_risk"]
    + 0.12 * impacts["delay_risk"]
    + 0.16 * impacts["burden_shift_risk"]
    + 0.16 * impacts["capacity_risk"]
    + 0.12 * impacts["incentive_risk"]
    + 0.15 * impacts["scale_uncertainty"]
    - 0.15 * impacts["monitoring_quality"]
)

impacts.sort_values("systems_impact_risk", ascending=True).plot(
    kind="barh",
    x="system_issue",
    y="systems_impact_risk",
    legend=False,
    figsize=(12, 9),
)
plt.title("Systems Impact Risk")
plt.xlabel("Risk")
plt.ylabel("System issue")
plt.tight_layout()
plt.savefig(FIGURES / "systems_impact_risk.png", dpi=160)
plt.close()

time_steps = np.arange(1, 41)

def simulate_system(row):
    state = np.zeros(len(time_steps))
    state[0] = 0.30
    for t in range(1, len(time_steps)):
        gain = (
            0.10 * row["speed"]
            + 0.16 * row["insight_depth"]
            + 0.12 * row["user_validation"]
            + 0.14 * row["evidence_quality"]
            + 0.10 * row["systems_awareness"]
            + 0.08 * row["ethical_review"]
            + 0.12 * row["decision_linkage"]
            + 0.08 * row["learning_memory"]
        )
        shallow_testing_penalty = 0.06 * row["speed"] * (1 - row["insight_depth"])
        decision_drift = 0.05 * (1 - row["decision_linkage"])
        disturbance = 0.06 * (1 - row["systems_awareness"]) * np.sin(t / 4)
        state[t] = state[t - 1] + gain / 5 - shallow_testing_penalty / 5 - decision_drift / 5 + disturbance / 10
        state[t] = np.clip(state[t], 0, 1.8)
    return state

simulation = pd.DataFrame({"time": time_steps})
for _, row in systems.iterrows():
    simulation[row["system_name"]] = simulate_system(row)

plt.figure(figsize=(11, 7))
for col in simulation.columns[1:]:
    plt.plot(simulation["time"], simulation[col], label=col)
plt.xlabel("Time Step")
plt.ylabel("Strategic Learning Performance")
plt.title("Iterative Strategic Learning Through Experimentation")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "iterative_strategic_learning.png", dpi=160)
plt.close()

systems.to_csv(TABLES / "advanced_experimentation_profile_scores.csv", index=False)
assumptions.to_csv(TABLES / "advanced_assumption_priority_scores.csv", index=False)
prototypes.to_csv(TABLES / "advanced_prototype_fit_scores.csv", index=False)
experiments.to_csv(TABLES / "advanced_experiment_quality_scores.csv", index=False)
evidence.to_csv(TABLES / "advanced_evidence_quality_scores.csv", index=False)
impacts.to_csv(TABLES / "advanced_systems_impact_scores.csv", index=False)
simulation.to_csv(TABLES / "iterative_strategic_learning_simulation.csv", index=False)

print("Advanced prototyping analytics complete.")
print(f"Wrote: {FIGURES / 'experimentation_profile_scores.png'}")
print(f"Wrote: {FIGURES / 'superficial_testing_risk.png'}")
print(f"Wrote: {FIGURES / 'assumption_priority_scores.png'}")
print(f"Wrote: {FIGURES / 'prototype_fit_scores.png'}")
print(f"Wrote: {FIGURES / 'experiment_quality_scores.png'}")
print(f"Wrote: {FIGURES / 'evidence_quality_scores.png'}")
print(f"Wrote: {FIGURES / 'systems_impact_risk.png'}")
print(f"Wrote: {FIGURES / 'iterative_strategic_learning.png'}")
