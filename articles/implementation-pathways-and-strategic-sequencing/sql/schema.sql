-- Advanced SQL schema for Implementation Pathways and Strategic Sequencing.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS pathway_readiness_scores;
DROP VIEW IF EXISTS dependency_risk_scores;
DROP VIEW IF EXISTS capacity_load_scores;
DROP VIEW IF EXISTS timing_window_scores;
DROP VIEW IF EXISTS reversibility_lockin_scores;
DROP VIEW IF EXISTS ethics_power_scores;

DROP TABLE IF EXISTS ethics_power;
DROP TABLE IF EXISTS reversibility_lockin;
DROP TABLE IF EXISTS timing_windows;
DROP TABLE IF EXISTS capacity_load;
DROP TABLE IF EXISTS dependencies;
DROP TABLE IF EXISTS pathways;

CREATE TABLE pathways (
    pathway_id TEXT PRIMARY KEY,
    pathway_name TEXT NOT NULL,
    pathway_type TEXT NOT NULL,
    capability_readiness REAL CHECK (capability_readiness BETWEEN 0 AND 1),
    evidence_strength REAL CHECK (evidence_strength BETWEEN 0 AND 1),
    governance_readiness REAL CHECK (governance_readiness BETWEEN 0 AND 1),
    legitimacy REAL CHECK (legitimacy BETWEEN 0 AND 1),
    dependency_load REAL CHECK (dependency_load BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    capacity_demand REAL CHECK (capacity_demand BETWEEN 0 AND 1),
    timing_urgency REAL CHECK (timing_urgency BETWEEN 0 AND 1),
    ethical_resilience REAL CHECK (ethical_resilience BETWEEN 0 AND 1),
    feedback_strength REAL CHECK (feedback_strength BETWEEN 0 AND 1),
    strategic_fit REAL CHECK (strategic_fit BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE dependencies (
    dependency_id TEXT PRIMARY KEY,
    pathway_id TEXT NOT NULL,
    dependency_type TEXT,
    dependency_name TEXT,
    dependency_strength REAL,
    readiness_level REAL,
    bottleneck_risk REAL,
    owner_clarity REAL,
    review_action TEXT,
    FOREIGN KEY (pathway_id) REFERENCES pathways(pathway_id)
);

CREATE TABLE capacity_load (
    capacity_id TEXT PRIMARY KEY,
    pathway_id TEXT NOT NULL,
    budget_load REAL,
    staff_load REAL,
    technical_load REAL,
    governance_load REAL,
    leadership_attention_load REAL,
    stakeholder_participation_load REAL,
    operational_disruption REAL,
    absorptive_capacity REAL,
    review_action TEXT,
    FOREIGN KEY (pathway_id) REFERENCES pathways(pathway_id)
);

CREATE TABLE timing_windows (
    timing_id TEXT PRIMARY KEY,
    pathway_id TEXT NOT NULL,
    external_window_strength REAL,
    internal_readiness REAL,
    urgency_quality REAL,
    delay_cost REAL,
    premature_action_risk REAL,
    option_value REAL,
    window_stability REAL,
    review_action TEXT,
    FOREIGN KEY (pathway_id) REFERENCES pathways(pathway_id)
);

CREATE TABLE reversibility_lockin (
    lockin_id TEXT PRIMARY KEY,
    pathway_id TEXT NOT NULL,
    technical_lockin REAL,
    institutional_lockin REAL,
    political_lockin REAL,
    metric_lockin REAL,
    resource_lockin REAL,
    narrative_lockin REAL,
    modularity REAL,
    exit_rule_quality REAL,
    review_action TEXT,
    FOREIGN KEY (pathway_id) REFERENCES pathways(pathway_id)
);

CREATE TABLE ethics_power (
    ethics_id TEXT PRIMARY KEY,
    pathway_id TEXT NOT NULL,
    ethical_issue TEXT,
    sponsor_power REAL,
    affected_stakeholder_voice REAL,
    benefit_concentration REAL,
    burden_concentration REAL,
    sequencing_transparency REAL,
    redress_quality REAL,
    pause_authority REAL,
    long_term_responsibility REAL,
    review_action TEXT,
    FOREIGN KEY (pathway_id) REFERENCES pathways(pathway_id)
);

CREATE VIEW pathway_readiness_scores AS
SELECT
    pathway_id,
    pathway_name,
    pathway_type,
    ROUND(
      0.15 * capability_readiness +
      0.14 * evidence_strength +
      0.14 * governance_readiness +
      0.13 * legitimacy -
      0.10 * dependency_load +
      0.09 * reversibility -
      0.09 * capacity_demand +
      0.07 * timing_urgency +
      0.11 * ethical_resilience +
      0.09 * feedback_strength +
      0.10 * strategic_fit,
      4
    ) AS sequencing_readiness_score,
    ROUND(
      0.22 * dependency_load +
      0.20 * capacity_demand +
      0.16 * (1 - evidence_strength) +
      0.14 * (1 - governance_readiness) +
      0.12 * (1 - reversibility) +
      0.10 * (1 - ethical_resilience) +
      0.06 * (1 - feedback_strength),
      4
    ) AS premature_commitment_risk
FROM pathways;

CREATE VIEW dependency_risk_scores AS
SELECT
    dependency_id,
    pathway_id,
    dependency_type,
    dependency_name,
    ROUND(
      0.38 * dependency_strength +
      0.30 * bottleneck_risk +
      0.20 * (1 - readiness_level) +
      0.12 * (1 - owner_clarity),
      4
    ) AS dependency_risk_score
FROM dependencies;

CREATE VIEW capacity_load_scores AS
SELECT
    capacity_id,
    pathway_id,
    ROUND(
      0.12 * budget_load +
      0.14 * staff_load +
      0.14 * technical_load +
      0.13 * governance_load +
      0.12 * leadership_attention_load +
      0.12 * stakeholder_participation_load +
      0.11 * operational_disruption +
      0.12 * (1 - absorptive_capacity),
      4
    ) AS capacity_load_score
FROM capacity_load;

CREATE VIEW timing_window_scores AS
SELECT
    timing_id,
    pathway_id,
    ROUND(
      0.20 * external_window_strength +
      0.18 * internal_readiness +
      0.16 * urgency_quality +
      0.14 * delay_cost -
      0.16 * premature_action_risk +
      0.10 * option_value +
      0.06 * window_stability,
      4
    ) AS timing_window_score
FROM timing_windows;

CREATE VIEW reversibility_lockin_scores AS
SELECT
    lockin_id,
    pathway_id,
    ROUND(
      0.16 * technical_lockin +
      0.15 * institutional_lockin +
      0.14 * political_lockin +
      0.12 * metric_lockin +
      0.13 * resource_lockin +
      0.12 * narrative_lockin +
      0.10 * (1 - modularity) +
      0.08 * (1 - exit_rule_quality),
      4
    ) AS lockin_risk_score
FROM reversibility_lockin;

CREATE VIEW ethics_power_scores AS
SELECT
    ethics_id,
    pathway_id,
    ethical_issue,
    ROUND(
      0.13 * sponsor_power +
      0.15 * (1 - affected_stakeholder_voice) +
      0.13 * benefit_concentration +
      0.15 * burden_concentration +
      0.11 * (1 - sequencing_transparency) +
      0.10 * (1 - redress_quality) +
      0.11 * (1 - pause_authority) +
      0.12 * (1 - long_term_responsibility),
      4
    ) AS power_risk
FROM ethics_power;
