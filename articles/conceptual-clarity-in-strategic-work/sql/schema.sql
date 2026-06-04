-- Advanced SQL schema for conceptual clarity in strategic work.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS conceptual_clarity_scores;
DROP VIEW IF EXISTS metric_proxy_risk_scores;
DROP VIEW IF EXISTS conceptual_drift_priorities;
DROP VIEW IF EXISTS concept_governance_scores;
DROP VIEW IF EXISTS distinction_risk_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS governance_reviews;
DROP TABLE IF EXISTS drift_events;
DROP TABLE IF EXISTS decision_implications;
DROP TABLE IF EXISTS metric_register;
DROP TABLE IF EXISTS distinction_map;
DROP TABLE IF EXISTS concept_boundaries;
DROP TABLE IF EXISTS interpretation_survey;
DROP TABLE IF EXISTS concept_inventory;

CREATE TABLE concept_inventory (
    concept_id TEXT PRIMARY KEY,
    concept_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    definition_clarity REAL CHECK (definition_clarity BETWEEN 0 AND 1),
    boundary_clarity REAL CHECK (boundary_clarity BETWEEN 0 AND 1),
    distinction_quality REAL CHECK (distinction_quality BETWEEN 0 AND 1),
    operational_implication REAL CHECK (operational_implication BETWEEN 0 AND 1),
    measurement_validity REAL CHECK (measurement_validity BETWEEN 0 AND 1),
    revision_capacity REAL CHECK (revision_capacity BETWEEN 0 AND 1),
    stakeholder_visibility REAL CHECK (stakeholder_visibility BETWEEN 0 AND 1),
    ethical_visibility REAL CHECK (ethical_visibility BETWEEN 0 AND 1),
    governance_maturity REAL CHECK (governance_maturity BETWEEN 0 AND 1)
);

CREATE TABLE interpretation_survey (
    interpretation_id TEXT PRIMARY KEY,
    concept_id TEXT NOT NULL,
    actor_group TEXT NOT NULL,
    interpretation_summary TEXT NOT NULL,
    interpretation_alignment REAL CHECK (interpretation_alignment BETWEEN 0 AND 1),
    decision_implication_alignment REAL CHECK (decision_implication_alignment BETWEEN 0 AND 1),
    confidence REAL CHECK (confidence BETWEEN 0 AND 1),
    contestation_level REAL CHECK (contestation_level BETWEEN 0 AND 1),
    FOREIGN KEY (concept_id) REFERENCES concept_inventory(concept_id)
);

CREATE TABLE concept_boundaries (
    boundary_id TEXT PRIMARY KEY,
    concept_id TEXT NOT NULL,
    boundary_rule TEXT NOT NULL,
    inclusion_clarity REAL CHECK (inclusion_clarity BETWEEN 0 AND 1),
    exclusion_clarity REAL CHECK (exclusion_clarity BETWEEN 0 AND 1),
    strategic_importance REAL CHECK (strategic_importance BETWEEN 0 AND 1),
    boundary_contestation REAL CHECK (boundary_contestation BETWEEN 0 AND 1),
    review_priority TEXT CHECK (review_priority IN ('low', 'moderate', 'high')),
    FOREIGN KEY (concept_id) REFERENCES concept_inventory(concept_id)
);

CREATE TABLE distinction_map (
    distinction_id TEXT PRIMARY KEY,
    concept_id TEXT NOT NULL,
    confused_with TEXT NOT NULL,
    distinction_statement TEXT NOT NULL,
    distinction_clarity REAL CHECK (distinction_clarity BETWEEN 0 AND 1),
    confusion_risk REAL CHECK (confusion_risk BETWEEN 0 AND 1),
    decision_consequence TEXT,
    FOREIGN KEY (concept_id) REFERENCES concept_inventory(concept_id)
);

CREATE TABLE metric_register (
    metric_id TEXT PRIMARY KEY,
    concept_id TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_type TEXT NOT NULL,
    proxy_strength REAL CHECK (proxy_strength BETWEEN 0 AND 1),
    proxy_risk REAL CHECK (proxy_risk BETWEEN 0 AND 1),
    incentive_distortion_risk REAL CHECK (incentive_distortion_risk BETWEEN 0 AND 1),
    qualitative_gap REAL CHECK (qualitative_gap BETWEEN 0 AND 1),
    validity_confidence REAL CHECK (validity_confidence BETWEEN 0 AND 1),
    FOREIGN KEY (concept_id) REFERENCES concept_inventory(concept_id)
);

CREATE TABLE decision_implications (
    implication_id TEXT PRIMARY KEY,
    concept_id TEXT NOT NULL,
    decision_context TEXT NOT NULL,
    decision_relevance REAL CHECK (decision_relevance BETWEEN 0 AND 1),
    resource_allocation_effect REAL CHECK (resource_allocation_effect BETWEEN 0 AND 1),
    role_clarity_effect REAL CHECK (role_clarity_effect BETWEEN 0 AND 1),
    tradeoff_visibility REAL CHECK (tradeoff_visibility BETWEEN 0 AND 1),
    escalation_need REAL CHECK (escalation_need BETWEEN 0 AND 1),
    FOREIGN KEY (concept_id) REFERENCES concept_inventory(concept_id)
);

CREATE TABLE drift_events (
    drift_id TEXT PRIMARY KEY,
    concept_id TEXT NOT NULL,
    drift_type TEXT NOT NULL,
    drift_description TEXT NOT NULL,
    drift_severity REAL CHECK (drift_severity BETWEEN 0 AND 1),
    strategic_exposure REAL CHECK (strategic_exposure BETWEEN 0 AND 1),
    detection_confidence REAL CHECK (detection_confidence BETWEEN 0 AND 1),
    recommended_response TEXT,
    FOREIGN KEY (concept_id) REFERENCES concept_inventory(concept_id)
);

CREATE TABLE governance_reviews (
    review_id TEXT PRIMARY KEY,
    concept_id TEXT NOT NULL,
    owner_group TEXT NOT NULL,
    review_cadence TEXT NOT NULL,
    definition_owner REAL CHECK (definition_owner BETWEEN 0 AND 1),
    metric_owner REAL CHECK (metric_owner BETWEEN 0 AND 1),
    revision_trigger_quality REAL CHECK (revision_trigger_quality BETWEEN 0 AND 1),
    documentation_quality REAL CHECK (documentation_quality BETWEEN 0 AND 1),
    stakeholder_review_quality REAL CHECK (stakeholder_review_quality BETWEEN 0 AND 1),
    governance_risk REAL CHECK (governance_risk BETWEEN 0 AND 1),
    FOREIGN KEY (concept_id) REFERENCES concept_inventory(concept_id)
);

CREATE TABLE decision_memory (
    decision_id TEXT PRIMARY KEY,
    concept_id TEXT NOT NULL,
    decision_date TEXT,
    decision_context TEXT NOT NULL,
    concept_definition_used TEXT,
    boundary_rules_used TEXT,
    metrics_used TEXT,
    interpretation_risks TEXT,
    tradeoffs_revealed TEXT,
    revision_trigger TEXT,
    FOREIGN KEY (concept_id) REFERENCES concept_inventory(concept_id)
);

CREATE VIEW conceptual_clarity_scores AS
SELECT
    concept_id,
    concept_name,
    domain,
    ROUND(
      0.17 * definition_clarity +
      0.14 * boundary_clarity +
      0.14 * distinction_quality +
      0.13 * operational_implication +
      0.15 * measurement_validity +
      0.10 * revision_capacity +
      0.07 * stakeholder_visibility +
      0.06 * ethical_visibility +
      0.04 * governance_maturity,
      4
    ) AS clarity_score
FROM concept_inventory;

CREATE VIEW metric_proxy_risk_scores AS
SELECT
    metric_id,
    concept_id,
    metric_name,
    metric_type,
    ROUND(
      0.28 * proxy_risk +
      0.26 * incentive_distortion_risk +
      0.22 * qualitative_gap +
      0.24 * (1.0 - validity_confidence),
      4
    ) AS proxy_failure_risk
FROM metric_register;

CREATE VIEW conceptual_drift_priorities AS
SELECT
    drift_id,
    concept_id,
    drift_type,
    ROUND(
      0.34 * drift_severity +
      0.34 * strategic_exposure +
      0.18 * detection_confidence,
      4
    ) AS drift_priority,
    recommended_response,
    drift_description
FROM drift_events;

CREATE VIEW concept_governance_scores AS
SELECT
    review_id,
    concept_id,
    owner_group,
    review_cadence,
    ROUND(
      0.18 * definition_owner +
      0.16 * metric_owner +
      0.20 * revision_trigger_quality +
      0.18 * documentation_quality +
      0.20 * stakeholder_review_quality -
      0.14 * governance_risk,
      4
    ) AS governance_strength
FROM governance_reviews;

CREATE VIEW distinction_risk_scores AS
SELECT
    distinction_id,
    concept_id,
    confused_with,
    ROUND(
      0.52 * confusion_risk +
      0.48 * (1.0 - distinction_clarity),
      4
    ) AS distinction_risk,
    distinction_statement,
    decision_consequence
FROM distinction_map;
