#!/usr/bin/env python3
"""
Optional advanced analytics for Measuring Strategic Effectiveness.
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

strategies = pd.read_csv(RAW / "strategies.csv")

strategies["strategic_effectiveness_score"] = (
    0.18 * strategies["performance"]
    + 0.14 * strategies["alignment"]
    + 0.15 * strategies["resilience"]
    + 0.15 * strategies["adaptability"]
    + 0.13 * strategies["impact"]
    + 0.10 * strategies["learning_value"]
    + 0.06 * strategies["evidence_confidence"]
    + 0.06 * strategies["ethical_resilience"]
    - 0.05 * strategies["measurement_burden"]
    + 0.08 * strategies["strategic_fit"]
)
strategies["confidence_adjusted_effectiveness"] = strategies["strategic_effectiveness_score"] * strategies["evidence_confidence"]

strategies.sort_values("strategic_effectiveness_score", ascending=True).plot(
    kind="barh",
    x="strategy_name",
    y="strategic_effectiveness_score",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Strategic effectiveness score")
plt.ylabel("Strategy")
plt.title("Strategic Effectiveness Scores")
plt.tight_layout()
plt.savefig(FIGURES / "strategic_effectiveness_scores.png", dpi=160)
plt.close()

strategies.sort_values("confidence_adjusted_effectiveness", ascending=True).plot(
    kind="barh",
    x="strategy_name",
    y="confidence_adjusted_effectiveness",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Confidence-adjusted effectiveness")
plt.ylabel("Strategy")
plt.title("Confidence-Adjusted Strategic Effectiveness")
plt.tight_layout()
plt.savefig(FIGURES / "confidence_adjusted_effectiveness.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 7))
plt.scatter(strategies["resilience"], strategies["adaptability"], s=strategies["performance"] * 420)
for _, row in strategies.iterrows():
    plt.annotate(row["strategy_id"], (row["resilience"], row["adaptability"]))
plt.xlabel("Resilience")
plt.ylabel("Adaptability")
plt.title("Resilience, Adaptability, and Performance")
plt.tight_layout()
plt.savefig(FIGURES / "resilience_adaptability_performance_map.png", dpi=160)
plt.close()

time_steps = np.arange(1, 41)
simulation = pd.DataFrame({"time": time_steps})
confidence = pd.DataFrame({"time": time_steps})

for _, row in strategies.iterrows():
    state = np.zeros(len(time_steps))
    conf = np.zeros(len(time_steps))
    state[0] = 0.80 + 0.20 * row["performance"]
    conf[0] = row["evidence_confidence"]

    for t in range(1, len(time_steps)):
        if t < 20:
            shock = 0.03
            gain = (
                0.16 * row["performance"]
                + 0.12 * row["alignment"]
                + 0.08 * row["resilience"]
                + 0.08 * row["adaptability"]
                + 0.10 * row["impact"]
                + 0.08 * row["learning_value"]
            )
        else:
            shock = 0.14
            gain = (
                0.08 * row["performance"]
                + 0.10 * row["alignment"]
                + 0.18 * row["resilience"]
                + 0.18 * row["adaptability"]
                + 0.12 * row["impact"]
                + 0.12 * row["learning_value"]
            )

        conf[t] = np.clip(conf[t - 1] + 0.03 * row["learning_value"] + 0.02 * row["adaptability"] - 0.02 * shock, 0, 1)
        state[t] = state[t - 1] + gain / 4 - shock / 5
        state[t] = state[t] * (0.97 + 0.06 * conf[t])
        state[t] = np.clip(state[t], 0, 1.8)

    simulation[row["strategy_name"]] = state
    confidence[row["strategy_name"]] = conf

plt.figure(figsize=(11, 7))
for col in simulation.columns[1:]:
    plt.plot(simulation["time"], simulation[col], label=col)
plt.xlabel("Time step")
plt.ylabel("Strategic effectiveness")
plt.title("Strategic Effectiveness Over Time")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "strategic_effectiveness_simulation.png", dpi=160)
plt.close()

strategies.to_csv(TABLES / "advanced_strategic_effectiveness_scores.csv", index=False)
simulation.to_csv(TABLES / "strategic_effectiveness_over_time.csv", index=False)
confidence.to_csv(TABLES / "strategic_effectiveness_confidence_over_time.csv", index=False)

print("Advanced strategic effectiveness analytics complete.")
print(f"Wrote: {FIGURES / 'strategic_effectiveness_scores.png'}")
print(f"Wrote: {FIGURES / 'confidence_adjusted_effectiveness.png'}")
print(f"Wrote: {FIGURES / 'resilience_adaptability_performance_map.png'}")
print(f"Wrote: {FIGURES / 'strategic_effectiveness_simulation.png'}")
