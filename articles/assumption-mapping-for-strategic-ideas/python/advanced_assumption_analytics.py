#!/usr/bin/env python3
"""
Optional advanced analytics for assumption mapping.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- assumption criticality vs uncertainty scatter
- evidence-adjusted risk chart
- learning value chart
- option confidence chart
- system response risk chart
- revision trigger quality chart
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

assumptions = pd.read_csv(RAW / "assumptions.csv")
options = pd.read_csv(RAW / "option_confidence.csv")
system_response = pd.read_csv(RAW / "system_response_assumptions.csv")
triggers = pd.read_csv(RAW / "revision_triggers.csv")

assumptions["evidence_composite"] = (
    0.40 * assumptions["evidence_strength"]
    + 0.30 * assumptions["evidence_relevance"]
    + 0.30 * assumptions["evidence_transferability"]
)

assumptions["priority_score"] = assumptions["criticality"] * assumptions["uncertainty"]
assumptions["evidence_adjusted_risk"] = (
    assumptions["criticality"]
    * assumptions["uncertainty"]
    * (1 - assumptions["evidence_composite"])
)
assumptions["commitment_risk"] = assumptions["evidence_adjusted_risk"] * (
    0.42 * (1 - assumptions["reversibility"])
    + 0.28 * assumptions["stakeholder_sensitivity"]
    + 0.18 * assumptions["system_sensitivity"]
    + 0.12 * assumptions["time_sensitivity"]
)
assumptions["learning_value"] = (
    0.34 * assumptions["evidence_adjusted_risk"]
    + 0.24 * assumptions["testability"]
    + 0.18 * assumptions["stakeholder_sensitivity"]
    + 0.14 * assumptions["system_sensitivity"]
    + 0.10 * assumptions["criticality"]
)

plt.figure(figsize=(10, 8))
plt.scatter(assumptions["uncertainty"], assumptions["criticality"])
for _, row in assumptions.iterrows():
    plt.annotate(row["assumption_id"], (row["uncertainty"], row["criticality"]))
plt.xlabel("Uncertainty")
plt.ylabel("Criticality")
plt.title("Assumption Criticality vs Uncertainty")
plt.tight_layout()
plt.savefig(FIGURES / "assumption_criticality_uncertainty.png", dpi=160)
plt.close()

assumptions.sort_values("evidence_adjusted_risk", ascending=True).plot(
    kind="barh",
    x="assumption_id",
    y="evidence_adjusted_risk",
    legend=False,
    figsize=(12, 9),
)
plt.title("Evidence-Adjusted Assumption Risk")
plt.xlabel("Risk")
plt.ylabel("Assumption")
plt.tight_layout()
plt.savefig(FIGURES / "evidence_adjusted_assumption_risk.png", dpi=160)
plt.close()

assumptions.sort_values("learning_value", ascending=True).plot(
    kind="barh",
    x="assumption_id",
    y="learning_value",
    legend=False,
    figsize=(12, 9),
)
plt.title("Assumption Learning Value")
plt.xlabel("Learning value")
plt.ylabel("Assumption")
plt.tight_layout()
plt.savefig(FIGURES / "assumption_learning_value.png", dpi=160)
plt.close()

options["option_confidence_score"] = (
    0.18 * options["expected_value"]
    - 0.18 * options["assumption_risk"]
    - 0.10 * options["commitment_risk"]
    + 0.14 * options["evidence_strength"]
    + 0.12 * options["learning_value"]
    + 0.10 * options["reversibility"]
    + 0.12 * options["stakeholder_legitimacy"]
    + 0.08 * options["implementation_readiness"]
    + 0.08 * options["system_resilience"]
)

options.sort_values("option_confidence_score", ascending=True).plot(
    kind="barh",
    x="option_name",
    y="option_confidence_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Option Confidence Scores")
plt.xlabel("Confidence")
plt.ylabel("Option")
plt.tight_layout()
plt.savefig(FIGURES / "option_confidence_scores.png", dpi=160)
plt.close()

system_response["system_response_risk"] = (
    0.14 * system_response["feedback_risk"]
    + 0.13 * system_response["adaptation_risk"]
    + 0.15 * system_response["burden_shift_risk"]
    + 0.11 * system_response["delay_risk"]
    + 0.13 * system_response["metric_gaming_risk"]
    + 0.12 * system_response["resistance_risk"]
    + 0.12 * system_response["leverage_relevance"]
    - 0.10 * system_response["monitoring_quality"]
)

system_response.sort_values("system_response_risk", ascending=True).plot(
    kind="barh",
    x="system_assumption_id",
    y="system_response_risk",
    legend=False,
    figsize=(12, 8),
)
plt.title("System Response Assumption Risk")
plt.xlabel("Risk")
plt.ylabel("System assumption")
plt.tight_layout()
plt.savefig(FIGURES / "system_response_risk.png", dpi=160)
plt.close()

triggers["trigger_quality_score"] = (
    0.15 * triggers["signal_quality"]
    + 0.15 * triggers["threshold_clarity"]
    + 0.16 * triggers["decision_linkage"]
    + 0.12 * triggers["timeliness"]
    + 0.12 * triggers["stakeholder_visibility"]
    + 0.12 * triggers["governance_owner_clarity"]
    + 0.18 * triggers["response_options_quality"]
)

triggers.sort_values("trigger_quality_score", ascending=True).plot(
    kind="barh",
    x="trigger_id",
    y="trigger_quality_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Revision Trigger Quality")
plt.xlabel("Trigger quality")
plt.ylabel("Trigger")
plt.tight_layout()
plt.savefig(FIGURES / "revision_trigger_quality.png", dpi=160)
plt.close()

assumptions.to_csv(TABLES / "advanced_assumption_scores.csv", index=False)
options.to_csv(TABLES / "advanced_option_confidence_scores.csv", index=False)
system_response.to_csv(TABLES / "advanced_system_response_scores.csv", index=False)
triggers.to_csv(TABLES / "advanced_revision_trigger_scores.csv", index=False)

print("Advanced assumption analytics complete.")
print(f"Wrote: {FIGURES / 'assumption_criticality_uncertainty.png'}")
print(f"Wrote: {FIGURES / 'evidence_adjusted_assumption_risk.png'}")
print(f"Wrote: {FIGURES / 'assumption_learning_value.png'}")
print(f"Wrote: {FIGURES / 'option_confidence_scores.png'}")
print(f"Wrote: {FIGURES / 'system_response_risk.png'}")
print(f"Wrote: {FIGURES / 'revision_trigger_quality.png'}")
