-- Advanced SQL schema for Alignment Drift and Strategic Coherence.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS coherence_scores;
DROP VIEW IF EXISTS drift_signal_scores;
DROP VIEW IF EXISTS resource_alignment_scores;
DROP VIEW IF EXISTS incentive_metric_scores;
DROP VIEW IF EXISTS governance_strength_scores;
DROP VIEW IF EXISTS ethics_power_scores;

DROP TABLE IF EXISTS ethics_power;
DROP TABLE IF EXISTS governance_reviews;
DROP TABLE IF EXISTS incentives_metrics;
DROP TABLE IF EXISTS resource_alignment;
DROP TABLE IF EXISTS drift_signals;
DROP TABLE IF EXISTS coherence_contexts;

CREATE TABLE coherence_contexts (
    context_id TEXT PRIMARY KEY,
    context_name TEXT NOT NULL,
    context_type TEXT NOT NULL,
    purpose_clarity REAL CHECK (purpose_clarity BETWEEN 0 AND 1),
    priority_discipline REAL CHECK (priority_discipline BETWEEN 0 AND 1),
    tradeoff_integrity REAL CHECK (tradeoff_integrity BETWEEN 0 AND 1),
    resource_alignment REAL CHECK (resource_alignment BETWEEN 0 AND 1),
    incentive_fit REAL CHECK (incentive_fit BETWEEN 0 AND 1),
    interpretive_consistency REAL CHECK (interpretive_consistency BETWEEN 0 AND 1),
    governance_strength REAL CHECK (governance_strength BETWEEN 0 AND 1),
    feedback_quality REAL CHECK (feedback_quality BETWEEN 0 AND 1),
    decision_memory REAL CHECK (decision_memory BETWEEN 0 AND 1),
    ethical_coherence REAL CHECK (ethical_coherence BETWEEN 0 AND 1),
    adaptive_capacity REAL CHECK (adaptive_capacity BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE drift_signals (
    signal_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    signal_type TEXT,
    signal_name TEXT,
    signal_strength REAL,
    evidence_quality REAL,
    visibility REAL,
    correction_difficulty REAL,
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES coherence_contexts(context_id)
);

CREATE TABLE resource_alignment (
    resource_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    budget_alignment REAL,
    staff_alignment REAL,
    leadership_attention REAL,
    technical_support REAL,
    governance_bandwidth REAL,
    communication_capacity REAL,
    portfolio_focus REAL,
    opportunity_cost_visibility REAL,
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES coherence_contexts(context_id)
);

CREATE TABLE incentives_metrics (
    metric_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    indicator_fit REAL,
    reward_alignment REAL,
    local_optimization_risk REAL,
    metric_gaming_risk REAL,
    short_termism REAL,
    qualitative_review_strength REAL,
    stakeholder_metric_balance REAL,
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES coherence_contexts(context_id)
);

CREATE TABLE governance_reviews (
    governance_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    review_cadence REAL,
    decision_authority REAL,
    assumption_review REAL,
    tradeoff_review REAL,
    stop_rule_quality REAL,
    resource_reallocation_power REAL,
    escalation_clarity REAL,
    decision_memory_quality REAL,
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES coherence_contexts(context_id)
);

CREATE TABLE ethics_power (
    ethics_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    ethical_issue TEXT,
    sponsor_power REAL,
    affected_stakeholder_voice REAL,
    benefit_concentration REAL,
    burden_concentration REAL,
    transparency REAL,
    redress_quality REAL,
    pause_authority REAL,
    long_term_responsibility REAL,
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES coherence_contexts(context_id)
);

CREATE VIEW coherence_scores AS
SELECT
    context_id,
    context_name,
    context_type,
    ROUND(
      0.13 * purpose_clarity +
      0.12 * priority_discipline +
      0.11 * tradeoff_integrity +
      0.12 * resource_alignment +
      0.12 * incentive_fit +
      0.10 * interpretive_consistency +
      0.11 * governance_strength +
      0.09 * feedback_quality +
      0.06 * decision_memory +
      0.07 * ethical_coherence +
      0.07 * adaptive_capacity,
      4
    ) AS strategic_coherence_score,
    ROUND(
      0.13 * (1 - purpose_clarity) +
      0.12 * (1 - priority_discipline) +
      0.11 * (1 - tradeoff_integrity) +
      0.12 * (1 - resource_alignment) +
      0.13 * (1 - incentive_fit) +
      0.10 * (1 - interpretive_consistency) +
      0.11 * (1 - governance_strength) +
      0.08 * (1 - feedback_quality) +
      0.06 * (1 - decision_memory) +
      0.07 * (1 - ethical_coherence) +
      0.07 * (1 - adaptive_capacity),
      4
    ) AS alignment_drift_risk
FROM coherence_contexts;

CREATE VIEW drift_signal_scores AS
SELECT
    signal_id,
    context_id,
    signal_type,
    signal_name,
    ROUND(
      0.34 * signal_strength +
      0.22 * correction_difficulty +
      0.18 * visibility +
      0.16 * evidence_quality +
      0.10,
      4
    ) AS drift_signal_risk
FROM drift_signals;

CREATE VIEW resource_alignment_scores AS
SELECT
    resource_id,
    context_id,
    ROUND(
      0.14 * budget_alignment +
      0.14 * staff_alignment +
      0.13 * leadership_attention +
      0.12 * technical_support +
      0.13 * governance_bandwidth +
      0.11 * communication_capacity +
      0.12 * portfolio_focus +
      0.11 * opportunity_cost_visibility,
      4
    ) AS resource_alignment_score
FROM resource_alignment;

CREATE VIEW incentive_metric_scores AS
SELECT
    metric_id,
    context_id,
    ROUND(
      0.25 * metric_gaming_risk +
      0.22 * local_optimization_risk +
      0.18 * short_termism +
      0.15 * (1 - indicator_fit) +
      0.12 * (1 - reward_alignment) +
      0.08 * (1 - stakeholder_metric_balance),
      4
    ) AS metric_distortion_risk
FROM incentives_metrics;

CREATE VIEW governance_strength_scores AS
SELECT
    governance_id,
    context_id,
    ROUND(
      0.12 * review_cadence +
      0.16 * decision_authority +
      0.14 * assumption_review +
      0.13 * tradeoff_review +
      0.13 * stop_rule_quality +
      0.14 * resource_reallocation_power +
      0.09 * escalation_clarity +
      0.09 * decision_memory_quality,
      4
    ) AS governance_strength_score
FROM governance_reviews;

CREATE VIEW ethics_power_scores AS
SELECT
    ethics_id,
    context_id,
    ethical_issue,
    ROUND(
      0.13 * sponsor_power +
      0.16 * (1 - affected_stakeholder_voice) +
      0.13 * benefit_concentration +
      0.16 * burden_concentration +
      0.11 * (1 - transparency) +
      0.10 * (1 - redress_quality) +
      0.10 * (1 - pause_authority) +
      0.11 * (1 - long_term_responsibility),
      4
    ) AS power_risk
FROM ethics_power;
