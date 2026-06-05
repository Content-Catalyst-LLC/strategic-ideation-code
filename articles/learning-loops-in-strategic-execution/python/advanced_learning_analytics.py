#!/usr/bin/env python3
"""
Optional advanced analytics for Learning Loops in Strategic Execution.
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

contexts = pd.read_csv(RAW / "learning_contexts.csv")

contexts["learning_loop_strength"] = (
    0.12 * contexts["feedback_quality"]
    + 0.12 * contexts["assumption_review"]
    + 0.11 * contexts["interpretation_discipline"]
    + 0.13 * contexts["decision_authority"]
    + 0.13 * contexts["learning_closure"]
    + 0.10 * contexts["decision_memory"]
    + 0.08 * contexts["psychological_safety"]
    + 0.08 * contexts["knowledge_scaling"]
    + 0.08 * contexts["ethical_learning"]
    + 0.07 * contexts["strategic_coherence"]
    + 0.08 * contexts["adaptive_capacity"]
)

contexts["learning_failure_risk"] = (
    0.11 * (1 - contexts["feedback_quality"])
    + 0.12 * (1 - contexts["assumption_review"])
    + 0.10 * (1 - contexts["interpretation_discipline"])
    + 0.14 * (1 - contexts["decision_authority"])
    + 0.14 * (1 - contexts["learning_closure"])
    + 0.11 * (1 - contexts["decision_memory"])
    + 0.08 * (1 - contexts["psychological_safety"])
    + 0.08 * (1 - contexts["knowledge_scaling"])
    + 0.08 * (1 - contexts["ethical_learning"])
    + 0.07 * (1 - contexts["strategic_coherence"])
    + 0.07 * (1 - contexts["adaptive_capacity"])
)

contexts.sort_values("learning_loop_strength", ascending=True).plot(
    kind="barh",
    x="context_name",
    y="learning_loop_strength",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Learning loop strength")
plt.ylabel("Context")
plt.title("Strategic Learning Loop Strength")
plt.tight_layout()
plt.savefig(FIGURES / "learning_loop_strength_scores.png", dpi=160)
plt.close()

contexts.sort_values("learning_failure_risk", ascending=True).plot(
    kind="barh",
    x="context_name",
    y="learning_failure_risk",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Learning failure risk")
plt.ylabel("Context")
plt.title("Learning Failure Risk")
plt.tight_layout()
plt.savefig(FIGURES / "learning_failure_risk.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 7))
plt.scatter(
    contexts["learning_failure_risk"],
    contexts["learning_loop_strength"],
    s=contexts["decision_authority"] * 420,
)
for _, row in contexts.iterrows():
    plt.annotate(row["context_id"], (row["learning_failure_risk"], row["learning_loop_strength"]))
plt.xlabel("Learning failure risk")
plt.ylabel("Learning loop strength")
plt.title("Learning Failure Risk and Learning Loop Strength")
plt.tight_layout()
plt.savefig(FIGURES / "learning_risk_strength_map.png", dpi=160)
plt.close()

time_steps = np.arange(1, 49)
strength_df = pd.DataFrame({"time": time_steps})
debt_df = pd.DataFrame({"time": time_steps})

for _, row in contexts.iterrows():
    strength = np.zeros(len(time_steps))
    debt = np.zeros(len(time_steps))

    strength[0] = row["learning_loop_strength"]
    debt[0] = 1 - strength[0]

    distortion = 1 - row["interpretation_discipline"]
    overload = 1 - row["strategic_coherence"]

    for t in range(1, len(time_steps)):
        learning_gain = (
            0.18 * row["feedback_quality"]
            + 0.16 * row["assumption_review"]
            + 0.15 * row["interpretation_discipline"]
            + 0.17 * row["decision_authority"]
            + 0.15 * row["learning_closure"]
            + 0.09 * row["decision_memory"]
            + 0.05 * row["psychological_safety"]
            + 0.05 * row["ethical_learning"]
        )

        learning_loss = (
            0.22 * distortion
            + 0.18 * overload
            + 0.14 * (1 - row["decision_authority"])
            + 0.12 * (1 - row["learning_closure"])
            + 0.10 * (1 - row["decision_memory"])
            + 0.09 * (1 - row["psychological_safety"])
            + 0.08 * (1 - row["knowledge_scaling"])
            + 0.07 * (1 - row["ethical_learning"])
        )

        strength[t] = np.clip(strength[t - 1] + learning_gain / 28 - learning_loss / 24, 0, 1)
        debt[t] = np.clip(debt[t - 1] + learning_loss / 22 - learning_gain / 30, 0, 1)

    strength_df[row["context_name"]] = strength
    debt_df[row["context_name"]] = debt

plt.figure(figsize=(11, 7))
for col in strength_df.columns[1:]:
    plt.plot(strength_df["time"], strength_df[col], label=col)
plt.xlabel("Time step")
plt.ylabel("Learning loop strength")
plt.title("Strategic Learning Loop Strength Over Time")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "learning_loop_strength_over_time.png", dpi=160)
plt.close()

plt.figure(figsize=(11, 7))
for col in debt_df.columns[1:]:
    plt.plot(debt_df["time"], debt_df[col], label=col)
plt.xlabel("Time step")
plt.ylabel("Learning debt")
plt.title("Learning Debt Over Time")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "learning_debt_over_time.png", dpi=160)
plt.close()

contexts.to_csv(TABLES / "advanced_learning_loop_scores.csv", index=False)
strength_df.to_csv(TABLES / "learning_loop_strength_over_time.csv", index=False)
debt_df.to_csv(TABLES / "learning_debt_over_time.csv", index=False)

print("Advanced learning loop analytics complete.")
print(f"Wrote: {FIGURES / 'learning_loop_strength_scores.png'}")
print(f"Wrote: {FIGURES / 'learning_failure_risk.png'}")
print(f"Wrote: {FIGURES / 'learning_risk_strength_map.png'}")
print(f"Wrote: {FIGURES / 'learning_loop_strength_over_time.png'}")
print(f"Wrote: {FIGURES / 'learning_debt_over_time.png'}")
