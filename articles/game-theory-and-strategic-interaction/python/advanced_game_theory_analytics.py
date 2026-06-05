#!/usr/bin/env python3
"""
Optional advanced analytics for Game Theory and Strategic Interaction.

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

profiles = pd.read_csv(RAW / "strategic_interaction_profiles.csv")
signals = pd.read_csv(RAW / "information_signals.csv")
equilibria = pd.read_csv(RAW / "equilibrium_diagnoses.csv")
cooperation = pd.read_csv(RAW / "cooperation_fragility.csv")
mechanisms = pd.read_csv(RAW / "mechanism_design.csv")
behavioral = pd.read_csv(RAW / "behavioral_game_theory.csv")
ethics = pd.read_csv(RAW / "ethics_power.csv")

profiles["strategic_interaction_score"] = (
    0.12 * profiles["rivalry"]
    + 0.18 * profiles["coordination_potential"]
    + 0.12 * profiles["information_asymmetry"]
    + 0.10 * profiles["retaliation_risk"]
    + 0.15 * profiles["institutional_support"]
    + 0.12 * profiles["behavioral_realism"]
    + 0.15 * profiles["mechanism_design_potential"]
    + 0.06 * profiles["ethical_complexity"]
)

profiles["cooperation_fragility"] = (
    0.22 * profiles["rivalry"]
    + 0.20 * profiles["retaliation_risk"]
    + 0.16 * profiles["information_asymmetry"]
    + 0.12 * profiles["ethical_complexity"]
    - 0.15 * profiles["institutional_support"]
    - 0.15 * profiles["coordination_potential"]
)

profiles["mechanism_opportunity"] = (
    0.30 * profiles["mechanism_design_potential"]
    + 0.18 * profiles["coordination_potential"]
    + 0.16 * profiles["information_asymmetry"]
    + 0.14 * profiles["ethical_complexity"]
    + 0.12 * profiles["institutional_support"]
    + 0.10 * profiles["behavioral_realism"]
)

profiles.sort_values("mechanism_opportunity", ascending=True).plot(
    kind="barh",
    x="setting_name",
    y="mechanism_opportunity",
    legend=False,
    figsize=(12, 8),
)
plt.title("Mechanism-Design Opportunity")
plt.xlabel("Opportunity score")
plt.ylabel("Setting")
plt.tight_layout()
plt.savefig(FIGURES / "mechanism_design_opportunity.png", dpi=160)
plt.close()

profiles.sort_values("cooperation_fragility", ascending=True).plot(
    kind="barh",
    x="setting_name",
    y="cooperation_fragility",
    legend=False,
    figsize=(12, 8),
)
plt.title("Cooperation Fragility")
plt.xlabel("Fragility")
plt.ylabel("Setting")
plt.tight_layout()
plt.savefig(FIGURES / "cooperation_fragility_by_setting.png", dpi=160)
plt.close()

signals["signal_strength"] = (
    0.18 * signals["credibility"]
    + 0.14 * signals["observability"]
    + 0.16 * signals["costliness"]
    - 0.12 * signals["ambiguity"]
    + 0.12 * signals["response_sensitivity"]
    - 0.12 * signals["misinterpretation_risk"]
    + 0.16 * signals["coordination_value"]
)

signals["response_risk"] = (
    0.24 * signals["response_sensitivity"]
    + 0.22 * signals["misinterpretation_risk"]
    + 0.18 * signals["ambiguity"]
    + 0.14 * (1 - signals["credibility"])
    + 0.12 * signals["observability"]
    + 0.10 * signals["costliness"]
)

signals.sort_values("response_risk", ascending=True).plot(
    kind="barh",
    x="signal_name",
    y="response_risk",
    legend=False,
    figsize=(12, 8),
)
plt.title("Signal Response and Misinterpretation Risk")
plt.xlabel("Risk")
plt.ylabel("Signal")
plt.tight_layout()
plt.savefig(FIGURES / "signal_response_risk.png", dpi=160)
plt.close()

equilibria["bad_equilibrium_risk"] = (
    0.18 * (1 - equilibria["desirability"])
    + 0.15 * equilibria["stability"]
    + 0.15 * (1 - equilibria["efficiency"])
    + 0.13 * (1 - equilibria["fairness"])
    + 0.10 * equilibria["exit_pressure"]
    + 0.12 * equilibria["coordination_barrier"]
    + 0.12 * equilibria["incentive_misalignment"]
    + 0.05 * equilibria["rule_change_need"]
)

equilibria.sort_values("bad_equilibrium_risk", ascending=True).plot(
    kind="barh",
    x="equilibrium_name",
    y="bad_equilibrium_risk",
    legend=False,
    figsize=(12, 8),
)
plt.title("Bad Equilibrium Risk")
plt.xlabel("Risk")
plt.ylabel("Equilibrium")
plt.tight_layout()
plt.savefig(FIGURES / "bad_equilibrium_risk.png", dpi=160)
plt.close()

cooperation["cooperation_fragility_score"] = (
    0.16 * (1 - cooperation["trust_level"])
    + 0.12 * (1 - cooperation["monitoring_quality"])
    + 0.18 * cooperation["defection_temptation"]
    + 0.10 * (1 - cooperation["retaliation_feasibility"])
    + 0.10 * (1 - cooperation["reputation_value"])
    + 0.12 * (1 - cooperation["reciprocity_quality"])
    + 0.12 * (1 - cooperation["enforcement_quality"])
    + 0.10 * (1 - cooperation["shared_upside"])
)

cooperation.sort_values("cooperation_fragility_score", ascending=True).plot(
    kind="barh",
    x="cooperation_need",
    y="cooperation_fragility_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Cooperation Fragility Score")
plt.xlabel("Fragility")
plt.ylabel("Cooperation need")
plt.tight_layout()
plt.savefig(FIGURES / "cooperation_fragility_scores.png", dpi=160)
plt.close()

mechanisms["mechanism_design_score"] = (
    0.15 * mechanisms["incentive_alignment"]
    + 0.13 * mechanisms["information_transparency"]
    + 0.13 * mechanisms["verification_quality"]
    + 0.13 * mechanisms["enforcement_quality"]
    + 0.12 * mechanisms["participation_quality"]
    + 0.13 * mechanisms["burden_distribution_quality"]
    + 0.11 * mechanisms["adaptability"]
    + 0.10 * mechanisms["implementation_feasibility"]
)

mechanisms.sort_values("mechanism_design_score", ascending=True).plot(
    kind="barh",
    x="mechanism_name",
    y="mechanism_design_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Mechanism Design Scores")
plt.xlabel("Score")
plt.ylabel("Mechanism")
plt.tight_layout()
plt.savefig(FIGURES / "mechanism_design_scores.png", dpi=160)
plt.close()

behavioral["behavioral_failure_risk"] = (
    0.18 * behavioral["bounded_reasoning_risk"]
    + 0.18 * behavioral["loss_aversion_risk"]
    + 0.16 * behavioral["legitimacy_sensitivity"]
    + 0.14 * behavioral["identity_salience"]
    + 0.12 * behavioral["fairness_salience"]
    + 0.12 * (1 - behavioral["trust_salience"])
    + 0.10 * (1 - behavioral["norm_strength"])
)

behavioral.sort_values("behavioral_failure_risk", ascending=True).plot(
    kind="barh",
    x="behavioral_factor",
    y="behavioral_failure_risk",
    legend=False,
    figsize=(12, 8),
)
plt.title("Behavioral Game-Theory Failure Risk")
plt.xlabel("Risk")
plt.ylabel("Behavioral factor")
plt.tight_layout()
plt.savefig(FIGURES / "behavioral_game_theory_risk.png", dpi=160)
plt.close()

ethics["ethics_power_risk"] = (
    0.16 * ethics["power_asymmetry"]
    + 0.13 * (1 - ethics["voice_quality"])
    + 0.13 * (1 - ethics["exit_option_quality"])
    + 0.12 * (1 - ethics["transparency"])
    + 0.16 * ethics["burden_shift_risk"]
    + 0.14 * ethics["manipulation_risk"]
    + 0.10 * (1 - ethics["legitimacy_quality"])
    + 0.06 * (1 - ethics["redress_quality"])
)

ethics.sort_values("ethics_power_risk", ascending=True).plot(
    kind="barh",
    x="ethical_issue",
    y="ethics_power_risk",
    legend=False,
    figsize=(12, 9),
)
plt.title("Ethics and Power Risk")
plt.xlabel("Risk")
plt.ylabel("Ethical issue")
plt.tight_layout()
plt.savefig(FIGURES / "ethics_power_risk.png", dpi=160)
plt.close()

time_steps = np.arange(1, 41)
stability = pd.DataFrame({"time": time_steps})
cooperation_path = pd.DataFrame({"time": time_steps})

for _, row in profiles.iterrows():
    state = np.zeros(len(time_steps))
    coop = np.zeros(len(time_steps))
    state[0] = 0.60
    coop[0] = row["coordination_potential"]

    for t in range(1, len(time_steps)):
        coop[t] = coop[t - 1] + (
            0.04 * row["institutional_support"]
            + 0.04 * row["mechanism_design_potential"]
            + 0.03 * row["behavioral_realism"]
            - 0.05 * row["retaliation_risk"]
            - 0.03 * row["rivalry"]
        )
        coop[t] = np.clip(coop[t], 0, 1.2)

        gain = 0.16 * coop[t] + 0.14 * row["institutional_support"] + 0.12 * row["mechanism_design_potential"]
        friction = 0.18 * row["retaliation_risk"] + 0.10 * row["rivalry"]
        state[t] = state[t - 1] + gain / 5 - friction / 5
        state[t] = np.clip(state[t], 0, 1.6)

    stability[row["setting_name"]] = state
    cooperation_path[row["setting_name"]] = coop

plt.figure(figsize=(11, 7))
for col in stability.columns[1:]:
    plt.plot(stability["time"], stability[col], label=col)
plt.xlabel("Time Step")
plt.ylabel("Strategic Stability")
plt.title("Strategic Interaction and Equilibrium Shifts")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "strategic_interaction_simulation.png", dpi=160)
plt.close()

profiles.to_csv(TABLES / "advanced_strategic_interaction_scores.csv", index=False)
signals.to_csv(TABLES / "advanced_signal_response_scores.csv", index=False)
equilibria.to_csv(TABLES / "advanced_equilibrium_diagnosis_scores.csv", index=False)
cooperation.to_csv(TABLES / "advanced_cooperation_fragility_scores.csv", index=False)
mechanisms.to_csv(TABLES / "advanced_mechanism_design_scores.csv", index=False)
behavioral.to_csv(TABLES / "advanced_behavioral_game_theory_scores.csv", index=False)
ethics.to_csv(TABLES / "advanced_ethics_power_scores.csv", index=False)
stability.to_csv(TABLES / "strategic_interaction_simulation.csv", index=False)
cooperation_path.to_csv(TABLES / "cooperation_pathway_simulation.csv", index=False)

print("Advanced game theory analytics complete.")
print(f"Wrote: {FIGURES / 'mechanism_design_opportunity.png'}")
print(f"Wrote: {FIGURES / 'cooperation_fragility_by_setting.png'}")
print(f"Wrote: {FIGURES / 'signal_response_risk.png'}")
print(f"Wrote: {FIGURES / 'bad_equilibrium_risk.png'}")
print(f"Wrote: {FIGURES / 'cooperation_fragility_scores.png'}")
print(f"Wrote: {FIGURES / 'mechanism_design_scores.png'}")
print(f"Wrote: {FIGURES / 'behavioral_game_theory_risk.png'}")
print(f"Wrote: {FIGURES / 'ethics_power_risk.png'}")
print(f"Wrote: {FIGURES / 'strategic_interaction_simulation.png'}")
