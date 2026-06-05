-- Advanced SQL schema for Prototyping and Rapid Experimentation.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS experimentation_profile_scores;
DROP VIEW IF EXISTS assumption_priority_scores;
DROP VIEW IF EXISTS prototype_fit_scores;
DROP VIEW IF EXISTS experiment_quality_scores;
DROP VIEW IF EXISTS evidence_quality_scores;
DROP VIEW IF EXISTS user_validation_scores;
DROP VIEW IF EXISTS iteration_learning_scores;
DROP VIEW IF EXISTS systems_impact_scores;
DROP VIEW IF EXISTS ethical_governance_scores;
DROP VIEW IF EXISTS decision_linkage_scores;

DROP TABLE IF EXISTS decision_linkage;
DROP TABLE IF EXISTS ethical_governance;
DROP TABLE IF EXISTS systems_impact;
DROP TABLE IF EXISTS iterations;
DROP TABLE IF EXISTS user_validation;
DROP TABLE IF EXISTS evidence;
DROP TABLE IF EXISTS experiments;
DROP TABLE IF EXISTS prototypes;
DROP TABLE IF EXISTS assumptions;
DROP TABLE IF EXISTS experimentation_systems;

CREATE TABLE experimentation_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    organization_type TEXT NOT NULL,
    domain TEXT NOT NULL,
    speed REAL CHECK (speed BETWEEN 0 AND 1),
    cost_efficiency REAL CHECK (cost_efficiency BETWEEN 0 AND 1),
    insight_depth REAL CHECK (insight_depth BETWEEN 0 AND 1),
    user_validation REAL CHECK (user_validation BETWEEN 0 AND 1),
    assumption_criticality REAL CHECK (assumption_criticality BETWEEN 0 AND 1),
    evidence_quality REAL CHECK (evidence_quality BETWEEN 0 AND 1),
    systems_awareness REAL CHECK (systems_awareness BETWEEN 0 AND 1),
    ethical_review REAL CHECK (ethical_review BETWEEN 0 AND 1),
    decision_linkage REAL CHECK (decision_linkage BETWEEN 0 AND 1),
    learning_memory REAL CHECK (learning_memory BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE assumptions (
    assumption_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    assumption_statement TEXT NOT NULL,
    assumption_type TEXT NOT NULL,
    uncertainty REAL CHECK (uncertainty BETWEEN 0 AND 1),
    strategic_significance REAL CHECK (strategic_significance BETWEEN 0 AND 1),
    reversibility_risk REAL CHECK (reversibility_risk BETWEEN 0 AND 1),
    cost_of_error REAL CHECK (cost_of_error BETWEEN 0 AND 1),
    evidence_gap REAL CHECK (evidence_gap BETWEEN 0 AND 1),
    stakeholder_sensitivity REAL CHECK (stakeholder_sensitivity BETWEEN 0 AND 1),
    testing_feasibility REAL CHECK (testing_feasibility BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES experimentation_systems(system_id)
);

CREATE TABLE prototypes (
    prototype_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    prototype_name TEXT NOT NULL,
    prototype_type TEXT NOT NULL,
    learning_target TEXT NOT NULL,
    fidelity REAL CHECK (fidelity BETWEEN 0 AND 1),
    learning_fit REAL CHECK (learning_fit BETWEEN 0 AND 1),
    cost_to_build REAL CHECK (cost_to_build BETWEEN 0 AND 1),
    speed_to_test REAL CHECK (speed_to_test BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    user_context_realism REAL CHECK (user_context_realism BETWEEN 0 AND 1),
    operational_realism REAL CHECK (operational_realism BETWEEN 0 AND 1),
    systems_visibility REAL CHECK (systems_visibility BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES experimentation_systems(system_id)
);

CREATE TABLE experiments (
    experiment_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    prototype_id TEXT NOT NULL,
    hypothesis TEXT NOT NULL,
    learning_target_clarity REAL CHECK (learning_target_clarity BETWEEN 0 AND 1),
    test_condition_quality REAL CHECK (test_condition_quality BETWEEN 0 AND 1),
    evidence_standard_quality REAL CHECK (evidence_standard_quality BETWEEN 0 AND 1),
    participant_fit REAL CHECK (participant_fit BETWEEN 0 AND 1),
    risk_boundary_quality REAL CHECK (risk_boundary_quality BETWEEN 0 AND 1),
    interpretation_limit_clarity REAL CHECK (interpretation_limit_clarity BETWEEN 0 AND 1),
    decision_rule_quality REAL CHECK (decision_rule_quality BETWEEN 0 AND 1),
    repeatability REAL CHECK (repeatability BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES experimentation_systems(system_id),
    FOREIGN KEY (prototype_id) REFERENCES prototypes(prototype_id)
);

CREATE TABLE evidence (
    evidence_id TEXT PRIMARY KEY,
    experiment_id TEXT NOT NULL,
    evidence_type TEXT NOT NULL,
    relevance REAL CHECK (relevance BETWEEN 0 AND 1),
    validity REAL CHECK (validity BETWEEN 0 AND 1),
    contextual_realism REAL CHECK (contextual_realism BETWEEN 0 AND 1),
    behavioral_richness REAL CHECK (behavioral_richness BETWEEN 0 AND 1),
    interpretability REAL CHECK (interpretability BETWEEN 0 AND 1),
    decision_usefulness REAL CHECK (decision_usefulness BETWEEN 0 AND 1),
    limitation_severity REAL CHECK (limitation_severity BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (experiment_id) REFERENCES experiments(experiment_id)
);

CREATE TABLE user_validation (
    validation_id TEXT PRIMARY KEY,
    experiment_id TEXT NOT NULL,
    user_group TEXT NOT NULL,
    observed_behavior TEXT NOT NULL,
    stated_feedback TEXT NOT NULL,
    behavioral_signal_strength REAL CHECK (behavioral_signal_strength BETWEEN 0 AND 1),
    preference_behavior_alignment REAL CHECK (preference_behavior_alignment BETWEEN 0 AND 1),
    nonuser_inclusion REAL CHECK (nonuser_inclusion BETWEEN 0 AND 1),
    accessibility_signal REAL CHECK (accessibility_signal BETWEEN 0 AND 1),
    trust_signal REAL CHECK (trust_signal BETWEEN 0 AND 1),
    workaround_signal REAL CHECK (workaround_signal BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (experiment_id) REFERENCES experiments(experiment_id)
);

CREATE TABLE iterations (
    iteration_id TEXT PRIMARY KEY,
    experiment_id TEXT NOT NULL,
    iteration_number INTEGER NOT NULL,
    learning_quality REAL CHECK (learning_quality BETWEEN 0 AND 1),
    change_traceability REAL CHECK (change_traceability BETWEEN 0 AND 1),
    assumption_revision REAL CHECK (assumption_revision BETWEEN 0 AND 1),
    prototype_revision_quality REAL CHECK (prototype_revision_quality BETWEEN 0 AND 1),
    remaining_uncertainty REAL CHECK (remaining_uncertainty BETWEEN 0 AND 1),
    decision_memory_quality REAL CHECK (decision_memory_quality BETWEEN 0 AND 1),
    next_test_clarity REAL CHECK (next_test_clarity BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (experiment_id) REFERENCES experiments(experiment_id)
);

CREATE TABLE systems_impact (
    impact_id TEXT PRIMARY KEY,
    experiment_id TEXT NOT NULL,
    system_issue TEXT NOT NULL,
    feedback_risk REAL CHECK (feedback_risk BETWEEN 0 AND 1),
    delay_risk REAL CHECK (delay_risk BETWEEN 0 AND 1),
    burden_shift_risk REAL CHECK (burden_shift_risk BETWEEN 0 AND 1),
    capacity_risk REAL CHECK (capacity_risk BETWEEN 0 AND 1),
    incentive_risk REAL CHECK (incentive_risk BETWEEN 0 AND 1),
    scale_uncertainty REAL CHECK (scale_uncertainty BETWEEN 0 AND 1),
    monitoring_quality REAL CHECK (monitoring_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (experiment_id) REFERENCES experiments(experiment_id)
);

CREATE TABLE ethical_governance (
    ethics_id TEXT PRIMARY KEY,
    experiment_id TEXT NOT NULL,
    ethical_issue TEXT NOT NULL,
    participant_risk_review REAL CHECK (participant_risk_review BETWEEN 0 AND 1),
    consent_quality REAL CHECK (consent_quality BETWEEN 0 AND 1),
    privacy_protection REAL CHECK (privacy_protection BETWEEN 0 AND 1),
    accessibility_review REAL CHECK (accessibility_review BETWEEN 0 AND 1),
    burden_review REAL CHECK (burden_review BETWEEN 0 AND 1),
    representation_quality REAL CHECK (representation_quality BETWEEN 0 AND 1),
    redress_path REAL CHECK (redress_path BETWEEN 0 AND 1),
    governance_traceability REAL CHECK (governance_traceability BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (experiment_id) REFERENCES experiments(experiment_id)
);

CREATE TABLE decision_linkage (
    decision_id TEXT PRIMARY KEY,
    experiment_id TEXT NOT NULL,
    decision_type TEXT NOT NULL,
    evidence_to_decision_clarity REAL CHECK (evidence_to_decision_clarity BETWEEN 0 AND 1),
    authority_connection REAL CHECK (authority_connection BETWEEN 0 AND 1),
    resource_connection REAL CHECK (resource_connection BETWEEN 0 AND 1),
    stop_rule_quality REAL CHECK (stop_rule_quality BETWEEN 0 AND 1),
    scale_rule_quality REAL CHECK (scale_rule_quality BETWEEN 0 AND 1),
    revision_trigger_quality REAL CHECK (revision_trigger_quality BETWEEN 0 AND 1),
    learning_record_quality REAL CHECK (learning_record_quality BETWEEN 0 AND 1),
    implementation_path_quality REAL CHECK (implementation_path_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (experiment_id) REFERENCES experiments(experiment_id)
);

CREATE VIEW experimentation_profile_scores AS
SELECT
    system_id,
    system_name,
    ROUND(
      0.10 * speed +
      0.09 * cost_efficiency +
      0.15 * insight_depth +
      0.12 * user_validation +
      0.12 * assumption_criticality +
      0.14 * evidence_quality +
      0.10 * systems_awareness +
      0.08 * ethical_review +
      0.10 * decision_linkage +
      0.10 * learning_memory,
      4
    ) AS experimentation_profile_score,
    ROUND(
      0.14 * speed +
      0.16 * (1 - insight_depth) +
      0.15 * (1 - evidence_quality) +
      0.13 * (1 - systems_awareness) +
      0.13 * (1 - ethical_review) +
      0.13 * (1 - decision_linkage) +
      0.09 * (1 - assumption_criticality) +
      0.07 * (1 - learning_memory),
      4
    ) AS superficial_testing_risk
FROM experimentation_systems;

CREATE VIEW assumption_priority_scores AS
SELECT
    assumption_id,
    system_id,
    assumption_statement,
    assumption_type,
    ROUND(
      0.16 * uncertainty +
      0.17 * strategic_significance +
      0.13 * reversibility_risk +
      0.14 * cost_of_error +
      0.13 * evidence_gap +
      0.14 * stakeholder_sensitivity +
      0.08 * testing_feasibility,
      4
    ) AS assumption_priority_score
FROM assumptions;

CREATE VIEW prototype_fit_scores AS
SELECT
    prototype_id,
    system_id,
    prototype_name,
    prototype_type,
    learning_target,
    ROUND(
      0.20 * learning_fit -
      0.10 * cost_to_build +
      0.12 * speed_to_test +
      0.13 * reversibility +
      0.14 * user_context_realism +
      0.13 * operational_realism +
      0.12 * systems_visibility +
      0.06 * (1 - ABS(fidelity - learning_fit)),
      4
    ) AS prototype_fit_score
FROM prototypes;

CREATE VIEW experiment_quality_scores AS
SELECT
    experiment_id,
    system_id,
    prototype_id,
    hypothesis,
    ROUND(
      0.15 * learning_target_clarity +
      0.12 * test_condition_quality +
      0.15 * evidence_standard_quality +
      0.12 * participant_fit +
      0.13 * risk_boundary_quality +
      0.11 * interpretation_limit_clarity +
      0.14 * decision_rule_quality +
      0.08 * repeatability,
      4
    ) AS experiment_quality_score
FROM experiments;

CREATE VIEW evidence_quality_scores AS
SELECT
    evidence_id,
    experiment_id,
    evidence_type,
    ROUND(
      0.16 * relevance +
      0.15 * validity +
      0.13 * contextual_realism +
      0.14 * behavioral_richness +
      0.13 * interpretability +
      0.16 * decision_usefulness -
      0.13 * limitation_severity,
      4
    ) AS evidence_quality_score
FROM evidence;

CREATE VIEW user_validation_scores AS
SELECT
    validation_id,
    experiment_id,
    user_group,
    observed_behavior,
    stated_feedback,
    ROUND(
      0.18 * behavioral_signal_strength +
      0.14 * preference_behavior_alignment +
      0.13 * nonuser_inclusion +
      0.13 * accessibility_signal +
      0.14 * trust_signal +
      0.10 * workaround_signal,
      4
    ) AS user_validation_score
FROM user_validation;

CREATE VIEW iteration_learning_scores AS
SELECT
    iteration_id,
    experiment_id,
    iteration_number,
    ROUND(
      0.16 * learning_quality +
      0.14 * change_traceability +
      0.14 * assumption_revision +
      0.12 * prototype_revision_quality -
      0.12 * remaining_uncertainty +
      0.14 * decision_memory_quality +
      0.14 * next_test_clarity,
      4
    ) AS iteration_learning_score
FROM iterations;

CREATE VIEW systems_impact_scores AS
SELECT
    impact_id,
    experiment_id,
    system_issue,
    ROUND(
      0.14 * feedback_risk +
      0.12 * delay_risk +
      0.16 * burden_shift_risk +
      0.16 * capacity_risk +
      0.12 * incentive_risk +
      0.15 * scale_uncertainty -
      0.15 * monitoring_quality,
      4
    ) AS systems_impact_risk
FROM systems_impact;

CREATE VIEW ethical_governance_scores AS
SELECT
    ethics_id,
    experiment_id,
    ethical_issue,
    ROUND(
      0.14 * participant_risk_review +
      0.13 * consent_quality +
      0.13 * privacy_protection +
      0.14 * accessibility_review +
      0.13 * burden_review +
      0.12 * representation_quality +
      0.10 * redress_path +
      0.11 * governance_traceability,
      4
    ) AS ethical_governance_score
FROM ethical_governance;

CREATE VIEW decision_linkage_scores AS
SELECT
    decision_id,
    experiment_id,
    decision_type,
    ROUND(
      0.14 * evidence_to_decision_clarity +
      0.14 * authority_connection +
      0.11 * resource_connection +
      0.12 * stop_rule_quality +
      0.12 * scale_rule_quality +
      0.13 * revision_trigger_quality +
      0.12 * learning_record_quality +
      0.12 * implementation_path_quality,
      4
    ) AS decision_linkage_score
FROM decision_linkage;
