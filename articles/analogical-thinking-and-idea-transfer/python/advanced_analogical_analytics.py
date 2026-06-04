#!/usr/bin/env python3
"""
Optional advanced analytics for analogical thinking and idea transfer.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- analogical strategy profile chart
- surface-distraction risk chart
- source-target mapping chart
- adaptation readiness chart
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

strategies = pd.read_csv(RAW / "analogical_strategies.csv")
mappings = pd.read_csv(RAW / "source_target_mappings.csv")
adaptations = pd.read_csv(RAW / "adaptation_tests.csv")
sources = pd.read_csv(RAW / "source_domains.csv")
targets = pd.read_csv(RAW / "target_problems.csv")

strategies["analogy_profile_score"] = (
    0.20 * strategies["structural_fit"]
    + 0.16 * strategies["functional_fit"]
    - 0.16 * strategies["surface_distraction"]
    + 0.16 * strategies["adaptation_quality"]
    + 0.12 * strategies["context_sensitivity"]
    + 0.08 * strategies["stakeholder_legitimacy"]
    + 0.08 * strategies["dynamic_compatibility"]
    + 0.12 * strategies["innovation_potential"]
    + 0.08 * strategies["evidence_strength"]
)

strategies["surface_distraction_risk"] = strategies["surface_distraction"] * (1 - strategies["structural_fit"])

strategies.sort_values("analogy_profile_score", ascending=True).plot(
    kind="barh",
    x="strategy_name",
    y="analogy_profile_score",
    legend=False,
    figsize=(11, 8),
)
plt.title("Analogical Strategy Profile Scores")
plt.xlabel("Profile score")
plt.ylabel("Strategy")
plt.tight_layout()
plt.savefig(FIGURES / "analogical_strategy_profile_scores.png", dpi=160)
plt.close()

strategies.sort_values("surface_distraction_risk", ascending=True).plot(
    kind="barh",
    x="strategy_name",
    y="surface_distraction_risk",
    legend=False,
    figsize=(11, 8),
)
plt.title("Surface-Distraction Risk")
plt.xlabel("Risk")
plt.ylabel("Strategy")
plt.tight_layout()
plt.savefig(FIGURES / "surface_distraction_risk.png", dpi=160)
plt.close()

mappings["mapping_score"] = (
    0.14 * mappings["actor_correspondence"]
    + 0.20 * mappings["relation_correspondence"]
    + 0.14 * mappings["flow_correspondence"]
    + 0.14 * mappings["constraint_correspondence"]
    + 0.14 * mappings["feedback_correspondence"]
    + 0.12 * mappings["failure_mode_correspondence"]
    + 0.08 * mappings["breakpoint_visibility"]
    + 0.04 * mappings["mapping_confidence"]
)

mappings = mappings.merge(sources[["source_id", "source_name"]], on="source_id", how="left")
mappings = mappings.merge(targets[["target_id", "target_name"]], on="target_id", how="left")
mappings["mapping_label"] = mappings["source_name"] + " → " + mappings["target_name"]

mappings.sort_values("mapping_score", ascending=True).plot(
    kind="barh",
    x="mapping_label",
    y="mapping_score",
    legend=False,
    figsize=(12, 9),
)
plt.title("Source-Target Mapping Scores")
plt.xlabel("Mapping score")
plt.ylabel("Mapping")
plt.tight_layout()
plt.savefig(FIGURES / "source_target_mapping_scores.png", dpi=160)
plt.close()

adaptations["adaptation_score"] = (
    0.14 * adaptations["constraint_fit"]
    + 0.14 * adaptations["stakeholder_fit"]
    + 0.18 * adaptations["mechanism_fit"]
    + 0.14 * adaptations["governance_fit"]
    + 0.12 * adaptations["implementation_fit"]
    + 0.12 * adaptations["evidence_fit"]
    + 0.12 * adaptations["ethical_fit"]
    + 0.04 * adaptations["adaptation_readiness"]
)

adaptations.sort_values("adaptation_score", ascending=True).plot(
    kind="barh",
    x="adaptation_id",
    y="adaptation_score",
    legend=False,
    figsize=(10, 7),
)
plt.title("Adaptation Readiness Scores")
plt.xlabel("Adaptation score")
plt.ylabel("Adaptation")
plt.tight_layout()
plt.savefig(FIGURES / "adaptation_readiness_scores.png", dpi=160)
plt.close()

strategies.to_csv(TABLES / "advanced_analogical_strategy_profiles.csv", index=False)
mappings.to_csv(TABLES / "advanced_source_target_mapping_scores.csv", index=False)
adaptations.to_csv(TABLES / "advanced_adaptation_readiness_scores.csv", index=False)

print("Advanced analogical analytics complete.")
print(f"Wrote: {FIGURES / 'analogical_strategy_profile_scores.png'}")
print(f"Wrote: {FIGURES / 'surface_distraction_risk.png'}")
print(f"Wrote: {FIGURES / 'source_target_mapping_scores.png'}")
print(f"Wrote: {FIGURES / 'adaptation_readiness_scores.png'}")
