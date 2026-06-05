-- Advanced SQL schema for Measuring Strategic Effectiveness.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS strategic_effectiveness_scores;
DROP VIEW IF EXISTS indicator_quality_scores;
DROP VIEW IF EXISTS evidence_confidence_scores;
DROP VIEW IF EXISTS feedback_learning_scores;
DROP VIEW IF EXISTS ethics_power_scores;

DROP TABLE IF EXISTS ethics_power;
DROP TABLE IF EXISTS feedback_learning;
DROP TABLE IF EXISTS evidence_confidence;
DROP TABLE IF EXISTS indicator_quality;
DROP TABLE IF EXISTS strategies;

CREATE TABLE strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy_name TEXT NOT NULL,
    strategy_type TEXT NOT NULL,
    performance REAL CHECK (performance BETWEEN 0 AND 1),
    alignment REAL CHECK (alignment BETWEEN 0 AND 1),
    resilience REAL CHECK (resilience BETWEEN 0 AND 1),
    adaptability REAL CHECK (adaptability BETWEEN 0 AND 1),
    impact REAL CHECK (impact BETWEEN 0 AND 1),
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    evidence_confidence REAL CHECK (evidence_confidence BETWEEN 0 AND 1),
    ethical_resilience REAL CHECK (ethical_resilience BETWEEN 0 AND 1),
    measurement_burden REAL CHECK (measurement_burden BETWEEN 0 AND 1),
    strategic_fit REAL CHECK (strategic_fit BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE indicator_quality (
    indicator_id TEXT PRIMARY KEY,
    strategy_id TEXT NOT NULL,
    indicator_set TEXT,
    leading_indicator_quality REAL,
    lagging_indicator_quality REAL,
    balance_quality REAL,
    data_reliability REAL,
    timeliness REAL,
    interpretability REAL,
    behavioral_incentive_risk REAL,
    coverage_gap REAL,
    review_action TEXT,
    FOREIGN KEY (strategy_id) REFERENCES strategies(strategy_id)
);

CREATE TABLE evidence_confidence (
    evidence_id TEXT PRIMARY KEY,
    strategy_id TEXT NOT NULL,
    baseline_quality REAL,
    comparison_quality REAL,
    causal_plausibility REAL,
    data_completeness REAL,
    stakeholder_evidence REAL,
    qualitative_depth REAL,
    uncertainty_tracking REAL,
    decision_use REAL,
    review_action TEXT,
    FOREIGN KEY (strategy_id) REFERENCES strategies(strategy_id)
);

CREATE TABLE feedback_learning (
    feedback_id TEXT PRIMARY KEY,
    strategy_id TEXT NOT NULL,
    feedback_frequency REAL,
    assumption_review REAL,
    revision_trigger_quality REAL,
    after_action_learning REAL,
    drift_detection REAL,
    adaptation_authority REAL,
    decision_memory_quality REAL,
    learning_culture REAL,
    review_action TEXT,
    FOREIGN KEY (strategy_id) REFERENCES strategies(strategy_id)
);

CREATE TABLE ethics_power (
    ethics_id TEXT PRIMARY KEY,
    strategy_id TEXT NOT NULL,
    ethical_issue TEXT,
    sponsor_power REAL,
    affected_stakeholder_voice REAL,
    benefit_concentration REAL,
    burden_concentration REAL,
    measurement_transparency REAL,
    redress_quality REAL,
    long_term_responsibility REAL,
    review_action TEXT,
    FOREIGN KEY (strategy_id) REFERENCES strategies(strategy_id)
);

CREATE VIEW strategic_effectiveness_scores AS
SELECT
    strategy_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.18 * performance +
      0.14 * alignment +
      0.15 * resilience +
      0.15 * adaptability +
      0.13 * impact +
      0.10 * learning_value +
      0.06 * evidence_confidence +
      0.06 * ethical_resilience -
      0.05 * measurement_burden +
      0.08 * strategic_fit,
      4
    ) AS strategic_effectiveness_score,
    ROUND(
      (
        0.18 * performance +
        0.14 * alignment +
        0.15 * resilience +
        0.15 * adaptability +
        0.13 * impact +
        0.10 * learning_value +
        0.06 * evidence_confidence +
        0.06 * ethical_resilience -
        0.05 * measurement_burden +
        0.08 * strategic_fit
      ) * evidence_confidence,
      4
    ) AS confidence_adjusted_effectiveness
FROM strategies;

CREATE VIEW indicator_quality_scores AS
SELECT
    indicator_id,
    strategy_id,
    ROUND(
      0.16 * leading_indicator_quality +
      0.14 * lagging_indicator_quality +
      0.16 * balance_quality +
      0.14 * data_reliability +
      0.10 * timeliness +
      0.12 * interpretability -
      0.10 * behavioral_incentive_risk -
      0.08 * coverage_gap +
      0.10,
      4
    ) AS indicator_quality_score
FROM indicator_quality;

CREATE VIEW evidence_confidence_scores AS
SELECT
    evidence_id,
    strategy_id,
    ROUND(
      0.14 * baseline_quality +
      0.14 * comparison_quality +
      0.16 * causal_plausibility +
      0.13 * data_completeness +
      0.13 * stakeholder_evidence +
      0.12 * qualitative_depth +
      0.10 * uncertainty_tracking +
      0.08 * decision_use,
      4
    ) AS evidence_confidence_score
FROM evidence_confidence;

CREATE VIEW feedback_learning_scores AS
SELECT
    feedback_id,
    strategy_id,
    ROUND(
      0.12 * feedback_frequency +
      0.14 * assumption_review +
      0.14 * revision_trigger_quality +
      0.13 * after_action_learning +
      0.13 * drift_detection +
      0.12 * adaptation_authority +
      0.11 * decision_memory_quality +
      0.11 * learning_culture,
      4
    ) AS feedback_learning_score
FROM feedback_learning;

CREATE VIEW ethics_power_scores AS
SELECT
    ethics_id,
    strategy_id,
    ethical_issue,
    ROUND(
      0.16 * sponsor_power +
      0.18 * (1 - affected_stakeholder_voice) +
      0.16 * benefit_concentration +
      0.18 * burden_concentration +
      0.12 * (1 - measurement_transparency) +
      0.10 * (1 - redress_quality) +
      0.10 * (1 - long_term_responsibility),
      4
    ) AS power_risk
FROM ethics_power;
