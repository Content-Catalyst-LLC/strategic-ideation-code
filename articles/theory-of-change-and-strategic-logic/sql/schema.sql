-- Advanced SQL schema for theory of change and strategic logic.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS strategic_logic_scores;
DROP VIEW IF EXISTS theory_link_risk_scores;
DROP VIEW IF EXISTS assumption_link_scores;
DROP VIEW IF EXISTS evidence_match_scores;
DROP VIEW IF EXISTS actor_response_scores;
DROP VIEW IF EXISTS system_feedback_scores;
DROP VIEW IF EXISTS outcome_sequence_scores;
DROP VIEW IF EXISTS prototype_test_scores;
DROP VIEW IF EXISTS implementation_learning_scores;
DROP VIEW IF EXISTS revision_trigger_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS revision_triggers;
DROP TABLE IF EXISTS implementation_learning;
DROP TABLE IF EXISTS prototype_tests;
DROP TABLE IF EXISTS outcome_sequence;
DROP TABLE IF EXISTS system_feedback;
DROP TABLE IF EXISTS actor_response;
DROP TABLE IF EXISTS evidence_sources;
DROP TABLE IF EXISTS assumptions;
DROP TABLE IF EXISTS theory_links;
DROP TABLE IF EXISTS strategic_ideas;

CREATE TABLE strategic_ideas (
    idea_id TEXT PRIMARY KEY,
    idea_name TEXT NOT NULL,
    idea_type TEXT NOT NULL,
    domain TEXT NOT NULL,
    problem_frame_quality REAL CHECK (problem_frame_quality BETWEEN 0 AND 1),
    mechanism_clarity REAL CHECK (mechanism_clarity BETWEEN 0 AND 1),
    strategic_alignment REAL CHECK (strategic_alignment BETWEEN 0 AND 1),
    implementation_feasibility REAL CHECK (implementation_feasibility BETWEEN 0 AND 1),
    stakeholder_legitimacy REAL CHECK (stakeholder_legitimacy BETWEEN 0 AND 1),
    system_complexity REAL CHECK (system_complexity BETWEEN 0 AND 1),
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE theory_links (
    link_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    link_stage TEXT NOT NULL,
    from_element TEXT NOT NULL,
    to_element TEXT NOT NULL,
    link_description TEXT,
    mechanism_clarity REAL CHECK (mechanism_clarity BETWEEN 0 AND 1),
    evidence_strength REAL CHECK (evidence_strength BETWEEN 0 AND 1),
    actor_dependency REAL CHECK (actor_dependency BETWEEN 0 AND 1),
    capacity_dependency REAL CHECK (capacity_dependency BETWEEN 0 AND 1),
    system_dependency REAL CHECK (system_dependency BETWEEN 0 AND 1),
    ethical_dependency REAL CHECK (ethical_dependency BETWEEN 0 AND 1),
    failure_consequence REAL CHECK (failure_consequence BETWEEN 0 AND 1),
    testability REAL CHECK (testability BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id)
);

CREATE TABLE assumptions (
    assumption_id TEXT PRIMARY KEY,
    link_id TEXT NOT NULL,
    idea_id TEXT NOT NULL,
    assumption_statement TEXT NOT NULL,
    assumption_type TEXT NOT NULL,
    criticality REAL CHECK (criticality BETWEEN 0 AND 1),
    uncertainty REAL CHECK (uncertainty BETWEEN 0 AND 1),
    evidence_strength REAL CHECK (evidence_strength BETWEEN 0 AND 1),
    evidence_relevance REAL CHECK (evidence_relevance BETWEEN 0 AND 1),
    evidence_transferability REAL CHECK (evidence_transferability BETWEEN 0 AND 1),
    testability REAL CHECK (testability BETWEEN 0 AND 1),
    stakeholder_sensitivity REAL CHECK (stakeholder_sensitivity BETWEEN 0 AND 1),
    system_sensitivity REAL CHECK (system_sensitivity BETWEEN 0 AND 1),
    decision_owner TEXT,
    review_action TEXT,
    FOREIGN KEY (link_id) REFERENCES theory_links(link_id),
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id)
);

CREATE TABLE evidence_sources (
    evidence_id TEXT PRIMARY KEY,
    link_id TEXT NOT NULL,
    assumption_id TEXT NOT NULL,
    evidence_type TEXT NOT NULL,
    evidence_description TEXT,
    reliability REAL CHECK (reliability BETWEEN 0 AND 1),
    relevance REAL CHECK (relevance BETWEEN 0 AND 1),
    transferability REAL CHECK (transferability BETWEEN 0 AND 1),
    timeliness REAL CHECK (timeliness BETWEEN 0 AND 1),
    bias_risk REAL CHECK (bias_risk BETWEEN 0 AND 1),
    coverage_quality REAL CHECK (coverage_quality BETWEEN 0 AND 1),
    interpretation_quality REAL CHECK (interpretation_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (link_id) REFERENCES theory_links(link_id),
    FOREIGN KEY (assumption_id) REFERENCES assumptions(assumption_id)
);

CREATE TABLE actor_response (
    actor_id TEXT PRIMARY KEY,
    link_id TEXT NOT NULL,
    idea_id TEXT NOT NULL,
    actor_group TEXT NOT NULL,
    expected_response TEXT NOT NULL,
    response_dependency REAL CHECK (response_dependency BETWEEN 0 AND 1),
    incentive_alignment REAL CHECK (incentive_alignment BETWEEN 0 AND 1),
    trust_condition REAL CHECK (trust_condition BETWEEN 0 AND 1),
    capacity_condition REAL CHECK (capacity_condition BETWEEN 0 AND 1),
    burden_risk REAL CHECK (burden_risk BETWEEN 0 AND 1),
    resistance_risk REAL CHECK (resistance_risk BETWEEN 0 AND 1),
    participation_quality REAL CHECK (participation_quality BETWEEN 0 AND 1),
    knowledge_value REAL CHECK (knowledge_value BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (link_id) REFERENCES theory_links(link_id),
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id)
);

CREATE TABLE system_feedback (
    feedback_id TEXT PRIMARY KEY,
    link_id TEXT NOT NULL,
    idea_id TEXT NOT NULL,
    feedback_pattern TEXT NOT NULL,
    feedback_type TEXT NOT NULL,
    feedback_risk REAL CHECK (feedback_risk BETWEEN 0 AND 1),
    adaptation_risk REAL CHECK (adaptation_risk BETWEEN 0 AND 1),
    delay_risk REAL CHECK (delay_risk BETWEEN 0 AND 1),
    burden_shift_risk REAL CHECK (burden_shift_risk BETWEEN 0 AND 1),
    metric_gaming_risk REAL CHECK (metric_gaming_risk BETWEEN 0 AND 1),
    context_dependency REAL CHECK (context_dependency BETWEEN 0 AND 1),
    monitoring_quality REAL CHECK (monitoring_quality BETWEEN 0 AND 1),
    leverage_relevance REAL CHECK (leverage_relevance BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (link_id) REFERENCES theory_links(link_id),
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id)
);

CREATE TABLE outcome_sequence (
    sequence_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    outcome_stage TEXT NOT NULL,
    outcome_name TEXT NOT NULL,
    time_horizon TEXT NOT NULL,
    precondition_quality REAL CHECK (precondition_quality BETWEEN 0 AND 1),
    indicator_quality REAL CHECK (indicator_quality BETWEEN 0 AND 1),
    measurement_feasibility REAL CHECK (measurement_feasibility BETWEEN 0 AND 1),
    actor_dependency REAL CHECK (actor_dependency BETWEEN 0 AND 1),
    system_dependency REAL CHECK (system_dependency BETWEEN 0 AND 1),
    impact_claim_risk REAL CHECK (impact_claim_risk BETWEEN 0 AND 1),
    review_cadence_quality REAL CHECK (review_cadence_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id)
);

CREATE TABLE prototype_tests (
    prototype_id TEXT PRIMARY KEY,
    link_id TEXT NOT NULL,
    idea_id TEXT NOT NULL,
    prototype_name TEXT NOT NULL,
    prototype_type TEXT NOT NULL,
    link_fit REAL CHECK (link_fit BETWEEN 0 AND 1),
    learning_speed REAL CHECK (learning_speed BETWEEN 0 AND 1),
    learning_depth REAL CHECK (learning_depth BETWEEN 0 AND 1),
    realism REAL CHECK (realism BETWEEN 0 AND 1),
    stakeholder_inclusion REAL CHECK (stakeholder_inclusion BETWEEN 0 AND 1),
    scale_signal_quality REAL CHECK (scale_signal_quality BETWEEN 0 AND 1),
    cost_efficiency REAL CHECK (cost_efficiency BETWEEN 0 AND 1),
    ethical_safety REAL CHECK (ethical_safety BETWEEN 0 AND 1),
    decision_usefulness REAL CHECK (decision_usefulness BETWEEN 0 AND 1),
    success_threshold REAL CHECK (success_threshold BETWEEN 0 AND 1),
    decision_if_failed TEXT,
    FOREIGN KEY (link_id) REFERENCES theory_links(link_id),
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id)
);

CREATE TABLE implementation_learning (
    learning_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    learning_focus TEXT NOT NULL,
    review_stage TEXT NOT NULL,
    evidence_quality REAL CHECK (evidence_quality BETWEEN 0 AND 1),
    feedback_quality REAL CHECK (feedback_quality BETWEEN 0 AND 1),
    decision_linkage REAL CHECK (decision_linkage BETWEEN 0 AND 1),
    governance_owner_clarity REAL CHECK (governance_owner_clarity BETWEEN 0 AND 1),
    revision_capacity REAL CHECK (revision_capacity BETWEEN 0 AND 1),
    stakeholder_visibility REAL CHECK (stakeholder_visibility BETWEEN 0 AND 1),
    timeliness REAL CHECK (timeliness BETWEEN 0 AND 1),
    learning_memory_quality REAL CHECK (learning_memory_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id)
);

CREATE TABLE revision_triggers (
    trigger_id TEXT PRIMARY KEY,
    link_id TEXT NOT NULL,
    idea_id TEXT NOT NULL,
    trigger_name TEXT NOT NULL,
    trigger_type TEXT NOT NULL,
    signal_quality REAL CHECK (signal_quality BETWEEN 0 AND 1),
    threshold_clarity REAL CHECK (threshold_clarity BETWEEN 0 AND 1),
    decision_linkage REAL CHECK (decision_linkage BETWEEN 0 AND 1),
    timeliness REAL CHECK (timeliness BETWEEN 0 AND 1),
    stakeholder_visibility REAL CHECK (stakeholder_visibility BETWEEN 0 AND 1),
    governance_owner_clarity REAL CHECK (governance_owner_clarity BETWEEN 0 AND 1),
    response_options_quality REAL CHECK (response_options_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (link_id) REFERENCES theory_links(link_id),
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id)
);

CREATE TABLE decision_memory (
    decision_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    link_id TEXT,
    decision_date TEXT,
    problem_frame TEXT,
    mechanism_statement TEXT,
    assumptions_reviewed TEXT,
    evidence_summary TEXT,
    prototype_summary TEXT,
    trigger_summary TEXT,
    decision_taken TEXT,
    learning_archived TEXT,
    next_review_date TEXT,
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id),
    FOREIGN KEY (link_id) REFERENCES theory_links(link_id)
);

CREATE VIEW strategic_logic_scores AS
SELECT
    idea_id,
    idea_name,
    idea_type,
    domain,
    ROUND(
      0.14 * problem_frame_quality +
      0.17 * mechanism_clarity +
      0.12 * strategic_alignment +
      0.11 * implementation_feasibility +
      0.12 * stakeholder_legitimacy -
      0.10 * system_complexity +
      0.13 * learning_value +
      0.11 * reversibility,
      4
    ) AS strategic_logic_score
FROM strategic_ideas;

CREATE VIEW theory_link_risk_scores AS
SELECT
    link_id,
    idea_id,
    link_stage,
    link_description,
    ROUND(
      0.16 * (1 - mechanism_clarity) +
      0.18 * (1 - evidence_strength) +
      0.13 * actor_dependency +
      0.11 * capacity_dependency +
      0.14 * system_dependency +
      0.12 * ethical_dependency +
      0.16 * failure_consequence,
      4
    ) AS link_risk_score,
    ROUND(
      (
        0.16 * (1 - mechanism_clarity) +
        0.18 * (1 - evidence_strength) +
        0.13 * actor_dependency +
        0.11 * capacity_dependency +
        0.14 * system_dependency +
        0.12 * ethical_dependency +
        0.16 * failure_consequence
      ) * testability,
      4
    ) AS test_priority_score
FROM theory_links;

CREATE VIEW assumption_link_scores AS
SELECT
    assumption_id,
    link_id,
    idea_id,
    assumption_statement,
    assumption_type,
    ROUND(0.40 * evidence_strength + 0.30 * evidence_relevance + 0.30 * evidence_transferability, 4) AS evidence_composite,
    ROUND(criticality * uncertainty * (1 - (0.40 * evidence_strength + 0.30 * evidence_relevance + 0.30 * evidence_transferability)), 4) AS assumption_risk_score
FROM assumptions;

CREATE VIEW evidence_match_scores AS
SELECT
    evidence_id,
    link_id,
    assumption_id,
    evidence_type,
    ROUND(
      0.18 * reliability +
      0.24 * relevance +
      0.18 * transferability +
      0.12 * timeliness -
      0.10 * bias_risk +
      0.12 * coverage_quality +
      0.16 * interpretation_quality,
      4
    ) AS evidence_match_score
FROM evidence_sources;

CREATE VIEW actor_response_scores AS
SELECT
    actor_id,
    link_id,
    idea_id,
    actor_group,
    ROUND(
      0.16 * response_dependency -
      0.12 * incentive_alignment +
      0.14 * (1 - trust_condition) +
      0.12 * (1 - capacity_condition) +
      0.15 * burden_risk +
      0.13 * resistance_risk -
      0.08 * participation_quality +
      0.10 * knowledge_value,
      4
    ) AS actor_response_risk
FROM actor_response;

CREATE VIEW system_feedback_scores AS
SELECT
    feedback_id,
    link_id,
    idea_id,
    feedback_pattern,
    feedback_type,
    ROUND(
      0.14 * feedback_risk +
      0.13 * adaptation_risk +
      0.12 * delay_risk +
      0.15 * burden_shift_risk +
      0.13 * metric_gaming_risk +
      0.12 * context_dependency -
      0.09 * monitoring_quality +
      0.12 * leverage_relevance,
      4
    ) AS feedback_risk_score
FROM system_feedback;

CREATE VIEW outcome_sequence_scores AS
SELECT
    sequence_id,
    idea_id,
    outcome_stage,
    outcome_name,
    time_horizon,
    ROUND(
      0.14 * precondition_quality +
      0.16 * indicator_quality +
      0.13 * measurement_feasibility -
      0.10 * actor_dependency -
      0.12 * system_dependency -
      0.15 * impact_claim_risk +
      0.14 * review_cadence_quality,
      4
    ) AS outcome_sequence_quality
FROM outcome_sequence;

CREATE VIEW prototype_test_scores AS
SELECT
    prototype_id,
    link_id,
    idea_id,
    prototype_name,
    prototype_type,
    ROUND(
      0.16 * link_fit +
      0.10 * learning_speed +
      0.15 * learning_depth +
      0.12 * realism +
      0.12 * stakeholder_inclusion +
      0.10 * scale_signal_quality +
      0.08 * cost_efficiency +
      0.09 * ethical_safety +
      0.18 * decision_usefulness,
      4
    ) AS prototype_test_score
FROM prototype_tests;

CREATE VIEW implementation_learning_scores AS
SELECT
    learning_id,
    idea_id,
    learning_focus,
    review_stage,
    ROUND(
      0.14 * evidence_quality +
      0.14 * feedback_quality +
      0.16 * decision_linkage +
      0.13 * governance_owner_clarity +
      0.13 * revision_capacity +
      0.10 * stakeholder_visibility +
      0.09 * timeliness +
      0.11 * learning_memory_quality,
      4
    ) AS learning_loop_quality
FROM implementation_learning;

CREATE VIEW revision_trigger_scores AS
SELECT
    trigger_id,
    link_id,
    idea_id,
    trigger_name,
    trigger_type,
    ROUND(
      0.15 * signal_quality +
      0.15 * threshold_clarity +
      0.16 * decision_linkage +
      0.12 * timeliness +
      0.12 * stakeholder_visibility +
      0.12 * governance_owner_clarity +
      0.18 * response_options_quality,
      4
    ) AS trigger_quality_score
FROM revision_triggers;
