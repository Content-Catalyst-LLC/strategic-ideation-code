#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Bad Ideas and Strategic Failure.

Uses only Python standard library.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "outputs" / "tables"
REPORTS = ROOT / "outputs" / "reports"

for path in (PROCESSED, TABLES, REPORTS):
    path.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def f(row: dict[str, str], key: str) -> float:
    return float(row[key])


ideas = read_csv(RAW / "bad_ideas.csv")
pathways = read_csv(RAW / "failure_pathways.csv")
evidence = read_csv(RAW / "evidence_overclaim.csv")
implementation = read_csv(RAW / "implementation_incentives.csv")
pnl = read_csv(RAW / "power_narrative_learning.csv")

idea_names = {row["idea_id"]: row["idea"] for row in ideas}

# ---------------------------------------------------------------------
# 1. Bad idea risk and idea quality
# ---------------------------------------------------------------------

idea_rows: list[dict[str, object]] = []
for row in ideas:
    idea_quality = (
        0.12 * f(row, "problem_frame_integrity")
        + 0.11 * f(row, "mechanism_clarity")
        + 0.13 * f(row, "evidence_quality")
        + 0.10 * f(row, "context_fit")
        + 0.12 * f(row, "implementation_readiness")
        + 0.10 * f(row, "incentive_alignment")
        + 0.10 * f(row, "ethical_visibility")
        + 0.09 * f(row, "strategic_merit")
        + 0.08 * f(row, "learning_design")
        + 0.05 * f(row, "narrative_honesty")
    )
    power_distortion = f(row, "institutional_support") - f(row, "strategic_merit")
    failure_risk = (
        0.12 * (1 - f(row, "problem_frame_integrity"))
        + 0.11 * (1 - f(row, "mechanism_clarity"))
        + 0.13 * (1 - f(row, "evidence_quality"))
        + 0.10 * (1 - f(row, "context_fit"))
        + 0.12 * (1 - f(row, "implementation_readiness"))
        + 0.10 * (1 - f(row, "incentive_alignment"))
        + 0.10 * (1 - f(row, "ethical_visibility"))
        + 0.08 * (1 - f(row, "learning_design"))
        + 0.05 * (1 - f(row, "narrative_honesty"))
        + 0.05 * max(0.0, power_distortion)
        + 0.04 * f(row, "ai_fluency_risk")
    )
    overclaim_signal = max(0.0, f(row, "institutional_support") - f(row, "evidence_quality")) + 0.5 * f(row, "ai_fluency_risk")

    if failure_risk > 0.60:
        diagnosis = "high_bad_idea_risk"
    elif power_distortion > 0.22:
        diagnosis = "power_protected_weakness"
    elif f(row, "evidence_quality") < 0.50:
        diagnosis = "evidence_failure"
    elif f(row, "implementation_readiness") < 0.45:
        diagnosis = "implementation_fantasy"
    elif f(row, "ethical_visibility") < 0.45:
        diagnosis = "hidden_burden_or_harm"
    elif f(row, "learning_design") < 0.45:
        diagnosis = "no_stop_rules_or_revision_triggers"
    elif f(row, "ai_fluency_risk") > 0.70:
        diagnosis = "ai_fluency_trap_review_required"
    else:
        diagnosis = "review_before_advancement"

    weakest_dimension = min(
        [
            ("problem_frame_integrity", f(row, "problem_frame_integrity")),
            ("mechanism_clarity", f(row, "mechanism_clarity")),
            ("evidence_quality", f(row, "evidence_quality")),
            ("context_fit", f(row, "context_fit")),
            ("implementation_readiness", f(row, "implementation_readiness")),
            ("incentive_alignment", f(row, "incentive_alignment")),
            ("ethical_visibility", f(row, "ethical_visibility")),
            ("learning_design", f(row, "learning_design")),
            ("narrative_honesty", f(row, "narrative_honesty")),
        ],
        key=lambda item: item[1],
    )[0]

    idea_rows.append({
        "idea_id": row["idea_id"],
        "idea": row["idea"],
        "idea_type": row["idea_type"],
        "idea_quality": round(idea_quality, 4),
        "failure_risk": round(failure_risk, 4),
        "power_distortion": round(power_distortion, 4),
        "overclaim_signal": round(overclaim_signal, 4),
        "weakest_dimension": weakest_dimension,
        "diagnosis": diagnosis,
        "description": row["description"],
    })

idea_rows.sort(key=lambda item: item["failure_risk"], reverse=True)
write_csv(TABLES / "bad_idea_risk_scores.csv", idea_rows)
write_csv(PROCESSED / "bad_idea_risk_scores.csv", idea_rows)

# ---------------------------------------------------------------------
# 2. Failure pathway scoring
# ---------------------------------------------------------------------

pathway_rows: list[dict[str, object]] = []
for row in pathways:
    pathway_risk = (
        0.16 * f(row, "premature_commitment")
        + 0.15 * f(row, "execution_strain")
        + 0.14 * f(row, "defensive_narrative")
        + 0.15 * f(row, "stakeholder_harm")
        + 0.14 * f(row, "learning_distortion")
        + 0.16 * f(row, "escalation_risk")
        + 0.10 * (1 - f(row, "mitigation_quality"))
    )
    pathway_rows.append({
        "pathway_id": row["pathway_id"],
        "idea_id": row["idea_id"],
        "idea": idea_names[row["idea_id"]],
        "weakness_type": row["weakness_type"],
        "failure_pathway_risk": round(pathway_risk, 4),
        "review_action": row["review_action"],
    })

pathway_rows.sort(key=lambda item: item["failure_pathway_risk"], reverse=True)
write_csv(TABLES / "failure_pathway_scores.csv", pathway_rows)

# ---------------------------------------------------------------------
# 3. Evidence and overclaim risk
# ---------------------------------------------------------------------

evidence_rows: list[dict[str, object]] = []
for row in evidence:
    claim_integrity = (
        0.15 * f(row, "source_quality")
        + 0.13 * f(row, "confidence_level")
        + 0.15 * f(row, "evidence_relevance")
        + 0.15 * f(row, "counterevidence_visibility")
        + 0.14 * f(row, "transfer_fit")
        + 0.14 * (1 - f(row, "overclaim_risk"))
        + 0.14 * (1 - f(row, "narrative_pressure"))
    )
    overclaim_exposure = (
        0.32 * f(row, "overclaim_risk")
        + 0.20 * f(row, "narrative_pressure")
        + 0.14 * (1 - f(row, "source_quality"))
        + 0.12 * (1 - f(row, "evidence_relevance"))
        + 0.12 * (1 - f(row, "counterevidence_visibility"))
        + 0.10 * (1 - f(row, "transfer_fit"))
    )
    evidence_rows.append({
        "claim_id": row["claim_id"],
        "idea_id": row["idea_id"],
        "idea": idea_names[row["idea_id"]],
        "claim_type": row["claim_type"],
        "claim_integrity_score": round(claim_integrity, 4),
        "overclaim_exposure": round(overclaim_exposure, 4),
        "review_action": row["review_action"],
    })

evidence_rows.sort(key=lambda item: item["overclaim_exposure"], reverse=True)
write_csv(TABLES / "evidence_overclaim_scores.csv", evidence_rows)

# ---------------------------------------------------------------------
# 4. Implementation and incentive risk
# ---------------------------------------------------------------------

impl_rows: list[dict[str, object]] = []
for row in implementation:
    readiness = (
        0.13 * f(row, "capacity_fit")
        + 0.12 * f(row, "role_clarity")
        + 0.12 * f(row, "dependency_visibility")
        + 0.10 * f(row, "technical_readiness")
        + 0.13 * f(row, "stakeholder_trust")
        + 0.14 * f(row, "incentive_alignment")
        + 0.10 * (1 - f(row, "gaming_risk"))
        + 0.08 * (1 - f(row, "hidden_labor"))
        + 0.08 * (1 - f(row, "adoption_assumption_risk"))
    )
    implementation_risk = (
        0.12 * (1 - f(row, "capacity_fit"))
        + 0.11 * (1 - f(row, "role_clarity"))
        + 0.11 * (1 - f(row, "dependency_visibility"))
        + 0.10 * (1 - f(row, "technical_readiness"))
        + 0.12 * (1 - f(row, "stakeholder_trust"))
        + 0.13 * (1 - f(row, "incentive_alignment"))
        + 0.13 * f(row, "gaming_risk")
        + 0.10 * f(row, "hidden_labor")
        + 0.08 * f(row, "adoption_assumption_risk")
    )
    impl_rows.append({
        "impl_id": row["impl_id"],
        "idea_id": row["idea_id"],
        "idea": idea_names[row["idea_id"]],
        "implementation_readiness_score": round(readiness, 4),
        "implementation_incentive_risk": round(implementation_risk, 4),
        "review_action": row["review_action"],
    })

impl_rows.sort(key=lambda item: item["implementation_incentive_risk"], reverse=True)
write_csv(TABLES / "implementation_incentive_scores.csv", impl_rows)

# ---------------------------------------------------------------------
# 5. Power, narrative, learning, and stop-rule quality
# ---------------------------------------------------------------------

pnl_rows: list[dict[str, object]] = []
for row in pnl:
    learning_integrity = (
        0.12 * (1 - f(row, "sponsor_power"))
        + 0.10 * (1 - f(row, "narrative_strength"))
        + 0.13 * f(row, "dissent_visibility")
        + 0.13 * f(row, "red_team_quality")
        + 0.15 * f(row, "stop_rule_quality")
        + 0.15 * f(row, "revision_trigger_quality")
        + 0.12 * f(row, "decision_memory_quality")
        + 0.10 * f(row, "ai_review_quality")
    )
    power_narrative_risk = (
        0.20 * f(row, "power_protection_risk")
        + 0.15 * f(row, "sponsor_power")
        + 0.13 * f(row, "narrative_strength")
        + 0.12 * (1 - f(row, "dissent_visibility"))
        + 0.12 * (1 - f(row, "red_team_quality"))
        + 0.10 * (1 - f(row, "stop_rule_quality"))
        + 0.10 * (1 - f(row, "revision_trigger_quality"))
        + 0.08 * (1 - f(row, "ai_review_quality"))
    )
    pnl_rows.append({
        "pnl_id": row["pnl_id"],
        "idea_id": row["idea_id"],
        "idea": idea_names[row["idea_id"]],
        "learning_integrity_score": round(learning_integrity, 4),
        "power_narrative_risk": round(power_narrative_risk, 4),
        "review_action": row["review_action"],
    })

pnl_rows.sort(key=lambda item: item["power_narrative_risk"], reverse=True)
write_csv(TABLES / "power_narrative_learning_scores.csv", pnl_rows)

summary = {
    "bad_idea_risk": idea_rows,
    "failure_pathways": pathway_rows,
    "evidence_overclaim": evidence_rows,
    "implementation_incentives": impl_rows,
    "power_narrative_learning": pnl_rows,
}
(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

report = [
    "# Bad Ideas and Strategic Failure Diagnostic Report",
    "",
    "## Executive summary",
    "",
    "This diagnostic evaluates whether strategic ideas are at risk of becoming strategic failures through weak problem framing, vague causal mechanism, thin evidence, poor context fit, implementation fantasy, incentive failure, hidden ethical burden, power distortion, narrative overclaiming, AI fluency, and missing stop rules.",
    "",
    "## Bad-idea risk ranking",
    "",
]
for item in idea_rows:
    report.append(
        f"- **{item['idea_id']} — {item['idea']}**: quality {item['idea_quality']}; "
        f"failure risk {item['failure_risk']}; power distortion {item['power_distortion']}; "
        f"weakest dimension: {item['weakest_dimension']}; diagnosis: {item['diagnosis']}."
    )

report.extend(["", "## Failure pathway review", ""])
for item in pathway_rows:
    report.append(
        f"- **{item['idea']}** ({item['weakness_type']}): failure pathway risk {item['failure_pathway_risk']}; action: {item['review_action']}."
    )

report.extend(["", "## Evidence and overclaim review", ""])
for item in evidence_rows:
    report.append(
        f"- **{item['idea']}** ({item['claim_type']}): claim integrity {item['claim_integrity_score']}; overclaim exposure {item['overclaim_exposure']}; action: {item['review_action']}."
    )

report.extend(["", "## Implementation and incentive review", ""])
for item in impl_rows:
    report.append(
        f"- **{item['idea']}**: implementation readiness {item['implementation_readiness_score']}; implementation/incentive risk {item['implementation_incentive_risk']}; action: {item['review_action']}."
    )

report.extend(["", "## Power, narrative, and learning review", ""])
for item in pnl_rows:
    report.append(
        f"- **{item['idea']}**: learning integrity {item['learning_integrity_score']}; power/narrative risk {item['power_narrative_risk']}; action: {item['review_action']}."
    )

report.extend([
    "",
    "## Professional interpretation",
    "",
    "Bad ideas should not be diagnosed only by whether they sound weak. They should be evaluated through problem-frame integrity, causal mechanism, evidence quality, implementation readiness, incentive alignment, ethical visibility, power distortion, narrative honesty, AI fluency, learning design, and stop-rule quality.",
])

(REPORTS / "bad_idea_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

print("Advanced bad-idea diagnostics complete.")
print(f"Wrote: {TABLES / 'bad_idea_risk_scores.csv'}")
print(f"Wrote: {TABLES / 'failure_pathway_scores.csv'}")
print(f"Wrote: {TABLES / 'evidence_overclaim_scores.csv'}")
print(f"Wrote: {TABLES / 'implementation_incentive_scores.csv'}")
print(f"Wrote: {TABLES / 'power_narrative_learning_scores.csv'}")
print(f"Wrote: {REPORTS / 'bad_idea_diagnostic_report.md'}")
