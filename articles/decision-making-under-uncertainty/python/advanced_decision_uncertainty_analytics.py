#!/usr/bin/env python3
"""
Optional advanced analytics for Decision-Making Under Uncertainty.

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

options = pd.read_csv(RAW / "decision_options.csv")
assumptions = pd.read_csv(RAW / "assumption_register.csv")
stress = pd.read_csv(RAW / "scenario_stress_tests.csv")
option_value = pd.read_csv(RAW / "option_value_reviews.csv")
experiments = pd.read_csv(RAW / "experiment_designs.csv")
biases = pd.read_csv(RAW / "heuristic_bias_reviews.csv")
ethics = pd.read_csv(RAW / "ethical_uncertainty.csv")

options["decision_profile_score"] = (
    0.14 * options["expected_return"]
    + 0.18 * options["robustness"]
    + 0.16 * options["flexibility"]
    + 0.12 * options["information_quality"]
    - 0.16 * options["exposure"]
    + 0.14 * options["option_value"]
    + 0.10 * options["reversibility"]
    + 0.08 * options["implementation_readiness"]
    + 0.10 * options["ethical_resilience"]
    + 0.10 * options["learning_value"]
)

options["fragility_risk"] = (
    0.24 * options["exposure"]
    + 0.18 * (1 - options["robustness"])
    + 0.14 * (1 - options["flexibility"])
    + 0.13 * (1 - options["option_value"])
    + 0.12 * (1 - options["reversibility"])
    + 0.10 * (1 - options["ethical_resilience"])
    + 0.09 * (1 - options["information_quality"])
)

options.sort_values("decision_profile_score", ascending=True).plot(
    kind="barh", x="option_name", y="decision_profile_score", legend=False, figsize=(12, 8)
)
plt.title("Decision Profile Under Uncertainty")
plt.xlabel("Profile score")
plt.ylabel("Option")
plt.tight_layout()
plt.savefig(FIGURES / "decision_profile_scores.png", dpi=160)
plt.close()

options.sort_values("fragility_risk", ascending=True).plot(
    kind="barh", x="option_name", y="fragility_risk", legend=False, figsize=(12, 8)
)
plt.title("Decision Fragility Risk")
plt.xlabel("Fragility risk")
plt.ylabel("Option")
plt.tight_layout()
plt.savefig(FIGURES / "decision_fragility_risk.png", dpi=160)
plt.close()

assumptions["assumption_risk"] = (
    0.25 * assumptions["uncertainty"]
    + 0.25 * assumptions["consequence"]
    + 0.15 * (1 - assumptions["evidence_quality"])
    + 0.14 * assumptions["decay_risk"]
    + 0.11 * (1 - assumptions["monitorability"])
    + 0.10 * (1 - assumptions["owner_clarity"])
)

assumptions.sort_values("assumption_risk", ascending=True).plot(
    kind="barh", x="assumption", y="assumption_risk", legend=False, figsize=(12, 9)
)
plt.title("Critical Assumption Risk")
plt.xlabel("Risk")
plt.ylabel("Assumption")
plt.tight_layout()
plt.savefig(FIGURES / "assumption_risk_scores.png", dpi=160)
plt.close()

scenario_cols = [
    "scenario_stable_growth",
    "scenario_tech_disruption",
    "scenario_environmental_stress",
    "scenario_regulatory_shift",
    "scenario_trust_crisis",
    "scenario_resource_constraint",
]

stress["mean_performance"] = stress[scenario_cols].mean(axis=1)
stress["worst_case"] = stress[scenario_cols].min(axis=1)
stress["best_case"] = stress[scenario_cols].max(axis=1)
stress["volatility"] = stress[scenario_cols].std(axis=1)
stress["robustness_score"] = (
    0.42 * stress["worst_case"]
    + 0.30 * stress["mean_performance"]
    - 0.18 * stress["volatility"]
    + 0.10 * stress["best_case"]
)

stress = stress.merge(options[["option_id", "option_name"]], on="option_id", how="left")

stress.sort_values("robustness_score", ascending=True).plot(
    kind="barh", x="option_name", y="robustness_score", legend=False, figsize=(12, 8)
)
plt.title("Scenario Robustness Score")
plt.xlabel("Robustness")
plt.ylabel("Option")
plt.tight_layout()
plt.savefig(FIGURES / "scenario_robustness_scores.png", dpi=160)
plt.close()

stress_long = stress.melt(
    id_vars=["option_name"],
    value_vars=scenario_cols,
    var_name="scenario",
    value_name="performance",
)

plt.figure(figsize=(11, 7))
for name in stress_long["option_name"].unique():
    subset = stress_long[stress_long["option_name"] == name]
    plt.plot(subset["scenario"], subset["performance"], marker="o", label=name)
plt.title("Option Performance Across Scenarios")
plt.ylabel("Performance")
plt.xticks(rotation=25)
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "option_performance_across_scenarios.png", dpi=160)
plt.close()

option_value["option_value_score"] = (
    0.18 * option_value["learning_value"]
    + 0.18 * option_value["future_flexibility"]
    + 0.15 * option_value["reversibility"]
    + 0.13 * option_value["staged_commitment_quality"]
    + 0.12 * option_value["modularity"]
    + 0.11 * option_value["exit_path_quality"]
    - 0.15 * option_value["lock_in_cost"]
    + 0.08 * option_value["monitoring_quality"]
)
option_value = option_value.merge(options[["option_id", "option_name"]], on="option_id", how="left")

option_value.sort_values("option_value_score", ascending=True).plot(
    kind="barh", x="option_name", y="option_value_score", legend=False, figsize=(12, 8)
)
plt.title("Option Value Scores")
plt.xlabel("Option value")
plt.ylabel("Option")
plt.tight_layout()
plt.savefig(FIGURES / "option_value_scores.png", dpi=160)
plt.close()

experiments["experiment_quality"] = (
    0.16 * experiments["learning_question_quality"]
    + 0.14 * experiments["reversibility"]
    + 0.14 * experiments["exposure_control"]
    + 0.15 * experiments["evidence_quality"]
    + 0.12 * experiments["stakeholder_feedback_quality"]
    + 0.14 * experiments["scaling_trigger_clarity"]
    + 0.15 * experiments["decision_relevance"]
)
experiments.sort_values("experiment_quality", ascending=True).plot(
    kind="barh", x="experiment_name", y="experiment_quality", legend=False, figsize=(12, 8)
)
plt.title("Experiment Design Quality")
plt.xlabel("Quality")
plt.ylabel("Experiment")
plt.tight_layout()
plt.savefig(FIGURES / "experiment_design_quality.png", dpi=160)
plt.close()

biases["bias_risk"] = (
    0.26 * biases["exposure_level"]
    + 0.26 * biases["decision_influence"]
    + 0.16 * (1 - biases["detectability"])
    + 0.16 * (1 - biases["mitigation_quality"])
    + 0.16 * (1 - biases["challenge_process_quality"])
)
biases.sort_values("bias_risk", ascending=True).plot(
    kind="barh", x="bias_or_heuristic", y="bias_risk", legend=False, figsize=(12, 8)
)
plt.title("Heuristic and Bias Risk")
plt.xlabel("Risk")
plt.ylabel("Bias or heuristic")
plt.tight_layout()
plt.savefig(FIGURES / "heuristic_bias_risk.png", dpi=160)
plt.close()

ethics["ethical_uncertainty_score"] = (
    0.14 * ethics["transparency"]
    + 0.15 * ethics["burden_shift_review"]
    + 0.15 * ethics["stakeholder_representation"]
    + 0.14 * ethics["accountability"]
    + 0.14 * ethics["revisability"]
    + 0.14 * ethics["precaution_quality"]
    + 0.14 * ethics["redress_path_quality"]
)
ethics["ethical_uncertainty_risk"] = 1 - ethics["ethical_uncertainty_score"]

ethics.sort_values("ethical_uncertainty_risk", ascending=True).plot(
    kind="barh", x="ethical_issue", y="ethical_uncertainty_risk", legend=False, figsize=(12, 9)
)
plt.title("Ethical Uncertainty Risk")
plt.xlabel("Risk")
plt.ylabel("Ethical issue")
plt.tight_layout()
plt.savefig(FIGURES / "ethical_uncertainty_risk.png", dpi=160)
plt.close()

time_steps = np.arange(1, 41)
simulation = pd.DataFrame({"time": time_steps})
option_path_simulation = pd.DataFrame({"time": time_steps})

for _, row in options.iterrows():
    state = np.zeros(len(time_steps))
    option_path = np.zeros(len(time_steps))
    state[0] = 1.0
    option_path[0] = row["option_value"]

    for t in range(1, len(time_steps)):
        if t < 20:
            shock = 0.03
            gain = 0.18 * row["expected_return"] + 0.08 * row["flexibility"]
        else:
            shock = 0.15
            gain = (
                0.08 * row["expected_return"]
                + 0.18 * row["robustness"]
                + 0.14 * row["flexibility"]
                + 0.08 * option_path[t - 1]
                - 0.14 * row["exposure"]
            )

        option_path[t] = np.clip(option_path[t - 1] + 0.04 * row["flexibility"] - 0.05 * row["exposure"], 0, 1.2)
        state[t] = np.clip(state[t - 1] + gain / 4 - shock / 5, 0, 1.8)

    simulation[row["option_name"]] = state
    option_path_simulation[row["option_name"]] = option_path

plt.figure(figsize=(11, 7))
for col in simulation.columns[1:]:
    plt.plot(simulation["time"], simulation[col], label=col)
plt.xlabel("Time Step")
plt.ylabel("Decision Viability")
plt.title("Decision-Making Under Uncertainty Simulation")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "decision_uncertainty_simulation.png", dpi=160)
plt.close()

options.to_csv(TABLES / "advanced_decision_option_scores.csv", index=False)
assumptions.to_csv(TABLES / "advanced_assumption_risk_scores.csv", index=False)
stress.to_csv(TABLES / "advanced_scenario_stress_test_scores.csv", index=False)
option_value.to_csv(TABLES / "advanced_option_value_scores.csv", index=False)
experiments.to_csv(TABLES / "advanced_experiment_design_scores.csv", index=False)
biases.to_csv(TABLES / "advanced_heuristic_bias_scores.csv", index=False)
ethics.to_csv(TABLES / "advanced_ethical_uncertainty_scores.csv", index=False)
simulation.to_csv(TABLES / "decision_uncertainty_simulation.csv", index=False)
option_path_simulation.to_csv(TABLES / "decision_option_value_simulation.csv", index=False)

print("Advanced decision uncertainty analytics complete.")
print(f"Wrote: {FIGURES / 'decision_profile_scores.png'}")
print(f"Wrote: {FIGURES / 'decision_fragility_risk.png'}")
print(f"Wrote: {FIGURES / 'assumption_risk_scores.png'}")
print(f"Wrote: {FIGURES / 'scenario_robustness_scores.png'}")
print(f"Wrote: {FIGURES / 'option_performance_across_scenarios.png'}")
print(f"Wrote: {FIGURES / 'option_value_scores.png'}")
print(f"Wrote: {FIGURES / 'experiment_design_quality.png'}")
print(f"Wrote: {FIGURES / 'heuristic_bias_risk.png'}")
print(f"Wrote: {FIGURES / 'ethical_uncertainty_risk.png'}")
print(f"Wrote: {FIGURES / 'decision_uncertainty_simulation.png'}")
