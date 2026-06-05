-- Advanced SQL schema for Strategic Foresight and Long-Term Thinking.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS foresight_profile_scores;
DROP VIEW IF EXISTS horizon_signal_scores;
DROP VIEW IF EXISTS driver_uncertainty_scores;
DROP VIEW IF EXISTS strategy_stress_test_scores;
DROP VIEW IF EXISTS path_dependence_scores;
DROP VIEW IF EXISTS adaptive_pathway_scores;
DROP VIEW IF EXISTS anticipatory_governance_scores;
DROP VIEW IF EXISTS futures_ethics_scores;
DROP VIEW IF EXISTS foresight_learning_memory_scores;

DROP TABLE IF EXISTS foresight_learning_memory;
DROP TABLE IF EXISTS futures_ethics;
DROP TABLE IF EXISTS anticipatory_governance;
DROP TABLE IF EXISTS adaptive_pathways;
DROP TABLE IF EXISTS path_dependence;
DROP TABLE IF EXISTS strategy_stress_tests;
DROP TABLE IF EXISTS driver_uncertainties;
DROP TABLE IF EXISTS horizon_signals;
DROP TABLE IF EXISTS foresight_profiles;

CREATE TABLE foresight_profiles (
    profile_id TEXT PRIMARY KEY,
    strategy_name TEXT NOT NULL,
    organization_type TEXT NOT NULL,
    domain TEXT NOT NULL,
    short_term_return REAL CHECK (short_term_return BETWEEN 0 AND 1),
    foresight_depth REAL CHECK (foresight_depth BETWEEN 0 AND 1),
    resilience REAL CHECK (resilience BETWEEN 0 AND 1),
    flexibility REAL CHECK (flexibility BETWEEN 0 AND 1),
    path_dependence_risk REAL CHECK (path_dependence_risk BETWEEN 0 AND 1),
    signal_capacity REAL CHECK (signal_capacity BETWEEN 0 AND 1),
    scenario_capacity REAL CHECK (scenario_capacity BETWEEN 0 AND 1),
    option_value REAL CHECK (option_value BETWEEN 0 AND 1),
    ethics_review REAL CHECK (ethics_review BETWEEN 0 AND 1),
    governance_capacity REAL CHECK (governance_capacity BETWEEN 0 AND 1),
    learning_memory REAL CHECK (learning_memory BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE horizon_signals (
    signal_id TEXT PRIMARY KEY,
    profile_id TEXT NOT NULL,
    signal_name TEXT NOT NULL,
    signal_category TEXT NOT NULL,
    signal_strength REAL CHECK (signal_strength BETWEEN 0 AND 1),
    noise_risk REAL CHECK (noise_risk BETWEEN 0 AND 1),
    lead_time_value REAL CHECK (lead_time_value BETWEEN 0 AND 1),
    strategic_relevance REAL CHECK (strategic_relevance BETWEEN 0 AND 1),
    interpretation_quality REAL CHECK (interpretation_quality BETWEEN 0 AND 1),
    monitoring_quality REAL CHECK (monitoring_quality BETWEEN 0 AND 1),
    owner_clarity REAL CHECK (owner_clarity BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (profile_id) REFERENCES foresight_profiles(profile_id)
);

CREATE TABLE driver_uncertainties (
    driver_id TEXT PRIMARY KEY,
    profile_id TEXT NOT NULL,
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
    FOREIGN KEY (profile_id) REFERENCES foresight_profiles(profile_id)
);

CREATE TABLE strategy_stress_tests (
    test_id TEXT PRIMARY KEY,
    strategy_name TEXT NOT NULL,
    future_stable_growth REAL CHECK (future_stable_growth BETWEEN 0 AND 1),
    future_tech_disruption REAL CHECK (future_tech_disruption BETWEEN 0 AND 1),
    future_environmental_stress REAL CHECK (future_environmental_stress BETWEEN 0 AND 1),
    future_institutional_fragmentation REAL CHECK (future_institutional_fragmentation BETWEEN 0 AND 1),
    future_public_trust_crisis REAL CHECK (future_public_trust_crisis BETWEEN 0 AND 1),
    flexibility REAL CHECK (flexibility BETWEEN 0 AND 1),
    implementation_readiness REAL CHECK (implementation_readiness BETWEEN 0 AND 1),
    ethical_resilience REAL CHECK (ethical_resilience BETWEEN 0 AND 1),
    option_value REAL CHECK (option_value BETWEEN 0 AND 1),
    review_action TEXT
);

CREATE TABLE path_dependence (
    path_id TEXT PRIMARY KEY,
    profile_id TEXT NOT NULL,
    path_dependency TEXT NOT NULL,
    dependency_type TEXT NOT NULL,
    lock_in_strength REAL CHECK (lock_in_strength BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    transition_cost REAL CHECK (transition_cost BETWEEN 0 AND 1),
    capability_gap REAL CHECK (capability_gap BETWEEN 0 AND 1),
    governance_constraint REAL CHECK (governance_constraint BETWEEN 0 AND 1),
    stakeholder_constraint REAL CHECK (stakeholder_constraint BETWEEN 0 AND 1),
    option_loss_risk REAL CHECK (option_loss_risk BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (profile_id) REFERENCES foresight_profiles(profile_id)
);

CREATE TABLE adaptive_pathways (
    pathway_id TEXT PRIMARY KEY,
    profile_id TEXT NOT NULL,
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
    FOREIGN KEY (profile_id) REFERENCES foresight_profiles(profile_id)
);

CREATE TABLE anticipatory_governance (
    governance_id TEXT PRIMARY KEY,
    profile_id TEXT NOT NULL,
    governance_practice TEXT NOT NULL,
    decision_rights_clarity REAL CHECK (decision_rights_clarity BETWEEN 0 AND 1),
    evidence_standard_quality REAL CHECK (evidence_standard_quality BETWEEN 0 AND 1),
    foresight_review_cadence REAL CHECK (foresight_review_cadence BETWEEN 0 AND 1),
    signal_owner_clarity REAL CHECK (signal_owner_clarity BETWEEN 0 AND 1),
    trigger_condition_quality REAL CHECK (trigger_condition_quality BETWEEN 0 AND 1),
    ethics_review_quality REAL CHECK (ethics_review_quality BETWEEN 0 AND 1),
    documentation_quality REAL CHECK (documentation_quality BETWEEN 0 AND 1),
    accountability_quality REAL CHECK (accountability_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (profile_id) REFERENCES foresight_profiles(profile_id)
);

CREATE TABLE futures_ethics (
    ethics_id TEXT PRIMARY KEY,
    profile_id TEXT NOT NULL,
    ethical_issue TEXT NOT NULL,
    representation_quality REAL CHECK (representation_quality BETWEEN 0 AND 1),
    power_review_quality REAL CHECK (power_review_quality BETWEEN 0 AND 1),
    burden_shift_review REAL CHECK (burden_shift_review BETWEEN 0 AND 1),
    intergenerational_review REAL CHECK (intergenerational_review BETWEEN 0 AND 1),
    accessibility_quality REAL CHECK (accessibility_quality BETWEEN 0 AND 1),
    accountability_quality REAL CHECK (accountability_quality BETWEEN 0 AND 1),
    redress_path_quality REAL CHECK (redress_path_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (profile_id) REFERENCES foresight_profiles(profile_id)
);

CREATE TABLE foresight_learning_memory (
    memory_id TEXT PRIMARY KEY,
    profile_id TEXT NOT NULL,
    memory_practice TEXT NOT NULL,
    focal_question_record REAL CHECK (focal_question_record BETWEEN 0 AND 1),
    signal_record_quality REAL CHECK (signal_record_quality BETWEEN 0 AND 1),
    driver_record_quality REAL CHECK (driver_record_quality BETWEEN 0 AND 1),
    uncertainty_record_quality REAL CHECK (uncertainty_record_quality BETWEEN 0 AND 1),
    scenario_record_quality REAL CHECK (scenario_record_quality BETWEEN 0 AND 1),
    decision_traceability REAL CHECK (decision_traceability BETWEEN 0 AND 1),
    pathway_record_quality REAL CHECK (pathway_record_quality BETWEEN 0 AND 1),
    remaining_uncertainty_quality REAL CHECK (remaining_uncertainty_quality BETWEEN 0 AND 1),
    reuse_quality REAL CHECK (reuse_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (profile_id) REFERENCES foresight_profiles(profile_id)
);

CREATE VIEW foresight_profile_scores AS
SELECT
    profile_id,
    strategy_name,
    ROUND(
      0.18 * foresight_depth +
      0.18 * resilience +
      0.16 * flexibility +
      0.14 * option_value +
      0.12 * scenario_capacity +
      0.10 * signal_capacity +
      0.08 * governance_capacity +
      0.08 * ethics_review -
      0.14 * path_dependence_risk,
      4
    ) AS future_viability_score,
    ROUND(
      short_term_return -
      ((foresight_depth + resilience + flexibility + option_value) / 4.0),
      4
    ) AS short_term_bias
FROM foresight_profiles;

CREATE VIEW horizon_signal_scores AS
SELECT
    signal_id,
    profile_id,
    signal_name,
    signal_category,
    ROUND(
      0.20 * strategic_relevance +
      0.18 * lead_time_value +
      0.16 * signal_strength +
      0.14 * interpretation_quality +
      0.12 * monitoring_quality +
      0.10 * owner_clarity -
      0.10 * noise_risk,
      4
    ) AS response_priority
FROM horizon_signals;

CREATE VIEW driver_uncertainty_scores AS
SELECT
    driver_id,
    profile_id,
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
    ) AS critical_uncertainty_score
FROM driver_uncertainties;

CREATE VIEW strategy_stress_test_scores AS
SELECT
    test_id,
    strategy_name,
    ROUND((future_stable_growth + future_tech_disruption + future_environmental_stress + future_institutional_fragmentation + future_public_trust_crisis) / 5.0, 4) AS mean_performance,
    MIN(future_stable_growth, future_tech_disruption, future_environmental_stress, future_institutional_fragmentation, future_public_trust_crisis) AS worst_case,
    MAX(future_stable_growth, future_tech_disruption, future_environmental_stress, future_institutional_fragmentation, future_public_trust_crisis) AS best_case
FROM strategy_stress_tests;

CREATE VIEW path_dependence_scores AS
SELECT
    path_id,
    profile_id,
    path_dependency,
    dependency_type,
    ROUND(
      0.20 * lock_in_strength +
      0.18 * (1 - reversibility) +
      0.16 * transition_cost +
      0.14 * capability_gap +
      0.12 * governance_constraint +
      0.10 * stakeholder_constraint +
      0.10 * option_loss_risk,
      4
    ) AS lock_in_risk
FROM path_dependence;

CREATE VIEW adaptive_pathway_scores AS
SELECT
    pathway_id,
    profile_id,
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

CREATE VIEW anticipatory_governance_scores AS
SELECT
    governance_id,
    profile_id,
    governance_practice,
    ROUND(
      0.13 * decision_rights_clarity +
      0.13 * evidence_standard_quality +
      0.13 * foresight_review_cadence +
      0.12 * signal_owner_clarity +
      0.14 * trigger_condition_quality +
      0.13 * ethics_review_quality +
      0.11 * documentation_quality +
      0.11 * accountability_quality,
      4
    ) AS anticipatory_governance_score
FROM anticipatory_governance;

CREATE VIEW futures_ethics_scores AS
SELECT
    ethics_id,
    profile_id,
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

CREATE VIEW foresight_learning_memory_scores AS
SELECT
    memory_id,
    profile_id,
    memory_practice,
    ROUND(
      0.11 * focal_question_record +
      0.12 * signal_record_quality +
      0.11 * driver_record_quality +
      0.11 * uncertainty_record_quality +
      0.12 * scenario_record_quality +
      0.13 * decision_traceability +
      0.11 * pathway_record_quality +
      0.10 * remaining_uncertainty_quality +
      0.09 * reuse_quality,
      4
    ) AS foresight_learning_memory_score
FROM foresight_learning_memory;
