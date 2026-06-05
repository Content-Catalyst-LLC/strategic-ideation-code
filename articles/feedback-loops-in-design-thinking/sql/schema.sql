-- Advanced SQL schema for Feedback Loops in Design Thinking.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS feedback_system_profile_scores;
DROP VIEW IF EXISTS signal_quality_scores;
DROP VIEW IF EXISTS interpretation_capacity_scores;
DROP VIEW IF EXISTS adjustment_pathway_scores;
DROP VIEW IF EXISTS user_feedback_scores;
DROP VIEW IF EXISTS temporal_learning_scores;
DROP VIEW IF EXISTS systems_impact_scores;
DROP VIEW IF EXISTS ethical_feedback_governance_scores;
DROP VIEW IF EXISTS decision_linkage_scores;
DROP VIEW IF EXISTS feedback_memory_scores;

DROP TABLE IF EXISTS feedback_memory;
DROP TABLE IF EXISTS decision_linkage;
DROP TABLE IF EXISTS ethical_governance;
DROP TABLE IF EXISTS systems_impact;
DROP TABLE IF EXISTS temporal_learning;
DROP TABLE IF EXISTS user_feedback;
DROP TABLE IF EXISTS adjustment_pathways;
DROP TABLE IF EXISTS interpretation_capacity;
DROP TABLE IF EXISTS signals;
DROP TABLE IF EXISTS feedback_systems;

CREATE TABLE feedback_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    organization_type TEXT NOT NULL,
    domain TEXT NOT NULL,
    signal_quality REAL CHECK (signal_quality BETWEEN 0 AND 1),
    interpretation_capacity REAL CHECK (interpretation_capacity BETWEEN 0 AND 1),
    adjustment_speed REAL CHECK (adjustment_speed BETWEEN 0 AND 1),
    user_insight_depth REAL CHECK (user_insight_depth BETWEEN 0 AND 1),
    stability REAL CHECK (stability BETWEEN 0 AND 1),
    ethical_integrity REAL CHECK (ethical_integrity BETWEEN 0 AND 1),
    systems_awareness REAL CHECK (systems_awareness BETWEEN 0 AND 1),
    decision_linkage REAL CHECK (decision_linkage BETWEEN 0 AND 1),
    learning_memory REAL CHECK (learning_memory BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE signals (
    signal_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    signal_source TEXT NOT NULL,
    signal_type TEXT NOT NULL,
    relevance REAL CHECK (relevance BETWEEN 0 AND 1),
    timeliness REAL CHECK (timeliness BETWEEN 0 AND 1),
    reliability REAL CHECK (reliability BETWEEN 0 AND 1),
    representativeness REAL CHECK (representativeness BETWEEN 0 AND 1),
    interpretability REAL CHECK (interpretability BETWEEN 0 AND 1),
    behavioral_richness REAL CHECK (behavioral_richness BETWEEN 0 AND 1),
    bias_risk REAL CHECK (bias_risk BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES feedback_systems(system_id)
);

CREATE TABLE interpretation_capacity (
    interpretation_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    interpretation_practice TEXT NOT NULL,
    contextual_understanding REAL CHECK (contextual_understanding BETWEEN 0 AND 1),
    domain_expertise REAL CHECK (domain_expertise BETWEEN 0 AND 1),
    user_research_capacity REAL CHECK (user_research_capacity BETWEEN 0 AND 1),
    systems_thinking_capacity REAL CHECK (systems_thinking_capacity BETWEEN 0 AND 1),
    bias_review REAL CHECK (bias_review BETWEEN 0 AND 1),
    triangulation_quality REAL CHECK (triangulation_quality BETWEEN 0 AND 1),
    decision_relevance REAL CHECK (decision_relevance BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES feedback_systems(system_id)
);

CREATE TABLE adjustment_pathways (
    adjustment_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    adjustment_pathway TEXT NOT NULL,
    decision_authority REAL CHECK (decision_authority BETWEEN 0 AND 1),
    resource_availability REAL CHECK (resource_availability BETWEEN 0 AND 1),
    revision_trigger_quality REAL CHECK (revision_trigger_quality BETWEEN 0 AND 1),
    implementation_speed REAL CHECK (implementation_speed BETWEEN 0 AND 1),
    change_traceability REAL CHECK (change_traceability BETWEEN 0 AND 1),
    stability_protection REAL CHECK (stability_protection BETWEEN 0 AND 1),
    communication_quality REAL CHECK (communication_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES feedback_systems(system_id)
);

CREATE TABLE user_feedback (
    feedback_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
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
    FOREIGN KEY (system_id) REFERENCES feedback_systems(system_id)
);

CREATE TABLE temporal_learning (
    temporal_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    temporal_issue TEXT NOT NULL,
    early_signal_quality REAL CHECK (early_signal_quality BETWEEN 0 AND 1),
    delayed_outcome_tracking REAL CHECK (delayed_outcome_tracking BETWEEN 0 AND 1),
    pattern_detection REAL CHECK (pattern_detection BETWEEN 0 AND 1),
    drift_detection REAL CHECK (drift_detection BETWEEN 0 AND 1),
    learning_cadence_quality REAL CHECK (learning_cadence_quality BETWEEN 0 AND 1),
    overreaction_risk REAL CHECK (overreaction_risk BETWEEN 0 AND 1),
    revision_timing_quality REAL CHECK (revision_timing_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES feedback_systems(system_id)
);

CREATE TABLE systems_impact (
    impact_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    system_issue TEXT NOT NULL,
    feedback_risk REAL CHECK (feedback_risk BETWEEN 0 AND 1),
    delay_risk REAL CHECK (delay_risk BETWEEN 0 AND 1),
    burden_shift_risk REAL CHECK (burden_shift_risk BETWEEN 0 AND 1),
    capacity_risk REAL CHECK (capacity_risk BETWEEN 0 AND 1),
    incentive_risk REAL CHECK (incentive_risk BETWEEN 0 AND 1),
    scale_uncertainty REAL CHECK (scale_uncertainty BETWEEN 0 AND 1),
    monitoring_quality REAL CHECK (monitoring_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES feedback_systems(system_id)
);

CREATE TABLE ethical_governance (
    ethics_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    ethical_issue TEXT NOT NULL,
    privacy_protection REAL CHECK (privacy_protection BETWEEN 0 AND 1),
    consent_quality REAL CHECK (consent_quality BETWEEN 0 AND 1),
    accessibility_review REAL CHECK (accessibility_review BETWEEN 0 AND 1),
    burden_review REAL CHECK (burden_review BETWEEN 0 AND 1),
    representation_quality REAL CHECK (representation_quality BETWEEN 0 AND 1),
    redress_path REAL CHECK (redress_path BETWEEN 0 AND 1),
    accountability_quality REAL CHECK (accountability_quality BETWEEN 0 AND 1),
    governance_traceability REAL CHECK (governance_traceability BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES feedback_systems(system_id)
);

CREATE TABLE decision_linkage (
    decision_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    decision_type TEXT NOT NULL,
    evidence_to_decision_clarity REAL CHECK (evidence_to_decision_clarity BETWEEN 0 AND 1),
    authority_connection REAL CHECK (authority_connection BETWEEN 0 AND 1),
    resource_connection REAL CHECK (resource_connection BETWEEN 0 AND 1),
    revision_trigger_quality REAL CHECK (revision_trigger_quality BETWEEN 0 AND 1),
    stop_rule_quality REAL CHECK (stop_rule_quality BETWEEN 0 AND 1),
    scale_rule_quality REAL CHECK (scale_rule_quality BETWEEN 0 AND 1),
    learning_record_quality REAL CHECK (learning_record_quality BETWEEN 0 AND 1),
    implementation_path_quality REAL CHECK (implementation_path_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES feedback_systems(system_id)
);

CREATE TABLE feedback_memory (
    memory_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    memory_practice TEXT NOT NULL,
    signal_archive_quality REAL CHECK (signal_archive_quality BETWEEN 0 AND 1),
    interpretation_record_quality REAL CHECK (interpretation_record_quality BETWEEN 0 AND 1),
    change_record_quality REAL CHECK (change_record_quality BETWEEN 0 AND 1),
    decision_rationale_quality REAL CHECK (decision_rationale_quality BETWEEN 0 AND 1),
    remaining_uncertainty_record REAL CHECK (remaining_uncertainty_record BETWEEN 0 AND 1),
    accessibility_of_learning REAL CHECK (accessibility_of_learning BETWEEN 0 AND 1),
    reuse_quality REAL CHECK (reuse_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES feedback_systems(system_id)
);

CREATE VIEW feedback_system_profile_scores AS
SELECT
    system_id,
    system_name,
    ROUND(
      0.13 * signal_quality +
      0.13 * interpretation_capacity +
      0.10 * adjustment_speed +
      0.13 * user_insight_depth +
      0.10 * stability +
      0.11 * ethical_integrity +
      0.10 * systems_awareness +
      0.10 * decision_linkage +
      0.10 * learning_memory,
      4
    ) AS feedback_profile_score,
    ROUND(
      0.16 * adjustment_speed +
      0.15 * (1 - signal_quality) +
      0.15 * (1 - interpretation_capacity) +
      0.13 * (1 - stability) +
      0.12 * (1 - systems_awareness) +
      0.12 * (1 - ethical_integrity) +
      0.10 * (1 - decision_linkage) +
      0.07 * (1 - learning_memory),
      4
    ) AS noisy_churn_risk
FROM feedback_systems;

CREATE VIEW signal_quality_scores AS
SELECT
    signal_id,
    system_id,
    signal_source,
    signal_type,
    ROUND(
      0.15 * relevance +
      0.13 * timeliness +
      0.14 * reliability +
      0.14 * representativeness +
      0.13 * interpretability +
      0.14 * behavioral_richness -
      0.13 * bias_risk,
      4
    ) AS signal_quality_score
FROM signals;

CREATE VIEW interpretation_capacity_scores AS
SELECT
    interpretation_id,
    system_id,
    interpretation_practice,
    ROUND(
      0.14 * contextual_understanding +
      0.13 * domain_expertise +
      0.15 * user_research_capacity +
      0.15 * systems_thinking_capacity +
      0.13 * bias_review +
      0.15 * triangulation_quality +
      0.15 * decision_relevance,
      4
    ) AS interpretation_capacity_score
FROM interpretation_capacity;

CREATE VIEW adjustment_pathway_scores AS
SELECT
    adjustment_id,
    system_id,
    adjustment_pathway,
    ROUND(
      0.15 * decision_authority +
      0.12 * resource_availability +
      0.14 * revision_trigger_quality +
      0.10 * implementation_speed +
      0.14 * change_traceability +
      0.13 * stability_protection +
      0.12 * communication_quality,
      4
    ) AS adjustment_pathway_score
FROM adjustment_pathways;

CREATE VIEW user_feedback_scores AS
SELECT
    feedback_id,
    system_id,
    user_group,
    observed_behavior,
    stated_feedback,
    ROUND(
      0.18 * behavioral_signal_strength +
      0.14 * preference_behavior_alignment +
      0.13 * nonuser_inclusion +
      0.15 * accessibility_signal +
      0.15 * trust_signal +
      0.11 * workaround_signal,
      4
    ) AS user_feedback_score
FROM user_feedback;

CREATE VIEW temporal_learning_scores AS
SELECT
    temporal_id,
    system_id,
    temporal_issue,
    ROUND(
      0.12 * early_signal_quality +
      0.15 * delayed_outcome_tracking +
      0.15 * pattern_detection +
      0.14 * drift_detection +
      0.14 * learning_cadence_quality -
      0.12 * overreaction_risk +
      0.14 * revision_timing_quality,
      4
    ) AS temporal_learning_score
FROM temporal_learning;

CREATE VIEW systems_impact_scores AS
SELECT
    impact_id,
    system_id,
    system_issue,
    ROUND(
      0.14 * feedback_risk +
      0.12 * delay_risk +
      0.16 * burden_shift_risk +
      0.16 * capacity_risk +
      0.12 * incentive_risk +
      0.14 * scale_uncertainty -
      0.16 * monitoring_quality,
      4
    ) AS systems_impact_risk
FROM systems_impact;

CREATE VIEW ethical_feedback_governance_scores AS
SELECT
    ethics_id,
    system_id,
    ethical_issue,
    ROUND(
      0.14 * privacy_protection +
      0.13 * consent_quality +
      0.14 * accessibility_review +
      0.13 * burden_review +
      0.13 * representation_quality +
      0.10 * redress_path +
      0.12 * accountability_quality +
      0.11 * governance_traceability,
      4
    ) AS ethical_governance_score
FROM ethical_governance;

CREATE VIEW decision_linkage_scores AS
SELECT
    decision_id,
    system_id,
    decision_type,
    ROUND(
      0.14 * evidence_to_decision_clarity +
      0.14 * authority_connection +
      0.11 * resource_connection +
      0.13 * revision_trigger_quality +
      0.11 * stop_rule_quality +
      0.10 * scale_rule_quality +
      0.13 * learning_record_quality +
      0.14 * implementation_path_quality,
      4
    ) AS decision_linkage_score
FROM decision_linkage;

CREATE VIEW feedback_memory_scores AS
SELECT
    memory_id,
    system_id,
    memory_practice,
    ROUND(
      0.13 * signal_archive_quality +
      0.14 * interpretation_record_quality +
      0.14 * change_record_quality +
      0.14 * decision_rationale_quality +
      0.13 * remaining_uncertainty_record +
      0.14 * accessibility_of_learning +
      0.14 * reuse_quality,
      4
    ) AS feedback_memory_score
FROM feedback_memory;
