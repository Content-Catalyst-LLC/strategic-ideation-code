#!/usr/bin/env python3
"""
Optional advanced analytics for leverage points in systems change.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- leverage profile chart
- governance need chart
- leverage vs governance scatter
- tipping readiness chart
- early-warning indicator chart
- leverage-point simulation chart
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

leverage = pd.read_csv(RAW / "leverage_points.csv")
thresholds = pd.read_csv(RAW / "tipping_thresholds.csv")
indicators = pd.read_csv(RAW / "early_warning_indicators.csv")

leverage["leverage_profile_score"] = (
    0.06 * leverage["implementation_ease"]
    + 0.16 * leverage["structural_depth"]
    + 0.14 * leverage["system_sensitivity"]
    + 0.13 * leverage["feedback_influence"]
    + 0.11 * leverage["information_effect"]
    + 0.13 * leverage["rule_power"]
    + 0.13 * leverage["goal_alignment"]
    + 0.08 * leverage["paradigm_relevance"]
    + 0.14 * leverage["transformative_potential"]
    + 0.08 * leverage["learning_capacity"]
    - 0.06 * leverage["unintended_consequence_risk"]
)

leverage["governance_need_score"] = (
    0.26 * leverage["legitimacy_requirement"]
    + 0.24 * leverage["unintended_consequence_risk"]
    + 0.22 * leverage["transformative_potential"]
    + 0.14 * (1 - leverage["implementation_ease"])
    + 0.14 * leverage["paradigm_relevance"]
)

leverage.sort_values("leverage_profile_score", ascending=True).plot(
    kind="barh",
    x="intervention_name",
    y="leverage_profile_score",
    legend=False,
    figsize=(12, 9),
)
plt.title("Leverage Profile Scores")
plt.xlabel("Leverage profile score")
plt.ylabel("Intervention")
plt.tight_layout()
plt.savefig(FIGURES / "leverage_profile_scores.png", dpi=160)
plt.close()

leverage.sort_values("governance_need_score", ascending=True).plot(
    kind="barh",
    x="intervention_name",
    y="governance_need_score",
    legend=False,
    figsize=(12, 9),
)
plt.title("Governance Need Scores")
plt.xlabel("Governance need")
plt.ylabel("Intervention")
plt.tight_layout()
plt.savefig(FIGURES / "governance_need_scores.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 7))
plt.scatter(leverage["governance_need_score"], leverage["leverage_profile_score"])
for _, row in leverage.iterrows():
    plt.annotate(row["leverage_id"], (row["governance_need_score"], row["leverage_profile_score"]))
plt.xlabel("Governance Need")
plt.ylabel("Leverage Profile")
plt.title("Leverage Profile vs Governance Need")
plt.tight_layout()
plt.savefig(FIGURES / "leverage_vs_governance.png", dpi=160)
plt.close()

thresholds["distance_to_threshold"] = (thresholds["threshold_level"] - thresholds["current_progress"]).clip(lower=0)
thresholds["tipping_readiness_score"] = (
    0.12 * (1 - thresholds["distance_to_threshold"])
    + 0.14 * thresholds["diffusion_potential"]
    + 0.16 * thresholds["self_reinforcement_strength"]
    + 0.14 * thresholds["complementary_condition_quality"]
    + 0.14 * thresholds["legitimacy_support"]
    + 0.14 * thresholds["infrastructure_support"]
    + 0.12 * thresholds["monitoring_quality"]
)

thresholds.sort_values("tipping_readiness_score", ascending=True).plot(
    kind="barh",
    x="threshold_name",
    y="tipping_readiness_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Positive Tipping Readiness Scores")
plt.xlabel("Tipping readiness")
plt.ylabel("Threshold")
plt.tight_layout()
plt.savefig(FIGURES / "tipping_readiness_scores.png", dpi=160)
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
plt.xlabel("Indicator quality")
plt.ylabel("Indicator")
plt.tight_layout()
plt.savefig(FIGURES / "early_warning_indicator_scores.png", dpi=160)
plt.close()

# Simulate leverage-point interventions over time.
time_steps = np.arange(1, 41)

def simulate_intervention(depth, feedback, information_effect, rule_power, delay, learning_capacity, initial_state=0.40):
    state = np.zeros(len(time_steps))
    state[0] = initial_state

    for t in range(1, len(time_steps)):
        early_gain = (
            0.05 * depth
            + 0.05 * feedback
            + 0.04 * information_effect
            + 0.03 * rule_power
            - 0.05 * delay
        )

        late_gain = (
            0.14 * depth
            + 0.12 * feedback
            + 0.08 * information_effect
            + 0.10 * rule_power
            + 0.08 * learning_capacity
            - 0.03 * delay
        )

        gain = early_gain if t < 15 else late_gain
        state[t] = state[t - 1] + gain / 5
        state[t] = np.clip(state[t], 0, 1.8)

    return state

simulation = pd.DataFrame({"time": time_steps})

for _, row in leverage.iterrows():
    if row["leverage_id"] in {"L001", "L004", "L005", "L006", "L007", "L008"}:
        simulation[row["intervention_name"]] = simulate_intervention(
            row["structural_depth"],
            row["feedback_influence"],
            row["information_effect"],
            row["rule_power"],
            1 - row["implementation_ease"],
            row["learning_capacity"],
        )

plt.figure(figsize=(11, 7))
for col in simulation.columns[1:]:
    plt.plot(simulation["time"], simulation[col], label=col)
plt.xlabel("Time Step")
plt.ylabel("System Shift Magnitude")
plt.title("Leverage-Point Interventions Over Time")
plt.legend()
plt.tight_layout()
plt.savefig(FIGURES / "leverage_point_interventions_simulation.png", dpi=160)
plt.close()

leverage.to_csv(TABLES / "advanced_leverage_profile_scores.csv", index=False)
thresholds.to_csv(TABLES / "advanced_tipping_readiness_scores.csv", index=False)
indicators.to_csv(TABLES / "advanced_indicator_quality_scores.csv", index=False)
simulation.to_csv(TABLES / "advanced_leverage_intervention_simulation.csv", index=False)

print("Advanced leverage analytics complete.")
print(f"Wrote: {FIGURES / 'leverage_profile_scores.png'}")
print(f"Wrote: {FIGURES / 'governance_need_scores.png'}")
print(f"Wrote: {FIGURES / 'leverage_vs_governance.png'}")
print(f"Wrote: {FIGURES / 'tipping_readiness_scores.png'}")
print(f"Wrote: {FIGURES / 'early_warning_indicator_scores.png'}")
print(f"Wrote: {FIGURES / 'leverage_point_interventions_simulation.png'}")
