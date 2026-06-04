#!/usr/bin/env python3
"""
Optional advanced analytics for heuristics in strategic ideation.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- heuristic context profile chart
- premature closure risk chart
- search breadth chart
- institutional shortcut risk chart
- intervention value chart
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

contexts = pd.read_csv(RAW / "heuristic_contexts.csv")
ideas = pd.read_csv(RAW / "idea_search_inventory.csv")
shortcuts = pd.read_csv(RAW / "institutional_shortcuts.csv")
interventions = pd.read_csv(RAW / "intervention_library.csv")

contexts["heuristic_profile_score"] = (
    -0.11 * contexts["availability_dependence"]
    -0.11 * contexts["anchoring_intensity"]
    -0.10 * contexts["recognition_comfort"]
    -0.11 * contexts["satisficing_tendency"]
    -0.07 * contexts["affect_pressure"]
    -0.08 * contexts["default_gravity"]
    -0.06 * contexts["social_proof_pressure"]
    + 0.17 * contexts["exploratory_diversity"]
    + 0.13 * contexts["stakeholder_variation"]
    + 0.13 * contexts["source_domain_diversity"]
    + 0.14 * contexts["systems_check_quality"]
    + 0.07 * contexts["political_safety"]
    + 0.08 * contexts["decision_memory_quality"]
)

contexts["closure_pressure"] = (
    contexts["anchoring_intensity"] *
    contexts["satisficing_tendency"]
)

contexts.sort_values("heuristic_profile_score", ascending=True).plot(
    kind="barh",
    x="context_name",
    y="heuristic_profile_score",
    legend=False,
    figsize=(11, 8),
)
plt.title("Heuristic Profile Scores")
plt.xlabel("Profile score")
plt.ylabel("Context")
plt.tight_layout()
plt.savefig(FIGURES / "heuristic_context_profile_scores.png", dpi=160)
plt.close()

contexts.sort_values("closure_pressure", ascending=True).plot(
    kind="barh",
    x="context_name",
    y="closure_pressure",
    legend=False,
    figsize=(11, 8),
)
plt.title("Premature Closure Pressure")
plt.xlabel("Closure pressure")
plt.ylabel("Context")
plt.tight_layout()
plt.savefig(FIGURES / "premature_closure_pressure.png", dpi=160)
plt.close()

ideas["search_breadth_score"] = (
    0.12 * ideas["stakeholder_visibility"]
    + 0.12 * ideas["novelty_level"]
    + 0.12 * ideas["evidence_pathway"]
    + 0.14 * ideas["strategic_relevance"]
    + 0.10 * ideas["implementation_pathway"]
    + 0.16 * ideas["search_breadth"]
    - 0.12 * ideas["closure_pressure"]
    - 0.08 * ideas["assumption_burden"]
)

ideas.sort_values("search_breadth_score", ascending=True).plot(
    kind="barh",
    x="idea_name",
    y="search_breadth_score",
    legend=False,
    figsize=(12, 10),
)
plt.title("Search Breadth Scores")
plt.xlabel("Search breadth score")
plt.ylabel("Idea")
plt.tight_layout()
plt.savefig(FIGURES / "search_breadth_scores.png", dpi=160)
plt.close()

shortcuts["institutional_shortcut_risk"] = (
    0.16 * shortcuts["search_narrowing_risk"]
    + 0.14 * shortcuts["metric_lock_in"]
    + 0.14 * shortcuts["template_dependency"]
    + 0.14 * shortcuts["leadership_preference_pressure"]
    + 0.14 * shortcuts["stakeholder_exclusion"]
    + 0.14 * shortcuts["revision_difficulty"]
    + 0.14 * shortcuts["strategic_obsolescence_risk"]
    - 0.08 * shortcuts["coordination_benefit"]
)

shortcuts.sort_values("institutional_shortcut_risk", ascending=True).plot(
    kind="barh",
    x="shortcut_name",
    y="institutional_shortcut_risk",
    legend=False,
    figsize=(12, 8),
)
plt.title("Institutional Shortcut Risk")
plt.xlabel("Risk score")
plt.ylabel("Shortcut")
plt.tight_layout()
plt.savefig(FIGURES / "institutional_shortcut_risk.png", dpi=160)
plt.close()

interventions["intervention_value_score"] = (
    0.18 * interventions["search_breadth_gain"]
    + 0.14 * interventions["stakeholder_gain"]
    + 0.16 * interventions["systems_fit_gain"]
    + 0.16 * interventions["closure_quality_gain"]
    + 0.16 * interventions["decision_memory_gain"]
    - 0.10 * interventions["process_cost"]
    - 0.08 * interventions["implementation_complexity"]
    - 0.08 * interventions["political_safety_need"]
)

interventions.sort_values("intervention_value_score", ascending=True).plot(
    kind="barh",
    x="intervention_name",
    y="intervention_value_score",
    legend=False,
    figsize=(12, 8),
)
plt.title("Heuristic Intervention Value Scores")
plt.xlabel("Intervention value")
plt.ylabel("Intervention")
plt.tight_layout()
plt.savefig(FIGURES / "heuristic_intervention_value_scores.png", dpi=160)
plt.close()

contexts.to_csv(TABLES / "advanced_heuristic_context_profiles.csv", index=False)
ideas.to_csv(TABLES / "advanced_search_breadth_scores.csv", index=False)
shortcuts.to_csv(TABLES / "advanced_institutional_shortcut_risk.csv", index=False)
interventions.to_csv(TABLES / "advanced_intervention_value_scores.csv", index=False)

print("Advanced heuristics analytics complete.")
print(f"Wrote: {FIGURES / 'heuristic_context_profile_scores.png'}")
print(f"Wrote: {FIGURES / 'premature_closure_pressure.png'}")
print(f"Wrote: {FIGURES / 'search_breadth_scores.png'}")
print(f"Wrote: {FIGURES / 'institutional_shortcut_risk.png'}")
print(f"Wrote: {FIGURES / 'heuristic_intervention_value_scores.png'}")
