#!/usr/bin/env python3
"""
Optional advanced analytics for Adaptive Strategy and Iteration.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- adaptive strategy score chart
- over-adaptation risk chart
- feedback response priority chart
- assumption revision need chart
- trigger condition chart
- whiplash risk chart
- portfolio balance chart
- adaptive strategy simulation
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

profiles = pd.read_csv(RAW / "strategy_profiles.csv")
signals = pd.read_csv(RAW / "feedback_signals.csv")
assumptions = pd.read_csv(RAW / "assumption_register.csv")
triggers = pd.read_csv(RAW / "trigger_conditions.csv")
timing = pd.read_csv(RAW / "timing_responsiveness.csv")
portfolio = pd.read_csv(RAW / "portfolio_balance.csv")

profiles["adaptive_strategy_score"] = (
    0.13 * profiles["flexibility"]
    + 0.15 * profiles["learning_capacity"]
    + 0.09 * profiles["exploration"]
    + 0.11 * profiles["exploitation_balance"]
    + 0.15 * profiles["coherence"]
    + 0.13 * profiles["feedback_intelligence"]
    + 0.10 * profiles["governance"]
    + 0.08 * profiles["systems_awareness"]
    + 0.06 * profiles["learning_memory"]
)

profiles["over_adaptation_risk"] = (
    0.20 * profiles["flexibility"] * (1 - profiles["coherence"])
    + 0.18 * (1 - profiles["governance"])
    + 0.16 * (1 - profiles["feedback_intelligence"])
    + 0.14 * (1 - profiles["learning_capacity"])
    + 0.12 * (1 - profiles["exploitation_balance"])
    + 0.10 * (1 - profiles["learning_memory"])
    + 0.10 * (1 - profiles["systems_awareness"])
)

profiles.sort_values("adaptive_strategy_score", ascending=True).plot(
    kind="barh",
    x="strategy_name",
    y="adaptive_strategy_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Adaptive Strategy Score")
plt.xlabel("Score")
plt.ylabel("Strategy")
plt.tight_layout()
plt.savefig(FIGURES / "adaptive_strategy_scores.png", dpi=160)
plt.close()

profiles.sort_values("over_adaptation_risk", ascending=True).plot(
    kind="barh",
    x="strategy_name",
    y="over_adaptation_risk",
    legend=False,
    figsize=(12, 8),
)
plt.title("Over-Adaptation Risk")
plt.xlabel("Risk")
plt.ylabel("Strategy")
plt.tight_layout()
plt.savefig(FIGURES / "over_adaptation_risk.png", dpi=160)
plt.close()

signals["response_priority"] = (
    0.18 * signals["signal_strength"]
    + 0.16 * signals["decision_relevance"]
    + 0.16 * signals["stakeholder_impact"]
    + 0.16 * signals["systems_relevance"]
    + 0.12 * signals["delay_risk"]
    - 0.14 * signals["noise_risk"]
    + 0.08 * signals["interpretation_quality"]
)

signals.sort_values("response_priority", ascending=True).plot(
    kind="barh",
    x="signal_id",
    y="response_priority",
    legend=False,
    figsize=(12, 8),
)
plt.title("Feedback Signal Response Priority")
plt.xlabel("Priority")
plt.ylabel("Signal")
plt.tight_layout()
plt.savefig(FIGURES / "feedback_signal_response_priority.png", dpi=160)
plt.close()

assumptions["revision_need"] = (
    0.24 * assumptions["uncertainty"]
    + 0.24 * assumptions["consequence"]
    + 0.22 * assumptions["decay_risk"]
    - 0.16 * assumptions["evidence_strength"]
    - 0.08 * assumptions["revision_readiness"]
    - 0.06 * assumptions["owner_clarity"]
)

assumptions.sort_values("revision_need", ascending=True).plot(
    kind="barh",
    x="assumption_id",
    y="revision_need",
    legend=False,
    figsize=(12, 8),
)
plt.title("Assumption Revision Need")
plt.xlabel("Revision need")
plt.ylabel("Assumption")
plt.tight_layout()
plt.savefig(FIGURES / "assumption_revision_need.png", dpi=160)
plt.close()

triggers["trigger_condition_score"] = (
    0.15 * triggers["trigger_clarity"]
    + 0.15 * triggers["evidence_threshold"]
    + 0.16 * triggers["decision_path_clarity"]
    + 0.13 * triggers["response_speed_fit"]
    + 0.13 * triggers["ethical_safeguards"]
    + 0.13 * triggers["authority_clarity"]
    + 0.15 * triggers["monitoring_quality"]
)

triggers.sort_values("trigger_condition_score", ascending=True).plot(
    kind="barh",
    x="trigger_name",
    y="trigger_condition_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Trigger Condition Scores")
plt.xlabel("Score")
plt.ylabel("Trigger")
plt.tight_layout()
plt.savefig(FIGURES / "trigger_condition_scores.png", dpi=160)
plt.close()

timing["whiplash_risk"] = (
    0.25 * timing["response_speed"] * (1 - timing["noise_filtering"])
    + 0.20 * (1 - timing["signal_interpretation"])
    + 0.18 * (1 - timing["stability_preservation"])
    + 0.15 * (1 - timing["revision_cadence"])
    + 0.12 * (1 - timing["stakeholder_communication"])
    + 0.10 * (1 - timing["delay_awareness"])
)

timing.sort_values("whiplash_risk", ascending=True).plot(
    kind="barh",
    x="timing_issue",
    y="whiplash_risk",
    legend=False,
    figsize=(12, 8),
)
plt.title("Strategic Whiplash Risk")
plt.xlabel("Risk")
plt.ylabel("Timing issue")
plt.tight_layout()
plt.savefig(FIGURES / "strategic_whiplash_risk.png", dpi=160)
plt.close()

portfolio["portfolio_balance_score"] = (
    0.15 * portfolio["exploration_strength"]
    + 0.15 * portfolio["exploitation_strength"]
    + 0.18 * portfolio["balance_quality"]
    + 0.14 * portfolio["option_value"]
    + 0.13 * portfolio["resource_discipline"]
    + 0.13 * portfolio["focus_quality"]
    + 0.12 * portfolio["transition_path_quality"]
)

portfolio.sort_values("portfolio_balance_score", ascending=True).plot(
    kind="barh",
    x="portfolio_name",
    y="portfolio_balance_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Exploration and Exploitation Portfolio Balance")
plt.xlabel("Score")
plt.ylabel("Portfolio")
plt.tight_layout()
plt.savefig(FIGURES / "exploration_exploitation_portfolio_balance.png", dpi=160)
plt.close()

time_steps = np.arange(1, 41)

def simulate_strategy(row):
    state = np.zeros(len(time_steps))
    state[0] = 1.0
    for t in range(1, len(time_steps)):
        if t < 20:
            environmental_shock = 0.03
            learning_gain = (
                0.14 * row["coherence"]
                + 0.08 * row["learning_capacity"]
                + 0.06 * row["feedback_intelligence"]
            )
        else:
            environmental_shock = 0.14
            learning_gain = (
                0.10 * row["coherence"]
                + 0.16 * row["flexibility"]
                + 0.18 * row["learning_capacity"]
                + 0.12 * row["feedback_intelligence"]
                + 0.08 * row["systems_awareness"]
            )

        over_adaptation_penalty = (
            0.10 * row["flexibility"] * (1 - row["coherence"])
            + 0.08 * (1 - row["governance"])
            + 0.06 * (1 - row["feedback_intelligence"])
        )

        governance_support = 0.08 * row["governance"]
        systems_support = 0.06 * row["systems_awareness"]

        state[t] = (
            state[t - 1]
            + learning_gain / 4
            + governance_support / 5
            + systems_support / 5
            - environmental_shock / 5
            - over_adaptation_penalty / 4
        )
        state[t] = np.clip(state[t], 0, 1.8)
    return state

simulation = pd.DataFrame({"time": time_steps})
for _, row in profiles.iterrows():
    simulation[row["strategy_name"]] = simulate_strategy(row)

plt.figure(figsize=(11, 7))
for col in simulation.columns[1:]:
    plt.plot(simulation["time"], simulation[col], label=col)
plt.xlabel("Time Step")
plt.ylabel("Strategic Viability")
plt.title("Adaptive Strategy Over Time")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "adaptive_strategy_simulation.png", dpi=160)
plt.close()

profiles.to_csv(TABLES / "advanced_adaptive_strategy_profile_scores.csv", index=False)
signals.to_csv(TABLES / "advanced_feedback_signal_scores.csv", index=False)
assumptions.to_csv(TABLES / "advanced_assumption_revision_scores.csv", index=False)
triggers.to_csv(TABLES / "advanced_trigger_condition_scores.csv", index=False)
timing.to_csv(TABLES / "advanced_timing_responsiveness_scores.csv", index=False)
portfolio.to_csv(TABLES / "advanced_portfolio_balance_scores.csv", index=False)
simulation.to_csv(TABLES / "adaptive_strategy_simulation.csv", index=False)

print("Advanced adaptive strategy analytics complete.")
print(f"Wrote: {FIGURES / 'adaptive_strategy_scores.png'}")
print(f"Wrote: {FIGURES / 'over_adaptation_risk.png'}")
print(f"Wrote: {FIGURES / 'feedback_signal_response_priority.png'}")
print(f"Wrote: {FIGURES / 'assumption_revision_need.png'}")
print(f"Wrote: {FIGURES / 'trigger_condition_scores.png'}")
print(f"Wrote: {FIGURES / 'strategic_whiplash_risk.png'}")
print(f"Wrote: {FIGURES / 'exploration_exploitation_portfolio_balance.png'}")
print(f"Wrote: {FIGURES / 'adaptive_strategy_simulation.png'}")
