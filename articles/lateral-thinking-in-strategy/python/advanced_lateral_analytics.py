#!/usr/bin/env python3
"""
Optional advanced analytics for lateral thinking in strategy.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- lateral context profile chart
- frame rigidity risk chart
- lateral move score chart
- reframe quality score chart
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
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError as exc:
    print("Missing optional advanced analytics dependencies.")
    print("Run:")
    print("  python3 -m venv .venv")
    print("  source .venv/bin/activate")
    print("  pip install -r python/requirements-advanced.txt")
    raise SystemExit(1) from exc

contexts = pd.read_csv(RAW / "lateral_contexts.csv")
moves = pd.read_csv(RAW / "lateral_moves.csv")
reframes = pd.read_csv(RAW / "reframed_problems.csv")

contexts["lateral_profile_score"] = (
    -0.14 * contexts["frame_rigidity"]
    + 0.14 * contexts["provocation_strength"]
    + 0.12 * contexts["analogical_distance"]
    + 0.09 * contexts["random_entry_capacity"]
    + 0.10 * contexts["reversal_capacity"]
    + 0.10 * contexts["challenge_quality"]
    + 0.14 * contexts["convergence_discipline"]
    + 0.12 * contexts["systems_integration"]
    + 0.08 * contexts["stakeholder_legitimacy"]
    + 0.07 * contexts["political_safety"]
    + 0.14 * contexts["transformational_potential"]
)

contexts["frame_rigidity_risk"] = contexts["frame_rigidity"] * (1 - contexts["provocation_strength"])
contexts["drift_risk"] = contexts["transformational_potential"] * (1 - contexts["convergence_discipline"])

contexts.sort_values("lateral_profile_score", ascending=True).plot(
    kind="barh",
    x="context_name",
    y="lateral_profile_score",
    legend=False,
    figsize=(11, 8),
)
plt.title("Lateral Thinking Profile Scores")
plt.xlabel("Profile score")
plt.ylabel("Context")
plt.tight_layout()
plt.savefig(FIGURES / "lateral_context_profile_scores.png", dpi=160)
plt.close()

contexts.sort_values("frame_rigidity_risk", ascending=True).plot(
    kind="barh",
    x="context_name",
    y="frame_rigidity_risk",
    legend=False,
    figsize=(11, 8),
)
plt.title("Frame Rigidity Risk")
plt.xlabel("Risk")
plt.ylabel("Context")
plt.tight_layout()
plt.savefig(FIGURES / "frame_rigidity_risk.png", dpi=160)
plt.close()

moves["lateral_move_score"] = (
    0.16 * moves["frame_disruption"]
    + 0.18 * moves["strategic_relevance"]
    + 0.16 * moves["reconstruction_quality"]
    + 0.12 * moves["evidence_pathway"]
    + 0.12 * moves["stakeholder_fit"]
    + 0.12 * moves["systems_fit"]
    + 0.10 * moves["novelty_value"]
    - 0.14 * moves["drift_risk"]
)

moves.sort_values("lateral_move_score", ascending=True).plot(
    kind="barh",
    x="move_name",
    y="lateral_move_score",
    legend=False,
    figsize=(12, 9),
)
plt.title("Lateral Move Scores")
plt.xlabel("Move score")
plt.ylabel("Move")
plt.tight_layout()
plt.savefig(FIGURES / "lateral_move_scores.png", dpi=160)
plt.close()

reframes["reframe_quality_score"] = (
    0.16 * reframes["problem_clarity"]
    + 0.18 * reframes["structural_shift"]
    + 0.14 * reframes["stakeholder_visibility"]
    + 0.16 * reframes["systems_alignment"]
    + 0.14 * reframes["decision_value"]
    + 0.12 * reframes["testability"]
    + 0.10 * reframes["implementation_pathway_quality"]
)

reframes.sort_values("reframe_quality_score", ascending=True).plot(
    kind="barh",
    x="reframed_problem",
    y="reframe_quality_score",
    legend=False,
    figsize=(12, 9),
)
plt.title("Reframed Problem Quality Scores")
plt.xlabel("Reframe score")
plt.ylabel("Reframed problem")
plt.tight_layout()
plt.savefig(FIGURES / "reframed_problem_quality_scores.png", dpi=160)
plt.close()

contexts.to_csv(TABLES / "advanced_lateral_context_profiles.csv", index=False)
moves.to_csv(TABLES / "advanced_lateral_move_scores.csv", index=False)
reframes.to_csv(TABLES / "advanced_reframed_problem_scores.csv", index=False)

print("Advanced lateral analytics complete.")
print(f"Wrote: {FIGURES / 'lateral_context_profile_scores.png'}")
print(f"Wrote: {FIGURES / 'frame_rigidity_risk.png'}")
print(f"Wrote: {FIGURES / 'lateral_move_scores.png'}")
print(f"Wrote: {FIGURES / 'reframed_problem_quality_scores.png'}")
