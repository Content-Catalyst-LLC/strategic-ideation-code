-- Advanced SQL schema for Opportunity Recognition and Evaluation.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS opportunity_profile_scores;
DROP VIEW IF EXISTS signal_quality_scores;
DROP VIEW IF EXISTS capability_alignment_scores;
DROP VIEW IF EXISTS timing_window_scores;
DROP VIEW IF EXISTS risk_and_error_scores;
DROP VIEW IF EXISTS ethics_power_scores;
DROP VIEW IF EXISTS learning_pathway_scores;
DROP VIEW IF EXISTS governance_review_scores;
DROP VIEW IF EXISTS decision_memory_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS governance_review;
DROP TABLE IF EXISTS learning_pathways;
DROP TABLE IF EXISTS ethics_power;
DROP TABLE IF EXISTS risk_errors;
DROP TABLE IF EXISTS timing_windows;
DROP TABLE IF EXISTS capability_alignment;
DROP TABLE IF EXISTS signal_quality;
DROP TABLE IF EXISTS opportunities;

CREATE TABLE opportunities (
    opportunity_id TEXT PRIMARY KEY,
    opportunity_name TEXT NOT NULL,
    opportunity_type TEXT NOT NULL,
    signal_strength REAL CHECK (signal_strength BETWEEN 0 AND 1),
    capability_alignment REAL CHECK (capability_alignment BETWEEN 0 AND 1),
    desirability REAL CHECK (desirability BETWEEN 0 AND 1),
    viability REAL CHECK (viability BETWEEN 0 AND 1),
    timing REAL CHECK (timing BETWEEN 0 AND 1),
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    option_value REAL CHECK (option_value BETWEEN 0 AND 1),
    strategic_fit REAL CHECK (strategic_fit BETWEEN 0 AND 1),
    ethical_resilience REAL CHECK (ethical_resilience BETWEEN 0 AND 1),
    risk REAL CHECK (risk BETWEEN 0 AND 1),
    evidence_confidence REAL CHECK (evidence_confidence BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE signal_quality (
    signal_id TEXT PRIMARY KEY,
    opportunity_id TEXT NOT NULL,
    signal_source TEXT,
    repeatability REAL,
    independence REAL,
    specificity REAL,
    trend_strength REAL,
    stakeholder_confirmation REAL,
    noise_level REAL,
    hype_level REAL,
    review_action TEXT,
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(opportunity_id)
);

CREATE TABLE capability_alignment (
    capability_id TEXT PRIMARY KEY,
    opportunity_id TEXT NOT NULL,
    skills_fit REAL,
    asset_fit REAL,
    authority_fit REAL,
    partnership_fit REAL,
    governance_fit REAL,
    implementation_capacity REAL,
    credibility_fit REAL,
    capability_gap REAL,
    review_action TEXT,
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(opportunity_id)
);

CREATE TABLE timing_windows (
    timing_id TEXT PRIMARY KEY,
    opportunity_id TEXT NOT NULL,
    readiness REAL,
    momentum REAL,
    window_width REAL,
    urgency REAL,
    ecosystem_maturity REAL,
    policy_timing REAL,
    competitive_pressure REAL,
    option_expiration_risk REAL,
    review_action TEXT,
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(opportunity_id)
);

CREATE TABLE risk_errors (
    risk_id TEXT PRIMARY KEY,
    opportunity_id TEXT NOT NULL,
    false_positive_cost REAL,
    false_negative_cost REAL,
    implementation_risk REAL,
    strategic_distraction REAL,
    opportunity_cost REAL,
    ethical_risk REAL,
    reputational_risk REAL,
    uncertainty_level REAL,
    review_action TEXT,
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(opportunity_id)
);

CREATE TABLE ethics_power (
    ethics_id TEXT PRIMARY KEY,
    opportunity_id TEXT NOT NULL,
    ethical_issue TEXT,
    sponsor_power REAL,
    affected_stakeholder_voice REAL,
    benefit_concentration REAL,
    burden_concentration REAL,
    transparency REAL,
    redress_quality REAL,
    long_term_responsibility REAL,
    review_action TEXT,
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(opportunity_id)
);

CREATE TABLE learning_pathways (
    learning_id TEXT PRIMARY KEY,
    opportunity_id TEXT NOT NULL,
    critical_assumption TEXT,
    smallest_responsible_test TEXT,
    evidence_threshold REAL,
    learning_value REAL,
    test_cost REAL,
    decision_gate TEXT,
    stop_rule_quality REAL,
    review_action TEXT,
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(opportunity_id)
);

CREATE TABLE governance_review (
    governance_id TEXT PRIMARY KEY,
    opportunity_id TEXT NOT NULL,
    owner_clarity REAL,
    review_cadence REAL,
    evidence_standard REAL,
    decision_gate_quality REAL,
    stakeholder_voice REAL,
    ethics_review REAL,
    stop_rule_quality REAL,
    decision_memory_quality REAL,
    review_action TEXT,
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(opportunity_id)
);

CREATE TABLE decision_memory (
    memory_id TEXT PRIMARY KEY,
    opportunity_id TEXT NOT NULL,
    memory_practice TEXT,
    signal_record REAL,
    capability_record REAL,
    assumption_record REAL,
    evidence_record REAL,
    risk_record REAL,
    ethics_record REAL,
    timing_record REAL,
    decision_gate_record REAL,
    revision_trigger_quality REAL,
    reuse_quality REAL,
    review_action TEXT,
    FOREIGN KEY (opportunity_id) REFERENCES opportunities(opportunity_id)
);

CREATE VIEW opportunity_profile_scores AS
SELECT
    opportunity_id,
    opportunity_name,
    opportunity_type,
    ROUND(
      0.13 * signal_strength +
      0.14 * capability_alignment +
      0.12 * desirability +
      0.12 * viability +
      0.10 * timing +
      0.12 * learning_value +
      0.11 * option_value +
      0.10 * strategic_fit +
      0.10 * ethical_resilience -
      0.14 * risk,
      4
    ) AS profile_score,
    ROUND(
      (
        0.13 * signal_strength +
        0.14 * capability_alignment +
        0.12 * desirability +
        0.12 * viability +
        0.10 * timing +
        0.12 * learning_value +
        0.11 * option_value +
        0.10 * strategic_fit +
        0.10 * ethical_resilience -
        0.14 * risk
      ) * evidence_confidence,
      4
    ) AS confidence_adjusted_score
FROM opportunities;

CREATE VIEW signal_quality_scores AS
SELECT
    signal_id,
    opportunity_id,
    ROUND(
      0.18 * repeatability +
      0.17 * independence +
      0.16 * specificity +
      0.16 * trend_strength +
      0.17 * stakeholder_confirmation -
      0.08 * noise_level -
      0.08 * hype_level,
      4
    ) AS signal_quality_score
FROM signal_quality;

CREATE VIEW capability_alignment_scores AS
SELECT
    capability_id,
    opportunity_id,
    ROUND(
      0.16 * skills_fit +
      0.15 * asset_fit +
      0.14 * authority_fit +
      0.14 * partnership_fit +
      0.14 * governance_fit +
      0.14 * implementation_capacity +
      0.13 * credibility_fit -
      0.10 * capability_gap,
      4
    ) AS capability_score
FROM capability_alignment;

CREATE VIEW timing_window_scores AS
SELECT
    timing_id,
    opportunity_id,
    ROUND(
      0.17 * readiness +
      0.15 * momentum +
      0.14 * window_width +
      0.12 * urgency +
      0.15 * ecosystem_maturity +
      0.14 * policy_timing +
      0.07 * competitive_pressure -
      0.06 * option_expiration_risk,
      4
    ) AS timing_strength
FROM timing_windows;

CREATE VIEW risk_and_error_scores AS
SELECT
    risk_id,
    opportunity_id,
    ROUND(
      0.20 * false_positive_cost +
      0.16 * implementation_risk +
      0.16 * strategic_distraction +
      0.16 * opportunity_cost +
      0.12 * ethical_risk +
      0.10 * reputational_risk +
      0.10 * uncertainty_level,
      4
    ) AS false_positive_risk,
    ROUND(
      0.40 * false_negative_cost +
      0.18 * (1 - implementation_risk) +
      0.14 * (1 - ethical_risk) +
      0.14 * (1 - reputational_risk) +
      0.14 * uncertainty_level,
      4
    ) AS missed_opportunity_risk
FROM risk_errors;

CREATE VIEW ethics_power_scores AS
SELECT
    ethics_id,
    opportunity_id,
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

CREATE VIEW learning_pathway_scores AS
SELECT
    learning_id,
    opportunity_id,
    critical_assumption,
    smallest_responsible_test,
    ROUND(
      0.26 * learning_value +
      0.22 * evidence_threshold +
      0.18 * stop_rule_quality +
      0.14 * (1 - test_cost) +
      0.20,
      4
    ) AS learning_pathway_score
FROM learning_pathways;

CREATE VIEW governance_review_scores AS
SELECT
    governance_id,
    opportunity_id,
    ROUND(
      0.12 * owner_clarity +
      0.12 * review_cadence +
      0.14 * evidence_standard +
      0.14 * decision_gate_quality +
      0.13 * stakeholder_voice +
      0.13 * ethics_review +
      0.11 * stop_rule_quality +
      0.11 * decision_memory_quality,
      4
    ) AS governance_score
FROM governance_review;

CREATE VIEW decision_memory_scores AS
SELECT
    memory_id,
    opportunity_id,
    memory_practice,
    ROUND(
      0.09 * signal_record +
      0.09 * capability_record +
      0.10 * assumption_record +
      0.10 * evidence_record +
      0.10 * risk_record +
      0.11 * ethics_record +
      0.10 * timing_record +
      0.11 * decision_gate_record +
      0.10 * revision_trigger_quality +
      0.10 * reuse_quality,
      4
    ) AS decision_memory_score
FROM decision_memory;
