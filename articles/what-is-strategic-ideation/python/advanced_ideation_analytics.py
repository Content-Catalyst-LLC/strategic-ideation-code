#!/usr/bin/env python3
"""
Optional advanced analytics for strategic ideation.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- idea portfolio score chart
- strategic fit vs systems leverage scatterplot
- assumption risk chart
- option architecture ranking table
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
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError as exc:
    print("Missing optional advanced analytics dependencies.")
    print("Run:")
    print("  python3 -m venv .venv")
    print("  source .venv/bin/activate")
    print("  pip install -r python/requirements-advanced.txt")
    raise SystemExit(1) from exc

ideas = pd.read_csv(RAW / "idea_portfolio.csv")
assumptions = pd.read_csv(RAW / "assumptions.csv")
options = pd.read_csv(RAW / "option_architecture.csv")

assumptions["assumption_risk"] = (1 - assumptions["confidence"]) * assumptions["criticality"]
assumption_risk = assumptions.groupby("idea_id", as_index=False)["assumption_risk"].mean()

ideas = ideas.merge(assumption_risk, on="idea_id", how="left")
ideas["assumption_risk"] = ideas["assumption_risk"].fillna(0)

ideas["portfolio_score"] = (
    0.20 * ideas["strategic_fit"]
    + 0.12 * ideas["feasibility"]
    + 0.18 * ideas["systems_leverage"]
    + 0.13 * ideas["learning_value"]
    + 0.16 * ideas["ethical_legitimacy"]
    + 0.09 * ideas["knowledge_reusability"]
    - 0.07 * ideas["uncertainty"]
    - 0.05 * ideas["assumption_risk"]
)

ideas.sort_values("portfolio_score", ascending=True).plot(
    kind="barh",
    x="idea_name",
    y="portfolio_score",
    legend=False,
    figsize=(11, 8),
)
plt.title("Strategic Ideation Portfolio Scores")
plt.xlabel("Portfolio score")
plt.ylabel("Idea")
plt.tight_layout()
plt.savefig(FIGURES / "idea_portfolio_scores.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 7))
plt.scatter(
    ideas["feasibility"],
    ideas["systems_leverage"],
    s=ideas["portfolio_score"] * 450,
    alpha=0.70,
)

for _, row in ideas.iterrows():
    plt.annotate(row["idea_id"], (row["feasibility"], row["systems_leverage"]))

plt.title("Ideas: Feasibility vs Systems Leverage")
plt.xlabel("Feasibility")
plt.ylabel("Systems leverage")
plt.tight_layout()
plt.savefig(FIGURES / "idea_feasibility_vs_systems_leverage.png", dpi=160)
plt.close()

assumptions.sort_values("assumption_risk", ascending=True).plot(
    kind="barh",
    x="assumption_id",
    y="assumption_risk",
    legend=False,
    figsize=(10, 7),
)
plt.title("Assumption Risk Register")
plt.xlabel("Risk = (1 - confidence) × criticality")
plt.ylabel("Assumption")
plt.tight_layout()
plt.savefig(FIGURES / "assumption_risk_register.png", dpi=160)
plt.close()

options["architecture_score"] = (
    0.16 * options["reversibility"]
    - 0.10 * options["dependency_complexity"]
    + 0.24 * options["portfolio_fit"]
    + 0.24 * options["scenario_robustness"]
    + 0.22 * options["sequencing_value"]
)

options.sort_values("architecture_score", ascending=False).to_csv(
    TABLES / "advanced_option_architecture_rankings.csv",
    index=False,
)

print("Advanced ideation analytics complete.")
print(f"Wrote: {FIGURES / 'idea_portfolio_scores.png'}")
print(f"Wrote: {FIGURES / 'idea_feasibility_vs_systems_leverage.png'}")
print(f"Wrote: {FIGURES / 'assumption_risk_register.png'}")
print(f"Wrote: {TABLES / 'advanced_option_architecture_rankings.csv'}")
