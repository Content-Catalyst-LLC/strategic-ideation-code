-- Advanced SQL schema for Scenario Planning and Futures Thinking.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS scenario_set_scores;
DROP VIEW IF EXISTS driver_uncertainty_scores;
DROP VIEW IF EXISTS strategy_stress_test_scores;
DROP VIEW IF EXISTS signal_monitoring_scores;
DROP VIEW IF EXISTS adaptive_pathway_scores;
DROP VIEW IF EXISTS futures_ethics_scores;
DROP VIEW IF EXISTS scenario_governance_scores;
DROP VIEW IF EXISTS scenario_learning_memory_scores;

DROP TABLE IF EXISTS scenario_learning_memory;
DROP TABLE IF EXISTS scenario_governance;
DROP TABLE IF EXISTS futures_ethics;
DROP TABLE IF EXISTS adaptive_pathways;
DROP TABLE IF EXISTS signal_monitoring;
DROP TABLE IF EXISTS strategy_stress_tests;
DROP TABLE IF EXISTS driver_uncertainties;
DROP TABLE IF EXISTS scenario_sets;

CREATE TABLE scenario_sets (
    scenario_set_id TEXT PRIMARY KEY,
    scenario_set_name TEXT NOT NULL,
    focal_question_clarity REAL CHECK (focal_question_clarity BETWEEN 0 AND 1),
    time_horizon_fit REAL CHECK (time_horizon_fit BETWEEN 0 AND 1),
    driver_analysis_quality REAL CHECK (driver_analysis_quality BETWEEN 0 AND 1),
    critical_uncertainty_quality REAL CHECK (critical_uncertainty_quality BETWEEN 0 AND 1),
    plausibility REAL CHECK (plausibility BETWEEN 0 AND 1),
    internal_coherence REAL CHECK (internal_coherence BETWEEN 0 AND 1),
    scenario_divergence REAL CHECK (scenario_divergence BETWEEN 0 AND 1),
    strategic_implication_quality REAL CHECK (strategic_implication_quality BETWEEN 0 AND 1),
    signal_monitoring_quality REAL CHECK (signal_monitoring_quality BETWEEN 0 AND 1),
    decision_linkage REAL CHECK (decision_linkage BETWEEN 0 AND 1),
    ethics_review REAL CHECK (ethics_review BETWEEN 0 AND 1),
    learning_memory REAL CHECK (learning_memory BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE driver_uncertainties (
    driver_id TEXT PRIMARY KEY,
    scenario_set_id TEXT NOT NULL,
    driver_name TEXT NOT NULL,
    driver_category TEXT NOT NULL,
    impact REAL CHECK (impact BETWEEN 0 AND 1),
    predictability REAL CHECK (predictability BETWEEN 0 AND 1),
    uncertainty REAL CHECK (uncertainty BETWEEN 0 AND 1),
    systemic_interdependence REAL CHECK (systemic_interdependence BETWEEN 0 AND 1),
    evidence_quality REAL CHECK (evidence_quality BETWEEN 0 AND 1),
    stakeholder_salience REAL CHECK (stakeholder_salience BETWEEN 0 AND 1),
    monitoring_feasibility REAL CHECK (monitoring_feasibility BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (scenario_set_id) REFERENCES scenario_sets(scenario_set_id)
);

CREATE TABLE strategy_stress_tests (
    test_id TEXT PRIMARY KEY,
    strategy_name TEXT NOT NULL,
    scenario_stable_growth REAL CHECK (scenario_stable_growth BETWEEN 0 AND 1),
    scenario_tech_disruption REAL CHECK (scenario_tech_disruption BETWEEN 0 AND 1),
    scenario_environmental_stress REAL CHECK (scenario_environmental_stress BETWEEN 0 AND 1),
    scenario_institutional_fragmentation REAL CHECK (scenario_institutional_fragmentation BETWEEN 0 AND 1),
    scenario_supply_disruption REAL CHECK (scenario_supply_disruption BETWEEN 0 AND 1),
    flexibility REAL CHECK (flexibility BETWEEN 0 AND 1),
    implementation_readiness REAL CHECK (implementation_readiness BETWEEN 0 AND 1),
    ethical_resilience REAL CHECK (ethical_resilience BETWEEN 0 AND 1),
    option_value REAL CHECK (option_value BETWEEN 0 AND 1),
    review_action TEXT
);

CREATE TABLE signal_monitoring (
    signal_id TEXT PRIMARY KEY,
    scenario_set_id TEXT NOT NULL,
    signal_name TEXT NOT NULL,
    signal_category TEXT NOT NULL,
    signal_strength REAL CHECK (signal_strength BETWEEN 0 AND 1),
    noise_risk REAL CHECK (noise_risk BETWEEN 0 AND 1),
    lead_time_value REAL CHECK (lead_time_value BETWEEN 0 AND 1),
    decision_relevance REAL CHECK (decision_relevance BETWEEN 0 AND 1),
    monitoring_quality REAL CHECK (monitoring_quality BETWEEN 0 AND 1),
    interpretation_quality REAL CHECK (interpretation_quality BETWEEN 0 AND 1),
    owner_clarity REAL CHECK (owner_clarity BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (scenario_set_id) REFERENCES scenario_sets(scenario_set_id)
);

CREATE TABLE adaptive_pathways (
    pathway_id TEXT PRIMARY KEY,
    scenario_set_id TEXT NOT NULL,
    pathway_name TEXT NOT NULL,
    trigger_clarity REAL CHECK (trigger_clarity BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    option_value REAL CHECK (option_value BETWEEN 0 AND 1),
    resource_flexibility REAL CHECK (resource_flexibility BETWEEN 0 AND 1),
    capability_readiness REAL CHECK (capability_readiness BETWEEN 0 AND 1),
    governance_clarity REAL CHECK (governance_clarity BETWEEN 0 AND 1),
    stakeholder_alignment REAL CHECK (stakeholder_alignment BETWEEN 0 AND 1),
    learning_memory REAL CHECK (learning_memory BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (scenario_set_id) REFERENCES scenario_sets(scenario_set_id)
);

CREATE TABLE futures_ethics (
    ethics_id TEXT PRIMARY KEY,
    scenario_set_id TEXT NOT NULL,
    ethical_issue TEXT NOT NULL,
    representation_quality REAL CHECK (representation_quality BETWEEN 0 AND 1),
    power_review_quality REAL CHECK (power_review_quality BETWEEN 0 AND 1),
    burden_shift_review REAL CHECK (burden_shift_review BETWEEN 0 AND 1),
    intergenerational_review REAL CHECK (intergenerational_review BETWEEN 0 AND 1),
    accessibility_quality REAL CHECK (accessibility_quality BETWEEN 0 AND 1),
    accountability_quality REAL CHECK (accountability_quality BETWEEN 0 AND 1),
    redress_path_quality REAL CHECK (redress_path_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (scenario_set_id) REFERENCES scenario_sets(scenario_set_id)
);

CREATE TABLE scenario_governance (
    governance_id TEXT PRIMARY KEY,
    scenario_set_id TEXT NOT NULL,
    governance_practice TEXT NOT NULL,
    decision_rights_clarity REAL CHECK (decision_rights_clarity BETWEEN 0 AND 1),
    evidence_standard_quality REAL CHECK (evidence_standard_quality BETWEEN 0 AND 1),
    scenario_review_cadence REAL CHECK (scenario_review_cadence BETWEEN 0 AND 1),
    signal_owner_clarity REAL CHECK (signal_owner_clarity BETWEEN 0 AND 1),
    trigger_condition_quality REAL CHECK (trigger_condition_quality BETWEEN 0 AND 1),
    documentation_quality REAL CHECK (documentation_quality BETWEEN 0 AND 1),
    accountability_quality REAL CHECK (accountability_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (scenario_set_id) REFERENCES scenario_sets(scenario_set_id)
);

CREATE TABLE scenario_learning_memory (
    memory_id TEXT PRIMARY KEY,
    scenario_set_id TEXT NOT NULL,
    memory_practice TEXT NOT NULL,
    focal_question_record REAL CHECK (focal_question_record BETWEEN 0 AND 1),
    driver_record_quality REAL CHECK (driver_record_quality BETWEEN 0 AND 1),
    uncertainty_record_quality REAL CHECK (uncertainty_record_quality BETWEEN 0 AND 1),
    scenario_logic_record REAL CHECK (scenario_logic_record BETWEEN 0 AND 1),
    implication_record_quality REAL CHECK (implication_record_quality BETWEEN 0 AND 1),
    signal_record_quality REAL CHECK (signal_record_quality BETWEEN 0 AND 1),
    decision_traceability REAL CHECK (decision_traceability BETWEEN 0 AND 1),
    remaining_uncertainty_quality REAL CHECK (remaining_uncertainty_quality BETWEEN 0 AND 1),
    reuse_quality REAL CHECK (reuse_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (scenario_set_id) REFERENCES scenario_sets(scenario_set_id)
);

CREATE VIEW scenario_set_scores AS
SELECT
    scenario_set_id,
    scenario_set_name,
    ROUND(
      0.10 * focal_question_clarity +
      0.08 * time_horizon_fit +
      0.11 * driver_analysis_quality +
      0.12 * critical_uncertainty_quality +
      0.09 * plausibility +
      0.10 * internal_coherence +
      0.11 * scenario_divergence +
      0.12 * strategic_implication_quality +
      0.08 * signal_monitoring_quality +
      0.06 * decision_linkage +
      0.07 * ethics_review +
      0.06 * learning_memory,
      4
    ) AS scenario_quality_score,
    ROUND(
      0.16 * (1 - decision_linkage) +
      0.14 * (1 - strategic_implication_quality) +
      0.12 * (1 - signal_monitoring_quality) +
      0.12 * (1 - learning_memory) +
      0.11 * (1 - focal_question_clarity) +
      0.11 * (1 - critical_uncertainty_quality) +
      0.10 * (1 - scenario_divergence) +
      0.08 * (1 - ethics_review) +
      0.06 * (1 - driver_analysis_quality),
      4
    ) AS workshop_theater_risk
FROM scenario_sets;

CREATE VIEW driver_uncertainty_scores AS
SELECT
    driver_id,
    scenario_set_id,
    driver_name,
    driver_category,
    ROUND(
      0.30 * impact +
      0.26 * uncertainty +
      0.16 * systemic_interdependence +
      0.12 * stakeholder_salience +
      0.08 * evidence_quality +
      0.08 * monitoring_feasibility,
      4
    ) AS critical_uncertainty_score,
    ROUND(
      0.24 * impact +
      0.22 * uncertainty +
      0.18 * systemic_interdependence +
      0.14 * stakeholder_salience +
      0.12 * monitoring_feasibility +
      0.10 * (1 - predictability),
      4
    ) AS watch_priority
FROM driver_uncertainties;

CREATE VIEW strategy_stress_test_scores AS
SELECT
    test_id,
    strategy_name,
    ROUND((scenario_stable_growth + scenario_tech_disruption + scenario_environmental_stress + scenario_institutional_fragmentation + scenario_supply_disruption) / 5.0, 4) AS mean_performance,
    MIN(scenario_stable_growth, scenario_tech_disruption, scenario_environmental_stress, scenario_institutional_fragmentation, scenario_supply_disruption) AS worst_case,
    MAX(scenario_stable_growth, scenario_tech_disruption, scenario_environmental_stress, scenario_institutional_fragmentation, scenario_supply_disruption) AS best_case
FROM strategy_stress_tests;

CREATE VIEW signal_monitoring_scores AS
SELECT
    signal_id,
    scenario_set_id,
    signal_name,
    signal_category,
    ROUND(
      0.20 * decision_relevance +
      0.18 * lead_time_value +
      0.16 * signal_strength +
      0.14 * interpretation_quality +
      0.12 * monitoring_quality +
      0.10 * owner_clarity -
      0.10 * noise_risk,
      4
    ) AS response_priority
FROM signal_monitoring;

CREATE VIEW adaptive_pathway_scores AS
SELECT
    pathway_id,
    scenario_set_id,
    pathway_name,
    ROUND(
      0.15 * trigger_clarity +
      0.14 * reversibility +
      0.16 * option_value +
      0.13 * resource_flexibility +
      0.13 * capability_readiness +
      0.12 * governance_clarity +
      0.10 * stakeholder_alignment +
      0.07 * learning_memory,
      4
    ) AS adaptive_pathway_score
FROM adaptive_pathways;

CREATE VIEW futures_ethics_scores AS
SELECT
    ethics_id,
    scenario_set_id,
    ethical_issue,
    ROUND(
      0.16 * representation_quality +
      0.15 * power_review_quality +
      0.16 * burden_shift_review +
      0.14 * intergenerational_review +
      0.13 * accessibility_quality +
      0.14 * accountability_quality +
      0.12 * redress_path_quality,
      4
    ) AS futures_ethics_score
FROM futures_ethics;

CREATE VIEW scenario_governance_scores AS
SELECT
    governance_id,
    scenario_set_id,
    governance_practice,
    ROUND(
      0.14 * decision_rights_clarity +
      0.14 * evidence_standard_quality +
      0.14 * scenario_review_cadence +
      0.13 * signal_owner_clarity +
      0.15 * trigger_condition_quality +
      0.15 * documentation_quality +
      0.15 * accountability_quality,
      4
    ) AS scenario_governance_score
FROM scenario_governance;

CREATE VIEW scenario_learning_memory_scores AS
SELECT
    memory_id,
    scenario_set_id,
    memory_practice,
    ROUND(
      0.11 * focal_question_record +
      0.11 * driver_record_quality +
      0.12 * uncertainty_record_quality +
      0.12 * scenario_logic_record +
      0.13 * implication_record_quality +
      0.11 * signal_record_quality +
      0.13 * decision_traceability +
      0.09 * remaining_uncertainty_quality +
      0.08 * reuse_quality,
      4
    ) AS scenario_learning_memory_score
FROM scenario_learning_memory;
