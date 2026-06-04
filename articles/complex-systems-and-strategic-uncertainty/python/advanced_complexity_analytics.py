#!/usr/bin/env python3
"""
Optional advanced analytics for complex systems and strategic uncertainty.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- complexity profile chart
- linear planning risk chart
- scenario risk chart
- adaptive option chart
- early-warning indicator chart
- complex system uncertainty simulation chart
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

environments = pd.read_csv(RAW / "complexity_environments.csv")
scenarios = pd.read_csv(RAW / "scenario_robustness.csv")
options = pd.read_csv(RAW / "adaptive_options.csv")
indicators = pd.read_csv(RAW / "early_warning_indicators.csv")

environments["complexity_profile_score"] = (
    0.13 * environments["interdependence"]
    + 0.13 * environments["nonlinearity"]
    + 0.14 * environments["feedback_intensity"]
    + 0.12 * environments["adaptation_pressure"]
    + 0.11 * environments["path_dependence"]
    + 0.10 * environments["boundary_ambiguity"]
    + 0.10 * environments["emergence_potential"]
    + 0.09 * environments["deep_uncertainty"]
    + 0.09 * environments["scenario_need"]
    + 0.09 * environments["learning_capacity_need"]
)

environments["linear_planning_risk"] = (
    0.20 * environments["nonlinearity"]
    + 0.20 * environments["feedback_intensity"]
    + 0.18 * environments["adaptation_pressure"]
    + 0.16 * environments["deep_uncertainty"]
    + 0.14 * environments["boundary_ambiguity"]
    + 0.12 * environments["emergence_potential"]
)

environments.sort_values("complexity_profile_score", ascending=True).plot(
    kind="barh",
    x="environment_name",
    y="complexity_profile_score",
    legend=False,
    figsize=(12, 9),
)
plt.title("Complexity Profile Scores")
plt.xlabel("Complexity profile score")
plt.ylabel("Environment")
plt.tight_layout()
plt.savefig(FIGURES / "complexity_profile_scores.png", dpi=160)
plt.close()

environments.sort_values("linear_planning_risk", ascending=True).plot(
    kind="barh",
    x="environment_name",
    y="linear_planning_risk",
    legend=False,
    figsize=(12, 9),
)
plt.title("Linear Planning Risk")
plt.xlabel("Risk score")
plt.ylabel("Environment")
plt.tight_layout()
plt.savefig(FIGURES / "linear_planning_risk.png", dpi=160)
plt.close()

scenarios["scenario_risk_score"] = (
    0.14 * scenarios["plausibility"]
    + 0.16 * scenarios["severity"]
    + 0.12 * scenarios["novelty"]
    + 0.16 * scenarios["strategic_disruption"]
    + 0.14 * scenarios["robustness_gap"]
    - 0.10 * scenarios["signal_visibility"]
    - 0.10 * scenarios["preparation_quality"]
    - 0.08 * scenarios["response_flexibility"]
)

scenarios.sort_values("scenario_risk_score", ascending=True).plot(
    kind="barh",
    x="scenario_name",
    y="scenario_risk_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Scenario Risk Scores")
plt.xlabel("Scenario risk score")
plt.ylabel("Scenario")
plt.tight_layout()
plt.savefig(FIGURES / "scenario_risk_scores.png", dpi=160)
plt.close()

options["adaptive_option_value_score"] = (
    0.14 * options["robustness"]
    + 0.15 * options["option_value"]
    + 0.12 * options["reversibility"]
    + 0.14 * options["learning_value"]
    + 0.12 * options["downside_protection"]
    - 0.10 * options["resource_intensity"]
    - 0.08 * options["time_to_learning"]
    + 0.12 * options["strategic_coherence"]
    - 0.08 * options["legitimacy_requirement"]
    + 0.10 * options["evidence_readiness"]
)

options.sort_values("adaptive_option_value_score", ascending=True).plot(
    kind="barh",
    x="option_name",
    y="adaptive_option_value_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Adaptive Option Value Scores")
plt.xlabel("Option value score")
plt.ylabel("Option")
plt.tight_layout()
plt.savefig(FIGURES / "adaptive_option_value_scores.png", dpi=160)
plt.close()

indicators["indicator_quality_score"] = (
    0.15 * indicators["leading_quality"]
    + 0.13 * indicators["visibility"]
    + 0.13 * indicators["reliability"]
    + 0.13 * indicators["timeliness"]
    + 0.12 * indicators["sensitivity"]
    + 0.14 * indicators["decision_linkage"]
    - 0.08 * indicators["false_positive_risk"]
    - 0.08 * indicators["monitoring_cost"]
)

indicators.sort_values("indicator_quality_score", ascending=True).plot(
    kind="barh",
    x="indicator_name",
    y="indicator_quality_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Early-Warning Indicator Quality Scores")
plt.xlabel("Indicator quality score")
plt.ylabel("Indicator")
plt.tight_layout()
plt.savefig(FIGURES / "early_warning_indicator_scores.png", dpi=160)
plt.close()

# Simulate strategic uncertainty in complex systems.
np.random.seed(42)
time_steps = np.arange(1, 41)

def simulate_environment(
    interdependence,
    feedback,
    adaptation,
    path_dependence,
    deep_uncertainty,
    initial_state=0.50,
):
    state = np.zeros(len(time_steps))
    state[0] = initial_state

    for t in range(1, len(time_steps)):
        nonlinear_component = 0.12 * interdependence * state[t - 1] * (1 - state[t - 1])
        feedback_component = 0.10 * feedback * state[t - 1]
        adaptation_component = 0.08 * adaptation * np.sin(t / 5)
        memory_component = 0.05 * path_dependence * state[t - 1]
        shock = np.random.normal(0, 0.015 * deep_uncertainty)

        state[t] = (
            state[t - 1]
            + nonlinear_component
            + feedback_component / 5
            + adaptation_component / 5
            + memory_component / 6
            + shock
        )

        state[t] = np.clip(state[t], 0, 1.8)

    return state

simulation = pd.DataFrame({"time": time_steps})

for _, row in environments.iterrows():
    if row["environment_id"] in {"ENV001", "ENV002", "ENV003", "ENV004", "ENV005"}:
        simulation[row["environment_name"]] = simulate_environment(
            row["interdependence"],
            row["feedback_intensity"],
            row["adaptation_pressure"],
            row["path_dependence"],
            row["deep_uncertainty"],
        )

plt.figure(figsize=(11, 7))
for col in simulation.columns[1:]:
    plt.plot(simulation["time"], simulation[col], label=col)
plt.xlabel("Time Step")
plt.ylabel("System State")
plt.title("Strategic Uncertainty in Complex Systems")
plt.legend()
plt.tight_layout()
plt.savefig(FIGURES / "complex_system_uncertainty_simulation.png", dpi=160)
plt.close()

environments.to_csv(TABLES / "advanced_complexity_profile_scores.csv", index=False)
scenarios.to_csv(TABLES / "advanced_scenario_risk_scores.csv", index=False)
options.to_csv(TABLES / "advanced_adaptive_option_scores.csv", index=False)
indicators.to_csv(TABLES / "advanced_early_warning_indicator_scores.csv", index=False)
simulation.to_csv(TABLES / "advanced_complex_system_uncertainty_simulation.csv", index=False)

print("Advanced complexity analytics complete.")
print(f"Wrote: {FIGURES / 'complexity_profile_scores.png'}")
print(f"Wrote: {FIGURES / 'linear_planning_risk.png'}")
print(f"Wrote: {FIGURES / 'scenario_risk_scores.png'}")
print(f"Wrote: {FIGURES / 'adaptive_option_value_scores.png'}")
print(f"Wrote: {FIGURES / 'early_warning_indicator_scores.png'}")
print(f"Wrote: {FIGURES / 'complex_system_uncertainty_simulation.png'}")
