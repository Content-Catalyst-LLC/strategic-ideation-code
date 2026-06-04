#!/usr/bin/env python3
"""
Optional advanced analytics for strategy, tactics, and ideation.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- layer alignment bar chart
- initiative portfolio scatterplot
- tactical translation gap table
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
TABLES = ROOT / "outputs" / "tables"
FIGURES = ROOT / "outputs" / "figures"

FIGURES.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)

try:
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError as exc:
    print("Missing optional advanced analytics dependencies.")
    print("Run:")
    print("  python3 -m venv .venv")
    print("  source .venv/bin/activate")
    print("  pip install -r python/requirements-advanced.txt")
    raise SystemExit(1) from exc


contexts = pd.read_csv(RAW / "layer_profile_contexts.csv")
initiatives = pd.read_csv(RAW / "strategic_initiatives.csv")
tactics = pd.read_csv(RAW / "tactical_actions.csv")

context_dimensions = [
    "ideation_quality",
    "strategic_clarity",
    "tactical_alignment",
    "feedback_quality",
    "adaptive_learning",
    "decision_memory",
    "ethical_legitimacy",
]

contexts["alignment_score"] = (
    0.16 * contexts["ideation_quality"]
    + 0.20 * contexts["strategic_clarity"]
    + 0.18 * contexts["tactical_alignment"]
    + 0.14 * contexts["feedback_quality"]
    + 0.14 * contexts["adaptive_learning"]
    + 0.08 * contexts["decision_memory"]
    + 0.10 * contexts["ethical_legitimacy"]
)

contexts.sort_values("alignment_score", ascending=True).plot(
    kind="barh",
    x="context_name",
    y="alignment_score",
    legend=False,
    figsize=(11, 7),
)
plt.title("Layer Alignment Score by Strategic Context")
plt.xlabel("Alignment score")
plt.ylabel("Context")
plt.tight_layout()
plt.savefig(FIGURES / "layer_alignment_scores.png", dpi=160)
plt.close()

initiatives["portfolio_score"] = (
    0.22 * initiatives["strategic_fit"]
    + 0.14 * initiatives["implementation_feasibility"]
    + 0.18 * initiatives["systems_leverage"]
    + 0.14 * initiatives["learning_value"]
    + 0.18 * initiatives["ethical_legitimacy"]
    - 0.08 * initiatives["uncertainty"]
)

plt.figure(figsize=(10, 7))
plt.scatter(
    initiatives["implementation_feasibility"],
    initiatives["systems_leverage"],
    s=initiatives["portfolio_score"] * 450,
    alpha=0.70,
)

for _, row in initiatives.iterrows():
    plt.annotate(row["initiative_id"], (row["implementation_feasibility"], row["systems_leverage"]))

plt.title("Strategic Initiatives: Feasibility vs Systems Leverage")
plt.xlabel("Implementation feasibility")
plt.ylabel("Systems leverage")
plt.tight_layout()
plt.savefig(FIGURES / "initiative_feasibility_vs_leverage.png", dpi=160)
plt.close()

tactics["translation_score"] = (
    0.26 * tactics["alignment_to_strategy"]
    + 0.20 * tactics["execution_readiness"]
    + 0.16 * tactics["resource_fit"]
    + 0.18 * tactics["feedback_capture"]
    + 0.20 * tactics["learning_routing"]
    - 0.12 * tactics["delivery_risk"]
)

tactics.sort_values("translation_score").to_csv(
    TABLES / "advanced_tactical_translation_rankings.csv",
    index=False,
)

print("Advanced analytics complete.")
print(f"Wrote: {FIGURES / 'layer_alignment_scores.png'}")
print(f"Wrote: {FIGURES / 'initiative_feasibility_vs_leverage.png'}")
print(f"Wrote: {TABLES / 'advanced_tactical_translation_rankings.csv'}")
