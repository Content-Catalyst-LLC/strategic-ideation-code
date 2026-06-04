-- Advanced SQL schema for abductive reasoning and strategic hypotheses.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS hypothesis_value_scores;
DROP VIEW IF EXISTS evidence_pathway_scores;
DROP VIEW IF EXISTS disconfirmation_scores;
DROP VIEW IF EXISTS commitment_readiness_scores;
DROP VIEW IF EXISTS revision_trigger_scores;
DROP VIEW IF EXISTS hypothesis_portfolio_scores;
DROP VIEW IF EXISTS intervention_value_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS intervention_library;
DROP TABLE IF EXISTS portfolio_status;
DROP TABLE IF EXISTS revision_triggers;
DROP TABLE IF EXISTS commitment_levels;
DROP TABLE IF EXISTS disconfirmation_tests;
DROP TABLE IF EXISTS evidence_pathways;
DROP TABLE IF EXISTS hypotheses;
DROP TABLE IF EXISTS observations;

CREATE TABLE observations (
    observation_id TEXT PRIMARY KEY,
    observation_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    signal_type TEXT NOT NULL,
    signal_strength REAL CHECK (signal_strength BETWEEN 0 AND 1),
    strategic_relevance REAL CHECK (strategic_relevance BETWEEN 0 AND 1),
    novelty REAL CHECK (novelty BETWEEN 0 AND 1),
    urgency REAL CHECK (urgency BETWEEN 0 AND 1),
    ambiguity REAL CHECK (ambiguity BETWEEN 0 AND 1),
    stakeholder_visibility REAL CHECK (stakeholder_visibility BETWEEN 0 AND 1),
    system_level TEXT NOT NULL,
    description TEXT
);

CREATE TABLE hypotheses (
    hypothesis_id TEXT PRIMARY KEY,
    observation_id TEXT NOT NULL,
    hypothesis_name TEXT NOT NULL,
    hypothesis_type TEXT NOT NULL,
    frame_family TEXT NOT NULL,
    mechanism_family TEXT NOT NULL,
    explanatory_strength REAL CHECK (explanatory_strength BETWEEN 0 AND 1),
    testability REAL CHECK (testability BETWEEN 0 AND 1),
    evidence_quality REAL CHECK (evidence_quality BETWEEN 0 AND 1),
    strategic_relevance REAL CHECK (strategic_relevance BETWEEN 0 AND 1),
    stakeholder_visibility REAL CHECK (stakeholder_visibility BETWEEN 0 AND 1),
    systems_fit REAL CHECK (systems_fit BETWEEN 0 AND 1),
    actionability REAL CHECK (actionability BETWEEN 0 AND 1),
    implementation_risk REAL CHECK (implementation_risk BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    confidence_prior REAL CHECK (confidence_prior BETWEEN 0 AND 1),
    FOREIGN KEY (observation_id) REFERENCES observations(observation_id)
);

CREATE TABLE evidence_pathways (
    evidence_id TEXT PRIMARY KEY,
    hypothesis_id TEXT NOT NULL,
    evidence_name TEXT NOT NULL,
    evidence_type TEXT NOT NULL,
    evidence_strength REAL CHECK (evidence_strength BETWEEN 0 AND 1),
    reliability REAL CHECK (reliability BETWEEN 0 AND 1),
    cost REAL CHECK (cost BETWEEN 0 AND 1),
    time_to_learn REAL CHECK (time_to_learn BETWEEN 0 AND 1),
    discrimination_power REAL CHECK (discrimination_power BETWEEN 0 AND 1),
    stakeholder_legitimacy REAL CHECK (stakeholder_legitimacy BETWEEN 0 AND 1),
    expected_if_true TEXT,
    weakens_if TEXT,
    FOREIGN KEY (hypothesis_id) REFERENCES hypotheses(hypothesis_id)
);

CREATE TABLE disconfirmation_tests (
    test_id TEXT PRIMARY KEY,
    hypothesis_id TEXT NOT NULL,
    test_name TEXT NOT NULL,
    disconfirmation_clarity REAL CHECK (disconfirmation_clarity BETWEEN 0 AND 1),
    severity_if_disconfirmed REAL CHECK (severity_if_disconfirmed BETWEEN 0 AND 1),
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    political_difficulty REAL CHECK (political_difficulty BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    decision_impact REAL CHECK (decision_impact BETWEEN 0 AND 1),
    revision_path_quality REAL CHECK (revision_path_quality BETWEEN 0 AND 1),
    FOREIGN KEY (hypothesis_id) REFERENCES hypotheses(hypothesis_id)
);

CREATE TABLE commitment_levels (
    commitment_id TEXT PRIMARY KEY,
    hypothesis_id TEXT NOT NULL,
    current_commitment TEXT NOT NULL,
    commitment_cost REAL CHECK (commitment_cost BETWEEN 0 AND 1),
    commitment_reversibility REAL CHECK (commitment_reversibility BETWEEN 0 AND 1),
    evidence_threshold_met REAL CHECK (evidence_threshold_met BETWEEN 0 AND 1),
    confidence_threshold_met REAL CHECK (confidence_threshold_met BETWEEN 0 AND 1),
    stakeholder_threshold_met REAL CHECK (stakeholder_threshold_met BETWEEN 0 AND 1),
    risk_threshold_met REAL CHECK (risk_threshold_met BETWEEN 0 AND 1),
    recommended_next_commitment TEXT,
    FOREIGN KEY (hypothesis_id) REFERENCES hypotheses(hypothesis_id)
);

CREATE TABLE revision_triggers (
    trigger_id TEXT PRIMARY KEY,
    hypothesis_id TEXT NOT NULL,
    trigger_name TEXT NOT NULL,
    trigger_type TEXT NOT NULL,
    trigger_clarity REAL CHECK (trigger_clarity BETWEEN 0 AND 1),
    monitoring_quality REAL CHECK (monitoring_quality BETWEEN 0 AND 1),
    reopen_value REAL CHECK (reopen_value BETWEEN 0 AND 1),
    revision_difficulty REAL CHECK (revision_difficulty BETWEEN 0 AND 1),
    decision_memory_quality REAL CHECK (decision_memory_quality BETWEEN 0 AND 1),
    action_if_triggered TEXT,
    FOREIGN KEY (hypothesis_id) REFERENCES hypotheses(hypothesis_id)
);

CREATE TABLE portfolio_status (
    portfolio_id TEXT PRIMARY KEY,
    hypothesis_id TEXT NOT NULL,
    portfolio_role TEXT NOT NULL,
    confidence_level REAL CHECK (confidence_level BETWEEN 0 AND 1),
    evidence_readiness REAL CHECK (evidence_readiness BETWEEN 0 AND 1),
    strategic_option_value REAL CHECK (strategic_option_value BETWEEN 0 AND 1),
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    resource_intensity REAL CHECK (resource_intensity BETWEEN 0 AND 1),
    time_sensitivity REAL CHECK (time_sensitivity BETWEEN 0 AND 1),
    risk_exposure REAL CHECK (risk_exposure BETWEEN 0 AND 1),
    portfolio_action TEXT,
    FOREIGN KEY (hypothesis_id) REFERENCES hypotheses(hypothesis_id)
);

CREATE TABLE intervention_library (
    intervention_id TEXT PRIMARY KEY,
    intervention_name TEXT NOT NULL,
    target_abductive_risk TEXT NOT NULL,
    process_cost REAL CHECK (process_cost BETWEEN 0 AND 1),
    implementation_complexity REAL CHECK (implementation_complexity BETWEEN 0 AND 1),
    hypothesis_quality_gain REAL CHECK (hypothesis_quality_gain BETWEEN 0 AND 1),
    evidence_quality_gain REAL CHECK (evidence_quality_gain BETWEEN 0 AND 1),
    disconfirmation_gain REAL CHECK (disconfirmation_gain BETWEEN 0 AND 1),
    stakeholder_gain REAL CHECK (stakeholder_gain BETWEEN 0 AND 1),
    revision_gain REAL CHECK (revision_gain BETWEEN 0 AND 1),
    decision_memory_gain REAL CHECK (decision_memory_gain BETWEEN 0 AND 1),
    political_safety_need REAL CHECK (political_safety_need BETWEEN 0 AND 1)
);

CREATE TABLE decision_memory (
    decision_id TEXT PRIMARY KEY,
    observation_id TEXT NOT NULL,
    hypothesis_id TEXT,
    evidence_id TEXT,
    decision_date TEXT,
    observation_summary TEXT,
    frame_used TEXT,
    rival_hypotheses_considered TEXT,
    mechanism_summary TEXT,
    disconfirming_evidence_defined TEXT,
    commitment_level TEXT,
    decision_outcome TEXT,
    revision_trigger TEXT,
    archived_learning TEXT,
    FOREIGN KEY (observation_id) REFERENCES observations(observation_id),
    FOREIGN KEY (hypothesis_id) REFERENCES hypotheses(hypothesis_id),
    FOREIGN KEY (evidence_id) REFERENCES evidence_pathways(evidence_id)
);

CREATE VIEW hypothesis_value_scores AS
SELECT
    hypothesis_id,
    observation_id,
    hypothesis_name,
    hypothesis_type,
    frame_family,
    mechanism_family,
    ROUND(
      0.16 * explanatory_strength +
      0.14 * testability +
      0.14 * evidence_quality +
      0.16 * strategic_relevance +
      0.12 * stakeholder_visibility +
      0.12 * systems_fit +
      0.10 * actionability +
      0.06 * reversibility -
      0.10 * implementation_risk,
      4
    ) AS hypothesis_value_score
FROM hypotheses;

CREATE VIEW evidence_pathway_scores AS
SELECT
    evidence_id,
    hypothesis_id,
    evidence_name,
    evidence_type,
    ROUND(
      0.18 * evidence_strength +
      0.16 * reliability +
      0.18 * discrimination_power +
      0.14 * stakeholder_legitimacy -
      0.10 * cost -
      0.08 * time_to_learn,
      4
    ) AS evidence_value_score
FROM evidence_pathways;

CREATE VIEW disconfirmation_scores AS
SELECT
    test_id,
    hypothesis_id,
    test_name,
    ROUND(
      0.18 * disconfirmation_clarity +
      0.14 * severity_if_disconfirmed +
      0.18 * learning_value -
      0.08 * political_difficulty +
      0.12 * reversibility +
      0.14 * decision_impact +
      0.14 * revision_path_quality,
      4
    ) AS disconfirmation_quality_score
FROM disconfirmation_tests;

CREATE VIEW commitment_readiness_scores AS
SELECT
    commitment_id,
    hypothesis_id,
    current_commitment,
    recommended_next_commitment,
    ROUND(
      0.16 * commitment_reversibility +
      0.18 * evidence_threshold_met +
      0.18 * confidence_threshold_met +
      0.14 * stakeholder_threshold_met +
      0.14 * risk_threshold_met -
      0.12 * commitment_cost,
      4
    ) AS commitment_readiness_score
FROM commitment_levels;

CREATE VIEW revision_trigger_scores AS
SELECT
    trigger_id,
    hypothesis_id,
    trigger_name,
    trigger_type,
    action_if_triggered,
    ROUND(
      0.18 * trigger_clarity +
      0.14 * monitoring_quality +
      0.18 * reopen_value -
      0.10 * revision_difficulty +
      0.16 * decision_memory_quality,
      4
    ) AS revision_quality_score
FROM revision_triggers;

CREATE VIEW hypothesis_portfolio_scores AS
SELECT
    portfolio_id,
    hypothesis_id,
    portfolio_role,
    portfolio_action,
    ROUND(
      0.16 * confidence_level +
      0.16 * evidence_readiness +
      0.18 * strategic_option_value +
      0.16 * learning_value -
      0.10 * resource_intensity +
      0.12 * time_sensitivity -
      0.10 * risk_exposure,
      4
    ) AS portfolio_value_score
FROM portfolio_status;

CREATE VIEW intervention_value_scores AS
SELECT
    intervention_id,
    intervention_name,
    target_abductive_risk,
    ROUND(
      0.16 * hypothesis_quality_gain +
      0.16 * evidence_quality_gain +
      0.16 * disconfirmation_gain +
      0.14 * stakeholder_gain +
      0.14 * revision_gain +
      0.14 * decision_memory_gain -
      0.10 * process_cost -
      0.08 * implementation_complexity -
      0.08 * political_safety_need,
      4
    ) AS intervention_value_score
FROM intervention_library;
