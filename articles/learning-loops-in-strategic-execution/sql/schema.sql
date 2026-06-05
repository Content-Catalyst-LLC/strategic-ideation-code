-- Advanced SQL schema for Learning Loops in Strategic Execution.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS learning_loop_scores;
DROP VIEW IF EXISTS feedback_quality_scores;
DROP VIEW IF EXISTS assumption_review_scores;
DROP VIEW IF EXISTS governance_learning_scores;
DROP VIEW IF EXISTS knowledge_scaling_scores;
DROP VIEW IF EXISTS ethics_power_scores;

DROP TABLE IF EXISTS ethics_power;
DROP TABLE IF EXISTS knowledge_scaling;
DROP TABLE IF EXISTS governance_learning;
DROP TABLE IF EXISTS assumption_reviews;
DROP TABLE IF EXISTS feedback_quality;
DROP TABLE IF EXISTS learning_contexts;

CREATE TABLE learning_contexts (
    context_id TEXT PRIMARY KEY,
    context_name TEXT NOT NULL,
    context_type TEXT NOT NULL,
    feedback_quality REAL CHECK (feedback_quality BETWEEN 0 AND 1),
    assumption_review REAL CHECK (assumption_review BETWEEN 0 AND 1),
    interpretation_discipline REAL CHECK (interpretation_discipline BETWEEN 0 AND 1),
    decision_authority REAL CHECK (decision_authority BETWEEN 0 AND 1),
    learning_closure REAL CHECK (learning_closure BETWEEN 0 AND 1),
    decision_memory REAL CHECK (decision_memory BETWEEN 0 AND 1),
    psychological_safety REAL CHECK (psychological_safety BETWEEN 0 AND 1),
    knowledge_scaling REAL CHECK (knowledge_scaling BETWEEN 0 AND 1),
    ethical_learning REAL CHECK (ethical_learning BETWEEN 0 AND 1),
    strategic_coherence REAL CHECK (strategic_coherence BETWEEN 0 AND 1),
    adaptive_capacity REAL CHECK (adaptive_capacity BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE feedback_quality (
    feedback_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    source_type TEXT,
    reliability REAL,
    timeliness REAL,
    contextual_relevance REAL,
    validity REAL,
    triangulation REAL,
    stakeholder_coverage REAL,
    noise_risk REAL,
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES learning_contexts(context_id)
);

CREATE TABLE assumption_reviews (
    assumption_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    assumption_type TEXT,
    assumption_name TEXT,
    explicitness REAL,
    evidence_linkage REAL,
    review_frequency REAL,
    failure_visibility REAL,
    revision_trigger_quality REAL,
    owner_clarity REAL,
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES learning_contexts(context_id)
);

CREATE TABLE governance_learning (
    governance_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    review_cadence REAL,
    decision_authority REAL,
    resource_reallocation_power REAL,
    revision_trigger_quality REAL,
    stop_rule_quality REAL,
    escalation_clarity REAL,
    lesson_owner_clarity REAL,
    follow_up_discipline REAL,
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES learning_contexts(context_id)
);

CREATE TABLE knowledge_scaling (
    scaling_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    template_quality REAL,
    metadata_quality REAL,
    repository_usability REAL,
    cross_team_reuse REAL,
    portfolio_synthesis REAL,
    onboarding_reuse REAL,
    searchability REAL,
    stewardship REAL,
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES learning_contexts(context_id)
);

CREATE TABLE ethics_power (
    ethics_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    ethical_issue TEXT,
    sponsor_power REAL,
    affected_stakeholder_voice REAL,
    frontline_voice REAL,
    burden_visibility REAL,
    interpretive_power_balance REAL,
    redress_quality REAL,
    pause_authority REAL,
    lesson_return REAL,
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES learning_contexts(context_id)
);

CREATE VIEW learning_loop_scores AS
SELECT
    context_id,
    context_name,
    context_type,
    ROUND(
      0.12 * feedback_quality +
      0.12 * assumption_review +
      0.11 * interpretation_discipline +
      0.13 * decision_authority +
      0.13 * learning_closure +
      0.10 * decision_memory +
      0.08 * psychological_safety +
      0.08 * knowledge_scaling +
      0.08 * ethical_learning +
      0.07 * strategic_coherence +
      0.08 * adaptive_capacity,
      4
    ) AS learning_loop_strength,
    ROUND(
      0.11 * (1 - feedback_quality) +
      0.12 * (1 - assumption_review) +
      0.10 * (1 - interpretation_discipline) +
      0.14 * (1 - decision_authority) +
      0.14 * (1 - learning_closure) +
      0.11 * (1 - decision_memory) +
      0.08 * (1 - psychological_safety) +
      0.08 * (1 - knowledge_scaling) +
      0.08 * (1 - ethical_learning) +
      0.07 * (1 - strategic_coherence) +
      0.07 * (1 - adaptive_capacity),
      4
    ) AS learning_failure_risk
FROM learning_contexts;

CREATE VIEW feedback_quality_scores AS
SELECT
    feedback_id,
    context_id,
    source_type,
    ROUND(
      0.16 * reliability +
      0.15 * timeliness +
      0.16 * contextual_relevance +
      0.16 * validity +
      0.13 * triangulation +
      0.13 * stakeholder_coverage -
      0.11 * noise_risk +
      0.11,
      4
    ) AS feedback_quality_score
FROM feedback_quality;

CREATE VIEW assumption_review_scores AS
SELECT
    assumption_id,
    context_id,
    assumption_type,
    assumption_name,
    ROUND(
      0.16 * explicitness +
      0.18 * evidence_linkage +
      0.15 * review_frequency +
      0.14 * failure_visibility +
      0.20 * revision_trigger_quality +
      0.17 * owner_clarity,
      4
    ) AS assumption_review_score
FROM assumption_reviews;

CREATE VIEW governance_learning_scores AS
SELECT
    governance_id,
    context_id,
    ROUND(
      0.11 * review_cadence +
      0.16 * decision_authority +
      0.14 * resource_reallocation_power +
      0.15 * revision_trigger_quality +
      0.13 * stop_rule_quality +
      0.10 * escalation_clarity +
      0.10 * lesson_owner_clarity +
      0.11 * follow_up_discipline,
      4
    ) AS governance_learning_score
FROM governance_learning;

CREATE VIEW knowledge_scaling_scores AS
SELECT
    scaling_id,
    context_id,
    ROUND(
      0.13 * template_quality +
      0.13 * metadata_quality +
      0.13 * repository_usability +
      0.14 * cross_team_reuse +
      0.13 * portfolio_synthesis +
      0.11 * onboarding_reuse +
      0.12 * searchability +
      0.11 * stewardship,
      4
    ) AS knowledge_scaling_score
FROM knowledge_scaling;

CREATE VIEW ethics_power_scores AS
SELECT
    ethics_id,
    context_id,
    ethical_issue,
    ROUND(
      0.13 * sponsor_power +
      0.14 * (1 - affected_stakeholder_voice) +
      0.13 * (1 - frontline_voice) +
      0.14 * (1 - burden_visibility) +
      0.14 * (1 - interpretive_power_balance) +
      0.11 * (1 - redress_quality) +
      0.11 * (1 - pause_authority) +
      0.10 * (1 - lesson_return),
      4
    ) AS learning_power_risk
FROM ethics_power;
