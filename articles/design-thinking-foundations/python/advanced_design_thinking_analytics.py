#!/usr/bin/env python3
"""
Optional advanced analytics for Design Thinking Foundations.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- design capability chart
- superficiality risk chart
- reframing quality chart
- prototype learning chart
- systems design risk chart
- ethical design risk chart
- iterative learning simulation
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

contexts = pd.read_csv(RAW / "design_contexts.csv")
frames = pd.read_csv(RAW / "problem_frames.csv")
prototypes = pd.read_csv(RAW / "prototypes.csv")
systems = pd.read_csv(RAW / "systems_design.csv")
ethics = pd.read_csv(RAW / "ethical_design.csv")

contexts["design_capability_score"] = (
    0.12 * contexts["empathy_depth"]
    + 0.13 * contexts["reframing_capacity"]
    + 0.10 * contexts["divergence_quality"]
    + 0.10 * contexts["convergence_quality"]
    + 0.12 * contexts["prototyping_strength"]
    + 0.12 * contexts["testing_quality"]
    + 0.11 * contexts["systems_awareness"]
    + 0.10 * contexts["ethical_review"]
    + 0.10 * contexts["decision_linkage"]
    + 0.06 * contexts["adaptability"]
    + 0.04 * contexts["institutional_memory"]
)

contexts["superficiality_risk"] = (
    0.18 * (1 - contexts["empathy_depth"])
    + 0.14 * (1 - contexts["reframing_capacity"])
    + 0.12 * (1 - contexts["testing_quality"])
    + 0.12 * (1 - contexts["systems_awareness"])
    + 0.12 * (1 - contexts["ethical_review"])
    + 0.16 * (1 - contexts["decision_linkage"])
    + 0.10 * (1 - contexts["institutional_memory"])
    + 0.06 * (1 - contexts["adaptability"])
)

contexts.sort_values("design_capability_score", ascending=True).plot(
    kind="barh",
    x="context_name",
    y="design_capability_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Design Thinking Capability Scores")
plt.xlabel("Capability")
plt.ylabel("Context")
plt.tight_layout()
plt.savefig(FIGURES / "design_capability_scores.png", dpi=160)
plt.close()

contexts.sort_values("superficiality_risk", ascending=True).plot(
    kind="barh",
    x="context_name",
    y="superficiality_risk",
    legend=False,
    figsize=(12, 8),
)
plt.title("Risk of Superficial Design Thinking")
plt.xlabel("Risk")
plt.ylabel("Context")
plt.tight_layout()
plt.savefig(FIGURES / "superficiality_risk.png", dpi=160)
plt.close()

frames["reframing_quality_score"] = (
    0.14 * frames["inquiry_influence"]
    + 0.12 * frames["boundary_quality"]
    + 0.13 * frames["stakeholder_evidence"]
    + 0.14 * frames["causal_depth"]
    + 0.13 * frames["systems_context"]
    + 0.12 * frames["ethical_awareness"]
    + 0.10 * frames["decision_usefulness"]
    + 0.12 * frames["reframing_maturity"]
)

frames.sort_values("reframing_quality_score", ascending=True).plot(
    kind="barh",
    x="frame_id",
    y="reframing_quality_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Problem Reframing Quality")
plt.xlabel("Quality")
plt.ylabel("Frame")
plt.tight_layout()
plt.savefig(FIGURES / "problem_reframing_quality.png", dpi=160)
plt.close()

prototypes["prototype_learning_score"] = (
    0.08 * prototypes["prototype_fidelity"]
    + 0.16 * prototypes["learning_potential"]
    + 0.10 * prototypes["test_speed"]
    + 0.12 * prototypes["stakeholder_inclusion"]
    + 0.12 * prototypes["realism"]
    + 0.12 * prototypes["system_signal_quality"]
    + 0.11 * prototypes["ethical_safety"]
    + 0.08 * prototypes["cost_efficiency"]
    + 0.11 * prototypes["decision_usefulness"]
)

prototypes.sort_values("prototype_learning_score", ascending=True).plot(
    kind="barh",
    x="prototype_name",
    y="prototype_learning_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Prototype Learning Scores")
plt.xlabel("Learning value")
plt.ylabel("Prototype")
plt.tight_layout()
plt.savefig(FIGURES / "prototype_learning_scores.png", dpi=160)
plt.close()

systems["systems_design_risk"] = (
    0.14 * systems["feedback_risk"]
    + 0.11 * systems["delay_risk"]
    + 0.16 * systems["burden_shift_risk"]
    + 0.14 * systems["incentive_misalignment"]
    + 0.12 * systems["metric_gaming_risk"]
    + 0.12 * systems["context_dependency"]
    + 0.11 * systems["leverage_relevance"]
    - 0.10 * systems["monitoring_quality"]
)

systems.sort_values("systems_design_risk", ascending=True).plot(
    kind="barh",
    x="design_issue",
    y="systems_design_risk",
    legend=False,
    figsize=(12, 9),
)
plt.title("Systems Design Risk")
plt.xlabel("Risk")
plt.ylabel("Design issue")
plt.tight_layout()
plt.savefig(FIGURES / "systems_design_risk.png", dpi=160)
plt.close()

ethics["ethical_design_score"] = (
    0.13 * ethics["participation_quality"]
    + 0.14 * ethics["power_awareness"]
    + 0.13 * ethics["burden_visibility"]
    + 0.11 * ethics["consent_quality"]
    + 0.12 * ethics["representation_quality"]
    + 0.12 * ethics["redress_quality"]
    + 0.13 * ethics["decision_traceability"]
    + 0.12 * ethics["harm_monitoring"]
)
ethics["ethical_design_risk"] = 1 - ethics["ethical_design_score"]

ethics.sort_values("ethical_design_risk", ascending=True).plot(
    kind="barh",
    x="ethical_issue",
    y="ethical_design_risk",
    legend=False,
    figsize=(12, 9),
)
plt.title("Ethical Design Risk")
plt.xlabel("Risk")
plt.ylabel("Ethical issue")
plt.tight_layout()
plt.savefig(FIGURES / "ethical_design_risk.png", dpi=160)
plt.close()

time_steps = np.arange(1, 31)

def simulate_context(row):
    state = np.zeros(len(time_steps))
    state[0] = 0.35
    for t in range(1, len(time_steps)):
        gain = (
            0.14 * row["empathy_depth"]
            + 0.16 * row["reframing_capacity"]
            + 0.18 * row["prototyping_strength"]
            + 0.14 * row["systems_awareness"]
            + 0.18 * row["decision_linkage"]
            + 0.10 * row["institutional_memory"]
        )
        decay = 0.04 * (1 - row["decision_linkage"])
        state[t] = np.clip(state[t - 1] + gain / 6 - decay, 0, 1.8)
    return state

simulation = pd.DataFrame({"time": time_steps})
for _, row in contexts.iterrows():
    simulation[row["context_name"]] = simulate_context(row)

plt.figure(figsize=(11, 7))
for col in simulation.columns[1:]:
    plt.plot(simulation["time"], simulation[col], label=col)
plt.xlabel("Time Step")
plt.ylabel("Strategic Learning Quality")
plt.title("Iterative Design Learning Over Time")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "iterative_design_learning_simulation.png", dpi=160)
plt.close()

contexts.to_csv(TABLES / "advanced_design_capability_scores.csv", index=False)
frames.to_csv(TABLES / "advanced_reframing_scores.csv", index=False)
prototypes.to_csv(TABLES / "advanced_prototype_learning_scores.csv", index=False)
systems.to_csv(TABLES / "advanced_systems_design_scores.csv", index=False)
ethics.to_csv(TABLES / "advanced_ethical_design_scores.csv", index=False)
simulation.to_csv(TABLES / "iterative_design_learning_simulation.csv", index=False)

print("Advanced design thinking analytics complete.")
print(f"Wrote: {FIGURES / 'design_capability_scores.png'}")
print(f"Wrote: {FIGURES / 'superficiality_risk.png'}")
print(f"Wrote: {FIGURES / 'problem_reframing_quality.png'}")
print(f"Wrote: {FIGURES / 'prototype_learning_scores.png'}")
print(f"Wrote: {FIGURES / 'systems_design_risk.png'}")
print(f"Wrote: {FIGURES / 'ethical_design_risk.png'}")
print(f"Wrote: {FIGURES / 'iterative_design_learning_simulation.png'}")
