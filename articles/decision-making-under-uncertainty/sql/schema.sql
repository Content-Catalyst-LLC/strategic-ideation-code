-- Advanced SQL schema for Decision-Making Under Uncertainty.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS decision_option_scores;
DROP VIEW IF EXISTS uncertainty_classification_scores;
DROP VIEW IF EXISTS assumption_risk_scores;
DROP VIEW IF EXISTS scenario_stress_test_scores;
DROP VIEW IF EXISTS option_value_scores;
DROP VIEW IF EXISTS experiment_design_scores;
DROP VIEW IF EXISTS heuristic_bias_scores;
DROP VIEW IF EXISTS ethical_uncertainty_scores;
DROP VIEW IF EXISTS decision_governance_scores;
DROP VIEW IF EXISTS decision_learning_memory_scores;

DROP TABLE IF EXISTS decision_learning_memory;
DROP TABLE IF EXISTS decision_governance;
DROP TABLE IF EXISTS ethical_uncertainty;
DROP TABLE IF EXISTS heuristic_bias_reviews;
DROP TABLE IF EXISTS experiment_designs;
DROP TABLE IF EXISTS option_value_reviews;
DROP TABLE IF EXISTS scenario_stress_tests;
DROP TABLE IF EXISTS assumption_register;
DROP TABLE IF EXISTS uncertainty_classifications;
DROP TABLE IF EXISTS decision_options;

CREATE TABLE decision_options (
    option_id TEXT PRIMARY KEY,
    option_name TEXT NOT NULL,
    decision_frame TEXT NOT NULL,
    expected_return REAL CHECK (expected_return BETWEEN 0 AND 1),
    robustness REAL CHECK (robustness BETWEEN 0 AND 1),
    flexibility REAL CHECK (flexibility BETWEEN 0 AND 1),
    information_quality REAL CHECK (information_quality BETWEEN 0 AND 1),
    exposure REAL CHECK (exposure BETWEEN 0 AND 1),
    option_value REAL CHECK (option_value BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    implementation_readiness REAL CHECK (implementation_readiness BETWEEN 0 AND 1),
    ethical_resilience REAL CHECK (ethical_resilience BETWEEN 0 AND 1),
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE uncertainty_classifications (
    uncertainty_id TEXT PRIMARY KEY,
    option_id TEXT NOT NULL,
    uncertainty_type TEXT NOT NULL,
    probability_clarity REAL CHECK (probability_clarity BETWEEN 0 AND 1),
    outcome_clarity REAL CHECK (outcome_clarity BETWEEN 0 AND 1),
    causal_clarity REAL CHECK (causal_clarity BETWEEN 0 AND 1),
    interpretive_agreement REAL CHECK (interpretive_agreement BETWEEN 0 AND 1),
    system_complexity REAL CHECK (system_complexity BETWEEN 0 AND 1),
    stakes REAL CHECK (stakes BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    evidence_quality REAL CHECK (evidence_quality BETWEEN 0 AND 1),
    decision_logic TEXT,
    FOREIGN KEY (option_id) REFERENCES decision_options(option_id)
);

CREATE TABLE assumption_register (
    assumption_id TEXT PRIMARY KEY,
    option_id TEXT NOT NULL,
    assumption TEXT NOT NULL,
    uncertainty REAL CHECK (uncertainty BETWEEN 0 AND 1),
    consequence REAL CHECK (consequence BETWEEN 0 AND 1),
    evidence_quality REAL CHECK (evidence_quality BETWEEN 0 AND 1),
    decay_risk REAL CHECK (decay_risk BETWEEN 0 AND 1),
    monitorability REAL CHECK (monitorability BETWEEN 0 AND 1),
    owner_clarity REAL CHECK (owner_clarity BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (option_id) REFERENCES decision_options(option_id)
);

CREATE TABLE scenario_stress_tests (
    test_id TEXT PRIMARY KEY,
    option_id TEXT NOT NULL,
    scenario_stable_growth REAL CHECK (scenario_stable_growth BETWEEN 0 AND 1),
    scenario_tech_disruption REAL CHECK (scenario_tech_disruption BETWEEN 0 AND 1),
    scenario_environmental_stress REAL CHECK (scenario_environmental_stress BETWEEN 0 AND 1),
    scenario_regulatory_shift REAL CHECK (scenario_regulatory_shift BETWEEN 0 AND 1),
    scenario_trust_crisis REAL CHECK (scenario_trust_crisis BETWEEN 0 AND 1),
    scenario_resource_constraint REAL CHECK (scenario_resource_constraint BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (option_id) REFERENCES decision_options(option_id)
);

CREATE TABLE option_value_reviews (
    review_id TEXT PRIMARY KEY,
    option_id TEXT NOT NULL,
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    future_flexibility REAL CHECK (future_flexibility BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    staged_commitment_quality REAL CHECK (staged_commitment_quality BETWEEN 0 AND 1),
    modularity REAL CHECK (modularity BETWEEN 0 AND 1),
    exit_path_quality REAL CHECK (exit_path_quality BETWEEN 0 AND 1),
    lock_in_cost REAL CHECK (lock_in_cost BETWEEN 0 AND 1),
    monitoring_quality REAL CHECK (monitoring_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (option_id) REFERENCES decision_options(option_id)
);

CREATE TABLE experiment_designs (
    experiment_id TEXT PRIMARY KEY,
    option_id TEXT NOT NULL,
    experiment_name TEXT NOT NULL,
    learning_question_quality REAL CHECK (learning_question_quality BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    exposure_control REAL CHECK (exposure_control BETWEEN 0 AND 1),
    evidence_quality REAL CHECK (evidence_quality BETWEEN 0 AND 1),
    stakeholder_feedback_quality REAL CHECK (stakeholder_feedback_quality BETWEEN 0 AND 1),
    scaling_trigger_clarity REAL CHECK (scaling_trigger_clarity BETWEEN 0 AND 1),
    decision_relevance REAL CHECK (decision_relevance BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (option_id) REFERENCES decision_options(option_id)
);

CREATE TABLE heuristic_bias_reviews (
    bias_id TEXT PRIMARY KEY,
    option_id TEXT NOT NULL,
    bias_or_heuristic TEXT NOT NULL,
    exposure_level REAL CHECK (exposure_level BETWEEN 0 AND 1),
    decision_influence REAL CHECK (decision_influence BETWEEN 0 AND 1),
    detectability REAL CHECK (detectability BETWEEN 0 AND 1),
    mitigation_quality REAL CHECK (mitigation_quality BETWEEN 0 AND 1),
    challenge_process_quality REAL CHECK (challenge_process_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (option_id) REFERENCES decision_options(option_id)
);

CREATE TABLE ethical_uncertainty (
    ethics_id TEXT PRIMARY KEY,
    option_id TEXT NOT NULL,
    ethical_issue TEXT NOT NULL,
    transparency REAL CHECK (transparency BETWEEN 0 AND 1),
    burden_shift_review REAL CHECK (burden_shift_review BETWEEN 0 AND 1),
    stakeholder_representation REAL CHECK (stakeholder_representation BETWEEN 0 AND 1),
    accountability REAL CHECK (accountability BETWEEN 0 AND 1),
    revisability REAL CHECK (revisability BETWEEN 0 AND 1),
    precaution_quality REAL CHECK (precaution_quality BETWEEN 0 AND 1),
    redress_path_quality REAL CHECK (redress_path_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (option_id) REFERENCES decision_options(option_id)
);

CREATE TABLE decision_governance (
    governance_id TEXT PRIMARY KEY,
    option_id TEXT NOT NULL,
    governance_practice TEXT NOT NULL,
    decision_rights_clarity REAL CHECK (decision_rights_clarity BETWEEN 0 AND 1),
    evidence_standard_quality REAL CHECK (evidence_standard_quality BETWEEN 0 AND 1),
    uncertainty_disclosure REAL CHECK (uncertainty_disclosure BETWEEN 0 AND 1),
    review_cadence REAL CHECK (review_cadence BETWEEN 0 AND 1),
    trigger_condition_quality REAL CHECK (trigger_condition_quality BETWEEN 0 AND 1),
    dissent_protection REAL CHECK (dissent_protection BETWEEN 0 AND 1),
    documentation_quality REAL CHECK (documentation_quality BETWEEN 0 AND 1),
    accountability_quality REAL CHECK (accountability_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (option_id) REFERENCES decision_options(option_id)
);

CREATE TABLE decision_learning_memory (
    memory_id TEXT PRIMARY KEY,
    option_id TEXT NOT NULL,
    memory_practice TEXT NOT NULL,
    decision_question_record REAL CHECK (decision_question_record BETWEEN 0 AND 1),
    frame_record_quality REAL CHECK (frame_record_quality BETWEEN 0 AND 1),
    option_record_quality REAL CHECK (option_record_quality BETWEEN 0 AND 1),
    assumption_record_quality REAL CHECK (assumption_record_quality BETWEEN 0 AND 1),
    uncertainty_record_quality REAL CHECK (uncertainty_record_quality BETWEEN 0 AND 1),
    evidence_record_quality REAL CHECK (evidence_record_quality BETWEEN 0 AND 1),
    trigger_record_quality REAL CHECK (trigger_record_quality BETWEEN 0 AND 1),
    revision_record_quality REAL CHECK (revision_record_quality BETWEEN 0 AND 1),
    reuse_quality REAL CHECK (reuse_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (option_id) REFERENCES decision_options(option_id)
);

CREATE VIEW decision_option_scores AS
SELECT
    option_id,
    option_name,
    decision_frame,
    ROUND(
      0.14 * expected_return +
      0.18 * robustness +
      0.16 * flexibility +
      0.12 * information_quality -
      0.16 * exposure +
      0.14 * option_value +
      0.10 * reversibility +
      0.08 * implementation_readiness +
      0.10 * ethical_resilience +
      0.10 * learning_value,
      4
    ) AS decision_profile_score,
    ROUND(
      0.24 * exposure +
      0.18 * (1 - robustness) +
      0.14 * (1 - flexibility) +
      0.13 * (1 - option_value) +
      0.12 * (1 - reversibility) +
      0.10 * (1 - ethical_resilience) +
      0.09 * (1 - information_quality),
      4
    ) AS fragility_risk
FROM decision_options;

CREATE VIEW uncertainty_classification_scores AS
SELECT
    uncertainty_id,
    option_id,
    uncertainty_type,
    ROUND(
      0.15 * (1 - probability_clarity) +
      0.13 * (1 - outcome_clarity) +
      0.13 * (1 - causal_clarity) +
      0.12 * (1 - interpretive_agreement) +
      0.17 * system_complexity +
      0.14 * stakes +
      0.08 * (1 - reversibility) +
      0.08 * (1 - evidence_quality),
      4
    ) AS classification_difficulty
FROM uncertainty_classifications;

CREATE VIEW assumption_risk_scores AS
SELECT
    assumption_id,
    option_id,
    assumption,
    ROUND(
      0.25 * uncertainty +
      0.25 * consequence +
      0.15 * (1 - evidence_quality) +
      0.14 * decay_risk +
      0.11 * (1 - monitorability) +
      0.10 * (1 - owner_clarity),
      4
    ) AS assumption_risk
FROM assumption_register;

CREATE VIEW scenario_stress_test_scores AS
SELECT
    test_id,
    option_id,
    ROUND((scenario_stable_growth + scenario_tech_disruption + scenario_environmental_stress + scenario_regulatory_shift + scenario_trust_crisis + scenario_resource_constraint) / 6.0, 4) AS mean_performance,
    MIN(scenario_stable_growth, scenario_tech_disruption, scenario_environmental_stress, scenario_regulatory_shift, scenario_trust_crisis, scenario_resource_constraint) AS worst_case,
    MAX(scenario_stable_growth, scenario_tech_disruption, scenario_environmental_stress, scenario_regulatory_shift, scenario_trust_crisis, scenario_resource_constraint) AS best_case
FROM scenario_stress_tests;

CREATE VIEW option_value_scores AS
SELECT
    review_id,
    option_id,
    ROUND(
      0.18 * learning_value +
      0.18 * future_flexibility +
      0.15 * reversibility +
      0.13 * staged_commitment_quality +
      0.12 * modularity +
      0.11 * exit_path_quality -
      0.15 * lock_in_cost +
      0.08 * monitoring_quality,
      4
    ) AS option_value_score
FROM option_value_reviews;

CREATE VIEW experiment_design_scores AS
SELECT
    experiment_id,
    option_id,
    experiment_name,
    ROUND(
      0.16 * learning_question_quality +
      0.14 * reversibility +
      0.14 * exposure_control +
      0.15 * evidence_quality +
      0.12 * stakeholder_feedback_quality +
      0.14 * scaling_trigger_clarity +
      0.15 * decision_relevance,
      4
    ) AS experiment_quality
FROM experiment_designs;

CREATE VIEW heuristic_bias_scores AS
SELECT
    bias_id,
    option_id,
    bias_or_heuristic,
    ROUND(
      0.26 * exposure_level +
      0.26 * decision_influence +
      0.16 * (1 - detectability) +
      0.16 * (1 - mitigation_quality) +
      0.16 * (1 - challenge_process_quality),
      4
    ) AS bias_risk
FROM heuristic_bias_reviews;

CREATE VIEW ethical_uncertainty_scores AS
SELECT
    ethics_id,
    option_id,
    ethical_issue,
    ROUND(
      0.14 * transparency +
      0.15 * burden_shift_review +
      0.15 * stakeholder_representation +
      0.14 * accountability +
      0.14 * revisability +
      0.14 * precaution_quality +
      0.14 * redress_path_quality,
      4
    ) AS ethical_uncertainty_score
FROM ethical_uncertainty;

CREATE VIEW decision_governance_scores AS
SELECT
    governance_id,
    option_id,
    governance_practice,
    ROUND(
      0.12 * decision_rights_clarity +
      0.12 * evidence_standard_quality +
      0.13 * uncertainty_disclosure +
      0.12 * review_cadence +
      0.14 * trigger_condition_quality +
      0.13 * dissent_protection +
      0.12 * documentation_quality +
      0.12 * accountability_quality,
      4
    ) AS decision_governance_score
FROM decision_governance;

CREATE VIEW decision_learning_memory_scores AS
SELECT
    memory_id,
    option_id,
    memory_practice,
    ROUND(
      0.11 * decision_question_record +
      0.11 * frame_record_quality +
      0.11 * option_record_quality +
      0.12 * assumption_record_quality +
      0.12 * uncertainty_record_quality +
      0.11 * evidence_record_quality +
      0.12 * trigger_record_quality +
      0.10 * revision_record_quality +
      0.10 * reuse_quality,
      4
    ) AS decision_learning_memory_score
FROM decision_learning_memory;
