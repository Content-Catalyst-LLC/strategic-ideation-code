#!/usr/bin/env python3
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
TABLES = ROOT / "outputs" / "tables"
FIGURES = ROOT / "outputs" / "figures"
TABLES.mkdir(parents=True, exist_ok=True); FIGURES.mkdir(parents=True, exist_ok=True)
try:
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError as exc:
    print("Missing optional advanced analytics dependencies.")
    print("Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r python/requirements-advanced.txt")
    raise SystemExit(1) from exc
contexts = pd.read_csv(RAW / "strategy_contexts.csv")
assumptions = pd.read_csv(RAW / "assumptions.csv")
options = pd.read_csv(RAW / "reconstructed_options.csv")
contexts["profile_score"] = (-0.16*contexts.assumption_load + 0.18*contexts.structural_clarity + 0.18*contexts.constraint_discrimination + 0.18*contexts.reconstruction_quality + 0.14*contexts.adaptive_potential + 0.10*contexts.evidence_contact + 0.10*contexts.ethical_visibility + 0.08*contexts.implementation_feasibility)
contexts.sort_values("profile_score", ascending=True).plot(kind="barh", x="context_name", y="profile_score", legend=False, figsize=(11,8))
plt.title("First Principles Strategy Profile Scores"); plt.tight_layout(); plt.savefig(FIGURES / "first_principles_profile_scores.png", dpi=160); plt.close()
assumptions["assumption_burden"] = (1-assumptions.confidence) * assumptions.strategic_influence
assumptions.sort_values("assumption_burden", ascending=True).plot(kind="barh", x="assumption_id", y="assumption_burden", legend=False, figsize=(10,8))
plt.title("Assumption Burden Register"); plt.tight_layout(); plt.savefig(FIGURES / "assumption_burden_register.png", dpi=160); plt.close()
options["option_score"] = (0.18*options.strategic_fit + 0.16*options.constraint_realism + 0.20*options.mechanism_alignment + 0.14*options.evidence_contact + 0.16*options.ethical_legitimacy + 0.14*options.implementation_feasibility - 0.08*options.uncertainty)
options.sort_values("option_score", ascending=False).to_csv(TABLES / "advanced_reconstructed_option_rankings.csv", index=False)
print("Advanced first principles analytics complete.")
