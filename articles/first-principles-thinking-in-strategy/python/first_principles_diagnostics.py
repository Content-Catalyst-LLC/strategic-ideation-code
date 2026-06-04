#!/usr/bin/env python3
"""Advanced first principles strategy diagnostics using only the Python standard library."""
from __future__ import annotations
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
TABLES = ROOT / "outputs" / "tables"
REPORTS = ROOT / "outputs" / "reports"
PROCESSED = ROOT / "data" / "processed"
for path in (TABLES, REPORTS, PROCESSED):
    path.mkdir(parents=True, exist_ok=True)

def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def write_csv(path: Path, rows, fields):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(rows)

def f(row, key): return float(row[key])
def is_true(value): return str(value).strip().lower() == "true"

contexts = read_csv(RAW / "strategy_contexts.csv")
constraints = read_csv(RAW / "constraints.csv")
assumptions = read_csv(RAW / "assumptions.csv")
mechanisms = read_csv(RAW / "mechanisms.csv")
options = read_csv(RAW / "reconstructed_options.csv")
tests = read_csv(RAW / "reality_tests.csv")

profile_rows = []
for row in contexts:
    score = (-0.16*f(row,"assumption_load") + 0.18*f(row,"structural_clarity") +
             0.18*f(row,"constraint_discrimination") + 0.18*f(row,"reconstruction_quality") +
             0.14*f(row,"adaptive_potential") + 0.10*f(row,"evidence_contact") +
             0.10*f(row,"ethical_visibility") + 0.08*f(row,"implementation_feasibility"))
    if f(row,"assumption_load") >= 0.80 and f(row,"constraint_discrimination") < 0.40:
        diagnosis = "assumption_lock_in"
    elif f(row,"structural_clarity") < 0.45:
        diagnosis = "weak_problem_decomposition"
    elif f(row,"ethical_visibility") < 0.45:
        diagnosis = "ethical_visibility_gap"
    elif score >= 0.62:
        diagnosis = "strong_first_principles_capacity"
    else:
        diagnosis = "requires_first_principles_review"
    profile_rows.append({
        "context_id": row["context_id"], "context_name": row["context_name"],
        "context_type": row["context_type"], "first_principles_profile_score": round(score,4),
        "diagnosis": diagnosis, "assumption_load": row["assumption_load"],
        "structural_clarity": row["structural_clarity"],
        "constraint_discrimination": row["constraint_discrimination"],
        "reconstruction_quality": row["reconstruction_quality"],
        "adaptive_potential": row["adaptive_potential"], "evidence_contact": row["evidence_contact"],
        "ethical_visibility": row["ethical_visibility"], "implementation_feasibility": row["implementation_feasibility"]})
profile_rows.sort(key=lambda r: r["first_principles_profile_score"], reverse=True)
profile_fields = list(profile_rows[0].keys())
write_csv(TABLES / "first_principles_profile_scores.csv", profile_rows, profile_fields)
write_csv(PROCESSED / "first_principles_profile_scores.csv", profile_rows, profile_fields)

constraint_rows = []
for row in constraints:
    real = is_true(row["is_real_constraint"])
    if real:
        priority = f(row,"strategic_importance") * f(row,"certainty") * (1 - f(row,"redesign_potential"))
        action = "respect_and_design_around" if priority >= 0.55 else "monitor"
        classification = "real_constraint"
    else:
        priority = f(row,"strategic_importance") * f(row,"redesign_potential") * (1 - f(row,"evidence_quality") + 0.25)
        action = "challenge_and_reconstruct" if priority >= 0.55 else "review_assumption_status"
        classification = "assumed_constraint"
    constraint_rows.append({"constraint_id": row["constraint_id"], "context_id": row["context_id"],
        "constraint_name": row["constraint_name"], "constraint_type": row["constraint_type"],
        "classification": classification, "constraint_priority": round(priority,4),
        "recommended_action": action, "notes": row["notes"]})
constraint_rows.sort(key=lambda r: r["constraint_priority"], reverse=True)
write_csv(TABLES / "constraint_classification_register.csv", constraint_rows, list(constraint_rows[0].keys()))

assumption_rows = []
for row in assumptions:
    burden = (1 - f(row,"confidence")) * f(row,"strategic_influence")
    urgency = "high" if burden >= 0.46 else "moderate" if burden >= 0.30 else "monitor"
    assumption_rows.append({"assumption_id": row["assumption_id"], "context_id": row["context_id"],
        "assumption_domain": row["assumption_domain"], "assumption": row["assumption"],
        "assumption_burden": round(burden,4), "urgency": urgency,
        "evidence_status": row["evidence_status"], "test_method": row["test_method"]})
assumption_rows.sort(key=lambda r: r["assumption_burden"], reverse=True)
write_csv(TABLES / "assumption_burden_register.csv", assumption_rows, list(assumption_rows[0].keys()))

mechanism_rows = []
for row in mechanisms:
    score = (0.24*f(row,"mechanism_strength") + 0.16*f(row,"visibility") +
             0.18*f(row,"current_strategy_alignment") + 0.24*f(row,"intervention_leverage") -
             0.12*f(row,"second_order_risk"))
    if f(row,"mechanism_strength") >= 0.80 and f(row,"visibility") < 0.50:
        flag = "powerful_hidden_mechanism"
    elif f(row,"current_strategy_alignment") < 0.45 and f(row,"intervention_leverage") >= 0.75:
        flag = "misaligned_high_leverage_mechanism"
    elif f(row,"second_order_risk") >= 0.60:
        flag = "second_order_risk_review"
    else:
        flag = "mechanism_mapped"
    mechanism_rows.append({"mechanism_id": row["mechanism_id"], "context_id": row["context_id"],
        "mechanism_name": row["mechanism_name"], "mechanism_type": row["mechanism_type"],
        "mechanism_score": round(score,4), "flag": flag})
mechanism_rows.sort(key=lambda r: r["mechanism_score"], reverse=True)
write_csv(TABLES / "mechanism_map_scores.csv", mechanism_rows, list(mechanism_rows[0].keys()))

option_rows = []
for row in options:
    score = (0.18*f(row,"strategic_fit") + 0.16*f(row,"constraint_realism") +
             0.20*f(row,"mechanism_alignment") + 0.14*f(row,"evidence_contact") +
             0.16*f(row,"ethical_legitimacy") + 0.14*f(row,"implementation_feasibility") -
             0.08*f(row,"uncertainty"))
    recommendation = "advance_to_strategy_review" if score >= 0.74 and f(row,"uncertainty") < 0.35 else "prototype_or_stress_test" if score >= 0.66 else "reframe_or_hold"
    option_rows.append({"option_id": row["option_id"], "context_id": row["context_id"],
        "option_name": row["option_name"], "reconstruction_type": row["reconstruction_type"],
        "reconstructed_option_score": round(score,4), "recommendation": recommendation})
option_rows.sort(key=lambda r: r["reconstructed_option_score"], reverse=True)
write_csv(TABLES / "reconstructed_option_scores.csv", option_rows, list(option_rows[0].keys()))

option_scores = {row["option_id"]: row["reconstructed_option_score"] for row in option_rows}
test_rows = []
for row in tests:
    score = option_scores.get(row["option_id"], 0)
    priority = "high_value_reality_test" if score >= 0.74 else "low_cost_learning_probe" if row["resource_intensity"] == "low" else "standard_review"
    test_rows.append({"test_id": row["test_id"], "option_id": row["option_id"],
        "test_name": row["test_name"], "test_type": row["test_type"],
        "review_layer": row["review_layer"], "estimated_weeks": row["estimated_weeks"],
        "resource_intensity": row["resource_intensity"], "test_priority": priority,
        "learning_goal": row["learning_goal"], "minimal_test": row["minimal_test"],
        "success_signal": row["success_signal"]})
write_csv(TABLES / "reality_test_plan.csv", test_rows, list(test_rows[0].keys()))

report = ["# First Principles Strategy Diagnostic Report", "", "## Executive summary", "",
          "This diagnostic separates assumption burden, real constraints, assumed constraints, governing mechanisms, reconstructed strategic options, and reality-test plans.", "",
          "## Highest assumption burdens"]
for item in assumption_rows[:5]:
    report.append(f"- **{item['assumption_id']} ({item['context_id']})**: burden {item['assumption_burden']}; {item['assumption']}; test: {item['test_method']}.")
report += ["", "## Strongest reconstructed options"]
for item in option_rows[:5]:
    report.append(f"- **{item['option_id']} — {item['option_name']}**: score {item['reconstructed_option_score']}; recommendation: {item['recommendation']}.")
report += ["", "## Professional interpretation", "",
           "The value of this workflow is disciplined separation: real constraints from assumed constraints, inherited assumptions from governing mechanisms, and elegant reconstruction from evidence-tested strategic judgment."]
(REPORTS / "first_principles_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")
(REPORTS / "diagnostic_summary.json").write_text(json.dumps({"top_profiles": profile_rows[:3], "top_options": option_rows[:3], "top_assumptions": assumption_rows[:3]}, indent=2), encoding="utf-8")

print("Advanced first principles diagnostics complete.")
