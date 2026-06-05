-- Advanced SQL schema for Journey Mapping and Experience Design.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS journey_profile_scores;
DROP VIEW IF EXISTS stage_friction_scores;
DROP VIEW IF EXISTS touchpoint_quality_scores;
DROP VIEW IF EXISTS transition_risk_scores;
DROP VIEW IF EXISTS accessibility_dignity_scores;
DROP VIEW IF EXISTS trust_status_scores;
DROP VIEW IF EXISTS decision_pathway_scores;
DROP VIEW IF EXISTS service_blueprint_scores;
DROP VIEW IF EXISTS redesign_priority_scores;
DROP VIEW IF EXISTS measurement_learning_scores;

DROP TABLE IF EXISTS measurement_learning;
DROP TABLE IF EXISTS redesign_interventions;
DROP TABLE IF EXISTS service_blueprint;
DROP TABLE IF EXISTS decision_pathways;
DROP TABLE IF EXISTS trust_status;
DROP TABLE IF EXISTS accessibility_dignity;
DROP TABLE IF EXISTS transitions;
DROP TABLE IF EXISTS touchpoints;
DROP TABLE IF EXISTS journey_stages;
DROP TABLE IF EXISTS journey_contexts;

CREATE TABLE journey_contexts (
    journey_id TEXT PRIMARY KEY,
    journey_name TEXT NOT NULL,
    organization_type TEXT NOT NULL,
    domain TEXT NOT NULL,
    clarity REAL CHECK (clarity BETWEEN 0 AND 1),
    emotional_confidence REAL CHECK (emotional_confidence BETWEEN 0 AND 1),
    friction REAL CHECK (friction BETWEEN 0 AND 1),
    transition_quality REAL CHECK (transition_quality BETWEEN 0 AND 1),
    accessibility REAL CHECK (accessibility BETWEEN 0 AND 1),
    trust REAL CHECK (trust BETWEEN 0 AND 1),
    completion_support REAL CHECK (completion_support BETWEEN 0 AND 1),
    backstage_alignment REAL CHECK (backstage_alignment BETWEEN 0 AND 1),
    measurement_quality REAL CHECK (measurement_quality BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE journey_stages (
    stage_id TEXT PRIMARY KEY,
    journey_id TEXT NOT NULL,
    stage_order INTEGER NOT NULL,
    stage_name TEXT NOT NULL,
    touchpoint_type TEXT NOT NULL,
    time_cost REAL CHECK (time_cost BETWEEN 0 AND 1),
    cognitive_load REAL CHECK (cognitive_load BETWEEN 0 AND 1),
    emotional_cost REAL CHECK (emotional_cost BETWEEN 0 AND 1),
    trust_risk REAL CHECK (trust_risk BETWEEN 0 AND 1),
    accessibility_burden REAL CHECK (accessibility_burden BETWEEN 0 AND 1),
    uncertainty REAL CHECK (uncertainty BETWEEN 0 AND 1),
    workaround_dependency REAL CHECK (workaround_dependency BETWEEN 0 AND 1),
    dropoff_risk REAL CHECK (dropoff_risk BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (journey_id) REFERENCES journey_contexts(journey_id)
);

CREATE TABLE touchpoints (
    touchpoint_id TEXT PRIMARY KEY,
    journey_id TEXT NOT NULL,
    stage_id TEXT NOT NULL,
    touchpoint_name TEXT NOT NULL,
    channel TEXT NOT NULL,
    clarity REAL CHECK (clarity BETWEEN 0 AND 1),
    status_visibility REAL CHECK (status_visibility BETWEEN 0 AND 1),
    response_quality REAL CHECK (response_quality BETWEEN 0 AND 1),
    emotional_support REAL CHECK (emotional_support BETWEEN 0 AND 1),
    accessibility_quality REAL CHECK (accessibility_quality BETWEEN 0 AND 1),
    error_recovery REAL CHECK (error_recovery BETWEEN 0 AND 1),
    privacy_confidence REAL CHECK (privacy_confidence BETWEEN 0 AND 1),
    decision_support REAL CHECK (decision_support BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (journey_id) REFERENCES journey_contexts(journey_id),
    FOREIGN KEY (stage_id) REFERENCES journey_stages(stage_id)
);

CREATE TABLE transitions (
    transition_id TEXT PRIMARY KEY,
    journey_id TEXT NOT NULL,
    from_stage TEXT NOT NULL,
    to_stage TEXT NOT NULL,
    transition_type TEXT NOT NULL,
    context_loss REAL CHECK (context_loss BETWEEN 0 AND 1),
    ownership_ambiguity REAL CHECK (ownership_ambiguity BETWEEN 0 AND 1),
    delay_risk REAL CHECK (delay_risk BETWEEN 0 AND 1),
    repetition_required REAL CHECK (repetition_required BETWEEN 0 AND 1),
    status_gap REAL CHECK (status_gap BETWEEN 0 AND 1),
    privacy_risk REAL CHECK (privacy_risk BETWEEN 0 AND 1),
    user_coordination_labor REAL CHECK (user_coordination_labor BETWEEN 0 AND 1),
    transition_criticality REAL CHECK (transition_criticality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (journey_id) REFERENCES journey_contexts(journey_id)
);

CREATE TABLE accessibility_dignity (
    access_id TEXT PRIMARY KEY,
    journey_id TEXT NOT NULL,
    access_issue TEXT NOT NULL,
    language_access REAL CHECK (language_access BETWEEN 0 AND 1),
    disability_access REAL CHECK (disability_access BETWEEN 0 AND 1),
    device_access REAL CHECK (device_access BETWEEN 0 AND 1),
    literacy_support REAL CHECK (literacy_support BETWEEN 0 AND 1),
    time_flexibility REAL CHECK (time_flexibility BETWEEN 0 AND 1),
    dignity_protection REAL CHECK (dignity_protection BETWEEN 0 AND 1),
    recovery_path_quality REAL CHECK (recovery_path_quality BETWEEN 0 AND 1),
    equity_risk REAL CHECK (equity_risk BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (journey_id) REFERENCES journey_contexts(journey_id)
);

CREATE TABLE trust_status (
    trust_id TEXT PRIMARY KEY,
    journey_id TEXT NOT NULL,
    trust_issue TEXT NOT NULL,
    status_visibility REAL CHECK (status_visibility BETWEEN 0 AND 1),
    commitment_clarity REAL CHECK (commitment_clarity BETWEEN 0 AND 1),
    privacy_confidence REAL CHECK (privacy_confidence BETWEEN 0 AND 1),
    consistency REAL CHECK (consistency BETWEEN 0 AND 1),
    response_timeliness REAL CHECK (response_timeliness BETWEEN 0 AND 1),
    explanation_quality REAL CHECK (explanation_quality BETWEEN 0 AND 1),
    escalation_visibility REAL CHECK (escalation_visibility BETWEEN 0 AND 1),
    trust_repair_capacity REAL CHECK (trust_repair_capacity BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (journey_id) REFERENCES journey_contexts(journey_id)
);

CREATE TABLE decision_pathways (
    decision_id TEXT PRIMARY KEY,
    journey_id TEXT NOT NULL,
    stage_id TEXT NOT NULL,
    decision_point TEXT NOT NULL,
    choice_clarity REAL CHECK (choice_clarity BETWEEN 0 AND 1),
    risk_visibility REAL CHECK (risk_visibility BETWEEN 0 AND 1),
    default_quality REAL CHECK (default_quality BETWEEN 0 AND 1),
    timing_fit REAL CHECK (timing_fit BETWEEN 0 AND 1),
    cognitive_support REAL CHECK (cognitive_support BETWEEN 0 AND 1),
    consequence_clarity REAL CHECK (consequence_clarity BETWEEN 0 AND 1),
    recovery_visibility REAL CHECK (recovery_visibility BETWEEN 0 AND 1),
    behavioral_risk REAL CHECK (behavioral_risk BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (journey_id) REFERENCES journey_contexts(journey_id),
    FOREIGN KEY (stage_id) REFERENCES journey_stages(stage_id)
);

CREATE TABLE service_blueprint (
    blueprint_id TEXT PRIMARY KEY,
    journey_id TEXT NOT NULL,
    visible_experience TEXT NOT NULL,
    backstage_dependency TEXT NOT NULL,
    dependency_quality REAL CHECK (dependency_quality BETWEEN 0 AND 1),
    data_continuity REAL CHECK (data_continuity BETWEEN 0 AND 1),
    role_clarity REAL CHECK (role_clarity BETWEEN 0 AND 1),
    workflow_fit REAL CHECK (workflow_fit BETWEEN 0 AND 1),
    staff_capacity REAL CHECK (staff_capacity BETWEEN 0 AND 1),
    governance_alignment REAL CHECK (governance_alignment BETWEEN 0 AND 1),
    feedback_loop_quality REAL CHECK (feedback_loop_quality BETWEEN 0 AND 1),
    implementation_risk REAL CHECK (implementation_risk BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (journey_id) REFERENCES journey_contexts(journey_id)
);

CREATE TABLE redesign_interventions (
    intervention_id TEXT PRIMARY KEY,
    journey_id TEXT NOT NULL,
    intervention_name TEXT NOT NULL,
    intervention_type TEXT NOT NULL,
    friction_reduction REAL CHECK (friction_reduction BETWEEN 0 AND 1),
    trust_gain REAL CHECK (trust_gain BETWEEN 0 AND 1),
    accessibility_gain REAL CHECK (accessibility_gain BETWEEN 0 AND 1),
    transition_gain REAL CHECK (transition_gain BETWEEN 0 AND 1),
    implementation_feasibility REAL CHECK (implementation_feasibility BETWEEN 0 AND 1),
    cost_efficiency REAL CHECK (cost_efficiency BETWEEN 0 AND 1),
    ethical_quality REAL CHECK (ethical_quality BETWEEN 0 AND 1),
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (journey_id) REFERENCES journey_contexts(journey_id)
);

CREATE TABLE measurement_learning (
    metric_id TEXT PRIMARY KEY,
    journey_id TEXT NOT NULL,
    learning_system TEXT NOT NULL,
    completion_tracking REAL CHECK (completion_tracking BETWEEN 0 AND 1),
    dropoff_tracking REAL CHECK (dropoff_tracking BETWEEN 0 AND 1),
    support_signal_tracking REAL CHECK (support_signal_tracking BETWEEN 0 AND 1),
    trust_measurement REAL CHECK (trust_measurement BETWEEN 0 AND 1),
    accessibility_monitoring REAL CHECK (accessibility_monitoring BETWEEN 0 AND 1),
    qualitative_review REAL CHECK (qualitative_review BETWEEN 0 AND 1),
    revision_trigger_quality REAL CHECK (revision_trigger_quality BETWEEN 0 AND 1),
    decision_memory_quality REAL CHECK (decision_memory_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (journey_id) REFERENCES journey_contexts(journey_id)
);

CREATE VIEW journey_profile_scores AS
SELECT
    journey_id,
    journey_name,
    organization_type,
    domain,
    ROUND(
      0.15 * clarity +
      0.12 * emotional_confidence -
      0.18 * friction +
      0.14 * transition_quality +
      0.12 * accessibility +
      0.12 * trust +
      0.10 * completion_support +
      0.10 * backstage_alignment +
      0.07 * measurement_quality,
      4
    ) AS journey_profile_score,
    ROUND(
      0.22 * friction +
      0.16 * (1 - transition_quality) +
      0.14 * (1 - accessibility) +
      0.13 * (1 - trust) +
      0.12 * (1 - clarity) +
      0.11 * (1 - backstage_alignment) +
      0.07 * (1 - completion_support) +
      0.05 * (1 - measurement_quality),
      4
    ) AS redesign_need_score
FROM journey_contexts;

CREATE VIEW stage_friction_scores AS
SELECT
    stage_id,
    journey_id,
    stage_order,
    stage_name,
    touchpoint_type,
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
    ) AS accumulated_friction_score
FROM journey_stages;

CREATE VIEW touchpoint_quality_scores AS
SELECT
    touchpoint_id,
    journey_id,
    stage_id,
    touchpoint_name,
    channel,
    ROUND(
      0.14 * clarity +
      0.13 * status_visibility +
      0.12 * response_quality +
      0.11 * emotional_support +
      0.12 * accessibility_quality +
      0.13 * error_recovery +
      0.11 * privacy_confidence +
      0.14 * decision_support,
      4
    ) AS touchpoint_quality_score
FROM touchpoints;

CREATE VIEW transition_risk_scores AS
SELECT
    transition_id,
    journey_id,
    from_stage,
    to_stage,
    transition_type,
    ROUND(
      0.15 * context_loss +
      0.13 * ownership_ambiguity +
      0.12 * delay_risk +
      0.13 * repetition_required +
      0.14 * status_gap +
      0.08 * privacy_risk +
      0.13 * user_coordination_labor +
      0.12 * transition_criticality,
      4
    ) AS transition_risk_score
FROM transitions;

CREATE VIEW accessibility_dignity_scores AS
SELECT
    access_id,
    journey_id,
    access_issue,
    ROUND(
      0.14 * language_access +
      0.16 * disability_access +
      0.12 * device_access +
      0.13 * literacy_support +
      0.11 * time_flexibility +
      0.16 * dignity_protection +
      0.12 * recovery_path_quality -
      0.12 * equity_risk,
      4
    ) AS accessibility_dignity_score
FROM accessibility_dignity;

CREATE VIEW trust_status_scores AS
SELECT
    trust_id,
    journey_id,
    trust_issue,
    ROUND(
      0.16 * status_visibility +
      0.13 * commitment_clarity +
      0.12 * privacy_confidence +
      0.13 * consistency +
      0.12 * response_timeliness +
      0.13 * explanation_quality +
      0.10 * escalation_visibility +
      0.11 * trust_repair_capacity,
      4
    ) AS trust_status_score
FROM trust_status;

CREATE VIEW decision_pathway_scores AS
SELECT
    decision_id,
    journey_id,
    stage_id,
    decision_point,
    ROUND(
      0.14 * choice_clarity +
      0.12 * risk_visibility +
      0.11 * default_quality +
      0.10 * timing_fit +
      0.15 * cognitive_support +
      0.14 * consequence_clarity +
      0.12 * recovery_visibility -
      0.12 * behavioral_risk,
      4
    ) AS decision_pathway_score
FROM decision_pathways;

CREATE VIEW service_blueprint_scores AS
SELECT
    blueprint_id,
    journey_id,
    visible_experience,
    backstage_dependency,
    ROUND(
      0.14 * dependency_quality +
      0.14 * data_continuity +
      0.12 * role_clarity +
      0.12 * workflow_fit +
      0.10 * staff_capacity +
      0.12 * governance_alignment +
      0.12 * feedback_loop_quality -
      0.14 * implementation_risk,
      4
    ) AS service_blueprint_score
FROM service_blueprint;

CREATE VIEW redesign_priority_scores AS
SELECT
    intervention_id,
    journey_id,
    intervention_name,
    intervention_type,
    ROUND(
      0.17 * friction_reduction +
      0.14 * trust_gain +
      0.14 * accessibility_gain +
      0.15 * transition_gain +
      0.10 * implementation_feasibility +
      0.08 * cost_efficiency +
      0.12 * ethical_quality +
      0.10 * learning_value,
      4
    ) AS redesign_value_score
FROM redesign_interventions;

CREATE VIEW measurement_learning_scores AS
SELECT
    metric_id,
    journey_id,
    learning_system,
    ROUND(
      0.12 * completion_tracking +
      0.12 * dropoff_tracking +
      0.12 * support_signal_tracking +
      0.12 * trust_measurement +
      0.13 * accessibility_monitoring +
      0.14 * qualitative_review +
      0.13 * revision_trigger_quality +
      0.12 * decision_memory_quality,
      4
    ) AS measurement_learning_score
FROM measurement_learning;
