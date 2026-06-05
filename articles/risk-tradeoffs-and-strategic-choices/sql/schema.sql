-- Advanced SQL schema for Risk, Tradeoffs, and Strategic Choices.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS strategic_tradeoff_scores;
DROP VIEW IF EXISTS risk_exposure_scores;
DROP VIEW IF EXISTS opportunity_cost_scores;
DROP VIEW IF EXISTS temporal_tradeoff_scores;
DROP VIEW IF EXISTS scenario_stress_test_scores;
DROP VIEW IF EXISTS lock_in_reversibility_scores;
DROP VIEW IF EXISTS resource_allocation_scores;
DROP VIEW IF EXISTS value_conflict_scores;
DROP VIEW IF EXISTS ethical_burden_scores;
DROP VIEW IF EXISTS decision_memory_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS ethical_burdens;
DROP TABLE IF EXISTS value_conflicts;
DROP TABLE IF EXISTS resource_allocation;
DROP TABLE IF EXISTS lock_in_reversibility;
DROP TABLE IF EXISTS scenario_stress_tests;
DROP TABLE IF EXISTS temporal_tradeoffs;
DROP TABLE IF EXISTS opportunity_costs;
DROP TABLE IF EXISTS risk_exposures;
DROP TABLE IF EXISTS strategic_options;

CREATE TABLE strategic_options (
    option_id TEXT PRIMARY KEY,
    option_name TEXT NOT NULL,
    option_type TEXT NOT NULL,
    short_term_return REAL CHECK (short_term_return BETWEEN 0 AND 1),
    resilience REAL CHECK (resilience BETWEEN 0 AND 1),
    flexibility REAL CHECK (flexibility BETWEEN 0 AND 1),
    stakeholder_legitimacy REAL CHECK (stakeholder_legitimacy BETWEEN 0 AND 1),
    opportunity_value REAL CHECK (opportunity_value BETWEEN 0 AND 1),
    exposure REAL CHECK (exposure BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    implementation_readiness REAL CHECK (implementation_readiness BETWEEN 0 AND 1),
    ethical_resilience REAL CHECK (ethical_resilience BETWEEN 0 AND 1),
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE risk_exposures (
    risk_id TEXT PRIMARY KEY,
    option_id TEXT NOT NULL,
    risk_type TEXT NOT NULL,
    financial_exposure REAL CHECK (financial_exposure BETWEEN 0 AND 1),
    implementation_exposure REAL CHECK (implementation_exposure BETWEEN 0 AND 1),
    reputation_exposure REAL CHECK (reputation_exposure BETWEEN 0 AND 1),
    regulatory_exposure REAL CHECK (regulatory_exposure BETWEEN 0 AND 1),
    ethical_exposure REAL CHECK (ethical_exposure BETWEEN 0 AND 1),
    systemic_exposure REAL CHECK (systemic_exposure BETWEEN 0 AND 1),
    strategic_exposure REAL CHECK (strategic_exposure BETWEEN 0 AND 1),
    absorptive_capacity REAL CHECK (absorptive_capacity BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (option_id) REFERENCES strategic_options(option_id)
);

CREATE TABLE opportunity_costs (
    cost_id TEXT PRIMARY KEY,
    option_id TEXT NOT NULL,
    forgone_alternative TEXT NOT NULL,
    capability_cost REAL CHECK (capability_cost BETWEEN 0 AND 1),
    learning_cost REAL CHECK (learning_cost BETWEEN 0 AND 1),
    flexibility_cost REAL CHECK (flexibility_cost BETWEEN 0 AND 1),
    preparedness_cost REAL CHECK (preparedness_cost BETWEEN 0 AND 1),
    legitimacy_cost REAL CHECK (legitimacy_cost BETWEEN 0 AND 1),
    innovation_cost REAL CHECK (innovation_cost BETWEEN 0 AND 1),
    delay_cost REAL CHECK (delay_cost BETWEEN 0 AND 1),
    visibility REAL CHECK (visibility BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (option_id) REFERENCES strategic_options(option_id)
);

CREATE TABLE temporal_tradeoffs (
    temporal_id TEXT PRIMARY KEY,
    option_id TEXT NOT NULL,
    immediate_value REAL CHECK (immediate_value BETWEEN 0 AND 1),
    short_term_value REAL CHECK (short_term_value BETWEEN 0 AND 1),
    medium_term_value REAL CHECK (medium_term_value BETWEEN 0 AND 1),
    long_term_value REAL CHECK (long_term_value BETWEEN 0 AND 1),
    intergenerational_value REAL CHECK (intergenerational_value BETWEEN 0 AND 1),
    near_term_cost REAL CHECK (near_term_cost BETWEEN 0 AND 1),
    deferred_cost REAL CHECK (deferred_cost BETWEEN 0 AND 1),
    benefit_cost_misalignment REAL CHECK (benefit_cost_misalignment BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (option_id) REFERENCES strategic_options(option_id)
);

CREATE TABLE scenario_stress_tests (
    scenario_id TEXT PRIMARY KEY,
    option_id TEXT NOT NULL,
    stable_growth REAL CHECK (stable_growth BETWEEN 0 AND 1),
    resource_constraint REAL CHECK (resource_constraint BETWEEN 0 AND 1),
    trust_crisis REAL CHECK (trust_crisis BETWEEN 0 AND 1),
    regulatory_shift REAL CHECK (regulatory_shift BETWEEN 0 AND 1),
    system_disruption REAL CHECK (system_disruption BETWEEN 0 AND 1),
    climate_or_environmental_stress REAL CHECK (climate_or_environmental_stress BETWEEN 0 AND 1),
    implementation_delay REAL CHECK (implementation_delay BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (option_id) REFERENCES strategic_options(option_id)
);

CREATE TABLE lock_in_reversibility (
    lock_id TEXT PRIMARY KEY,
    option_id TEXT NOT NULL,
    irreversibility REAL CHECK (irreversibility BETWEEN 0 AND 1),
    switching_cost REAL CHECK (switching_cost BETWEEN 0 AND 1),
    ecosystem_dependence REAL CHECK (ecosystem_dependence BETWEEN 0 AND 1),
    contractual_constraint REAL CHECK (contractual_constraint BETWEEN 0 AND 1),
    data_or_platform_dependence REAL CHECK (data_or_platform_dependence BETWEEN 0 AND 1),
    governance_constraint REAL CHECK (governance_constraint BETWEEN 0 AND 1),
    retained_flexibility REAL CHECK (retained_flexibility BETWEEN 0 AND 1),
    exit_path_quality REAL CHECK (exit_path_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (option_id) REFERENCES strategic_options(option_id)
);

CREATE TABLE resource_allocation (
    resource_id TEXT PRIMARY KEY,
    option_id TEXT NOT NULL,
    budget_alignment REAL CHECK (budget_alignment BETWEEN 0 AND 1),
    staffing_alignment REAL CHECK (staffing_alignment BETWEEN 0 AND 1),
    executive_attention REAL CHECK (executive_attention BETWEEN 0 AND 1),
    measurement_alignment REAL CHECK (measurement_alignment BETWEEN 0 AND 1),
    contingency_reserve REAL CHECK (contingency_reserve BETWEEN 0 AND 1),
    learning_budget REAL CHECK (learning_budget BETWEEN 0 AND 1),
    stakeholder_review_budget REAL CHECK (stakeholder_review_budget BETWEEN 0 AND 1),
    declared_priority_match REAL CHECK (declared_priority_match BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (option_id) REFERENCES strategic_options(option_id)
);

CREATE TABLE value_conflicts (
    conflict_id TEXT PRIMARY KEY,
    option_id TEXT NOT NULL,
    value_conflict TEXT NOT NULL,
    efficiency_pressure REAL CHECK (efficiency_pressure BETWEEN 0 AND 1),
    resilience_pressure REAL CHECK (resilience_pressure BETWEEN 0 AND 1),
    equity_pressure REAL CHECK (equity_pressure BETWEEN 0 AND 1),
    speed_pressure REAL CHECK (speed_pressure BETWEEN 0 AND 1),
    legitimacy_pressure REAL CHECK (legitimacy_pressure BETWEEN 0 AND 1),
    innovation_pressure REAL CHECK (innovation_pressure BETWEEN 0 AND 1),
    control_pressure REAL CHECK (control_pressure BETWEEN 0 AND 1),
    clarity_of_priority REAL CHECK (clarity_of_priority BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (option_id) REFERENCES strategic_options(option_id)
);

CREATE TABLE ethical_burdens (
    ethics_id TEXT PRIMARY KEY,
    option_id TEXT NOT NULL,
    ethical_issue TEXT NOT NULL,
    benefit_concentration REAL CHECK (benefit_concentration BETWEEN 0 AND 1),
    burden_concentration REAL CHECK (burden_concentration BETWEEN 0 AND 1),
    stakeholder_voice REAL CHECK (stakeholder_voice BETWEEN 0 AND 1),
    transparency REAL CHECK (transparency BETWEEN 0 AND 1),
    redress_quality REAL CHECK (redress_quality BETWEEN 0 AND 1),
    future_generation_burden REAL CHECK (future_generation_burden BETWEEN 0 AND 1),
    distributional_review_quality REAL CHECK (distributional_review_quality BETWEEN 0 AND 1),
    accountability_clarity REAL CHECK (accountability_clarity BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (option_id) REFERENCES strategic_options(option_id)
);

CREATE TABLE decision_memory (
    memory_id TEXT PRIMARY KEY,
    option_id TEXT NOT NULL,
    memory_practice TEXT NOT NULL,
    decision_question_record REAL CHECK (decision_question_record BETWEEN 0 AND 1),
    objective_conflict_record REAL CHECK (objective_conflict_record BETWEEN 0 AND 1),
    option_record REAL CHECK (option_record BETWEEN 0 AND 1),
    exposure_record REAL CHECK (exposure_record BETWEEN 0 AND 1),
    opportunity_cost_record REAL CHECK (opportunity_cost_record BETWEEN 0 AND 1),
    temporal_tradeoff_record REAL CHECK (temporal_tradeoff_record BETWEEN 0 AND 1),
    value_priority_record REAL CHECK (value_priority_record BETWEEN 0 AND 1),
    revision_trigger_record REAL CHECK (revision_trigger_record BETWEEN 0 AND 1),
    reuse_quality REAL CHECK (reuse_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (option_id) REFERENCES strategic_options(option_id)
);

CREATE VIEW strategic_tradeoff_scores AS
SELECT
    option_id,
    option_name,
    option_type,
    ROUND(
      0.18 * short_term_return +
      0.20 * resilience +
      0.16 * flexibility +
      0.14 * stakeholder_legitimacy +
      0.14 * opportunity_value -
      0.18 * exposure +
      0.08 * reversibility +
      0.06 * implementation_readiness +
      0.08 * ethical_resilience +
      0.08 * learning_value,
      4
    ) AS strategic_tradeoff_score,
    ROUND(
      0.26 * exposure +
      0.18 * (1 - resilience) +
      0.14 * (1 - flexibility) +
      0.12 * (1 - stakeholder_legitimacy) +
      0.12 * (1 - opportunity_value) +
      0.10 * (1 - reversibility) +
      0.08 * (1 - ethical_resilience),
      4
    ) AS fragility_warning
FROM strategic_options;

CREATE VIEW risk_exposure_scores AS
SELECT
    risk_id,
    option_id,
    risk_type,
    ROUND(
      0.13 * financial_exposure +
      0.13 * implementation_exposure +
      0.12 * reputation_exposure +
      0.11 * regulatory_exposure +
      0.13 * ethical_exposure +
      0.14 * systemic_exposure +
      0.14 * strategic_exposure +
      0.10 * (1 - absorptive_capacity),
      4
    ) AS gross_exposure
FROM risk_exposures;

CREATE VIEW opportunity_cost_scores AS
SELECT
    cost_id,
    option_id,
    forgone_alternative,
    ROUND(
      0.15 * capability_cost +
      0.15 * learning_cost +
      0.14 * flexibility_cost +
      0.15 * preparedness_cost +
      0.13 * legitimacy_cost +
      0.12 * innovation_cost +
      0.08 * delay_cost +
      0.08 * (1 - visibility),
      4
    ) AS opportunity_cost_score
FROM opportunity_costs;

CREATE VIEW temporal_tradeoff_scores AS
SELECT
    temporal_id,
    option_id,
    ROUND(
      0.26 * deferred_cost +
      0.22 * benefit_cost_misalignment +
      0.16 * near_term_cost +
      0.14 * (1 - long_term_value) +
      0.12 * (1 - intergenerational_value),
      4
    ) AS temporal_risk
FROM temporal_tradeoffs;

CREATE VIEW scenario_stress_test_scores AS
SELECT
    scenario_id,
    option_id,
    ROUND((stable_growth + resource_constraint + trust_crisis + regulatory_shift + system_disruption + climate_or_environmental_stress + implementation_delay) / 7.0, 4) AS mean_performance,
    MIN(stable_growth, resource_constraint, trust_crisis, regulatory_shift, system_disruption, climate_or_environmental_stress, implementation_delay) AS worst_case,
    MAX(stable_growth, resource_constraint, trust_crisis, regulatory_shift, system_disruption, climate_or_environmental_stress, implementation_delay) AS best_case
FROM scenario_stress_tests;

CREATE VIEW lock_in_reversibility_scores AS
SELECT
    lock_id,
    option_id,
    ROUND(
      0.16 * irreversibility +
      0.15 * switching_cost +
      0.14 * ecosystem_dependence +
      0.12 * contractual_constraint +
      0.13 * data_or_platform_dependence +
      0.10 * governance_constraint -
      0.12 * retained_flexibility -
      0.08 * exit_path_quality,
      4
    ) AS lock_in_score
FROM lock_in_reversibility;

CREATE VIEW resource_allocation_scores AS
SELECT
    resource_id,
    option_id,
    ROUND(
      0.14 * budget_alignment +
      0.14 * staffing_alignment +
      0.12 * executive_attention +
      0.12 * measurement_alignment +
      0.13 * contingency_reserve +
      0.13 * learning_budget +
      0.12 * stakeholder_review_budget +
      0.10 * declared_priority_match,
      4
    ) AS resource_coherence
FROM resource_allocation;

CREATE VIEW value_conflict_scores AS
SELECT
    conflict_id,
    option_id,
    value_conflict,
    ROUND(
      0.20 * (1 - clarity_of_priority) +
      0.10 * efficiency_pressure +
      0.10 * resilience_pressure +
      0.10 * equity_pressure +
      0.10 * speed_pressure +
      0.10 * legitimacy_pressure +
      0.10 * innovation_pressure +
      0.10 * control_pressure,
      4
    ) AS value_conflict_score
FROM value_conflicts;

CREATE VIEW ethical_burden_scores AS
SELECT
    ethics_id,
    option_id,
    ethical_issue,
    ROUND(
      0.15 * benefit_concentration +
      0.18 * burden_concentration +
      0.13 * (1 - stakeholder_voice) +
      0.11 * (1 - transparency) +
      0.11 * (1 - redress_quality) +
      0.16 * future_generation_burden +
      0.10 * (1 - distributional_review_quality) +
      0.06 * (1 - accountability_clarity),
      4
    ) AS ethical_burden_risk
FROM ethical_burdens;

CREATE VIEW decision_memory_scores AS
SELECT
    memory_id,
    option_id,
    memory_practice,
    ROUND(
      0.11 * decision_question_record +
      0.12 * objective_conflict_record +
      0.10 * option_record +
      0.12 * exposure_record +
      0.13 * opportunity_cost_record +
      0.12 * temporal_tradeoff_record +
      0.12 * value_priority_record +
      0.10 * revision_trigger_record +
      0.08 * reuse_quality,
      4
    ) AS decision_memory_score
FROM decision_memory;
