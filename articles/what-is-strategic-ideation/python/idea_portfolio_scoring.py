#!/usr/bin/env python3
"""
Strategic ideation portfolio scoring workflow.

This script uses synthetic data to demonstrate:
- weighted idea scoring
- uncertainty penalty
- assumption-risk adjustment
- revision flags
- exported tables

It intentionally uses only the Python standard library.
"""

from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw"
OUT = ROOT / "outputs" / "tables"
PROCESSED = ROOT / "data" / "processed"

OUT.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


ideas = read_csv(DATA / "synthetic_ideas.csv")
criteria = read_csv(DATA / "criteria.csv")
assumptions = read_csv(DATA / "assumptions.csv")

weights = {row["criterion"]: float(row["weight"]) for row in criteria}

assumption_risk_by_idea: dict[str, float] = {}

for idea_id in {row["idea_id"] for row in ideas}:
    linked = [a for a in assumptions if a["idea_id"] == idea_id]
    if not linked:
        assumption_risk_by_idea[idea_id] = 0.0
        continue

    risks = []
    for item in linked:
        confidence = float(item["confidence"])
        criticality = float(item["criticality"])
        risks.append((1.0 - confidence) * criticality)

    assumption_risk_by_idea[idea_id] = mean(risks)


scored_rows: list[dict[str, object]] = []

for idea in ideas:
    idea_id = idea["idea_id"]
    uncertainty = float(idea["uncertainty"])
    assumption_risk = assumption_risk_by_idea.get(idea_id, 0.0)

    positive_score = (
        weights["strategic_fit"] * float(idea["strategic_fit"])
        + weights["feasibility"] * float(idea["feasibility"])
        + weights["systems_leverage"] * float(idea["systems_leverage"])
        + weights["learning_value"] * float(idea["learning_value"])
        + weights["ethical_legitimacy"] * float(idea["ethical_legitimacy"])
    )

    uncertainty_penalty = weights["uncertainty_penalty"] * uncertainty
    assumption_penalty = 0.12 * assumption_risk
    final_score = positive_score - uncertainty_penalty - assumption_penalty

    if final_score >= 0.78 and assumption_risk < 0.30:
        recommendation = "advance"
    elif final_score >= 0.68:
        recommendation = "prototype_or_revise"
    else:
        recommendation = "hold_for_reframing"

    scored_rows.append(
        {
            "idea_id": idea_id,
            "idea_name": idea["idea_name"],
            "category": idea["category"],
            "final_score": round(final_score, 4),
            "assumption_risk": round(assumption_risk, 4),
            "uncertainty": uncertainty,
            "estimated_cost": idea["estimated_cost"],
            "implementation_months": idea["implementation_months"],
            "recommendation": recommendation,
        }
    )

scored_rows.sort(key=lambda row: row["final_score"], reverse=True)

fields = [
    "idea_id",
    "idea_name",
    "category",
    "final_score",
    "assumption_risk",
    "uncertainty",
    "estimated_cost",
    "implementation_months",
    "recommendation",
]

write_csv(OUT / "idea_portfolio_scores.csv", scored_rows, fields)
write_csv(PROCESSED / "idea_portfolio_scores.csv", scored_rows, fields)

print("Strategic ideation portfolio scores")
print("-----------------------------------")
for row in scored_rows:
    print(
        f"{row['idea_id']} | {row['final_score']:.4f} | "
        f"{row['recommendation']} | {row['idea_name']}"
    )

print(f"\nWrote: {OUT / 'idea_portfolio_scores.csv'}")
