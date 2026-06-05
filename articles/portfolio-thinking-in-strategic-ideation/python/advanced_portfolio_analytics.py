#!/usr/bin/env python3
"""
Optional advanced analytics for Portfolio Thinking in Strategic Ideation.

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

ideas = pd.read_csv(RAW / "strategic_ideas.csv")
targets = pd.read_csv(RAW / "portfolio_targets.csv")
risk_learning = pd.read_csv(RAW / "risk_learning_profiles.csv")
capacity = pd.read_csv(RAW / "capacity_load.csv")
dependencies = pd.read_csv(RAW / "dependencies.csv")
time_horizons = pd.read_csv(RAW / "time_horizons.csv")
ethics_power = pd.read_csv(RAW / "ethics_power.csv")
governance = pd.read_csv(RAW / "governance_review.csv")

ideas["portfolio_contribution"] = (
    0.17 * ideas["impact"]
    + 0.16 * ideas["strategic_fit"]
    + 0.15 * ideas["learning_value"]
    + 0.15 * ideas["option_value"]
    + 0.12 * ideas["ethical_resilience"]
    + 0.10 * ideas["evidence_strength"]
    + 0.08 * ideas["governance_readiness"]
    - 0.10 * ideas["risk"]
    - 0.08 * ideas["capacity_demand"]
    - 0.04 * (ideas["dependency_count"] / 6).clip(upper=1)
)

ideas["overload_warning"] = (
    0.30 * ideas["capacity_demand"]
    + 0.24 * ideas["risk"]
    + 0.14 * (1 - ideas["strategic_fit"])
    + 0.12 * (1 - ideas["ethical_resilience"])
    + 0.10 * (1 - ideas["option_value"])
    + 0.10 * (ideas["dependency_count"] / 6).clip(upper=1)
)

ideas.sort_values("portfolio_contribution", ascending=True).plot(
    kind="barh",
    x="idea_name",
    y="portfolio_contribution",
    legend=False,
    figsize=(12, 8),
)
plt.title("Strategic Idea Portfolio Contribution")
plt.xlabel("Contribution")
plt.ylabel("Idea")
plt.tight_layout()
plt.savefig(FIGURES / "portfolio_contribution_scores.png", dpi=160)
plt.close()

ideas.sort_values("overload_warning", ascending=True).plot(
    kind="barh",
    x="idea_name",
    y="overload_warning",
    legend=False,
    figsize=(12, 8),
)
plt.title("Portfolio Overload Warning")
plt.xlabel("Warning")
plt.ylabel("Idea")
plt.tight_layout()
plt.savefig(FIGURES / "portfolio_overload_warning.png", dpi=160)
plt.close()

role_counts = ideas.groupby("role").size().reset_index(name="current_count")
role_counts["current_share"] = role_counts["current_count"] / role_counts["current_count"].sum()
role_balance = targets.merge(role_counts, on="role", how="left").fillna({"current_count": 0, "current_share": 0})
role_balance["absolute_gap"] = (role_balance["current_share"] - role_balance["target_share"]).abs()
role_balance.sort_values("absolute_gap", ascending=False).to_csv(TABLES / "advanced_role_balance.csv", index=False)

plt.figure(figsize=(10, 6))
plt.bar(role_balance["role"], role_balance["current_share"], label="Current share")
plt.plot(role_balance["role"], role_balance["target_share"], marker="o", label="Target share")
plt.title("Portfolio Role Balance")
plt.ylabel("Share")
plt.xticks(rotation=35, ha="right")
plt.legend()
plt.tight_layout()
plt.savefig(FIGURES / "portfolio_role_balance.png", dpi=160)
plt.close()

risk_learning["exposure_score"] = (
    0.20 * risk_learning["implementation_risk"]
    + 0.22 * risk_learning["strategic_risk"]
    + 0.18 * risk_learning["ethical_risk"]
    + 0.18 * risk_learning["systemic_risk"]
    + 0.22 * risk_learning["opportunity_cost"]
)
risk_learning["learning_strength"] = (
    0.36 * risk_learning["learning_quality"]
    + 0.24 * risk_learning["assumption_clarity"]
    + 0.22 * (1 - risk_learning["evidence_gap"])
    + 0.18 * (1 - risk_learning["exposure_score"])
)
risk_learning = risk_learning.merge(ideas[["idea_id", "idea_name"]], on="idea_id", how="left")

plt.figure(figsize=(9, 7))
plt.scatter(risk_learning["exposure_score"], risk_learning["learning_strength"])
for _, row in risk_learning.iterrows():
    plt.annotate(row["idea_id"], (row["exposure_score"], row["learning_strength"]))
plt.xlabel("Exposure score")
plt.ylabel("Learning strength")
plt.title("Risk-Learning Portfolio Map")
plt.tight_layout()
plt.savefig(FIGURES / "risk_learning_portfolio_map.png", dpi=160)
plt.close()

capacity["gross_demand"] = (
    0.16 * capacity["budget_demand"]
    + 0.16 * capacity["staff_demand"]
    + 0.14 * capacity["leadership_attention"]
    + 0.14 * capacity["technical_capacity_demand"]
    + 0.14 * capacity["governance_bandwidth"]
    + 0.12 * capacity["stakeholder_absorption"]
    + 0.10 * capacity["communication_load"]
)
capacity["capacity_load"] = capacity["gross_demand"] / capacity["available_capacity"].clip(lower=0.01)
capacity = capacity.merge(ideas[["idea_id", "idea_name"]], on="idea_id", how="left")

capacity.sort_values("capacity_load", ascending=True).plot(
    kind="barh",
    x="idea_name",
    y="capacity_load",
    legend=False,
    figsize=(12, 8),
)
plt.axvline(1.0, linestyle="--")
plt.title("Capacity Load by Idea")
plt.xlabel("Capacity load")
plt.ylabel("Idea")
plt.tight_layout()
plt.savefig(FIGURES / "capacity_load_scores.png", dpi=160)
plt.close()

dependencies["sequence_priority"] = (
    0.30 * dependencies["dependency_strength"]
    + 0.26 * dependencies["sequencing_urgency"]
    + 0.24 * dependencies["readiness_gap"]
    + 0.20 * dependencies["criticality"]
)
dependencies.to_csv(TABLES / "advanced_dependency_sequence_scores.csv", index=False)

time_horizons["future_value"] = (
    0.20 * time_horizons["medium_term_value"]
    + 0.30 * time_horizons["long_term_value"]
    + 0.24 * time_horizons["intergenerational_value"]
    + 0.16 * time_horizons["deferred_value"]
    + 0.10 * time_horizons["short_term_value"]
)
time_horizons = time_horizons.merge(ideas[["idea_id", "idea_name"]], on="idea_id", how="left")

time_horizons.sort_values("future_value", ascending=True).plot(
    kind="barh",
    x="idea_name",
    y="future_value",
    legend=False,
    figsize=(12, 8),
)
plt.title("Future Value by Idea")
plt.xlabel("Future value")
plt.ylabel("Idea")
plt.tight_layout()
plt.savefig(FIGURES / "future_value_scores.png", dpi=160)
plt.close()

ethics_power["power_risk"] = (
    0.18 * ethics_power["sponsor_power"]
    + 0.18 * (1 - ethics_power["affected_stakeholder_voice"])
    + 0.16 * ethics_power["benefit_concentration"]
    + 0.18 * ethics_power["burden_concentration"]
    + 0.12 * (1 - ethics_power["transparency"])
    + 0.10 * (1 - ethics_power["redress_quality"])
    + 0.08 * (1 - ethics_power["long_term_responsibility"])
)
ethics_power = ethics_power.merge(ideas[["idea_id", "idea_name"]], on="idea_id", how="left")

ethics_power.sort_values("power_risk", ascending=True).plot(
    kind="barh",
    x="idea_name",
    y="power_risk",
    legend=False,
    figsize=(12, 8),
)
plt.title("Ethics and Power Risk")
plt.xlabel("Risk")
plt.ylabel("Idea")
plt.tight_layout()
plt.savefig(FIGURES / "ethics_power_risk.png", dpi=160)
plt.close()

governance["governance_score"] = (
    0.12 * governance["entry_rule_quality"]
    + 0.12 * governance["review_cadence_quality"]
    + 0.13 * governance["pruning_rule_quality"]
    + 0.14 * governance["evidence_standard_quality"]
    + 0.13 * governance["decision_rights_clarity"]
    + 0.12 * governance["escalation_path_quality"]
    + 0.12 * governance["decision_memory_quality"]
    + 0.12 * governance["portfolio_visibility"]
)
governance = governance.merge(ideas[["idea_id", "idea_name"]], on="idea_id", how="left")

governance.sort_values("governance_score", ascending=True).plot(
    kind="barh",
    x="idea_name",
    y="governance_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Portfolio Governance Score")
plt.xlabel("Governance score")
plt.ylabel("Idea")
plt.tight_layout()
plt.savefig(FIGURES / "portfolio_governance_scores.png", dpi=160)
plt.close()

time_steps = np.arange(1, 41)
portfolios = {
    "Incremental Heavy Portfolio": {
        "impact": 0.62, "risk": 0.34, "learning": 0.38, "option_value": 0.32,
        "capacity_demand": 0.46, "strategic_fit": 0.74, "ethical_resilience": 0.58
    },
    "Balanced Adaptive Portfolio": {
        "impact": 0.70, "risk": 0.46, "learning": 0.72, "option_value": 0.76,
        "capacity_demand": 0.58, "strategic_fit": 0.76, "ethical_resilience": 0.72
    },
    "Transformational Bet Portfolio": {
        "impact": 0.88, "risk": 0.78, "learning": 0.66, "option_value": 0.54,
        "capacity_demand": 0.86, "strategic_fit": 0.68, "ethical_resilience": 0.48
    },
    "Exploration Heavy Portfolio": {
        "impact": 0.58, "risk": 0.54, "learning": 0.88, "option_value": 0.82,
        "capacity_demand": 0.62, "strategic_fit": 0.60, "ethical_resilience": 0.66
    },
    "Resilience and Legitimacy Portfolio": {
        "impact": 0.60, "risk": 0.36, "learning": 0.62, "option_value": 0.70,
        "capacity_demand": 0.56, "strategic_fit": 0.72, "ethical_resilience": 0.86
    }
}

def simulate_portfolio(profile):
    state = np.zeros(len(time_steps))
    adaptive_capacity = np.zeros(len(time_steps))
    state[0] = 1.0
    adaptive_capacity[0] = profile["option_value"]

    for t in range(1, len(time_steps)):
        if t < 18:
            environment_shock = 0.03
            performance_gain = (
                0.18 * profile["impact"]
                + 0.10 * profile["strategic_fit"]
                - 0.08 * profile["capacity_demand"]
            )
        else:
            environment_shock = 0.14
            performance_gain = (
                0.12 * profile["impact"]
                + 0.14 * profile["learning"]
                + 0.14 * profile["option_value"]
                + 0.10 * adaptive_capacity[t - 1]
                + 0.10 * profile["ethical_resilience"]
                - 0.14 * profile["risk"]
                - 0.10 * profile["capacity_demand"]
            )

        adaptive_capacity[t] = np.clip(
            adaptive_capacity[t - 1]
            + 0.05 * profile["learning"]
            + 0.04 * profile["option_value"]
            + 0.03 * profile["ethical_resilience"]
            - 0.04 * profile["capacity_demand"]
            - 0.03 * profile["risk"],
            0,
            1.2,
        )

        state[t] = np.clip(state[t - 1] + performance_gain / 4 - environment_shock / 5, 0, 1.8)

    return state, adaptive_capacity

performance_df = pd.DataFrame({"time": time_steps})
capacity_df = pd.DataFrame({"time": time_steps})

for name, profile in portfolios.items():
    performance, adaptive = simulate_portfolio(profile)
    performance_df[name] = performance
    capacity_df[name] = adaptive

plt.figure(figsize=(11, 7))
for col in performance_df.columns[1:]:
    plt.plot(performance_df["time"], performance_df[col], label=col)
plt.xlabel("Time Step")
plt.ylabel("Portfolio Viability")
plt.title("Strategic Idea Portfolio Performance")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "portfolio_performance_simulation.png", dpi=160)
plt.close()

ideas.to_csv(TABLES / "advanced_portfolio_idea_scores.csv", index=False)
risk_learning.to_csv(TABLES / "advanced_risk_learning_scores.csv", index=False)
capacity.to_csv(TABLES / "advanced_capacity_load_scores.csv", index=False)
time_horizons.to_csv(TABLES / "advanced_time_horizon_scores.csv", index=False)
ethics_power.to_csv(TABLES / "advanced_ethics_power_scores.csv", index=False)
governance.to_csv(TABLES / "advanced_governance_review_scores.csv", index=False)
performance_df.to_csv(TABLES / "portfolio_performance_simulation.csv", index=False)
capacity_df.to_csv(TABLES / "portfolio_adaptive_capacity_simulation.csv", index=False)

print("Advanced portfolio analytics complete.")
print(f"Wrote: {FIGURES / 'portfolio_contribution_scores.png'}")
print(f"Wrote: {FIGURES / 'portfolio_overload_warning.png'}")
print(f"Wrote: {FIGURES / 'portfolio_role_balance.png'}")
print(f"Wrote: {FIGURES / 'risk_learning_portfolio_map.png'}")
print(f"Wrote: {FIGURES / 'capacity_load_scores.png'}")
print(f"Wrote: {FIGURES / 'future_value_scores.png'}")
print(f"Wrote: {FIGURES / 'ethics_power_risk.png'}")
print(f"Wrote: {FIGURES / 'portfolio_governance_scores.png'}")
print(f"Wrote: {FIGURES / 'portfolio_performance_simulation.png'}")
