#!/usr/bin/env python3
"""
Optional advanced analytics for problem framing and problem definition.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- problem-framing score chart
- symptom-framing risk chart
- boundary quality chart
- causal quality chart
- assumption priority chart
- frame-to-option-space simulation chart
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

frames = pd.read_csv(RAW / "problem_frames.csv")
boundaries = pd.read_csv(RAW / "boundary_audit.csv")
causal = pd.read_csv(RAW / "causal_models.csv")
assumptions = pd.read_csv(RAW / "assumption_audit.csv")

frames["problem_framing_score"] = (
    0.16 * frames["boundary_breadth"]
    + 0.15 * frames["stakeholder_inclusion"]
    + 0.15 * frames["systems_awareness"]
    + 0.16 * frames["causal_depth"]
    + 0.12 * frames["assumption_clarity"]
    + 0.13 * frames["reframing_capacity"]
    + 0.11 * frames["actionability"]
    - 0.10 * frames["institutional_lock_in_risk"]
    - 0.08 * frames["political_convenience_risk"]
)

frames["symptom_framing_risk"] = (
    (1.0 - frames["causal_depth"]) * 0.30
    + (1.0 - frames["systems_awareness"]) * 0.25
    + (0.70 - frames["boundary_breadth"]).clip(lower=0) * 0.20
    + frames["institutional_lock_in_risk"] * 0.15
    + frames["political_convenience_risk"] * 0.10
)

frames.sort_values("problem_framing_score", ascending=True).plot(
    kind="barh",
    x="frame_name",
    y="problem_framing_score",
    legend=False,
    figsize=(12, 9),
)
plt.title("Problem-Framing Quality Scores")
plt.xlabel("Problem-framing score")
plt.ylabel("Frame")
plt.tight_layout()
plt.savefig(FIGURES / "problem_framing_scores.png", dpi=160)
plt.close()

frames.sort_values("symptom_framing_risk", ascending=True).plot(
    kind="barh",
    x="frame_name",
    y="symptom_framing_risk",
    legend=False,
    figsize=(12, 9),
)
plt.title("Symptom-Framing Risk")
plt.xlabel("Risk score")
plt.ylabel("Frame")
plt.tight_layout()
plt.savefig(FIGURES / "symptom_framing_risk.png", dpi=160)
plt.close()

boundaries["boundary_quality_score"] = (
    0.16 * boundaries["stakeholder_visibility"]
    + 0.15 * boundaries["downstream_effect_visibility"]
    + 0.14 * boundaries["externality_visibility"]
    + 0.14 * boundaries["implementation_visibility"]
    + 0.13 * boundaries["time_horizon_quality"]
    + 0.14 * boundaries["hidden_dependency_visibility"]
    - 0.12 * boundaries["boundary_risk"]
    - 0.08 * boundaries["revision_need"]
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

causal["causal_quality_score"] = (
    0.18 * causal["causal_depth"]
    + 0.16 * causal["mechanism_clarity"]
    + 0.16 * causal["feedback_awareness"]
    + 0.14 * causal["incentive_awareness"]
    + 0.12 * causal["delay_awareness"]
    + 0.12 * causal["evidence_strength"]
    + 0.12 * causal["alternative_cause_review"]
    - 0.14 * causal["linear_oversimplification_risk"]
)

causal.sort_values("causal_quality_score", ascending=True).plot(
    kind="barh",
    x="causal_story",
    y="causal_quality_score",
    legend=False,
    figsize=(12, 9),
)
plt.title("Causal-Depth Quality Scores")
plt.xlabel("Causal quality score")
plt.ylabel("Causal story")
plt.tight_layout()
plt.savefig(FIGURES / "causal_quality_scores.png", dpi=160)
plt.close()

assumptions["assumption_priority_score"] = (
    0.18 * assumptions["importance"]
    + 0.16 * assumptions["uncertainty"]
    + 0.16 * assumptions["stakeholder_sensitivity"]
    + 0.14 * assumptions["assumption_risk"]
    - 0.12 * assumptions["visibility"]
    - 0.10 * assumptions["testability"]
    - 0.10 * assumptions["disconfirmation_quality"]
    - 0.08 * assumptions["reversibility"]
)

assumptions.sort_values("assumption_priority_score", ascending=True).plot(
    kind="barh",
    x="assumption_id",
    y="assumption_priority_score",
    legend=False,
    figsize=(10, 7),
)
plt.title("Priority Assumptions to Test")
plt.xlabel("Priority score")
plt.ylabel("Assumption")
plt.tight_layout()
plt.savefig(FIGURES / "assumption_priority_scores.png", dpi=160)
plt.close()

# Frame-to-option-space simulation.
time_steps = np.arange(1, 31)

def simulate_frame(boundary, systems, stakeholders, causal_depth, reframing, lock_in_risk, initial_state=0.30):
    state = np.zeros(len(time_steps))
    state[0] = initial_state

    for t in range(1, len(time_steps)):
        gain = (
            0.14 * boundary
            + 0.16 * systems
            + 0.14 * stakeholders
            + 0.16 * causal_depth
            + 0.18 * reframing
        )
        lock_in_drag = 0.10 * lock_in_risk
        learning_bonus = 0.01 * systems * reframing * np.log1p(t)
        state[t] = state[t - 1] + gain / 5 - lock_in_drag / 5 + learning_bonus
        state[t] = np.clip(state[t], 0, 1.8)

    return state

simulation = pd.DataFrame({"time": time_steps})

for _, row in frames.iterrows():
    if row["frame_id"] in {"F001", "F002", "F003", "F005", "F010"}:
        simulation[row["frame_name"]] = simulate_frame(
            boundary=row["boundary_breadth"],
            systems=row["systems_awareness"],
            stakeholders=row["stakeholder_inclusion"],
            causal_depth=row["causal_depth"],
            reframing=row["reframing_capacity"],
            lock_in_risk=row["institutional_lock_in_risk"],
        )

plt.figure(figsize=(11, 7))
for col in simulation.columns[1:]:
    plt.plot(simulation["time"], simulation[col], label=col)
plt.xlabel("Framing Cycle")
plt.ylabel("Option-Space Quality")
plt.title("Framing Shifts and Idea-Space Expansion")
plt.legend()
plt.tight_layout()
plt.savefig(FIGURES / "frame_option_space_simulation.png", dpi=160)
plt.close()

frames.to_csv(TABLES / "advanced_problem_framing_scores.csv", index=False)
boundaries.to_csv(TABLES / "advanced_boundary_quality_scores.csv", index=False)
causal.to_csv(TABLES / "advanced_causal_quality_scores.csv", index=False)
assumptions.to_csv(TABLES / "advanced_assumption_priority_scores.csv", index=False)
simulation.to_csv(TABLES / "advanced_frame_option_space_simulation.csv", index=False)

print("Advanced framing analytics complete.")
print(f"Wrote: {FIGURES / 'problem_framing_scores.png'}")
print(f"Wrote: {FIGURES / 'symptom_framing_risk.png'}")
print(f"Wrote: {FIGURES / 'boundary_quality_scores.png'}")
print(f"Wrote: {FIGURES / 'causal_quality_scores.png'}")
print(f"Wrote: {FIGURES / 'assumption_priority_scores.png'}")
print(f"Wrote: {FIGURES / 'frame_option_space_simulation.png'}")
