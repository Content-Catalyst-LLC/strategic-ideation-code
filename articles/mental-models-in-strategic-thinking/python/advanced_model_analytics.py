#!/usr/bin/env python3
"""
Optional advanced analytics for mental models in strategic thinking.

Requires:
    pip install -r python/requirements-advanced.txt

Outputs:
- mental model profile chart
- monoculture risk chart
- causal adequacy scatterplot
- scenario stress-test ranking
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

models = pd.read_csv(RAW / "mental_model_profiles.csv")
causal = pd.read_csv(RAW / "causal_frames.csv")
stress = pd.read_csv(RAW / "scenario_stress_tests.csv")

models["adaptive_model_score"] = (
    0.17 * models["systems_richness"]
    + 0.13 * models["probabilistic_depth"]
    + 0.16 * models["model_flexibility"]
    + 0.14 * models["model_plurality"]
    + 0.16 * models["revision_capacity"]
    - 0.08 * models["institutional_embedding"]
    + 0.12 * models["ethical_visibility"]
    + 0.10 * models["stakeholder_visibility"]
    + 0.10 * models["evidence_responsiveness"]
)

models["monoculture_risk"] = (
    0.28 * models["institutional_embedding"]
    + 0.20 * (1 - models["model_plurality"])
    + 0.18 * (1 - models["model_flexibility"])
    + 0.18 * (1 - models["revision_capacity"])
    + 0.16 * (1 - models["stakeholder_visibility"])
)

models.sort_values("adaptive_model_score", ascending=True).plot(
    kind="barh",
    x="model_name",
    y="adaptive_model_score",
    legend=False,
    figsize=(11, 8),
)
plt.title("Adaptive Mental-Model Scores")
plt.xlabel("Adaptive model score")
plt.ylabel("Mental model")
plt.tight_layout()
plt.savefig(FIGURES / "adaptive_mental_model_scores.png", dpi=160)
plt.close()

models.sort_values("monoculture_risk", ascending=True).plot(
    kind="barh",
    x="model_name",
    y="monoculture_risk",
    legend=False,
    figsize=(11, 8),
)
plt.title("Model Monoculture and Lock-In Risk")
plt.xlabel("Risk score")
plt.ylabel("Mental model")
plt.tight_layout()
plt.savefig(FIGURES / "model_monoculture_risk.png", dpi=160)
plt.close()

causal["causal_adequacy_score"] = (
    0.24 * causal["environment_fit"]
    + 0.20 * causal["feedback_awareness"]
    + 0.18 * causal["delay_awareness"]
    + 0.18 * causal["nonlinearity_awareness"]
    + 0.20 * causal["second_order_awareness"]
    - 0.18 * causal["blind_spot_risk"]
)

plt.figure(figsize=(10, 7))
plt.scatter(
    causal["blind_spot_risk"],
    causal["causal_adequacy_score"],
    s=causal["environment_fit"] * 450,
    alpha=0.70,
)

for _, row in causal.iterrows():
    plt.annotate(row["frame_id"], (row["blind_spot_risk"], row["causal_adequacy_score"]))

plt.title("Causal Adequacy vs Blind-Spot Risk")
plt.xlabel("Blind-spot risk")
plt.ylabel("Causal adequacy score")
plt.tight_layout()
plt.savefig(FIGURES / "causal_adequacy_vs_blind_spot.png", dpi=160)
plt.close()

stress["stress_score"] = (
    0.34 * stress["performance_under_stress"]
    + 0.24 * stress["revision_speed"]
    - 0.22 * stress["blind_spot_exposure"]
    + 0.30 * stress["strategic_robustness"]
)

stress.sort_values("stress_score", ascending=False).to_csv(
    TABLES / "advanced_scenario_stress_rankings.csv",
    index=False,
)

print("Advanced model analytics complete.")
print(f"Wrote: {FIGURES / 'adaptive_mental_model_scores.png'}")
print(f"Wrote: {FIGURES / 'model_monoculture_risk.png'}")
print(f"Wrote: {FIGURES / 'causal_adequacy_vs_blind_spot.png'}")
print(f"Wrote: {TABLES / 'advanced_scenario_stress_rankings.csv'}")
