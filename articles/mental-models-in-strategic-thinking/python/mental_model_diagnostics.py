#!/usr/bin/env python3
"""
Advanced strategist-facing mental-model diagnostics.

This dependency-light workflow uses only the Python standard library.

It produces:
- mental-model profile scores
- model monoculture and lock-in risk
- causal-frame adequacy scores
- evidence disconfirmation map
- revision priority register
- scenario stress-test scores
- a markdown strategist diagnostic report

The workflow is designed for strategy teams that need to audit the models
through which they interpret environments, evidence, causality, legitimacy,
and future uncertainty.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean

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


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def f(row: dict[str, str], key: str) -> float:
    return float(row[key])


models = read_csv(RAW / "mental_model_profiles.csv")
causal_frames = read_csv(RAW / "causal_frames.csv")
artifacts = read_csv(RAW / "institutional_artifacts.csv")
evidence = read_csv(RAW / "evidence_feedback.csv")
audits = read_csv(RAW / "model_audit_items.csv")
stress_tests = read_csv(RAW / "scenario_stress_tests.csv")

# ---------------------------------------------------------------------
# 1. Mental model profile scores
# ---------------------------------------------------------------------

profile_rows: list[dict[str, object]] = []

for row in models:
    adaptive_score = (
        0.17 * f(row, "systems_richness")
        + 0.13 * f(row, "probabilistic_depth")
        + 0.16 * f(row, "model_flexibility")
        + 0.14 * f(row, "model_plurality")
        + 0.16 * f(row, "revision_capacity")
        - 0.08 * f(row, "institutional_embedding")
        + 0.12 * f(row, "ethical_visibility")
        + 0.10 * f(row, "stakeholder_visibility")
        + 0.10 * f(row, "evidence_responsiveness")
    )

    monoculture_risk = (
        0.28 * f(row, "institutional_embedding")
        + 0.20 * (1 - f(row, "model_plurality"))
        + 0.18 * (1 - f(row, "model_flexibility"))
        + 0.18 * (1 - f(row, "revision_capacity"))
        + 0.16 * (1 - f(row, "stakeholder_visibility"))
    )

    if adaptive_score >= 0.75 and monoculture_risk < 0.35:
        diagnosis = "adaptive_model_strength"
    elif monoculture_risk >= 0.65:
        diagnosis = "model_monoculture_or_lock_in_risk"
    elif f(row, "ethical_visibility") < 0.45 or f(row, "stakeholder_visibility") < 0.45:
        diagnosis = "ethical_or_stakeholder_blind_spot"
    elif f(row, "revision_capacity") < 0.40:
        diagnosis = "low_revision_capacity"
    else:
        diagnosis = "requires_model_review"

    profile_rows.append(
        {
            "model_id": row["model_id"],
            "model_name": row["model_name"],
            "dominant_frame": row["dominant_frame"],
            "adaptive_model_score": round(adaptive_score, 4),
            "monoculture_risk": round(monoculture_risk, 4),
            "diagnosis": diagnosis,
            "systems_richness": row["systems_richness"],
            "model_plurality": row["model_plurality"],
            "revision_capacity": row["revision_capacity"],
            "ethical_visibility": row["ethical_visibility"],
            "stakeholder_visibility": row["stakeholder_visibility"],
        }
    )

profile_rows.sort(key=lambda item: item["adaptive_model_score"], reverse=True)

write_csv(
    TABLES / "mental_model_profile_scores.csv",
    profile_rows,
    [
        "model_id",
        "model_name",
        "dominant_frame",
        "adaptive_model_score",
        "monoculture_risk",
        "diagnosis",
        "systems_richness",
        "model_plurality",
        "revision_capacity",
        "ethical_visibility",
        "stakeholder_visibility",
    ],
)

write_csv(
    PROCESSED / "mental_model_profile_scores.csv",
    profile_rows,
    [
        "model_id",
        "model_name",
        "dominant_frame",
        "adaptive_model_score",
        "monoculture_risk",
        "diagnosis",
        "systems_richness",
        "model_plurality",
        "revision_capacity",
        "ethical_visibility",
        "stakeholder_visibility",
    ],
)

# ---------------------------------------------------------------------
# 2. Causal-frame adequacy
# ---------------------------------------------------------------------

causal_rows: list[dict[str, object]] = []

for row in causal_frames:
    adequacy = (
        0.24 * f(row, "environment_fit")
        + 0.20 * f(row, "feedback_awareness")
        + 0.18 * f(row, "delay_awareness")
        + 0.18 * f(row, "nonlinearity_awareness")
        + 0.20 * f(row, "second_order_awareness")
        - 0.18 * f(row, "blind_spot_risk")
    )

    if adequacy >= 0.70:
        flag = "causal_frame_strong"
    elif f(row, "blind_spot_risk") >= 0.70:
        flag = "high_blind_spot_risk"
    elif f(row, "feedback_awareness") < 0.45 or f(row, "nonlinearity_awareness") < 0.45:
        flag = "linear_or_feedback_weakness"
    else:
        flag = "causal_frame_review"

    causal_rows.append(
        {
            "frame_id": row["frame_id"],
            "model_id": row["model_id"],
            "causal_type": row["causal_type"],
            "causal_adequacy_score": round(adequacy, 4),
            "flag": flag,
            "environment_fit": row["environment_fit"],
            "feedback_awareness": row["feedback_awareness"],
            "delay_awareness": row["delay_awareness"],
            "nonlinearity_awareness": row["nonlinearity_awareness"],
            "second_order_awareness": row["second_order_awareness"],
            "blind_spot_risk": row["blind_spot_risk"],
            "causal_assumption": row["causal_assumption"],
        }
    )

causal_rows.sort(key=lambda item: item["causal_adequacy_score"], reverse=True)

write_csv(
    TABLES / "causal_frame_adequacy.csv",
    causal_rows,
    [
        "frame_id",
        "model_id",
        "causal_type",
        "causal_adequacy_score",
        "flag",
        "environment_fit",
        "feedback_awareness",
        "delay_awareness",
        "nonlinearity_awareness",
        "second_order_awareness",
        "blind_spot_risk",
        "causal_assumption",
    ],
)

# ---------------------------------------------------------------------
# 3. Institutional monoculture and lock-in risk
# ---------------------------------------------------------------------

artifact_rows: list[dict[str, object]] = []

for row in artifacts:
    lock_in_risk = (
        0.24 * f(row, "measurement_bias")
        + 0.28 * f(row, "lock_in_strength")
        + 0.18 * (1 - f(row, "revision_pathway"))
        + 0.14 * (1 - f(row, "stakeholder_visibility"))
        + 0.16 * (1 - f(row, "ethical_visibility"))
    )

    if lock_in_risk >= 0.70:
        diagnosis = "high_model_lock_in"
    elif f(row, "revision_pathway") < 0.45:
        diagnosis = "weak_revision_pathway"
    elif f(row, "stakeholder_visibility") < 0.45 or f(row, "ethical_visibility") < 0.45:
        diagnosis = "visibility_gap"
    else:
        diagnosis = "manageable_institutional_model"

    artifact_rows.append(
        {
            "artifact_id": row["artifact_id"],
            "artifact_name": row["artifact_name"],
            "artifact_type": row["artifact_type"],
            "encoded_model": row["encoded_model"],
            "lock_in_risk": round(lock_in_risk, 4),
            "diagnosis": diagnosis,
            "measurement_bias": row["measurement_bias"],
            "lock_in_strength": row["lock_in_strength"],
            "revision_pathway": row["revision_pathway"],
            "stakeholder_visibility": row["stakeholder_visibility"],
            "ethical_visibility": row["ethical_visibility"],
            "strategic_risk": row["strategic_risk"],
        }
    )

artifact_rows.sort(key=lambda item: item["lock_in_risk"], reverse=True)

write_csv(
    TABLES / "model_monoculture_risk.csv",
    artifact_rows,
    [
        "artifact_id",
        "artifact_name",
        "artifact_type",
        "encoded_model",
        "lock_in_risk",
        "diagnosis",
        "measurement_bias",
        "lock_in_strength",
        "revision_pathway",
        "stakeholder_visibility",
        "ethical_visibility",
        "strategic_risk",
    ],
)

# ---------------------------------------------------------------------
# 4. Evidence disconfirmation and revision mapping
# ---------------------------------------------------------------------

evidence_rows: list[dict[str, object]] = []

for row in evidence:
    revision_priority = (
        0.40 * f(row, "disconfirmation_strength")
        + 0.30 * f(row, "evidence_quality")
        + 0.20 * (1.0 if row["revision_required"].lower() == "true" else 0.0)
        + 0.10 * (1.0 if row["model_response"] in ("treated_as_exception", "delayed_review", "contested") else 0.0)
    )

    if revision_priority >= 0.78:
        urgency = "urgent_model_revision"
    elif revision_priority >= 0.62:
        urgency = "structured_revision_review"
    else:
        urgency = "monitor"

    evidence_rows.append(
        {
            "evidence_id": row["evidence_id"],
            "model_id": row["model_id"],
            "evidence_type": row["evidence_type"],
            "revision_priority": round(revision_priority, 4),
            "urgency": urgency,
            "model_response": row["model_response"],
            "affected_layer": row["affected_layer"],
            "evidence_summary": row["evidence_summary"],
        }
    )

evidence_rows.sort(key=lambda item: item["revision_priority"], reverse=True)

write_csv(
    TABLES / "evidence_disconfirmation_map.csv",
    evidence_rows,
    [
        "evidence_id",
        "model_id",
        "evidence_type",
        "revision_priority",
        "urgency",
        "model_response",
        "affected_layer",
        "evidence_summary",
    ],
)

# ---------------------------------------------------------------------
# 5. Audit revision priority register
# ---------------------------------------------------------------------

audit_rows: list[dict[str, object]] = []

for row in audits:
    gap = f(row, "desired_score") - f(row, "current_score")
    if row["priority"] == "high":
        priority_weight = 1.0
    elif row["priority"] == "moderate":
        priority_weight = 0.75
    else:
        priority_weight = 0.50

    revision_score = max(gap, 0) * priority_weight

    if revision_score >= 0.42:
        action = "schedule_immediate_model_audit"
    elif revision_score >= 0.24:
        action = "include_in_next_strategy_review"
    else:
        action = "monitor"

    audit_rows.append(
        {
            "audit_id": row["audit_id"],
            "model_id": row["model_id"],
            "audit_dimension": row["audit_dimension"],
            "current_score": row["current_score"],
            "desired_score": row["desired_score"],
            "revision_gap": round(gap, 4),
            "revision_priority_score": round(revision_score, 4),
            "recommended_action": action,
            "review_method": row["review_method"],
            "audit_question": row["audit_question"],
        }
    )

audit_rows.sort(key=lambda item: item["revision_priority_score"], reverse=True)

write_csv(
    TABLES / "revision_priority_register.csv",
    audit_rows,
    [
        "audit_id",
        "model_id",
        "audit_dimension",
        "current_score",
        "desired_score",
        "revision_gap",
        "revision_priority_score",
        "recommended_action",
        "review_method",
        "audit_question",
    ],
)

# ---------------------------------------------------------------------
# 6. Scenario stress tests
# ---------------------------------------------------------------------

stress_rows: list[dict[str, object]] = []

for row in stress_tests:
    stress_score = (
        0.34 * f(row, "performance_under_stress")
        + 0.24 * f(row, "revision_speed")
        - 0.22 * f(row, "blind_spot_exposure")
        + 0.30 * f(row, "strategic_robustness")
    )

    if stress_score >= 0.68:
        result = "robust_under_stress"
    elif f(row, "blind_spot_exposure") >= 0.75:
        result = "model_blind_spot_exposed"
    else:
        result = "stress_review_required"

    stress_rows.append(
        {
            "scenario_id": row["scenario_id"],
            "scenario_name": row["scenario_name"],
            "model_id": row["model_id"],
            "stress_condition": row["stress_condition"],
            "stress_score": round(stress_score, 4),
            "result": result,
            "performance_under_stress": row["performance_under_stress"],
            "revision_speed": row["revision_speed"],
            "blind_spot_exposure": row["blind_spot_exposure"],
            "strategic_robustness": row["strategic_robustness"],
        }
    )

stress_rows.sort(key=lambda item: item["stress_score"], reverse=True)

write_csv(
    TABLES / "scenario_stress_test_scores.csv",
    stress_rows,
    [
        "scenario_id",
        "scenario_name",
        "model_id",
        "stress_condition",
        "stress_score",
        "result",
        "performance_under_stress",
        "revision_speed",
        "blind_spot_exposure",
        "strategic_robustness",
    ],
)

# ---------------------------------------------------------------------
# 7. Strategist report
# ---------------------------------------------------------------------

top_models = profile_rows[:4]
high_lock_in = artifact_rows[:5]
urgent_evidence = evidence_rows[:5]
urgent_audits = audit_rows[:5]
stress_failures = [row for row in stress_rows if row["result"] != "robust_under_stress"][:5]
causal_weaknesses = [row for row in causal_rows if row["flag"] != "causal_frame_strong"][:5]

report: list[str] = []

report.append("# Mental Model Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic separates model quality, causal-frame adequacy, institutional lock-in, "
    "evidence disconfirmation, audit priorities, and scenario stress-test performance. "
    "The purpose is to help strategists identify when the problem is not lack of information, "
    "but the model through which information is interpreted."
)
report.append("")
report.append("## Strongest adaptive mental models")
report.append("")

for item in top_models:
    report.append(
        f"- **{item['model_id']} — {item['model_name']}**: adaptive score {item['adaptive_model_score']}; "
        f"monoculture risk {item['monoculture_risk']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Institutional artifacts with highest model lock-in risk")
report.append("")

for item in high_lock_in:
    report.append(
        f"- **{item['artifact_id']} — {item['artifact_name']}**: lock-in risk {item['lock_in_risk']}; "
        f"encoded model: {item['encoded_model']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Evidence requiring model revision review")
report.append("")

for item in urgent_evidence:
    report.append(
        f"- **{item['evidence_id']} ({item['model_id']})**: priority {item['revision_priority']}; "
        f"urgency: {item['urgency']}; affected layer: {item['affected_layer']}; "
        f"summary: {item['evidence_summary']}"
    )

report.append("")
report.append("## Highest-priority model audit items")
report.append("")

for item in urgent_audits:
    report.append(
        f"- **{item['audit_id']} ({item['model_id']})**: dimension {item['audit_dimension']}; "
        f"priority score {item['revision_priority_score']}; action: {item['recommended_action']}; "
        f"question: {item['audit_question']}"
    )

report.append("")
report.append("## Causal-frame weaknesses")
report.append("")

for item in causal_weaknesses:
    report.append(
        f"- **{item['frame_id']} ({item['model_id']})**: causal type {item['causal_type']}; "
        f"adequacy score {item['causal_adequacy_score']}; flag: {item['flag']}."
    )

report.append("")
report.append("## Scenario stress-test concerns")
report.append("")

for item in stress_failures:
    report.append(
        f"- **{item['scenario_id']} — {item['scenario_name']}**: model {item['model_id']}; "
        f"stress score {item['stress_score']}; result: {item['result']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "The main value of this workflow is disciplined model awareness. It helps a strategist ask: "
    "Which model is governing interpretation? What causal assumptions does it contain? What evidence "
    "is it rejecting or absorbing without revision? Which institutional artifacts protect it? Which "
    "stakeholders or harms does it fail to see? What scenario would expose its limits?"
)

(REPORTS / "mental_model_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_models": top_models,
    "high_lock_in_artifacts": high_lock_in,
    "urgent_evidence": urgent_evidence,
    "urgent_audits": urgent_audits,
    "causal_weaknesses": causal_weaknesses,
    "stress_failures": stress_failures,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced mental-model diagnostics complete.")
print(f"Wrote: {TABLES / 'mental_model_profile_scores.csv'}")
print(f"Wrote: {TABLES / 'model_monoculture_risk.csv'}")
print(f"Wrote: {TABLES / 'causal_frame_adequacy.csv'}")
print(f"Wrote: {TABLES / 'revision_priority_register.csv'}")
print(f"Wrote: {TABLES / 'evidence_disconfirmation_map.csv'}")
print(f"Wrote: {TABLES / 'scenario_stress_test_scores.csv'}")
print(f"Wrote: {REPORTS / 'mental_model_diagnostic_report.md'}")
