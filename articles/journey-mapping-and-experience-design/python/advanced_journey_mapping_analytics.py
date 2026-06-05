#!/usr/bin/env python3
"""
Optional advanced analytics for Journey Mapping and Experience Design.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- journey profile chart
- redesign need chart
- stage friction chart
- transition risk chart
- accessibility dignity risk chart
- service blueprint risk chart
- accumulated friction simulation
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

contexts = pd.read_csv(RAW / "journey_contexts.csv")
stages_df = pd.read_csv(RAW / "journey_stages.csv")
transitions = pd.read_csv(RAW / "transitions.csv")
accessibility = pd.read_csv(RAW / "accessibility_dignity.csv")
blueprints = pd.read_csv(RAW / "service_blueprint.csv")

contexts["journey_profile_score"] = (
    0.15 * contexts["clarity"]
    + 0.12 * contexts["emotional_confidence"]
    - 0.18 * contexts["friction"]
    + 0.14 * contexts["transition_quality"]
    + 0.12 * contexts["accessibility"]
    + 0.12 * contexts["trust"]
    + 0.10 * contexts["completion_support"]
    + 0.10 * contexts["backstage_alignment"]
    + 0.07 * contexts["measurement_quality"]
)

contexts["redesign_need_score"] = (
    0.22 * contexts["friction"]
    + 0.16 * (1 - contexts["transition_quality"])
    + 0.14 * (1 - contexts["accessibility"])
    + 0.13 * (1 - contexts["trust"])
    + 0.12 * (1 - contexts["clarity"])
    + 0.11 * (1 - contexts["backstage_alignment"])
    + 0.07 * (1 - contexts["completion_support"])
    + 0.05 * (1 - contexts["measurement_quality"])
)

contexts.sort_values("journey_profile_score", ascending=True).plot(
    kind="barh",
    x="journey_name",
    y="journey_profile_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Journey Experience Profile Scores")
plt.xlabel("Profile score")
plt.ylabel("Journey")
plt.tight_layout()
plt.savefig(FIGURES / "journey_profile_scores.png", dpi=160)
plt.close()

contexts.sort_values("redesign_need_score", ascending=True).plot(
    kind="barh",
    x="journey_name",
    y="redesign_need_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Journey Redesign Need")
plt.xlabel("Need")
plt.ylabel("Journey")
plt.tight_layout()
plt.savefig(FIGURES / "redesign_need_scores.png", dpi=160)
plt.close()

stages_df["accumulated_friction_score"] = (
    0.13 * stages_df["time_cost"]
    + 0.14 * stages_df["cognitive_load"]
    + 0.14 * stages_df["emotional_cost"]
    + 0.14 * stages_df["trust_risk"]
    + 0.12 * stages_df["accessibility_burden"]
    + 0.13 * stages_df["uncertainty"]
    + 0.10 * stages_df["workaround_dependency"]
    + 0.10 * stages_df["dropoff_risk"]
)

stages_df.sort_values("accumulated_friction_score", ascending=True).plot(
    kind="barh",
    x="stage_name",
    y="accumulated_friction_score",
    legend=False,
    figsize=(12, 9),
)
plt.title("Stage-Level Accumulated Friction")
plt.xlabel("Friction")
plt.ylabel("Stage")
plt.tight_layout()
plt.savefig(FIGURES / "stage_friction_scores.png", dpi=160)
plt.close()

transitions["transition_risk_score"] = (
    0.15 * transitions["context_loss"]
    + 0.13 * transitions["ownership_ambiguity"]
    + 0.12 * transitions["delay_risk"]
    + 0.13 * transitions["repetition_required"]
    + 0.14 * transitions["status_gap"]
    + 0.08 * transitions["privacy_risk"]
    + 0.13 * transitions["user_coordination_labor"]
    + 0.12 * transitions["transition_criticality"]
)

transitions.sort_values("transition_risk_score", ascending=True).plot(
    kind="barh",
    x="transition_id",
    y="transition_risk_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Transition Risk Scores")
plt.xlabel("Risk")
plt.ylabel("Transition")
plt.tight_layout()
plt.savefig(FIGURES / "transition_risk_scores.png", dpi=160)
plt.close()

accessibility["accessibility_dignity_score"] = (
    0.14 * accessibility["language_access"]
    + 0.16 * accessibility["disability_access"]
    + 0.12 * accessibility["device_access"]
    + 0.13 * accessibility["literacy_support"]
    + 0.11 * accessibility["time_flexibility"]
    + 0.16 * accessibility["dignity_protection"]
    + 0.12 * accessibility["recovery_path_quality"]
    - 0.12 * accessibility["equity_risk"]
)
accessibility["accessibility_dignity_risk"] = 1 - accessibility["accessibility_dignity_score"].clip(0, 1)

accessibility.sort_values("accessibility_dignity_risk", ascending=True).plot(
    kind="barh",
    x="access_issue",
    y="accessibility_dignity_risk",
    legend=False,
    figsize=(12, 9),
)
plt.title("Accessibility and Dignity Risk")
plt.xlabel("Risk")
plt.ylabel("Access issue")
plt.tight_layout()
plt.savefig(FIGURES / "accessibility_dignity_risk.png", dpi=160)
plt.close()

blueprints["service_blueprint_score"] = (
    0.14 * blueprints["dependency_quality"]
    + 0.14 * blueprints["data_continuity"]
    + 0.12 * blueprints["role_clarity"]
    + 0.12 * blueprints["workflow_fit"]
    + 0.10 * blueprints["staff_capacity"]
    + 0.12 * blueprints["governance_alignment"]
    + 0.12 * blueprints["feedback_loop_quality"]
    - 0.14 * blueprints["implementation_risk"]
)
blueprints["service_blueprint_risk"] = 1 - blueprints["service_blueprint_score"].clip(0, 1)

blueprints.sort_values("service_blueprint_risk", ascending=True).plot(
    kind="barh",
    x="visible_experience",
    y="service_blueprint_risk",
    legend=False,
    figsize=(12, 9),
)
plt.title("Service Blueprint Dependency Risk")
plt.xlabel("Risk")
plt.ylabel("Visible experience")
plt.tight_layout()
plt.savefig(FIGURES / "service_blueprint_risk.png", dpi=160)
plt.close()

stage_steps = np.arange(1, 11)

def simulate(row):
    state = np.zeros(len(stage_steps))
    state[0] = 0.80
    for t in range(1, len(stage_steps)):
        gain = (
            0.10 * row["clarity"]
            + 0.08 * row["transition_quality"]
            + 0.08 * row["completion_support"]
            + 0.07 * row["accessibility"]
            + 0.07 * row["trust"]
        )
        burden = 0.12 * row["friction"]
        transition_penalty = 0.05 * (1 - row["transition_quality"])
        access_penalty = 0.04 * (1 - row["accessibility"])
        state[t] = np.clip(
            state[t - 1] + gain / 5 - burden / 5 - transition_penalty / 5 - access_penalty / 5,
            0,
            1.5,
        )
    return state

simulation = pd.DataFrame({"stage": stage_steps})
for _, row in contexts.iterrows():
    simulation[row["journey_name"]] = simulate(row)

plt.figure(figsize=(11, 7))
for col in simulation.columns[1:]:
    plt.plot(simulation["stage"], simulation[col], marker="o", label=col)
plt.xlabel("Journey Stage")
plt.ylabel("Experience Quality")
plt.title("Accumulated Friction Across Journey Stages")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "accumulated_friction_simulation.png", dpi=160)
plt.close()

contexts.to_csv(TABLES / "advanced_journey_profile_scores.csv", index=False)
stages_df.to_csv(TABLES / "advanced_stage_friction_scores.csv", index=False)
transitions.to_csv(TABLES / "advanced_transition_risk_scores.csv", index=False)
accessibility.to_csv(TABLES / "advanced_accessibility_dignity_scores.csv", index=False)
blueprints.to_csv(TABLES / "advanced_service_blueprint_scores.csv", index=False)
simulation.to_csv(TABLES / "accumulated_friction_simulation.csv", index=False)

print("Advanced journey mapping analytics complete.")
print(f"Wrote: {FIGURES / 'journey_profile_scores.png'}")
print(f"Wrote: {FIGURES / 'redesign_need_scores.png'}")
print(f"Wrote: {FIGURES / 'stage_friction_scores.png'}")
print(f"Wrote: {FIGURES / 'transition_risk_scores.png'}")
print(f"Wrote: {FIGURES / 'accessibility_dignity_risk.png'}")
print(f"Wrote: {FIGURES / 'service_blueprint_risk.png'}")
print(f"Wrote: {FIGURES / 'accumulated_friction_simulation.png'}")
