#!/usr/bin/env python3
"""
Optional advanced analytics for second-order effects and unintended consequences.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- second-order risk chart
- false-success risk chart
- burden risk chart
- fragility chart
- indicator quality chart
- second-order simulation chart
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

interventions = pd.read_csv(RAW / "interventions.csv")
burdens = pd.read_csv(RAW / "burden_shifts.csv")
fragility = pd.read_csv(RAW / "fragility_risks.csv")
indicators = pd.read_csv(RAW / "early_warning_indicators.csv")

interventions["second_order_risk_score"] = (
    0.16 * interventions["adaptation_pressure"]
    + 0.15 * interventions["feedback_amplification"]
    + 0.14 * interventions["delay_risk"]
    + 0.15 * interventions["burden_shift_risk"]
    + 0.14 * interventions["gaming_risk"]
    + 0.16 * interventions["long_term_fragility"]
    - 0.10 * interventions["learning_capacity"]
    - 0.06 * interventions["stakeholder_legitimacy"]
    - 0.06 * interventions["strategic_reversibility"]
)

interventions["false_success_risk"] = (
    0.26 * interventions["first_order_gain"]
    + 0.20 * interventions["long_term_fragility"]
    + 0.16 * interventions["delay_risk"]
    + 0.14 * interventions["gaming_risk"]
    + 0.12 * interventions["burden_shift_risk"]
    - 0.16 * interventions["learning_capacity"]
)

interventions.sort_values("second_order_risk_score", ascending=True).plot(
    kind="barh",
    x="intervention_name",
    y="second_order_risk_score",
    legend=False,
    figsize=(12, 9),
)
plt.title("Second-Order Risk Scores")
plt.xlabel("Second-order risk")
plt.ylabel("Intervention")
plt.tight_layout()
plt.savefig(FIGURES / "second_order_risk_scores.png", dpi=160)
plt.close()

interventions.sort_values("false_success_risk", ascending=True).plot(
    kind="barh",
    x="intervention_name",
    y="false_success_risk",
    legend=False,
    figsize=(12, 9),
)
plt.title("False First-Order Success Risk")
plt.xlabel("False-success risk")
plt.ylabel("Intervention")
plt.tight_layout()
plt.savefig(FIGURES / "false_success_risk_scores.png", dpi=160)
plt.close()

burdens["burden_risk_score"] = (
    0.16 * burdens["hidden_cost"]
    + 0.15 * burdens["administrative_load"]
    + 0.13 * burdens["emotional_load"]
    + 0.14 * burdens["risk_transfer"]
    + 0.14 * burdens["equity_risk"]
    - 0.14 * burdens["visibility_to_decision_makers"]
    - 0.14 * burdens["participatory_review_quality"]
)

burdens.sort_values("burden_risk_score", ascending=True).plot(
    kind="barh",
    x="burden_location",
    y="burden_risk_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Burden-Shift Risk Scores")
plt.xlabel("Burden risk")
plt.ylabel("Burden location")
plt.tight_layout()
plt.savefig(FIGURES / "burden_shift_risk_scores.png", dpi=160)
plt.close()

fragility["fragility_score"] = (
    0.14 * fragility["slack_reduction"]
    + 0.13 * fragility["redundancy_reduction"]
    + 0.13 * fragility["trust_erosion"]
    + 0.13 * fragility["option_closure"]
    + 0.14 * fragility["dependency_creation"]
    + 0.14 * fragility["recovery_capacity_loss"]
    + 0.13 * fragility["stress_exposure"]
    - 0.12 * fragility["monitoring_quality"]
)

fragility.sort_values("fragility_score", ascending=True).plot(
    kind="barh",
    x="fragility_type",
    y="fragility_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Fragility Risk Scores")
plt.xlabel("Fragility score")
plt.ylabel("Fragility type")
plt.tight_layout()
plt.savefig(FIGURES / "fragility_risk_scores.png", dpi=160)
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

# Second-order effects over time simulation.
time_steps = np.arange(1, 41)

def simulate_intervention(first_gain, adaptation, fragility, feedback, burden_shift, learning_capacity, initial_state=0.40):
    state = np.zeros(len(time_steps))
    state[0] = initial_state

    for t in range(1, len(time_steps)):
        if t < 12:
            gain = 0.18 * first_gain
        else:
            gain = (
                0.08 * first_gain
                - 0.12 * adaptation
                - 0.14 * fragility
                + 0.06 * feedback
                - 0.08 * burden_shift
                + 0.10 * learning_capacity
            )

        state[t] = state[t - 1] + gain / 5
        state[t] = np.clip(state[t], 0, 1.8)

    return state

simulation = pd.DataFrame({"time": time_steps})

for _, row in interventions.iterrows():
    if row["intervention_id"] in {"I001", "I002", "I003", "I004", "I007", "I008"}:
        simulation[row["intervention_name"]] = simulate_intervention(
            row["first_order_gain"],
            row["adaptation_pressure"],
            row["long_term_fragility"],
            row["feedback_amplification"],
            row["burden_shift_risk"],
            row["learning_capacity"],
        )

plt.figure(figsize=(11, 7))
for col in simulation.columns[1:]:
    plt.plot(simulation["time"], simulation[col], label=col)
plt.xlabel("Time Step")
plt.ylabel("System Outcome")
plt.title("Second-Order Effects Over Time")
plt.legend()
plt.tight_layout()
plt.savefig(FIGURES / "second_order_effects_simulation.png", dpi=160)
plt.close()

interventions.to_csv(TABLES / "advanced_second_order_scores.csv", index=False)
burdens.to_csv(TABLES / "advanced_burden_shift_scores.csv", index=False)
fragility.to_csv(TABLES / "advanced_fragility_scores.csv", index=False)
indicators.to_csv(TABLES / "advanced_indicator_quality_scores.csv", index=False)
simulation.to_csv(TABLES / "advanced_second_order_effects_simulation.csv", index=False)

print("Advanced second-order analytics complete.")
print(f"Wrote: {FIGURES / 'second_order_risk_scores.png'}")
print(f"Wrote: {FIGURES / 'false_success_risk_scores.png'}")
print(f"Wrote: {FIGURES / 'burden_shift_risk_scores.png'}")
print(f"Wrote: {FIGURES / 'fragility_risk_scores.png'}")
print(f"Wrote: {FIGURES / 'early_warning_indicator_scores.png'}")
print(f"Wrote: {FIGURES / 'second_order_effects_simulation.png'}")
