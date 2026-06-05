-- Advanced SQL schema for Strategic Ideation and Institutional Power.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS power_idea_scores;
DROP VIEW IF EXISTS agenda_power_scores;
DROP VIEW IF EXISTS evidence_parity_scores;
DROP VIEW IF EXISTS participation_voice_scores;
DROP VIEW IF EXISTS resource_memory_ai_scores;

DROP TABLE IF EXISTS resource_memory_ai;
DROP TABLE IF EXISTS participation_voice;
DROP TABLE IF EXISTS evidence_parity;
DROP TABLE IF EXISTS agenda_power;
DROP TABLE IF EXISTS power_ideas;

CREATE TABLE power_ideas (
    idea_id TEXT PRIMARY KEY,
    idea TEXT NOT NULL,
    idea_type TEXT,
    strategic_merit REAL,
    evidence_strength REAL,
    executive_sponsorship REAL,
    resource_fit REAL,
    stakeholder_influence REAL,
    dissent_protection REAL,
    classification_visibility REAL,
    power_alignment REAL,
    advancement_likelihood REAL,
    ethical_visibility REAL,
    description TEXT
);

CREATE TABLE agenda_power (
    agenda_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    agenda_source TEXT,
    leadership_priority REAL,
    stakeholder_priority REAL,
    frontline_priority REAL,
    evidence_signal_strength REAL,
    long_term_relevance REAL,
    political_safety REAL,
    agenda_exclusion_risk REAL,
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES power_ideas(idea_id)
);

CREATE TABLE evidence_parity (
    evidence_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    evidence_type TEXT,
    evidence_strength REAL,
    evidence_threshold_applied REAL,
    counterevidence_visibility REAL,
    source_diversity REAL,
    stakeholder_evidence_quality REAL,
    expertise_balance REAL,
    overclaim_risk REAL,
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES power_ideas(idea_id)
);

CREATE TABLE participation_voice (
    voice_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    participation_mode TEXT,
    invited_voice REAL,
    actual_influence REAL,
    agenda_influence REAL,
    criteria_influence REAL,
    decision_influence REAL,
    dissent_safety REAL,
    redress_access REAL,
    tokenism_risk REAL,
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES power_ideas(idea_id)
);

CREATE TABLE resource_memory_ai (
    record_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    resource_support REAL,
    incentive_fit REAL,
    memory_traceability REAL,
    prior_failure_visibility REAL,
    dissent_memory REAL,
    ai_disclosure REAL,
    ai_source_traceability REAL,
    ai_bias_review REAL,
    ai_power_amplification_risk REAL,
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES power_ideas(idea_id)
);

CREATE VIEW power_idea_scores AS
SELECT
    idea_id,
    idea,
    idea_type,
    ROUND(
      0.28 * strategic_merit +
      0.21 * evidence_strength +
      0.16 * stakeholder_influence +
      0.13 * dissent_protection +
      0.12 * classification_visibility +
      0.10 * ethical_visibility,
      4
    ) AS merit_score,
    ROUND(
      0.28 * executive_sponsorship +
      0.24 * resource_fit +
      0.24 * power_alignment +
      0.24 * advancement_likelihood,
      4
    ) AS institutional_support,
    ROUND(
      (0.28 * executive_sponsorship +
       0.24 * resource_fit +
       0.24 * power_alignment +
       0.24 * advancement_likelihood)
      -
      (0.28 * strategic_merit +
       0.21 * evidence_strength +
       0.16 * stakeholder_influence +
       0.13 * dissent_protection +
       0.12 * classification_visibility +
       0.10 * ethical_visibility),
      4
    ) AS power_distortion,
    ROUND(advancement_likelihood - stakeholder_influence, 4) AS voice_gap
FROM power_ideas;

CREATE VIEW agenda_power_scores AS
SELECT
    agenda_id,
    idea_id,
    agenda_source,
    ROUND(
      0.18 * stakeholder_priority +
      0.16 * frontline_priority +
      0.18 * evidence_signal_strength +
      0.18 * long_term_relevance +
      0.10 * leadership_priority +
      0.10 * (1 - political_safety) +
      0.10 * (1 - agenda_exclusion_risk),
      4
    ) AS agenda_legitimacy,
    ROUND(
      0.30 * leadership_priority +
      0.25 * political_safety +
      0.20 * agenda_exclusion_risk +
      0.15 * (1 - stakeholder_priority) +
      0.10 * (1 - long_term_relevance),
      4
    ) AS power_filtered_attention
FROM agenda_power;

CREATE VIEW evidence_parity_scores AS
SELECT
    evidence_id,
    idea_id,
    evidence_type,
    ROUND(
      0.16 * evidence_strength +
      0.14 * evidence_threshold_applied +
      0.15 * counterevidence_visibility +
      0.14 * source_diversity +
      0.15 * stakeholder_evidence_quality +
      0.12 * expertise_balance +
      0.14 * (1 - overclaim_risk),
      4
    ) AS evidence_parity_score,
    ROUND(evidence_threshold_applied - evidence_strength, 4) AS threshold_gap,
    overclaim_risk
FROM evidence_parity;

CREATE VIEW participation_voice_scores AS
SELECT
    voice_id,
    idea_id,
    participation_mode,
    ROUND(
      0.12 * invited_voice +
      0.18 * actual_influence +
      0.14 * agenda_influence +
      0.14 * criteria_influence +
      0.16 * decision_influence +
      0.14 * dissent_safety +
      0.12 * redress_access,
      4
    ) AS participation_influence_score,
    ROUND(
      0.24 * tokenism_risk +
      0.16 * (1 - actual_influence) +
      0.14 * (1 - agenda_influence) +
      0.14 * (1 - criteria_influence) +
      0.14 * (1 - decision_influence) +
      0.10 * (1 - dissent_safety) +
      0.08 * (1 - redress_access),
      4
    ) AS tokenism_risk_score,
    ROUND(invited_voice - actual_influence, 4) AS influence_gap
FROM participation_voice;

CREATE VIEW resource_memory_ai_scores AS
SELECT
    record_id,
    idea_id,
    ROUND(
      0.14 * resource_support +
      0.10 * incentive_fit +
      0.16 * memory_traceability +
      0.14 * prior_failure_visibility +
      0.16 * dissent_memory +
      0.10 * ai_disclosure +
      0.10 * ai_source_traceability +
      0.10 * ai_bias_review,
      4
    ) AS resource_memory_integrity,
    ROUND(
      0.30 * ai_power_amplification_risk +
      0.16 * (1 - ai_disclosure) +
      0.16 * (1 - ai_source_traceability) +
      0.16 * (1 - ai_bias_review) +
      0.12 * (1 - dissent_memory) +
      0.10 * (1 - prior_failure_visibility),
      4
    ) AS ai_power_risk
FROM resource_memory_ai;
