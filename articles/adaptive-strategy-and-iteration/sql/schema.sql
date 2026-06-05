-- Advanced SQL schema for Adaptive Strategy and Iteration.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS adaptive_strategy_profile_scores;
DROP VIEW IF EXISTS feedback_signal_scores;
DROP VIEW IF EXISTS assumption_revision_scores;
DROP VIEW IF EXISTS trigger_condition_scores;
DROP VIEW IF EXISTS experiment_portfolio_scores;
DROP VIEW IF EXISTS timing_responsiveness_scores;
DROP VIEW IF EXISTS exploration_exploitation_scores;
DROP VIEW IF EXISTS systems_impact_scores;
DROP VIEW IF EXISTS adaptive_governance_scores;
DROP VIEW IF EXISTS learning_memory_scores;

DROP TABLE IF EXISTS learning_memory;
DROP TABLE IF EXISTS governance_reviews;
DROP TABLE IF EXISTS systems_impacts;
DROP TABLE IF EXISTS portfolio_balance;
DROP TABLE IF EXISTS timing_responsiveness;
DROP TABLE IF EXISTS experiment_portfolio;
DROP TABLE IF EXISTS trigger_conditions;
DROP TABLE IF EXISTS assumption_register;
DROP TABLE IF EXISTS feedback_signals;
DROP TABLE IF EXISTS strategy_profiles;

CREATE TABLE strategy_profiles (
    strategy_id TEXT PRIMARY KEY,
    strategy_name TEXT NOT NULL,
    organization_type TEXT NOT NULL,
    domain TEXT NOT NULL,
    flexibility REAL CHECK (flexibility BETWEEN 0 AND 1),
    learning_capacity REAL CHECK (learning_capacity BETWEEN 0 AND 1),
    exploration REAL CHECK (exploration BETWEEN 0 AND 1),
    exploitation_balance REAL CHECK (exploitation_balance BETWEEN 0 AND 1),
    coherence REAL CHECK (coherence BETWEEN 0 AND 1),
    feedback_intelligence REAL CHECK (feedback_intelligence BETWEEN 0 AND 1),
    governance REAL CHECK (governance BETWEEN 0 AND 1),
    systems_awareness REAL CHECK (systems_awareness BETWEEN 0 AND 1),
    learning_memory REAL CHECK (learning_memory BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE feedback_signals (
    signal_id TEXT PRIMARY KEY,
    strategy_id TEXT NOT NULL,
    signal_type TEXT NOT NULL,
    signal_description TEXT NOT NULL,
    signal_strength REAL CHECK (signal_strength BETWEEN 0 AND 1),
    noise_risk REAL CHECK (noise_risk BETWEEN 0 AND 1),
    delay_risk REAL CHECK (delay_risk BETWEEN 0 AND 1),
    interpretation_quality REAL CHECK (interpretation_quality BETWEEN 0 AND 1),
    decision_relevance REAL CHECK (decision_relevance BETWEEN 0 AND 1),
    stakeholder_impact REAL CHECK (stakeholder_impact BETWEEN 0 AND 1),
    systems_relevance REAL CHECK (systems_relevance BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (strategy_id) REFERENCES strategy_profiles(strategy_id)
);

CREATE TABLE assumption_register (
    assumption_id TEXT PRIMARY KEY,
    strategy_id TEXT NOT NULL,
    assumption TEXT NOT NULL,
    assumption_type TEXT NOT NULL,
    uncertainty REAL CHECK (uncertainty BETWEEN 0 AND 1),
    consequence REAL CHECK (consequence BETWEEN 0 AND 1),
    evidence_strength REAL CHECK (evidence_strength BETWEEN 0 AND 1),
    decay_risk REAL CHECK (decay_risk BETWEEN 0 AND 1),
    revision_readiness REAL CHECK (revision_readiness BETWEEN 0 AND 1),
    owner_clarity REAL CHECK (owner_clarity BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (strategy_id) REFERENCES strategy_profiles(strategy_id)
);

CREATE TABLE trigger_conditions (
    trigger_id TEXT PRIMARY KEY,
    strategy_id TEXT NOT NULL,
    trigger_name TEXT NOT NULL,
    trigger_clarity REAL CHECK (trigger_clarity BETWEEN 0 AND 1),
    evidence_threshold REAL CHECK (evidence_threshold BETWEEN 0 AND 1),
    decision_path_clarity REAL CHECK (decision_path_clarity BETWEEN 0 AND 1),
    response_speed_fit REAL CHECK (response_speed_fit BETWEEN 0 AND 1),
    ethical_safeguards REAL CHECK (ethical_safeguards BETWEEN 0 AND 1),
    authority_clarity REAL CHECK (authority_clarity BETWEEN 0 AND 1),
    monitoring_quality REAL CHECK (monitoring_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (strategy_id) REFERENCES strategy_profiles(strategy_id)
);

CREATE TABLE experiment_portfolio (
    experiment_id TEXT PRIMARY KEY,
    strategy_id TEXT NOT NULL,
    experiment_type TEXT NOT NULL,
    critical_assumption_fit REAL CHECK (critical_assumption_fit BETWEEN 0 AND 1),
    evidence_standard_quality REAL CHECK (evidence_standard_quality BETWEEN 0 AND 1),
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    decision_linkage REAL CHECK (decision_linkage BETWEEN 0 AND 1),
    resource_fit REAL CHECK (resource_fit BETWEEN 0 AND 1),
    scale_relevance REAL CHECK (scale_relevance BETWEEN 0 AND 1),
    ethical_review REAL CHECK (ethical_review BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (strategy_id) REFERENCES strategy_profiles(strategy_id)
);

CREATE TABLE timing_responsiveness (
    timing_id TEXT PRIMARY KEY,
    strategy_id TEXT NOT NULL,
    timing_issue TEXT NOT NULL,
    response_speed REAL CHECK (response_speed BETWEEN 0 AND 1),
    signal_interpretation REAL CHECK (signal_interpretation BETWEEN 0 AND 1),
    noise_filtering REAL CHECK (noise_filtering BETWEEN 0 AND 1),
    delay_awareness REAL CHECK (delay_awareness BETWEEN 0 AND 1),
    revision_cadence REAL CHECK (revision_cadence BETWEEN 0 AND 1),
    stakeholder_communication REAL CHECK (stakeholder_communication BETWEEN 0 AND 1),
    stability_preservation REAL CHECK (stability_preservation BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (strategy_id) REFERENCES strategy_profiles(strategy_id)
);

CREATE TABLE portfolio_balance (
    portfolio_id TEXT PRIMARY KEY,
    strategy_id TEXT NOT NULL,
    portfolio_name TEXT NOT NULL,
    exploration_strength REAL CHECK (exploration_strength BETWEEN 0 AND 1),
    exploitation_strength REAL CHECK (exploitation_strength BETWEEN 0 AND 1),
    balance_quality REAL CHECK (balance_quality BETWEEN 0 AND 1),
    option_value REAL CHECK (option_value BETWEEN 0 AND 1),
    resource_discipline REAL CHECK (resource_discipline BETWEEN 0 AND 1),
    focus_quality REAL CHECK (focus_quality BETWEEN 0 AND 1),
    transition_path_quality REAL CHECK (transition_path_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (strategy_id) REFERENCES strategy_profiles(strategy_id)
);

CREATE TABLE systems_impacts (
    impact_id TEXT PRIMARY KEY,
    strategy_id TEXT NOT NULL,
    systems_issue TEXT NOT NULL,
    feedback_loop_risk REAL CHECK (feedback_loop_risk BETWEEN 0 AND 1),
    delay_risk REAL CHECK (delay_risk BETWEEN 0 AND 1),
    burden_shift_risk REAL CHECK (burden_shift_risk BETWEEN 0 AND 1),
    capacity_risk REAL CHECK (capacity_risk BETWEEN 0 AND 1),
    incentive_risk REAL CHECK (incentive_risk BETWEEN 0 AND 1),
    scale_uncertainty REAL CHECK (scale_uncertainty BETWEEN 0 AND 1),
    monitoring_quality REAL CHECK (monitoring_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (strategy_id) REFERENCES strategy_profiles(strategy_id)
);

CREATE TABLE governance_reviews (
    governance_id TEXT PRIMARY KEY,
    strategy_id TEXT NOT NULL,
    governance_practice TEXT NOT NULL,
    decision_rights_clarity REAL CHECK (decision_rights_clarity BETWEEN 0 AND 1),
    evidence_standard_quality REAL CHECK (evidence_standard_quality BETWEEN 0 AND 1),
    revision_authority_clarity REAL CHECK (revision_authority_clarity BETWEEN 0 AND 1),
    ethical_threshold_quality REAL CHECK (ethical_threshold_quality BETWEEN 0 AND 1),
    stakeholder_review_quality REAL CHECK (stakeholder_review_quality BETWEEN 0 AND 1),
    documentation_quality REAL CHECK (documentation_quality BETWEEN 0 AND 1),
    accountability_quality REAL CHECK (accountability_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (strategy_id) REFERENCES strategy_profiles(strategy_id)
);

CREATE TABLE learning_memory (
    memory_id TEXT PRIMARY KEY,
    strategy_id TEXT NOT NULL,
    memory_practice TEXT NOT NULL,
    assumption_record_quality REAL CHECK (assumption_record_quality BETWEEN 0 AND 1),
    feedback_record_quality REAL CHECK (feedback_record_quality BETWEEN 0 AND 1),
    interpretation_quality REAL CHECK (interpretation_quality BETWEEN 0 AND 1),
    revision_rationale_quality REAL CHECK (revision_rationale_quality BETWEEN 0 AND 1),
    decision_traceability REAL CHECK (decision_traceability BETWEEN 0 AND 1),
    remaining_uncertainty_quality REAL CHECK (remaining_uncertainty_quality BETWEEN 0 AND 1),
    reuse_quality REAL CHECK (reuse_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (strategy_id) REFERENCES strategy_profiles(strategy_id)
);

CREATE VIEW adaptive_strategy_profile_scores AS
SELECT
    strategy_id,
    strategy_name,
    ROUND(
      0.13 * flexibility +
      0.15 * learning_capacity +
      0.09 * exploration +
      0.11 * exploitation_balance +
      0.15 * coherence +
      0.13 * feedback_intelligence +
      0.10 * governance +
      0.08 * systems_awareness +
      0.06 * learning_memory,
      4
    ) AS adaptive_strategy_score,
    ROUND(
      0.20 * flexibility * (1 - coherence) +
      0.18 * (1 - governance) +
      0.16 * (1 - feedback_intelligence) +
      0.14 * (1 - learning_capacity) +
      0.12 * (1 - exploitation_balance) +
      0.10 * (1 - learning_memory) +
      0.10 * (1 - systems_awareness),
      4
    ) AS over_adaptation_risk
FROM strategy_profiles;

CREATE VIEW feedback_signal_scores AS
SELECT
    signal_id,
    strategy_id,
    signal_type,
    signal_description,
    ROUND(
      0.18 * signal_strength +
      0.16 * decision_relevance +
      0.16 * stakeholder_impact +
      0.16 * systems_relevance +
      0.12 * delay_risk -
      0.14 * noise_risk +
      0.08 * interpretation_quality,
      4
    ) AS response_priority
FROM feedback_signals;

CREATE VIEW assumption_revision_scores AS
SELECT
    assumption_id,
    strategy_id,
    assumption,
    assumption_type,
    ROUND(0.50 * uncertainty + 0.50 * consequence, 4) AS criticality,
    ROUND(
      0.24 * uncertainty +
      0.24 * consequence +
      0.22 * decay_risk -
      0.16 * evidence_strength -
      0.08 * revision_readiness -
      0.06 * owner_clarity,
      4
    ) AS revision_need
FROM assumption_register;

CREATE VIEW trigger_condition_scores AS
SELECT
    trigger_id,
    strategy_id,
    trigger_name,
    ROUND(
      0.15 * trigger_clarity +
      0.15 * evidence_threshold +
      0.16 * decision_path_clarity +
      0.13 * response_speed_fit +
      0.13 * ethical_safeguards +
      0.13 * authority_clarity +
      0.15 * monitoring_quality,
      4
    ) AS trigger_condition_score
FROM trigger_conditions;

CREATE VIEW experiment_portfolio_scores AS
SELECT
    experiment_id,
    strategy_id,
    experiment_type,
    ROUND(
      0.16 * critical_assumption_fit +
      0.16 * evidence_standard_quality +
      0.17 * learning_value +
      0.16 * decision_linkage +
      0.11 * resource_fit +
      0.12 * scale_relevance +
      0.12 * ethical_review,
      4
    ) AS experiment_score
FROM experiment_portfolio;

CREATE VIEW timing_responsiveness_scores AS
SELECT
    timing_id,
    strategy_id,
    timing_issue,
    ROUND(
      0.11 * response_speed +
      0.16 * signal_interpretation +
      0.15 * noise_filtering +
      0.13 * delay_awareness +
      0.14 * revision_cadence +
      0.13 * stakeholder_communication +
      0.18 * stability_preservation,
      4
    ) AS timing_discipline_score,
    ROUND(
      0.25 * response_speed * (1 - noise_filtering) +
      0.20 * (1 - signal_interpretation) +
      0.18 * (1 - stability_preservation) +
      0.15 * (1 - revision_cadence) +
      0.12 * (1 - stakeholder_communication) +
      0.10 * (1 - delay_awareness),
      4
    ) AS whiplash_risk
FROM timing_responsiveness;

CREATE VIEW exploration_exploitation_scores AS
SELECT
    portfolio_id,
    strategy_id,
    portfolio_name,
    ROUND(
      0.15 * exploration_strength +
      0.15 * exploitation_strength +
      0.18 * balance_quality +
      0.14 * option_value +
      0.13 * resource_discipline +
      0.13 * focus_quality +
      0.12 * transition_path_quality,
      4
    ) AS portfolio_balance_score
FROM portfolio_balance;

CREATE VIEW systems_impact_scores AS
SELECT
    impact_id,
    strategy_id,
    systems_issue,
    ROUND(
      0.14 * feedback_loop_risk +
      0.13 * delay_risk +
      0.16 * burden_shift_risk +
      0.15 * capacity_risk +
      0.12 * incentive_risk +
      0.14 * scale_uncertainty -
      0.16 * monitoring_quality,
      4
    ) AS systems_impact_risk
FROM systems_impacts;

CREATE VIEW adaptive_governance_scores AS
SELECT
    governance_id,
    strategy_id,
    governance_practice,
    ROUND(
      0.15 * decision_rights_clarity +
      0.15 * evidence_standard_quality +
      0.14 * revision_authority_clarity +
      0.14 * ethical_threshold_quality +
      0.13 * stakeholder_review_quality +
      0.14 * documentation_quality +
      0.15 * accountability_quality,
      4
    ) AS adaptive_governance_score
FROM governance_reviews;

CREATE VIEW learning_memory_scores AS
SELECT
    memory_id,
    strategy_id,
    memory_practice,
    ROUND(
      0.14 * assumption_record_quality +
      0.14 * feedback_record_quality +
      0.15 * interpretation_quality +
      0.15 * revision_rationale_quality +
      0.14 * decision_traceability +
      0.14 * remaining_uncertainty_quality +
      0.14 * reuse_quality,
      4
    ) AS learning_memory_score
FROM learning_memory;
