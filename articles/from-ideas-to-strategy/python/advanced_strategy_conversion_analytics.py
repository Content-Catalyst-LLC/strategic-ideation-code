#!/usr/bin/env python3
"""
Optional advanced analytics for From Ideas to Strategy.

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

initiatives = pd.read_csv(RAW / "initiatives.csv")

initiatives["strategy_conversion_score"] = (
    0.14 * initiatives["feasibility"]
    + 0.15 * initiatives["viability"]
    + 0.13 * initiatives["desirability"]
    - 0.11 * initiatives["integration_difficulty"]
    + 0.15 * initiatives["execution_readiness"]
    + 0.13 * initiatives["strategic_fit"]
    + 0.08 * initiatives["evidence_confidence"]
    + 0.08 * initiatives["ethical_resilience"]
    - 0.07 * initiatives["resource_intensity"]
    + 0.10 * initiatives["governance_readiness"]
    + 0.06 * initiatives["learning_value"]
)
initiatives["confidence_adjusted_score"] = initiatives["strategy_conversion_score"] * initiatives["evidence_confidence"]

initiatives.sort_values("strategy_conversion_score", ascending=True).plot(
    kind="barh",
    x="initiative_name",
    y="strategy_conversion_score",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Strategy conversion score")
plt.ylabel("Initiative")
plt.title("Idea-to-Strategy Conversion Scores")
plt.tight_layout()
plt.savefig(FIGURES / "strategy_conversion_scores.png", dpi=160)
plt.close()

initiatives.sort_values("confidence_adjusted_score", ascending=True).plot(
    kind="barh",
    x="initiative_name",
    y="confidence_adjusted_score",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Confidence-adjusted score")
plt.ylabel("Initiative")
plt.title("Confidence-Adjusted Strategy Conversion Scores")
plt.tight_layout()
plt.savefig(FIGURES / "confidence_adjusted_strategy_conversion.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 7))
plt.scatter(
    initiatives["integration_difficulty"],
    initiatives["execution_readiness"],
    s=initiatives["strategic_fit"] * 420,
)
for _, row in initiatives.iterrows():
    plt.annotate(row["initiative_id"], (row["integration_difficulty"], row["execution_readiness"]))
plt.xlabel("Integration difficulty")
plt.ylabel("Execution readiness")
plt.title("Integration Difficulty and Execution Readiness")
plt.tight_layout()
plt.savefig(FIGURES / "integration_execution_map.png", dpi=160)
plt.close()

time_steps = np.arange(1, 31)
simulation = pd.DataFrame({"time": time_steps})
confidence_simulation = pd.DataFrame({"time": time_steps})

for _, row in initiatives.iterrows():
    state = np.zeros(len(time_steps))
    confidence = np.zeros(len(time_steps))
    state[0] = 0.20 + 0.12 * row["desirability"]
    confidence[0] = row["evidence_confidence"] * 0.55

    for t in range(1, len(time_steps)):
        conversion_gain = (
            0.16 * row["feasibility"]
            + 0.18 * row["viability"]
            + 0.16 * row["desirability"]
            + 0.18 * row["execution_readiness"]
            + 0.14 * row["strategic_fit"]
            + 0.10 * row["ethical_resilience"]
            + 0.08 * row["governance_readiness"]
        )
        friction = (
            0.24 * row["integration_difficulty"]
            + 0.10 * (1 - row["evidence_confidence"])
            + 0.08 * row["resource_intensity"]
        )
        learning_gain = (
            0.03 * row["learning_value"]
            + 0.03 * row["evidence_confidence"]
            + 0.02 * row["execution_readiness"]
            - 0.02 * row["integration_difficulty"]
        )
        confidence[t] = np.clip(confidence[t - 1] + learning_gain, 0, 1)
        state[t] = state[t - 1] + conversion_gain / 5 - friction / 4
        state[t] = state[t] * (0.96 + 0.08 * confidence[t])
        state[t] = np.clip(state[t], 0, 1.8)

    simulation[row["initiative_name"]] = state
    confidence_simulation[row["initiative_name"]] = confidence

plt.figure(figsize=(11, 7))
for col in simulation.columns[1:]:
    plt.plot(simulation["time"], simulation[col], label=col)
plt.xlabel("Time step")
plt.ylabel("Strategy conversion strength")
plt.title("Strategic Convergence Under Constraint")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "strategy_conversion_simulation.png", dpi=160)
plt.close()

initiatives.to_csv(TABLES / "advanced_strategy_conversion_scores.csv", index=False)
simulation.to_csv(TABLES / "strategy_conversion_simulation.csv", index=False)
confidence_simulation.to_csv(TABLES / "strategy_conversion_confidence_simulation.csv", index=False)

print("Advanced strategy conversion analytics complete.")
print(f"Wrote: {FIGURES / 'strategy_conversion_scores.png'}")
print(f"Wrote: {FIGURES / 'confidence_adjusted_strategy_conversion.png'}")
print(f"Wrote: {FIGURES / 'integration_execution_map.png'}")
print(f"Wrote: {FIGURES / 'strategy_conversion_simulation.png'}")
