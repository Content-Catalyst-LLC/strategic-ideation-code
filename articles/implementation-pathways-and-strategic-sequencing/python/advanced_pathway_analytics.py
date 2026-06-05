#!/usr/bin/env python3
"""
Optional advanced analytics for Implementation Pathways and Strategic Sequencing.
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

pathways = pd.read_csv(RAW / "pathways.csv")

pathways["sequencing_readiness_score"] = (
    0.15 * pathways["capability_readiness"]
    + 0.14 * pathways["evidence_strength"]
    + 0.14 * pathways["governance_readiness"]
    + 0.13 * pathways["legitimacy"]
    - 0.10 * pathways["dependency_load"]
    + 0.09 * pathways["reversibility"]
    - 0.09 * pathways["capacity_demand"]
    + 0.07 * pathways["timing_urgency"]
    + 0.11 * pathways["ethical_resilience"]
    + 0.09 * pathways["feedback_strength"]
    + 0.10 * pathways["strategic_fit"]
)

pathways["premature_commitment_risk"] = (
    0.22 * pathways["dependency_load"]
    + 0.20 * pathways["capacity_demand"]
    + 0.16 * (1 - pathways["evidence_strength"])
    + 0.14 * (1 - pathways["governance_readiness"])
    + 0.12 * (1 - pathways["reversibility"])
    + 0.10 * (1 - pathways["ethical_resilience"])
    + 0.06 * (1 - pathways["feedback_strength"])
)

pathways.sort_values("sequencing_readiness_score", ascending=True).plot(
    kind="barh",
    x="pathway_name",
    y="sequencing_readiness_score",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Sequencing readiness score")
plt.ylabel("Pathway")
plt.title("Implementation Pathway Sequencing Readiness")
plt.tight_layout()
plt.savefig(FIGURES / "pathway_readiness_scores.png", dpi=160)
plt.close()

pathways.sort_values("premature_commitment_risk", ascending=True).plot(
    kind="barh",
    x="pathway_name",
    y="premature_commitment_risk",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Premature commitment risk")
plt.ylabel("Pathway")
plt.title("Premature Commitment Risk")
plt.tight_layout()
plt.savefig(FIGURES / "premature_commitment_risk.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 7))
plt.scatter(
    pathways["dependency_load"],
    pathways["capacity_demand"],
    s=pathways["timing_urgency"] * 420,
)
for _, row in pathways.iterrows():
    plt.annotate(row["pathway_id"], (row["dependency_load"], row["capacity_demand"]))
plt.xlabel("Dependency load")
plt.ylabel("Capacity demand")
plt.title("Dependency Load, Capacity Demand, and Timing Urgency")
plt.tight_layout()
plt.savefig(FIGURES / "dependency_capacity_timing_map.png", dpi=160)
plt.close()

time_steps = np.arange(1, 37)
readiness_df = pd.DataFrame({"time": time_steps})
lockin_df = pd.DataFrame({"time": time_steps})
strain_df = pd.DataFrame({"time": time_steps})

for _, row in pathways.iterrows():
    readiness = np.zeros(len(time_steps))
    lock_in = np.zeros(len(time_steps))
    strain = np.zeros(len(time_steps))

    readiness[0] = 0.25 + 0.25 * row["capability_readiness"]
    lock_in[0] = 0.18 * (1 - row["reversibility"])
    strain[0] = 0.20 * row["capacity_demand"]

    for t in range(1, len(time_steps)):
        learning_gain = (
            0.05 * row["evidence_strength"]
            + 0.04 * row["feedback_strength"]
            + 0.03 * row["governance_readiness"]
            + 0.03 * row["legitimacy"]
        )
        capacity_friction = 0.05 * row["capacity_demand"] + 0.04 * row["dependency_load"]
        timing_pressure = 0.03 * row["timing_urgency"] if t < 14 else 0.01 * row["timing_urgency"]

        readiness[t] = np.clip(readiness[t - 1] + learning_gain + timing_pressure - capacity_friction, 0, 1.5)
        lock_in[t] = np.clip(lock_in[t - 1] + 0.025 * (1 - row["reversibility"]) + 0.015 * row["dependency_load"], 0, 1)
        strain[t] = np.clip(strain[t - 1] + 0.025 * row["capacity_demand"] + 0.015 * row["dependency_load"] - 0.02 * row["capability_readiness"], 0, 1)

    readiness_df[row["pathway_name"]] = readiness
    lockin_df[row["pathway_name"]] = lock_in
    strain_df[row["pathway_name"]] = strain

plt.figure(figsize=(11, 7))
for col in readiness_df.columns[1:]:
    plt.plot(readiness_df["time"], readiness_df[col], label=col)
plt.xlabel("Time step")
plt.ylabel("Pathway readiness")
plt.title("Implementation Pathway Readiness Over Time")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "pathway_readiness_over_time.png", dpi=160)
plt.close()

pathways.to_csv(TABLES / "advanced_pathway_readiness_scores.csv", index=False)
readiness_df.to_csv(TABLES / "pathway_readiness_over_time.csv", index=False)
lockin_df.to_csv(TABLES / "pathway_lockin_over_time.csv", index=False)
strain_df.to_csv(TABLES / "pathway_capacity_strain_over_time.csv", index=False)

print("Advanced pathway analytics complete.")
print(f"Wrote: {FIGURES / 'pathway_readiness_scores.png'}")
print(f"Wrote: {FIGURES / 'premature_commitment_risk.png'}")
print(f"Wrote: {FIGURES / 'dependency_capacity_timing_map.png'}")
print(f"Wrote: {FIGURES / 'pathway_readiness_over_time.png'}")
