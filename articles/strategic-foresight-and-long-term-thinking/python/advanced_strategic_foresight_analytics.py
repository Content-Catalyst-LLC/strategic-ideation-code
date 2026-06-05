#!/usr/bin/env python3
"""
Optional advanced analytics for Strategic Foresight and Long-Term Thinking.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- future viability chart
- short-term bias chart
- signal priority chart
- critical uncertainty chart
- strategy robustness chart
- path dependence chart
- adaptive pathway chart
- futures ethics risk chart
- long-term viability simulation
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

profiles = pd.read_csv(RAW / "foresight_profiles.csv")
signals = pd.read_csv(RAW / "horizon_signals.csv")
drivers = pd.read_csv(RAW / "driver_uncertainties.csv")
stress = pd.read_csv(RAW / "strategy_stress_tests.csv")
path_dep = pd.read_csv(RAW / "path_dependence.csv")
pathways = pd.read_csv(RAW / "adaptive_pathways.csv")
ethics = pd.read_csv(RAW / "futures_ethics.csv")

profiles["future_viability_score"] = (
    0.18 * profiles["foresight_depth"]
    + 0.18 * profiles["resilience"]
    + 0.16 * profiles["flexibility"]
    + 0.14 * profiles["option_value"]
    + 0.12 * profiles["scenario_capacity"]
    + 0.10 * profiles["signal_capacity"]
    + 0.08 * profiles["governance_capacity"]
    + 0.08 * profiles["ethics_review"]
    - 0.14 * profiles["path_dependence_risk"]
)

profiles["short_term_bias"] = (
    profiles["short_term_return"]
    - (
        profiles["foresight_depth"]
        + profiles["resilience"]
        + profiles["flexibility"]
        + profiles["option_value"]
    ) / 4
)

profiles.sort_values("future_viability_score", ascending=True).plot(
    kind="barh",
    x="strategy_name",
    y="future_viability_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Future Viability Score")
plt.xlabel("Score")
plt.ylabel("Strategy")
plt.tight_layout()
plt.savefig(FIGURES / "future_viability_scores.png", dpi=160)
plt.close()

profiles.sort_values("short_term_bias", ascending=True).plot(
    kind="barh",
    x="strategy_name",
    y="short_term_bias",
    legend=False,
    figsize=(12, 8),
)
plt.title("Short-Term Optimization Bias")
plt.xlabel("Bias")
plt.ylabel("Strategy")
plt.tight_layout()
plt.savefig(FIGURES / "short_term_bias.png", dpi=160)
plt.close()

signals["response_priority"] = (
    0.20 * signals["strategic_relevance"]
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
plt.title("Horizon Signal Response Priority")
plt.xlabel("Priority")
plt.ylabel("Signal")
plt.tight_layout()
plt.savefig(FIGURES / "horizon_signal_priority.png", dpi=160)
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

future_cols = [
    "future_stable_growth",
    "future_tech_disruption",
    "future_environmental_stress",
    "future_institutional_fragmentation",
    "future_public_trust_crisis",
]

stress["mean_performance"] = stress[future_cols].mean(axis=1)
stress["worst_case"] = stress[future_cols].min(axis=1)
stress["volatility"] = stress[future_cols].std(axis=1)
stress["robustness_profile"] = (
    0.30 * stress["worst_case"]
    + 0.24 * stress["mean_performance"]
    + 0.16 * stress["flexibility"]
    + 0.12 * stress["implementation_readiness"]
    + 0.10 * stress["ethical_resilience"]
    + 0.10 * stress["option_value"]
    - 0.12 * stress["volatility"]
)

stress.sort_values("robustness_profile", ascending=True).plot(
    kind="barh",
    x="strategy_name",
    y="robustness_profile",
    legend=False,
    figsize=(12, 8),
)
plt.title("Cross-Future Strategy Robustness")
plt.xlabel("Robustness profile")
plt.ylabel("Strategy")
plt.tight_layout()
plt.savefig(FIGURES / "strategy_robustness_profiles.png", dpi=160)
plt.close()

path_dep["lock_in_risk_score"] = (
    0.20 * path_dep["lock_in_strength"]
    + 0.18 * (1 - path_dep["reversibility"])
    + 0.16 * path_dep["transition_cost"]
    + 0.14 * path_dep["capability_gap"]
    + 0.12 * path_dep["governance_constraint"]
    + 0.10 * path_dep["stakeholder_constraint"]
    + 0.10 * path_dep["option_loss_risk"]
)

path_dep.sort_values("lock_in_risk_score", ascending=True).plot(
    kind="barh",
    x="path_dependency",
    y="lock_in_risk_score",
    legend=False,
    figsize=(12, 9),
)
plt.title("Path Dependence and Lock-In Risk")
plt.xlabel("Risk")
plt.ylabel("Path dependency")
plt.tight_layout()
plt.savefig(FIGURES / "path_dependence_lock_in_risk.png", dpi=160)
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

time_steps = np.arange(1, 41)

def simulate_strategy(row):
    state = np.zeros(len(time_steps))
    option_value = np.zeros(len(time_steps))
    state[0] = 1.0
    option_value[0] = row["option_value"]

    for t in range(1, len(time_steps)):
        if t < 20:
            shock = 0.03
            gain = (
                0.14 * row["short_term_return"]
                + 0.08 * row["flexibility"]
                + 0.06 * row["foresight_depth"]
            )
        else:
            shock = 0.15
            gain = (
                0.08 * row["short_term_return"]
                + 0.18 * row["resilience"]
                + 0.14 * row["flexibility"]
                + 0.12 * row["foresight_depth"]
                + 0.08 * row["signal_capacity"]
                - 0.16 * row["path_dependence_risk"]
            )

        option_value[t] = option_value[t - 1] + 0.04 * row["flexibility"] + 0.04 * row["foresight_depth"] - 0.06 * row["path_dependence_risk"]
        option_value[t] = np.clip(option_value[t], 0, 1.2)

        state[t] = state[t - 1] + gain / 4 - shock / 5 + option_value[t] / 45
        state[t] = np.clip(state[t], 0, 1.8)

    return state, option_value

simulation = pd.DataFrame({"time": time_steps})
option_simulation = pd.DataFrame({"time": time_steps})

for _, row in profiles.iterrows():
    path, options = simulate_strategy(row)
    simulation[row["strategy_name"]] = path
    option_simulation[row["strategy_name"]] = options

plt.figure(figsize=(11, 7))
for col in simulation.columns[1:]:
    plt.plot(simulation["time"], simulation[col], label=col)

plt.xlabel("Time Step")
plt.ylabel("Strategic Viability")
plt.title("Strategic Foresight Across Alternative Futures")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "strategic_foresight_simulation.png", dpi=160)
plt.close()

profiles.to_csv(TABLES / "advanced_foresight_profile_scores.csv", index=False)
signals.to_csv(TABLES / "advanced_horizon_signal_scores.csv", index=False)
drivers.to_csv(TABLES / "advanced_driver_uncertainty_scores.csv", index=False)
stress.to_csv(TABLES / "advanced_strategy_stress_test_scores.csv", index=False)
path_dep.to_csv(TABLES / "advanced_path_dependence_scores.csv", index=False)
pathways.to_csv(TABLES / "advanced_adaptive_pathway_scores.csv", index=False)
ethics.to_csv(TABLES / "advanced_futures_ethics_scores.csv", index=False)
simulation.to_csv(TABLES / "strategic_foresight_simulation.csv", index=False)
option_simulation.to_csv(TABLES / "strategic_option_value_simulation.csv", index=False)

print("Advanced strategic foresight analytics complete.")
print(f"Wrote: {FIGURES / 'future_viability_scores.png'}")
print(f"Wrote: {FIGURES / 'short_term_bias.png'}")
print(f"Wrote: {FIGURES / 'horizon_signal_priority.png'}")
print(f"Wrote: {FIGURES / 'critical_uncertainty_scores.png'}")
print(f"Wrote: {FIGURES / 'strategy_robustness_profiles.png'}")
print(f"Wrote: {FIGURES / 'path_dependence_lock_in_risk.png'}")
print(f"Wrote: {FIGURES / 'adaptive_pathway_scores.png'}")
print(f"Wrote: {FIGURES / 'futures_ethics_risk.png'}")
print(f"Wrote: {FIGURES / 'strategic_foresight_simulation.png'}")
