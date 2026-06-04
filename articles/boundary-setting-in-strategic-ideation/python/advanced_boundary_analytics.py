#!/usr/bin/env python3
"""
Optional advanced analytics for boundary setting in strategic ideation.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- boundary quality chart
- boundary risk chart
- boundary sensitivity chart
- option boundary comparison chart
- stakeholder exclusion chart
- drift risk chart
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

boundaries = pd.read_csv(RAW / "boundary_frames.csv")
options = pd.read_csv(RAW / "options.csv")
stakeholders = pd.read_csv(RAW / "stakeholder_boundaries.csv")
drift = pd.read_csv(RAW / "boundary_drift.csv")

boundaries["boundary_quality_score"] = (
    0.12 * boundaries["problem_clarity"]
    + 0.13 * boundaries["system_context"]
    + 0.14 * boundaries["stakeholder_inclusion"]
    + 0.14 * boundaries["causal_adequacy"]
    + 0.12 * boundaries["temporal_adequacy"]
    + 0.11 * boundaries["institutional_responsibility"]
    + 0.11 * boundaries["evidence_diversity"]
    + 0.10 * boundaries["ethical_review"]
    + 0.09 * boundaries["revision_readiness"]
    + 0.04 * boundaries["actionability"]
)

boundaries["boundary_risk_score"] = 1 - boundaries["boundary_quality_score"]

boundaries.sort_values("boundary_quality_score", ascending=True).plot(
    kind="barh",
    x="boundary_name",
    y="boundary_quality_score",
    legend=False,
    figsize=(12, 9),
)
plt.title("Boundary Quality Scores")
plt.xlabel("Boundary quality")
plt.ylabel("Boundary frame")
plt.tight_layout()
plt.savefig(FIGURES / "boundary_quality_scores.png", dpi=160)
plt.close()

boundaries.sort_values("boundary_risk_score", ascending=True).plot(
    kind="barh",
    x="boundary_name",
    y="boundary_risk_score",
    legend=False,
    figsize=(12, 9),
)
plt.title("Boundary Risk Scores")
plt.xlabel("Boundary risk")
plt.ylabel("Boundary frame")
plt.tight_layout()
plt.savefig(FIGURES / "boundary_risk_scores.png", dpi=160)
plt.close()

weights = {
    "internal_boundary": {
        "internal_efficiency": 0.38,
        "stakeholder_value": 0.10,
        "system_leverage": 0.10,
        "long_term_resilience": 0.10,
        "ethical_responsibility": 0.08,
        "implementation_feasibility": 0.16,
        "learning_value": 0.04,
        "strategic_reversibility": 0.04,
    },
    "stakeholder_boundary": {
        "internal_efficiency": 0.08,
        "stakeholder_value": 0.34,
        "system_leverage": 0.12,
        "long_term_resilience": 0.10,
        "ethical_responsibility": 0.20,
        "implementation_feasibility": 0.08,
        "learning_value": 0.05,
        "strategic_reversibility": 0.03,
    },
    "system_boundary": {
        "internal_efficiency": 0.08,
        "stakeholder_value": 0.12,
        "system_leverage": 0.34,
        "long_term_resilience": 0.18,
        "ethical_responsibility": 0.10,
        "implementation_feasibility": 0.06,
        "learning_value": 0.08,
        "strategic_reversibility": 0.04,
    },
    "long_term_boundary": {
        "internal_efficiency": 0.06,
        "stakeholder_value": 0.12,
        "system_leverage": 0.20,
        "long_term_resilience": 0.32,
        "ethical_responsibility": 0.14,
        "implementation_feasibility": 0.05,
        "learning_value": 0.08,
        "strategic_reversibility": 0.03,
    },
    "ethical_boundary": {
        "internal_efficiency": 0.06,
        "stakeholder_value": 0.22,
        "system_leverage": 0.12,
        "long_term_resilience": 0.16,
        "ethical_responsibility": 0.28,
        "implementation_feasibility": 0.05,
        "learning_value": 0.07,
        "strategic_reversibility": 0.04,
    },
}

scores = options[["option_id", "option_name"]].copy()

for boundary, boundary_weights in weights.items():
    scores[boundary] = sum(options[col] * weight for col, weight in boundary_weights.items())

score_cols = [col for col in scores.columns if col.endswith("_boundary")]
scores["mean_score"] = scores[score_cols].mean(axis=1)
scores["boundary_sensitivity"] = scores[score_cols].max(axis=1) - scores[score_cols].min(axis=1)

scores.set_index("option_name")[score_cols].plot(kind="bar", figsize=(12, 7))
plt.ylabel("Boundary-weighted score")
plt.title("Strategic Option Scores Across Boundary Frames")
plt.tight_layout()
plt.savefig(FIGURES / "option_scores_across_boundaries.png", dpi=160)
plt.close()

scores.sort_values("boundary_sensitivity", ascending=True).plot(
    kind="barh",
    x="option_name",
    y="boundary_sensitivity",
    legend=False,
    figsize=(12, 8),
)
plt.xlabel("Boundary sensitivity")
plt.ylabel("Option")
plt.title("Boundary Sensitivity by Option")
plt.tight_layout()
plt.savefig(FIGURES / "boundary_sensitivity_scores.png", dpi=160)
plt.close()

stakeholders["stakeholder_exclusion_risk"] = (
    0.18 * stakeholders["affectedness"]
    + 0.15 * stakeholders["knowledge_value"]
    + 0.15 * stakeholders["burden_risk"]
    + 0.14 * stakeholders["trust_sensitivity"]
    + 0.12 * stakeholders["implementation_role"]
    - 0.15 * stakeholders["inclusion_quality"]
    - 0.11 * stakeholders["representation_quality"]
)

stakeholders.sort_values("stakeholder_exclusion_risk", ascending=True).plot(
    kind="barh",
    x="stakeholder_group",
    y="stakeholder_exclusion_risk",
    legend=False,
    figsize=(12, 8),
)
plt.title("Stakeholder Exclusion Risk")
plt.xlabel("Exclusion risk")
plt.ylabel("Stakeholder group")
plt.tight_layout()
plt.savefig(FIGURES / "stakeholder_exclusion_risk.png", dpi=160)
plt.close()

drift["boundary_drift_risk"] = (
    0.12 * drift["scope_change"]
    + 0.12 * drift["stakeholder_change"]
    + 0.14 * drift["metric_change"]
    + 0.13 * drift["responsibility_change"]
    + 0.13 * drift["evidence_change"]
    - 0.14 * drift["explicitness"]
    - 0.10 * drift["evidence_basis"]
    + 0.12 * drift["coherence_risk"]
)

drift.sort_values("boundary_drift_risk", ascending=True).plot(
    kind="barh",
    x="drift_type",
    y="boundary_drift_risk",
    legend=False,
    figsize=(12, 8),
)
plt.title("Boundary Drift Risk")
plt.xlabel("Drift risk")
plt.ylabel("Drift type")
plt.tight_layout()
plt.savefig(FIGURES / "boundary_drift_risk.png", dpi=160)
plt.close()

boundaries.to_csv(TABLES / "advanced_boundary_quality_scores.csv", index=False)
scores.to_csv(TABLES / "advanced_boundary_sensitivity_scores.csv", index=False)
stakeholders.to_csv(TABLES / "advanced_stakeholder_exclusion_scores.csv", index=False)
drift.to_csv(TABLES / "advanced_boundary_drift_scores.csv", index=False)

print("Advanced boundary analytics complete.")
print(f"Wrote: {FIGURES / 'boundary_quality_scores.png'}")
print(f"Wrote: {FIGURES / 'boundary_risk_scores.png'}")
print(f"Wrote: {FIGURES / 'option_scores_across_boundaries.png'}")
print(f"Wrote: {FIGURES / 'boundary_sensitivity_scores.png'}")
print(f"Wrote: {FIGURES / 'stakeholder_exclusion_risk.png'}")
print(f"Wrote: {FIGURES / 'boundary_drift_risk.png'}")
