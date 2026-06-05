#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Ethics of Strategic Ideation.

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


ideas = read_csv(RAW / "ethical_ideas.csv")
impacts = read_csv(RAW / "stakeholder_impacts.csv")
claims = read_csv(RAW / "claim_evidence_ethics.csv")
ai_uses = read_csv(RAW / "ai_use_ethics.csv")
accountability = read_csv(RAW / "accountability_redress.csv")

idea_names = {row["idea_id"]: row["idea"] for row in ideas}

# ---------------------------------------------------------------------
# 1. Ethical idea legitimacy and risk
# ---------------------------------------------------------------------

idea_rows: list[dict[str, object]] = []
for row in ideas:
    legitimacy = (
        0.12 * f(row, "stakeholder_voice")
        + 0.12 * f(row, "evidence_integrity")
        + 0.10 * f(row, "burden_visibility")
        + 0.09 * f(row, "uncertainty_visibility")
        + 0.08 * f(row, "reversibility")
        + 0.11 * f(row, "long_term_responsibility")
        + 0.07 * f(row, "ai_governance")
        + 0.09 * f(row, "accountability")
        + 0.07 * f(row, "redress_quality")
        + 0.08 * f(row, "problem_frame_integrity")
        + 0.07 * f(row, "power_review")
    )
    risk = (
        0.13 * (1 - f(row, "stakeholder_voice"))
        + 0.12 * (1 - f(row, "evidence_integrity"))
        + 0.12 * (1 - f(row, "burden_visibility"))
        + 0.10 * (1 - f(row, "uncertainty_visibility"))
        + 0.09 * (1 - f(row, "reversibility"))
        + 0.10 * (1 - f(row, "long_term_responsibility"))
        + 0.10 * (1 - f(row, "ai_governance"))
        + 0.08 * (1 - f(row, "accountability"))
        + 0.07 * (1 - f(row, "redress_quality"))
        + 0.05 * (1 - f(row, "problem_frame_integrity"))
        + 0.04 * (1 - f(row, "power_review"))
    )

    if legitimacy >= 0.76:
        diagnosis = "strong_ethical_foundation"
    elif f(row, "stakeholder_voice") < 0.50:
        diagnosis = "stakeholder_voice_gap"
    elif f(row, "burden_visibility") < 0.50:
        diagnosis = "burden_visibility_gap"
    elif f(row, "evidence_integrity") < 0.60:
        diagnosis = "evidence_integrity_gap"
    elif f(row, "ai_governance") < 0.45:
        diagnosis = "ai_governance_review_required"
    elif f(row, "redress_quality") < 0.45:
        diagnosis = "redress_gap"
    elif f(row, "reversibility") < 0.45:
        diagnosis = "irreversibility_risk"
    elif f(row, "power_review") < 0.45:
        diagnosis = "power_and_realism_review_required"
    else:
        diagnosis = "targeted_ethics_repair"

    weakest_dimension = min(
        [
            ("stakeholder_voice", f(row, "stakeholder_voice")),
            ("evidence_integrity", f(row, "evidence_integrity")),
            ("burden_visibility", f(row, "burden_visibility")),
            ("uncertainty_visibility", f(row, "uncertainty_visibility")),
            ("reversibility", f(row, "reversibility")),
            ("long_term_responsibility", f(row, "long_term_responsibility")),
            ("ai_governance", f(row, "ai_governance")),
            ("accountability", f(row, "accountability")),
            ("redress_quality", f(row, "redress_quality")),
            ("problem_frame_integrity", f(row, "problem_frame_integrity")),
            ("power_review", f(row, "power_review")),
        ],
        key=lambda item: item[1],
    )[0]

    idea_rows.append({
        "idea_id": row["idea_id"],
        "idea": row["idea"],
        "idea_type": row["idea_type"],
        "ethical_legitimacy": round(legitimacy, 4),
        "ethical_risk": round(risk, 4),
        "weakest_dimension": weakest_dimension,
        "diagnosis": diagnosis,
        "description": row["description"],
    })

idea_rows.sort(key=lambda item: item["ethical_legitimacy"], reverse=True)
write_csv(TABLES / "ethical_idea_scores.csv", idea_rows)
write_csv(PROCESSED / "ethical_idea_scores.csv", idea_rows)

# ---------------------------------------------------------------------
# 2. Stakeholder impact and burden distribution
# ---------------------------------------------------------------------

impact_rows: list[dict[str, object]] = []
for row in impacts:
    impact_legitimacy = (
        0.12 * f(row, "benefit_score")
        + 0.16 * (1 - f(row, "burden_score"))
        + 0.14 * (1 - f(row, "risk_exposure"))
        + 0.14 * f(row, "voice_quality")
        + 0.12 * f(row, "consent_quality")
        + 0.12 * f(row, "redress_access")
        + 0.10 * (1 - f(row, "trust_sensitivity"))
        + 0.10 * (1 - f(row, "long_term_exposure"))
    )
    burden_risk = (
        0.20 * f(row, "burden_score")
        + 0.20 * f(row, "risk_exposure")
        + 0.14 * (1 - f(row, "voice_quality"))
        + 0.12 * (1 - f(row, "consent_quality"))
        + 0.12 * (1 - f(row, "redress_access"))
        + 0.12 * f(row, "trust_sensitivity")
        + 0.10 * f(row, "long_term_exposure")
    )
    impact_rows.append({
        "impact_id": row["impact_id"],
        "idea_id": row["idea_id"],
        "idea": idea_names[row["idea_id"]],
        "stakeholder_group": row["stakeholder_group"],
        "stakeholder_impact_legitimacy": round(impact_legitimacy, 4),
        "burden_risk": round(burden_risk, 4),
        "review_action": row["review_action"],
    })

impact_rows.sort(key=lambda item: item["burden_risk"], reverse=True)
write_csv(TABLES / "stakeholder_impact_scores.csv", impact_rows)

# ---------------------------------------------------------------------
# 3. Claim-evidence ethical integrity
# ---------------------------------------------------------------------

claim_rows: list[dict[str, object]] = []
for row in claims:
    integrity = (
        0.14 * f(row, "source_quality")
        + 0.14 * f(row, "confidence_level")
        + 0.13 * f(row, "uncertainty_visibility")
        + 0.13 * f(row, "counterevidence_visibility")
        + 0.12 * f(row, "transfer_limits")
        + 0.14 * (1 - f(row, "overclaim_risk"))
        + 0.20 * f(row, "ethical_salience")
    )
    claim_rows.append({
        "claim_id": row["claim_id"],
        "idea_id": row["idea_id"],
        "idea": idea_names[row["idea_id"]],
        "claim_type": row["claim_type"],
        "claim_text": row["claim_text"],
        "claim_evidence_ethics_score": round(integrity, 4),
        "overclaim_risk": f(row, "overclaim_risk"),
        "review_action": row["review_action"],
    })

claim_rows.sort(key=lambda item: item["claim_evidence_ethics_score"])
write_csv(TABLES / "claim_evidence_ethics_scores.csv", claim_rows)

# ---------------------------------------------------------------------
# 4. AI ethics review
# ---------------------------------------------------------------------

ai_rows: list[dict[str, object]] = []
for row in ai_uses:
    governance = (
        0.12 * f(row, "disclosure_quality")
        + 0.13 * f(row, "source_traceability")
        + 0.13 * f(row, "human_review")
        + 0.13 * f(row, "bias_review")
        + 0.12 * f(row, "stakeholder_review")
        + 0.12 * f(row, "uncertainty_preservation")
        + 0.12 * f(row, "accountability_clarity")
        + 0.13 * (1 - f(row, "automation_risk"))
    )
    ai_rows.append({
        "ai_use_id": row["ai_use_id"],
        "idea_id": row["idea_id"],
        "idea": idea_names[row["idea_id"]],
        "ai_use_case": row["ai_use_case"],
        "ai_ethics_governance_score": round(governance, 4),
        "automation_risk": f(row, "automation_risk"),
        "review_action": row["review_action"],
    })

ai_rows.sort(key=lambda item: item["ai_ethics_governance_score"])
write_csv(TABLES / "ai_ethics_scores.csv", ai_rows)

# ---------------------------------------------------------------------
# 5. Accountability and redress
# ---------------------------------------------------------------------

accountability_rows: list[dict[str, object]] = []
for row in accountability:
    score = (
        0.13 * f(row, "owner_clarity")
        + 0.13 * f(row, "monitoring_quality")
        + 0.12 * f(row, "escalation_path")
        + 0.13 * f(row, "appeal_process")
        + 0.13 * f(row, "correction_capacity")
        + 0.13 * f(row, "redress_access")
        + 0.14 * f(row, "revision_trigger_quality")
        + 0.12 * f(row, "public_accountability")
    )
    accountability_rows.append({
        "accountability_id": row["accountability_id"],
        "idea_id": row["idea_id"],
        "idea": idea_names[row["idea_id"]],
        "accountability_redress_score": round(score, 4),
        "review_action": row["review_action"],
    })

accountability_rows.sort(key=lambda item: item["accountability_redress_score"])
write_csv(TABLES / "accountability_redress_scores.csv", accountability_rows)

summary = {
    "ethical_ideas": idea_rows,
    "stakeholder_impacts": impact_rows,
    "claim_evidence_ethics": claim_rows,
    "ai_ethics": ai_rows,
    "accountability_redress": accountability_rows,
}
(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

report = [
    "# Ethics of Strategic Ideation Diagnostic Report",
    "",
    "## Executive summary",
    "",
    "This diagnostic evaluates whether strategic ideas have been framed, generated, evaluated, and prepared for decision in ethically responsible ways. It reviews stakeholder voice, evidence integrity, burden visibility, uncertainty, reversibility, long-term responsibility, AI governance, accountability, redress, problem-frame integrity, and power review.",
    "",
    "## Ethical legitimacy ranking",
    "",
]
for item in idea_rows:
    report.append(
        f"- **{item['idea_id']} — {item['idea']}**: ethical legitimacy {item['ethical_legitimacy']}; "
        f"ethical risk {item['ethical_risk']}; weakest dimension: {item['weakest_dimension']}; diagnosis: {item['diagnosis']}."
    )

report.extend(["", "## Stakeholder burden and impact priorities", ""])
for item in impact_rows:
    report.append(
        f"- **{item['idea']} / {item['stakeholder_group']}**: burden risk {item['burden_risk']}; "
        f"impact legitimacy {item['stakeholder_impact_legitimacy']}; action: {item['review_action']}."
    )

report.extend(["", "## Claim-evidence ethical integrity", ""])
for item in claim_rows:
    report.append(
        f"- **{item['idea']} / {item['claim_type']}**: claim-evidence ethics score {item['claim_evidence_ethics_score']}; "
        f"overclaim risk {item['overclaim_risk']}; action: {item['review_action']}."
    )

report.extend(["", "## AI-assisted ideation governance", ""])
for item in ai_rows:
    report.append(
        f"- **{item['idea']} / {item['ai_use_case']}**: AI ethics governance score {item['ai_ethics_governance_score']}; "
        f"automation risk {item['automation_risk']}; action: {item['review_action']}."
    )

report.extend(["", "## Accountability and redress review", ""])
for item in accountability_rows:
    report.append(
        f"- **{item['idea']}**: accountability and redress score {item['accountability_redress_score']}; action: {item['review_action']}."
    )

report.extend([
    "",
    "## Professional interpretation",
    "",
    "Ethical strategic ideation asks whether ideas are responsibly framed, whether affected stakeholders have meaningful voice, whether claims match evidence, whether burdens are visible, whether uncertainty and reversibility are designed into the pathway, whether AI assistance is governed, and whether accountability and redress exist before implementation begins.",
])

(REPORTS / "ethical_ideation_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

print("Advanced ethical ideation diagnostics complete.")
print(f"Wrote: {TABLES / 'ethical_idea_scores.csv'}")
print(f"Wrote: {TABLES / 'stakeholder_impact_scores.csv'}")
print(f"Wrote: {TABLES / 'claim_evidence_ethics_scores.csv'}")
print(f"Wrote: {TABLES / 'ai_ethics_scores.csv'}")
print(f"Wrote: {TABLES / 'accountability_redress_scores.csv'}")
print(f"Wrote: {REPORTS / 'ethical_ideation_diagnostic_report.md'}")
