-- Advanced SQL schema for Content Frameworks in Strategic Ideation.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS framework_scores;
DROP VIEW IF EXISTS component_reuse_scores;
DROP VIEW IF EXISTS framework_component_scores;
DROP VIEW IF EXISTS decision_support_scores;
DROP VIEW IF EXISTS narrative_coherence_scores;
DROP VIEW IF EXISTS governance_ethics_scores;

DROP TABLE IF EXISTS governance_ethics;
DROP TABLE IF EXISTS narrative_coherence;
DROP TABLE IF EXISTS decision_support;
DROP TABLE IF EXISTS framework_component_links;
DROP TABLE IF EXISTS components;
DROP TABLE IF EXISTS frameworks;

CREATE TABLE frameworks (
    framework_id TEXT PRIMARY KEY,
    framework_name TEXT NOT NULL,
    framework_type TEXT NOT NULL,
    structure_quality REAL CHECK (structure_quality BETWEEN 0 AND 1),
    conceptual_clarity REAL CHECK (conceptual_clarity BETWEEN 0 AND 1),
    evidence_discipline REAL CHECK (evidence_discipline BETWEEN 0 AND 1),
    assumption_visibility REAL CHECK (assumption_visibility BETWEEN 0 AND 1),
    narrative_coherence REAL CHECK (narrative_coherence BETWEEN 0 AND 1),
    decision_relevance REAL CHECK (decision_relevance BETWEEN 0 AND 1),
    modularity REAL CHECK (modularity BETWEEN 0 AND 1),
    reuse_readiness REAL CHECK (reuse_readiness BETWEEN 0 AND 1),
    governance_strength REAL CHECK (governance_strength BETWEEN 0 AND 1),
    ethical_visibility REAL CHECK (ethical_visibility BETWEEN 0 AND 1),
    ai_governance REAL CHECK (ai_governance BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE components (
    component_id TEXT PRIMARY KEY,
    component_name TEXT NOT NULL,
    component_type TEXT,
    clarity REAL,
    requiredness REAL,
    reuse_value REAL,
    decision_value REAL,
    evidence_value REAL,
    maintenance_need REAL,
    ethical_importance REAL,
    review_action TEXT
);

CREATE TABLE framework_component_links (
    link_id TEXT PRIMARY KEY,
    framework_id TEXT NOT NULL,
    component_id TEXT NOT NULL,
    relationship_type TEXT,
    importance REAL,
    implementation_quality REAL,
    reuse_frequency REAL,
    review_action TEXT,
    FOREIGN KEY (framework_id) REFERENCES frameworks(framework_id),
    FOREIGN KEY (component_id) REFERENCES components(component_id)
);

CREATE TABLE decision_support (
    decision_id TEXT PRIMARY KEY,
    framework_id TEXT NOT NULL,
    decision_type TEXT,
    criteria_visibility REAL,
    evidence_visibility REAL,
    assumption_visibility REAL,
    tradeoff_visibility REAL,
    reversibility_visibility REAL,
    stakeholder_visibility REAL,
    revision_trigger_quality REAL,
    decision_owner_clarity REAL,
    review_action TEXT,
    FOREIGN KEY (framework_id) REFERENCES frameworks(framework_id)
);

CREATE TABLE narrative_coherence (
    narrative_id TEXT PRIMARY KEY,
    framework_id TEXT NOT NULL,
    problem_clarity REAL,
    stakes_clarity REAL,
    insight_quality REAL,
    direction_clarity REAL,
    mechanism_clarity REAL,
    evidence_integration REAL,
    choice_clarity REAL,
    audience_fit REAL,
    review_action TEXT,
    FOREIGN KEY (framework_id) REFERENCES frameworks(framework_id)
);

CREATE TABLE governance_ethics (
    governance_id TEXT PRIMARY KEY,
    framework_id TEXT NOT NULL,
    ownership_clarity REAL,
    version_control REAL,
    quality_standards REAL,
    user_training REAL,
    review_cadence REAL,
    exception_process REAL,
    stakeholder_voice REAL,
    burden_visibility REAL,
    dissent_preservation REAL,
    ethical_risk REAL,
    review_action TEXT,
    FOREIGN KEY (framework_id) REFERENCES frameworks(framework_id)
);

CREATE VIEW framework_scores AS
SELECT
    framework_id,
    framework_name,
    framework_type,
    ROUND(
      0.10 * structure_quality +
      0.10 * conceptual_clarity +
      0.11 * evidence_discipline +
      0.10 * assumption_visibility +
      0.10 * narrative_coherence +
      0.12 * decision_relevance +
      0.10 * modularity +
      0.10 * reuse_readiness +
      0.08 * governance_strength +
      0.06 * ethical_visibility +
      0.03 * ai_governance,
      4
    ) AS framework_strength,
    ROUND(
      0.10 * (1 - structure_quality) +
      0.11 * (1 - conceptual_clarity) +
      0.12 * (1 - evidence_discipline) +
      0.11 * (1 - assumption_visibility) +
      0.09 * (1 - narrative_coherence) +
      0.12 * (1 - decision_relevance) +
      0.09 * (1 - modularity) +
      0.09 * (1 - reuse_readiness) +
      0.08 * (1 - governance_strength) +
      0.06 * (1 - ethical_visibility) +
      0.03 * (1 - ai_governance),
      4
    ) AS framework_risk
FROM frameworks;

CREATE VIEW component_reuse_scores AS
SELECT
    component_id,
    component_name,
    component_type,
    ROUND(
      0.14 * clarity +
      0.16 * requiredness +
      0.18 * reuse_value +
      0.17 * decision_value +
      0.14 * evidence_value -
      0.08 * maintenance_need +
      0.13 * ethical_importance +
      0.06,
      4
    ) AS component_reuse_score
FROM components;

CREATE VIEW framework_component_scores AS
SELECT
    link_id,
    framework_id,
    component_id,
    relationship_type,
    ROUND(
      0.30 * importance +
      0.28 * implementation_quality +
      0.26 * reuse_frequency +
      0.16,
      4
    ) AS framework_component_score
FROM framework_component_links;

CREATE VIEW decision_support_scores AS
SELECT
    decision_id,
    framework_id,
    decision_type,
    ROUND(
      0.12 * criteria_visibility +
      0.13 * evidence_visibility +
      0.12 * assumption_visibility +
      0.13 * tradeoff_visibility +
      0.11 * reversibility_visibility +
      0.12 * stakeholder_visibility +
      0.14 * revision_trigger_quality +
      0.13 * decision_owner_clarity,
      4
    ) AS decision_support_score
FROM decision_support;

CREATE VIEW narrative_coherence_scores AS
SELECT
    narrative_id,
    framework_id,
    ROUND(
      0.13 * problem_clarity +
      0.12 * stakes_clarity +
      0.13 * insight_quality +
      0.13 * direction_clarity +
      0.13 * mechanism_clarity +
      0.13 * evidence_integration +
      0.12 * choice_clarity +
      0.11 * audience_fit,
      4
    ) AS narrative_coherence_score
FROM narrative_coherence;

CREATE VIEW governance_ethics_scores AS
SELECT
    governance_id,
    framework_id,
    ROUND(
      0.13 * ownership_clarity +
      0.13 * version_control +
      0.14 * quality_standards +
      0.10 * user_training +
      0.11 * review_cadence +
      0.10 * exception_process +
      0.10 * stakeholder_voice +
      0.08 * burden_visibility +
      0.08 * dissent_preservation -
      0.03 * ethical_risk +
      0.06,
      4
    ) AS framework_stewardship_score,
    ROUND(
      0.20 * ethical_risk +
      0.14 * (1 - stakeholder_voice) +
      0.14 * (1 - burden_visibility) +
      0.14 * (1 - dissent_preservation) +
      0.12 * (1 - quality_standards) +
      0.10 * (1 - ownership_clarity) +
      0.08 * (1 - review_cadence) +
      0.08 * (1 - exception_process),
      4
    ) AS ethical_framework_risk
FROM governance_ethics;
