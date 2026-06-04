-- Advanced SQL schema for second-order effects and unintended consequences.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS second_order_effect_scores;
DROP VIEW IF EXISTS propagation_pathway_scores;
DROP VIEW IF EXISTS feedback_loop_scores;
DROP VIEW IF EXISTS adaptive_actor_scores;
DROP VIEW IF EXISTS burden_shift_scores;
DROP VIEW IF EXISTS fragility_scores;
DROP VIEW IF EXISTS scenario_stress_scores;
DROP VIEW IF EXISTS early_warning_indicator_scores;
DROP VIEW IF EXISTS learning_loop_scores;
DROP VIEW IF EXISTS intervention_value_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS intervention_library;
DROP TABLE IF EXISTS learning_loops;
DROP TABLE IF EXISTS early_warning_indicators;
DROP TABLE IF EXISTS scenario_stress_tests;
DROP TABLE IF EXISTS fragility_risks;
DROP TABLE IF EXISTS burden_shifts;
DROP TABLE IF EXISTS adaptive_actors;
DROP TABLE IF EXISTS feedback_loops;
DROP TABLE IF EXISTS propagation_pathways;
DROP TABLE IF EXISTS interventions;

CREATE TABLE interventions (
    intervention_id TEXT PRIMARY KEY,
    intervention_name TEXT NOT NULL,
    intervention_type TEXT NOT NULL,
    domain TEXT NOT NULL,
    first_order_gain REAL CHECK (first_order_gain BETWEEN 0 AND 1),
    adaptation_pressure REAL CHECK (adaptation_pressure BETWEEN 0 AND 1),
    feedback_amplification REAL CHECK (feedback_amplification BETWEEN 0 AND 1),
    delay_risk REAL CHECK (delay_risk BETWEEN 0 AND 1),
    burden_shift_risk REAL CHECK (burden_shift_risk BETWEEN 0 AND 1),
    gaming_risk REAL CHECK (gaming_risk BETWEEN 0 AND 1),
    long_term_fragility REAL CHECK (long_term_fragility BETWEEN 0 AND 1),
    learning_capacity REAL CHECK (learning_capacity BETWEEN 0 AND 1),
    stakeholder_legitimacy REAL CHECK (stakeholder_legitimacy BETWEEN 0 AND 1),
    strategic_reversibility REAL CHECK (strategic_reversibility BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE propagation_pathways (
    pathway_id TEXT PRIMARY KEY,
    intervention_id TEXT NOT NULL,
    pathway_name TEXT NOT NULL,
    pathway_type TEXT NOT NULL,
    cross_boundary_reach REAL CHECK (cross_boundary_reach BETWEEN 0 AND 1),
    dependency_creation REAL CHECK (dependency_creation BETWEEN 0 AND 1),
    externality_risk REAL CHECK (externality_risk BETWEEN 0 AND 1),
    downstream_visibility REAL CHECK (downstream_visibility BETWEEN 0 AND 1),
    time_to_visibility REAL CHECK (time_to_visibility BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    monitoring_quality REAL CHECK (monitoring_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (intervention_id) REFERENCES interventions(intervention_id)
);

CREATE TABLE feedback_loops (
    loop_id TEXT PRIMARY KEY,
    intervention_id TEXT NOT NULL,
    loop_name TEXT NOT NULL,
    loop_type TEXT NOT NULL,
    loop_strength REAL CHECK (loop_strength BETWEEN 0 AND 1),
    visibility REAL CHECK (visibility BETWEEN 0 AND 1),
    reinforcing_risk REAL CHECK (reinforcing_risk BETWEEN 0 AND 1),
    balancing_capacity REAL CHECK (balancing_capacity BETWEEN 0 AND 1),
    policy_resistance_risk REAL CHECK (policy_resistance_risk BETWEEN 0 AND 1),
    delay_risk REAL CHECK (delay_risk BETWEEN 0 AND 1),
    intervention_readiness REAL CHECK (intervention_readiness BETWEEN 0 AND 1),
    diagnostic_note TEXT,
    FOREIGN KEY (intervention_id) REFERENCES interventions(intervention_id)
);

CREATE TABLE adaptive_actors (
    actor_id TEXT PRIMARY KEY,
    intervention_id TEXT NOT NULL,
    actor_group TEXT NOT NULL,
    adaptation_speed REAL CHECK (adaptation_speed BETWEEN 0 AND 1),
    strategic_awareness REAL CHECK (strategic_awareness BETWEEN 0 AND 1),
    workaround_likelihood REAL CHECK (workaround_likelihood BETWEEN 0 AND 1),
    resistance_likelihood REAL CHECK (resistance_likelihood BETWEEN 0 AND 1),
    gaming_likelihood REAL CHECK (gaming_likelihood BETWEEN 0 AND 1),
    imitation_likelihood REAL CHECK (imitation_likelihood BETWEEN 0 AND 1),
    trust_sensitivity REAL CHECK (trust_sensitivity BETWEEN 0 AND 1),
    influence_on_outcome REAL CHECK (influence_on_outcome BETWEEN 0 AND 1),
    monitoring_gap REAL CHECK (monitoring_gap BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (intervention_id) REFERENCES interventions(intervention_id)
);

CREATE TABLE burden_shifts (
    burden_id TEXT PRIMARY KEY,
    intervention_id TEXT NOT NULL,
    burden_location TEXT NOT NULL,
    burden_type TEXT NOT NULL,
    hidden_cost REAL CHECK (hidden_cost BETWEEN 0 AND 1),
    administrative_load REAL CHECK (administrative_load BETWEEN 0 AND 1),
    emotional_load REAL CHECK (emotional_load BETWEEN 0 AND 1),
    risk_transfer REAL CHECK (risk_transfer BETWEEN 0 AND 1),
    equity_risk REAL CHECK (equity_risk BETWEEN 0 AND 1),
    visibility_to_decision_makers REAL CHECK (visibility_to_decision_makers BETWEEN 0 AND 1),
    participatory_review_quality REAL CHECK (participatory_review_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (intervention_id) REFERENCES interventions(intervention_id)
);

CREATE TABLE fragility_risks (
    fragility_id TEXT PRIMARY KEY,
    intervention_id TEXT NOT NULL,
    fragility_type TEXT NOT NULL,
    slack_reduction REAL CHECK (slack_reduction BETWEEN 0 AND 1),
    redundancy_reduction REAL CHECK (redundancy_reduction BETWEEN 0 AND 1),
    trust_erosion REAL CHECK (trust_erosion BETWEEN 0 AND 1),
    option_closure REAL CHECK (option_closure BETWEEN 0 AND 1),
    dependency_creation REAL CHECK (dependency_creation BETWEEN 0 AND 1),
    recovery_capacity_loss REAL CHECK (recovery_capacity_loss BETWEEN 0 AND 1),
    stress_exposure REAL CHECK (stress_exposure BETWEEN 0 AND 1),
    monitoring_quality REAL CHECK (monitoring_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (intervention_id) REFERENCES interventions(intervention_id)
);

CREATE TABLE scenario_stress_tests (
    scenario_id TEXT PRIMARY KEY,
    intervention_id TEXT NOT NULL,
    scenario_name TEXT NOT NULL,
    scenario_type TEXT NOT NULL,
    plausibility REAL CHECK (plausibility BETWEEN 0 AND 1),
    severity REAL CHECK (severity BETWEEN 0 AND 1),
    delay_exposure REAL CHECK (delay_exposure BETWEEN 0 AND 1),
    adaptation_exposure REAL CHECK (adaptation_exposure BETWEEN 0 AND 1),
    feedback_exposure REAL CHECK (feedback_exposure BETWEEN 0 AND 1),
    burden_exposure REAL CHECK (burden_exposure BETWEEN 0 AND 1),
    fragility_exposure REAL CHECK (fragility_exposure BETWEEN 0 AND 1),
    preparation_quality REAL CHECK (preparation_quality BETWEEN 0 AND 1),
    response_flexibility REAL CHECK (response_flexibility BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (intervention_id) REFERENCES interventions(intervention_id)
);

CREATE TABLE early_warning_indicators (
    indicator_id TEXT PRIMARY KEY,
    intervention_id TEXT NOT NULL,
    indicator_name TEXT NOT NULL,
    signal_type TEXT NOT NULL,
    leading_quality REAL CHECK (leading_quality BETWEEN 0 AND 1),
    visibility REAL CHECK (visibility BETWEEN 0 AND 1),
    reliability REAL CHECK (reliability BETWEEN 0 AND 1),
    timeliness REAL CHECK (timeliness BETWEEN 0 AND 1),
    sensitivity REAL CHECK (sensitivity BETWEEN 0 AND 1),
    false_positive_risk REAL CHECK (false_positive_risk BETWEEN 0 AND 1),
    decision_linkage REAL CHECK (decision_linkage BETWEEN 0 AND 1),
    monitoring_cost REAL CHECK (monitoring_cost BETWEEN 0 AND 1),
    trigger_threshold REAL CHECK (trigger_threshold BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (intervention_id) REFERENCES interventions(intervention_id)
);

CREATE TABLE learning_loops (
    learning_id TEXT PRIMARY KEY,
    intervention_id TEXT NOT NULL,
    learning_loop_name TEXT NOT NULL,
    feedback_quality REAL CHECK (feedback_quality BETWEEN 0 AND 1),
    revision_trigger_clarity REAL CHECK (revision_trigger_clarity BETWEEN 0 AND 1),
    decision_memory_quality REAL CHECK (decision_memory_quality BETWEEN 0 AND 1),
    stakeholder_learning_visibility REAL CHECK (stakeholder_learning_visibility BETWEEN 0 AND 1),
    scenario_update_quality REAL CHECK (scenario_update_quality BETWEEN 0 AND 1),
    governance_response_capacity REAL CHECK (governance_response_capacity BETWEEN 0 AND 1),
    cycle_time REAL CHECK (cycle_time BETWEEN 0 AND 1),
    learning_risk REAL CHECK (learning_risk BETWEEN 0 AND 1),
    action_if_triggered TEXT,
    FOREIGN KEY (intervention_id) REFERENCES interventions(intervention_id)
);

CREATE TABLE intervention_library (
    intervention_id TEXT PRIMARY KEY,
    intervention_name TEXT NOT NULL,
    target_second_order_risk TEXT NOT NULL,
    process_cost REAL CHECK (process_cost BETWEEN 0 AND 1),
    implementation_complexity REAL CHECK (implementation_complexity BETWEEN 0 AND 1),
    propagation_mapping_gain REAL CHECK (propagation_mapping_gain BETWEEN 0 AND 1),
    feedback_review_gain REAL CHECK (feedback_review_gain BETWEEN 0 AND 1),
    burden_review_gain REAL CHECK (burden_review_gain BETWEEN 0 AND 1),
    incentive_review_gain REAL CHECK (incentive_review_gain BETWEEN 0 AND 1),
    fragility_review_gain REAL CHECK (fragility_review_gain BETWEEN 0 AND 1),
    learning_gain REAL CHECK (learning_gain BETWEEN 0 AND 1),
    decision_memory_gain REAL CHECK (decision_memory_gain BETWEEN 0 AND 1),
    political_safety_need REAL CHECK (political_safety_need BETWEEN 0 AND 1)
);

CREATE TABLE decision_memory (
    decision_id TEXT PRIMARY KEY,
    intervention_id TEXT NOT NULL,
    decision_date TEXT,
    first_order_effect TEXT,
    anticipated_second_order_effects TEXT,
    propagation_pathways TEXT,
    feedback_loops_reviewed TEXT,
    adaptive_actors_reviewed TEXT,
    burden_shifts_reviewed TEXT,
    fragility_risks_reviewed TEXT,
    scenarios_tested TEXT,
    early_warning_indicators TEXT,
    revision_triggers TEXT,
    archived_learning TEXT,
    FOREIGN KEY (intervention_id) REFERENCES interventions(intervention_id)
);

CREATE VIEW second_order_effect_scores AS
SELECT
    intervention_id,
    intervention_name,
    intervention_type,
    domain,
    ROUND(
      0.16 * adaptation_pressure +
      0.15 * feedback_amplification +
      0.14 * delay_risk +
      0.15 * burden_shift_risk +
      0.14 * gaming_risk +
      0.16 * long_term_fragility -
      0.10 * learning_capacity -
      0.06 * stakeholder_legitimacy -
      0.06 * strategic_reversibility,
      4
    ) AS second_order_risk_score
FROM interventions;

CREATE VIEW propagation_pathway_scores AS
SELECT
    pathway_id,
    intervention_id,
    pathway_name,
    pathway_type,
    ROUND(
      0.16 * cross_boundary_reach +
      0.15 * dependency_creation +
      0.16 * externality_risk +
      0.14 * time_to_visibility -
      0.12 * downstream_visibility -
      0.12 * reversibility -
      0.10 * monitoring_quality,
      4
    ) AS pathway_risk_score
FROM propagation_pathways;

CREATE VIEW feedback_loop_scores AS
SELECT
    loop_id,
    intervention_id,
    loop_name,
    loop_type,
    ROUND(
      0.16 * loop_strength +
      0.16 * reinforcing_risk +
      0.16 * policy_resistance_risk +
      0.13 * delay_risk -
      0.12 * visibility -
      0.12 * balancing_capacity -
      0.10 * intervention_readiness,
      4
    ) AS feedback_risk_score
FROM feedback_loops;

CREATE VIEW adaptive_actor_scores AS
SELECT
    actor_id,
    intervention_id,
    actor_group,
    ROUND(
      0.14 * adaptation_speed +
      0.14 * strategic_awareness +
      0.14 * workaround_likelihood +
      0.14 * resistance_likelihood +
      0.14 * gaming_likelihood +
      0.10 * imitation_likelihood +
      0.12 * influence_on_outcome +
      0.10 * monitoring_gap -
      0.10 * trust_sensitivity,
      4
    ) AS adaptation_risk_score
FROM adaptive_actors;

CREATE VIEW burden_shift_scores AS
SELECT
    burden_id,
    intervention_id,
    burden_location,
    burden_type,
    ROUND(
      0.16 * hidden_cost +
      0.15 * administrative_load +
      0.13 * emotional_load +
      0.14 * risk_transfer +
      0.14 * equity_risk -
      0.14 * visibility_to_decision_makers -
      0.14 * participatory_review_quality,
      4
    ) AS burden_risk_score
FROM burden_shifts;

CREATE VIEW fragility_scores AS
SELECT
    fragility_id,
    intervention_id,
    fragility_type,
    ROUND(
      0.14 * slack_reduction +
      0.13 * redundancy_reduction +
      0.13 * trust_erosion +
      0.13 * option_closure +
      0.14 * dependency_creation +
      0.14 * recovery_capacity_loss +
      0.13 * stress_exposure -
      0.12 * monitoring_quality,
      4
    ) AS fragility_score
FROM fragility_risks;

CREATE VIEW scenario_stress_scores AS
SELECT
    scenario_id,
    intervention_id,
    scenario_name,
    scenario_type,
    ROUND(
      0.12 * plausibility +
      0.14 * severity +
      0.13 * delay_exposure +
      0.13 * adaptation_exposure +
      0.13 * feedback_exposure +
      0.13 * burden_exposure +
      0.14 * fragility_exposure -
      0.10 * preparation_quality -
      0.08 * response_flexibility,
      4
    ) AS scenario_risk_score
FROM scenario_stress_tests;

CREATE VIEW early_warning_indicator_scores AS
SELECT
    indicator_id,
    intervention_id,
    indicator_name,
    signal_type,
    ROUND(
      0.15 * leading_quality +
      0.13 * visibility +
      0.13 * reliability +
      0.13 * timeliness +
      0.12 * sensitivity +
      0.14 * decision_linkage -
      0.08 * false_positive_risk -
      0.08 * monitoring_cost,
      4
    ) AS indicator_quality_score
FROM early_warning_indicators;

CREATE VIEW learning_loop_scores AS
SELECT
    learning_id,
    intervention_id,
    learning_loop_name,
    ROUND(
      0.14 * feedback_quality +
      0.14 * revision_trigger_clarity +
      0.14 * decision_memory_quality +
      0.14 * stakeholder_learning_visibility +
      0.12 * scenario_update_quality +
      0.12 * governance_response_capacity +
      0.08 * cycle_time -
      0.10 * learning_risk,
      4
    ) AS learning_quality_score
FROM learning_loops;

CREATE VIEW intervention_value_scores AS
SELECT
    intervention_id,
    intervention_name,
    target_second_order_risk,
    ROUND(
      0.13 * propagation_mapping_gain +
      0.14 * feedback_review_gain +
      0.14 * burden_review_gain +
      0.13 * incentive_review_gain +
      0.13 * fragility_review_gain +
      0.14 * learning_gain +
      0.13 * decision_memory_gain -
      0.08 * process_cost -
      0.08 * implementation_complexity -
      0.08 * political_safety_need,
      4
    ) AS intervention_value_score
FROM intervention_library;
