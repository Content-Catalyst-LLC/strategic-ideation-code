-- Advanced SQL schema for complex systems and strategic uncertainty.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS complexity_profile_scores;
DROP VIEW IF EXISTS uncertainty_driver_scores;
DROP VIEW IF EXISTS feedback_loop_scores;
DROP VIEW IF EXISTS adaptive_actor_scores;
DROP VIEW IF EXISTS path_dependence_scores;
DROP VIEW IF EXISTS scenario_risk_scores;
DROP VIEW IF EXISTS adaptive_option_scores;
DROP VIEW IF EXISTS early_warning_indicator_scores;
DROP VIEW IF EXISTS learning_loop_scores;
DROP VIEW IF EXISTS intervention_value_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS intervention_library;
DROP TABLE IF EXISTS learning_loops;
DROP TABLE IF EXISTS early_warning_indicators;
DROP TABLE IF EXISTS adaptive_options;
DROP TABLE IF EXISTS scenario_robustness;
DROP TABLE IF EXISTS path_dependence;
DROP TABLE IF EXISTS adaptive_actors;
DROP TABLE IF EXISTS feedback_loops;
DROP TABLE IF EXISTS uncertainty_drivers;
DROP TABLE IF EXISTS complexity_environments;

CREATE TABLE complexity_environments (
    environment_id TEXT PRIMARY KEY,
    environment_name TEXT NOT NULL,
    environment_type TEXT NOT NULL,
    domain TEXT NOT NULL,
    interdependence REAL CHECK (interdependence BETWEEN 0 AND 1),
    nonlinearity REAL CHECK (nonlinearity BETWEEN 0 AND 1),
    feedback_intensity REAL CHECK (feedback_intensity BETWEEN 0 AND 1),
    adaptation_pressure REAL CHECK (adaptation_pressure BETWEEN 0 AND 1),
    path_dependence REAL CHECK (path_dependence BETWEEN 0 AND 1),
    boundary_ambiguity REAL CHECK (boundary_ambiguity BETWEEN 0 AND 1),
    emergence_potential REAL CHECK (emergence_potential BETWEEN 0 AND 1),
    deep_uncertainty REAL CHECK (deep_uncertainty BETWEEN 0 AND 1),
    scenario_need REAL CHECK (scenario_need BETWEEN 0 AND 1),
    learning_capacity_need REAL CHECK (learning_capacity_need BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE uncertainty_drivers (
    driver_id TEXT PRIMARY KEY,
    environment_id TEXT NOT NULL,
    driver_name TEXT NOT NULL,
    driver_type TEXT NOT NULL,
    volatility REAL CHECK (volatility BETWEEN 0 AND 1),
    ambiguity REAL CHECK (ambiguity BETWEEN 0 AND 1),
    model_uncertainty REAL CHECK (model_uncertainty BETWEEN 0 AND 1),
    probability_instability REAL CHECK (probability_instability BETWEEN 0 AND 1),
    value_contestation REAL CHECK (value_contestation BETWEEN 0 AND 1),
    actor_reflexivity REAL CHECK (actor_reflexivity BETWEEN 0 AND 1),
    monitoring_quality REAL CHECK (monitoring_quality BETWEEN 0 AND 1),
    mitigation_quality REAL CHECK (mitigation_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (environment_id) REFERENCES complexity_environments(environment_id)
);

CREATE TABLE feedback_loops (
    loop_id TEXT PRIMARY KEY,
    environment_id TEXT NOT NULL,
    loop_name TEXT NOT NULL,
    loop_type TEXT NOT NULL,
    loop_strength REAL CHECK (loop_strength BETWEEN 0 AND 1),
    visibility REAL CHECK (visibility BETWEEN 0 AND 1),
    reinforcing_risk REAL CHECK (reinforcing_risk BETWEEN 0 AND 1),
    balancing_capacity REAL CHECK (balancing_capacity BETWEEN 0 AND 1),
    delay_risk REAL CHECK (delay_risk BETWEEN 0 AND 1),
    intervention_readiness REAL CHECK (intervention_readiness BETWEEN 0 AND 1),
    stakeholder_burden_risk REAL CHECK (stakeholder_burden_risk BETWEEN 0 AND 1),
    diagnostic_note TEXT,
    FOREIGN KEY (environment_id) REFERENCES complexity_environments(environment_id)
);

CREATE TABLE adaptive_actors (
    actor_id TEXT PRIMARY KEY,
    environment_id TEXT NOT NULL,
    actor_group TEXT NOT NULL,
    adaptation_speed REAL CHECK (adaptation_speed BETWEEN 0 AND 1),
    strategic_awareness REAL CHECK (strategic_awareness BETWEEN 0 AND 1),
    workaround_likelihood REAL CHECK (workaround_likelihood BETWEEN 0 AND 1),
    imitation_likelihood REAL CHECK (imitation_likelihood BETWEEN 0 AND 1),
    resistance_likelihood REAL CHECK (resistance_likelihood BETWEEN 0 AND 1),
    gaming_likelihood REAL CHECK (gaming_likelihood BETWEEN 0 AND 1),
    learning_capacity REAL CHECK (learning_capacity BETWEEN 0 AND 1),
    influence_on_system REAL CHECK (influence_on_system BETWEEN 0 AND 1),
    monitoring_gap REAL CHECK (monitoring_gap BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (environment_id) REFERENCES complexity_environments(environment_id)
);

CREATE TABLE path_dependence (
    path_id TEXT PRIMARY KEY,
    environment_id TEXT NOT NULL,
    path_factor TEXT NOT NULL,
    path_type TEXT NOT NULL,
    legacy_strength REAL CHECK (legacy_strength BETWEEN 0 AND 1),
    sunk_cost_pressure REAL CHECK (sunk_cost_pressure BETWEEN 0 AND 1),
    coordination_lock_in REAL CHECK (coordination_lock_in BETWEEN 0 AND 1),
    standardization_lock_in REAL CHECK (standardization_lock_in BETWEEN 0 AND 1),
    trust_memory_effect REAL CHECK (trust_memory_effect BETWEEN 0 AND 1),
    transition_cost REAL CHECK (transition_cost BETWEEN 0 AND 1),
    option_closure_risk REAL CHECK (option_closure_risk BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (environment_id) REFERENCES complexity_environments(environment_id)
);

CREATE TABLE scenario_robustness (
    scenario_id TEXT PRIMARY KEY,
    environment_id TEXT NOT NULL,
    scenario_name TEXT NOT NULL,
    scenario_type TEXT NOT NULL,
    plausibility REAL CHECK (plausibility BETWEEN 0 AND 1),
    severity REAL CHECK (severity BETWEEN 0 AND 1),
    novelty REAL CHECK (novelty BETWEEN 0 AND 1),
    strategic_disruption REAL CHECK (strategic_disruption BETWEEN 0 AND 1),
    signal_visibility REAL CHECK (signal_visibility BETWEEN 0 AND 1),
    preparation_quality REAL CHECK (preparation_quality BETWEEN 0 AND 1),
    response_flexibility REAL CHECK (response_flexibility BETWEEN 0 AND 1),
    robustness_gap REAL CHECK (robustness_gap BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (environment_id) REFERENCES complexity_environments(environment_id)
);

CREATE TABLE adaptive_options (
    option_id TEXT PRIMARY KEY,
    environment_id TEXT NOT NULL,
    option_name TEXT NOT NULL,
    option_type TEXT NOT NULL,
    robustness REAL CHECK (robustness BETWEEN 0 AND 1),
    option_value REAL CHECK (option_value BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    downside_protection REAL CHECK (downside_protection BETWEEN 0 AND 1),
    resource_intensity REAL CHECK (resource_intensity BETWEEN 0 AND 1),
    time_to_learning REAL CHECK (time_to_learning BETWEEN 0 AND 1),
    strategic_coherence REAL CHECK (strategic_coherence BETWEEN 0 AND 1),
    legitimacy_requirement REAL CHECK (legitimacy_requirement BETWEEN 0 AND 1),
    evidence_readiness REAL CHECK (evidence_readiness BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (environment_id) REFERENCES complexity_environments(environment_id)
);

CREATE TABLE early_warning_indicators (
    indicator_id TEXT PRIMARY KEY,
    environment_id TEXT NOT NULL,
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
    FOREIGN KEY (environment_id) REFERENCES complexity_environments(environment_id)
);

CREATE TABLE learning_loops (
    learning_id TEXT PRIMARY KEY,
    environment_id TEXT NOT NULL,
    learning_loop_name TEXT NOT NULL,
    feedback_quality REAL CHECK (feedback_quality BETWEEN 0 AND 1),
    revision_trigger_clarity REAL CHECK (revision_trigger_clarity BETWEEN 0 AND 1),
    decision_memory_quality REAL CHECK (decision_memory_quality BETWEEN 0 AND 1),
    scenario_update_quality REAL CHECK (scenario_update_quality BETWEEN 0 AND 1),
    stakeholder_learning_visibility REAL CHECK (stakeholder_learning_visibility BETWEEN 0 AND 1),
    governance_response_capacity REAL CHECK (governance_response_capacity BETWEEN 0 AND 1),
    cycle_time REAL CHECK (cycle_time BETWEEN 0 AND 1),
    learning_risk REAL CHECK (learning_risk BETWEEN 0 AND 1),
    action_if_triggered TEXT,
    FOREIGN KEY (environment_id) REFERENCES complexity_environments(environment_id)
);

CREATE TABLE intervention_library (
    intervention_id TEXT PRIMARY KEY,
    intervention_name TEXT NOT NULL,
    target_complexity_risk TEXT NOT NULL,
    process_cost REAL CHECK (process_cost BETWEEN 0 AND 1),
    implementation_complexity REAL CHECK (implementation_complexity BETWEEN 0 AND 1),
    complexity_diagnosis_gain REAL CHECK (complexity_diagnosis_gain BETWEEN 0 AND 1),
    scenario_gain REAL CHECK (scenario_gain BETWEEN 0 AND 1),
    feedback_gain REAL CHECK (feedback_gain BETWEEN 0 AND 1),
    option_value_gain REAL CHECK (option_value_gain BETWEEN 0 AND 1),
    learning_gain REAL CHECK (learning_gain BETWEEN 0 AND 1),
    resilience_gain REAL CHECK (resilience_gain BETWEEN 0 AND 1),
    decision_memory_gain REAL CHECK (decision_memory_gain BETWEEN 0 AND 1),
    political_safety_need REAL CHECK (political_safety_need BETWEEN 0 AND 1)
);

CREATE TABLE decision_memory (
    decision_id TEXT PRIMARY KEY,
    environment_id TEXT NOT NULL,
    decision_date TEXT,
    system_classification TEXT,
    complexity_dimensions TEXT,
    uncertainty_drivers TEXT,
    feedback_loops_reviewed TEXT,
    adaptive_actors_reviewed TEXT,
    path_dependence_reviewed TEXT,
    scenarios_tested TEXT,
    selected_options TEXT,
    early_warning_indicators TEXT,
    revision_triggers TEXT,
    archived_learning TEXT,
    FOREIGN KEY (environment_id) REFERENCES complexity_environments(environment_id)
);

CREATE VIEW complexity_profile_scores AS
SELECT
    environment_id,
    environment_name,
    environment_type,
    domain,
    ROUND(
      0.13 * interdependence +
      0.13 * nonlinearity +
      0.14 * feedback_intensity +
      0.12 * adaptation_pressure +
      0.11 * path_dependence +
      0.10 * boundary_ambiguity +
      0.10 * emergence_potential +
      0.09 * deep_uncertainty +
      0.09 * scenario_need +
      0.09 * learning_capacity_need,
      4
    ) AS complexity_profile_score
FROM complexity_environments;

CREATE VIEW uncertainty_driver_scores AS
SELECT
    driver_id,
    environment_id,
    driver_name,
    driver_type,
    ROUND(
      0.16 * volatility +
      0.16 * ambiguity +
      0.16 * model_uncertainty +
      0.14 * probability_instability +
      0.14 * value_contestation +
      0.12 * actor_reflexivity -
      0.08 * monitoring_quality -
      0.08 * mitigation_quality,
      4
    ) AS uncertainty_intensity_score
FROM uncertainty_drivers;

CREATE VIEW feedback_loop_scores AS
SELECT
    loop_id,
    environment_id,
    loop_name,
    loop_type,
    ROUND(
      0.16 * loop_strength +
      0.16 * reinforcing_risk +
      0.14 * delay_risk +
      0.12 * stakeholder_burden_risk -
      0.12 * visibility -
      0.12 * balancing_capacity -
      0.10 * intervention_readiness,
      4
    ) AS feedback_risk_score
FROM feedback_loops;

CREATE VIEW adaptive_actor_scores AS
SELECT
    actor_id,
    environment_id,
    actor_group,
    ROUND(
      0.14 * adaptation_speed +
      0.14 * strategic_awareness +
      0.14 * workaround_likelihood +
      0.12 * imitation_likelihood +
      0.12 * resistance_likelihood +
      0.12 * gaming_likelihood +
      0.12 * influence_on_system -
      0.10 * learning_capacity +
      0.10 * monitoring_gap,
      4
    ) AS adaptation_risk_score
FROM adaptive_actors;

CREATE VIEW path_dependence_scores AS
SELECT
    path_id,
    environment_id,
    path_factor,
    path_type,
    ROUND(
      0.14 * legacy_strength +
      0.14 * sunk_cost_pressure +
      0.14 * coordination_lock_in +
      0.12 * standardization_lock_in +
      0.12 * trust_memory_effect +
      0.12 * transition_cost +
      0.12 * option_closure_risk -
      0.12 * reversibility,
      4
    ) AS lock_in_risk_score
FROM path_dependence;

CREATE VIEW scenario_risk_scores AS
SELECT
    scenario_id,
    environment_id,
    scenario_name,
    scenario_type,
    ROUND(
      0.14 * plausibility +
      0.16 * severity +
      0.12 * novelty +
      0.16 * strategic_disruption +
      0.14 * robustness_gap -
      0.10 * signal_visibility -
      0.10 * preparation_quality -
      0.08 * response_flexibility,
      4
    ) AS scenario_risk_score
FROM scenario_robustness;

CREATE VIEW adaptive_option_scores AS
SELECT
    option_id,
    environment_id,
    option_name,
    option_type,
    ROUND(
      0.14 * robustness +
      0.15 * option_value +
      0.12 * reversibility +
      0.14 * learning_value +
      0.12 * downside_protection -
      0.10 * resource_intensity -
      0.08 * time_to_learning +
      0.12 * strategic_coherence -
      0.08 * legitimacy_requirement +
      0.10 * evidence_readiness,
      4
    ) AS adaptive_option_value_score
FROM adaptive_options;

CREATE VIEW early_warning_indicator_scores AS
SELECT
    indicator_id,
    environment_id,
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
    environment_id,
    learning_loop_name,
    ROUND(
      0.14 * feedback_quality +
      0.14 * revision_trigger_clarity +
      0.14 * decision_memory_quality +
      0.14 * scenario_update_quality +
      0.12 * stakeholder_learning_visibility +
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
    target_complexity_risk,
    ROUND(
      0.13 * complexity_diagnosis_gain +
      0.14 * scenario_gain +
      0.14 * feedback_gain +
      0.14 * option_value_gain +
      0.14 * learning_gain +
      0.12 * resilience_gain +
      0.12 * decision_memory_gain -
      0.08 * process_cost -
      0.08 * implementation_complexity -
      0.08 * political_safety_need,
      4
    ) AS intervention_value_score
FROM intervention_library;
