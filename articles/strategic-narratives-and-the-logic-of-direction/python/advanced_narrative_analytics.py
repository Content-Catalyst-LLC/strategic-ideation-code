#!/usr/bin/env python3
"""
Optional advanced analytics for strategic narratives.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- narrative coherence chart
- performance gap chart
- narrative drift chart
- governance strength table
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

profiles = pd.read_csv(RAW / "narrative_profiles.csv")
performance = pd.read_csv(RAW / "performance_evidence.csv")
drift = pd.read_csv(RAW / "narrative_drift_events.csv")
governance = pd.read_csv(RAW / "narrative_governance.csv")

profiles["narrative_coherence_score"] = (
    0.14 * profiles["diagnosis_clarity"]
    + 0.12 * profiles["purpose_clarity"]
    + 0.14 * profiles["choice_clarity"]
    + 0.12 * profiles["sequencing_logic"]
    + 0.11 * profiles["role_clarity"]
    + 0.10 * profiles["future_credibility"]
    + 0.11 * profiles["accountability_strength"]
    + 0.08 * profiles["evidence_grounding"]
    + 0.05 * profiles["stakeholder_visibility"]
    + 0.03 * profiles["ethical_visibility"]
)

profiles["drift_risk"] = 1 - profiles["narrative_coherence_score"]

profiles.sort_values("narrative_coherence_score", ascending=True).plot(
    kind="barh",
    x="narrative_name",
    y="narrative_coherence_score",
    legend=False,
    figsize=(11, 8),
)
plt.title("Strategic Narrative Coherence Scores")
plt.xlabel("Narrative coherence score")
plt.ylabel("Narrative")
plt.tight_layout()
plt.savefig(FIGURES / "narrative_coherence_scores.png", dpi=160)
plt.close()

performance["narrative_performance_gap"] = (
    0.26 * (1 - performance["evidence_strength"])
    + 0.28 * (1 - performance["action_alignment"])
    + 0.26 * performance["contradiction_risk"]
    + 0.12 * performance["stakeholder_signal"]
    + 0.08 * performance["revision_required"].map(lambda value: 1 if str(value).lower() == "true" else 0)
)

performance.sort_values("narrative_performance_gap", ascending=True).plot(
    kind="barh",
    x="evidence_id",
    y="narrative_performance_gap",
    legend=False,
    figsize=(11, 8),
)
plt.title("Narrative-Performance Gap Scores")
plt.xlabel("Gap score")
plt.ylabel("Evidence")
plt.tight_layout()
plt.savefig(FIGURES / "narrative_performance_gap_scores.png", dpi=160)
plt.close()

drift["drift_priority"] = (
    0.34 * drift["drift_severity"]
    + 0.34 * drift["strategic_exposure"]
    + 0.18 * drift["detection_confidence"]
)

drift.sort_values("drift_priority", ascending=True).plot(
    kind="barh",
    x="drift_id",
    y="drift_priority",
    legend=False,
    figsize=(11, 8),
)
plt.title("Narrative Drift Priority")
plt.xlabel("Drift priority")
plt.ylabel("Drift event")
plt.tight_layout()
plt.savefig(FIGURES / "narrative_drift_priority.png", dpi=160)
plt.close()

governance["governance_strength"] = (
    0.14 * governance["diagnosis_owner"]
    + 0.14 * governance["choice_owner"]
    + 0.18 * governance["evidence_review_quality"]
    + 0.18 * governance["stakeholder_review_quality"]
    + 0.18 * governance["performance_gap_review"]
    + 0.18 * governance["revision_trigger_quality"]
    - 0.16 * governance["governance_risk"]
)

governance.sort_values("governance_strength", ascending=False).to_csv(
    TABLES / "advanced_narrative_governance_rankings.csv",
    index=False,
)

print("Advanced narrative analytics complete.")
print(f"Wrote: {FIGURES / 'narrative_coherence_scores.png'}")
print(f"Wrote: {FIGURES / 'narrative_performance_gap_scores.png'}")
print(f"Wrote: {FIGURES / 'narrative_drift_priority.png'}")
print(f"Wrote: {TABLES / 'advanced_narrative_governance_rankings.csv'}")
