#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "outputs" / "tables"
REPORTS = ROOT / "outputs" / "reports"
for path in (PROCESSED, TABLES, REPORTS):
    path.mkdir(parents=True, exist_ok=True)

def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def write_csv(path: Path, rows, fieldnames):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def f(row, key):
    return float(row[key])

options = read_csv(RAW / "strategic_options.csv")
uncertainties = read_csv(RAW / "uncertainty_materiality.csv")
lock_in = read_csv(RAW / "lock_in_reversibility.csv")
experiments = read_csv(RAW / "learning_experiments.csv")
gates = read_csv(RAW / "decision_gates.csv")
modularity = read_csv(RAW / "modularity_switching.csv")
scenarios = read_csv(RAW / "scenario_options.csv")
expiration = read_csv(RAW / "option_expiration.csv")
governance = read_csv(RAW / "governance_readiness.csv")
ethics = read_csv(RAW / "ethics_burden.csv")
memory = read_csv(RAW / "decision_memory.csv")
option_names = {row["option_id"]: row["option_name"] for row in options}

option_rows = []
for row in options:
    option_value_score = (
        0.10*f(row,"initial_return") + 0.17*f(row,"learning_value") + 0.17*f(row,"flexibility") +
        0.12*f(row,"reversibility") + 0.11*f(row,"scalability") + 0.13*f(row,"modularity") -
        0.14*f(row,"lock_in_exposure") - 0.06*f(row,"carrying_cost") +
        0.11*f(row,"governance_readiness") + 0.09*f(row,"ethical_resilience")
    )
    lock_in_warning = (
        0.30*f(row,"lock_in_exposure") + 0.18*(1-f(row,"reversibility")) +
        0.16*(1-f(row,"flexibility")) + 0.14*(1-f(row,"modularity")) +
        0.12*(1-f(row,"governance_readiness")) + 0.10*(1-f(row,"ethical_resilience"))
    )
    diagnosis = "strong_option_value" if option_value_score >= 0.68 else "high_lock_in_warning" if lock_in_warning >= 0.64 else "developing_option_value"
    option_rows.append({**row, "option_value_score": round(option_value_score,4), "lock_in_warning": round(lock_in_warning,4), "diagnosis": diagnosis})
option_rows.sort(key=lambda x: x["option_value_score"], reverse=True)
write_csv(TABLES / "option_value_scores.csv", option_rows, list(option_rows[0].keys()))
write_csv(PROCESSED / "option_value_scores.csv", option_rows, list(option_rows[0].keys()))

uncertainty_rows=[]
for row in uncertainties:
    intensity = (0.13*f(row,"market_uncertainty")+0.13*f(row,"technical_uncertainty")+0.12*f(row,"regulatory_uncertainty")+0.13*f(row,"stakeholder_uncertainty")+0.12*f(row,"cost_uncertainty")+0.14*f(row,"system_response_uncertainty")+0.11*f(row,"information_arrival_likelihood")+0.12*f(row,"decision_impact"))
    relevance = intensity * (0.6 + 0.4*f(row,"information_arrival_likelihood"))
    uncertainty_rows.append({**row, "option_name": option_names[row["option_id"]], "uncertainty_intensity": round(intensity,4), "option_relevance": round(relevance,4)})
uncertainty_rows.sort(key=lambda x: x["option_relevance"], reverse=True)
write_csv(TABLES / "uncertainty_materiality_scores.csv", uncertainty_rows, list(uncertainty_rows[0].keys()))

lock_rows=[]
for row in lock_in:
    lock_score = (0.16*f(row,"irreversibility")+0.15*f(row,"switching_cost")+0.14*f(row,"ecosystem_dependence")+0.12*f(row,"contractual_constraint")+0.13*f(row,"data_or_platform_dependence")+0.12*f(row,"political_or_reputation_commitment")-0.11*f(row,"retained_flexibility")-0.07*f(row,"exit_path_quality"))
    rev_score = (0.34*f(row,"retained_flexibility")+0.30*f(row,"exit_path_quality")+0.12*(1-f(row,"irreversibility"))+0.10*(1-f(row,"switching_cost"))+0.08*(1-f(row,"ecosystem_dependence"))+0.06*(1-f(row,"contractual_constraint")))
    lock_rows.append({**row, "option_name": option_names[row["option_id"]], "lock_in_score": round(lock_score,4), "reversibility_score": round(rev_score,4)})
lock_rows.sort(key=lambda x: x["lock_in_score"], reverse=True)
write_csv(TABLES / "lock_in_reversibility_scores.csv", lock_rows, list(lock_rows[0].keys()))

def weighted_rows(rows, output_name, weights, negative=None):
    negative = negative or []
    out=[]
    metric = output_name.replace(".csv","").replace("_scores", "_score")
    for row in rows:
        score=0
        for key,w in weights.items():
            value=f(row,key)
            score += w*(1-value if key in negative else value)
        out.append({**row, "option_name": option_names[row["option_id"]], metric: round(score,4)})
    out.sort(key=lambda x: x[metric], reverse=True)
    write_csv(TABLES / output_name, out, list(out[0].keys()))
    return out

experiment_rows = weighted_rows(experiments, "learning_experiment_scores.csv", {"assumption_clarity":0.13,"evidence_quality":0.14,"transferability":0.11,"decision_relevance":0.17,"measurement_quality":0.12,"stakeholder_validity":0.11,"cost_efficiency":0.09,"stopping_rule_quality":0.13})
gate_rows = weighted_rows(gates, "decision_gate_scores.csv", {"evidence_threshold_clarity":0.14,"scale_trigger_quality":0.13,"revise_trigger_quality":0.13,"stop_trigger_quality":0.15,"owner_clarity":0.11,"review_cadence_quality":0.11,"signal_monitoring_quality":0.12,"documentation_quality":0.11})
modularity_rows = weighted_rows(modularity, "modularity_switching_scores.csv", {"component_modularity":0.15,"interface_openness":0.15,"data_portability":0.13,"vendor_substitutability":0.12,"policy_revisability":0.12,"organizational_adaptability":0.12,"switching_readiness":0.13,"dependency_concentration":0.08}, negative=["dependency_concentration"])
expiration_rows = weighted_rows(expiration, "option_expiration_scores.csv", {"market_window_pressure":0.15,"competitor_movement":0.14,"regulatory_deadline":0.13,"stakeholder_patience_loss":0.14,"capability_decay":0.12,"information_value_decay":0.12,"carrying_cost_pressure":0.10,"renewal_path_quality":0.10}, negative=["renewal_path_quality"])
governance_rows = weighted_rows(governance, "governance_readiness_scores.csv", {"decision_rights_clarity":0.13,"evidence_standard_quality":0.14,"review_cadence_quality":0.12,"trigger_authority":0.13,"accountability_clarity":0.12,"stakeholder_voice":0.12,"documentation_quality":0.12,"revision_capacity":0.12})
ethics_rows = weighted_rows(ethics, "ethics_burden_scores.csv", {"delay_burden":0.13,"experimentation_burden":0.14,"exit_burden":0.15,"asymmetric_flexibility":0.16,"stakeholder_voice":0.12,"transparency":0.10,"transition_support":0.10,"redress_quality":0.10}, negative=["stakeholder_voice","transparency","transition_support","redress_quality"])
memory_rows = weighted_rows(memory, "decision_memory_scores.csv", {"uncertainty_record_quality":0.11,"option_inventory_quality":0.12,"learning_agenda_quality":0.12,"trigger_record_quality":0.12,"lock_in_record_quality":0.12,"ethics_record_quality":0.11,"decision_gate_record_quality":0.11,"revision_history_quality":0.10,"reuse_quality":0.09})

scenario_cols = ["stable_growth","market_shift","regulatory_change","technology_disruption","stakeholder_resistance","cost_shock","implementation_delay","system_stress"]
scenario_rows=[]
for row in scenarios:
    vals=[f(row,c) for c in scenario_cols]
    mean=sum(vals)/len(vals); worst=min(vals); best=max(vals); volatility=math.sqrt(sum((v-mean)**2 for v in vals)/len(vals))
    robustness=0.40*worst+0.30*mean+0.12*best-0.18*volatility
    scenario_rows.append({**row,"option_name":option_names[row["option_id"]],"mean_performance":round(mean,4),"worst_case":round(worst,4),"best_case":round(best,4),"volatility":round(volatility,4),"robustness_score":round(robustness,4)})
scenario_rows.sort(key=lambda x: x["robustness_score"], reverse=True)
write_csv(TABLES / "scenario_option_scores.csv", scenario_rows, list(scenario_rows[0].keys()))

report=[]
report.append("# Option Value and Strategic Flexibility Diagnostic Report
")
report.append("## Executive summary
")
report.append("This diagnostic evaluates option value and strategic flexibility across uncertainty, learning, reversibility, modularity, lock-in, staged commitment, scenario robustness, expiration, governance, ethics, and decision memory.
")
sections=[("Strongest option-value profiles", option_rows[:6], "option_value_score"), ("Highest lock-in scores", lock_rows[:6], "lock_in_score"), ("Highest uncertainty materiality", uncertainty_rows[:6], "option_relevance"), ("Strongest learning experiments", experiment_rows[:6], "learning_experiment_score"), ("Strongest scenario robustness", scenario_rows[:6], "robustness_score"), ("Highest option expiration pressure", expiration_rows[:6], "option_expiration_score"), ("Strongest governance readiness", governance_rows[:6], "governance_readiness_score"), ("Highest ethics burden risk", ethics_rows[:6], "ethics_burden_score"), ("Strongest decision memory", memory_rows[:6], "decision_memory_score")]
for heading, rows, metric in sections:
    report.append(f"
## {heading}
")
    for item in rows:
        label = item.get("option_name") or item.get("experiment_name") or item.get("gate_name") or item.get("window_name") or item.get("governance_model") or item.get("ethical_issue") or item.get("memory_practice") or item.get("option_id")
        report.append(f"- **{label}**: {metric} = {item.get(metric, 'n/a')}.")
report.append("
## Professional interpretation
")
report.append("Option value is strongest when uncertainty is material, commitment is hard to reverse, learning improves future decisions, and governance defines when to expand, revise, pause, or stop. Strategic flexibility is not indefinite delay; it is disciplined commitment under uncertainty.
")
(REPORTS / "option_value_diagnostic_report.md").write_text("
".join(report), encoding="utf-8")
(REPORTS / "diagnostic_summary.json").write_text(json.dumps({"top_options": option_rows[:6], "lock_warnings": lock_rows[:6], "scenario_robustness": scenario_rows[:6]}, indent=2), encoding="utf-8")

print("Advanced option value and strategic flexibility diagnostics complete.")
for p in ["option_value_scores.csv","uncertainty_materiality_scores.csv","lock_in_reversibility_scores.csv","learning_experiment_scores.csv","decision_gate_scores.csv","modularity_switching_scores.csv","scenario_option_scores.csv","option_expiration_scores.csv","governance_readiness_scores.csv","ethics_burden_scores.csv","decision_memory_scores.csv"]:
    print(f"Wrote: {TABLES / p}")
print(f"Wrote: {REPORTS / 'option_value_diagnostic_report.md'}")
