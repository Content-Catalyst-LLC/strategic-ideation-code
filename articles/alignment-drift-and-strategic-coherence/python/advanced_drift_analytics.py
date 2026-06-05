#!/usr/bin/env python3
"""
Optional advanced analytics for Alignment Drift and Strategic Coherence.
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

contexts = pd.read_csv(RAW / "coherence_contexts.csv")

contexts["strategic_coherence_score"] = (
    0.13 * contexts["purpose_clarity"]
    + 0.12 * contexts["priority_discipline"]
    + 0.11 * contexts["tradeoff_integrity"]
    + 0.12 * contexts["resource_alignment"]
    + 0.12 * contexts["incentive_fit"]
    + 0.10 * contexts["interpretive_consistency"]
    + 0.11 * contexts["governance_strength"]
    + 0.09 * contexts["feedback_quality"]
    + 0.06 * contexts["decision_memory"]
    + 0.07 * contexts["ethical_coherence"]
    + 0.07 * contexts["adaptive_capacity"]
)

contexts["alignment_drift_risk"] = (
    0.13 * (1 - contexts["purpose_clarity"])
    + 0.12 * (1 - contexts["priority_discipline"])
    + 0.11 * (1 - contexts["tradeoff_integrity"])
    + 0.12 * (1 - contexts["resource_alignment"])
    + 0.13 * (1 - contexts["incentive_fit"])
    + 0.10 * (1 - contexts["interpretive_consistency"])
    + 0.11 * (1 - contexts["governance_strength"])
    + 0.08 * (1 - contexts["feedback_quality"])
    + 0.06 * (1 - contexts["decision_memory"])
    + 0.07 * (1 - contexts["ethical_coherence"])
    + 0.07 * (1 - contexts["adaptive_capacity"])
)

contexts.sort_values("strategic_coherence_score", ascending=True).plot(
    kind="barh",
    x="context_name",
    y="strategic_coherence_score",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Strategic coherence score")
plt.ylabel("Context")
plt.title("Strategic Coherence Scores")
plt.tight_layout()
plt.savefig(FIGURES / "strategic_coherence_scores.png", dpi=160)
plt.close()

contexts.sort_values("alignment_drift_risk", ascending=True).plot(
    kind="barh",
    x="context_name",
    y="alignment_drift_risk",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Alignment drift risk")
plt.ylabel("Context")
plt.title("Alignment Drift Risk")
plt.tight_layout()
plt.savefig(FIGURES / "alignment_drift_risk.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 7))
plt.scatter(
    contexts["alignment_drift_risk"],
    contexts["strategic_coherence_score"],
    s=contexts["governance_strength"] * 420,
)
for _, row in contexts.iterrows():
    plt.annotate(row["context_id"], (row["alignment_drift_risk"], row["strategic_coherence_score"]))
plt.xlabel("Alignment drift risk")
plt.ylabel("Strategic coherence")
plt.title("Alignment Drift Risk and Strategic Coherence")
plt.tight_layout()
plt.savefig(FIGURES / "drift_coherence_map.png", dpi=160)
plt.close()

time_steps = np.arange(1, 49)
coherence_df = pd.DataFrame({"time": time_steps})
drift_df = pd.DataFrame({"time": time_steps})

for _, row in contexts.iterrows():
    coherence = np.zeros(len(time_steps))
    drift = np.zeros(len(time_steps))

    coherence[0] = row["strategic_coherence_score"]
    drift[0] = 1 - coherence[0]

    metric_distortion = 1 - row["incentive_fit"]
    overload = 1 - row["priority_discipline"]
    ambiguity = 1 - row["interpretive_consistency"]

    for t in range(1, len(time_steps)):
        pressure = (
            0.20 * metric_distortion
            + 0.18 * overload
            + 0.16 * ambiguity
            + 0.14 * (1 - row["incentive_fit"])
            + 0.12 * (1 - row["resource_alignment"])
            + 0.10 * (1 - row["ethical_coherence"])
            + 0.10 * (1 - row["decision_memory"])
        )
        correction = (
            0.24 * row["governance_strength"]
            + 0.22 * row["feedback_quality"]
            + 0.18 * row["purpose_clarity"]
            + 0.14 * row["interpretive_consistency"]
            + 0.12 * row["decision_memory"]
            + 0.10 * row["ethical_coherence"]
        )
        drift[t] = np.clip(drift[t - 1] + pressure / 20 - correction / 28, 0, 1)
        coherence[t] = np.clip(coherence[t - 1] + correction / 30 - pressure / 24, 0, 1)

    coherence_df[row["context_name"]] = coherence
    drift_df[row["context_name"]] = drift

plt.figure(figsize=(11, 7))
for col in coherence_df.columns[1:]:
    plt.plot(coherence_df["time"], coherence_df[col], label=col)
plt.xlabel("Time step")
plt.ylabel("Strategic coherence")
plt.title("Strategic Coherence Over Time")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "strategic_coherence_over_time.png", dpi=160)
plt.close()

plt.figure(figsize=(11, 7))
for col in drift_df.columns[1:]:
    plt.plot(drift_df["time"], drift_df[col], label=col)
plt.xlabel("Time step")
plt.ylabel("Alignment drift")
plt.title("Alignment Drift Over Time")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "alignment_drift_over_time.png", dpi=160)
plt.close()

contexts.to_csv(TABLES / "advanced_coherence_scores.csv", index=False)
coherence_df.to_csv(TABLES / "strategic_coherence_over_time.csv", index=False)
drift_df.to_csv(TABLES / "alignment_drift_over_time.csv", index=False)

print("Advanced alignment drift analytics complete.")
print(f"Wrote: {FIGURES / 'strategic_coherence_scores.png'}")
print(f"Wrote: {FIGURES / 'alignment_drift_risk.png'}")
print(f"Wrote: {FIGURES / 'drift_coherence_map.png'}")
print(f"Wrote: {FIGURES / 'strategic_coherence_over_time.png'}")
print(f"Wrote: {FIGURES / 'alignment_drift_over_time.png'}")
