-- Advanced SQL schema for From Ideas to Strategy.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS strategy_conversion_scores;
DROP VIEW IF EXISTS strategic_fit_scores;
DROP VIEW IF EXISTS integration_readiness_scores;
DROP VIEW IF EXISTS resource_commitment_scores;
DROP VIEW IF EXISTS alignment_coordination_scores;
DROP VIEW IF EXISTS feedback_learning_scores;
DROP VIEW IF EXISTS ethics_power_scores;
DROP VIEW IF EXISTS governance_review_scores;
DROP VIEW IF EXISTS decision_memory_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS governance_review;
DROP TABLE IF EXISTS ethics_power;
DROP TABLE IF EXISTS feedback_learning;
DROP TABLE IF EXISTS alignment_coordination;
DROP TABLE IF EXISTS resource_commitment;
DROP TABLE IF EXISTS integration_readiness;
DROP TABLE IF EXISTS strategic_fit;
DROP TABLE IF EXISTS initiatives;

CREATE TABLE initiatives (
    initiative_id TEXT PRIMARY KEY,
    initiative_name TEXT NOT NULL,
    initiative_type TEXT NOT NULL,
    feasibility REAL CHECK (feasibility BETWEEN 0 AND 1),
    viability REAL CHECK (viability BETWEEN 0 AND 1),
    desirability REAL CHECK (desirability BETWEEN 0 AND 1),
    integration_difficulty REAL CHECK (integration_difficulty BETWEEN 0 AND 1),
    execution_readiness REAL CHECK (execution_readiness BETWEEN 0 AND 1),
    strategic_fit REAL CHECK (strategic_fit BETWEEN 0 AND 1),
    evidence_confidence REAL CHECK (evidence_confidence BETWEEN 0 AND 1),
    ethical_resilience REAL CHECK (ethical_resilience BETWEEN 0 AND 1),
    resource_intensity REAL CHECK (resource_intensity BETWEEN 0 AND 1),
    governance_readiness REAL CHECK (governance_readiness BETWEEN 0 AND 1),
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE strategic_fit (
    fit_id TEXT PRIMARY KEY,
    initiative_id TEXT NOT NULL,
    purpose_clarity REAL,
    objective_alignment REAL,
    portfolio_fit REAL,
    capability_fit REAL,
    time_horizon_fit REAL,
    narrative_coherence REAL,
    stakeholder_fit REAL,
    opportunity_cost_clarity REAL,
    review_action TEXT,
    FOREIGN KEY (initiative_id) REFERENCES initiatives(initiative_id)
);

CREATE TABLE integration_readiness (
    integration_id TEXT PRIMARY KEY,
    initiative_id TEXT NOT NULL,
    process_readiness REAL,
    technology_readiness REAL,
    role_clarity REAL,
    governance_fit REAL,
    culture_fit REAL,
    stakeholder_absorption REAL,
    data_readiness REAL,
    dependency_complexity REAL,
    review_action TEXT,
    FOREIGN KEY (initiative_id) REFERENCES initiatives(initiative_id)
);

CREATE TABLE resource_commitment (
    resource_id TEXT PRIMARY KEY,
    initiative_id TEXT NOT NULL,
    budget_commitment REAL,
    staff_commitment REAL,
    leadership_attention REAL,
    authority_commitment REAL,
    technical_capacity REAL,
    communications_capacity REAL,
    political_capital REAL,
    commitment_stage TEXT,
    review_action TEXT,
    FOREIGN KEY (initiative_id) REFERENCES initiatives(initiative_id)
);

CREATE TABLE alignment_coordination (
    alignment_id TEXT PRIMARY KEY,
    initiative_id TEXT NOT NULL,
    purpose_alignment REAL,
    role_alignment REAL,
    incentive_alignment REAL,
    communication_alignment REAL,
    decision_rights_clarity REAL,
    cross_function_coordination REAL,
    stakeholder_alignment REAL,
    dissent_capture REAL,
    review_action TEXT,
    FOREIGN KEY (initiative_id) REFERENCES initiatives(initiative_id)
);

CREATE TABLE feedback_learning (
    feedback_id TEXT PRIMARY KEY,
    initiative_id TEXT NOT NULL,
    indicator_quality REAL,
    feedback_frequency REAL,
    assumption_tracking REAL,
    revision_trigger_quality REAL,
    after_action_learning REAL,
    stakeholder_feedback REAL,
    adaptation_capacity REAL,
    drift_detection REAL,
    review_action TEXT,
    FOREIGN KEY (initiative_id) REFERENCES initiatives(initiative_id)
);

CREATE TABLE ethics_power (
    ethics_id TEXT PRIMARY KEY,
    initiative_id TEXT NOT NULL,
    ethical_issue TEXT,
    sponsor_power REAL,
    affected_stakeholder_voice REAL,
    benefit_concentration REAL,
    burden_concentration REAL,
    transparency REAL,
    redress_quality REAL,
    long_term_responsibility REAL,
    review_action TEXT,
    FOREIGN KEY (initiative_id) REFERENCES initiatives(initiative_id)
);

CREATE TABLE governance_review (
    governance_id TEXT PRIMARY KEY,
    initiative_id TEXT NOT NULL,
    owner_clarity REAL,
    decision_gate_quality REAL,
    evidence_standard REAL,
    review_cadence REAL,
    escalation_path REAL,
    stop_rule_quality REAL,
    adaptation_authority REAL,
    decision_memory_quality REAL,
    review_action TEXT,
    FOREIGN KEY (initiative_id) REFERENCES initiatives(initiative_id)
);

CREATE TABLE decision_memory (
    memory_id TEXT PRIMARY KEY,
    initiative_id TEXT NOT NULL,
    memory_practice TEXT,
    purpose_record REAL,
    evidence_record REAL,
    tradeoff_record REAL,
    capability_record REAL,
    integration_record REAL,
    resource_record REAL,
    ethics_record REAL,
    governance_record REAL,
    revision_trigger_quality REAL,
    reuse_quality REAL,
    review_action TEXT,
    FOREIGN KEY (initiative_id) REFERENCES initiatives(initiative_id)
);

CREATE VIEW strategy_conversion_scores AS
SELECT
    initiative_id,
    initiative_name,
    initiative_type,
    ROUND(
      0.14 * feasibility +
      0.15 * viability +
      0.13 * desirability -
      0.11 * integration_difficulty +
      0.15 * execution_readiness +
      0.13 * strategic_fit +
      0.08 * evidence_confidence +
      0.08 * ethical_resilience -
      0.07 * resource_intensity +
      0.10 * governance_readiness +
      0.06 * learning_value,
      4
    ) AS strategy_conversion_score
FROM initiatives;

CREATE VIEW strategic_fit_scores AS
SELECT
    fit_id,
    initiative_id,
    ROUND(
      0.16 * purpose_clarity +
      0.16 * objective_alignment +
      0.14 * portfolio_fit +
      0.13 * capability_fit +
      0.12 * time_horizon_fit +
      0.12 * narrative_coherence +
      0.10 * stakeholder_fit +
      0.07 * opportunity_cost_clarity,
      4
    ) AS strategic_fit_score
FROM strategic_fit;

CREATE VIEW integration_readiness_scores AS
SELECT
    integration_id,
    initiative_id,
    ROUND(
      0.14 * process_readiness +
      0.13 * technology_readiness +
      0.13 * role_clarity +
      0.13 * governance_fit +
      0.12 * culture_fit +
      0.12 * stakeholder_absorption +
      0.12 * data_readiness -
      0.11 * dependency_complexity +
      0.12,
      4
    ) AS integration_readiness_score
FROM integration_readiness;

CREATE VIEW resource_commitment_scores AS
SELECT
    resource_id,
    initiative_id,
    ROUND(
      0.16 * budget_commitment +
      0.16 * staff_commitment +
      0.16 * leadership_attention +
      0.13 * authority_commitment +
      0.13 * technical_capacity +
      0.12 * communications_capacity +
      0.14 * political_capital,
      4
    ) AS resource_commitment_score
FROM resource_commitment;

CREATE VIEW alignment_coordination_scores AS
SELECT
    alignment_id,
    initiative_id,
    ROUND(
      0.14 * purpose_alignment +
      0.13 * role_alignment +
      0.13 * incentive_alignment +
      0.12 * communication_alignment +
      0.13 * decision_rights_clarity +
      0.13 * cross_function_coordination +
      0.12 * stakeholder_alignment +
      0.10 * dissent_capture,
      4
    ) AS alignment_coordination_score
FROM alignment_coordination;

CREATE VIEW feedback_learning_scores AS
SELECT
    feedback_id,
    initiative_id,
    ROUND(
      0.13 * indicator_quality +
      0.12 * feedback_frequency +
      0.14 * assumption_tracking +
      0.14 * revision_trigger_quality +
      0.13 * after_action_learning +
      0.13 * stakeholder_feedback +
      0.12 * adaptation_capacity +
      0.09 * drift_detection,
      4
    ) AS feedback_learning_score
FROM feedback_learning;

CREATE VIEW ethics_power_scores AS
SELECT
    ethics_id,
    initiative_id,
    ethical_issue,
    ROUND(
      0.16 * sponsor_power +
      0.18 * (1 - affected_stakeholder_voice) +
      0.16 * benefit_concentration +
      0.18 * burden_concentration +
      0.12 * (1 - transparency) +
      0.10 * (1 - redress_quality) +
      0.10 * (1 - long_term_responsibility),
      4
    ) AS power_risk
FROM ethics_power;

CREATE VIEW governance_review_scores AS
SELECT
    governance_id,
    initiative_id,
    ROUND(
      0.13 * owner_clarity +
      0.14 * decision_gate_quality +
      0.13 * evidence_standard +
      0.12 * review_cadence +
      0.12 * escalation_path +
      0.12 * stop_rule_quality +
      0.12 * adaptation_authority +
      0.12 * decision_memory_quality,
      4
    ) AS governance_score
FROM governance_review;

CREATE VIEW decision_memory_scores AS
SELECT
    memory_id,
    initiative_id,
    memory_practice,
    ROUND(
      0.10 * purpose_record +
      0.10 * evidence_record +
      0.10 * tradeoff_record +
      0.10 * capability_record +
      0.10 * integration_record +
      0.10 * resource_record +
      0.11 * ethics_record +
      0.10 * governance_record +
      0.10 * revision_trigger_quality +
      0.09 * reuse_quality,
      4
    ) AS decision_memory_score
FROM decision_memory;
