-- Advanced SQL schema for systems thinking in ideation.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS systems_ideation_scores;
DROP VIEW IF EXISTS feedback_loop_scores;
DROP VIEW IF EXISTS leverage_point_scores;
DROP VIEW IF EXISTS boundary_quality_scores;
DROP VIEW IF EXISTS consequence_risk_scores;
DROP VIEW IF EXISTS intervention_portfolio_scores;
DROP VIEW IF EXISTS learning_loop_scores;
DROP VIEW IF EXISTS intervention_value_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS intervention_library;
DROP TABLE IF EXISTS learning_loops;
DROP TABLE IF EXISTS intervention_portfolio;
DROP TABLE IF EXISTS unintended_consequences;
DROP TABLE IF EXISTS boundary_reviews;
DROP TABLE IF EXISTS leverage_points;
DROP TABLE IF EXISTS feedback_loops;
DROP TABLE IF EXISTS systems_profiles;

CREATE TABLE systems_profiles (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_type TEXT NOT NULL,
    domain TEXT NOT NULL,
    feedback_awareness REAL CHECK (feedback_awareness BETWEEN 0 AND 1),
    leverage_sensitivity REAL CHECK (leverage_sensitivity BETWEEN 0 AND 1),
    root_cause_depth REAL CHECK (root_cause_depth BETWEEN 0 AND 1),
    stakeholder_visibility REAL CHECK (stakeholder_visibility BETWEEN 0 AND 1),
    boundary_quality REAL CHECK (boundary_quality BETWEEN 0 AND 1),
    stock_flow_awareness REAL CHECK (stock_flow_awareness BETWEEN 0 AND 1),
    delay_awareness REAL CHECK (delay_awareness BETWEEN 0 AND 1),
    adaptive_learning REAL CHECK (adaptive_learning BETWEEN 0 AND 1),
    unintended_consequence_risk REAL CHECK (unintended_consequence_risk BETWEEN 0 AND 1),
    local_optimization_risk REAL CHECK (local_optimization_risk BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE feedback_loops (
    loop_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    loop_name TEXT NOT NULL,
    loop_type TEXT NOT NULL,
    loop_strength REAL CHECK (loop_strength BETWEEN 0 AND 1),
    visibility REAL CHECK (visibility BETWEEN 0 AND 1),
    intervention_readiness REAL CHECK (intervention_readiness BETWEEN 0 AND 1),
    reinforcing_risk REAL CHECK (reinforcing_risk BETWEEN 0 AND 1),
    balancing_capacity REAL CHECK (balancing_capacity BETWEEN 0 AND 1),
    delay_risk REAL CHECK (delay_risk BETWEEN 0 AND 1),
    stakeholder_burden_risk REAL CHECK (stakeholder_burden_risk BETWEEN 0 AND 1),
    diagnostic_note TEXT,
    FOREIGN KEY (system_id) REFERENCES systems_profiles(system_id)
);

CREATE TABLE leverage_points (
    leverage_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    intervention_name TEXT NOT NULL,
    leverage_level TEXT NOT NULL,
    leverage_depth REAL CHECK (leverage_depth BETWEEN 0 AND 1),
    implementation_feasibility REAL CHECK (implementation_feasibility BETWEEN 0 AND 1),
    evidence_quality REAL CHECK (evidence_quality BETWEEN 0 AND 1),
    stakeholder_legitimacy REAL CHECK (stakeholder_legitimacy BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    system_sensitivity REAL CHECK (system_sensitivity BETWEEN 0 AND 1),
    risk_exposure REAL CHECK (risk_exposure BETWEEN 0 AND 1),
    time_to_effect REAL CHECK (time_to_effect BETWEEN 0 AND 1),
    expected_system_effect TEXT,
    FOREIGN KEY (system_id) REFERENCES systems_profiles(system_id)
);

CREATE TABLE boundary_reviews (
    boundary_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    boundary_name TEXT NOT NULL,
    boundary_scope TEXT NOT NULL,
    stakeholder_inclusion REAL CHECK (stakeholder_inclusion BETWEEN 0 AND 1),
    downstream_effect_visibility REAL CHECK (downstream_effect_visibility BETWEEN 0 AND 1),
    externality_visibility REAL CHECK (externality_visibility BETWEEN 0 AND 1),
    implementation_visibility REAL CHECK (implementation_visibility BETWEEN 0 AND 1),
    ecological_or_social_context REAL CHECK (ecological_or_social_context BETWEEN 0 AND 1),
    hidden_dependency_visibility REAL CHECK (hidden_dependency_visibility BETWEEN 0 AND 1),
    boundary_risk REAL CHECK (boundary_risk BETWEEN 0 AND 1),
    review_recommendation TEXT,
    FOREIGN KEY (system_id) REFERENCES systems_profiles(system_id)
);

CREATE TABLE unintended_consequences (
    consequence_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    intervention_name TEXT NOT NULL,
    consequence_type TEXT NOT NULL,
    likelihood REAL CHECK (likelihood BETWEEN 0 AND 1),
    severity REAL CHECK (severity BETWEEN 0 AND 1),
    detectability REAL CHECK (detectability BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    stakeholder_burden REAL CHECK (stakeholder_burden BETWEEN 0 AND 1),
    delay_length REAL CHECK (delay_length BETWEEN 0 AND 1),
    mitigation_quality REAL CHECK (mitigation_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES systems_profiles(system_id)
);

CREATE TABLE intervention_portfolio (
    portfolio_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    intervention_name TEXT NOT NULL,
    portfolio_role TEXT NOT NULL,
    leverage_level TEXT NOT NULL,
    confidence_level REAL CHECK (confidence_level BETWEEN 0 AND 1),
    evidence_readiness REAL CHECK (evidence_readiness BETWEEN 0 AND 1),
    strategic_option_value REAL CHECK (strategic_option_value BETWEEN 0 AND 1),
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    resource_intensity REAL CHECK (resource_intensity BETWEEN 0 AND 1),
    time_sensitivity REAL CHECK (time_sensitivity BETWEEN 0 AND 1),
    risk_exposure REAL CHECK (risk_exposure BETWEEN 0 AND 1),
    portfolio_action TEXT,
    FOREIGN KEY (system_id) REFERENCES systems_profiles(system_id)
);

CREATE TABLE learning_loops (
    learning_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    learning_loop_name TEXT NOT NULL,
    feedback_quality REAL CHECK (feedback_quality BETWEEN 0 AND 1),
    revision_trigger_clarity REAL CHECK (revision_trigger_clarity BETWEEN 0 AND 1),
    decision_memory_quality REAL CHECK (decision_memory_quality BETWEEN 0 AND 1),
    stakeholder_learning_visibility REAL CHECK (stakeholder_learning_visibility BETWEEN 0 AND 1),
    implementation_signal_quality REAL CHECK (implementation_signal_quality BETWEEN 0 AND 1),
    governance_response_capacity REAL CHECK (governance_response_capacity BETWEEN 0 AND 1),
    cycle_time REAL CHECK (cycle_time BETWEEN 0 AND 1),
    learning_risk REAL CHECK (learning_risk BETWEEN 0 AND 1),
    action_if_triggered TEXT,
    FOREIGN KEY (system_id) REFERENCES systems_profiles(system_id)
);

CREATE TABLE intervention_library (
    intervention_id TEXT PRIMARY KEY,
    intervention_name TEXT NOT NULL,
    target_systems_risk TEXT NOT NULL,
    process_cost REAL CHECK (process_cost BETWEEN 0 AND 1),
    implementation_complexity REAL CHECK (implementation_complexity BETWEEN 0 AND 1),
    structure_quality_gain REAL CHECK (structure_quality_gain BETWEEN 0 AND 1),
    feedback_gain REAL CHECK (feedback_gain BETWEEN 0 AND 1),
    leverage_gain REAL CHECK (leverage_gain BETWEEN 0 AND 1),
    stakeholder_gain REAL CHECK (stakeholder_gain BETWEEN 0 AND 1),
    boundary_gain REAL CHECK (boundary_gain BETWEEN 0 AND 1),
    learning_gain REAL CHECK (learning_gain BETWEEN 0 AND 1),
    unintended_consequence_reduction REAL CHECK (unintended_consequence_reduction BETWEEN 0 AND 1),
    political_safety_need REAL CHECK (political_safety_need BETWEEN 0 AND 1)
);

CREATE TABLE decision_memory (
    decision_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    decision_date TEXT,
    pattern_statement TEXT,
    system_boundary TEXT,
    structural_drivers TEXT,
    feedback_loops_reviewed TEXT,
    leverage_points_considered TEXT,
    second_order_effects TEXT,
    selected_intervention TEXT,
    evidence_pathway TEXT,
    revision_trigger TEXT,
    archived_learning TEXT,
    FOREIGN KEY (system_id) REFERENCES systems_profiles(system_id)
);

CREATE VIEW systems_ideation_scores AS
SELECT
    system_id,
    system_name,
    system_type,
    domain,
    ROUND(
      0.14 * feedback_awareness +
      0.14 * leverage_sensitivity +
      0.13 * root_cause_depth +
      0.12 * stakeholder_visibility +
      0.12 * boundary_quality +
      0.10 * stock_flow_awareness +
      0.10 * delay_awareness +
      0.13 * adaptive_learning -
      0.10 * unintended_consequence_risk -
      0.08 * local_optimization_risk,
      4
    ) AS systems_ideation_score
FROM systems_profiles;

CREATE VIEW feedback_loop_scores AS
SELECT
    loop_id,
    system_id,
    loop_name,
    loop_type,
    ROUND(
      0.16 * loop_strength +
      0.16 * visibility +
      0.18 * intervention_readiness +
      0.16 * balancing_capacity -
      0.12 * reinforcing_risk -
      0.10 * delay_risk -
      0.10 * stakeholder_burden_risk,
      4
    ) AS feedback_loop_quality_score
FROM feedback_loops;

CREATE VIEW leverage_point_scores AS
SELECT
    leverage_id,
    system_id,
    intervention_name,
    leverage_level,
    ROUND(
      0.22 * leverage_depth +
      0.12 * implementation_feasibility +
      0.12 * evidence_quality +
      0.12 * stakeholder_legitimacy +
      0.08 * reversibility +
      0.16 * system_sensitivity -
      0.10 * risk_exposure -
      0.08 * time_to_effect,
      4
    ) AS leverage_value_score
FROM leverage_points;

CREATE VIEW boundary_quality_scores AS
SELECT
    boundary_id,
    system_id,
    boundary_name,
    boundary_scope,
    ROUND(
      0.16 * stakeholder_inclusion +
      0.14 * downstream_effect_visibility +
      0.14 * externality_visibility +
      0.14 * implementation_visibility +
      0.14 * ecological_or_social_context +
      0.14 * hidden_dependency_visibility -
      0.12 * boundary_risk,
      4
    ) AS boundary_quality_score
FROM boundary_reviews;

CREATE VIEW consequence_risk_scores AS
SELECT
    consequence_id,
    system_id,
    intervention_name,
    consequence_type,
    ROUND(
      0.20 * likelihood +
      0.20 * severity +
      0.16 * stakeholder_burden +
      0.12 * delay_length -
      0.12 * detectability -
      0.10 * reversibility -
      0.10 * mitigation_quality,
      4
    ) AS consequence_risk_score
FROM unintended_consequences;

CREATE VIEW intervention_portfolio_scores AS
SELECT
    portfolio_id,
    system_id,
    intervention_name,
    portfolio_role,
    leverage_level,
    ROUND(
      0.14 * confidence_level +
      0.14 * evidence_readiness +
      0.18 * strategic_option_value +
      0.16 * learning_value -
      0.10 * resource_intensity +
      0.12 * time_sensitivity -
      0.10 * risk_exposure,
      4
    ) AS portfolio_value_score
FROM intervention_portfolio;

CREATE VIEW learning_loop_scores AS
SELECT
    learning_id,
    system_id,
    learning_loop_name,
    ROUND(
      0.16 * feedback_quality +
      0.16 * revision_trigger_clarity +
      0.16 * decision_memory_quality +
      0.14 * stakeholder_learning_visibility +
      0.14 * implementation_signal_quality +
      0.14 * governance_response_capacity +
      0.08 * cycle_time -
      0.10 * learning_risk,
      4
    ) AS learning_quality_score
FROM learning_loops;

CREATE VIEW intervention_value_scores AS
SELECT
    intervention_id,
    intervention_name,
    target_systems_risk,
    ROUND(
      0.14 * structure_quality_gain +
      0.14 * feedback_gain +
      0.16 * leverage_gain +
      0.14 * stakeholder_gain +
      0.14 * boundary_gain +
      0.14 * learning_gain +
      0.14 * unintended_consequence_reduction -
      0.10 * process_cost -
      0.08 * implementation_complexity -
      0.08 * political_safety_need,
      4
    ) AS intervention_value_score
FROM intervention_library;
