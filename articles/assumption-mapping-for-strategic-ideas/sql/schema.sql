-- Advanced SQL schema for assumption mapping in strategic ideation.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS assumption_risk_scores;
DROP VIEW IF EXISTS evidence_review_scores;
DROP VIEW IF EXISTS test_prioritization_scores;
DROP VIEW IF EXISTS prototype_learning_scores;
DROP VIEW IF EXISTS theory_of_change_assumption_scores;
DROP VIEW IF EXISTS option_confidence_scores;
DROP VIEW IF EXISTS stakeholder_assumption_scores;
DROP VIEW IF EXISTS system_response_assumption_scores;
DROP VIEW IF EXISTS future_assumption_scores;
DROP VIEW IF EXISTS revision_trigger_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS revision_triggers;
DROP TABLE IF EXISTS future_assumptions;
DROP TABLE IF EXISTS system_response_assumptions;
DROP TABLE IF EXISTS stakeholder_assumptions;
DROP TABLE IF EXISTS option_confidence;
DROP TABLE IF EXISTS prototype_learning;
DROP TABLE IF EXISTS theory_of_change_links;
DROP TABLE IF EXISTS assumption_tests;
DROP TABLE IF EXISTS evidence_sources;
DROP TABLE IF EXISTS assumptions;
DROP TABLE IF EXISTS strategic_ideas;

CREATE TABLE strategic_ideas (
    idea_id TEXT PRIMARY KEY,
    idea_name TEXT NOT NULL,
    idea_type TEXT NOT NULL,
    domain TEXT NOT NULL,
    expected_impact REAL CHECK (expected_impact BETWEEN 0 AND 1),
    strategic_alignment REAL CHECK (strategic_alignment BETWEEN 0 AND 1),
    implementation_feasibility REAL CHECK (implementation_feasibility BETWEEN 0 AND 1),
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    stakeholder_sensitivity REAL CHECK (stakeholder_sensitivity BETWEEN 0 AND 1),
    system_complexity REAL CHECK (system_complexity BETWEEN 0 AND 1),
    commitment_size REAL CHECK (commitment_size BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE assumptions (
    assumption_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    assumption_statement TEXT NOT NULL,
    assumption_type TEXT NOT NULL,
    criticality REAL CHECK (criticality BETWEEN 0 AND 1),
    uncertainty REAL CHECK (uncertainty BETWEEN 0 AND 1),
    evidence_strength REAL CHECK (evidence_strength BETWEEN 0 AND 1),
    evidence_relevance REAL CHECK (evidence_relevance BETWEEN 0 AND 1),
    evidence_transferability REAL CHECK (evidence_transferability BETWEEN 0 AND 1),
    testability REAL CHECK (testability BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    stakeholder_sensitivity REAL CHECK (stakeholder_sensitivity BETWEEN 0 AND 1),
    time_sensitivity REAL CHECK (time_sensitivity BETWEEN 0 AND 1),
    system_sensitivity REAL CHECK (system_sensitivity BETWEEN 0 AND 1),
    decision_owner TEXT,
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id)
);

CREATE TABLE evidence_sources (
    evidence_id TEXT PRIMARY KEY,
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
    FOREIGN KEY (assumption_id) REFERENCES assumptions(assumption_id)
);

CREATE TABLE assumption_tests (
    test_id TEXT PRIMARY KEY,
    assumption_id TEXT NOT NULL,
    test_name TEXT NOT NULL,
    test_type TEXT NOT NULL,
    test_cost REAL CHECK (test_cost BETWEEN 0 AND 1),
    test_speed REAL CHECK (test_speed BETWEEN 0 AND 1),
    learning_quality REAL CHECK (learning_quality BETWEEN 0 AND 1),
    decision_relevance REAL CHECK (decision_relevance BETWEEN 0 AND 1),
    stakeholder_inclusion REAL CHECK (stakeholder_inclusion BETWEEN 0 AND 1),
    implementation_realism REAL CHECK (implementation_realism BETWEEN 0 AND 1),
    scale_relevance REAL CHECK (scale_relevance BETWEEN 0 AND 1),
    ethical_safety REAL CHECK (ethical_safety BETWEEN 0 AND 1),
    success_threshold REAL CHECK (success_threshold BETWEEN 0 AND 1),
    decision_if_failed TEXT,
    FOREIGN KEY (assumption_id) REFERENCES assumptions(assumption_id)
);

CREATE TABLE theory_of_change_links (
    toc_link_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    assumption_id TEXT NOT NULL,
    link_stage TEXT NOT NULL,
    link_description TEXT,
    mechanism_clarity REAL CHECK (mechanism_clarity BETWEEN 0 AND 1),
    evidence_strength REAL CHECK (evidence_strength BETWEEN 0 AND 1),
    actor_response_dependency REAL CHECK (actor_response_dependency BETWEEN 0 AND 1),
    capacity_dependency REAL CHECK (capacity_dependency BETWEEN 0 AND 1),
    system_dependency REAL CHECK (system_dependency BETWEEN 0 AND 1),
    ethical_dependency REAL CHECK (ethical_dependency BETWEEN 0 AND 1),
    failure_consequence REAL CHECK (failure_consequence BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id),
    FOREIGN KEY (assumption_id) REFERENCES assumptions(assumption_id)
);

CREATE TABLE prototype_learning (
    prototype_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    assumption_id TEXT NOT NULL,
    prototype_name TEXT NOT NULL,
    prototype_type TEXT NOT NULL,
    assumption_fit REAL CHECK (assumption_fit BETWEEN 0 AND 1),
    learning_speed REAL CHECK (learning_speed BETWEEN 0 AND 1),
    learning_depth REAL CHECK (learning_depth BETWEEN 0 AND 1),
    realism REAL CHECK (realism BETWEEN 0 AND 1),
    stakeholder_inclusion REAL CHECK (stakeholder_inclusion BETWEEN 0 AND 1),
    scale_signal_quality REAL CHECK (scale_signal_quality BETWEEN 0 AND 1),
    cost_efficiency REAL CHECK (cost_efficiency BETWEEN 0 AND 1),
    ethical_safety REAL CHECK (ethical_safety BETWEEN 0 AND 1),
    decision_usefulness REAL CHECK (decision_usefulness BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id),
    FOREIGN KEY (assumption_id) REFERENCES assumptions(assumption_id)
);

CREATE TABLE option_confidence (
    option_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    option_name TEXT NOT NULL,
    expected_value REAL CHECK (expected_value BETWEEN 0 AND 1),
    assumption_risk REAL CHECK (assumption_risk BETWEEN 0 AND 1),
    commitment_risk REAL CHECK (commitment_risk BETWEEN 0 AND 1),
    evidence_strength REAL CHECK (evidence_strength BETWEEN 0 AND 1),
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    stakeholder_legitimacy REAL CHECK (stakeholder_legitimacy BETWEEN 0 AND 1),
    implementation_readiness REAL CHECK (implementation_readiness BETWEEN 0 AND 1),
    system_resilience REAL CHECK (system_resilience BETWEEN 0 AND 1),
    decision_recommendation TEXT,
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id)
);

CREATE TABLE stakeholder_assumptions (
    stakeholder_assumption_id TEXT PRIMARY KEY,
    assumption_id TEXT NOT NULL,
    stakeholder_group TEXT NOT NULL,
    assumed_response TEXT NOT NULL,
    inclusion_quality REAL CHECK (inclusion_quality BETWEEN 0 AND 1),
    affectedness REAL CHECK (affectedness BETWEEN 0 AND 1),
    trust_dependency REAL CHECK (trust_dependency BETWEEN 0 AND 1),
    burden_risk REAL CHECK (burden_risk BETWEEN 0 AND 1),
    knowledge_value REAL CHECK (knowledge_value BETWEEN 0 AND 1),
    representation_quality REAL CHECK (representation_quality BETWEEN 0 AND 1),
    redress_need REAL CHECK (redress_need BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (assumption_id) REFERENCES assumptions(assumption_id)
);

CREATE TABLE system_response_assumptions (
    system_assumption_id TEXT PRIMARY KEY,
    assumption_id TEXT NOT NULL,
    system_response TEXT NOT NULL,
    feedback_risk REAL CHECK (feedback_risk BETWEEN 0 AND 1),
    adaptation_risk REAL CHECK (adaptation_risk BETWEEN 0 AND 1),
    burden_shift_risk REAL CHECK (burden_shift_risk BETWEEN 0 AND 1),
    delay_risk REAL CHECK (delay_risk BETWEEN 0 AND 1),
    metric_gaming_risk REAL CHECK (metric_gaming_risk BETWEEN 0 AND 1),
    resistance_risk REAL CHECK (resistance_risk BETWEEN 0 AND 1),
    leverage_relevance REAL CHECK (leverage_relevance BETWEEN 0 AND 1),
    monitoring_quality REAL CHECK (monitoring_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (assumption_id) REFERENCES assumptions(assumption_id)
);

CREATE TABLE future_assumptions (
    future_assumption_id TEXT PRIMARY KEY,
    assumption_id TEXT NOT NULL,
    future_condition TEXT NOT NULL,
    plausibility REAL CHECK (plausibility BETWEEN 0 AND 1),
    uncertainty REAL CHECK (uncertainty BETWEEN 0 AND 1),
    strategic_dependency REAL CHECK (strategic_dependency BETWEEN 0 AND 1),
    monitorability REAL CHECK (monitorability BETWEEN 0 AND 1),
    scenario_sensitivity REAL CHECK (scenario_sensitivity BETWEEN 0 AND 1),
    early_signal_quality REAL CHECK (early_signal_quality BETWEEN 0 AND 1),
    adaptation_options REAL CHECK (adaptation_options BETWEEN 0 AND 1),
    review_cadence_quality REAL CHECK (review_cadence_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (assumption_id) REFERENCES assumptions(assumption_id)
);

CREATE TABLE revision_triggers (
    trigger_id TEXT PRIMARY KEY,
    assumption_id TEXT NOT NULL,
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
    FOREIGN KEY (assumption_id) REFERENCES assumptions(assumption_id)
);

CREATE TABLE decision_memory (
    decision_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    assumption_id TEXT,
    decision_date TEXT,
    assumption_statement TEXT,
    evidence_summary TEXT,
    test_summary TEXT,
    revision_trigger TEXT,
    decision_taken TEXT,
    learning_archived TEXT,
    next_review_date TEXT,
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id),
    FOREIGN KEY (assumption_id) REFERENCES assumptions(assumption_id)
);

CREATE VIEW assumption_risk_scores AS
SELECT
    assumption_id,
    idea_id,
    assumption_statement,
    assumption_type,
    ROUND(criticality * uncertainty, 4) AS priority_score,
    ROUND(0.40 * evidence_strength + 0.30 * evidence_relevance + 0.30 * evidence_transferability, 4) AS evidence_composite,
    ROUND(criticality * uncertainty * (1 - (0.40 * evidence_strength + 0.30 * evidence_relevance + 0.30 * evidence_transferability)), 4) AS evidence_adjusted_risk
FROM assumptions;

CREATE VIEW evidence_review_scores AS
SELECT
    evidence_id,
    assumption_id,
    evidence_type,
    ROUND(
      0.18 * reliability +
      0.22 * relevance +
      0.18 * transferability +
      0.12 * timeliness -
      0.10 * bias_risk +
      0.12 * coverage_quality +
      0.18 * interpretation_quality,
      4
    ) AS evidence_quality_score
FROM evidence_sources;

CREATE VIEW test_prioritization_scores AS
SELECT
    t.test_id,
    t.assumption_id,
    t.test_name,
    t.test_type,
    ROUND(
      0.24 * ars.evidence_adjusted_risk -
      0.08 * t.test_cost +
      0.10 * t.test_speed +
      0.18 * t.learning_quality +
      0.16 * t.decision_relevance +
      0.10 * t.stakeholder_inclusion +
      0.08 * t.implementation_realism +
      0.07 * t.scale_relevance +
      0.09 * t.ethical_safety,
      4
    ) AS test_value_score
FROM assumption_tests t
JOIN assumption_risk_scores ars ON t.assumption_id = ars.assumption_id;

CREATE VIEW prototype_learning_scores AS
SELECT
    prototype_id,
    idea_id,
    assumption_id,
    prototype_name,
    prototype_type,
    ROUND(
      0.18 * assumption_fit +
      0.12 * learning_speed +
      0.16 * learning_depth +
      0.12 * realism +
      0.12 * stakeholder_inclusion +
      0.10 * scale_signal_quality +
      0.08 * cost_efficiency +
      0.10 * ethical_safety +
      0.12 * decision_usefulness,
      4
    ) AS prototype_learning_score
FROM prototype_learning;

CREATE VIEW theory_of_change_assumption_scores AS
SELECT
    toc_link_id,
    idea_id,
    assumption_id,
    link_stage,
    ROUND(
      0.16 * (1 - mechanism_clarity) +
      0.18 * (1 - evidence_strength) +
      0.14 * actor_response_dependency +
      0.12 * capacity_dependency +
      0.14 * system_dependency +
      0.12 * ethical_dependency +
      0.14 * failure_consequence,
      4
    ) AS theory_link_risk_score
FROM theory_of_change_links;

CREATE VIEW option_confidence_scores AS
SELECT
    option_id,
    idea_id,
    option_name,
    ROUND(
      0.18 * expected_value -
      0.18 * assumption_risk -
      0.10 * commitment_risk +
      0.14 * evidence_strength +
      0.12 * learning_value +
      0.10 * reversibility +
      0.12 * stakeholder_legitimacy +
      0.08 * implementation_readiness +
      0.08 * system_resilience,
      4
    ) AS option_confidence_score
FROM option_confidence;

CREATE VIEW stakeholder_assumption_scores AS
SELECT
    stakeholder_assumption_id,
    assumption_id,
    stakeholder_group,
    ROUND(
      0.14 * affectedness +
      0.14 * trust_dependency +
      0.16 * burden_risk +
      0.12 * knowledge_value -
      0.14 * inclusion_quality -
      0.12 * representation_quality +
      0.14 * redress_need,
      4
    ) AS stakeholder_assumption_risk
FROM stakeholder_assumptions;

CREATE VIEW system_response_assumption_scores AS
SELECT
    system_assumption_id,
    assumption_id,
    ROUND(
      0.14 * feedback_risk +
      0.13 * adaptation_risk +
      0.15 * burden_shift_risk +
      0.11 * delay_risk +
      0.13 * metric_gaming_risk +
      0.12 * resistance_risk +
      0.12 * leverage_relevance -
      0.10 * monitoring_quality,
      4
    ) AS system_response_risk
FROM system_response_assumptions;

CREATE VIEW future_assumption_scores AS
SELECT
    future_assumption_id,
    assumption_id,
    future_condition,
    ROUND(
      0.12 * (1 - plausibility) +
      0.18 * uncertainty +
      0.18 * strategic_dependency -
      0.10 * monitorability +
      0.14 * scenario_sensitivity -
      0.10 * early_signal_quality -
      0.10 * adaptation_options -
      0.08 * review_cadence_quality,
      4
    ) AS future_assumption_risk
FROM future_assumptions;

CREATE VIEW revision_trigger_scores AS
SELECT
    trigger_id,
    assumption_id,
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
