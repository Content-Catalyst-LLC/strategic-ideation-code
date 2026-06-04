-- Advanced SQL schema for lateral thinking in strategy.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS lateral_context_profiles;
DROP VIEW IF EXISTS frame_rigidity_risks;
DROP VIEW IF EXISTS dominant_frame_scores;
DROP VIEW IF EXISTS assumption_challenge_priorities;
DROP VIEW IF EXISTS lateral_move_scores;
DROP VIEW IF EXISTS reframed_problem_scores;
DROP VIEW IF EXISTS convergence_integration_scores;
DROP VIEW IF EXISTS stakeholder_legitimacy_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS stakeholder_legitimacy;
DROP TABLE IF EXISTS convergence_integration;
DROP TABLE IF EXISTS reframed_problems;
DROP TABLE IF EXISTS lateral_moves;
DROP TABLE IF EXISTS assumption_register;
DROP TABLE IF EXISTS dominant_frames;
DROP TABLE IF EXISTS lateral_contexts;

CREATE TABLE lateral_contexts (
    context_id TEXT PRIMARY KEY,
    context_name TEXT NOT NULL,
    context_type TEXT NOT NULL,
    frame_rigidity REAL CHECK (frame_rigidity BETWEEN 0 AND 1),
    provocation_strength REAL CHECK (provocation_strength BETWEEN 0 AND 1),
    analogical_distance REAL CHECK (analogical_distance BETWEEN 0 AND 1),
    random_entry_capacity REAL CHECK (random_entry_capacity BETWEEN 0 AND 1),
    reversal_capacity REAL CHECK (reversal_capacity BETWEEN 0 AND 1),
    challenge_quality REAL CHECK (challenge_quality BETWEEN 0 AND 1),
    convergence_discipline REAL CHECK (convergence_discipline BETWEEN 0 AND 1),
    systems_integration REAL CHECK (systems_integration BETWEEN 0 AND 1),
    stakeholder_legitimacy REAL CHECK (stakeholder_legitimacy BETWEEN 0 AND 1),
    political_safety REAL CHECK (political_safety BETWEEN 0 AND 1),
    transformational_potential REAL CHECK (transformational_potential BETWEEN 0 AND 1)
);

CREATE TABLE dominant_frames (
    frame_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    frame_name TEXT NOT NULL,
    frame_origin TEXT NOT NULL,
    problem_clarity REAL CHECK (problem_clarity BETWEEN 0 AND 1),
    assumption_visibility REAL CHECK (assumption_visibility BETWEEN 0 AND 1),
    metric_lock_in REAL CHECK (metric_lock_in BETWEEN 0 AND 1),
    category_rigidity REAL CHECK (category_rigidity BETWEEN 0 AND 1),
    stakeholder_exclusion REAL CHECK (stakeholder_exclusion BETWEEN 0 AND 1),
    system_boundary_quality REAL CHECK (system_boundary_quality BETWEEN 0 AND 1),
    frame_obsolescence_risk REAL CHECK (frame_obsolescence_risk BETWEEN 0 AND 1),
    FOREIGN KEY (context_id) REFERENCES lateral_contexts(context_id)
);

CREATE TABLE assumption_register (
    assumption_id TEXT PRIMARY KEY,
    frame_id TEXT NOT NULL,
    context_id TEXT NOT NULL,
    assumption_text TEXT NOT NULL,
    assumption_type TEXT NOT NULL,
    evidence_strength REAL CHECK (evidence_strength BETWEEN 0 AND 1),
    strategic_importance REAL CHECK (strategic_importance BETWEEN 0 AND 1),
    challenge_potential REAL CHECK (challenge_potential BETWEEN 0 AND 1),
    stakeholder_burden_visibility REAL CHECK (stakeholder_burden_visibility BETWEEN 0 AND 1),
    power_protection_risk REAL CHECK (power_protection_risk BETWEEN 0 AND 1),
    revision_priority TEXT,
    FOREIGN KEY (frame_id) REFERENCES dominant_frames(frame_id),
    FOREIGN KEY (context_id) REFERENCES lateral_contexts(context_id)
);

CREATE TABLE lateral_moves (
    move_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    frame_id TEXT NOT NULL,
    technique TEXT NOT NULL,
    move_name TEXT NOT NULL,
    frame_disruption REAL CHECK (frame_disruption BETWEEN 0 AND 1),
    strategic_relevance REAL CHECK (strategic_relevance BETWEEN 0 AND 1),
    reconstruction_quality REAL CHECK (reconstruction_quality BETWEEN 0 AND 1),
    evidence_pathway REAL CHECK (evidence_pathway BETWEEN 0 AND 1),
    stakeholder_fit REAL CHECK (stakeholder_fit BETWEEN 0 AND 1),
    systems_fit REAL CHECK (systems_fit BETWEEN 0 AND 1),
    novelty_value REAL CHECK (novelty_value BETWEEN 0 AND 1),
    drift_risk REAL CHECK (drift_risk BETWEEN 0 AND 1),
    FOREIGN KEY (context_id) REFERENCES lateral_contexts(context_id),
    FOREIGN KEY (frame_id) REFERENCES dominant_frames(frame_id)
);

CREATE TABLE reframed_problems (
    reframe_id TEXT PRIMARY KEY,
    move_id TEXT NOT NULL,
    context_id TEXT NOT NULL,
    reframed_problem TEXT NOT NULL,
    problem_clarity REAL CHECK (problem_clarity BETWEEN 0 AND 1),
    structural_shift REAL CHECK (structural_shift BETWEEN 0 AND 1),
    stakeholder_visibility REAL CHECK (stakeholder_visibility BETWEEN 0 AND 1),
    systems_alignment REAL CHECK (systems_alignment BETWEEN 0 AND 1),
    decision_value REAL CHECK (decision_value BETWEEN 0 AND 1),
    testability REAL CHECK (testability BETWEEN 0 AND 1),
    implementation_pathway_quality REAL CHECK (implementation_pathway_quality BETWEEN 0 AND 1),
    FOREIGN KEY (move_id) REFERENCES lateral_moves(move_id),
    FOREIGN KEY (context_id) REFERENCES lateral_contexts(context_id)
);

CREATE TABLE convergence_integration (
    integration_id TEXT PRIMARY KEY,
    reframe_id TEXT NOT NULL,
    context_id TEXT NOT NULL,
    criteria_clarity REAL CHECK (criteria_clarity BETWEEN 0 AND 1),
    evidence_readiness REAL CHECK (evidence_readiness BETWEEN 0 AND 1),
    prototype_readiness REAL CHECK (prototype_readiness BETWEEN 0 AND 1),
    risk_review_quality REAL CHECK (risk_review_quality BETWEEN 0 AND 1),
    stakeholder_review_quality REAL CHECK (stakeholder_review_quality BETWEEN 0 AND 1),
    systems_review_quality REAL CHECK (systems_review_quality BETWEEN 0 AND 1),
    implementation_readiness REAL CHECK (implementation_readiness BETWEEN 0 AND 1),
    decision_memory_quality REAL CHECK (decision_memory_quality BETWEEN 0 AND 1),
    FOREIGN KEY (reframe_id) REFERENCES reframed_problems(reframe_id),
    FOREIGN KEY (context_id) REFERENCES lateral_contexts(context_id)
);

CREATE TABLE stakeholder_legitimacy (
    review_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    reframe_id TEXT NOT NULL,
    stakeholder_group TEXT NOT NULL,
    inclusion_level REAL CHECK (inclusion_level BETWEEN 0 AND 1),
    burden_visibility REAL CHECK (burden_visibility BETWEEN 0 AND 1),
    knowledge_recognition REAL CHECK (knowledge_recognition BETWEEN 0 AND 1),
    interpretive_trust REAL CHECK (interpretive_trust BETWEEN 0 AND 1),
    political_safety REAL CHECK (political_safety BETWEEN 0 AND 1),
    legitimacy_signal REAL CHECK (legitimacy_signal BETWEEN 0 AND 1),
    power_challenge_risk REAL CHECK (power_challenge_risk BETWEEN 0 AND 1),
    FOREIGN KEY (context_id) REFERENCES lateral_contexts(context_id),
    FOREIGN KEY (reframe_id) REFERENCES reframed_problems(reframe_id)
);

CREATE TABLE decision_memory (
    decision_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    frame_id TEXT,
    move_id TEXT,
    reframe_id TEXT,
    decision_date TEXT,
    dominant_frame TEXT,
    assumptions_challenged TEXT,
    lateral_technique_used TEXT,
    reframe_summary TEXT,
    evidence_considered TEXT,
    stakeholders_consulted TEXT,
    convergence_decision TEXT,
    revision_trigger TEXT,
    FOREIGN KEY (context_id) REFERENCES lateral_contexts(context_id),
    FOREIGN KEY (frame_id) REFERENCES dominant_frames(frame_id),
    FOREIGN KEY (move_id) REFERENCES lateral_moves(move_id),
    FOREIGN KEY (reframe_id) REFERENCES reframed_problems(reframe_id)
);

CREATE VIEW lateral_context_profiles AS
SELECT
    context_id,
    context_name,
    context_type,
    ROUND(
      -0.14 * frame_rigidity +
      0.14 * provocation_strength +
      0.12 * analogical_distance +
      0.09 * random_entry_capacity +
      0.10 * reversal_capacity +
      0.10 * challenge_quality +
      0.14 * convergence_discipline +
      0.12 * systems_integration +
      0.08 * stakeholder_legitimacy +
      0.07 * political_safety +
      0.14 * transformational_potential,
      4
    ) AS lateral_profile_score
FROM lateral_contexts;

CREATE VIEW frame_rigidity_risks AS
SELECT
    context_id,
    context_name,
    ROUND(frame_rigidity * (1.0 - provocation_strength), 4) AS frame_rigidity_risk,
    ROUND(transformational_potential * (1.0 - convergence_discipline), 4) AS drift_risk,
    ROUND(MAX(0.0, 0.60 - stakeholder_legitimacy), 4) AS legitimacy_gap,
    ROUND(MAX(0.0, 0.55 - political_safety), 4) AS political_safety_gap
FROM lateral_contexts;

CREATE VIEW dominant_frame_scores AS
SELECT
    frame_id,
    context_id,
    frame_name,
    ROUND(
      0.18 * problem_clarity +
      0.18 * assumption_visibility -
      0.16 * metric_lock_in -
      0.16 * category_rigidity -
      0.14 * stakeholder_exclusion +
      0.18 * system_boundary_quality -
      0.10 * frame_obsolescence_risk,
      4
    ) AS frame_quality_score
FROM dominant_frames;

CREATE VIEW assumption_challenge_priorities AS
SELECT
    assumption_id,
    frame_id,
    context_id,
    assumption_text,
    ROUND(
      0.24 * strategic_importance +
      0.24 * challenge_potential +
      0.18 * (1.0 - evidence_strength) +
      0.16 * power_protection_risk +
      0.10 * (1.0 - stakeholder_burden_visibility),
      4
    ) AS challenge_priority
FROM assumption_register;

CREATE VIEW lateral_move_scores AS
SELECT
    move_id,
    context_id,
    frame_id,
    technique,
    move_name,
    ROUND(
      0.16 * frame_disruption +
      0.18 * strategic_relevance +
      0.16 * reconstruction_quality +
      0.12 * evidence_pathway +
      0.12 * stakeholder_fit +
      0.12 * systems_fit +
      0.10 * novelty_value -
      0.14 * drift_risk,
      4
    ) AS lateral_move_score
FROM lateral_moves;

CREATE VIEW reframed_problem_scores AS
SELECT
    reframe_id,
    move_id,
    context_id,
    reframed_problem,
    ROUND(
      0.16 * problem_clarity +
      0.18 * structural_shift +
      0.14 * stakeholder_visibility +
      0.16 * systems_alignment +
      0.14 * decision_value +
      0.12 * testability +
      0.10 * implementation_pathway_quality,
      4
    ) AS reframe_quality_score
FROM reframed_problems;

CREATE VIEW convergence_integration_scores AS
SELECT
    integration_id,
    reframe_id,
    context_id,
    ROUND(
      0.14 * criteria_clarity +
      0.14 * evidence_readiness +
      0.14 * prototype_readiness +
      0.14 * risk_review_quality +
      0.14 * stakeholder_review_quality +
      0.14 * systems_review_quality +
      0.12 * implementation_readiness +
      0.10 * decision_memory_quality,
      4
    ) AS convergence_integration_score
FROM convergence_integration;

CREATE VIEW stakeholder_legitimacy_scores AS
SELECT
    review_id,
    context_id,
    reframe_id,
    stakeholder_group,
    ROUND(
      0.14 * inclusion_level +
      0.16 * burden_visibility +
      0.16 * knowledge_recognition +
      0.14 * interpretive_trust +
      0.14 * political_safety +
      0.16 * legitimacy_signal -
      0.10 * power_challenge_risk,
      4
    ) AS stakeholder_legitimacy_score
FROM stakeholder_legitimacy;
