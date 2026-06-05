#!/usr/bin/env python3
"""
Optional advanced analytics for Prototype Evidence and Strategic Learning.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- prototype learning quality chart
- validation-theater risk chart
- assumption priority gap chart
- evidence quality chart
- behavioral concern chart
- systems impact risk chart
- ethical governance risk chart
- strategic learning simulation
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

systems = pd.read_csv(RAW / "prototype_systems.csv")
assumptions = pd.read_csv(RAW / "assumptions.csv")
evidence = pd.read_csv(RAW / "evidence_records.csv")
behavior = pd.read_csv(RAW / "behavioral_observations.csv")
effects = pd.read_csv(RAW / "systems_effects.csv")
ethics = pd.read_csv(RAW / "ethical_reviews.csv")

systems["prototype_learning_quality"] = (
    0.13 * systems["assumption_clarity"]
    + 0.13 * systems["learning_target_fit"]
    + 0.15 * systems["evidence_quality"]
    + 0.13 * systems["behavioral_grounding"]
    + 0.11 * systems["context_realism"]
    + 0.11 * systems["systems_awareness"]
    + 0.11 * systems["decision_linkage"]
    + 0.07 * systems["ethical_review"]
    + 0.06 * systems["learning_memory"]
)

systems["validation_theater_risk"] = (
    0.17 * (1 - systems["assumption_clarity"])
    + 0.16 * (1 - systems["evidence_quality"])
    + 0.14 * (1 - systems["behavioral_grounding"])
    + 0.13 * (1 - systems["decision_linkage"])
    + 0.12 * (1 - systems["learning_memory"])
    + 0.11 * (1 - systems["systems_awareness"])
    + 0.09 * (1 - systems["ethical_review"])
    + 0.08 * (1 - systems["context_realism"])
)

systems.sort_values("prototype_learning_quality", ascending=True).plot(
    kind="barh",
    x="system_name",
    y="prototype_learning_quality",
    legend=False,
    figsize=(12, 8),
)
plt.title("Prototype Learning Quality")
plt.xlabel("Quality score")
plt.ylabel("System")
plt.tight_layout()
plt.savefig(FIGURES / "prototype_learning_quality_scores.png", dpi=160)
plt.close()

systems.sort_values("validation_theater_risk", ascending=True).plot(
    kind="barh",
    x="system_name",
    y="validation_theater_risk",
    legend=False,
    figsize=(12, 8),
)
plt.title("Validation Theater Risk")
plt.xlabel("Risk")
plt.ylabel("System")
plt.tight_layout()
plt.savefig(FIGURES / "validation_theater_risk.png", dpi=160)
plt.close()

assumptions["criticality"] = 0.50 * assumptions["uncertainty"] + 0.50 * assumptions["consequence"]
assumptions["test_design_score"] = (
    0.22 * assumptions["explicitness"]
    + 0.24 * assumptions["testability"]
    + 0.22 * assumptions["learning_target_clarity"]
    + 0.17 * assumptions["evidence_standard_defined"]
    + 0.15 * assumptions["decision_rule_defined"]
)
assumptions["strategic_priority_gap"] = assumptions["criticality"] * (1 - assumptions["test_design_score"])

assumptions.sort_values("strategic_priority_gap", ascending=True).plot(
    kind="barh",
    x="assumption_id",
    y="strategic_priority_gap",
    legend=False,
    figsize=(12, 8),
)
plt.title("Critical Assumption Priority Gaps")
plt.xlabel("Criticality × test-design weakness")
plt.ylabel("Assumption")
plt.tight_layout()
plt.savefig(FIGURES / "assumption_priority_gaps.png", dpi=160)
plt.close()

evidence["evidence_quality_score"] = (
    0.14 * evidence["relevance"]
    + 0.15 * evidence["validity"]
    + 0.13 * evidence["context_realism"]
    + 0.14 * evidence["behavioral_richness"]
    + 0.12 * evidence["sample_fit"]
    + 0.13 * evidence["interpretability"]
    + 0.11 * evidence["decision_usefulness"]
    + 0.08 * evidence["limitation_clarity"]
)

evidence.sort_values("evidence_quality_score", ascending=True).plot(
    kind="barh",
    x="prototype_type",
    y="evidence_quality_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Evidence Quality Scores")
plt.xlabel("Evidence quality")
plt.ylabel("Prototype type")
plt.tight_layout()
plt.savefig(FIGURES / "evidence_quality_scores.png", dpi=160)
plt.close()

behavior["behavioral_concern_score"] = (
    0.18 * behavior["hesitation_signal"]
    + 0.18 * behavior["workaround_signal"]
    + 0.20 * behavior["abandonment_signal"]
    + 0.18 * behavior["burden_signal"]
    + 0.14 * (1 - behavior["preference_behavior_alignment"])
    + 0.12 * (1 - behavior["commitment_signal"])
)

behavior.sort_values("behavioral_concern_score", ascending=True).plot(
    kind="barh",
    x="observation_id",
    y="behavioral_concern_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Behavioral Concern Scores")
plt.xlabel("Concern")
plt.ylabel("Observation")
plt.tight_layout()
plt.savefig(FIGURES / "behavioral_concern_scores.png", dpi=160)
plt.close()

effects["systems_impact_risk"] = (
    0.14 * effects["feedback_loop_risk"]
    + 0.12 * effects["delay_risk"]
    + 0.16 * effects["burden_shift_risk"]
    + 0.16 * effects["capacity_risk"]
    + 0.12 * effects["incentive_risk"]
    + 0.14 * effects["scale_uncertainty"]
    - 0.16 * effects["monitoring_quality"]
)

effects.sort_values("systems_impact_risk", ascending=True).plot(
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

ethics["ethical_governance_score"] = (
    0.13 * ethics["consent_quality"]
    + 0.13 * ethics["privacy_protection"]
    + 0.14 * ethics["accessibility_review"]
    + 0.13 * ethics["burden_review"]
    + 0.13 * ethics["representation_quality"]
    + 0.10 * ethics["redress_path"]
    + 0.12 * ethics["expectation_management"]
    + 0.12 * ethics["accountability_quality"]
)
ethics["ethical_governance_risk"] = 1 - ethics["ethical_governance_score"]

ethics.sort_values("ethical_governance_risk", ascending=True).plot(
    kind="barh",
    x="ethical_issue",
    y="ethical_governance_risk",
    legend=False,
    figsize=(12, 9),
)
plt.title("Ethical Prototype Governance Risk")
plt.xlabel("Risk")
plt.ylabel("Ethical issue")
plt.tight_layout()
plt.savefig(FIGURES / "ethical_prototype_governance_risk.png", dpi=160)
plt.close()

time_steps = np.arange(1, 41)

def simulate_system(row):
    learning = np.zeros(len(time_steps))
    uncertainty = np.zeros(len(time_steps))
    learning[0] = 0.30
    uncertainty[0] = 0.70

    for t in range(1, len(time_steps)):
        gain = (
            0.12 * row["assumption_clarity"]
            + 0.12 * row["learning_target_fit"]
            + 0.16 * row["evidence_quality"]
            + 0.12 * row["behavioral_grounding"]
            + 0.10 * row["context_realism"]
            + 0.10 * row["systems_awareness"]
            + 0.12 * row["decision_linkage"]
            + 0.07 * row["ethical_review"]
            + 0.07 * row["learning_memory"]
        )
        theater_penalty = (
            0.07 * (1 - row["assumption_clarity"])
            + 0.07 * (1 - row["evidence_quality"])
            + 0.06 * (1 - row["behavioral_grounding"])
            + 0.06 * (1 - row["decision_linkage"])
        )
        overgeneralization_penalty = (
            0.05 * (1 - row["context_realism"])
            + 0.05 * (1 - row["systems_awareness"])
            + 0.04 * (1 - row["learning_memory"])
        )
        ethics_penalty = 0.04 * (1 - row["ethical_review"])
        disturbance = 0.06 * (1 - row["context_realism"]) * np.sin(t / 4)

        learning[t] = learning[t - 1] + gain / 5 - theater_penalty / 5 - overgeneralization_penalty / 5 - ethics_penalty / 5 + disturbance / 10
        learning[t] = np.clip(learning[t], 0, 1.8)
        uncertainty[t] = max(0.0, 1.0 - min(1.0, learning[t]))

    return learning, uncertainty

simulation = pd.DataFrame({"time": time_steps})
uncertainty = pd.DataFrame({"time": time_steps})

for _, row in systems.iterrows():
    learning, uncertainty_series = simulate_system(row)
    simulation[row["system_name"]] = learning
    uncertainty[row["system_name"]] = uncertainty_series

plt.figure(figsize=(11, 7))
for col in simulation.columns[1:]:
    plt.plot(simulation["time"], simulation[col], label=col)
plt.xlabel("Prototype Cycle")
plt.ylabel("Strategic Learning")
plt.title("Strategic Learning From Prototype Evidence")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "strategic_learning_simulation.png", dpi=160)
plt.close()

systems.to_csv(TABLES / "advanced_prototype_system_profile_scores.csv", index=False)
assumptions.to_csv(TABLES / "advanced_assumption_evidence_scores.csv", index=False)
evidence.to_csv(TABLES / "advanced_evidence_quality_scores.csv", index=False)
behavior.to_csv(TABLES / "advanced_behavioral_observation_scores.csv", index=False)
effects.to_csv(TABLES / "advanced_systems_impact_scores.csv", index=False)
ethics.to_csv(TABLES / "advanced_ethical_prototype_governance.csv", index=False)
simulation.to_csv(TABLES / "strategic_learning_simulation.csv", index=False)
uncertainty.to_csv(TABLES / "uncertainty_reduction_simulation.csv", index=False)

print("Advanced prototype evidence analytics complete.")
print(f"Wrote: {FIGURES / 'prototype_learning_quality_scores.png'}")
print(f"Wrote: {FIGURES / 'validation_theater_risk.png'}")
print(f"Wrote: {FIGURES / 'assumption_priority_gaps.png'}")
print(f"Wrote: {FIGURES / 'evidence_quality_scores.png'}")
print(f"Wrote: {FIGURES / 'behavioral_concern_scores.png'}")
print(f"Wrote: {FIGURES / 'systems_impact_risk.png'}")
print(f"Wrote: {FIGURES / 'ethical_prototype_governance_risk.png'}")
print(f"Wrote: {FIGURES / 'strategic_learning_simulation.png'}")
