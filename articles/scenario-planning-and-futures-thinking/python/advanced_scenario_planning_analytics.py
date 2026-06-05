#!/usr/bin/env python3
"""
Optional advanced analytics for Scenario Planning and Futures Thinking.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- scenario quality chart
- workshop theater risk chart
- critical uncertainty chart
- strategy robustness chart
- fragility risk chart
- signal monitoring chart
- adaptive pathway chart
- futures ethics risk chart
"""

from __future__ import annotations

from pathlib import Path
import math

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

scenarios = pd.read_csv(RAW / "scenario_sets.csv")
drivers = pd.read_csv(RAW / "driver_uncertainties.csv")
stress = pd.read_csv(RAW / "strategy_stress_tests.csv")
signals = pd.read_csv(RAW / "signal_monitoring.csv")
pathways = pd.read_csv(RAW / "adaptive_pathways.csv")
ethics = pd.read_csv(RAW / "futures_ethics.csv")

scenarios["scenario_quality_score"] = (
    0.10 * scenarios["focal_question_clarity"]
    + 0.08 * scenarios["time_horizon_fit"]
    + 0.11 * scenarios["driver_analysis_quality"]
    + 0.12 * scenarios["critical_uncertainty_quality"]
    + 0.09 * scenarios["plausibility"]
    + 0.10 * scenarios["internal_coherence"]
    + 0.11 * scenarios["scenario_divergence"]
    + 0.12 * scenarios["strategic_implication_quality"]
    + 0.08 * scenarios["signal_monitoring_quality"]
    + 0.06 * scenarios["decision_linkage"]
    + 0.07 * scenarios["ethics_review"]
    + 0.06 * scenarios["learning_memory"]
)

scenarios["workshop_theater_risk"] = (
    0.16 * (1 - scenarios["decision_linkage"])
    + 0.14 * (1 - scenarios["strategic_implication_quality"])
    + 0.12 * (1 - scenarios["signal_monitoring_quality"])
    + 0.12 * (1 - scenarios["learning_memory"])
    + 0.11 * (1 - scenarios["focal_question_clarity"])
    + 0.11 * (1 - scenarios["critical_uncertainty_quality"])
    + 0.10 * (1 - scenarios["scenario_divergence"])
    + 0.08 * (1 - scenarios["ethics_review"])
    + 0.06 * (1 - scenarios["driver_analysis_quality"])
)

scenarios.sort_values("scenario_quality_score", ascending=True).plot(
    kind="barh",
    x="scenario_set_name",
    y="scenario_quality_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Scenario Set Quality")
plt.xlabel("Quality score")
plt.ylabel("Scenario set")
plt.tight_layout()
plt.savefig(FIGURES / "scenario_set_quality.png", dpi=160)
plt.close()

scenarios.sort_values("workshop_theater_risk", ascending=True).plot(
    kind="barh",
    x="scenario_set_name",
    y="workshop_theater_risk",
    legend=False,
    figsize=(12, 8),
)
plt.title("Scenario Workshop Theater Risk")
plt.xlabel("Risk")
plt.ylabel("Scenario set")
plt.tight_layout()
plt.savefig(FIGURES / "workshop_theater_risk.png", dpi=160)
plt.close()

drivers["critical_uncertainty_score"] = (
    0.30 * drivers["impact"]
    + 0.26 * drivers["uncertainty"]
    + 0.16 * drivers["systemic_interdependence"]
    + 0.12 * drivers["stakeholder_salience"]
    + 0.08 * drivers["evidence_quality"]
    + 0.08 * drivers["monitoring_feasibility"]
)

drivers.sort_values("critical_uncertainty_score", ascending=True).plot(
    kind="barh",
    x="driver_name",
    y="critical_uncertainty_score",
    legend=False,
    figsize=(12, 9),
)
plt.title("Critical Driver and Uncertainty Scores")
plt.xlabel("Score")
plt.ylabel("Driver")
plt.tight_layout()
plt.savefig(FIGURES / "critical_uncertainty_scores.png", dpi=160)
plt.close()

scenario_cols = [
    "scenario_stable_growth",
    "scenario_tech_disruption",
    "scenario_environmental_stress",
    "scenario_institutional_fragmentation",
    "scenario_supply_disruption",
]

stress["mean_performance"] = stress[scenario_cols].mean(axis=1)
stress["worst_case"] = stress[scenario_cols].min(axis=1)
stress["best_case"] = stress[scenario_cols].max(axis=1)
stress["volatility"] = stress[scenario_cols].std(axis=1)

stress["robustness_profile"] = (
    0.30 * stress["worst_case"]
    + 0.24 * stress["mean_performance"]
    + 0.16 * stress["flexibility"]
    + 0.12 * stress["implementation_readiness"]
    + 0.10 * stress["ethical_resilience"]
    + 0.10 * stress["option_value"]
    - 0.12 * stress["volatility"]
)

stress["fragility_risk"] = (
    0.30 * (1 - stress["worst_case"])
    + 0.18 * stress["volatility"]
    + 0.14 * (1 - stress["flexibility"])
    + 0.12 * (1 - stress["option_value"])
    + 0.10 * (1 - stress["ethical_resilience"])
    + 0.08 * (1 - stress["implementation_readiness"])
)

stress.sort_values("robustness_profile", ascending=True).plot(
    kind="barh",
    x="strategy_name",
    y="robustness_profile",
    legend=False,
    figsize=(12, 8),
)
plt.title("Scenario-Based Strategy Robustness")
plt.xlabel("Robustness profile")
plt.ylabel("Strategy")
plt.tight_layout()
plt.savefig(FIGURES / "strategy_robustness_profiles.png", dpi=160)
plt.close()

stress_long = stress.melt(
    id_vars=["strategy_name"],
    value_vars=scenario_cols,
    var_name="scenario",
    value_name="performance"
)

plt.figure(figsize=(11, 7))
for strategy in stress_long["strategy_name"].unique():
    subset = stress_long[stress_long["strategy_name"] == strategy]
    plt.plot(subset["scenario"], subset["performance"], marker="o", label=strategy)

plt.ylabel("Performance")
plt.title("Strategy Performance Across Scenarios")
plt.legend(fontsize=8)
plt.xticks(rotation=25)
plt.tight_layout()
plt.savefig(FIGURES / "strategy_performance_across_scenarios.png", dpi=160)
plt.close()

stress.sort_values("fragility_risk", ascending=True).plot(
    kind="barh",
    x="strategy_name",
    y="fragility_risk",
    legend=False,
    figsize=(12, 8),
)
plt.title("Scenario Fragility Risk")
plt.xlabel("Risk")
plt.ylabel("Strategy")
plt.tight_layout()
plt.savefig(FIGURES / "scenario_fragility_risk.png", dpi=160)
plt.close()

signals["response_priority"] = (
    0.20 * signals["decision_relevance"]
    + 0.18 * signals["lead_time_value"]
    + 0.16 * signals["signal_strength"]
    + 0.14 * signals["interpretation_quality"]
    + 0.12 * signals["monitoring_quality"]
    + 0.10 * signals["owner_clarity"]
    - 0.10 * signals["noise_risk"]
)

signals.sort_values("response_priority", ascending=True).plot(
    kind="barh",
    x="signal_name",
    y="response_priority",
    legend=False,
    figsize=(12, 9),
)
plt.title("Signal Monitoring Response Priority")
plt.xlabel("Priority")
plt.ylabel("Signal")
plt.tight_layout()
plt.savefig(FIGURES / "signal_monitoring_priority.png", dpi=160)
plt.close()

pathways["adaptive_pathway_score"] = (
    0.15 * pathways["trigger_clarity"]
    + 0.14 * pathways["reversibility"]
    + 0.16 * pathways["option_value"]
    + 0.13 * pathways["resource_flexibility"]
    + 0.13 * pathways["capability_readiness"]
    + 0.12 * pathways["governance_clarity"]
    + 0.10 * pathways["stakeholder_alignment"]
    + 0.07 * pathways["learning_memory"]
)

pathways.sort_values("adaptive_pathway_score", ascending=True).plot(
    kind="barh",
    x="pathway_name",
    y="adaptive_pathway_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Adaptive Pathway Scores")
plt.xlabel("Score")
plt.ylabel("Pathway")
plt.tight_layout()
plt.savefig(FIGURES / "adaptive_pathway_scores.png", dpi=160)
plt.close()

ethics["futures_ethics_score"] = (
    0.16 * ethics["representation_quality"]
    + 0.15 * ethics["power_review_quality"]
    + 0.16 * ethics["burden_shift_review"]
    + 0.14 * ethics["intergenerational_review"]
    + 0.13 * ethics["accessibility_quality"]
    + 0.14 * ethics["accountability_quality"]
    + 0.12 * ethics["redress_path_quality"]
)
ethics["futures_ethics_risk"] = 1 - ethics["futures_ethics_score"]

ethics.sort_values("futures_ethics_risk", ascending=True).plot(
    kind="barh",
    x="ethical_issue",
    y="futures_ethics_risk",
    legend=False,
    figsize=(12, 9),
)
plt.title("Futures Ethics Risk")
plt.xlabel("Risk")
plt.ylabel("Ethical issue")
plt.tight_layout()
plt.savefig(FIGURES / "futures_ethics_risk.png", dpi=160)
plt.close()

scenarios.to_csv(TABLES / "advanced_scenario_set_scores.csv", index=False)
drivers.to_csv(TABLES / "advanced_driver_uncertainty_scores.csv", index=False)
stress.to_csv(TABLES / "advanced_strategy_stress_test_scores.csv", index=False)
signals.to_csv(TABLES / "advanced_signal_monitoring_scores.csv", index=False)
pathways.to_csv(TABLES / "advanced_adaptive_pathway_scores.csv", index=False)
ethics.to_csv(TABLES / "advanced_futures_ethics_scores.csv", index=False)

print("Advanced scenario planning analytics complete.")
print(f"Wrote: {FIGURES / 'scenario_set_quality.png'}")
print(f"Wrote: {FIGURES / 'workshop_theater_risk.png'}")
print(f"Wrote: {FIGURES / 'critical_uncertainty_scores.png'}")
print(f"Wrote: {FIGURES / 'strategy_robustness_profiles.png'}")
print(f"Wrote: {FIGURES / 'strategy_performance_across_scenarios.png'}")
print(f"Wrote: {FIGURES / 'scenario_fragility_risk.png'}")
print(f"Wrote: {FIGURES / 'signal_monitoring_priority.png'}")
print(f"Wrote: {FIGURES / 'adaptive_pathway_scores.png'}")
print(f"Wrote: {FIGURES / 'futures_ethics_risk.png'}")
