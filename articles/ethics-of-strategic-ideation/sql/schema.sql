-- Advanced SQL schema for Ethics of Strategic Ideation.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS ethical_idea_scores;
DROP VIEW IF EXISTS stakeholder_impact_scores;
DROP VIEW IF EXISTS claim_evidence_ethics_scores;
DROP VIEW IF EXISTS ai_ethics_scores;
DROP VIEW IF EXISTS accountability_redress_scores;

DROP TABLE IF EXISTS accountability_redress;
DROP TABLE IF EXISTS ai_use_ethics;
DROP TABLE IF EXISTS claim_evidence_ethics;
DROP TABLE IF EXISTS stakeholder_impacts;
DROP TABLE IF EXISTS ethical_ideas;

CREATE TABLE ethical_ideas (
    idea_id TEXT PRIMARY KEY,
    idea TEXT NOT NULL,
    idea_type TEXT,
    stakeholder_voice REAL,
    evidence_integrity REAL,
    burden_visibility REAL,
    uncertainty_visibility REAL,
    reversibility REAL,
    long_term_responsibility REAL,
    ai_governance REAL,
    accountability REAL,
    redress_quality REAL,
    problem_frame_integrity REAL,
    power_review REAL,
    description TEXT
);

CREATE TABLE stakeholder_impacts (
    impact_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    stakeholder_group TEXT,
    benefit_score REAL,
    burden_score REAL,
    risk_exposure REAL,
    voice_quality REAL,
    consent_quality REAL,
    redress_access REAL,
    trust_sensitivity REAL,
    long_term_exposure REAL,
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES ethical_ideas(idea_id)
);

CREATE TABLE claim_evidence_ethics (
    claim_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    claim_type TEXT,
    claim_text TEXT,
    source_quality REAL,
    confidence_level REAL,
    uncertainty_visibility REAL,
    counterevidence_visibility REAL,
    transfer_limits REAL,
    overclaim_risk REAL,
    ethical_salience REAL,
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES ethical_ideas(idea_id)
);

CREATE TABLE ai_use_ethics (
    ai_use_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    ai_use_case TEXT,
    disclosure_quality REAL,
    source_traceability REAL,
    human_review REAL,
    bias_review REAL,
    stakeholder_review REAL,
    uncertainty_preservation REAL,
    accountability_clarity REAL,
    automation_risk REAL,
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES ethical_ideas(idea_id)
);

CREATE TABLE accountability_redress (
    accountability_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    owner_clarity REAL,
    monitoring_quality REAL,
    escalation_path REAL,
    appeal_process REAL,
    correction_capacity REAL,
    redress_access REAL,
    revision_trigger_quality REAL,
    public_accountability REAL,
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES ethical_ideas(idea_id)
);

CREATE VIEW ethical_idea_scores AS
SELECT
    idea_id,
    idea,
    idea_type,
    ROUND(
      0.12 * stakeholder_voice +
      0.12 * evidence_integrity +
      0.10 * burden_visibility +
      0.09 * uncertainty_visibility +
      0.08 * reversibility +
      0.11 * long_term_responsibility +
      0.07 * ai_governance +
      0.09 * accountability +
      0.07 * redress_quality +
      0.08 * problem_frame_integrity +
      0.07 * power_review,
      4
    ) AS ethical_legitimacy,
    ROUND(
      0.13 * (1 - stakeholder_voice) +
      0.12 * (1 - evidence_integrity) +
      0.12 * (1 - burden_visibility) +
      0.10 * (1 - uncertainty_visibility) +
      0.09 * (1 - reversibility) +
      0.10 * (1 - long_term_responsibility) +
      0.10 * (1 - ai_governance) +
      0.08 * (1 - accountability) +
      0.07 * (1 - redress_quality) +
      0.05 * (1 - problem_frame_integrity) +
      0.04 * (1 - power_review),
      4
    ) AS ethical_risk
FROM ethical_ideas;

CREATE VIEW stakeholder_impact_scores AS
SELECT
    impact_id,
    idea_id,
    stakeholder_group,
    ROUND(
      0.12 * benefit_score +
      0.16 * (1 - burden_score) +
      0.14 * (1 - risk_exposure) +
      0.14 * voice_quality +
      0.12 * consent_quality +
      0.12 * redress_access +
      0.10 * (1 - trust_sensitivity) +
      0.10 * (1 - long_term_exposure),
      4
    ) AS stakeholder_impact_legitimacy,
    ROUND(
      0.20 * burden_score +
      0.20 * risk_exposure +
      0.14 * (1 - voice_quality) +
      0.12 * (1 - consent_quality) +
      0.12 * (1 - redress_access) +
      0.12 * trust_sensitivity +
      0.10 * long_term_exposure,
      4
    ) AS burden_risk
FROM stakeholder_impacts;

CREATE VIEW claim_evidence_ethics_scores AS
SELECT
    claim_id,
    idea_id,
    claim_type,
    ROUND(
      0.14 * source_quality +
      0.14 * confidence_level +
      0.13 * uncertainty_visibility +
      0.13 * counterevidence_visibility +
      0.12 * transfer_limits +
      0.14 * (1 - overclaim_risk) +
      0.20 * ethical_salience,
      4
    ) AS claim_evidence_ethics_score,
    overclaim_risk
FROM claim_evidence_ethics;

CREATE VIEW ai_ethics_scores AS
SELECT
    ai_use_id,
    idea_id,
    ai_use_case,
    ROUND(
      0.12 * disclosure_quality +
      0.13 * source_traceability +
      0.13 * human_review +
      0.13 * bias_review +
      0.12 * stakeholder_review +
      0.12 * uncertainty_preservation +
      0.12 * accountability_clarity +
      0.13 * (1 - automation_risk),
      4
    ) AS ai_ethics_governance_score,
    automation_risk
FROM ai_use_ethics;

CREATE VIEW accountability_redress_scores AS
SELECT
    accountability_id,
    idea_id,
    ROUND(
      0.13 * owner_clarity +
      0.13 * monitoring_quality +
      0.12 * escalation_path +
      0.13 * appeal_process +
      0.13 * correction_capacity +
      0.13 * redress_access +
      0.14 * revision_trigger_quality +
      0.12 * public_accountability,
      4
    ) AS accountability_redress_score
FROM accountability_redress;
