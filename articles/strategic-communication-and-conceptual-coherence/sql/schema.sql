-- Advanced SQL schema for Strategic Communication and Conceptual Coherence.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS communication_profile_scores;
DROP VIEW IF EXISTS concept_definition_scores;
DROP VIEW IF EXISTS claim_evidence_scores;
DROP VIEW IF EXISTS audience_adaptation_scores;
DROP VIEW IF EXISTS decision_alignment_scores;
DROP VIEW IF EXISTS governance_ethics_scores;

DROP TABLE IF EXISTS governance_ethics;
DROP TABLE IF EXISTS decision_alignment;
DROP TABLE IF EXISTS audience_adaptation;
DROP TABLE IF EXISTS claim_evidence;
DROP TABLE IF EXISTS concepts;
DROP TABLE IF EXISTS communication_profiles;

CREATE TABLE communication_profiles (
    profile_id TEXT PRIMARY KEY,
    communication_profile TEXT NOT NULL,
    profile_type TEXT NOT NULL,
    concept_definition REAL CHECK (concept_definition BETWEEN 0 AND 1),
    narrative_coherence REAL CHECK (narrative_coherence BETWEEN 0 AND 1),
    evidence_integrity REAL CHECK (evidence_integrity BETWEEN 0 AND 1),
    audience_adaptation REAL CHECK (audience_adaptation BETWEEN 0 AND 1),
    decision_alignment REAL CHECK (decision_alignment BETWEEN 0 AND 1),
    implementation_translatability REAL CHECK (implementation_translatability BETWEEN 0 AND 1),
    feedback_quality REAL CHECK (feedback_quality BETWEEN 0 AND 1),
    governance_strength REAL CHECK (governance_strength BETWEEN 0 AND 1),
    ethical_visibility REAL CHECK (ethical_visibility BETWEEN 0 AND 1),
    ai_governance REAL CHECK (ai_governance BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE concepts (
    concept_id TEXT PRIMARY KEY,
    concept_name TEXT NOT NULL,
    definition_quality REAL,
    boundary_clarity REAL,
    mechanism_clarity REAL,
    evidence_linkage REAL,
    decision_relevance REAL,
    implementation_meaning REAL,
    version_control REAL,
    drift_risk REAL,
    review_action TEXT
);

CREATE TABLE claim_evidence (
    claim_id TEXT PRIMARY KEY,
    profile_id TEXT NOT NULL,
    claim_type TEXT,
    claim_text TEXT,
    evidence_quality REAL,
    confidence_level REAL,
    assumption_visibility REAL,
    uncertainty_visibility REAL,
    counterevidence_visibility REAL,
    source_traceability REAL,
    overclaim_risk REAL,
    review_action TEXT,
    FOREIGN KEY (profile_id) REFERENCES communication_profiles(profile_id)
);

CREATE TABLE audience_adaptation (
    adaptation_id TEXT PRIMARY KEY,
    profile_id TEXT NOT NULL,
    audience TEXT,
    core_meaning_preservation REAL,
    language_fit REAL,
    evidence_fit REAL,
    depth_fit REAL,
    tradeoff_visibility REAL,
    uncertainty_visibility REAL,
    feedback_channel_quality REAL,
    distortion_risk REAL,
    review_action TEXT,
    FOREIGN KEY (profile_id) REFERENCES communication_profiles(profile_id)
);

CREATE TABLE decision_alignment (
    alignment_id TEXT PRIMARY KEY,
    profile_id TEXT NOT NULL,
    decision_accuracy REAL,
    rationale_clarity REAL,
    tradeoff_alignment REAL,
    owner_visibility REAL,
    timeline_visibility REAL,
    revision_trigger_quality REAL,
    implementation_guidance REAL,
    metric_consistency REAL,
    review_action TEXT,
    FOREIGN KEY (profile_id) REFERENCES communication_profiles(profile_id)
);

CREATE TABLE governance_ethics (
    governance_id TEXT PRIMARY KEY,
    profile_id TEXT NOT NULL,
    core_message_ownership REAL,
    definition_standards REAL,
    evidence_review REAL,
    version_control REAL,
    audience_rules REAL,
    feedback_loop_quality REAL,
    stakeholder_voice REAL,
    burden_visibility REAL,
    dissent_preservation REAL,
    ethical_risk REAL,
    review_action TEXT,
    FOREIGN KEY (profile_id) REFERENCES communication_profiles(profile_id)
);

CREATE VIEW communication_profile_scores AS
SELECT
    profile_id,
    communication_profile,
    profile_type,
    ROUND(
      0.11 * concept_definition +
      0.11 * narrative_coherence +
      0.13 * evidence_integrity +
      0.10 * audience_adaptation +
      0.13 * decision_alignment +
      0.11 * implementation_translatability +
      0.08 * feedback_quality +
      0.10 * governance_strength +
      0.09 * ethical_visibility +
      0.04 * ai_governance,
      4
    ) AS coherence_strength,
    ROUND(
      0.12 * (1 - concept_definition) +
      0.10 * (1 - narrative_coherence) +
      0.13 * (1 - evidence_integrity) +
      0.10 * (1 - audience_adaptation) +
      0.13 * (1 - decision_alignment) +
      0.11 * (1 - implementation_translatability) +
      0.08 * (1 - feedback_quality) +
      0.09 * (1 - governance_strength) +
      0.10 * (1 - ethical_visibility) +
      0.04 * (1 - ai_governance),
      4
    ) AS meaning_loss_risk
FROM communication_profiles;

CREATE VIEW concept_definition_scores AS
SELECT
    concept_id,
    concept_name,
    ROUND(
      0.16 * definition_quality +
      0.14 * boundary_clarity +
      0.14 * mechanism_clarity +
      0.14 * evidence_linkage +
      0.15 * decision_relevance +
      0.12 * implementation_meaning +
      0.10 * version_control -
      0.05 * drift_risk,
      4
    ) AS concept_definition_score,
    drift_risk
FROM concepts;

CREATE VIEW claim_evidence_scores AS
SELECT
    claim_id,
    profile_id,
    claim_type,
    ROUND(
      0.15 * evidence_quality +
      0.15 * confidence_level +
      0.13 * assumption_visibility +
      0.13 * uncertainty_visibility +
      0.11 * counterevidence_visibility +
      0.15 * source_traceability -
      0.08 * overclaim_risk +
      0.06,
      4
    ) AS claim_evidence_integrity_score,
    overclaim_risk
FROM claim_evidence;

CREATE VIEW audience_adaptation_scores AS
SELECT
    adaptation_id,
    profile_id,
    audience,
    ROUND(
      0.17 * core_meaning_preservation +
      0.12 * language_fit +
      0.13 * evidence_fit +
      0.11 * depth_fit +
      0.12 * tradeoff_visibility +
      0.12 * uncertainty_visibility +
      0.13 * feedback_channel_quality -
      0.10 * distortion_risk +
      0.10,
      4
    ) AS audience_adaptation_score,
    distortion_risk
FROM audience_adaptation;

CREATE VIEW decision_alignment_scores AS
SELECT
    alignment_id,
    profile_id,
    ROUND(
      0.14 * decision_accuracy +
      0.13 * rationale_clarity +
      0.12 * tradeoff_alignment +
      0.11 * owner_visibility +
      0.10 * timeline_visibility +
      0.14 * revision_trigger_quality +
      0.14 * implementation_guidance +
      0.12 * metric_consistency,
      4
    ) AS decision_alignment_score
FROM decision_alignment;

CREATE VIEW governance_ethics_scores AS
SELECT
    governance_id,
    profile_id,
    ROUND(
      0.13 * core_message_ownership +
      0.13 * definition_standards +
      0.14 * evidence_review +
      0.11 * version_control +
      0.11 * audience_rules +
      0.11 * feedback_loop_quality +
      0.09 * stakeholder_voice +
      0.08 * burden_visibility +
      0.08 * dissent_preservation -
      0.04 * ethical_risk +
      0.06,
      4
    ) AS communication_stewardship_score,
    ROUND(
      0.20 * ethical_risk +
      0.14 * (1 - stakeholder_voice) +
      0.14 * (1 - burden_visibility) +
      0.14 * (1 - dissent_preservation) +
      0.12 * (1 - evidence_review) +
      0.10 * (1 - definition_standards) +
      0.08 * (1 - feedback_loop_quality) +
      0.08 * (1 - audience_rules),
      4
    ) AS ethical_communication_risk
FROM governance_ethics;
