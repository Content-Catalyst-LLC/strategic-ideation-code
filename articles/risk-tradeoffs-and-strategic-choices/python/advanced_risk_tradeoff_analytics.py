#!/usr/bin/env python3
"""
Optional advanced analytics for Risk, Tradeoffs, and Strategic Choices.

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

options = pd.read_csv(RAW / "strategic_options.csv")
risks = pd.read_csv(RAW / "risk_exposures.csv")
opportunity_costs = pd.read_csv(RAW / "opportunity_costs.csv")
temporal = pd.read_csv(RAW / "temporal_tradeoffs.csv")
scenarios = pd.read_csv(RAW / "scenario_stress_tests.csv")
lock_in = pd.read_csv(RAW / "lock_in_reversibility.csv")
resources = pd.read_csv(RAW / "resource_allocation.csv")
values = pd.read_csv(RAW / "value_conflicts.csv")
ethics = pd.read_csv(RAW / "ethical_burdens.csv")

options["strategic_tradeoff_score"] = (
    0.18 * options["short_term_return"]
    + 0.20 * options["resilience"]
    + 0.16 * options["flexibility"]
    + 0.14 * options["stakeholder_legitimacy"]
    + 0.14 * options["opportunity_value"]
    - 0.18 * options["exposure"]
    + 0.08 * options["reversibility"]
    + 0.06 * options["implementation_readiness"]
    + 0.08 * options["ethical_resilience"]
    + 0.08 * options["learning_value"]
)

options["fragility_warning"] = (
    0.26 * options["exposure"]
    + 0.18 * (1 - options["resilience"])
    + 0.14 * (1 - options["flexibility"])
    + 0.12 * (1 - options["stakeholder_legitimacy"])
    + 0.12 * (1 - options["opportunity_value"])
    + 0.10 * (1 - options["reversibility"])
    + 0.08 * (1 - options["ethical_resilience"])
)

options.sort_values("strategic_tradeoff_score", ascending=True).plot(
    kind="barh",
    x="option_name",
    y="strategic_tradeoff_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Strategic Tradeoff Profile")
plt.xlabel("Profile score")
plt.ylabel("Option")
plt.tight_layout()
plt.savefig(FIGURES / "strategic_tradeoff_scores.png", dpi=160)
plt.close()

options.sort_values("fragility_warning", ascending=True).plot(
    kind="barh",
    x="option_name",
    y="fragility_warning",
    legend=False,
    figsize=(12, 8),
)
plt.title("Strategic Fragility Warning")
plt.xlabel("Warning")
plt.ylabel("Option")
plt.tight_layout()
plt.savefig(FIGURES / "strategic_fragility_warning.png", dpi=160)
plt.close()

risks["gross_exposure"] = (
    0.13 * risks["financial_exposure"]
    + 0.13 * risks["implementation_exposure"]
    + 0.12 * risks["reputation_exposure"]
    + 0.11 * risks["regulatory_exposure"]
    + 0.13 * risks["ethical_exposure"]
    + 0.14 * risks["systemic_exposure"]
    + 0.14 * risks["strategic_exposure"]
    + 0.10 * (1 - risks["absorptive_capacity"])
)
risks["net_exposure"] = risks["gross_exposure"] - 0.18 * risks["absorptive_capacity"]
risks = risks.merge(options[["option_id", "option_name"]], on="option_id", how="left")

risks.sort_values("net_exposure", ascending=True).plot(
    kind="barh",
    x="option_name",
    y="net_exposure",
    legend=False,
    figsize=(12, 8),
)
plt.title("Risk Exposure by Option")
plt.xlabel("Net exposure")
plt.ylabel("Option")
plt.tight_layout()
plt.savefig(FIGURES / "risk_exposure_scores.png", dpi=160)
plt.close()

opportunity_costs["opportunity_cost_score"] = (
    0.15 * opportunity_costs["capability_cost"]
    + 0.15 * opportunity_costs["learning_cost"]
    + 0.14 * opportunity_costs["flexibility_cost"]
    + 0.15 * opportunity_costs["preparedness_cost"]
    + 0.13 * opportunity_costs["legitimacy_cost"]
    + 0.12 * opportunity_costs["innovation_cost"]
    + 0.08 * opportunity_costs["delay_cost"]
    + 0.08 * (1 - opportunity_costs["visibility"])
)
opportunity_costs["hidden_cost_risk"] = opportunity_costs["opportunity_cost_score"] * (1 + (1 - opportunity_costs["visibility"]) * 0.35)
opportunity_costs = opportunity_costs.merge(options[["option_id", "option_name"]], on="option_id", how="left")

opportunity_costs.sort_values("hidden_cost_risk", ascending=True).plot(
    kind="barh",
    x="option_name",
    y="hidden_cost_risk",
    legend=False,
    figsize=(12, 8),
)
plt.title("Hidden Opportunity Cost Risk")
plt.xlabel("Hidden cost risk")
plt.ylabel("Option")
plt.tight_layout()
plt.savefig(FIGURES / "hidden_opportunity_cost_risk.png", dpi=160)
plt.close()

scenario_cols = [
    "stable_growth",
    "resource_constraint",
    "trust_crisis",
    "regulatory_shift",
    "system_disruption",
    "climate_or_environmental_stress",
    "implementation_delay",
]

scenarios["mean_performance"] = scenarios[scenario_cols].mean(axis=1)
scenarios["worst_case"] = scenarios[scenario_cols].min(axis=1)
scenarios["best_case"] = scenarios[scenario_cols].max(axis=1)
scenarios["volatility"] = scenarios[scenario_cols].std(axis=1)
scenarios["robustness_score"] = (
    0.40 * scenarios["worst_case"]
    + 0.32 * scenarios["mean_performance"]
    + 0.10 * scenarios["best_case"]
    - 0.18 * scenarios["volatility"]
)
scenarios = scenarios.merge(options[["option_id", "option_name"]], on="option_id", how="left")

scenarios.sort_values("robustness_score", ascending=True).plot(
    kind="barh",
    x="option_name",
    y="robustness_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Scenario Robustness Score")
plt.xlabel("Robustness")
plt.ylabel("Option")
plt.tight_layout()
plt.savefig(FIGURES / "scenario_robustness_scores.png", dpi=160)
plt.close()

scenario_long = scenarios.melt(
    id_vars=["option_name"],
    value_vars=scenario_cols,
    var_name="scenario",
    value_name="performance",
)

plt.figure(figsize=(11, 7))
for name in scenario_long["option_name"].unique():
    subset = scenario_long[scenario_long["option_name"] == name]
    plt.plot(subset["scenario"], subset["performance"], marker="o", label=name)
plt.title("Strategic Options Across Stress Scenarios")
plt.ylabel("Performance")
plt.xticks(rotation=25)
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "options_across_stress_scenarios.png", dpi=160)
plt.close()

lock_in["lock_in_score"] = (
    0.16 * lock_in["irreversibility"]
    + 0.15 * lock_in["switching_cost"]
    + 0.14 * lock_in["ecosystem_dependence"]
    + 0.12 * lock_in["contractual_constraint"]
    + 0.13 * lock_in["data_or_platform_dependence"]
    + 0.10 * lock_in["governance_constraint"]
    - 0.12 * lock_in["retained_flexibility"]
    - 0.08 * lock_in["exit_path_quality"]
)
lock_in = lock_in.merge(options[["option_id", "option_name"]], on="option_id", how="left")

lock_in.sort_values("lock_in_score", ascending=True).plot(
    kind="barh",
    x="option_name",
    y="lock_in_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Lock-In Score")
plt.xlabel("Lock-in")
plt.ylabel("Option")
plt.tight_layout()
plt.savefig(FIGURES / "lock_in_scores.png", dpi=160)
plt.close()

resources["resource_coherence"] = (
    0.14 * resources["budget_alignment"]
    + 0.14 * resources["staffing_alignment"]
    + 0.12 * resources["executive_attention"]
    + 0.12 * resources["measurement_alignment"]
    + 0.13 * resources["contingency_reserve"]
    + 0.13 * resources["learning_budget"]
    + 0.12 * resources["stakeholder_review_budget"]
    + 0.10 * resources["declared_priority_match"]
)
resources = resources.merge(options[["option_id", "option_name"]], on="option_id", how="left")

resources.sort_values("resource_coherence", ascending=True).plot(
    kind="barh",
    x="option_name",
    y="resource_coherence",
    legend=False,
    figsize=(12, 8),
)
plt.title("Resource Coherence")
plt.xlabel("Coherence")
plt.ylabel("Option")
plt.tight_layout()
plt.savefig(FIGURES / "resource_coherence_scores.png", dpi=160)
plt.close()

value_cols = [
    "efficiency_pressure",
    "resilience_pressure",
    "equity_pressure",
    "speed_pressure",
    "legitimacy_pressure",
    "innovation_pressure",
    "control_pressure",
]
values["pressure_spread"] = values[value_cols].max(axis=1) - values[value_cols].min(axis=1)
values["value_conflict_intensity"] = (
    0.30 * values["pressure_spread"]
    + 0.20 * (1 - values["clarity_of_priority"])
    + 0.10 * values["efficiency_pressure"]
    + 0.10 * values["resilience_pressure"]
    + 0.10 * values["equity_pressure"]
    + 0.10 * values["legitimacy_pressure"]
    + 0.10 * values["innovation_pressure"]
)

values.sort_values("value_conflict_intensity", ascending=True).plot(
    kind="barh",
    x="value_conflict",
    y="value_conflict_intensity",
    legend=False,
    figsize=(12, 8),
)
plt.title("Value Conflict Intensity")
plt.xlabel("Intensity")
plt.ylabel("Conflict")
plt.tight_layout()
plt.savefig(FIGURES / "value_conflict_intensity.png", dpi=160)
plt.close()

ethics["ethical_burden_risk"] = (
    0.15 * ethics["benefit_concentration"]
    + 0.18 * ethics["burden_concentration"]
    + 0.13 * (1 - ethics["stakeholder_voice"])
    + 0.11 * (1 - ethics["transparency"])
    + 0.11 * (1 - ethics["redress_quality"])
    + 0.16 * ethics["future_generation_burden"]
    + 0.10 * (1 - ethics["distributional_review_quality"])
    + 0.06 * (1 - ethics["accountability_clarity"])
)

ethics.sort_values("ethical_burden_risk", ascending=True).plot(
    kind="barh",
    x="ethical_issue",
    y="ethical_burden_risk",
    legend=False,
    figsize=(12, 9),
)
plt.title("Ethical Burden Risk")
plt.xlabel("Risk")
plt.ylabel("Ethical issue")
plt.tight_layout()
plt.savefig(FIGURES / "ethical_burden_risk.png", dpi=160)
plt.close()

time_steps = np.arange(1, 41)
viability = pd.DataFrame({"time": time_steps})
option_value_pathway = pd.DataFrame({"time": time_steps})

for _, row in options.iterrows():
    state = np.zeros(len(time_steps))
    option_value_path = np.zeros(len(time_steps))
    state[0] = 1.0
    option_value_path[0] = row["opportunity_value"]

    for t in range(1, len(time_steps)):
        if t < 20:
            shock = 0.03
            gain = 0.18 * row["short_term_return"] + 0.06 * row["flexibility"]
        else:
            shock = 0.14
            gain = (
                0.10 * row["short_term_return"]
                + 0.16 * row["resilience"]
                + 0.12 * row["flexibility"]
                + 0.08 * option_value_path[t - 1]
                - 0.14 * row["exposure"]
            )

        option_value_path[t] = np.clip(option_value_path[t - 1] + 0.04 * row["flexibility"] - 0.05 * row["exposure"], 0, 1.2)
        state[t] = np.clip(state[t - 1] + gain / 4 - shock / 5, 0, 1.8)

    viability[row["option_name"]] = state
    option_value_pathway[row["option_name"]] = option_value_path

plt.figure(figsize=(11, 7))
for col in viability.columns[1:]:
    plt.plot(viability["time"], viability[col], label=col)
plt.xlabel("Time Step")
plt.ylabel("Strategic Viability")
plt.title("Risk, Tradeoffs, and Strategic Choice Simulation")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "risk_tradeoffs_simulation.png", dpi=160)
plt.close()

options.to_csv(TABLES / "advanced_strategic_tradeoff_scores.csv", index=False)
risks.to_csv(TABLES / "advanced_risk_exposure_scores.csv", index=False)
opportunity_costs.to_csv(TABLES / "advanced_opportunity_cost_scores.csv", index=False)
scenarios.to_csv(TABLES / "advanced_scenario_stress_test_scores.csv", index=False)
lock_in.to_csv(TABLES / "advanced_lock_in_scores.csv", index=False)
resources.to_csv(TABLES / "advanced_resource_coherence_scores.csv", index=False)
values.to_csv(TABLES / "advanced_value_conflict_scores.csv", index=False)
ethics.to_csv(TABLES / "advanced_ethical_burden_scores.csv", index=False)
viability.to_csv(TABLES / "risk_tradeoffs_simulation.csv", index=False)
option_value_pathway.to_csv(TABLES / "risk_tradeoffs_option_value_pathway.csv", index=False)

print("Advanced risk and tradeoff analytics complete.")
print(f"Wrote: {FIGURES / 'strategic_tradeoff_scores.png'}")
print(f"Wrote: {FIGURES / 'strategic_fragility_warning.png'}")
print(f"Wrote: {FIGURES / 'risk_exposure_scores.png'}")
print(f"Wrote: {FIGURES / 'hidden_opportunity_cost_risk.png'}")
print(f"Wrote: {FIGURES / 'scenario_robustness_scores.png'}")
print(f"Wrote: {FIGURES / 'options_across_stress_scenarios.png'}")
print(f"Wrote: {FIGURES / 'lock_in_scores.png'}")
print(f"Wrote: {FIGURES / 'resource_coherence_scores.png'}")
print(f"Wrote: {FIGURES / 'value_conflict_intensity.png'}")
print(f"Wrote: {FIGURES / 'ethical_burden_risk.png'}")
print(f"Wrote: {FIGURES / 'risk_tradeoffs_simulation.png'}")
