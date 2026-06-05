-- Advanced SQL schema for Strategy Implementation and Alignment.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS implementation_profile_scores;
DROP VIEW IF EXISTS alignment_dimension_scores;
DROP VIEW IF EXISTS ethics_power_scores;

DROP TABLE IF EXISTS ethics_power;
DROP TABLE IF EXISTS alignment_dimensions;
DROP TABLE IF EXISTS implementation_profiles;

CREATE TABLE implementation_profiles (
    organization_id TEXT PRIMARY KEY,
    organization_name TEXT NOT NULL,
    organization_type TEXT NOT NULL,
    goal_clarity REAL CHECK (goal_clarity BETWEEN 0 AND 1),
    coordination_quality REAL CHECK (coordination_quality BETWEEN 0 AND 1),
    structural_support REAL CHECK (structural_support BETWEEN 0 AND 1),
    cultural_support REAL CHECK (cultural_support BETWEEN 0 AND 1),
    incentive_alignment REAL CHECK (incentive_alignment BETWEEN 0 AND 1),
    resource_sufficiency REAL CHECK (resource_sufficiency BETWEEN 0 AND 1),
    communication_quality REAL CHECK (communication_quality BETWEEN 0 AND 1),
    accountability_strength REAL CHECK (accountability_strength BETWEEN 0 AND 1),
    adaptive_execution REAL CHECK (adaptive_execution BETWEEN 0 AND 1),
    external_alignment REAL CHECK (external_alignment BETWEEN 0 AND 1),
    ethical_resilience REAL CHECK (ethical_resilience BETWEEN 0 AND 1)
);

CREATE TABLE alignment_dimensions (
    dimension_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    dimension TEXT,
    translation REAL,
    structure REAL,
    culture REAL,
    incentives REAL,
    resources REAL,
    coordination REAL,
    feedback REAL,
    leadership REAL,
    governance REAL,
    decision_memory REAL,
    ethics REAL,
    review_action TEXT,
    FOREIGN KEY (organization_id) REFERENCES implementation_profiles(organization_id)
);

CREATE TABLE ethics_power (
    ethics_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    ethical_issue TEXT,
    sponsor_power REAL,
    affected_stakeholder_voice REAL,
    benefit_concentration REAL,
    burden_concentration REAL,
    transparency REAL,
    redress_quality REAL,
    long_term_responsibility REAL,
    review_action TEXT,
    FOREIGN KEY (organization_id) REFERENCES implementation_profiles(organization_id)
);

CREATE VIEW implementation_profile_scores AS
SELECT
    organization_id,
    organization_name,
    organization_type,
    ROUND(
      0.12 * goal_clarity +
      0.15 * coordination_quality +
      0.12 * structural_support +
      0.12 * cultural_support +
      0.13 * incentive_alignment +
      0.12 * resource_sufficiency +
      0.11 * communication_quality +
      0.10 * accountability_strength +
      0.10 * adaptive_execution +
      0.08 * external_alignment +
      0.05 * ethical_resilience,
      4
    ) AS implementation_profile_score,
    ROUND(
      0.16 * (1 - coordination_quality) +
      0.14 * (1 - cultural_support) +
      0.14 * (1 - incentive_alignment) +
      0.12 * (1 - communication_quality) +
      0.12 * (1 - adaptive_execution) +
      0.10 * (1 - external_alignment) +
      0.10 * (1 - accountability_strength) +
      0.06 * (1 - ethical_resilience) +
      0.06 * (1 - structural_support),
      4
    ) AS alignment_drift_risk
FROM implementation_profiles;

CREATE VIEW alignment_dimension_scores AS
SELECT
    dimension_id,
    organization_id,
    dimension,
    ROUND((translation + structure + culture + incentives + resources + coordination + feedback + leadership + governance + decision_memory + ethics) / 11.0, 4) AS alignment_system_score
FROM alignment_dimensions;

CREATE VIEW ethics_power_scores AS
SELECT
    ethics_id,
    organization_id,
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
