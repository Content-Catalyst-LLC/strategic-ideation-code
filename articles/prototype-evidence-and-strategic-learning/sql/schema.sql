-- Advanced SQL schema for Prototype Evidence and Strategic Learning.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS prototype_system_profile_scores;
DROP VIEW IF EXISTS assumption_evidence_scores;
DROP VIEW IF EXISTS evidence_quality_scores;
DROP VIEW IF EXISTS behavioral_observation_scores;
DROP VIEW IF EXISTS context_realism_scores;
DROP VIEW IF EXISTS systems_impact_scores;
DROP VIEW IF EXISTS ethical_prototype_governance_scores;
DROP VIEW IF EXISTS decision_rule_scores;
DROP VIEW IF EXISTS learning_memory_scores;

DROP TABLE IF EXISTS learning_memory;
DROP TABLE IF EXISTS decision_rules;
DROP TABLE IF EXISTS ethical_reviews;
DROP TABLE IF EXISTS systems_effects;
DROP TABLE IF EXISTS context_reviews;
DROP TABLE IF EXISTS behavioral_observations;
DROP TABLE IF EXISTS evidence_records;
DROP TABLE IF EXISTS assumptions;
DROP TABLE IF EXISTS prototype_systems;

CREATE TABLE prototype_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    organization_type TEXT NOT NULL,
    domain TEXT NOT NULL,
    assumption_clarity REAL CHECK (assumption_clarity BETWEEN 0 AND 1),
    learning_target_fit REAL CHECK (learning_target_fit BETWEEN 0 AND 1),
    evidence_quality REAL CHECK (evidence_quality BETWEEN 0 AND 1),
    behavioral_grounding REAL CHECK (behavioral_grounding BETWEEN 0 AND 1),
    context_realism REAL CHECK (context_realism BETWEEN 0 AND 1),
    systems_awareness REAL CHECK (systems_awareness BETWEEN 0 AND 1),
    decision_linkage REAL CHECK (decision_linkage BETWEEN 0 AND 1),
    ethical_review REAL CHECK (ethical_review BETWEEN 0 AND 1),
    learning_memory REAL CHECK (learning_memory BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE assumptions (
    assumption_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    assumption TEXT NOT NULL,
    assumption_type TEXT NOT NULL,
    uncertainty REAL CHECK (uncertainty BETWEEN 0 AND 1),
    consequence REAL CHECK (consequence BETWEEN 0 AND 1),
    explicitness REAL CHECK (explicitness BETWEEN 0 AND 1),
    testability REAL CHECK (testability BETWEEN 0 AND 1),
    learning_target_clarity REAL CHECK (learning_target_clarity BETWEEN 0 AND 1),
    evidence_standard_defined REAL CHECK (evidence_standard_defined BETWEEN 0 AND 1),
    decision_rule_defined REAL CHECK (decision_rule_defined BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES prototype_systems(system_id)
);

CREATE TABLE evidence_records (
    evidence_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    prototype_type TEXT NOT NULL,
    evidence_type TEXT NOT NULL,
    relevance REAL CHECK (relevance BETWEEN 0 AND 1),
    validity REAL CHECK (validity BETWEEN 0 AND 1),
    context_realism REAL CHECK (context_realism BETWEEN 0 AND 1),
    behavioral_richness REAL CHECK (behavioral_richness BETWEEN 0 AND 1),
    sample_fit REAL CHECK (sample_fit BETWEEN 0 AND 1),
    interpretability REAL CHECK (interpretability BETWEEN 0 AND 1),
    decision_usefulness REAL CHECK (decision_usefulness BETWEEN 0 AND 1),
    limitation_clarity REAL CHECK (limitation_clarity BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES prototype_systems(system_id)
);

CREATE TABLE behavioral_observations (
    observation_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    observed_behavior TEXT NOT NULL,
    stated_feedback TEXT NOT NULL,
    behavior_signal_strength REAL CHECK (behavior_signal_strength BETWEEN 0 AND 1),
    preference_behavior_alignment REAL CHECK (preference_behavior_alignment BETWEEN 0 AND 1),
    hesitation_signal REAL CHECK (hesitation_signal BETWEEN 0 AND 1),
    workaround_signal REAL CHECK (workaround_signal BETWEEN 0 AND 1),
    abandonment_signal REAL CHECK (abandonment_signal BETWEEN 0 AND 1),
    commitment_signal REAL CHECK (commitment_signal BETWEEN 0 AND 1),
    burden_signal REAL CHECK (burden_signal BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES prototype_systems(system_id)
);

CREATE TABLE context_reviews (
    context_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    test_context TEXT NOT NULL,
    realism_of_setting REAL CHECK (realism_of_setting BETWEEN 0 AND 1),
    realism_of_incentives REAL CHECK (realism_of_incentives BETWEEN 0 AND 1),
    realism_of_support REAL CHECK (realism_of_support BETWEEN 0 AND 1),
    realism_of_constraints REAL CHECK (realism_of_constraints BETWEEN 0 AND 1),
    participant_fit REAL CHECK (participant_fit BETWEEN 0 AND 1),
    scale_similarity REAL CHECK (scale_similarity BETWEEN 0 AND 1),
    time_horizon_fit REAL CHECK (time_horizon_fit BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES prototype_systems(system_id)
);

CREATE TABLE systems_effects (
    effect_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    system_issue TEXT NOT NULL,
    feedback_loop_risk REAL CHECK (feedback_loop_risk BETWEEN 0 AND 1),
    delay_risk REAL CHECK (delay_risk BETWEEN 0 AND 1),
    burden_shift_risk REAL CHECK (burden_shift_risk BETWEEN 0 AND 1),
    capacity_risk REAL CHECK (capacity_risk BETWEEN 0 AND 1),
    incentive_risk REAL CHECK (incentive_risk BETWEEN 0 AND 1),
    scale_uncertainty REAL CHECK (scale_uncertainty BETWEEN 0 AND 1),
    monitoring_quality REAL CHECK (monitoring_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES prototype_systems(system_id)
);

CREATE TABLE ethical_reviews (
    ethics_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    ethical_issue TEXT NOT NULL,
    consent_quality REAL CHECK (consent_quality BETWEEN 0 AND 1),
    privacy_protection REAL CHECK (privacy_protection BETWEEN 0 AND 1),
    accessibility_review REAL CHECK (accessibility_review BETWEEN 0 AND 1),
    burden_review REAL CHECK (burden_review BETWEEN 0 AND 1),
    representation_quality REAL CHECK (representation_quality BETWEEN 0 AND 1),
    redress_path REAL CHECK (redress_path BETWEEN 0 AND 1),
    expectation_management REAL CHECK (expectation_management BETWEEN 0 AND 1),
    accountability_quality REAL CHECK (accountability_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES prototype_systems(system_id)
);

CREATE TABLE decision_rules (
    decision_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    decision_context TEXT NOT NULL,
    evidence_to_decision_clarity REAL CHECK (evidence_to_decision_clarity BETWEEN 0 AND 1),
    threshold_defined REAL CHECK (threshold_defined BETWEEN 0 AND 1),
    stop_rule_quality REAL CHECK (stop_rule_quality BETWEEN 0 AND 1),
    revise_rule_quality REAL CHECK (revise_rule_quality BETWEEN 0 AND 1),
    scale_rule_quality REAL CHECK (scale_rule_quality BETWEEN 0 AND 1),
    resource_connection REAL CHECK (resource_connection BETWEEN 0 AND 1),
    authority_connection REAL CHECK (authority_connection BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES prototype_systems(system_id)
);

CREATE TABLE learning_memory (
    memory_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    memory_practice TEXT NOT NULL,
    assumption_record_quality REAL CHECK (assumption_record_quality BETWEEN 0 AND 1),
    prototype_description_quality REAL CHECK (prototype_description_quality BETWEEN 0 AND 1),
    evidence_record_quality REAL CHECK (evidence_record_quality BETWEEN 0 AND 1),
    interpretation_quality REAL CHECK (interpretation_quality BETWEEN 0 AND 1),
    decision_rationale_quality REAL CHECK (decision_rationale_quality BETWEEN 0 AND 1),
    limitation_record_quality REAL CHECK (limitation_record_quality BETWEEN 0 AND 1),
    remaining_uncertainty_quality REAL CHECK (remaining_uncertainty_quality BETWEEN 0 AND 1),
    reuse_quality REAL CHECK (reuse_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES prototype_systems(system_id)
);

CREATE VIEW prototype_system_profile_scores AS
SELECT
    system_id,
    system_name,
    ROUND(
      0.13 * assumption_clarity +
      0.13 * learning_target_fit +
      0.15 * evidence_quality +
      0.13 * behavioral_grounding +
      0.11 * context_realism +
      0.11 * systems_awareness +
      0.11 * decision_linkage +
      0.07 * ethical_review +
      0.06 * learning_memory,
      4
    ) AS prototype_learning_quality,
    ROUND(
      0.17 * (1 - assumption_clarity) +
      0.16 * (1 - evidence_quality) +
      0.14 * (1 - behavioral_grounding) +
      0.13 * (1 - decision_linkage) +
      0.12 * (1 - learning_memory) +
      0.11 * (1 - systems_awareness) +
      0.09 * (1 - ethical_review) +
      0.08 * (1 - context_realism),
      4
    ) AS validation_theater_risk
FROM prototype_systems;

CREATE VIEW assumption_evidence_scores AS
SELECT
    assumption_id,
    system_id,
    assumption,
    assumption_type,
    ROUND(0.50 * uncertainty + 0.50 * consequence, 4) AS criticality,
    ROUND(
      0.22 * explicitness +
      0.24 * testability +
      0.22 * learning_target_clarity +
      0.17 * evidence_standard_defined +
      0.15 * decision_rule_defined,
      4
    ) AS test_design_score
FROM assumptions;

CREATE VIEW evidence_quality_scores AS
SELECT
    evidence_id,
    system_id,
    prototype_type,
    evidence_type,
    ROUND(
      0.14 * relevance +
      0.15 * validity +
      0.13 * context_realism +
      0.14 * behavioral_richness +
      0.12 * sample_fit +
      0.13 * interpretability +
      0.11 * decision_usefulness +
      0.08 * limitation_clarity,
      4
    ) AS evidence_quality_score
FROM evidence_records;

CREATE VIEW behavioral_observation_scores AS
SELECT
    observation_id,
    system_id,
    observed_behavior,
    stated_feedback,
    ROUND(
      0.18 * hesitation_signal +
      0.18 * workaround_signal +
      0.20 * abandonment_signal +
      0.18 * burden_signal +
      0.14 * (1 - preference_behavior_alignment) +
      0.12 * (1 - commitment_signal),
      4
    ) AS behavioral_concern_score
FROM behavioral_observations;

CREATE VIEW context_realism_scores AS
SELECT
    context_id,
    system_id,
    test_context,
    ROUND(
      0.16 * realism_of_setting +
      0.13 * realism_of_incentives +
      0.13 * realism_of_support +
      0.15 * realism_of_constraints +
      0.14 * participant_fit +
      0.15 * scale_similarity +
      0.14 * time_horizon_fit,
      4
    ) AS context_realism_score
FROM context_reviews;

CREATE VIEW systems_impact_scores AS
SELECT
    effect_id,
    system_id,
    system_issue,
    ROUND(
      0.14 * feedback_loop_risk +
      0.12 * delay_risk +
      0.16 * burden_shift_risk +
      0.16 * capacity_risk +
      0.12 * incentive_risk +
      0.14 * scale_uncertainty -
      0.16 * monitoring_quality,
      4
    ) AS systems_impact_risk
FROM systems_effects;

CREATE VIEW ethical_prototype_governance_scores AS
SELECT
    ethics_id,
    system_id,
    ethical_issue,
    ROUND(
      0.13 * consent_quality +
      0.13 * privacy_protection +
      0.14 * accessibility_review +
      0.13 * burden_review +
      0.13 * representation_quality +
      0.10 * redress_path +
      0.12 * expectation_management +
      0.12 * accountability_quality,
      4
    ) AS ethical_governance_score
FROM ethical_reviews;

CREATE VIEW decision_rule_scores AS
SELECT
    decision_id,
    system_id,
    decision_context,
    ROUND(
      0.16 * evidence_to_decision_clarity +
      0.14 * threshold_defined +
      0.13 * stop_rule_quality +
      0.13 * revise_rule_quality +
      0.13 * scale_rule_quality +
      0.14 * resource_connection +
      0.17 * authority_connection,
      4
    ) AS decision_rule_score
FROM decision_rules;

CREATE VIEW learning_memory_scores AS
SELECT
    memory_id,
    system_id,
    memory_practice,
    ROUND(
      0.12 * assumption_record_quality +
      0.12 * prototype_description_quality +
      0.14 * evidence_record_quality +
      0.14 * interpretation_quality +
      0.14 * decision_rationale_quality +
      0.12 * limitation_record_quality +
      0.11 * remaining_uncertainty_quality +
      0.11 * reuse_quality,
      4
    ) AS learning_memory_score
FROM learning_memory;
