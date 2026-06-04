-- Advanced SQL schema for strategic narratives and the logic of direction.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS narrative_coherence_scores;
DROP VIEW IF EXISTS direction_logic_scores;
DROP VIEW IF EXISTS narrative_performance_gap_scores;
DROP VIEW IF EXISTS role_alignment_scores;
DROP VIEW IF EXISTS narrative_drift_priorities;
DROP VIEW IF EXISTS narrative_governance_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS narrative_governance;
DROP TABLE IF EXISTS narrative_drift_events;
DROP TABLE IF EXISTS stakeholder_interpretations;
DROP TABLE IF EXISTS role_alignment;
DROP TABLE IF EXISTS performance_evidence;
DROP TABLE IF EXISTS direction_logic;
DROP TABLE IF EXISTS narrative_elements;
DROP TABLE IF EXISTS narrative_profiles;

CREATE TABLE narrative_profiles (
    narrative_id TEXT PRIMARY KEY,
    narrative_name TEXT NOT NULL,
    narrative_type TEXT NOT NULL,
    diagnosis_clarity REAL CHECK (diagnosis_clarity BETWEEN 0 AND 1),
    purpose_clarity REAL CHECK (purpose_clarity BETWEEN 0 AND 1),
    choice_clarity REAL CHECK (choice_clarity BETWEEN 0 AND 1),
    sequencing_logic REAL CHECK (sequencing_logic BETWEEN 0 AND 1),
    role_clarity REAL CHECK (role_clarity BETWEEN 0 AND 1),
    future_credibility REAL CHECK (future_credibility BETWEEN 0 AND 1),
    accountability_strength REAL CHECK (accountability_strength BETWEEN 0 AND 1),
    evidence_grounding REAL CHECK (evidence_grounding BETWEEN 0 AND 1),
    stakeholder_visibility REAL CHECK (stakeholder_visibility BETWEEN 0 AND 1),
    ethical_visibility REAL CHECK (ethical_visibility BETWEEN 0 AND 1)
);

CREATE TABLE narrative_elements (
    element_id TEXT PRIMARY KEY,
    narrative_id TEXT NOT NULL,
    element_type TEXT NOT NULL,
    element_statement TEXT NOT NULL,
    element_quality REAL CHECK (element_quality BETWEEN 0 AND 1),
    internal_alignment REAL CHECK (internal_alignment BETWEEN 0 AND 1),
    evidence_support REAL CHECK (evidence_support BETWEEN 0 AND 1),
    contestation_level REAL CHECK (contestation_level BETWEEN 0 AND 1),
    revision_need REAL CHECK (revision_need BETWEEN 0 AND 1),
    FOREIGN KEY (narrative_id) REFERENCES narrative_profiles(narrative_id)
);

CREATE TABLE direction_logic (
    logic_id TEXT PRIMARY KEY,
    narrative_id TEXT NOT NULL,
    alignment_pair TEXT NOT NULL,
    alignment_score REAL CHECK (alignment_score BETWEEN 0 AND 1),
    dependency_clarity REAL CHECK (dependency_clarity BETWEEN 0 AND 1),
    tradeoff_visibility REAL CHECK (tradeoff_visibility BETWEEN 0 AND 1),
    strategic_importance REAL CHECK (strategic_importance BETWEEN 0 AND 1),
    logic_gap REAL CHECK (logic_gap BETWEEN 0 AND 1),
    FOREIGN KEY (narrative_id) REFERENCES narrative_profiles(narrative_id)
);

CREATE TABLE performance_evidence (
    evidence_id TEXT PRIMARY KEY,
    narrative_id TEXT NOT NULL,
    evidence_type TEXT NOT NULL,
    claim_tested TEXT NOT NULL,
    evidence_strength REAL CHECK (evidence_strength BETWEEN 0 AND 1),
    action_alignment REAL CHECK (action_alignment BETWEEN 0 AND 1),
    contradiction_risk REAL CHECK (contradiction_risk BETWEEN 0 AND 1),
    stakeholder_signal REAL CHECK (stakeholder_signal BETWEEN 0 AND 1),
    revision_required INTEGER CHECK (revision_required IN (0, 1)),
    FOREIGN KEY (narrative_id) REFERENCES narrative_profiles(narrative_id)
);

CREATE TABLE role_alignment (
    role_id TEXT PRIMARY KEY,
    narrative_id TEXT NOT NULL,
    actor_group TEXT NOT NULL,
    role_clarity REAL CHECK (role_clarity BETWEEN 0 AND 1),
    contribution_clarity REAL CHECK (contribution_clarity BETWEEN 0 AND 1),
    decision_authority_clarity REAL CHECK (decision_authority_clarity BETWEEN 0 AND 1),
    feedback_channel_quality REAL CHECK (feedback_channel_quality BETWEEN 0 AND 1),
    commitment_level REAL CHECK (commitment_level BETWEEN 0 AND 1),
    misalignment_risk REAL CHECK (misalignment_risk BETWEEN 0 AND 1),
    FOREIGN KEY (narrative_id) REFERENCES narrative_profiles(narrative_id)
);

CREATE TABLE stakeholder_interpretations (
    interpretation_id TEXT PRIMARY KEY,
    narrative_id TEXT NOT NULL,
    stakeholder_group TEXT NOT NULL,
    understanding_quality REAL CHECK (understanding_quality BETWEEN 0 AND 1),
    trust_in_narrative REAL CHECK (trust_in_narrative BETWEEN 0 AND 1),
    perceived_truthfulness REAL CHECK (perceived_truthfulness BETWEEN 0 AND 1),
    perceived_inclusion REAL CHECK (perceived_inclusion BETWEEN 0 AND 1),
    perceived_burden_visibility REAL CHECK (perceived_burden_visibility BETWEEN 0 AND 1),
    contestation_level REAL CHECK (contestation_level BETWEEN 0 AND 1),
    FOREIGN KEY (narrative_id) REFERENCES narrative_profiles(narrative_id)
);

CREATE TABLE narrative_drift_events (
    drift_id TEXT PRIMARY KEY,
    narrative_id TEXT NOT NULL,
    drift_type TEXT NOT NULL,
    drift_description TEXT NOT NULL,
    drift_severity REAL CHECK (drift_severity BETWEEN 0 AND 1),
    strategic_exposure REAL CHECK (strategic_exposure BETWEEN 0 AND 1),
    detection_confidence REAL CHECK (detection_confidence BETWEEN 0 AND 1),
    recommended_response TEXT,
    FOREIGN KEY (narrative_id) REFERENCES narrative_profiles(narrative_id)
);

CREATE TABLE narrative_governance (
    governance_id TEXT PRIMARY KEY,
    narrative_id TEXT NOT NULL,
    owner_group TEXT NOT NULL,
    review_cadence TEXT NOT NULL,
    diagnosis_owner REAL CHECK (diagnosis_owner BETWEEN 0 AND 1),
    choice_owner REAL CHECK (choice_owner BETWEEN 0 AND 1),
    evidence_review_quality REAL CHECK (evidence_review_quality BETWEEN 0 AND 1),
    stakeholder_review_quality REAL CHECK (stakeholder_review_quality BETWEEN 0 AND 1),
    performance_gap_review REAL CHECK (performance_gap_review BETWEEN 0 AND 1),
    revision_trigger_quality REAL CHECK (revision_trigger_quality BETWEEN 0 AND 1),
    governance_risk REAL CHECK (governance_risk BETWEEN 0 AND 1),
    FOREIGN KEY (narrative_id) REFERENCES narrative_profiles(narrative_id)
);

CREATE TABLE decision_memory (
    decision_id TEXT PRIMARY KEY,
    narrative_id TEXT NOT NULL,
    decision_date TEXT,
    decision_context TEXT NOT NULL,
    narrative_element_used TEXT,
    choice_made TEXT,
    sacrifice_accepted TEXT,
    evidence_considered TEXT,
    stakeholder_interpretation TEXT,
    performance_gap_risk TEXT,
    revision_trigger TEXT,
    FOREIGN KEY (narrative_id) REFERENCES narrative_profiles(narrative_id)
);

CREATE VIEW narrative_coherence_scores AS
SELECT
    narrative_id,
    narrative_name,
    narrative_type,
    ROUND(
      0.14 * diagnosis_clarity +
      0.12 * purpose_clarity +
      0.14 * choice_clarity +
      0.12 * sequencing_logic +
      0.11 * role_clarity +
      0.10 * future_credibility +
      0.11 * accountability_strength +
      0.08 * evidence_grounding +
      0.05 * stakeholder_visibility +
      0.03 * ethical_visibility,
      4
    ) AS coherence_score
FROM narrative_profiles;

CREATE VIEW direction_logic_scores AS
SELECT
    logic_id,
    narrative_id,
    alignment_pair,
    ROUND(
      0.30 * alignment_score +
      0.22 * dependency_clarity +
      0.20 * tradeoff_visibility +
      0.16 * strategic_importance -
      0.18 * logic_gap,
      4
    ) AS direction_logic_score
FROM direction_logic;

CREATE VIEW narrative_performance_gap_scores AS
SELECT
    evidence_id,
    narrative_id,
    evidence_type,
    claim_tested,
    ROUND(
      0.26 * (1.0 - evidence_strength) +
      0.28 * (1.0 - action_alignment) +
      0.26 * contradiction_risk +
      0.12 * stakeholder_signal +
      0.08 * revision_required,
      4
    ) AS narrative_performance_gap
FROM performance_evidence;

CREATE VIEW role_alignment_scores AS
SELECT
    role_id,
    narrative_id,
    actor_group,
    ROUND(
      0.22 * role_clarity +
      0.20 * contribution_clarity +
      0.18 * decision_authority_clarity +
      0.18 * feedback_channel_quality +
      0.14 * commitment_level -
      0.18 * misalignment_risk,
      4
    ) AS role_alignment_score
FROM role_alignment;

CREATE VIEW narrative_drift_priorities AS
SELECT
    drift_id,
    narrative_id,
    drift_type,
    ROUND(
      0.34 * drift_severity +
      0.34 * strategic_exposure +
      0.18 * detection_confidence,
      4
    ) AS drift_priority,
    recommended_response,
    drift_description
FROM narrative_drift_events;

CREATE VIEW narrative_governance_scores AS
SELECT
    governance_id,
    narrative_id,
    owner_group,
    review_cadence,
    ROUND(
      0.14 * diagnosis_owner +
      0.14 * choice_owner +
      0.18 * evidence_review_quality +
      0.18 * stakeholder_review_quality +
      0.18 * performance_gap_review +
      0.18 * revision_trigger_quality -
      0.16 * governance_risk,
      4
    ) AS governance_strength
FROM narrative_governance;
