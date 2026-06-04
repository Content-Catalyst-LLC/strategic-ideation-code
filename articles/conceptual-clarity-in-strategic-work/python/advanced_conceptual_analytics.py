#!/usr/bin/env python3
"""
Optional advanced analytics for conceptual clarity in strategic work.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- conceptual clarity score chart
- ambiguity risk chart
- metric proxy-risk chart
- conceptual drift table
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

concepts = pd.read_csv(RAW / "concept_inventory.csv")
metrics = pd.read_csv(RAW / "metric_register.csv")
drift = pd.read_csv(RAW / "drift_events.csv")

concepts["conceptual_clarity_score"] = (
    0.17 * concepts["definition_clarity"]
    + 0.14 * concepts["boundary_clarity"]
    + 0.14 * concepts["distinction_quality"]
    + 0.13 * concepts["operational_implication"]
    + 0.15 * concepts["measurement_validity"]
    + 0.10 * concepts["revision_capacity"]
    + 0.07 * concepts["stakeholder_visibility"]
    + 0.06 * concepts["ethical_visibility"]
    + 0.04 * concepts["governance_maturity"]
)

concepts["ambiguity_risk"] = 1 - concepts["conceptual_clarity_score"]

concepts.sort_values("conceptual_clarity_score", ascending=True).plot(
    kind="barh",
    x="concept_name",
    y="conceptual_clarity_score",
    legend=False,
    figsize=(11, 8),
)
plt.title("Conceptual Clarity Scores")
plt.xlabel("Conceptual clarity score")
plt.ylabel("Concept")
plt.tight_layout()
plt.savefig(FIGURES / "conceptual_clarity_scores.png", dpi=160)
plt.close()

concepts.sort_values("ambiguity_risk", ascending=True).plot(
    kind="barh",
    x="concept_name",
    y="ambiguity_risk",
    legend=False,
    figsize=(11, 8),
)
plt.title("Ambiguity Risk by Strategic Concept")
plt.xlabel("Ambiguity risk")
plt.ylabel("Concept")
plt.tight_layout()
plt.savefig(FIGURES / "ambiguity_risk_by_concept.png", dpi=160)
plt.close()

metrics["proxy_failure_risk"] = (
    0.28 * metrics["proxy_risk"]
    + 0.26 * metrics["incentive_distortion_risk"]
    + 0.22 * metrics["qualitative_gap"]
    + 0.24 * (1 - metrics["validity_confidence"])
)

metrics.sort_values("proxy_failure_risk", ascending=True).plot(
    kind="barh",
    x="metric_name",
    y="proxy_failure_risk",
    legend=False,
    figsize=(12, 9),
)
plt.title("Metric Proxy Failure Risk")
plt.xlabel("Proxy failure risk")
plt.ylabel("Metric")
plt.tight_layout()
plt.savefig(FIGURES / "metric_proxy_failure_risk.png", dpi=160)
plt.close()

drift["drift_priority"] = (
    0.34 * drift["drift_severity"]
    + 0.34 * drift["strategic_exposure"]
    + 0.18 * drift["detection_confidence"]
)

drift.sort_values("drift_priority", ascending=False).to_csv(
    TABLES / "advanced_conceptual_drift_rankings.csv",
    index=False,
)

print("Advanced conceptual analytics complete.")
print(f"Wrote: {FIGURES / 'conceptual_clarity_scores.png'}")
print(f"Wrote: {FIGURES / 'ambiguity_risk_by_concept.png'}")
print(f"Wrote: {FIGURES / 'metric_proxy_failure_risk.png'}")
print(f"Wrote: {TABLES / 'advanced_conceptual_drift_rankings.csv'}")
