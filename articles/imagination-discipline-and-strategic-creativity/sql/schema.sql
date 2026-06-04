-- Advanced SQL schema for imagination, discipline, and strategic creativity.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS strategic_creativity_scores;
DROP VIEW IF EXISTS novelty_depth_scores;
DROP VIEW IF EXISTS constraint_scores;
DROP VIEW IF EXISTS stakeholder_grounding_scores;
DROP VIEW IF EXISTS systems_fit_scores;
DROP VIEW IF EXISTS evidence_pathway_scores;
DROP VIEW IF EXISTS idea_maturation_scores;
DROP VIEW IF EXISTS creative_portfolio_scores;
DROP VIEW IF EXISTS intervention_value_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS intervention_library;
DROP TABLE IF EXISTS creative_portfolio;
DROP TABLE IF EXISTS idea_maturation;
DROP TABLE IF EXISTS evidence_pathways;
DROP TABLE IF EXISTS systems_fit;
DROP TABLE IF EXISTS stakeholder_reviews;
DROP TABLE IF EXISTS constraint_audit;
DROP TABLE IF EXISTS creative_ideas;

CREATE TABLE creative_ideas (
    idea_id TEXT PRIMARY KEY,
    idea_name TEXT NOT NULL,
    idea_type TEXT NOT NULL,
    frame_family TEXT NOT NULL,
    source_domain TEXT NOT NULL,
    novelty REAL CHECK (novelty BETWEEN 0 AND 1),
    strategic_relevance REAL CHECK (strategic_relevance BETWEEN 0 AND 1),
    conceptual_coherence REAL CHECK (conceptual_coherence BETWEEN 0 AND 1),
    mechanism_clarity REAL CHECK (mechanism_clarity BETWEEN 0 AND 1),
    testability REAL CHECK (testability BETWEEN 0 AND 1),
    stakeholder_grounding REAL CHECK (stakeholder_grounding BETWEEN 0 AND 1),
    systems_fit REAL CHECK (systems_fit BETWEEN 0 AND 1),
    developmental_potential REAL CHECK (developmental_potential BETWEEN 0 AND 1),
    implementation_risk REAL CHECK (implementation_risk BETWEEN 0 AND 1),
    revision_capacity REAL CHECK (revision_capacity BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE constraint_audit (
    constraint_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    constraint_name TEXT NOT NULL,
    constraint_type TEXT NOT NULL,
    constraint_legitimacy REAL CHECK (constraint_legitimacy BETWEEN 0 AND 1),
    creative_focus_gain REAL CHECK (creative_focus_gain BETWEEN 0 AND 1),
    search_narrowing_risk REAL CHECK (search_narrowing_risk BETWEEN 0 AND 1),
    assumption_disguise_risk REAL CHECK (assumption_disguise_risk BETWEEN 0 AND 1),
    ethical_importance REAL CHECK (ethical_importance BETWEEN 0 AND 1),
    changeability REAL CHECK (changeability BETWEEN 0 AND 1),
    sequencing_value REAL CHECK (sequencing_value BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES creative_ideas(idea_id)
);

CREATE TABLE stakeholder_reviews (
    review_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    stakeholder_group TEXT NOT NULL,
    visibility_quality REAL CHECK (visibility_quality BETWEEN 0 AND 1),
    burden_visibility REAL CHECK (burden_visibility BETWEEN 0 AND 1),
    trust_sensitivity REAL CHECK (trust_sensitivity BETWEEN 0 AND 1),
    agency_preservation REAL CHECK (agency_preservation BETWEEN 0 AND 1),
    participation_quality REAL CHECK (participation_quality BETWEEN 0 AND 1),
    legitimacy_score REAL CHECK (legitimacy_score BETWEEN 0 AND 1),
    hidden_harm_risk REAL CHECK (hidden_harm_risk BETWEEN 0 AND 1),
    review_recommendation TEXT,
    FOREIGN KEY (idea_id) REFERENCES creative_ideas(idea_id)
);

CREATE TABLE systems_fit (
    systems_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    feedback_awareness REAL CHECK (feedback_awareness BETWEEN 0 AND 1),
    incentive_fit REAL CHECK (incentive_fit BETWEEN 0 AND 1),
    dependency_visibility REAL CHECK (dependency_visibility BETWEEN 0 AND 1),
    delay_awareness REAL CHECK (delay_awareness BETWEEN 0 AND 1),
    second_order_review REAL CHECK (second_order_review BETWEEN 0 AND 1),
    boundary_quality REAL CHECK (boundary_quality BETWEEN 0 AND 1),
    adaptation_review REAL CHECK (adaptation_review BETWEEN 0 AND 1),
    robustness_across_scenarios REAL CHECK (robustness_across_scenarios BETWEEN 0 AND 1),
    systems_risk REAL CHECK (systems_risk BETWEEN 0 AND 1),
    systems_recommendation TEXT,
    FOREIGN KEY (idea_id) REFERENCES creative_ideas(idea_id)
);

CREATE TABLE evidence_pathways (
    evidence_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    evidence_name TEXT NOT NULL,
    evidence_type TEXT NOT NULL,
    evidence_strength REAL CHECK (evidence_strength BETWEEN 0 AND 1),
    reliability REAL CHECK (reliability BETWEEN 0 AND 1),
    cost REAL CHECK (cost BETWEEN 0 AND 1),
    time_to_learn REAL CHECK (time_to_learn BETWEEN 0 AND 1),
    discrimination_power REAL CHECK (discrimination_power BETWEEN 0 AND 1),
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    disconfirmation_quality REAL CHECK (disconfirmation_quality BETWEEN 0 AND 1),
    expected_if_promising TEXT,
    weakens_if TEXT,
    FOREIGN KEY (idea_id) REFERENCES creative_ideas(idea_id)
);

CREATE TABLE idea_maturation (
    maturation_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    stage TEXT NOT NULL,
    clarification_gain REAL CHECK (clarification_gain BETWEEN 0 AND 1),
    evidence_gain REAL CHECK (evidence_gain BETWEEN 0 AND 1),
    stakeholder_gain REAL CHECK (stakeholder_gain BETWEEN 0 AND 1),
    systems_gain REAL CHECK (systems_gain BETWEEN 0 AND 1),
    recombination_gain REAL CHECK (recombination_gain BETWEEN 0 AND 1),
    revision_quality REAL CHECK (revision_quality BETWEEN 0 AND 1),
    stage_gate_quality REAL CHECK (stage_gate_quality BETWEEN 0 AND 1),
    next_stage_recommendation TEXT,
    FOREIGN KEY (idea_id) REFERENCES creative_ideas(idea_id)
);

CREATE TABLE creative_portfolio (
    portfolio_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    portfolio_role TEXT NOT NULL,
    confidence_level REAL CHECK (confidence_level BETWEEN 0 AND 1),
    evidence_readiness REAL CHECK (evidence_readiness BETWEEN 0 AND 1),
    strategic_option_value REAL CHECK (strategic_option_value BETWEEN 0 AND 1),
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    resource_intensity REAL CHECK (resource_intensity BETWEEN 0 AND 1),
    time_sensitivity REAL CHECK (time_sensitivity BETWEEN 0 AND 1),
    risk_exposure REAL CHECK (risk_exposure BETWEEN 0 AND 1),
    portfolio_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES creative_ideas(idea_id)
);

CREATE TABLE intervention_library (
    intervention_id TEXT PRIMARY KEY,
    intervention_name TEXT NOT NULL,
    target_creativity_risk TEXT NOT NULL,
    process_cost REAL CHECK (process_cost BETWEEN 0 AND 1),
    implementation_complexity REAL CHECK (implementation_complexity BETWEEN 0 AND 1),
    creativity_quality_gain REAL CHECK (creativity_quality_gain BETWEEN 0 AND 1),
    evidence_quality_gain REAL CHECK (evidence_quality_gain BETWEEN 0 AND 1),
    stakeholder_gain REAL CHECK (stakeholder_gain BETWEEN 0 AND 1),
    systems_fit_gain REAL CHECK (systems_fit_gain BETWEEN 0 AND 1),
    revision_gain REAL CHECK (revision_gain BETWEEN 0 AND 1),
    decision_memory_gain REAL CHECK (decision_memory_gain BETWEEN 0 AND 1),
    political_safety_need REAL CHECK (political_safety_need BETWEEN 0 AND 1)
);

CREATE TABLE decision_memory (
    decision_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    decision_date TEXT,
    starting_frame TEXT,
    novelty_depth_summary TEXT,
    mechanism_summary TEXT,
    constraint_review TEXT,
    stakeholder_review TEXT,
    systems_review TEXT,
    evidence_pathway TEXT,
    decision_outcome TEXT,
    revision_trigger TEXT,
    archived_learning TEXT,
    FOREIGN KEY (idea_id) REFERENCES creative_ideas(idea_id)
);

CREATE VIEW strategic_creativity_scores AS
SELECT
    idea_id,
    idea_name,
    idea_type,
    frame_family,
    source_domain,
    ROUND(
      0.14 * novelty +
      0.16 * strategic_relevance +
      0.13 * conceptual_coherence +
      0.14 * mechanism_clarity +
      0.11 * testability +
      0.13 * stakeholder_grounding +
      0.13 * systems_fit +
      0.12 * developmental_potential +
      0.08 * revision_capacity -
      0.12 * implementation_risk,
      4
    ) AS strategic_creativity_score
FROM creative_ideas;

CREATE VIEW novelty_depth_scores AS
SELECT
    idea_id,
    idea_name,
    novelty,
    mechanism_clarity,
    stakeholder_grounding,
    systems_fit,
    ROUND(novelty * (1.0 - ((mechanism_clarity + stakeholder_grounding + systems_fit) / 3.0)), 4) AS novelty_theater_risk
FROM creative_ideas;

CREATE VIEW constraint_scores AS
SELECT
    constraint_id,
    idea_id,
    constraint_name,
    constraint_type,
    ROUND(
      0.18 * constraint_legitimacy +
      0.18 * creative_focus_gain +
      0.16 * ethical_importance +
      0.14 * sequencing_value -
      0.12 * search_narrowing_risk -
      0.12 * assumption_disguise_risk,
      4
    ) AS productive_constraint_value,
    ROUND(
      0.30 * search_narrowing_risk +
      0.30 * assumption_disguise_risk +
      0.18 * changeability -
      0.18 * constraint_legitimacy -
      0.12 * ethical_importance,
      4
    ) AS dead_constraint_risk
FROM constraint_audit;

CREATE VIEW stakeholder_grounding_scores AS
SELECT
    review_id,
    idea_id,
    stakeholder_group,
    ROUND(
      0.16 * visibility_quality +
      0.16 * burden_visibility +
      0.14 * trust_sensitivity +
      0.14 * agency_preservation +
      0.14 * participation_quality +
      0.16 * legitimacy_score -
      0.10 * hidden_harm_risk,
      4
    ) AS stakeholder_grounding_score
FROM stakeholder_reviews;

CREATE VIEW systems_fit_scores AS
SELECT
    systems_id,
    idea_id,
    ROUND(
      0.14 * feedback_awareness +
      0.14 * incentive_fit +
      0.12 * dependency_visibility +
      0.12 * delay_awareness +
      0.14 * second_order_review +
      0.12 * boundary_quality +
      0.12 * adaptation_review +
      0.14 * robustness_across_scenarios -
      0.12 * systems_risk,
      4
    ) AS systems_fit_score
FROM systems_fit;

CREATE VIEW evidence_pathway_scores AS
SELECT
    evidence_id,
    idea_id,
    evidence_name,
    evidence_type,
    ROUND(
      0.16 * evidence_strength +
      0.14 * reliability +
      0.16 * discrimination_power +
      0.18 * learning_value +
      0.14 * disconfirmation_quality -
      0.10 * cost -
      0.08 * time_to_learn,
      4
    ) AS evidence_value_score
FROM evidence_pathways;

CREATE VIEW idea_maturation_scores AS
SELECT
    maturation_id,
    idea_id,
    stage,
    ROUND(
      0.14 * clarification_gain +
      0.14 * evidence_gain +
      0.14 * stakeholder_gain +
      0.14 * systems_gain +
      0.14 * recombination_gain +
      0.16 * revision_quality +
      0.14 * stage_gate_quality,
      4
    ) AS maturation_score
FROM idea_maturation;

CREATE VIEW creative_portfolio_scores AS
SELECT
    portfolio_id,
    idea_id,
    portfolio_role,
    portfolio_action,
    ROUND(
      0.14 * confidence_level +
      0.14 * evidence_readiness +
      0.18 * strategic_option_value +
      0.16 * learning_value -
      0.10 * resource_intensity +
      0.12 * time_sensitivity -
      0.10 * risk_exposure,
      4
    ) AS portfolio_value_score
FROM creative_portfolio;

CREATE VIEW intervention_value_scores AS
SELECT
    intervention_id,
    intervention_name,
    target_creativity_risk,
    ROUND(
      0.16 * creativity_quality_gain +
      0.14 * evidence_quality_gain +
      0.14 * stakeholder_gain +
      0.14 * systems_fit_gain +
      0.14 * revision_gain +
      0.14 * decision_memory_gain -
      0.10 * process_cost -
      0.08 * implementation_complexity -
      0.08 * political_safety_need,
      4
    ) AS intervention_value_score
FROM intervention_library;
