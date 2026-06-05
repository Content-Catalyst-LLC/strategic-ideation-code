#!/usr/bin/env python3
"""
Optional advanced analytics for theory of change and strategic logic.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- strategic logic chart
- theory link risk chart
- mechanism clarity vs evidence chart
- actor response risk chart
- system feedback risk chart
- prototype test score chart
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
links = pd.read_csv(RAW / "theory_links.csv")
actors = pd.read_csv(RAW / "actor_response.csv")
feedback = pd.read_csv(RAW / "system_feedback.csv")
prototypes = pd.read_csv(RAW / "prototype_tests.csv")

ideas["strategic_logic_score"] = (
    0.14 * ideas["problem_frame_quality"]
    + 0.17 * ideas["mechanism_clarity"]
    + 0.12 * ideas["strategic_alignment"]
    + 0.11 * ideas["implementation_feasibility"]
    + 0.12 * ideas["stakeholder_legitimacy"]
    - 0.10 * ideas["system_complexity"]
    + 0.13 * ideas["learning_value"]
    + 0.11 * ideas["reversibility"]
)

ideas.sort_values("strategic_logic_score", ascending=True).plot(
    kind="barh",
    x="idea_name",
    y="strategic_logic_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Strategic Logic Scores")
plt.xlabel("Strategic logic")
plt.ylabel("Idea")
plt.tight_layout()
plt.savefig(FIGURES / "strategic_logic_scores.png", dpi=160)
plt.close()

links["link_risk_score"] = (
    0.16 * (1 - links["mechanism_clarity"])
    + 0.18 * (1 - links["evidence_strength"])
    + 0.13 * links["actor_dependency"]
    + 0.11 * links["capacity_dependency"]
    + 0.14 * links["system_dependency"]
    + 0.12 * links["ethical_dependency"]
    + 0.16 * links["failure_consequence"]
)

links.sort_values("link_risk_score", ascending=True).plot(
    kind="barh",
    x="link_id",
    y="link_risk_score",
    legend=False,
    figsize=(12, 9),
)
plt.title("Theory-of-Change Link Risk")
plt.xlabel("Link risk")
plt.ylabel("Link")
plt.tight_layout()
plt.savefig(FIGURES / "theory_link_risk_scores.png", dpi=160)
plt.close()

plt.figure(figsize=(10, 8))
plt.scatter(links["evidence_strength"], links["mechanism_clarity"])
for _, row in links.iterrows():
    plt.annotate(row["link_id"], (row["evidence_strength"], row["mechanism_clarity"]))
plt.xlabel("Evidence strength")
plt.ylabel("Mechanism clarity")
plt.title("Mechanism Clarity vs Evidence Strength")
plt.tight_layout()
plt.savefig(FIGURES / "mechanism_clarity_vs_evidence.png", dpi=160)
plt.close()

actors["actor_response_risk"] = (
    0.16 * actors["response_dependency"]
    - 0.12 * actors["incentive_alignment"]
    + 0.14 * (1 - actors["trust_condition"])
    + 0.12 * (1 - actors["capacity_condition"])
    + 0.15 * actors["burden_risk"]
    + 0.13 * actors["resistance_risk"]
    - 0.08 * actors["participation_quality"]
    + 0.10 * actors["knowledge_value"]
)

actors.sort_values("actor_response_risk", ascending=True).plot(
    kind="barh",
    x="actor_group",
    y="actor_response_risk",
    legend=False,
    figsize=(12, 8),
)
plt.title("Actor Response Risk")
plt.xlabel("Risk")
plt.ylabel("Actor group")
plt.tight_layout()
plt.savefig(FIGURES / "actor_response_risk.png", dpi=160)
plt.close()

feedback["feedback_risk_score"] = (
    0.14 * feedback["feedback_risk"]
    + 0.13 * feedback["adaptation_risk"]
    + 0.12 * feedback["delay_risk"]
    + 0.15 * feedback["burden_shift_risk"]
    + 0.13 * feedback["metric_gaming_risk"]
    + 0.12 * feedback["context_dependency"]
    - 0.09 * feedback["monitoring_quality"]
    + 0.12 * feedback["leverage_relevance"]
)

feedback.sort_values("feedback_risk_score", ascending=True).plot(
    kind="barh",
    x="feedback_id",
    y="feedback_risk_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("System Feedback Risk")
plt.xlabel("Risk")
plt.ylabel("Feedback pattern")
plt.tight_layout()
plt.savefig(FIGURES / "system_feedback_risk.png", dpi=160)
plt.close()

prototypes["prototype_test_score"] = (
    0.16 * prototypes["link_fit"]
    + 0.10 * prototypes["learning_speed"]
    + 0.15 * prototypes["learning_depth"]
    + 0.12 * prototypes["realism"]
    + 0.12 * prototypes["stakeholder_inclusion"]
    + 0.10 * prototypes["scale_signal_quality"]
    + 0.08 * prototypes["cost_efficiency"]
    + 0.09 * prototypes["ethical_safety"]
    + 0.18 * prototypes["decision_usefulness"]
)

prototypes.sort_values("prototype_test_score", ascending=True).plot(
    kind="barh",
    x="prototype_name",
    y="prototype_test_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Prototype Test Design Scores")
plt.xlabel("Score")
plt.ylabel("Prototype")
plt.tight_layout()
plt.savefig(FIGURES / "prototype_test_design_scores.png", dpi=160)
plt.close()

ideas.to_csv(TABLES / "advanced_strategic_logic_scores.csv", index=False)
links.to_csv(TABLES / "advanced_theory_link_risk_scores.csv", index=False)
actors.to_csv(TABLES / "advanced_actor_response_scores.csv", index=False)
feedback.to_csv(TABLES / "advanced_system_feedback_scores.csv", index=False)
prototypes.to_csv(TABLES / "advanced_prototype_test_scores.csv", index=False)

print("Advanced theory-of-change analytics complete.")
print(f"Wrote: {FIGURES / 'strategic_logic_scores.png'}")
print(f"Wrote: {FIGURES / 'theory_link_risk_scores.png'}")
print(f"Wrote: {FIGURES / 'mechanism_clarity_vs_evidence.png'}")
print(f"Wrote: {FIGURES / 'actor_response_risk.png'}")
print(f"Wrote: {FIGURES / 'system_feedback_risk.png'}")
print(f"Wrote: {FIGURES / 'prototype_test_design_scores.png'}")
