#!/usr/bin/env python3
"""
Advanced strategist-facing diagnostics for Game Theory and Strategic Interaction.

This dependency-light workflow uses only the Python standard library.

It produces:
- strategic interaction scores
- actor payoff scores
- information signal scores
- equilibrium diagnosis scores
- cooperation fragility scores
- repeated interaction scores
- mechanism design scores
- behavioral game theory scores
- ethics and power scores
- strategic interaction memory scores
- a markdown strategist diagnostic report
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


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def f(row: dict[str, str], key: str) -> float:
    return float(row[key])


profiles = read_csv(RAW / "strategic_interaction_profiles.csv")
actors = read_csv(RAW / "actor_payoffs.csv")
signals = read_csv(RAW / "information_signals.csv")
equilibria = read_csv(RAW / "equilibrium_diagnoses.csv")
cooperation = read_csv(RAW / "cooperation_fragility.csv")
repeated = read_csv(RAW / "repeated_interactions.csv")
mechanisms = read_csv(RAW / "mechanism_design.csv")
behavioral = read_csv(RAW / "behavioral_game_theory.csv")
ethics = read_csv(RAW / "ethics_power.csv")
memory = read_csv(RAW / "strategic_interaction_memory.csv")

setting_names = {row["setting_id"]: row["setting_name"] for row in profiles}

# ---------------------------------------------------------------------
# 1. Strategic interaction profile scoring
# ---------------------------------------------------------------------

profile_rows: list[dict[str, object]] = []

for row in profiles:
    strategic_interaction_score = (
        0.12 * f(row, "rivalry")
        + 0.18 * f(row, "coordination_potential")
        + 0.12 * f(row, "information_asymmetry")
        + 0.10 * f(row, "retaliation_risk")
        + 0.15 * f(row, "institutional_support")
        + 0.12 * f(row, "behavioral_realism")
        + 0.15 * f(row, "mechanism_design_potential")
        + 0.06 * f(row, "ethical_complexity")
    )

    cooperation_fragility = (
        0.22 * f(row, "rivalry")
        + 0.20 * f(row, "retaliation_risk")
        + 0.16 * f(row, "information_asymmetry")
        + 0.12 * f(row, "ethical_complexity")
        - 0.15 * f(row, "institutional_support")
        - 0.15 * f(row, "coordination_potential")
    )

    mechanism_opportunity = (
        0.30 * f(row, "mechanism_design_potential")
        + 0.18 * f(row, "coordination_potential")
        + 0.16 * f(row, "information_asymmetry")
        + 0.14 * f(row, "ethical_complexity")
        + 0.12 * f(row, "institutional_support")
        + 0.10 * f(row, "behavioral_realism")
    )

    if cooperation_fragility >= 0.34:
        diagnosis = "high_cooperation_fragility"
    elif f(row, "mechanism_design_potential") >= 0.78:
        diagnosis = "strong_rule_redesign_opportunity"
    elif f(row, "coordination_potential") >= 0.78:
        diagnosis = "coordination_strategy_priority"
    elif f(row, "information_asymmetry") >= 0.70:
        diagnosis = "information_asymmetry_priority"
    else:
        diagnosis = "interaction_aware_strategy_needed"

    profile_rows.append(
        {
            "setting_id": row["setting_id"],
            "setting_name": row["setting_name"],
            "domain": row["domain"],
            "strategic_interaction_score": round(strategic_interaction_score, 4),
            "cooperation_fragility": round(cooperation_fragility, 4),
            "mechanism_opportunity": round(mechanism_opportunity, 4),
            "diagnosis": diagnosis,
            "rivalry": row["rivalry"],
            "coordination_potential": row["coordination_potential"],
            "information_asymmetry": row["information_asymmetry"],
            "retaliation_risk": row["retaliation_risk"],
            "institutional_support": row["institutional_support"],
            "behavioral_realism": row["behavioral_realism"],
            "mechanism_design_potential": row["mechanism_design_potential"],
            "ethical_complexity": row["ethical_complexity"],
            "description": row["description"],
        }
    )

profile_rows.sort(key=lambda item: item["mechanism_opportunity"], reverse=True)
write_csv(TABLES / "strategic_interaction_scores.csv", profile_rows, list(profile_rows[0].keys()))
write_csv(PROCESSED / "strategic_interaction_scores.csv", profile_rows, list(profile_rows[0].keys()))

# ---------------------------------------------------------------------
# 2. Actor payoff scoring
# ---------------------------------------------------------------------

actor_rows: list[dict[str, object]] = []

for row in actors:
    payoff_complexity = (
        0.14 * f(row, "material_payoff")
        + 0.12 * f(row, "reputation_payoff")
        + 0.12 * f(row, "legitimacy_payoff")
        + 0.12 * f(row, "risk_avoidance")
        + 0.12 * f(row, "control_preference")
        + 0.14 * f(row, "cooperation_dependency")
        + 0.10 * (1 - f(row, "exit_option_quality"))
        + 0.14 * f(row, "power_level")
    )

    power_dependency_risk = (
        0.24 * f(row, "power_level")
        + 0.18 * (1 - f(row, "exit_option_quality"))
        + 0.18 * f(row, "control_preference")
        + 0.14 * f(row, "risk_avoidance")
        + 0.14 * (1 - f(row, "cooperation_dependency"))
        + 0.12 * f(row, "material_payoff")
    )

    if power_dependency_risk >= 0.66:
        action = "review_power_and_dependency"
    elif f(row, "cooperation_dependency") >= 0.74:
        action = "build_cooperation_mechanism"
    elif f(row, "exit_option_quality") < 0.42:
        action = "improve_exit_or_voice"
    else:
        action = row["review_action"]

    actor_rows.append(
        {
            "actor_id": row["actor_id"],
            "setting_id": row["setting_id"],
            "setting_name": setting_names.get(row["setting_id"], row["setting_id"]),
            "actor_name": row["actor_name"],
            "actor_role": row["actor_role"],
            "payoff_complexity": round(payoff_complexity, 4),
            "power_dependency_risk": round(power_dependency_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "material_payoff": row["material_payoff"],
            "reputation_payoff": row["reputation_payoff"],
            "legitimacy_payoff": row["legitimacy_payoff"],
            "risk_avoidance": row["risk_avoidance"],
            "control_preference": row["control_preference"],
            "cooperation_dependency": row["cooperation_dependency"],
            "exit_option_quality": row["exit_option_quality"],
            "power_level": row["power_level"],
        }
    )

actor_rows.sort(key=lambda item: item["power_dependency_risk"], reverse=True)
write_csv(TABLES / "actor_payoff_scores.csv", actor_rows, list(actor_rows[0].keys()))

# ---------------------------------------------------------------------
# 3. Information signal scoring
# ---------------------------------------------------------------------

signal_rows: list[dict[str, object]] = []

for row in signals:
    signal_strength = (
        0.18 * f(row, "credibility")
        + 0.14 * f(row, "observability")
        + 0.16 * f(row, "costliness")
        - 0.12 * f(row, "ambiguity")
        + 0.12 * f(row, "response_sensitivity")
        - 0.12 * f(row, "misinterpretation_risk")
        + 0.16 * f(row, "coordination_value")
    )

    response_risk = (
        0.24 * f(row, "response_sensitivity")
        + 0.22 * f(row, "misinterpretation_risk")
        + 0.18 * f(row, "ambiguity")
        + 0.14 * (1 - f(row, "credibility"))
        + 0.12 * f(row, "observability")
        + 0.10 * f(row, "costliness")
    )

    if response_risk >= 0.62:
        action = "reduce_signal_misinterpretation"
    elif f(row, "coordination_value") >= 0.78:
        action = "use_as_coordination_signal"
    elif f(row, "credibility") < 0.60:
        action = "increase_signal_credibility"
    else:
        action = row["review_action"]

    signal_rows.append(
        {
            "signal_id": row["signal_id"],
            "setting_id": row["setting_id"],
            "setting_name": setting_names.get(row["setting_id"], row["setting_id"]),
            "signal_name": row["signal_name"],
            "signal_type": row["signal_type"],
            "signal_strength": round(signal_strength, 4),
            "response_risk": round(response_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "credibility": row["credibility"],
            "observability": row["observability"],
            "costliness": row["costliness"],
            "ambiguity": row["ambiguity"],
            "response_sensitivity": row["response_sensitivity"],
            "misinterpretation_risk": row["misinterpretation_risk"],
            "coordination_value": row["coordination_value"],
        }
    )

signal_rows.sort(key=lambda item: item["response_risk"], reverse=True)
write_csv(TABLES / "information_signal_scores.csv", signal_rows, list(signal_rows[0].keys()))

# ---------------------------------------------------------------------
# 4. Equilibrium diagnosis scoring
# ---------------------------------------------------------------------

equilibrium_rows: list[dict[str, object]] = []

for row in equilibria:
    bad_equilibrium_risk = (
        0.18 * (1 - f(row, "desirability"))
        + 0.15 * f(row, "stability")
        + 0.15 * (1 - f(row, "efficiency"))
        + 0.13 * (1 - f(row, "fairness"))
        + 0.10 * f(row, "exit_pressure")
        + 0.12 * f(row, "coordination_barrier")
        + 0.12 * f(row, "incentive_misalignment")
        + 0.05 * f(row, "rule_change_need")
    )

    redesign_priority = (
        0.20 * f(row, "rule_change_need")
        + 0.18 * f(row, "incentive_misalignment")
        + 0.16 * f(row, "coordination_barrier")
        + 0.14 * (1 - f(row, "desirability"))
        + 0.12 * (1 - f(row, "efficiency"))
        + 0.10 * (1 - f(row, "fairness"))
        + 0.10 * f(row, "stability")
    )

    if bad_equilibrium_risk >= 0.62:
        action = "urgent_equilibrium_shift_needed"
    elif redesign_priority >= 0.64:
        action = "prioritize_rule_or_incentive_redesign"
    elif f(row, "coordination_barrier") >= 0.70:
        action = "create_coordination_mechanism"
    else:
        action = row["review_action"]

    equilibrium_rows.append(
        {
            "equilibrium_id": row["equilibrium_id"],
            "setting_id": row["setting_id"],
            "setting_name": setting_names.get(row["setting_id"], row["setting_id"]),
            "equilibrium_name": row["equilibrium_name"],
            "bad_equilibrium_risk": round(bad_equilibrium_risk, 4),
            "redesign_priority": round(redesign_priority, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "desirability": row["desirability"],
            "stability": row["stability"],
            "efficiency": row["efficiency"],
            "fairness": row["fairness"],
            "exit_pressure": row["exit_pressure"],
            "coordination_barrier": row["coordination_barrier"],
            "incentive_misalignment": row["incentive_misalignment"],
            "rule_change_need": row["rule_change_need"],
        }
    )

equilibrium_rows.sort(key=lambda item: item["bad_equilibrium_risk"], reverse=True)
write_csv(TABLES / "equilibrium_diagnosis_scores.csv", equilibrium_rows, list(equilibrium_rows[0].keys()))

# ---------------------------------------------------------------------
# 5. Cooperation fragility scoring
# ---------------------------------------------------------------------

cooperation_rows: list[dict[str, object]] = []

for row in cooperation:
    fragility_score = (
        0.16 * (1 - f(row, "trust_level"))
        + 0.12 * (1 - f(row, "monitoring_quality"))
        + 0.18 * f(row, "defection_temptation")
        + 0.10 * (1 - f(row, "retaliation_feasibility"))
        + 0.10 * (1 - f(row, "reputation_value"))
        + 0.12 * (1 - f(row, "reciprocity_quality"))
        + 0.12 * (1 - f(row, "enforcement_quality"))
        + 0.10 * (1 - f(row, "shared_upside"))
    )

    cooperation_capacity = 1 - fragility_score

    if fragility_score >= 0.58:
        action = "high_cooperation_fragility"
    elif f(row, "monitoring_quality") < 0.52:
        action = "improve_monitoring_and_verification"
    elif f(row, "trust_level") < 0.48:
        action = "build_trust_and_staged_commitment"
    elif f(row, "defection_temptation") >= 0.70:
        action = "reduce_defection_incentive"
    else:
        action = row["review_action"]

    cooperation_rows.append(
        {
            "cooperation_id": row["cooperation_id"],
            "setting_id": row["setting_id"],
            "setting_name": setting_names.get(row["setting_id"], row["setting_id"]),
            "cooperation_need": row["cooperation_need"],
            "cooperation_fragility_score": round(fragility_score, 4),
            "cooperation_capacity": round(cooperation_capacity, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "trust_level": row["trust_level"],
            "monitoring_quality": row["monitoring_quality"],
            "defection_temptation": row["defection_temptation"],
            "retaliation_feasibility": row["retaliation_feasibility"],
            "reputation_value": row["reputation_value"],
            "reciprocity_quality": row["reciprocity_quality"],
            "enforcement_quality": row["enforcement_quality"],
            "shared_upside": row["shared_upside"],
        }
    )

cooperation_rows.sort(key=lambda item: item["cooperation_fragility_score"], reverse=True)
write_csv(TABLES / "cooperation_fragility_scores.csv", cooperation_rows, list(cooperation_rows[0].keys()))

# ---------------------------------------------------------------------
# 6. Repeated interaction scoring
# ---------------------------------------------------------------------

repeated_rows: list[dict[str, object]] = []

for row in repeated:
    repeated_game_capacity = (
        0.14 * f(row, "interaction_frequency")
        + 0.17 * f(row, "future_shadow")
        + 0.14 * f(row, "reputation_visibility")
        + 0.14 * f(row, "memory_quality")
        + 0.10 * f(row, "retaliation_proportionality")
        + 0.14 * f(row, "forgiveness_capacity")
        + 0.17 * f(row, "trust_repair_quality")
    )

    escalation_risk = (
        0.18 * f(row, "retaliation_proportionality")
        + 0.18 * (1 - f(row, "forgiveness_capacity"))
        + 0.16 * (1 - f(row, "trust_repair_quality"))
        + 0.14 * (1 - f(row, "memory_quality"))
        + 0.12 * (1 - f(row, "future_shadow"))
        + 0.12 * (1 - f(row, "reputation_visibility"))
        + 0.10 * f(row, "interaction_frequency")
    )

    if repeated_game_capacity >= 0.68:
        action = "strong_repeated_interaction_basis"
    elif escalation_risk >= 0.56:
        action = "reduce_escalation_and_repair_trust"
    elif f(row, "memory_quality") < 0.52:
        action = "improve_interaction_memory"
    else:
        action = row["review_action"]

    repeated_rows.append(
        {
            "repeat_id": row["repeat_id"],
            "setting_id": row["setting_id"],
            "setting_name": setting_names.get(row["setting_id"], row["setting_id"]),
            "relationship_name": row["relationship_name"],
            "repeated_game_capacity": round(repeated_game_capacity, 4),
            "escalation_risk": round(escalation_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "interaction_frequency": row["interaction_frequency"],
            "future_shadow": row["future_shadow"],
            "reputation_visibility": row["reputation_visibility"],
            "memory_quality": row["memory_quality"],
            "retaliation_proportionality": row["retaliation_proportionality"],
            "forgiveness_capacity": row["forgiveness_capacity"],
            "trust_repair_quality": row["trust_repair_quality"],
        }
    )

repeated_rows.sort(key=lambda item: item["repeated_game_capacity"], reverse=True)
write_csv(TABLES / "repeated_interaction_scores.csv", repeated_rows, list(repeated_rows[0].keys()))

# ---------------------------------------------------------------------
# 7. Mechanism design scoring
# ---------------------------------------------------------------------

mechanism_rows: list[dict[str, object]] = []

for row in mechanisms:
    mechanism_score = (
        0.15 * f(row, "incentive_alignment")
        + 0.13 * f(row, "information_transparency")
        + 0.13 * f(row, "verification_quality")
        + 0.13 * f(row, "enforcement_quality")
        + 0.12 * f(row, "participation_quality")
        + 0.13 * f(row, "burden_distribution_quality")
        + 0.11 * f(row, "adaptability")
        + 0.10 * f(row, "implementation_feasibility")
    )

    implementation_gap = 1 - mechanism_score

    if mechanism_score >= 0.72:
        action = "strong_mechanism_design"
    elif f(row, "incentive_alignment") < 0.58:
        action = "improve_incentive_alignment"
    elif f(row, "verification_quality") < 0.58:
        action = "improve_verification"
    elif f(row, "burden_distribution_quality") < 0.58:
        action = "review_burden_distribution"
    else:
        action = row["review_action"]

    mechanism_rows.append(
        {
            "mechanism_id": row["mechanism_id"],
            "setting_id": row["setting_id"],
            "setting_name": setting_names.get(row["setting_id"], row["setting_id"]),
            "mechanism_name": row["mechanism_name"],
            "mechanism_design_score": round(mechanism_score, 4),
            "implementation_gap": round(implementation_gap, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "incentive_alignment": row["incentive_alignment"],
            "information_transparency": row["information_transparency"],
            "verification_quality": row["verification_quality"],
            "enforcement_quality": row["enforcement_quality"],
            "participation_quality": row["participation_quality"],
            "burden_distribution_quality": row["burden_distribution_quality"],
            "adaptability": row["adaptability"],
            "implementation_feasibility": row["implementation_feasibility"],
        }
    )

mechanism_rows.sort(key=lambda item: item["mechanism_design_score"], reverse=True)
write_csv(TABLES / "mechanism_design_scores.csv", mechanism_rows, list(mechanism_rows[0].keys()))

# ---------------------------------------------------------------------
# 8. Behavioral game theory scoring
# ---------------------------------------------------------------------

behavior_rows: list[dict[str, object]] = []

for row in behavioral:
    behavioral_salience = (
        0.14 * f(row, "fairness_salience")
        + 0.14 * f(row, "trust_salience")
        + 0.12 * f(row, "identity_salience")
        + 0.14 * f(row, "bounded_reasoning_risk")
        + 0.14 * f(row, "loss_aversion_risk")
        + 0.14 * f(row, "norm_strength")
        + 0.18 * f(row, "legitimacy_sensitivity")
    )

    behavioral_failure_risk = (
        0.18 * f(row, "bounded_reasoning_risk")
        + 0.18 * f(row, "loss_aversion_risk")
        + 0.16 * f(row, "legitimacy_sensitivity")
        + 0.14 * f(row, "identity_salience")
        + 0.12 * f(row, "fairness_salience")
        + 0.12 * (1 - f(row, "trust_salience"))
        + 0.10 * (1 - f(row, "norm_strength"))
    )

    if behavioral_failure_risk >= 0.66:
        action = "integrate_behavioral_game_theory_review"
    elif f(row, "legitimacy_sensitivity") >= 0.78:
        action = "prioritize_legitimacy"
    elif f(row, "loss_aversion_risk") >= 0.72:
        action = "address_perceived_losses"
    else:
        action = row["review_action"]

    behavior_rows.append(
        {
            "behavior_id": row["behavior_id"],
            "setting_id": row["setting_id"],
            "setting_name": setting_names.get(row["setting_id"], row["setting_id"]),
            "behavioral_factor": row["behavioral_factor"],
            "behavioral_salience": round(behavioral_salience, 4),
            "behavioral_failure_risk": round(behavioral_failure_risk, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "fairness_salience": row["fairness_salience"],
            "trust_salience": row["trust_salience"],
            "identity_salience": row["identity_salience"],
            "bounded_reasoning_risk": row["bounded_reasoning_risk"],
            "loss_aversion_risk": row["loss_aversion_risk"],
            "norm_strength": row["norm_strength"],
            "legitimacy_sensitivity": row["legitimacy_sensitivity"],
        }
    )

behavior_rows.sort(key=lambda item: item["behavioral_failure_risk"], reverse=True)
write_csv(TABLES / "behavioral_game_theory_scores.csv", behavior_rows, list(behavior_rows[0].keys()))

# ---------------------------------------------------------------------
# 9. Ethics and power scoring
# ---------------------------------------------------------------------

ethics_rows: list[dict[str, object]] = []

for row in ethics:
    ethics_risk = (
        0.16 * f(row, "power_asymmetry")
        + 0.13 * (1 - f(row, "voice_quality"))
        + 0.13 * (1 - f(row, "exit_option_quality"))
        + 0.12 * (1 - f(row, "transparency"))
        + 0.16 * f(row, "burden_shift_risk")
        + 0.14 * f(row, "manipulation_risk")
        + 0.10 * (1 - f(row, "legitimacy_quality"))
        + 0.06 * (1 - f(row, "redress_quality"))
    )

    responsibility_score = 1 - ethics_risk

    if ethics_risk >= 0.62:
        action = "urgent_ethics_and_power_review"
    elif f(row, "power_asymmetry") >= 0.75:
        action = "review_power_asymmetry"
    elif f(row, "exit_option_quality") < 0.45:
        action = "improve_exit_or_voice"
    elif f(row, "burden_shift_risk") >= 0.75:
        action = "review_burden_shifting"
    else:
        action = row["review_action"]

    ethics_rows.append(
        {
            "ethics_id": row["ethics_id"],
            "setting_id": row["setting_id"],
            "setting_name": setting_names.get(row["setting_id"], row["setting_id"]),
            "ethical_issue": row["ethical_issue"],
            "ethics_power_risk": round(ethics_risk, 4),
            "responsibility_score": round(responsibility_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "power_asymmetry": row["power_asymmetry"],
            "voice_quality": row["voice_quality"],
            "exit_option_quality": row["exit_option_quality"],
            "transparency": row["transparency"],
            "burden_shift_risk": row["burden_shift_risk"],
            "manipulation_risk": row["manipulation_risk"],
            "legitimacy_quality": row["legitimacy_quality"],
            "redress_quality": row["redress_quality"],
        }
    )

ethics_rows.sort(key=lambda item: item["ethics_power_risk"], reverse=True)
write_csv(TABLES / "ethics_power_scores.csv", ethics_rows, list(ethics_rows[0].keys()))

# ---------------------------------------------------------------------
# 10. Strategic interaction memory scoring
# ---------------------------------------------------------------------

memory_rows: list[dict[str, object]] = []

for row in memory:
    memory_score = (
        0.11 * f(row, "player_record_quality")
        + 0.11 * f(row, "payoff_record_quality")
        + 0.11 * f(row, "information_record_quality")
        + 0.12 * f(row, "equilibrium_record_quality")
        + 0.11 * f(row, "signal_record_quality")
        + 0.12 * f(row, "mechanism_record_quality")
        + 0.11 * f(row, "ethics_record_quality")
        + 0.10 * f(row, "revision_record_quality")
        + 0.11 * f(row, "reuse_quality")
    )

    if memory_score >= 0.70:
        action = "strong_strategic_interaction_memory"
    elif f(row, "equilibrium_record_quality") < 0.52:
        action = "document_equilibrium_logic"
    elif f(row, "mechanism_record_quality") < 0.52:
        action = "document_rule_design_logic"
    elif f(row, "ethics_record_quality") < 0.52:
        action = "document_ethics_and_power"
    else:
        action = row["review_action"]

    memory_rows.append(
        {
            "memory_id": row["memory_id"],
            "setting_id": row["setting_id"],
            "setting_name": setting_names.get(row["setting_id"], row["setting_id"]),
            "memory_practice": row["memory_practice"],
            "strategic_interaction_memory_score": round(memory_score, 4),
            "recommended_action": action,
            "source_review_action": row["review_action"],
            "player_record_quality": row["player_record_quality"],
            "payoff_record_quality": row["payoff_record_quality"],
            "information_record_quality": row["information_record_quality"],
            "equilibrium_record_quality": row["equilibrium_record_quality"],
            "signal_record_quality": row["signal_record_quality"],
            "mechanism_record_quality": row["mechanism_record_quality"],
            "ethics_record_quality": row["ethics_record_quality"],
            "revision_record_quality": row["revision_record_quality"],
            "reuse_quality": row["reuse_quality"],
        }
    )

memory_rows.sort(key=lambda item: item["strategic_interaction_memory_score"], reverse=True)
write_csv(TABLES / "strategic_interaction_memory_scores.csv", memory_rows, list(memory_rows[0].keys()))

# ---------------------------------------------------------------------
# 11. Strategist report
# ---------------------------------------------------------------------

top_profiles = profile_rows[:6]
fragile_profiles = sorted(profile_rows, key=lambda item: item["cooperation_fragility"], reverse=True)[:5]
mechanism_opportunities = sorted(profile_rows, key=lambda item: item["mechanism_opportunity"], reverse=True)[:5]
actor_risks = actor_rows[:6]
signal_risks = signal_rows[:6]
bad_equilibria = equilibrium_rows[:6]
cooperation_risks = cooperation_rows[:6]
repeated_strengths = repeated_rows[:5]
mechanism_strengths = mechanism_rows[:6]
mechanism_gaps = sorted(mechanism_rows, key=lambda item: item["implementation_gap"], reverse=True)[:5]
behavioral_risks = behavior_rows[:6]
ethics_risks = ethics_rows[:6]
memory_strengths = memory_rows[:5]
memory_gaps = sorted(memory_rows, key=lambda item: item["strategic_interaction_memory_score"])[:4]

report: list[str] = []
report.append("# Game Theory and Strategic Interaction Diagnostic Report")
report.append("")
report.append("## Executive summary")
report.append("")
report.append(
    "This diagnostic evaluates strategic interaction environments. It reviews players, incentives, payoffs, signals, equilibrium risks, cooperation fragility, repeated interaction, mechanism design, behavioral realism, ethics, power, and strategic learning memory."
)

report.append("")
report.append("## Highest mechanism-design opportunities")
report.append("")
for item in mechanism_opportunities:
    report.append(
        f"- **{item['setting_id']} — {item['setting_name']}**: mechanism opportunity {item['mechanism_opportunity']}; "
        f"cooperation fragility {item['cooperation_fragility']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Strategic interaction profiles")
report.append("")
for item in top_profiles:
    report.append(
        f"- **{item['setting_id']} — {item['setting_name']}**: interaction score {item['strategic_interaction_score']}; "
        f"mechanism opportunity {item['mechanism_opportunity']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Highest cooperation fragility")
report.append("")
for item in fragile_profiles:
    report.append(
        f"- **{item['setting_id']} — {item['setting_name']}**: cooperation fragility {item['cooperation_fragility']}; "
        f"mechanism opportunity {item['mechanism_opportunity']}; diagnosis: {item['diagnosis']}."
    )

report.append("")
report.append("## Actor payoff and power risks")
report.append("")
for item in actor_risks:
    report.append(
        f"- **{item['actor_id']} — {item['actor_name']}**: power/dependency risk {item['power_dependency_risk']}; "
        f"payoff complexity {item['payoff_complexity']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Signal and misinterpretation risks")
report.append("")
for item in signal_risks:
    report.append(
        f"- **{item['signal_id']} — {item['signal_name']}**: response risk {item['response_risk']}; "
        f"signal strength {item['signal_strength']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Bad equilibrium risks")
report.append("")
for item in bad_equilibria:
    report.append(
        f"- **{item['equilibrium_id']} — {item['equilibrium_name']}**: bad equilibrium risk {item['bad_equilibrium_risk']}; "
        f"redesign priority {item['redesign_priority']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Cooperation fragility risks")
report.append("")
for item in cooperation_risks:
    report.append(
        f"- **{item['cooperation_id']} — {item['cooperation_need']}**: fragility {item['cooperation_fragility_score']}; "
        f"capacity {item['cooperation_capacity']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strongest repeated-interaction bases")
report.append("")
for item in repeated_strengths:
    report.append(
        f"- **{item['repeat_id']} — {item['relationship_name']}**: repeated-game capacity {item['repeated_game_capacity']}; "
        f"escalation risk {item['escalation_risk']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strongest mechanism designs")
report.append("")
for item in mechanism_strengths:
    report.append(
        f"- **{item['mechanism_id']} — {item['mechanism_name']}**: design score {item['mechanism_design_score']}; "
        f"implementation gap {item['implementation_gap']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Mechanism design gaps")
report.append("")
for item in mechanism_gaps:
    report.append(
        f"- **{item['mechanism_id']} — {item['mechanism_name']}**: implementation gap {item['implementation_gap']}; "
        f"design score {item['mechanism_design_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Behavioral game-theory risks")
report.append("")
for item in behavioral_risks:
    report.append(
        f"- **{item['behavior_id']} — {item['behavioral_factor']}**: behavioral failure risk {item['behavioral_failure_risk']}; "
        f"behavioral salience {item['behavioral_salience']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Ethics and power risks")
report.append("")
for item in ethics_risks:
    report.append(
        f"- **{item['ethics_id']} — {item['ethical_issue']}**: ethics/power risk {item['ethics_power_risk']}; "
        f"responsibility score {item['responsibility_score']}; action: {item['recommended_action']}."
    )

report.append("")
report.append("## Strategic interaction memory")
report.append("")
for item in memory_strengths:
    report.append(
        f"- **{item['memory_id']} — {item['memory_practice']}**: memory score {item['strategic_interaction_memory_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Weak interaction-memory warnings")
report.append("")
for item in memory_gaps:
    report.append(
        f"- **{item['memory_id']} — {item['memory_practice']}**: memory score {item['strategic_interaction_memory_score']}; "
        f"action: {item['recommended_action']}."
    )

report.append("")
report.append("## Professional interpretation")
report.append("")
report.append(
    "Game-theoretic strategy is strongest when strategic ideas are tested against response. The central question is not only what the organization should do, but what that move will cause others to do next. Better strategy often requires redesigning incentives, information, timing, rules, and governance rather than merely selecting a more forceful move."
)

(REPORTS / "game_theory_diagnostic_report.md").write_text("\n".join(report), encoding="utf-8")

summary = {
    "top_profiles": top_profiles,
    "fragile_profiles": fragile_profiles,
    "mechanism_opportunities": mechanism_opportunities,
    "actor_risks": actor_risks,
    "signal_risks": signal_risks,
    "bad_equilibria": bad_equilibria,
    "cooperation_risks": cooperation_risks,
    "repeated_strengths": repeated_strengths,
    "mechanism_strengths": mechanism_strengths,
    "mechanism_gaps": mechanism_gaps,
    "behavioral_risks": behavioral_risks,
    "ethics_risks": ethics_risks,
    "memory_strengths": memory_strengths,
    "memory_gaps": memory_gaps,
}

(REPORTS / "diagnostic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

print("Advanced game theory and strategic interaction diagnostics complete.")
print(f"Wrote: {TABLES / 'strategic_interaction_scores.csv'}")
print(f"Wrote: {TABLES / 'actor_payoff_scores.csv'}")
print(f"Wrote: {TABLES / 'information_signal_scores.csv'}")
print(f"Wrote: {TABLES / 'equilibrium_diagnosis_scores.csv'}")
print(f"Wrote: {TABLES / 'cooperation_fragility_scores.csv'}")
print(f"Wrote: {TABLES / 'repeated_interaction_scores.csv'}")
print(f"Wrote: {TABLES / 'mechanism_design_scores.csv'}")
print(f"Wrote: {TABLES / 'behavioral_game_theory_scores.csv'}")
print(f"Wrote: {TABLES / 'ethics_power_scores.csv'}")
print(f"Wrote: {TABLES / 'strategic_interaction_memory_scores.csv'}")
print(f"Wrote: {REPORTS / 'game_theory_diagnostic_report.md'}")
