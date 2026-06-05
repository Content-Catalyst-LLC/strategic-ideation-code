#!/usr/bin/env python3
"""
Optional advanced analytics for Opportunity Recognition and Evaluation.

Requires:
    pip install -r python/requirements-advanced.txt
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

opps = pd.read_csv(RAW / "opportunities.csv")

opps["profile_score"] = (
    0.13 * opps["signal_strength"]
    + 0.14 * opps["capability_alignment"]
    + 0.12 * opps["desirability"]
    + 0.12 * opps["viability"]
    + 0.10 * opps["timing"]
    + 0.12 * opps["learning_value"]
    + 0.11 * opps["option_value"]
    + 0.10 * opps["strategic_fit"]
    + 0.10 * opps["ethical_resilience"]
    - 0.14 * opps["risk"]
)
opps["confidence_adjusted_score"] = opps["profile_score"] * opps["evidence_confidence"]
opps["risk_adjusted_learning"] = opps["learning_value"] + opps["option_value"] - opps["risk"]

opps.sort_values("profile_score", ascending=True).plot(
    kind="barh",
    x="opportunity_name",
    y="profile_score",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Profile score")
plt.ylabel("Opportunity")
plt.title("Opportunity Profile Scores")
plt.tight_layout()
plt.savefig(FIGURES / "opportunity_profile_scores.png", dpi=160)
plt.close()

opps.sort_values("confidence_adjusted_score", ascending=True).plot(
    kind="barh",
    x="opportunity_name",
    y="confidence_adjusted_score",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Confidence-adjusted score")
plt.ylabel("Opportunity")
plt.title("Confidence-Adjusted Opportunity Scores")
plt.tight_layout()
plt.savefig(FIGURES / "confidence_adjusted_opportunity_scores.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 7))
plt.scatter(opps["risk"], opps["learning_value"], s=opps["option_value"] * 420)
for _, row in opps.iterrows():
    plt.annotate(row["opportunity_id"], (row["risk"], row["learning_value"]))
plt.xlabel("Risk")
plt.ylabel("Learning value")
plt.title("Risk, Learning Value, and Option Value")
plt.tight_layout()
plt.savefig(FIGURES / "risk_learning_option_map.png", dpi=160)
plt.close()

time_steps = np.arange(1, 31)
simulation = pd.DataFrame({"time": time_steps})

for _, row in opps.iterrows():
    state = np.zeros(len(time_steps))
    confidence = np.zeros(len(time_steps))
    state[0] = 0.28 + 0.14 * row["signal_strength"]
    confidence[0] = row["evidence_confidence"] * 0.50

    for t in range(1, len(time_steps)):
        learning_gain = (
            0.16 * row["signal_strength"]
            + 0.18 * row["capability_alignment"]
            + 0.16 * row["viability"]
            + 0.16 * row["learning_value"]
            + 0.14 * row["option_value"]
            + 0.12 * row["ethical_resilience"]
        )
        friction = 0.20 * row["risk"]
        confidence[t] = np.clip(confidence[t - 1] + 0.04 * row["learning_value"] - 0.02 * row["risk"], 0, 1)
        state[t] = np.clip((state[t - 1] + learning_gain / 5 - friction / 4) * (0.95 + 0.10 * confidence[t]), 0, 1.8)

    simulation[row["opportunity_name"]] = state

plt.figure(figsize=(11, 7))
for col in simulation.columns[1:]:
    plt.plot(simulation["time"], simulation[col], label=col)
plt.xlabel("Time step")
plt.ylabel("Evaluation strength")
plt.title("Opportunity Evaluation Under Uncertainty")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "opportunity_evaluation_simulation.png", dpi=160)
plt.close()

opps.to_csv(TABLES / "advanced_opportunity_profile_scores.csv", index=False)
simulation.to_csv(TABLES / "opportunity_evaluation_simulation.csv", index=False)

print("Advanced opportunity analytics complete.")
print(f"Wrote: {FIGURES / 'opportunity_profile_scores.png'}")
print(f"Wrote: {FIGURES / 'confidence_adjusted_opportunity_scores.png'}")
print(f"Wrote: {FIGURES / 'risk_learning_option_map.png'}")
print(f"Wrote: {FIGURES / 'opportunity_evaluation_simulation.png'}")
