#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Strategic Ideation and Institutional Power.

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


ideas = read_csv(RAW / "power_ideas.csv")
agenda = read_csv(RAW / "agenda_power.csv")
evidence = read_csv(RAW / "evidence_parity.csv")
voice = read_csv(RAW / "participation_voice.csv")
rma = read_csv(RAW / "resource_memory_ai.csv")

idea_names = {row["idea_id"]: row["idea"] for row in ideas}

# ---------------------------------------------------------------------
# 1. Power distortion and merit/support gaps
# ---------------------------------------------------------------------

idea_rows: list[dict[str, object]] = []
for row in ideas:
    merit_score = (
        0.28 * f(row, "strategic_merit")
        + 0.21 * f(row, "evidence_strength")
        + 0.16 * f(row, "stakeholder_influence")
        + 0.13 * f(row, "dissent_protection")
        + 0.12 * f(row, "classification_visibility")
        + 0.10 * f(row, "ethical_visibility")
    )
    institutional_support = (
        0.28 * f(row, "executive_sponsorship")
        + 0.24 * f(row, "resource_fit")
        + 0.24 * f(row, "power_alignment")
        + 0.24 * f(row, "advancement_likelihood")
    )
    power_distortion = institutional_support - merit_score
    voice_gap = f(row, "advancement_likelihood") - f(row, "stakeholder_influence")
    evidence_asymmetry_risk = max(0.0, f(row, "power_alignment") - f(row, "evidence_strength"))
    sponsorship_merit_gap = f(row, "executive_sponsorship") - f(row, "strategic_merit")

    if power_distortion > 0.20:
        diagnosis = "power_alignment_may_be_driving_advancement"
    elif voice_gap > 0.25:
        diagnosis = "advancement_without_stakeholder_influence"
    elif evidence_asymmetry_risk > 0.20:
        diagnosis = "power_aligned_idea_with_weak_evidence"
    elif f(row, "dissent_protection") < 0.45:
        diagnosis = "dissent_suppression_risk"
    elif f(row, "classification_visibility") < 0.50:
        diagnosis = "classification_power_gap"
    elif merit_score > institutional_support + 0.18:
        diagnosis = "high_merit_low_support_idea"
    else:
        diagnosis = "review_with_standard_power_aware_governance"

    idea_rows.append({
        "idea_id": row["idea_id"],
        "idea": row["idea"],
        "idea_type": row["idea_type"],
        "merit_score": round(merit_score, 4),
        "institutional_support": round(institutional_support, 4),
        "power_distortion": round(power_distortion, 4),
        "voice_gap": round(voice_gap, 4),
        "evidence_asymmetry_risk": round(evidence_asymmetry_risk, 4),
        "sponsorship_merit_gap": round(sponsorship_merit_gap, 4),
        "diagnosis": diagnosis,
        "description": row["description"],
    })

idea_rows.sort(key=lambda item: item["power_distortion"], reverse=True)
write_csv(TABLES / "power_idea_scores.csv", idea_rows)
write_csv(PROCESSED / "power_idea_scores.csv", idea_rows)

# ---------------------------------------------------------------------
# 2. Agenda-setting review
# ---------------------------------------------------------------------

agenda_rows: list[dict[str, object]] = []
for row in agenda:
    agenda_legitimacy = (
        0.18 * f(row, "stakeholder_priority")
        + 0.16 * f(row, "frontline_priority")
        + 0.18 * f(row, "evidence_signal_strength")
        + 0.18 * f(row, "long_term_relevance")
        + 0.10 * f(row, "leadership_priority")
        + 0.10 * (1 - f(row, "political_safety"))
        + 0.10 * (1 - f(row, "agenda_exclusion_risk"))
    )
    power_filtered_attention = (
        0.30 * f(row, "leadership_priority")
        + 0.25 * f(row, "political_safety")
        + 0.20 * f(row, "agenda_exclusion_risk")
        + 0.15 * (1 - f(row, "stakeholder_priority"))
        + 0.10 * (1 - f(row, "long_term_relevance"))
    )
    agenda_rows.append({
        "agenda_id": row["agenda_id"],
        "idea_id": row["idea_id"],
        "idea": idea_names[row["idea_id"]],
        "agenda_source": row["agenda_source"],
        "agenda_legitimacy": round(agenda_legitimacy, 4),
        "power_filtered_attention": round(power_filtered_attention, 4),
        "review_action": row["review_action"],
    })

agenda_rows.sort(key=lambda item: item["power_filtered_attention"], reverse=True)
write_csv(TABLES / "agenda_power_scores.csv", agenda_rows)

# ---------------------------------------------------------------------
# 3. Evidence parity review
# ---------------------------------------------------------------------

evidence_rows: list[dict[str, object]] = []
for row in evidence:
    parity_score = (
        0.16 * f(row, "evidence_strength")
        + 0.14 * f(row, "evidence_threshold_applied")
        + 0.15 * f(row, "counterevidence_visibility")
        + 0.14 * f(row, "source_diversity")
        + 0.15 * f(row, "stakeholder_evidence_quality")
        + 0.12 * f(row, "expertise_balance")
        + 0.14 * (1 - f(row, "overclaim_risk"))
    )
    threshold_gap = f(row, "evidence_threshold_applied") - f(row, "evidence_strength")
    evidence_rows.append({
        "evidence_id": row["evidence_id"],
        "idea_id": row["idea_id"],
        "idea": idea_names[row["idea_id"]],
        "evidence_type": row["evidence_type"],
        "evidence_parity_score": round(parity_score, 4),
        "threshold_gap": round(threshold_gap, 4),
        "overclaim_risk": f(row, "overclaim_risk"),
        "review_action": row["review_action"],
    })

evidence_rows.sort(key=lambda item: item["evidence_parity_score"])
write_csv(TABLES / "evidence_parity_scores.csv", evidence_rows)

# ---------------------------------------------------------------------
# 4. Participation influence and tokenism
# ---------------------------------------------------------------------

voice_rows: list[dict[str, object]] = []
for row in voice:
    influence_score = (
        0.12 * f(row, "invited_voice")
        + 0.18 * f(row, "actual_influence")
        + 0.14 * f(row, "agenda_influence")
        + 0.14 * f(row, "criteria_influence")
        + 0.16 * f(row, "decision_influence")
        + 0.14 * f(row, "dissent_safety")
        + 0.12 * f(row, "redress_access")
    )
    tokenism_risk = (
        0.24 * f(row, "tokenism_risk")
        + 0.16 * (1 - f(row, "actual_influence"))
        + 0.14 * (1 - f(row, "agenda_influence"))
        + 0.14 * (1 - f(row, "criteria_influence"))
        + 0.14 * (1 - f(row, "decision_influence"))
        + 0.10 * (1 - f(row, "dissent_safety"))
        + 0.08 * (1 - f(row, "redress_access"))
    )
    influence_gap = f(row, "invited_voice") - f(row, "actual_influence")
    voice_rows.append({
        "voice_id": row["voice_id"],
        "idea_id": row["idea_id"],
        "idea": idea_names[row["idea_id"]],
        "participation_mode": row["participation_mode"],
        "participation_influence_score": round(influence_score, 4),
        "tokenism_risk": round(tokenism_risk, 4),
        "influence_gap": round(influence_gap, 4),
        "review_action": row["review_action"],
    })

voice_rows.sort(key=lambda item: item["tokenism_risk"], reverse=True)
write_csv(TABLES / "participation_voice_scores.csv", voice_rows)

# ---------------------------------------------------------------------
# 5. Resource, memory, and AI mediation review
# ---------------------------------------------------------------------

rma_rows: list[dict[str, object]] = []
for row in rma:
    resource_memory_integrity = (
        0.14 * f(row, "resource_support")
        + 0.10 * f(row, "incentive_fit")
        + 0.16 * f(row, "memory_traceability")
        + 0.14 * f(row, "prior_failure_visibility")
        + 0.16 * f(row, "dissent_memory")
        + 0.10 * f(row, "ai_disclosure")
        + 0.10 * f(row, "ai_source_traceability")
        + 0.10 * f(row, "ai_bias_review")
    )
    ai_power_risk = (
        0.30 * f(row, "ai_power_amplification_risk")
        + 0.16 * (1 - f(row, "ai_disclosure"))
        + 0.16 * (1 - f(row, "ai_source_traceability"))
        + 0.16 * (1 - f(row, "ai_bias_review"))
        + 0.12 * (1 - f(row, "dissent_memory"))
        + 0.10 * (1 - f(row, "prior_failure_visibility"))
    )
    rma_rows.append({
        "record_id": row["record_id"],
        "idea_id": row["idea_id"],
        "idea": idea_names[row["idea_id"]],
        "resource_memory_integrity": round(resource_memory_integrity, 4),
        "ai_power_risk": round(ai_power_risk, 4),
        "review_action": row["review_action"],
    })

rma_rows.sort(key=lambda item: item["ai_power_risk"], reverse=True)
write_csv(TABLES / "resource_memory_ai_scores.csv", rma_rows)

summary = {
    "power_ideas": idea_rows,
    "agenda_power": agenda_rows,
    "evidence_parity": evidence_rows,
    "participation_voice": voice_rows,
    "resource_memory_ai": rma_rows,
}
(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

report = [
    "# Strategic Ideation and Institutional Power Diagnostic Report",
    "",
    "## Executive summary",
    "",
    "This diagnostic evaluates whether strategic ideas are advancing through strategic merit, evidence, stakeholder influence, and ethical visibility—or through sponsorship, resource fit, political safety, power alignment, selective memory, and ungoverned AI mediation.",
    "",
    "## Power distortion ranking",
    "",
]
for item in idea_rows:
    report.append(
        f"- **{item['idea_id']} — {item['idea']}**: merit {item['merit_score']}; institutional support {item['institutional_support']}; "
        f"power distortion {item['power_distortion']}; voice gap {item['voice_gap']}; diagnosis: {item['diagnosis']}."
    )

report.extend(["", "## Agenda-setting review", ""])
for item in agenda_rows:
    report.append(
        f"- **{item['idea']}** ({item['agenda_source']}): agenda legitimacy {item['agenda_legitimacy']}; "
        f"power-filtered attention {item['power_filtered_attention']}; action: {item['review_action']}."
    )

report.extend(["", "## Evidence parity review", ""])
for item in evidence_rows:
    report.append(
        f"- **{item['idea']}** ({item['evidence_type']}): evidence parity {item['evidence_parity_score']}; "
        f"threshold gap {item['threshold_gap']}; overclaim risk {item['overclaim_risk']}; action: {item['review_action']}."
    )

report.extend(["", "## Participation, influence, and tokenism review", ""])
for item in voice_rows:
    report.append(
        f"- **{item['idea']}** ({item['participation_mode']}): influence score {item['participation_influence_score']}; "
        f"tokenism risk {item['tokenism_risk']}; influence gap {item['influence_gap']}; action: {item['review_action']}."
    )

report.extend(["", "## Resource, memory, and AI mediation review", ""])
for item in rma_rows:
    report.append(
        f"- **{item['idea']}**: resource-memory integrity {item['resource_memory_integrity']}; "
        f"AI power risk {item['ai_power_risk']}; action: {item['review_action']}."
    )

report.extend([
    "",
    "## Professional interpretation",
    "",
    "Power-aware strategic ideation asks whether ideas are being judged by merit, evidence, stakeholder influence, ethical visibility, and long-term value, or filtered by authority, political safety, resource alignment, classification bias, selective memory, and AI-mediated institutional preference.",
])

(REPORTS / "institutional_power_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

print("Advanced institutional power diagnostics complete.")
print(f"Wrote: {TABLES / 'power_idea_scores.csv'}")
print(f"Wrote: {TABLES / 'agenda_power_scores.csv'}")
print(f"Wrote: {TABLES / 'evidence_parity_scores.csv'}")
print(f"Wrote: {TABLES / 'participation_voice_scores.csv'}")
print(f"Wrote: {TABLES / 'resource_memory_ai_scores.csv'}")
print(f"Wrote: {REPORTS / 'institutional_power_diagnostic_report.md'}")
