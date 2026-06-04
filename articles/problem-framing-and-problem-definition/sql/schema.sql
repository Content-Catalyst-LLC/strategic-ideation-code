-- Advanced SQL schema for problem framing and problem definition.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS problem_framing_scores;
DROP VIEW IF EXISTS frame_origin_scores;
DROP VIEW IF EXISTS boundary_quality_scores;
DROP VIEW IF EXISTS stakeholder_frame_scores;
DROP VIEW IF EXISTS causal_quality_scores;
DROP VIEW IF EXISTS assumption_priority_scores;
DROP VIEW IF EXISTS alternative_frame_scores;
DROP VIEW IF EXISTS reframing_trigger_scores;
DROP VIEW IF EXISTS intervention_value_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS intervention_library;
DROP TABLE IF EXISTS reframing_triggers;
DROP TABLE IF EXISTS alternative_frames;
DROP TABLE IF EXISTS assumption_audit;
DROP TABLE IF EXISTS causal_models;
DROP TABLE IF EXISTS stakeholder_frames;
DROP TABLE IF EXISTS boundary_audit;
DROP TABLE IF EXISTS frame_origins;
DROP TABLE IF EXISTS problem_frames;

CREATE TABLE problem_frames (
    frame_id TEXT PRIMARY KEY,
    frame_name TEXT NOT NULL,
    frame_type TEXT NOT NULL,
    domain TEXT NOT NULL,
    boundary_breadth REAL CHECK (boundary_breadth BETWEEN 0 AND 1),
    stakeholder_inclusion REAL CHECK (stakeholder_inclusion BETWEEN 0 AND 1),
    systems_awareness REAL CHECK (systems_awareness BETWEEN 0 AND 1),
    causal_depth REAL CHECK (causal_depth BETWEEN 0 AND 1),
    assumption_clarity REAL CHECK (assumption_clarity BETWEEN 0 AND 1),
    reframing_capacity REAL CHECK (reframing_capacity BETWEEN 0 AND 1),
    actionability REAL CHECK (actionability BETWEEN 0 AND 1),
    institutional_lock_in_risk REAL CHECK (institutional_lock_in_risk BETWEEN 0 AND 1),
    political_convenience_risk REAL CHECK (political_convenience_risk BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE frame_origins (
    origin_id TEXT PRIMARY KEY,
    frame_id TEXT NOT NULL,
    origin_source TEXT NOT NULL,
    authority_weight REAL CHECK (authority_weight BETWEEN 0 AND 1),
    metric_dependency REAL CHECK (metric_dependency BETWEEN 0 AND 1),
    legacy_dependency REAL CHECK (legacy_dependency BETWEEN 0 AND 1),
    stakeholder_evidence_strength REAL CHECK (stakeholder_evidence_strength BETWEEN 0 AND 1),
    frontline_evidence_strength REAL CHECK (frontline_evidence_strength BETWEEN 0 AND 1),
    political_safety REAL CHECK (political_safety BETWEEN 0 AND 1),
    diagnostic_independence REAL CHECK (diagnostic_independence BETWEEN 0 AND 1),
    origin_risk REAL CHECK (origin_risk BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (frame_id) REFERENCES problem_frames(frame_id)
);

CREATE TABLE boundary_audit (
    boundary_id TEXT PRIMARY KEY,
    frame_id TEXT NOT NULL,
    boundary_name TEXT NOT NULL,
    boundary_type TEXT NOT NULL,
    stakeholder_visibility REAL CHECK (stakeholder_visibility BETWEEN 0 AND 1),
    downstream_effect_visibility REAL CHECK (downstream_effect_visibility BETWEEN 0 AND 1),
    externality_visibility REAL CHECK (externality_visibility BETWEEN 0 AND 1),
    implementation_visibility REAL CHECK (implementation_visibility BETWEEN 0 AND 1),
    time_horizon_quality REAL CHECK (time_horizon_quality BETWEEN 0 AND 1),
    hidden_dependency_visibility REAL CHECK (hidden_dependency_visibility BETWEEN 0 AND 1),
    boundary_risk REAL CHECK (boundary_risk BETWEEN 0 AND 1),
    revision_need REAL CHECK (revision_need BETWEEN 0 AND 1),
    review_recommendation TEXT,
    FOREIGN KEY (frame_id) REFERENCES problem_frames(frame_id)
);

CREATE TABLE stakeholder_frames (
    stakeholder_frame_id TEXT PRIMARY KEY,
    frame_id TEXT NOT NULL,
    stakeholder_group TEXT NOT NULL,
    problem_definition_alignment REAL CHECK (problem_definition_alignment BETWEEN 0 AND 1),
    burden_visibility REAL CHECK (burden_visibility BETWEEN 0 AND 1),
    trust_sensitivity REAL CHECK (trust_sensitivity BETWEEN 0 AND 1),
    agency_visibility REAL CHECK (agency_visibility BETWEEN 0 AND 1),
    legitimacy_contribution REAL CHECK (legitimacy_contribution BETWEEN 0 AND 1),
    conflict_visibility REAL CHECK (conflict_visibility BETWEEN 0 AND 1),
    participation_quality REAL CHECK (participation_quality BETWEEN 0 AND 1),
    hidden_harm_risk REAL CHECK (hidden_harm_risk BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (frame_id) REFERENCES problem_frames(frame_id)
);

CREATE TABLE causal_models (
    causal_id TEXT PRIMARY KEY,
    frame_id TEXT NOT NULL,
    causal_story TEXT NOT NULL,
    causal_depth REAL CHECK (causal_depth BETWEEN 0 AND 1),
    mechanism_clarity REAL CHECK (mechanism_clarity BETWEEN 0 AND 1),
    feedback_awareness REAL CHECK (feedback_awareness BETWEEN 0 AND 1),
    incentive_awareness REAL CHECK (incentive_awareness BETWEEN 0 AND 1),
    delay_awareness REAL CHECK (delay_awareness BETWEEN 0 AND 1),
    evidence_strength REAL CHECK (evidence_strength BETWEEN 0 AND 1),
    alternative_cause_review REAL CHECK (alternative_cause_review BETWEEN 0 AND 1),
    linear_oversimplification_risk REAL CHECK (linear_oversimplification_risk BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (frame_id) REFERENCES problem_frames(frame_id)
);

CREATE TABLE assumption_audit (
    assumption_id TEXT PRIMARY KEY,
    frame_id TEXT NOT NULL,
    assumption_text TEXT NOT NULL,
    assumption_type TEXT NOT NULL,
    importance REAL CHECK (importance BETWEEN 0 AND 1),
    uncertainty REAL CHECK (uncertainty BETWEEN 0 AND 1),
    visibility REAL CHECK (visibility BETWEEN 0 AND 1),
    testability REAL CHECK (testability BETWEEN 0 AND 1),
    disconfirmation_quality REAL CHECK (disconfirmation_quality BETWEEN 0 AND 1),
    stakeholder_sensitivity REAL CHECK (stakeholder_sensitivity BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    assumption_risk REAL CHECK (assumption_risk BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (frame_id) REFERENCES problem_frames(frame_id)
);

CREATE TABLE alternative_frames (
    comparison_id TEXT PRIMARY KEY,
    primary_frame_id TEXT NOT NULL,
    rival_frame_id TEXT NOT NULL,
    comparison_focus TEXT NOT NULL,
    novelty_gain REAL CHECK (novelty_gain BETWEEN 0 AND 1),
    causal_gain REAL CHECK (causal_gain BETWEEN 0 AND 1),
    stakeholder_gain REAL CHECK (stakeholder_gain BETWEEN 0 AND 1),
    boundary_gain REAL CHECK (boundary_gain BETWEEN 0 AND 1),
    actionability_gain REAL CHECK (actionability_gain BETWEEN 0 AND 1),
    evidence_need REAL CHECK (evidence_need BETWEEN 0 AND 1),
    risk_of_confusion REAL CHECK (risk_of_confusion BETWEEN 0 AND 1),
    recommendation TEXT,
    FOREIGN KEY (primary_frame_id) REFERENCES problem_frames(frame_id),
    FOREIGN KEY (rival_frame_id) REFERENCES problem_frames(frame_id)
);

CREATE TABLE reframing_triggers (
    trigger_id TEXT PRIMARY KEY,
    frame_id TEXT NOT NULL,
    trigger_name TEXT NOT NULL,
    trigger_type TEXT NOT NULL,
    evidence_threshold REAL CHECK (evidence_threshold BETWEEN 0 AND 1),
    stakeholder_signal_strength REAL CHECK (stakeholder_signal_strength BETWEEN 0 AND 1),
    implementation_signal_strength REAL CHECK (implementation_signal_strength BETWEEN 0 AND 1),
    systems_signal_strength REAL CHECK (systems_signal_strength BETWEEN 0 AND 1),
    urgency REAL CHECK (urgency BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    decision_memory_need REAL CHECK (decision_memory_need BETWEEN 0 AND 1),
    trigger_quality REAL CHECK (trigger_quality BETWEEN 0 AND 1),
    action_if_triggered TEXT,
    FOREIGN KEY (frame_id) REFERENCES problem_frames(frame_id)
);

CREATE TABLE intervention_library (
    intervention_id TEXT PRIMARY KEY,
    intervention_name TEXT NOT NULL,
    target_framing_risk TEXT NOT NULL,
    process_cost REAL CHECK (process_cost BETWEEN 0 AND 1),
    implementation_complexity REAL CHECK (implementation_complexity BETWEEN 0 AND 1),
    boundary_gain REAL CHECK (boundary_gain BETWEEN 0 AND 1),
    causal_depth_gain REAL CHECK (causal_depth_gain BETWEEN 0 AND 1),
    stakeholder_gain REAL CHECK (stakeholder_gain BETWEEN 0 AND 1),
    assumption_clarity_gain REAL CHECK (assumption_clarity_gain BETWEEN 0 AND 1),
    reframing_capacity_gain REAL CHECK (reframing_capacity_gain BETWEEN 0 AND 1),
    decision_memory_gain REAL CHECK (decision_memory_gain BETWEEN 0 AND 1),
    political_safety_need REAL CHECK (political_safety_need BETWEEN 0 AND 1)
);

CREATE TABLE decision_memory (
    decision_id TEXT PRIMARY KEY,
    frame_id TEXT NOT NULL,
    decision_date TEXT,
    current_problem_statement TEXT,
    frame_origin TEXT,
    boundary_review TEXT,
    stakeholder_frame_review TEXT,
    causal_model TEXT,
    assumptions_tested TEXT,
    alternative_frames_considered TEXT,
    selected_problem_definition TEXT,
    reframing_trigger TEXT,
    archived_learning TEXT,
    FOREIGN KEY (frame_id) REFERENCES problem_frames(frame_id)
);

CREATE VIEW problem_framing_scores AS
SELECT
    frame_id,
    frame_name,
    frame_type,
    domain,
    ROUND(
      0.16 * boundary_breadth +
      0.15 * stakeholder_inclusion +
      0.15 * systems_awareness +
      0.16 * causal_depth +
      0.12 * assumption_clarity +
      0.13 * reframing_capacity +
      0.11 * actionability -
      0.10 * institutional_lock_in_risk -
      0.08 * political_convenience_risk,
      4
    ) AS problem_framing_score
FROM problem_frames;

CREATE VIEW frame_origin_scores AS
SELECT
    origin_id,
    frame_id,
    origin_source,
    ROUND(
      0.24 * authority_weight +
      0.24 * metric_dependency +
      0.24 * legacy_dependency +
      0.18 * origin_risk -
      0.16 * diagnostic_independence,
      4
    ) AS lock_in_risk
FROM frame_origins;

CREATE VIEW boundary_quality_scores AS
SELECT
    boundary_id,
    frame_id,
    boundary_name,
    boundary_type,
    ROUND(
      0.16 * stakeholder_visibility +
      0.15 * downstream_effect_visibility +
      0.14 * externality_visibility +
      0.14 * implementation_visibility +
      0.13 * time_horizon_quality +
      0.14 * hidden_dependency_visibility -
      0.12 * boundary_risk -
      0.08 * revision_need,
      4
    ) AS boundary_quality_score
FROM boundary_audit;

CREATE VIEW stakeholder_frame_scores AS
SELECT
    stakeholder_frame_id,
    frame_id,
    stakeholder_group,
    ROUND(
      0.12 * problem_definition_alignment +
      0.16 * burden_visibility +
      0.14 * trust_sensitivity +
      0.14 * agency_visibility +
      0.16 * legitimacy_contribution +
      0.12 * conflict_visibility +
      0.14 * participation_quality -
      0.12 * hidden_harm_risk,
      4
    ) AS stakeholder_frame_quality_score
FROM stakeholder_frames;

CREATE VIEW causal_quality_scores AS
SELECT
    causal_id,
    frame_id,
    causal_story,
    ROUND(
      0.18 * causal_depth +
      0.16 * mechanism_clarity +
      0.16 * feedback_awareness +
      0.14 * incentive_awareness +
      0.12 * delay_awareness +
      0.12 * evidence_strength +
      0.12 * alternative_cause_review -
      0.14 * linear_oversimplification_risk,
      4
    ) AS causal_quality_score
FROM causal_models;

CREATE VIEW assumption_priority_scores AS
SELECT
    assumption_id,
    frame_id,
    assumption_text,
    assumption_type,
    ROUND(
      0.18 * importance +
      0.16 * uncertainty +
      0.16 * stakeholder_sensitivity +
      0.14 * assumption_risk -
      0.12 * visibility -
      0.10 * testability -
      0.10 * disconfirmation_quality -
      0.08 * reversibility,
      4
    ) AS assumption_priority_score
FROM assumption_audit;

CREATE VIEW alternative_frame_scores AS
SELECT
    comparison_id,
    primary_frame_id,
    rival_frame_id,
    comparison_focus,
    ROUND(
      0.16 * novelty_gain +
      0.18 * causal_gain +
      0.16 * stakeholder_gain +
      0.16 * boundary_gain +
      0.12 * actionability_gain -
      0.10 * evidence_need -
      0.08 * risk_of_confusion,
      4
    ) AS comparison_value_score
FROM alternative_frames;

CREATE VIEW reframing_trigger_scores AS
SELECT
    trigger_id,
    frame_id,
    trigger_name,
    trigger_type,
    ROUND(
      0.16 * evidence_threshold +
      0.15 * stakeholder_signal_strength +
      0.15 * implementation_signal_strength +
      0.14 * systems_signal_strength +
      0.12 * urgency +
      0.10 * reversibility +
      0.10 * decision_memory_need +
      0.12 * trigger_quality,
      4
    ) AS trigger_strength_score
FROM reframing_triggers;

CREATE VIEW intervention_value_scores AS
SELECT
    intervention_id,
    intervention_name,
    target_framing_risk,
    ROUND(
      0.14 * boundary_gain +
      0.16 * causal_depth_gain +
      0.16 * stakeholder_gain +
      0.14 * assumption_clarity_gain +
      0.16 * reframing_capacity_gain +
      0.14 * decision_memory_gain -
      0.10 * process_cost -
      0.08 * implementation_complexity -
      0.08 * political_safety_need,
      4
    ) AS intervention_value_score
FROM intervention_library;
