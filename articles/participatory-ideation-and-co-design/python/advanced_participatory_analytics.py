#!/usr/bin/env python3
"""
Optional advanced analytics for Participatory Ideation and Co-Design.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- participation quality chart
- tokenism/extraction risk chart
- representation gap chart
- influence boundary chart
- accessibility support chart
- power risk chart
- participatory idea-quality simulation
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

systems = pd.read_csv(RAW / "participation_systems.csv")
stakeholders = pd.read_csv(RAW / "stakeholders.csv")
boundaries = pd.read_csv(RAW / "influence_boundaries.csv")
access = pd.read_csv(RAW / "accessibility_supports.csv")
power = pd.read_csv(RAW / "power_risks.csv")

systems["participation_quality_score"] = (
    0.13 * systems["representation"]
    + 0.15 * systems["influence"]
    + 0.11 * systems["accessibility"]
    + 0.11 * systems["reciprocity"]
    + 0.13 * systems["power_awareness"]
    + 0.12 * systems["knowledge_integration"]
    + 0.11 * systems["decision_linkage"]
    + 0.10 * systems["accountability"]
    + 0.04 * systems["learning_memory"]
)

systems["tokenism_extraction_risk"] = (
    0.16 * (1 - systems["influence"])
    + 0.14 * (1 - systems["decision_linkage"])
    + 0.14 * (1 - systems["accountability"])
    + 0.13 * (1 - systems["reciprocity"])
    + 0.13 * (1 - systems["power_awareness"])
    + 0.11 * (1 - systems["representation"])
    + 0.10 * (1 - systems["accessibility"])
    + 0.09 * (1 - systems["learning_memory"])
)

systems.sort_values("participation_quality_score", ascending=True).plot(
    kind="barh",
    x="system_name",
    y="participation_quality_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Participatory Ideation Quality")
plt.xlabel("Quality score")
plt.ylabel("System")
plt.tight_layout()
plt.savefig(FIGURES / "participation_quality_scores.png", dpi=160)
plt.close()

systems.sort_values("tokenism_extraction_risk", ascending=True).plot(
    kind="barh",
    x="system_name",
    y="tokenism_extraction_risk",
    legend=False,
    figsize=(12, 8),
)
plt.title("Tokenism and Extraction Risk")
plt.xlabel("Risk")
plt.ylabel("System")
plt.tight_layout()
plt.savefig(FIGURES / "tokenism_extraction_risk.png", dpi=160)
plt.close()

stakeholders["representation_need"] = (
    0.20 * stakeholders["affectedness"]
    + 0.11 * (1 - stakeholders["decision_power"])
    + 0.12 * stakeholders["implementation_role"]
    + 0.18 * stakeholders["knowledge_value"]
    + 0.16 * stakeholders["usual_exclusion_risk"]
)
stakeholders["representation_score"] = (
    0.55 * stakeholders["participation_depth"]
    + 0.45 * stakeholders["representation_quality"]
)
stakeholders["representation_gap"] = stakeholders["representation_need"] - stakeholders["representation_score"]

stakeholders.sort_values("representation_gap", ascending=True).plot(
    kind="barh",
    x="stakeholder_group",
    y="representation_gap",
    legend=False,
    figsize=(12, 8),
)
plt.title("Stakeholder Representation Gaps")
plt.xlabel("Need minus current representation")
plt.ylabel("Stakeholder group")
plt.tight_layout()
plt.savefig(FIGURES / "stakeholder_representation_gaps.png", dpi=160)
plt.close()

boundaries["influence_boundary_score"] = (
    0.16 * boundaries["problem_frame_open"]
    + 0.14 * boundaries["idea_generation_open"]
    + 0.14 * boundaries["prototype_open"]
    + 0.13 * boundaries["evaluation_criteria_open"]
    + 0.11 * boundaries["implementation_open"]
    + 0.10 * boundaries["governance_open"]
    + 0.11 * boundaries["constraint_transparency"]
    + 0.11 * boundaries["decision_authority_clarity"]
)

boundaries.sort_values("influence_boundary_score", ascending=True).plot(
    kind="barh",
    x="participation_purpose",
    y="influence_boundary_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Influence Boundary Scores")
plt.xlabel("Influence score")
plt.ylabel("Participation purpose")
plt.tight_layout()
plt.savefig(FIGURES / "influence_boundary_scores.png", dpi=160)
plt.close()

access["accessibility_support_score"] = (
    0.13 * access["language_access"]
    + 0.14 * access["disability_access"]
    + 0.12 * access["schedule_flexibility"]
    + 0.11 * access["technology_access"]
    + 0.13 * access["compensation_support"]
    + 0.12 * access["care_transport_support"]
    + 0.13 * access["psychological_safety"]
    + 0.12 * access["cultural_fit"]
)

access.sort_values("accessibility_support_score", ascending=True).plot(
    kind="barh",
    x="access_design",
    y="accessibility_support_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Accessibility Support Scores")
plt.xlabel("Access score")
plt.ylabel("Access design")
plt.tight_layout()
plt.savefig(FIGURES / "accessibility_support_scores.png", dpi=160)
plt.close()

power["power_risk_score"] = (
    0.13 * power["invitation_bias"]
    + 0.15 * power["framing_control"]
    + 0.11 * power["language_barrier"]
    + 0.13 * power["dominant_voice_risk"]
    + 0.16 * power["interpretive_capture"]
    + 0.16 * power["decision_capture"]
    + 0.10 * power["participant_risk"]
    - 0.06 * power["mitigation_quality"]
)

power.sort_values("power_risk_score", ascending=True).plot(
    kind="barh",
    x="power_issue",
    y="power_risk_score",
    legend=False,
    figsize=(12, 9),
)
plt.title("Power Risk Scores")
plt.xlabel("Power risk")
plt.ylabel("Power issue")
plt.tight_layout()
plt.savefig(FIGURES / "power_risk_scores.png", dpi=160)
plt.close()

time_steps = np.arange(1, 41)

def simulate_system(row):
    quality = np.zeros(len(time_steps))
    quality[0] = 0.30
    for t in range(1, len(time_steps)):
        learning_gain = (
            0.12 * row["representation"]
            + 0.15 * row["influence"]
            + 0.10 * row["accessibility"]
            + 0.10 * row["reciprocity"]
            + 0.13 * row["power_awareness"]
            + 0.12 * row["knowledge_integration"]
            + 0.10 * row["decision_linkage"]
            + 0.10 * row["accountability"]
            + 0.05 * row["learning_memory"]
        )
        tokenism_penalty = (
            0.08 * (1 - row["influence"])
            + 0.06 * (1 - row["decision_linkage"])
            + 0.06 * (1 - row["accountability"])
        )
        extraction_penalty = 0.05 * (1 - row["reciprocity"])
        power_penalty = 0.05 * (1 - row["power_awareness"])
        disturbance = 0.06 * (1 - row["accessibility"]) * np.sin(t / 4)

        quality[t] = (
            quality[t - 1]
            + learning_gain / 5
            - tokenism_penalty / 5
            - extraction_penalty / 5
            - power_penalty / 5
            + disturbance / 10
        )
        quality[t] = np.clip(quality[t], 0, 1.8)
    return quality

simulation = pd.DataFrame({"time": time_steps})
for _, row in systems.iterrows():
    simulation[row["system_name"]] = simulate_system(row)

plt.figure(figsize=(11, 7))
for col in simulation.columns[1:]:
    plt.plot(simulation["time"], simulation[col], label=col)
plt.xlabel("Participation Cycle")
plt.ylabel("Strategic Idea Quality")
plt.title("Participatory Ideation and Idea Quality Over Time")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig(FIGURES / "participatory_idea_quality_simulation.png", dpi=160)
plt.close()

systems.to_csv(TABLES / "advanced_participation_system_profile_scores.csv", index=False)
stakeholders.to_csv(TABLES / "advanced_stakeholder_representation_scores.csv", index=False)
boundaries.to_csv(TABLES / "advanced_influence_boundary_scores.csv", index=False)
access.to_csv(TABLES / "advanced_accessibility_support_scores.csv", index=False)
power.to_csv(TABLES / "advanced_power_risk_scores.csv", index=False)
simulation.to_csv(TABLES / "participatory_idea_quality_simulation.csv", index=False)

print("Advanced participatory ideation analytics complete.")
print(f"Wrote: {FIGURES / 'participation_quality_scores.png'}")
print(f"Wrote: {FIGURES / 'tokenism_extraction_risk.png'}")
print(f"Wrote: {FIGURES / 'stakeholder_representation_gaps.png'}")
print(f"Wrote: {FIGURES / 'influence_boundary_scores.png'}")
print(f"Wrote: {FIGURES / 'accessibility_support_scores.png'}")
print(f"Wrote: {FIGURES / 'power_risk_scores.png'}")
print(f"Wrote: {FIGURES / 'participatory_idea_quality_simulation.png'}")
