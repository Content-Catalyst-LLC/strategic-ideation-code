-- Advanced SQL schema for mental-model analysis in strategic thinking.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS mental_model_profile_scores;
DROP VIEW IF EXISTS causal_frame_scores;
DROP VIEW IF EXISTS artifact_lock_in_scores;
DROP VIEW IF EXISTS evidence_revision_priorities;
DROP VIEW IF EXISTS scenario_stress_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS scenario_stress_tests;
DROP TABLE IF EXISTS model_audit_items;
DROP TABLE IF EXISTS evidence_feedback;
DROP TABLE IF EXISTS institutional_artifacts;
DROP TABLE IF EXISTS causal_frames;
DROP TABLE IF EXISTS mental_models;

CREATE TABLE mental_models (
    model_id TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    dominant_frame TEXT NOT NULL,
    systems_richness REAL CHECK (systems_richness BETWEEN 0 AND 1),
    probabilistic_depth REAL CHECK (probabilistic_depth BETWEEN 0 AND 1),
    model_flexibility REAL CHECK (model_flexibility BETWEEN 0 AND 1),
    model_plurality REAL CHECK (model_plurality BETWEEN 0 AND 1),
    revision_capacity REAL CHECK (revision_capacity BETWEEN 0 AND 1),
    institutional_embedding REAL CHECK (institutional_embedding BETWEEN 0 AND 1),
    ethical_visibility REAL CHECK (ethical_visibility BETWEEN 0 AND 1),
    stakeholder_visibility REAL CHECK (stakeholder_visibility BETWEEN 0 AND 1),
    evidence_responsiveness REAL CHECK (evidence_responsiveness BETWEEN 0 AND 1)
);

CREATE TABLE causal_frames (
    frame_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    causal_assumption TEXT NOT NULL,
    causal_type TEXT NOT NULL,
    environment_fit REAL CHECK (environment_fit BETWEEN 0 AND 1),
    feedback_awareness REAL CHECK (feedback_awareness BETWEEN 0 AND 1),
    delay_awareness REAL CHECK (delay_awareness BETWEEN 0 AND 1),
    nonlinearity_awareness REAL CHECK (nonlinearity_awareness BETWEEN 0 AND 1),
    second_order_awareness REAL CHECK (second_order_awareness BETWEEN 0 AND 1),
    blind_spot_risk REAL CHECK (blind_spot_risk BETWEEN 0 AND 1),
    FOREIGN KEY (model_id) REFERENCES mental_models(model_id)
);

CREATE TABLE institutional_artifacts (
    artifact_id TEXT PRIMARY KEY,
    artifact_name TEXT NOT NULL,
    artifact_type TEXT NOT NULL,
    encoded_model TEXT NOT NULL,
    measurement_bias REAL CHECK (measurement_bias BETWEEN 0 AND 1),
    lock_in_strength REAL CHECK (lock_in_strength BETWEEN 0 AND 1),
    revision_pathway REAL CHECK (revision_pathway BETWEEN 0 AND 1),
    stakeholder_visibility REAL CHECK (stakeholder_visibility BETWEEN 0 AND 1),
    ethical_visibility REAL CHECK (ethical_visibility BETWEEN 0 AND 1),
    strategic_risk REAL CHECK (strategic_risk BETWEEN 0 AND 1)
);

CREATE TABLE evidence_feedback (
    evidence_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    evidence_summary TEXT NOT NULL,
    evidence_type TEXT NOT NULL,
    disconfirmation_strength REAL CHECK (disconfirmation_strength BETWEEN 0 AND 1),
    evidence_quality REAL CHECK (evidence_quality BETWEEN 0 AND 1),
    model_response TEXT,
    revision_required INTEGER CHECK (revision_required IN (0, 1)),
    affected_layer TEXT,
    FOREIGN KEY (model_id) REFERENCES mental_models(model_id)
);

CREATE TABLE model_audit_items (
    audit_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    audit_dimension TEXT NOT NULL,
    audit_question TEXT NOT NULL,
    current_score REAL CHECK (current_score BETWEEN 0 AND 1),
    desired_score REAL CHECK (desired_score BETWEEN 0 AND 1),
    priority TEXT CHECK (priority IN ('low', 'moderate', 'high')),
    review_method TEXT,
    FOREIGN KEY (model_id) REFERENCES mental_models(model_id)
);

CREATE TABLE scenario_stress_tests (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    model_id TEXT NOT NULL,
    stress_condition TEXT NOT NULL,
    performance_under_stress REAL CHECK (performance_under_stress BETWEEN 0 AND 1),
    revision_speed REAL CHECK (revision_speed BETWEEN 0 AND 1),
    blind_spot_exposure REAL CHECK (blind_spot_exposure BETWEEN 0 AND 1),
    strategic_robustness REAL CHECK (strategic_robustness BETWEEN 0 AND 1),
    FOREIGN KEY (model_id) REFERENCES mental_models(model_id)
);

CREATE TABLE decision_memory (
    decision_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    decision_date TEXT,
    model_revision_summary TEXT NOT NULL,
    evidence_trigger TEXT,
    previous_assumption TEXT,
    revised_assumption TEXT,
    rejected_interpretations TEXT,
    next_review_trigger TEXT,
    FOREIGN KEY (model_id) REFERENCES mental_models(model_id)
);

CREATE VIEW mental_model_profile_scores AS
SELECT
    model_id,
    model_name,
    dominant_frame,
    ROUND(
      0.17 * systems_richness +
      0.13 * probabilistic_depth +
      0.16 * model_flexibility +
      0.14 * model_plurality +
      0.16 * revision_capacity -
      0.08 * institutional_embedding +
      0.12 * ethical_visibility +
      0.10 * stakeholder_visibility +
      0.10 * evidence_responsiveness,
      4
    ) AS adaptive_model_score
FROM mental_models;

CREATE VIEW causal_frame_scores AS
SELECT
    frame_id,
    model_id,
    causal_type,
    ROUND(
      0.24 * environment_fit +
      0.20 * feedback_awareness +
      0.18 * delay_awareness +
      0.18 * nonlinearity_awareness +
      0.20 * second_order_awareness -
      0.18 * blind_spot_risk,
      4
    ) AS causal_adequacy_score
FROM causal_frames;

CREATE VIEW artifact_lock_in_scores AS
SELECT
    artifact_id,
    artifact_name,
    artifact_type,
    encoded_model,
    ROUND(
      0.24 * measurement_bias +
      0.28 * lock_in_strength +
      0.18 * (1.0 - revision_pathway) +
      0.14 * (1.0 - stakeholder_visibility) +
      0.16 * (1.0 - ethical_visibility),
      4
    ) AS lock_in_risk
FROM institutional_artifacts;

CREATE VIEW evidence_revision_priorities AS
SELECT
    evidence_id,
    model_id,
    evidence_type,
    ROUND(
      0.40 * disconfirmation_strength +
      0.30 * evidence_quality +
      0.20 * revision_required +
      0.10 * CASE
        WHEN model_response IN ('treated_as_exception', 'delayed_review', 'contested') THEN 1.0
        ELSE 0.0
      END,
      4
    ) AS revision_priority,
    affected_layer,
    evidence_summary
FROM evidence_feedback;

CREATE VIEW scenario_stress_scores AS
SELECT
    scenario_id,
    scenario_name,
    model_id,
    stress_condition,
    ROUND(
      0.34 * performance_under_stress +
      0.24 * revision_speed -
      0.22 * blind_spot_exposure +
      0.30 * strategic_robustness,
      4
    ) AS stress_score
FROM scenario_stress_tests;
