#!/usr/bin/env python3
"""
Optional advanced analytics for abductive reasoning and strategic hypotheses.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- hypothesis value chart
- evidence pathway chart
- commitment readiness chart
- portfolio value chart
- simple confidence updating chart
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

hypotheses = pd.read_csv(RAW / "hypotheses.csv")
evidence = pd.read_csv(RAW / "evidence_pathways.csv")
commitments = pd.read_csv(RAW / "commitment_levels.csv")
portfolio = pd.read_csv(RAW / "portfolio_status.csv")

hypotheses["hypothesis_value_score"] = (
    0.16 * hypotheses["explanatory_strength"]
    + 0.14 * hypotheses["testability"]
    + 0.14 * hypotheses["evidence_quality"]
    + 0.16 * hypotheses["strategic_relevance"]
    + 0.12 * hypotheses["stakeholder_visibility"]
    + 0.12 * hypotheses["systems_fit"]
    + 0.10 * hypotheses["actionability"]
    + 0.06 * hypotheses["reversibility"]
    - 0.10 * hypotheses["implementation_risk"]
)

hypotheses.sort_values("hypothesis_value_score", ascending=True).plot(
    kind="barh",
    x="hypothesis_name",
    y="hypothesis_value_score",
    legend=False,
    figsize=(12, 10),
)
plt.title("Strategic Hypothesis Value Scores")
plt.xlabel("Hypothesis value score")
plt.ylabel("Hypothesis")
plt.tight_layout()
plt.savefig(FIGURES / "hypothesis_value_scores.png", dpi=160)
plt.close()

evidence["evidence_value_score"] = (
    0.18 * evidence["evidence_strength"]
    + 0.16 * evidence["reliability"]
    + 0.18 * evidence["discrimination_power"]
    + 0.14 * evidence["stakeholder_legitimacy"]
    - 0.10 * evidence["cost"]
    - 0.08 * evidence["time_to_learn"]
)

evidence.sort_values("evidence_value_score", ascending=True).plot(
    kind="barh",
    x="evidence_name",
    y="evidence_value_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Evidence Pathway Value Scores")
plt.xlabel("Evidence value score")
plt.ylabel("Evidence pathway")
plt.tight_layout()
plt.savefig(FIGURES / "evidence_pathway_scores.png", dpi=160)
plt.close()

commitments["commitment_readiness_score"] = (
    0.16 * commitments["commitment_reversibility"]
    + 0.18 * commitments["evidence_threshold_met"]
    + 0.18 * commitments["confidence_threshold_met"]
    + 0.14 * commitments["stakeholder_threshold_met"]
    + 0.14 * commitments["risk_threshold_met"]
    - 0.12 * commitments["commitment_cost"]
)

commitments.sort_values("commitment_readiness_score", ascending=True).plot(
    kind="barh",
    x="hypothesis_id",
    y="commitment_readiness_score",
    legend=False,
    figsize=(10, 7),
)
plt.title("Commitment Readiness Scores")
plt.xlabel("Readiness score")
plt.ylabel("Hypothesis")
plt.tight_layout()
plt.savefig(FIGURES / "commitment_readiness_scores.png", dpi=160)
plt.close()

portfolio["portfolio_value_score"] = (
    0.16 * portfolio["confidence_level"]
    + 0.16 * portfolio["evidence_readiness"]
    + 0.18 * portfolio["strategic_option_value"]
    + 0.16 * portfolio["learning_value"]
    - 0.10 * portfolio["resource_intensity"]
    + 0.12 * portfolio["time_sensitivity"]
    - 0.10 * portfolio["risk_exposure"]
)

portfolio.sort_values("portfolio_value_score", ascending=True).plot(
    kind="barh",
    x="hypothesis_id",
    y="portfolio_value_score",
    legend=False,
    figsize=(10, 7),
)
plt.title("Hypothesis Portfolio Value Scores")
plt.xlabel("Portfolio value score")
plt.ylabel("Hypothesis")
plt.tight_layout()
plt.savefig(FIGURES / "hypothesis_portfolio_value_scores.png", dpi=160)
plt.close()

# Stylized confidence updating for selected hypotheses.
selected = ["H001", "H003", "H010", "H014"]
update = hypotheses[hypotheses["hypothesis_id"].isin(selected)][
    ["hypothesis_id", "confidence_prior", "evidence_quality", "testability", "systems_fit"]
].copy()

stages = []
for _, row in update.iterrows():
    confidence = float(row["confidence_prior"])
    likelihoods = [
        float(row["evidence_quality"]),
        float(row["testability"]),
        float(row["systems_fit"]),
    ]
    labels = ["prior", "evidence_quality", "testability", "systems_fit"]
    stages.append({"hypothesis_id": row["hypothesis_id"], "stage": labels[0], "confidence": confidence})
    for label, likelihood in zip(labels[1:], likelihoods):
        confidence = (confidence * likelihood) / max(0.001, (confidence * likelihood + (1 - confidence) * (1 - likelihood)))
        stages.append({"hypothesis_id": row["hypothesis_id"], "stage": label, "confidence": confidence})

history = pd.DataFrame(stages)

plt.figure(figsize=(10, 6))
for hypothesis_id, group in history.groupby("hypothesis_id"):
    plt.plot(group["stage"], group["confidence"], marker="o", label=hypothesis_id)
plt.title("Stylized Hypothesis Confidence Updating")
plt.xlabel("Evidence stage")
plt.ylabel("Relative confidence")
plt.legend()
plt.tight_layout()
plt.savefig(FIGURES / "hypothesis_confidence_updating.png", dpi=160)
plt.close()

hypotheses.to_csv(TABLES / "advanced_hypothesis_scores.csv", index=False)
evidence.to_csv(TABLES / "advanced_evidence_pathway_scores.csv", index=False)
commitments.to_csv(TABLES / "advanced_commitment_readiness_scores.csv", index=False)
portfolio.to_csv(TABLES / "advanced_portfolio_value_scores.csv", index=False)
history.to_csv(TABLES / "advanced_hypothesis_confidence_updating.csv", index=False)

print("Advanced abductive hypothesis analytics complete.")
print(f"Wrote: {FIGURES / 'hypothesis_value_scores.png'}")
print(f"Wrote: {FIGURES / 'evidence_pathway_scores.png'}")
print(f"Wrote: {FIGURES / 'commitment_readiness_scores.png'}")
print(f"Wrote: {FIGURES / 'hypothesis_portfolio_value_scores.png'}")
print(f"Wrote: {FIGURES / 'hypothesis_confidence_updating.png'}")
