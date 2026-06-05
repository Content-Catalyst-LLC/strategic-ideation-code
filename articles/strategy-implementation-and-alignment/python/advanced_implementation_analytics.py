#!/usr/bin/env python3
"""
Optional advanced analytics for Strategy Implementation and Alignment.
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

orgs = pd.read_csv(RAW / "implementation_profiles.csv")

orgs["implementation_profile_score"] = (
    0.12 * orgs["goal_clarity"]
    + 0.15 * orgs["coordination_quality"]
    + 0.12 * orgs["structural_support"]
    + 0.12 * orgs["cultural_support"]
    + 0.13 * orgs["incentive_alignment"]
    + 0.12 * orgs["resource_sufficiency"]
    + 0.11 * orgs["communication_quality"]
    + 0.10 * orgs["accountability_strength"]
    + 0.10 * orgs["adaptive_execution"]
    + 0.08 * orgs["external_alignment"]
    + 0.05 * orgs["ethical_resilience"]
)
orgs["alignment_drift_risk"] = (
    0.16 * (1 - orgs["coordination_quality"])
    + 0.14 * (1 - orgs["cultural_support"])
    + 0.14 * (1 - orgs["incentive_alignment"])
    + 0.12 * (1 - orgs["communication_quality"])
    + 0.12 * (1 - orgs["adaptive_execution"])
    + 0.10 * (1 - orgs["external_alignment"])
    + 0.10 * (1 - orgs["accountability_strength"])
    + 0.06 * (1 - orgs["ethical_resilience"])
    + 0.06 * (1 - orgs["structural_support"])
)

orgs.sort_values("implementation_profile_score", ascending=True).plot(
    kind="barh",
    x="organization_name",
    y="implementation_profile_score",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Implementation profile score")
plt.ylabel("Organization")
plt.title("Strategy Implementation Profile Scores")
plt.tight_layout()
plt.savefig(FIGURES / "implementation_profile_scores.png", dpi=160)
plt.close()

orgs.sort_values("alignment_drift_risk", ascending=True).plot(
    kind="barh",
    x="organization_name",
    y="alignment_drift_risk",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Alignment drift risk")
plt.ylabel("Organization")
plt.title("Alignment Drift Risk")
plt.tight_layout()
plt.savefig(FIGURES / "alignment_drift_risk.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 7))
plt.scatter(orgs["alignment_drift_risk"], orgs["adaptive_execution"], s=orgs["resource_sufficiency"] * 420)
for _, row in orgs.iterrows():
    plt.annotate(row["organization_id"], (row["alignment_drift_risk"], row["adaptive_execution"]))
plt.xlabel("Alignment drift risk")
plt.ylabel("Adaptive execution")
plt.title("Alignment Drift Risk and Adaptive Execution")
plt.tight_layout()
plt.savefig(FIGURES / "drift_adaptation_map.png", dpi=160)
plt.close()

time_steps = np.arange(1, 41)
implementation = pd.DataFrame({"time": time_steps})

for _, row in orgs.iterrows():
    state = np.zeros(len(time_steps))
    state[0] = 0.55 + 0.15 * row["goal_clarity"]
    for t in range(1, len(time_steps)):
        environmental_friction = 0.04 if t < 20 else 0.13
        adaptive_weight = 0.08 if t < 20 else 0.18
        execution_gain = (
            0.14 * row["coordination_quality"]
            + 0.12 * row["structural_support"]
            + 0.10 * row["cultural_support"]
            + 0.12 * row["incentive_alignment"]
            + 0.10 * row["resource_sufficiency"]
            + 0.10 * row["communication_quality"]
            + 0.10 * row["accountability_strength"]
            + adaptive_weight * row["adaptive_execution"]
        )
        drift_pressure = (
            0.18 * (1 - row["coordination_quality"])
            + 0.16 * (1 - row["incentive_alignment"])
            + 0.16 * (1 - row["communication_quality"])
            + 0.14 * (1 - row["accountability_strength"])
            + 0.18 * environmental_friction
            + 0.18 * (1 - row["adaptive_execution"])
        )
        drift = max(0, min(1, drift_pressure - row["adaptive_execution"] / 5))
        state[t] = max(0, min(1.8, state[t - 1] + execution_gain / 5 - environmental_friction / 4 - drift / 8))
    implementation[row["organization_name"]] = state

plt.figure(figsize=(11, 7))
for col in implementation.columns[1:]:
    plt.plot(implementation["time"], implementation[col], label=col)
plt.xlabel("Time step")
plt.ylabel("Implementation viability")
plt.title("Implementation and Alignment Over Time")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "implementation_alignment_simulation.png", dpi=160)
plt.close()

orgs.to_csv(TABLES / "advanced_implementation_profile_scores.csv", index=False)
implementation.to_csv(TABLES / "implementation_over_time.csv", index=False)

print("Advanced implementation analytics complete.")
print(f"Wrote: {FIGURES / 'implementation_profile_scores.png'}")
print(f"Wrote: {FIGURES / 'alignment_drift_risk.png'}")
print(f"Wrote: {FIGURES / 'drift_adaptation_map.png'}")
print(f"Wrote: {FIGURES / 'implementation_alignment_simulation.png'}")
