#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Strategic Communication and Conceptual Coherence.

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


profiles = read_csv(RAW / "communication_profiles.csv")
concepts = read_csv(RAW / "concepts.csv")
claims = read_csv(RAW / "claim_evidence.csv")
audiences = read_csv(RAW / "audience_adaptation.csv")
decisions = read_csv(RAW / "decision_alignment.csv")
governance = read_csv(RAW / "governance_ethics.csv")

profile_names = {row["profile_id"]: row["communication_profile"] for row in profiles}

# ---------------------------------------------------------------------
# 1. Communication profile coherence
# ---------------------------------------------------------------------

profile_rows: list[dict[str, object]] = []

for row in profiles:
    strength = (
        0.11 * f(row, "concept_definition")
        + 0.11 * f(row, "narrative_coherence")
        + 0.13 * f(row, "evidence_integrity")
        + 0.10 * f(row, "audience_adaptation")
        + 0.13 * f(row, "decision_alignment")
        + 0.11 * f(row, "implementation_translatability")
        + 0.08 * f(row, "feedback_quality")
        + 0.10 * f(row, "governance_strength")
        + 0.09 * f(row, "ethical_visibility")
        + 0.04 * f(row, "ai_governance")
    )
    meaning_loss_risk = (
        0.12 * (1 - f(row, "concept_definition"))
        + 0.10 * (1 - f(row, "narrative_coherence"))
        + 0.13 * (1 - f(row, "evidence_integrity"))
        + 0.10 * (1 - f(row, "audience_adaptation"))
        + 0.13 * (1 - f(row, "decision_alignment"))
        + 0.11 * (1 - f(row, "implementation_translatability"))
        + 0.08 * (1 - f(row, "feedback_quality"))
        + 0.09 * (1 - f(row, "governance_strength"))
        + 0.10 * (1 - f(row, "ethical_visibility"))
        + 0.04 * (1 - f(row, "ai_governance"))
    )

    if strength >= 0.76:
        diagnosis = "strong_conceptual_coherence"
    elif f(row, "evidence_integrity") < 0.55:
        diagnosis = "evidence_integrity_gap"
    elif f(row, "decision_alignment") < 0.60:
        diagnosis = "decision_alignment_gap"
    elif f(row, "implementation_translatability") < 0.55:
        diagnosis = "implementation_meaning_gap"
    elif f(row, "governance_strength") < 0.55:
        diagnosis = "communication_governance_gap"
    elif f(row, "ethical_visibility") < 0.55:
        diagnosis = "ethical_visibility_review_required"
    elif f(row, "ai_governance") < 0.45 and row["profile_type"] == "ai_assisted":
        diagnosis = "urgent_ai_communication_governance_required"
    elif f(row, "concept_definition") < 0.60:
        diagnosis = "concept_definition_gap"
    else:
        diagnosis = "targeted_coherence_repair"

    weakest_dimension = min(
        [
            ("concept_definition", f(row, "concept_definition")),
            ("narrative_coherence", f(row, "narrative_coherence")),
            ("evidence_integrity", f(row, "evidence_integrity")),
            ("audience_adaptation", f(row, "audience_adaptation")),
            ("decision_alignment", f(row, "decision_alignment")),
            ("implementation_translatability", f(row, "implementation_translatability")),
            ("feedback_quality", f(row, "feedback_quality")),
            ("governance_strength", f(row, "governance_strength")),
            ("ethical_visibility", f(row, "ethical_visibility")),
            ("ai_governance", f(row, "ai_governance")),
        ],
        key=lambda item: item[1],
    )[0]

    profile_rows.append({
        "profile_id": row["profile_id"],
        "communication_profile": row["communication_profile"],
        "profile_type": row["profile_type"],
        "coherence_strength": round(strength, 4),
        "meaning_loss_risk": round(meaning_loss_risk, 4),
        "weakest_dimension": weakest_dimension,
        "diagnosis": diagnosis,
        "description": row["description"],
    })

profile_rows.sort(key=lambda item: item["coherence_strength"], reverse=True)
write_csv(TABLES / "communication_profile_scores.csv", profile_rows)
write_csv(PROCESSED / "communication_profile_scores.csv", profile_rows)

# ---------------------------------------------------------------------
# 2. Concept definition and drift review
# ---------------------------------------------------------------------

concept_rows: list[dict[str, object]] = []
for row in concepts:
    score = (
        0.16 * f(row, "definition_quality")
        + 0.14 * f(row, "boundary_clarity")
        + 0.14 * f(row, "mechanism_clarity")
        + 0.14 * f(row, "evidence_linkage")
        + 0.15 * f(row, "decision_relevance")
        + 0.12 * f(row, "implementation_meaning")
        + 0.10 * f(row, "version_control")
        - 0.05 * f(row, "drift_risk")
    )
    concept_rows.append({
        "concept_id": row["concept_id"],
        "concept_name": row["concept_name"],
        "concept_definition_score": round(score, 4),
        "drift_risk": f(row, "drift_risk"),
        "recommended_action": row["review_action"],
    })

concept_rows.sort(key=lambda item: item["concept_definition_score"])
write_csv(TABLES / "concept_definition_scores.csv", concept_rows)

# ---------------------------------------------------------------------
# 3. Claim-evidence integrity
# ---------------------------------------------------------------------

claim_rows: list[dict[str, object]] = []
for row in claims:
    score = (
        0.15 * f(row, "evidence_quality")
        + 0.15 * f(row, "confidence_level")
        + 0.13 * f(row, "assumption_visibility")
        + 0.13 * f(row, "uncertainty_visibility")
        + 0.11 * f(row, "counterevidence_visibility")
        + 0.15 * f(row, "source_traceability")
        - 0.08 * f(row, "overclaim_risk")
        + 0.06
    )
    claim_rows.append({
        "claim_id": row["claim_id"],
        "profile_id": row["profile_id"],
        "communication_profile": profile_names[row["profile_id"]],
        "claim_type": row["claim_type"],
        "claim_text": row["claim_text"],
        "claim_evidence_integrity_score": round(score, 4),
        "overclaim_risk": f(row, "overclaim_risk"),
        "recommended_action": row["review_action"],
    })

claim_rows.sort(key=lambda item: item["claim_evidence_integrity_score"])
write_csv(TABLES / "claim_evidence_scores.csv", claim_rows)

# ---------------------------------------------------------------------
# 4. Audience adaptation and distortion risk
# ---------------------------------------------------------------------

audience_rows: list[dict[str, object]] = []
for row in audiences:
    score = (
        0.17 * f(row, "core_meaning_preservation")
        + 0.12 * f(row, "language_fit")
        + 0.13 * f(row, "evidence_fit")
        + 0.11 * f(row, "depth_fit")
        + 0.12 * f(row, "tradeoff_visibility")
        + 0.12 * f(row, "uncertainty_visibility")
        + 0.13 * f(row, "feedback_channel_quality")
        - 0.10 * f(row, "distortion_risk")
        + 0.10
    )
    audience_rows.append({
        "adaptation_id": row["adaptation_id"],
        "profile_id": row["profile_id"],
        "communication_profile": profile_names[row["profile_id"]],
        "audience": row["audience"],
        "audience_adaptation_score": round(score, 4),
        "distortion_risk": f(row, "distortion_risk"),
        "recommended_action": row["review_action"],
    })

audience_rows.sort(key=lambda item: item["audience_adaptation_score"])
write_csv(TABLES / "audience_adaptation_scores.csv", audience_rows)

# ---------------------------------------------------------------------
# 5. Decision and implementation alignment
# ---------------------------------------------------------------------

decision_rows: list[dict[str, object]] = []
for row in decisions:
    score = (
        0.14 * f(row, "decision_accuracy")
        + 0.13 * f(row, "rationale_clarity")
        + 0.12 * f(row, "tradeoff_alignment")
        + 0.11 * f(row, "owner_visibility")
        + 0.10 * f(row, "timeline_visibility")
        + 0.14 * f(row, "revision_trigger_quality")
        + 0.14 * f(row, "implementation_guidance")
        + 0.12 * f(row, "metric_consistency")
    )
    decision_rows.append({
        "alignment_id": row["alignment_id"],
        "profile_id": row["profile_id"],
        "communication_profile": profile_names[row["profile_id"]],
        "decision_alignment_score": round(score, 4),
        "recommended_action": row["review_action"],
    })

decision_rows.sort(key=lambda item: item["decision_alignment_score"])
write_csv(TABLES / "decision_alignment_scores.csv", decision_rows)

# ---------------------------------------------------------------------
# 6. Governance and ethics
# ---------------------------------------------------------------------

governance_rows: list[dict[str, object]] = []
for row in governance:
    stewardship = (
        0.13 * f(row, "core_message_ownership")
        + 0.13 * f(row, "definition_standards")
        + 0.14 * f(row, "evidence_review")
        + 0.11 * f(row, "version_control")
        + 0.11 * f(row, "audience_rules")
        + 0.11 * f(row, "feedback_loop_quality")
        + 0.09 * f(row, "stakeholder_voice")
        + 0.08 * f(row, "burden_visibility")
        + 0.08 * f(row, "dissent_preservation")
        - 0.04 * f(row, "ethical_risk")
        + 0.06
    )
    ethics_risk = (
        0.20 * f(row, "ethical_risk")
        + 0.14 * (1 - f(row, "stakeholder_voice"))
        + 0.14 * (1 - f(row, "burden_visibility"))
        + 0.14 * (1 - f(row, "dissent_preservation"))
        + 0.12 * (1 - f(row, "evidence_review"))
        + 0.10 * (1 - f(row, "definition_standards"))
        + 0.08 * (1 - f(row, "feedback_loop_quality"))
        + 0.08 * (1 - f(row, "audience_rules"))
    )
    governance_rows.append({
        "governance_id": row["governance_id"],
        "profile_id": row["profile_id"],
        "communication_profile": profile_names[row["profile_id"]],
        "communication_stewardship_score": round(stewardship, 4),
        "ethical_communication_risk": round(ethics_risk, 4),
        "recommended_action": row["review_action"],
    })

governance_rows.sort(key=lambda item: item["communication_stewardship_score"])
write_csv(TABLES / "governance_ethics_scores.csv", governance_rows)

summary = {
    "communication_profiles": profile_rows,
    "concepts": concept_rows,
    "claim_evidence": claim_rows,
    "audience_adaptation": audience_rows,
    "decision_alignment": decision_rows,
    "governance_ethics": governance_rows,
}
(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

report = [
    "# Strategic Communication and Conceptual Coherence Diagnostic Report",
    "",
    "## Executive summary",
    "",
    "This diagnostic evaluates whether strategic communication preserves meaning as strategy travels across audiences, documents, decisions, implementation contexts, feedback loops, and time. It reviews concept definition, narrative coherence, evidence integrity, audience adaptation, decision alignment, implementation translatability, feedback quality, governance strength, ethical visibility, and AI governance.",
    "",
    "## Communication coherence ranking",
    "",
]
for item in profile_rows:
    report.append(
        f"- **{item['profile_id']} — {item['communication_profile']}**: coherence strength {item['coherence_strength']}; "
        f"meaning loss risk {item['meaning_loss_risk']}; weakest dimension: {item['weakest_dimension']}; diagnosis: {item['diagnosis']}."
    )

report.extend(["", "## Concept definition and drift repair priorities", ""])
for item in concept_rows:
    report.append(
        f"- **{item['concept_name']}**: concept definition score {item['concept_definition_score']}; "
        f"drift risk {item['drift_risk']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Claim-evidence integrity review", ""])
for item in claim_rows:
    report.append(
        f"- **{item['communication_profile']} / {item['claim_type']}**: claim-evidence score {item['claim_evidence_integrity_score']}; "
        f"overclaim risk {item['overclaim_risk']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Audience adaptation and distortion review", ""])
for item in audience_rows:
    report.append(
        f"- **{item['communication_profile']} → {item['audience']}**: adaptation score {item['audience_adaptation_score']}; "
        f"distortion risk {item['distortion_risk']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Decision and implementation alignment", ""])
for item in decision_rows:
    report.append(
        f"- **{item['communication_profile']}**: decision alignment score {item['decision_alignment_score']}; action: {item['recommended_action']}."
    )

report.extend(["", "## Governance and ethics review", ""])
for item in governance_rows:
    report.append(
        f"- **{item['communication_profile']}**: stewardship {item['communication_stewardship_score']}; ethical risk {item['ethical_communication_risk']}; action: {item['recommended_action']}."
    )

report.extend([
    "",
    "## Professional interpretation",
    "",
    "Strategic communication is coherent when language, evidence, narrative, decisions, implementation guidance, feedback, governance, and ethics preserve the same strategic meaning. Meaning loss appears when concepts become slogans, evidence detaches from claims, audience adaptation becomes distortion, implementation teams cannot translate messages into action, or AI-assisted communication produces fluent but conceptually weak output.",
])

(REPORTS / "communication_coherence_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

print("Advanced communication coherence diagnostics complete.")
print(f"Wrote: {TABLES / 'communication_profile_scores.csv'}")
print(f"Wrote: {TABLES / 'concept_definition_scores.csv'}")
print(f"Wrote: {TABLES / 'claim_evidence_scores.csv'}")
print(f"Wrote: {TABLES / 'audience_adaptation_scores.csv'}")
print(f"Wrote: {TABLES / 'decision_alignment_scores.csv'}")
print(f"Wrote: {TABLES / 'governance_ethics_scores.csv'}")
print(f"Wrote: {REPORTS / 'communication_coherence_diagnostic_report.md'}")
