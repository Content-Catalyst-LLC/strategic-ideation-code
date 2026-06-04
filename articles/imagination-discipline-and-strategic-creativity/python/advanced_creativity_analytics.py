#!/usr/bin/env python3
"""
Optional advanced analytics for imagination, discipline, and strategic creativity.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- strategic creativity score chart
- novelty-theater risk chart
- constraint risk chart
- stakeholder grounding chart
- systems fit chart
- idea maturation chart
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

ideas = pd.read_csv(RAW / "creative_ideas.csv")
constraints = pd.read_csv(RAW / "constraint_audit.csv")
stakeholders = pd.read_csv(RAW / "stakeholder_reviews.csv")
systems = pd.read_csv(RAW / "systems_fit.csv")
maturation = pd.read_csv(RAW / "idea_maturation.csv")
portfolio = pd.read_csv(RAW / "creative_portfolio.csv")

ideas["strategic_creativity_score"] = (
    0.14 * ideas["novelty"]
    + 0.16 * ideas["strategic_relevance"]
    + 0.13 * ideas["conceptual_coherence"]
    + 0.14 * ideas["mechanism_clarity"]
    + 0.11 * ideas["testability"]
    + 0.13 * ideas["stakeholder_grounding"]
    + 0.13 * ideas["systems_fit"]
    + 0.12 * ideas["developmental_potential"]
    + 0.08 * ideas["revision_capacity"]
    - 0.12 * ideas["implementation_risk"]
)

ideas["novelty_theater_risk"] = ideas["novelty"] * (
    1.0 - ((ideas["mechanism_clarity"] + ideas["systems_fit"] + ideas["stakeholder_grounding"]) / 3.0)
)

ideas.sort_values("strategic_creativity_score", ascending=True).plot(
    kind="barh",
    x="idea_name",
    y="strategic_creativity_score",
    legend=False,
    figsize=(12, 10),
)
plt.title("Strategic Creativity Scores")
plt.xlabel("Strategic creativity score")
plt.ylabel("Idea")
plt.tight_layout()
plt.savefig(FIGURES / "strategic_creativity_scores.png", dpi=160)
plt.close()

ideas.sort_values("novelty_theater_risk", ascending=True).plot(
    kind="barh",
    x="idea_name",
    y="novelty_theater_risk",
    legend=False,
    figsize=(12, 10),
)
plt.title("Novelty-Theater Risk")
plt.xlabel("Risk score")
plt.ylabel("Idea")
plt.tight_layout()
plt.savefig(FIGURES / "novelty_theater_risk.png", dpi=160)
plt.close()

constraints["dead_constraint_risk"] = (
    0.30 * constraints["search_narrowing_risk"]
    + 0.30 * constraints["assumption_disguise_risk"]
    + 0.18 * constraints["changeability"]
    - 0.18 * constraints["constraint_legitimacy"]
    - 0.12 * constraints["ethical_importance"]
)

constraints.sort_values("dead_constraint_risk", ascending=True).plot(
    kind="barh",
    x="constraint_name",
    y="dead_constraint_risk",
    legend=False,
    figsize=(12, 8),
)
plt.title("Dead Constraint Risk")
plt.xlabel("Risk score")
plt.ylabel("Constraint")
plt.tight_layout()
plt.savefig(FIGURES / "dead_constraint_risk.png", dpi=160)
plt.close()

stakeholders["stakeholder_grounding_score"] = (
    0.16 * stakeholders["visibility_quality"]
    + 0.16 * stakeholders["burden_visibility"]
    + 0.14 * stakeholders["trust_sensitivity"]
    + 0.14 * stakeholders["agency_preservation"]
    + 0.14 * stakeholders["participation_quality"]
    + 0.16 * stakeholders["legitimacy_score"]
    - 0.10 * stakeholders["hidden_harm_risk"]
)

stakeholders.sort_values("stakeholder_grounding_score", ascending=True).plot(
    kind="barh",
    x="review_id",
    y="stakeholder_grounding_score",
    legend=False,
    figsize=(10, 7),
)
plt.title("Stakeholder Grounding Scores")
plt.xlabel("Grounding score")
plt.ylabel("Review")
plt.tight_layout()
plt.savefig(FIGURES / "stakeholder_grounding_scores.png", dpi=160)
plt.close()

systems["systems_fit_score"] = (
    0.14 * systems["feedback_awareness"]
    + 0.14 * systems["incentive_fit"]
    + 0.12 * systems["dependency_visibility"]
    + 0.12 * systems["delay_awareness"]
    + 0.14 * systems["second_order_review"]
    + 0.12 * systems["boundary_quality"]
    + 0.12 * systems["adaptation_review"]
    + 0.14 * systems["robustness_across_scenarios"]
    - 0.12 * systems["systems_risk"]
)

systems.sort_values("systems_fit_score", ascending=True).plot(
    kind="barh",
    x="systems_id",
    y="systems_fit_score",
    legend=False,
    figsize=(10, 7),
)
plt.title("Systems Fit Scores")
plt.xlabel("Systems fit score")
plt.ylabel("Review")
plt.tight_layout()
plt.savefig(FIGURES / "systems_fit_scores.png", dpi=160)
plt.close()

maturation["maturation_score"] = (
    0.14 * maturation["clarification_gain"]
    + 0.14 * maturation["evidence_gain"]
    + 0.14 * maturation["stakeholder_gain"]
    + 0.14 * maturation["systems_gain"]
    + 0.14 * maturation["recombination_gain"]
    + 0.16 * maturation["revision_quality"]
    + 0.14 * maturation["stage_gate_quality"]
)

maturation.sort_values("maturation_score", ascending=True).plot(
    kind="barh",
    x="idea_id",
    y="maturation_score",
    legend=False,
    figsize=(10, 7),
)
plt.title("Idea Maturation Scores")
plt.xlabel("Maturation score")
plt.ylabel("Idea")
plt.tight_layout()
plt.savefig(FIGURES / "idea_maturation_scores.png", dpi=160)
plt.close()

portfolio["portfolio_value_score"] = (
    0.14 * portfolio["confidence_level"]
    + 0.14 * portfolio["evidence_readiness"]
    + 0.18 * portfolio["strategic_option_value"]
    + 0.16 * portfolio["learning_value"]
    - 0.10 * portfolio["resource_intensity"]
    + 0.12 * portfolio["time_sensitivity"]
    - 0.10 * portfolio["risk_exposure"]
)

portfolio.sort_values("portfolio_value_score", ascending=True).plot(
    kind="barh",
    x="idea_id",
    y="portfolio_value_score",
    legend=False,
    figsize=(10, 7),
)
plt.title("Creative Portfolio Value Scores")
plt.xlabel("Portfolio value score")
plt.ylabel("Idea")
plt.tight_layout()
plt.savefig(FIGURES / "creative_portfolio_value_scores.png", dpi=160)
plt.close()

ideas.to_csv(TABLES / "advanced_strategic_creativity_scores.csv", index=False)
constraints.to_csv(TABLES / "advanced_constraint_risks.csv", index=False)
stakeholders.to_csv(TABLES / "advanced_stakeholder_grounding_scores.csv", index=False)
systems.to_csv(TABLES / "advanced_systems_fit_scores.csv", index=False)
maturation.to_csv(TABLES / "advanced_idea_maturation_scores.csv", index=False)
portfolio.to_csv(TABLES / "advanced_creative_portfolio_scores.csv", index=False)

print("Advanced strategic creativity analytics complete.")
print(f"Wrote: {FIGURES / 'strategic_creativity_scores.png'}")
print(f"Wrote: {FIGURES / 'novelty_theater_risk.png'}")
print(f"Wrote: {FIGURES / 'dead_constraint_risk.png'}")
print(f"Wrote: {FIGURES / 'stakeholder_grounding_scores.png'}")
print(f"Wrote: {FIGURES / 'systems_fit_scores.png'}")
print(f"Wrote: {FIGURES / 'idea_maturation_scores.png'}")
print(f"Wrote: {FIGURES / 'creative_portfolio_value_scores.png'}")
