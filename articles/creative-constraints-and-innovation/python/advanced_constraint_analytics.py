#!/usr/bin/env python3
"""
Optional advanced analytics for creative constraints and innovation.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- productive constraint profile chart
- rigidity risk chart
- diffusion risk chart
- innovation option score chart
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

contexts = pd.read_csv(RAW / "constraint_contexts.csv")
options = pd.read_csv(RAW / "innovation_options.csv")
constraints = pd.read_csv(RAW / "constraint_register.csv")

contexts["rigidity_pressure"] = (
    0.24 * contexts["resource_pressure"]
    + 0.25 * contexts["technical_rigidity"]
    + 0.27 * contexts["institutional_rigidity"]
    + 0.24 * contexts["ecological_boundary_pressure"]
)

contexts["productive_constraint_profile"] = (
    -0.10 * contexts["resource_pressure"]
    -0.10 * contexts["technical_rigidity"]
    -0.10 * contexts["institutional_rigidity"]
    + 0.12 * contexts["ecological_boundary_pressure"]
    + 0.16 * contexts["ethical_constraint_visibility"]
    + 0.16 * contexts["search_focus"]
    + 0.16 * contexts["adaptive_opportunity"]
    + 0.14 * contexts["stakeholder_legitimacy"]
    + 0.14 * contexts["learning_capacity"]
    + 0.12 * contexts["implementation_readiness"]
)

contexts["rigidity_risk"] = contexts["rigidity_pressure"] * (1 - contexts["learning_capacity"])
contexts["diffusion_risk"] = (1 - contexts["search_focus"]) * contexts["adaptive_opportunity"]

contexts.sort_values("productive_constraint_profile", ascending=True).plot(
    kind="barh",
    x="context_name",
    y="productive_constraint_profile",
    legend=False,
    figsize=(11, 8),
)
plt.title("Productive Constraint Profile Scores")
plt.xlabel("Profile score")
plt.ylabel("Context")
plt.tight_layout()
plt.savefig(FIGURES / "productive_constraint_profile_scores.png", dpi=160)
plt.close()

contexts.sort_values("rigidity_risk", ascending=True).plot(
    kind="barh",
    x="context_name",
    y="rigidity_risk",
    legend=False,
    figsize=(11, 8),
)
plt.title("Constraint Rigidity Risk")
plt.xlabel("Risk")
plt.ylabel("Context")
plt.tight_layout()
plt.savefig(FIGURES / "constraint_rigidity_risk.png", dpi=160)
plt.close()

contexts.sort_values("diffusion_risk", ascending=True).plot(
    kind="barh",
    x="context_name",
    y="diffusion_risk",
    legend=False,
    figsize=(11, 8),
)
plt.title("Constraint Diffusion Risk")
plt.xlabel("Risk")
plt.ylabel("Context")
plt.tight_layout()
plt.savefig(FIGURES / "constraint_diffusion_risk.png", dpi=160)
plt.close()

options["innovation_option_score"] = (
    0.12 * options["novelty"]
    + 0.16 * options["strategic_fit"]
    + 0.14 * options["constraint_fit"]
    + 0.14 * options["adaptive_value"]
    + 0.12 * options["stakeholder_value"]
    + 0.12 * options["ecological_responsibility"]
    + 0.12 * options["ethical_legitimacy"]
    + 0.10 * options["implementation_readiness"]
    - 0.08 * options["assumption_burden"]
)

options.sort_values("innovation_option_score", ascending=True).plot(
    kind="barh",
    x="option_name",
    y="innovation_option_score",
    legend=False,
    figsize=(12, 9),
)
plt.title("Innovation Option Scores Under Constraint")
plt.xlabel("Option score")
plt.ylabel("Option")
plt.tight_layout()
plt.savefig(FIGURES / "innovation_option_scores.png", dpi=160)
plt.close()

constraints.to_csv(TABLES / "advanced_constraint_register_export.csv", index=False)

print("Advanced creative constraint analytics complete.")
print(f"Wrote: {FIGURES / 'productive_constraint_profile_scores.png'}")
print(f"Wrote: {FIGURES / 'constraint_rigidity_risk.png'}")
print(f"Wrote: {FIGURES / 'constraint_diffusion_risk.png'}")
print(f"Wrote: {FIGURES / 'innovation_option_scores.png'}")
print(f"Wrote: {TABLES / 'advanced_constraint_register_export.csv'}")
