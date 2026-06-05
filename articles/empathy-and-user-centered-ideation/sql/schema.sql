-- Advanced SQL schema for Empathy and User-Centered Ideation.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS empathy_profile_scores;
DROP VIEW IF EXISTS stakeholder_field_scores;
DROP VIEW IF EXISTS observation_quality_scores;
DROP VIEW IF EXISTS journey_friction_scores;
DROP VIEW IF EXISTS unmet_need_scores;
DROP VIEW IF EXISTS preference_behavior_gap_scores;
DROP VIEW IF EXISTS reframing_quality_scores;
DROP VIEW IF EXISTS ethical_empathy_scores;
DROP VIEW IF EXISTS systems_empathy_scores;
DROP VIEW IF EXISTS decision_linkage_scores;

DROP TABLE IF EXISTS decision_linkage;
DROP TABLE IF EXISTS systems_empathy;
DROP TABLE IF EXISTS ethical_empathy;
DROP TABLE IF EXISTS problem_reframes;
DROP TABLE IF EXISTS preference_behavior;
DROP TABLE IF EXISTS unmet_needs;
DROP TABLE IF EXISTS journey_friction;
DROP TABLE IF EXISTS observations;
DROP TABLE IF EXISTS stakeholder_field;
DROP TABLE IF EXISTS empathy_contexts;

CREATE TABLE empathy_contexts (
    context_id TEXT PRIMARY KEY,
    context_name TEXT NOT NULL,
    organization_type TEXT NOT NULL,
    domain TEXT NOT NULL,
    observational_depth REAL CHECK (observational_depth BETWEEN 0 AND 1),
    projection_risk REAL CHECK (projection_risk BETWEEN 0 AND 1),
    unmet_need_visibility REAL CHECK (unmet_need_visibility BETWEEN 0 AND 1),
    stakeholder_breadth REAL CHECK (stakeholder_breadth BETWEEN 0 AND 1),
    reframing_potential REAL CHECK (reframing_potential BETWEEN 0 AND 1),
    ethical_review REAL CHECK (ethical_review BETWEEN 0 AND 1),
    systems_awareness REAL CHECK (systems_awareness BETWEEN 0 AND 1),
    decision_linkage REAL CHECK (decision_linkage BETWEEN 0 AND 1),
    institutional_memory REAL CHECK (institutional_memory BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE stakeholder_field (
    stakeholder_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    stakeholder_group TEXT NOT NULL,
    relationship_to_system TEXT NOT NULL,
    visibility REAL CHECK (visibility BETWEEN 0 AND 1),
    influence REAL CHECK (influence BETWEEN 0 AND 1),
    vulnerability REAL CHECK (vulnerability BETWEEN 0 AND 1),
    knowledge_value REAL CHECK (knowledge_value BETWEEN 0 AND 1),
    participation_access REAL CHECK (participation_access BETWEEN 0 AND 1),
    burden_risk REAL CHECK (burden_risk BETWEEN 0 AND 1),
    representation_gap REAL CHECK (representation_gap BETWEEN 0 AND 1),
    decision_relevance REAL CHECK (decision_relevance BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES empathy_contexts(context_id)
);

CREATE TABLE observations (
    observation_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    stakeholder_id TEXT NOT NULL,
    observation_method TEXT NOT NULL,
    observed_signal TEXT NOT NULL,
    contextual_depth REAL CHECK (contextual_depth BETWEEN 0 AND 1),
    behavioral_clarity REAL CHECK (behavioral_clarity BETWEEN 0 AND 1),
    workaround_visibility REAL CHECK (workaround_visibility BETWEEN 0 AND 1),
    emotional_signal REAL CHECK (emotional_signal BETWEEN 0 AND 1),
    accessibility_signal REAL CHECK (accessibility_signal BETWEEN 0 AND 1),
    trust_signal REAL CHECK (trust_signal BETWEEN 0 AND 1),
    interpretation_confidence REAL CHECK (interpretation_confidence BETWEEN 0 AND 1),
    strategic_relevance REAL CHECK (strategic_relevance BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES empathy_contexts(context_id),
    FOREIGN KEY (stakeholder_id) REFERENCES stakeholder_field(stakeholder_id)
);

CREATE TABLE journey_friction (
    journey_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    stage_name TEXT NOT NULL,
    stakeholder_group TEXT NOT NULL,
    time_cost REAL CHECK (time_cost BETWEEN 0 AND 1),
    cognitive_load REAL CHECK (cognitive_load BETWEEN 0 AND 1),
    emotional_cost REAL CHECK (emotional_cost BETWEEN 0 AND 1),
    trust_risk REAL CHECK (trust_risk BETWEEN 0 AND 1),
    accessibility_burden REAL CHECK (accessibility_burden BETWEEN 0 AND 1),
    uncertainty REAL CHECK (uncertainty BETWEEN 0 AND 1),
    workaround_dependency REAL CHECK (workaround_dependency BETWEEN 0 AND 1),
    dropoff_risk REAL CHECK (dropoff_risk BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES empathy_contexts(context_id)
);

CREATE TABLE unmet_needs (
    need_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    stakeholder_group TEXT NOT NULL,
    need_statement TEXT NOT NULL,
    need_type TEXT NOT NULL,
    visibility REAL CHECK (visibility BETWEEN 0 AND 1),
    criticality REAL CHECK (criticality BETWEEN 0 AND 1),
    frequency REAL CHECK (frequency BETWEEN 0 AND 1),
    burden_intensity REAL CHECK (burden_intensity BETWEEN 0 AND 1),
    evidence_strength REAL CHECK (evidence_strength BETWEEN 0 AND 1),
    solution_fit_uncertainty REAL CHECK (solution_fit_uncertainty BETWEEN 0 AND 1),
    stakeholder_sensitivity REAL CHECK (stakeholder_sensitivity BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES empathy_contexts(context_id)
);

CREATE TABLE preference_behavior (
    gap_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    stakeholder_group TEXT NOT NULL,
    stated_preference TEXT NOT NULL,
    observed_behavior TEXT NOT NULL,
    preference_clarity REAL CHECK (preference_clarity BETWEEN 0 AND 1),
    behavioral_evidence REAL CHECK (behavioral_evidence BETWEEN 0 AND 1),
    alignment_score REAL CHECK (alignment_score BETWEEN 0 AND 1),
    interpretive_uncertainty REAL CHECK (interpretive_uncertainty BETWEEN 0 AND 1),
    strategic_importance REAL CHECK (strategic_importance BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES empathy_contexts(context_id)
);

CREATE TABLE problem_reframes (
    reframe_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    initial_frame TEXT NOT NULL,
    reframed_problem TEXT NOT NULL,
    evidence_basis TEXT NOT NULL,
    inquiry_influence REAL CHECK (inquiry_influence BETWEEN 0 AND 1),
    projection_reduction REAL CHECK (projection_reduction BETWEEN 0 AND 1),
    causal_depth REAL CHECK (causal_depth BETWEEN 0 AND 1),
    stakeholder_evidence REAL CHECK (stakeholder_evidence BETWEEN 0 AND 1),
    systems_context REAL CHECK (systems_context BETWEEN 0 AND 1),
    ethical_awareness REAL CHECK (ethical_awareness BETWEEN 0 AND 1),
    decision_usefulness REAL CHECK (decision_usefulness BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES empathy_contexts(context_id)
);

CREATE TABLE ethical_empathy (
    ethics_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    ethical_issue TEXT NOT NULL,
    participation_quality REAL CHECK (participation_quality BETWEEN 0 AND 1),
    power_awareness REAL CHECK (power_awareness BETWEEN 0 AND 1),
    burden_visibility REAL CHECK (burden_visibility BETWEEN 0 AND 1),
    consent_quality REAL CHECK (consent_quality BETWEEN 0 AND 1),
    representation_quality REAL CHECK (representation_quality BETWEEN 0 AND 1),
    redress_quality REAL CHECK (redress_quality BETWEEN 0 AND 1),
    decision_traceability REAL CHECK (decision_traceability BETWEEN 0 AND 1),
    harm_monitoring REAL CHECK (harm_monitoring BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES empathy_contexts(context_id)
);

CREATE TABLE systems_empathy (
    system_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    system_issue TEXT NOT NULL,
    feedback_risk REAL CHECK (feedback_risk BETWEEN 0 AND 1),
    delay_risk REAL CHECK (delay_risk BETWEEN 0 AND 1),
    burden_shift_risk REAL CHECK (burden_shift_risk BETWEEN 0 AND 1),
    incentive_misalignment REAL CHECK (incentive_misalignment BETWEEN 0 AND 1),
    metric_gaming_risk REAL CHECK (metric_gaming_risk BETWEEN 0 AND 1),
    context_dependency REAL CHECK (context_dependency BETWEEN 0 AND 1),
    leverage_relevance REAL CHECK (leverage_relevance BETWEEN 0 AND 1),
    monitoring_quality REAL CHECK (monitoring_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES empathy_contexts(context_id)
);

CREATE TABLE decision_linkage (
    decision_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    insight_artifact TEXT NOT NULL,
    decision_type TEXT NOT NULL,
    artifact_quality REAL CHECK (artifact_quality BETWEEN 0 AND 1),
    evidence_quality REAL CHECK (evidence_quality BETWEEN 0 AND 1),
    decision_relevance REAL CHECK (decision_relevance BETWEEN 0 AND 1),
    authority_connection REAL CHECK (authority_connection BETWEEN 0 AND 1),
    resource_connection REAL CHECK (resource_connection BETWEEN 0 AND 1),
    revision_trigger_quality REAL CHECK (revision_trigger_quality BETWEEN 0 AND 1),
    learning_memory_quality REAL CHECK (learning_memory_quality BETWEEN 0 AND 1),
    implementation_path_quality REAL CHECK (implementation_path_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES empathy_contexts(context_id)
);

CREATE VIEW empathy_profile_scores AS
SELECT
    context_id,
    context_name,
    organization_type,
    domain,
    ROUND(
      0.16 * observational_depth -
      0.14 * projection_risk +
      0.16 * unmet_need_visibility +
      0.12 * stakeholder_breadth +
      0.16 * reframing_potential +
      0.10 * ethical_review +
      0.10 * systems_awareness +
      0.14 * decision_linkage +
      0.10 * institutional_memory,
      4
    ) AS empathy_profile_score,
    ROUND(
      0.20 * projection_risk +
      0.16 * (1 - decision_linkage) +
      0.14 * (1 - observational_depth) +
      0.12 * (1 - unmet_need_visibility) +
      0.12 * (1 - ethical_review) +
      0.10 * (1 - systems_awareness) +
      0.08 * (1 - stakeholder_breadth) +
      0.08 * (1 - institutional_memory),
      4
    ) AS superficiality_risk
FROM empathy_contexts;

CREATE VIEW stakeholder_field_scores AS
SELECT
    stakeholder_id,
    context_id,
    stakeholder_group,
    relationship_to_system,
    ROUND(
      0.14 * (1 - visibility) +
      0.12 * influence +
      0.18 * vulnerability +
      0.16 * knowledge_value +
      0.12 * (1 - participation_access) +
      0.12 * burden_risk +
      0.10 * representation_gap +
      0.06 * decision_relevance,
      4
    ) AS inclusion_priority_score
FROM stakeholder_field;

CREATE VIEW observation_quality_scores AS
SELECT
    observation_id,
    context_id,
    stakeholder_id,
    observation_method,
    observed_signal,
    ROUND(
      0.15 * contextual_depth +
      0.15 * behavioral_clarity +
      0.14 * workaround_visibility +
      0.11 * emotional_signal +
      0.10 * accessibility_signal +
      0.11 * trust_signal +
      0.12 * interpretation_confidence +
      0.12 * strategic_relevance,
      4
    ) AS observation_quality_score
FROM observations;

CREATE VIEW journey_friction_scores AS
SELECT
    journey_id,
    context_id,
    stage_name,
    stakeholder_group,
    ROUND(
      0.13 * time_cost +
      0.14 * cognitive_load +
      0.14 * emotional_cost +
      0.14 * trust_risk +
      0.12 * accessibility_burden +
      0.13 * uncertainty +
      0.10 * workaround_dependency +
      0.10 * dropoff_risk,
      4
    ) AS accumulated_burden_score
FROM journey_friction;

CREATE VIEW unmet_need_scores AS
SELECT
    need_id,
    context_id,
    stakeholder_group,
    need_statement,
    need_type,
    ROUND(
      0.10 * (1 - visibility) +
      0.18 * criticality +
      0.12 * frequency +
      0.16 * burden_intensity +
      0.12 * evidence_strength +
      0.14 * solution_fit_uncertainty +
      0.18 * stakeholder_sensitivity,
      4
    ) AS unmet_need_priority
FROM unmet_needs;

CREATE VIEW preference_behavior_gap_scores AS
SELECT
    gap_id,
    context_id,
    stakeholder_group,
    stated_preference,
    observed_behavior,
    ROUND(
      0.18 * (1 - alignment_score) +
      0.16 * behavioral_evidence +
      0.14 * interpretive_uncertainty +
      0.16 * strategic_importance +
      0.10 * preference_clarity,
      4
    ) AS preference_behavior_gap_score
FROM preference_behavior;

CREATE VIEW reframing_quality_scores AS
SELECT
    reframe_id,
    context_id,
    initial_frame,
    reframed_problem,
    evidence_basis,
    ROUND(
      0.14 * inquiry_influence +
      0.14 * projection_reduction +
      0.14 * causal_depth +
      0.13 * stakeholder_evidence +
      0.12 * systems_context +
      0.11 * ethical_awareness +
      0.12 * decision_usefulness,
      4
    ) AS reframing_quality_score
FROM problem_reframes;

CREATE VIEW ethical_empathy_scores AS
SELECT
    ethics_id,
    context_id,
    ethical_issue,
    ROUND(
      0.13 * participation_quality +
      0.14 * power_awareness +
      0.13 * burden_visibility +
      0.11 * consent_quality +
      0.12 * representation_quality +
      0.12 * redress_quality +
      0.13 * decision_traceability +
      0.12 * harm_monitoring,
      4
    ) AS ethical_empathy_score
FROM ethical_empathy;

CREATE VIEW systems_empathy_scores AS
SELECT
    system_id,
    context_id,
    system_issue,
    ROUND(
      0.14 * feedback_risk +
      0.11 * delay_risk +
      0.16 * burden_shift_risk +
      0.14 * incentive_misalignment +
      0.12 * metric_gaming_risk +
      0.12 * context_dependency +
      0.11 * leverage_relevance -
      0.10 * monitoring_quality,
      4
    ) AS systems_empathy_risk
FROM systems_empathy;

CREATE VIEW decision_linkage_scores AS
SELECT
    decision_id,
    context_id,
    insight_artifact,
    decision_type,
    ROUND(
      0.12 * artifact_quality +
      0.14 * evidence_quality +
      0.15 * decision_relevance +
      0.15 * authority_connection +
      0.11 * resource_connection +
      0.12 * revision_trigger_quality +
      0.10 * learning_memory_quality +
      0.11 * implementation_path_quality,
      4
    ) AS decision_linkage_score
FROM decision_linkage;
