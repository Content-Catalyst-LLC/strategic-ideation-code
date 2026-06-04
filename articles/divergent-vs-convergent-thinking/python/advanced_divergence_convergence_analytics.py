#!/usr/bin/env python3
"""
Optional advanced analytics for divergent vs convergent thinking.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- divergence-convergence profile chart
- premature convergence risk chart
- unbounded divergence risk chart
- idea portfolio chart
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

contexts = pd.read_csv(RAW / "ideation_contexts.csv")
ideas = pd.read_csv(RAW / "idea_portfolio.csv")
criteria = pd.read_csv(RAW / "evaluation_criteria.csv")

contexts["profile_score"] = (
    0.16 * contexts["exploratory_breadth"]
    + 0.16 * contexts["evaluative_discipline"]
    + 0.18 * contexts["iteration_quality"]
    + 0.14 * contexts["constraint_clarity"]
    + 0.12 * contexts["stakeholder_inclusion"]
    + 0.12 * contexts["evidence_contact"]
    + 0.08 * contexts["action_readiness"]
    + 0.04 * contexts["decision_memory_quality"]
)

contexts["premature_convergence_risk"] = (1 - contexts["exploratory_breadth"]) * contexts["closure_pressure"]
contexts["unbounded_divergence_risk"] = contexts["exploratory_breadth"] * (1 - contexts["evaluative_discipline"])

contexts.sort_values("profile_score", ascending=True).plot(
    kind="barh",
    x="context_name",
    y="profile_score",
    legend=False,
    figsize=(11, 8),
)
plt.title("Divergence-Convergence Profile Scores")
plt.xlabel("Profile score")
plt.ylabel("Context")
plt.tight_layout()
plt.savefig(FIGURES / "divergence_convergence_profile_scores.png", dpi=160)
plt.close()

contexts.sort_values("premature_convergence_risk", ascending=True).plot(
    kind="barh",
    x="context_name",
    y="premature_convergence_risk",
    legend=False,
    figsize=(11, 8),
)
plt.title("Premature Convergence Risk")
plt.xlabel("Risk")
plt.ylabel("Context")
plt.tight_layout()
plt.savefig(FIGURES / "premature_convergence_risk.png", dpi=160)
plt.close()

contexts.sort_values("unbounded_divergence_risk", ascending=True).plot(
    kind="barh",
    x="context_name",
    y="unbounded_divergence_risk",
    legend=False,
    figsize=(11, 8),
)
plt.title("Unbounded Divergence Risk")
plt.xlabel("Risk")
plt.ylabel("Context")
plt.tight_layout()
plt.savefig(FIGURES / "unbounded_divergence_risk.png", dpi=160)
plt.close()

ideas["idea_score"] = (
    0.12 * ideas["novelty"]
    + 0.18 * ideas["strategic_fit"]
    + 0.14 * ideas["evidence_strength"]
    + 0.12 * ideas["feasibility"]
    + 0.14 * ideas["stakeholder_value"]
    + 0.10 * ideas["risk_visibility"]
    + 0.12 * ideas["ethical_legitimacy"]
    + 0.10 * ideas["implementation_readiness"]
    - 0.08 * ideas["assumption_burden"]
)

ideas.sort_values("idea_score", ascending=True).plot(
    kind="barh",
    x="idea_name",
    y="idea_score",
    legend=False,
    figsize=(12, 9),
)
plt.title("Idea Portfolio Scores")
plt.xlabel("Idea score")
plt.ylabel("Idea")
plt.tight_layout()
plt.savefig(FIGURES / "idea_portfolio_scores.png", dpi=160)
plt.close()

criteria["criteria_quality_score"] = (
    0.24 * criteria["definition_clarity"]
    + 0.18 * criteria["weight_justification"]
    + 0.20 * criteria["measurement_validity"]
    - 0.18 * criteria["bias_risk"]
    + 0.16 * criteria["stakeholder_relevance"]
    + 0.12 * criteria["strategic_importance"]
)

criteria.sort_values("criteria_quality_score", ascending=True).to_csv(
    TABLES / "advanced_criteria_quality_rankings.csv",
    index=False,
)

print("Advanced divergence-convergence analytics complete.")
print(f"Wrote: {FIGURES / 'divergence_convergence_profile_scores.png'}")
print(f"Wrote: {FIGURES / 'premature_convergence_risk.png'}")
print(f"Wrote: {FIGURES / 'unbounded_divergence_risk.png'}")
print(f"Wrote: {FIGURES / 'idea_portfolio_scores.png'}")
print(f"Wrote: {TABLES / 'advanced_criteria_quality_rankings.csv'}")
