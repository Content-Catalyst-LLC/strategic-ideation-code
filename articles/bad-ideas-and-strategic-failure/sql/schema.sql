-- Advanced SQL schema for Bad Ideas and Strategic Failure.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS bad_idea_risk_scores;
DROP VIEW IF EXISTS failure_pathway_scores;
DROP VIEW IF EXISTS evidence_overclaim_scores;
DROP VIEW IF EXISTS implementation_incentive_scores;
DROP VIEW IF EXISTS power_narrative_learning_scores;

DROP TABLE IF EXISTS power_narrative_learning;
DROP TABLE IF EXISTS implementation_incentives;
DROP TABLE IF EXISTS evidence_overclaim;
DROP TABLE IF EXISTS failure_pathways;
DROP TABLE IF EXISTS bad_ideas;

CREATE TABLE bad_ideas (
    idea_id TEXT PRIMARY KEY,
    idea TEXT NOT NULL,
    idea_type TEXT,
    problem_frame_integrity REAL,
    mechanism_clarity REAL,
    evidence_quality REAL,
    context_fit REAL,
    implementation_readiness REAL,
    incentive_alignment REAL,
    ethical_visibility REAL,
    institutional_support REAL,
    strategic_merit REAL,
    learning_design REAL,
    narrative_honesty REAL,
    ai_fluency_risk REAL,
    description TEXT
);

CREATE TABLE failure_pathways (
    pathway_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    weakness_type TEXT,
    premature_commitment REAL,
    execution_strain REAL,
    defensive_narrative REAL,
    stakeholder_harm REAL,
    learning_distortion REAL,
    escalation_risk REAL,
    mitigation_quality REAL,
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES bad_ideas(idea_id)
);

CREATE TABLE evidence_overclaim (
    claim_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    claim_type TEXT,
    claim_text TEXT,
    source_quality REAL,
    confidence_level REAL,
    evidence_relevance REAL,
    counterevidence_visibility REAL,
    transfer_fit REAL,
    overclaim_risk REAL,
    narrative_pressure REAL,
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES bad_ideas(idea_id)
);

CREATE TABLE implementation_incentives (
    impl_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    capacity_fit REAL,
    role_clarity REAL,
    dependency_visibility REAL,
    technical_readiness REAL,
    stakeholder_trust REAL,
    incentive_alignment REAL,
    gaming_risk REAL,
    hidden_labor REAL,
    adoption_assumption_risk REAL,
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES bad_ideas(idea_id)
);

CREATE TABLE power_narrative_learning (
    pnl_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    sponsor_power REAL,
    narrative_strength REAL,
    dissent_visibility REAL,
    red_team_quality REAL,
    stop_rule_quality REAL,
    revision_trigger_quality REAL,
    decision_memory_quality REAL,
    ai_review_quality REAL,
    power_protection_risk REAL,
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES bad_ideas(idea_id)
);

CREATE VIEW bad_idea_risk_scores AS
SELECT
    idea_id,
    idea,
    idea_type,
    ROUND(
      0.12 * problem_frame_integrity +
      0.11 * mechanism_clarity +
      0.13 * evidence_quality +
      0.10 * context_fit +
      0.12 * implementation_readiness +
      0.10 * incentive_alignment +
      0.10 * ethical_visibility +
      0.09 * strategic_merit +
      0.08 * learning_design +
      0.05 * narrative_honesty,
      4
    ) AS idea_quality,
    ROUND(institutional_support - strategic_merit, 4) AS power_distortion,
    ROUND(
      0.12 * (1 - problem_frame_integrity) +
      0.11 * (1 - mechanism_clarity) +
      0.13 * (1 - evidence_quality) +
      0.10 * (1 - context_fit) +
      0.12 * (1 - implementation_readiness) +
      0.10 * (1 - incentive_alignment) +
      0.10 * (1 - ethical_visibility) +
      0.08 * (1 - learning_design) +
      0.05 * (1 - narrative_honesty) +
      0.05 * MAX(0, institutional_support - strategic_merit) +
      0.04 * ai_fluency_risk,
      4
    ) AS failure_risk
FROM bad_ideas;

CREATE VIEW failure_pathway_scores AS
SELECT
    pathway_id,
    idea_id,
    weakness_type,
    ROUND(
      0.16 * premature_commitment +
      0.15 * execution_strain +
      0.14 * defensive_narrative +
      0.15 * stakeholder_harm +
      0.14 * learning_distortion +
      0.16 * escalation_risk +
      0.10 * (1 - mitigation_quality),
      4
    ) AS failure_pathway_risk
FROM failure_pathways;

CREATE VIEW evidence_overclaim_scores AS
SELECT
    claim_id,
    idea_id,
    claim_type,
    ROUND(
      0.15 * source_quality +
      0.13 * confidence_level +
      0.15 * evidence_relevance +
      0.15 * counterevidence_visibility +
      0.14 * transfer_fit +
      0.14 * (1 - overclaim_risk) +
      0.14 * (1 - narrative_pressure),
      4
    ) AS claim_integrity_score,
    ROUND(
      0.32 * overclaim_risk +
      0.20 * narrative_pressure +
      0.14 * (1 - source_quality) +
      0.12 * (1 - evidence_relevance) +
      0.12 * (1 - counterevidence_visibility) +
      0.10 * (1 - transfer_fit),
      4
    ) AS overclaim_exposure
FROM evidence_overclaim;

CREATE VIEW implementation_incentive_scores AS
SELECT
    impl_id,
    idea_id,
    ROUND(
      0.13 * capacity_fit +
      0.12 * role_clarity +
      0.12 * dependency_visibility +
      0.10 * technical_readiness +
      0.13 * stakeholder_trust +
      0.14 * incentive_alignment +
      0.10 * (1 - gaming_risk) +
      0.08 * (1 - hidden_labor) +
      0.08 * (1 - adoption_assumption_risk),
      4
    ) AS implementation_readiness_score,
    ROUND(
      0.12 * (1 - capacity_fit) +
      0.11 * (1 - role_clarity) +
      0.11 * (1 - dependency_visibility) +
      0.10 * (1 - technical_readiness) +
      0.12 * (1 - stakeholder_trust) +
      0.13 * (1 - incentive_alignment) +
      0.13 * gaming_risk +
      0.10 * hidden_labor +
      0.08 * adoption_assumption_risk,
      4
    ) AS implementation_incentive_risk
FROM implementation_incentives;

CREATE VIEW power_narrative_learning_scores AS
SELECT
    pnl_id,
    idea_id,
    ROUND(
      0.12 * (1 - sponsor_power) +
      0.10 * (1 - narrative_strength) +
      0.13 * dissent_visibility +
      0.13 * red_team_quality +
      0.15 * stop_rule_quality +
      0.15 * revision_trigger_quality +
      0.12 * decision_memory_quality +
      0.10 * ai_review_quality,
      4
    ) AS learning_integrity_score,
    ROUND(
      0.20 * power_protection_risk +
      0.15 * sponsor_power +
      0.13 * narrative_strength +
      0.12 * (1 - dissent_visibility) +
      0.12 * (1 - red_team_quality) +
      0.10 * (1 - stop_rule_quality) +
      0.10 * (1 - revision_trigger_quality) +
      0.08 * (1 - ai_review_quality),
      4
    ) AS power_narrative_risk
FROM power_narrative_learning;
