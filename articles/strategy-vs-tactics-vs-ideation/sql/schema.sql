-- Advanced SQL schema for strategy, tactics, ideation, feedback, and decision memory.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS initiative_weighted_scores;
DROP VIEW IF EXISTS tactical_translation_scores;
DROP VIEW IF EXISTS feedback_priority_queue;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS feedback_events;
DROP TABLE IF EXISTS tactical_actions;
DROP TABLE IF EXISTS assumptions;
DROP TABLE IF EXISTS evaluations;
DROP TABLE IF EXISTS criteria;
DROP TABLE IF EXISTS strategic_initiatives;
DROP TABLE IF EXISTS layer_contexts;

CREATE TABLE layer_contexts (
    context_id TEXT PRIMARY KEY,
    context_name TEXT NOT NULL,
    context_type TEXT NOT NULL,
    ideation_quality REAL CHECK (ideation_quality BETWEEN 0 AND 1),
    strategic_clarity REAL CHECK (strategic_clarity BETWEEN 0 AND 1),
    tactical_alignment REAL CHECK (tactical_alignment BETWEEN 0 AND 1),
    feedback_quality REAL CHECK (feedback_quality BETWEEN 0 AND 1),
    adaptive_learning REAL CHECK (adaptive_learning BETWEEN 0 AND 1),
    decision_memory REAL CHECK (decision_memory BETWEEN 0 AND 1),
    ethical_legitimacy REAL CHECK (ethical_legitimacy BETWEEN 0 AND 1)
);

CREATE TABLE strategic_initiatives (
    initiative_id TEXT PRIMARY KEY,
    initiative_name TEXT NOT NULL,
    problem_frame TEXT NOT NULL,
    strategic_priority TEXT NOT NULL,
    primary_layer TEXT CHECK (primary_layer IN ('ideation', 'strategy', 'tactics', 'learning', 'ethics')),
    current_status TEXT CHECK (current_status IN ('planned', 'active', 'review', 'paused', 'retired')),
    strategic_fit REAL CHECK (strategic_fit BETWEEN 0 AND 1),
    implementation_feasibility REAL CHECK (implementation_feasibility BETWEEN 0 AND 1),
    systems_leverage REAL CHECK (systems_leverage BETWEEN 0 AND 1),
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    ethical_legitimacy REAL CHECK (ethical_legitimacy BETWEEN 0 AND 1),
    uncertainty REAL CHECK (uncertainty BETWEEN 0 AND 1)
);

CREATE TABLE criteria (
    criterion_id TEXT PRIMARY KEY,
    criterion_name TEXT NOT NULL,
    weight REAL NOT NULL CHECK (weight >= 0),
    description TEXT
);

CREATE TABLE evaluations (
    evaluation_id TEXT PRIMARY KEY,
    initiative_id TEXT NOT NULL,
    criterion_id TEXT NOT NULL,
    score REAL NOT NULL CHECK (score BETWEEN 0 AND 1),
    evaluator_role TEXT,
    evidence_note TEXT,
    evaluated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (initiative_id) REFERENCES strategic_initiatives(initiative_id),
    FOREIGN KEY (criterion_id) REFERENCES criteria(criterion_id)
);

CREATE TABLE assumptions (
    assumption_id TEXT PRIMARY KEY,
    initiative_id TEXT NOT NULL,
    assumption_text TEXT NOT NULL,
    layer TEXT CHECK (layer IN ('ideation', 'strategy', 'tactics', 'learning', 'ethics')),
    confidence REAL CHECK (confidence BETWEEN 0 AND 1),
    criticality REAL CHECK (criticality BETWEEN 0 AND 1),
    test_method TEXT,
    evidence_status TEXT CHECK (evidence_status IN ('untested', 'partial', 'strong', 'contested')),
    FOREIGN KEY (initiative_id) REFERENCES strategic_initiatives(initiative_id)
);

CREATE TABLE tactical_actions (
    tactic_id TEXT PRIMARY KEY,
    initiative_id TEXT NOT NULL,
    tactic_name TEXT NOT NULL,
    owner_group TEXT NOT NULL,
    alignment_to_strategy REAL CHECK (alignment_to_strategy BETWEEN 0 AND 1),
    execution_readiness REAL CHECK (execution_readiness BETWEEN 0 AND 1),
    resource_fit REAL CHECK (resource_fit BETWEEN 0 AND 1),
    feedback_capture REAL CHECK (feedback_capture BETWEEN 0 AND 1),
    learning_routing REAL CHECK (learning_routing BETWEEN 0 AND 1),
    delivery_risk REAL CHECK (delivery_risk BETWEEN 0 AND 1),
    FOREIGN KEY (initiative_id) REFERENCES strategic_initiatives(initiative_id)
);

CREATE TABLE feedback_events (
    feedback_id TEXT PRIMARY KEY,
    initiative_id TEXT NOT NULL,
    tactic_id TEXT,
    feedback_summary TEXT NOT NULL,
    observed_layer TEXT CHECK (observed_layer IN ('ideation', 'strategy', 'tactics', 'learning', 'ethics')),
    affected_layer TEXT CHECK (affected_layer IN ('ideation', 'strategy', 'tactics', 'learning', 'ethics')),
    severity REAL CHECK (severity BETWEEN 0 AND 1),
    signal_strength REAL CHECK (signal_strength BETWEEN 0 AND 1),
    recommended_routing TEXT,
    FOREIGN KEY (initiative_id) REFERENCES strategic_initiatives(initiative_id),
    FOREIGN KEY (tactic_id) REFERENCES tactical_actions(tactic_id)
);

CREATE TABLE decision_memory (
    decision_id TEXT PRIMARY KEY,
    initiative_id TEXT NOT NULL,
    decision_date TEXT,
    decision_summary TEXT NOT NULL,
    chosen_option TEXT,
    rejected_options TEXT,
    rationale TEXT,
    assumptions_to_revisit TEXT,
    next_review_trigger TEXT,
    FOREIGN KEY (initiative_id) REFERENCES strategic_initiatives(initiative_id)
);

CREATE VIEW initiative_weighted_scores AS
SELECT
    initiative_id,
    initiative_name,
    primary_layer,
    ROUND(
      0.22 * strategic_fit +
      0.14 * implementation_feasibility +
      0.18 * systems_leverage +
      0.14 * learning_value +
      0.18 * ethical_legitimacy -
      0.08 * uncertainty,
      4
    ) AS weighted_score
FROM strategic_initiatives;

CREATE VIEW tactical_translation_scores AS
SELECT
    tactic_id,
    initiative_id,
    tactic_name,
    owner_group,
    ROUND(
      0.26 * alignment_to_strategy +
      0.20 * execution_readiness +
      0.16 * resource_fit +
      0.18 * feedback_capture +
      0.20 * learning_routing -
      0.12 * delivery_risk,
      4
    ) AS translation_score
FROM tactical_actions;

CREATE VIEW feedback_priority_queue AS
SELECT
    feedback_id,
    initiative_id,
    tactic_id,
    affected_layer,
    ROUND(severity * signal_strength, 4) AS priority_score,
    recommended_routing,
    feedback_summary
FROM feedback_events
ORDER BY priority_score DESC;
