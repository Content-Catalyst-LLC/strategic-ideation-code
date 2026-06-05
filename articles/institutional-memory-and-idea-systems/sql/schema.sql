-- Advanced SQL schema for Institutional Memory and Idea Systems.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS memory_system_scores;
DROP VIEW IF EXISTS idea_lifecycle_scores;
DROP VIEW IF EXISTS decision_memory_scores;
DROP VIEW IF EXISTS retrieval_reuse_scores;
DROP VIEW IF EXISTS learning_update_scores;
DROP VIEW IF EXISTS stewardship_ethics_scores;

DROP TABLE IF EXISTS stewardship_ethics;
DROP TABLE IF EXISTS learning_updates;
DROP TABLE IF EXISTS retrieval_tests;
DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS idea_lifecycle;
DROP TABLE IF EXISTS memory_systems;

CREATE TABLE memory_systems (
    system_id TEXT PRIMARY KEY,
    system_area TEXT NOT NULL,
    system_type TEXT NOT NULL,
    capture_quality REAL CHECK (capture_quality BETWEEN 0 AND 1),
    metadata_completeness REAL CHECK (metadata_completeness BETWEEN 0 AND 1),
    context_preservation REAL CHECK (context_preservation BETWEEN 0 AND 1),
    decision_memory REAL CHECK (decision_memory BETWEEN 0 AND 1),
    learning_integration REAL CHECK (learning_integration BETWEEN 0 AND 1),
    retrieval_readiness REAL CHECK (retrieval_readiness BETWEEN 0 AND 1),
    reuse_potential REAL CHECK (reuse_potential BETWEEN 0 AND 1),
    stewardship_quality REAL CHECK (stewardship_quality BETWEEN 0 AND 1),
    continuity_resilience REAL CHECK (continuity_resilience BETWEEN 0 AND 1),
    ethical_memory REAL CHECK (ethical_memory BETWEEN 0 AND 1),
    ai_governance REAL CHECK (ai_governance BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE idea_lifecycle (
    idea_id TEXT PRIMARY KEY,
    idea_title TEXT NOT NULL,
    lifecycle_stage TEXT,
    source_quality REAL,
    problem_clarity REAL,
    mechanism_clarity REAL,
    evidence_level REAL,
    assumption_quality REAL,
    decision_status_quality REAL,
    learning_update_quality REAL,
    reuse_condition_quality REAL,
    review_action TEXT
);

CREATE TABLE decision_memory (
    decision_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    decision_type TEXT,
    rationale_quality REAL,
    evidence_quality REAL,
    assumption_visibility REAL,
    alternative_visibility REAL,
    tradeoff_visibility REAL,
    dissent_preservation REAL,
    owner_clarity REAL,
    revision_trigger_quality REAL,
    traceability_quality REAL,
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES idea_lifecycle(idea_id)
);

CREATE TABLE retrieval_tests (
    test_id TEXT PRIMARY KEY,
    query_type TEXT,
    query_text TEXT,
    expected_record TEXT,
    relevance REAL,
    context_completeness REAL,
    trustworthiness REAL,
    timing_usefulness REAL,
    searchability REAL,
    reuse_potential REAL,
    transfer_caution_quality REAL,
    review_action TEXT
);

CREATE TABLE learning_updates (
    learning_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    learning_source TEXT,
    evidence_quality REAL,
    interpretation_quality REAL,
    assumption_update_quality REAL,
    decision_update_quality REAL,
    stakeholder_update_quality REAL,
    reuse_tag_quality REAL,
    followup_quality REAL,
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES idea_lifecycle(idea_id)
);

CREATE TABLE stewardship_ethics (
    stewardship_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    ownership_clarity REAL,
    lifecycle_governance REAL,
    metadata_stewardship REAL,
    repository_curation REAL,
    access_governance REAL,
    continuity_planning REAL,
    stakeholder_memory REAL,
    dissent_preservation REAL,
    privacy_sensitivity REAL,
    ethical_risk REAL,
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES memory_systems(system_id)
);

CREATE VIEW memory_system_scores AS
SELECT
    system_id,
    system_area,
    system_type,
    ROUND(
      0.09 * capture_quality +
      0.11 * metadata_completeness +
      0.11 * context_preservation +
      0.13 * decision_memory +
      0.12 * learning_integration +
      0.12 * retrieval_readiness +
      0.10 * reuse_potential +
      0.08 * stewardship_quality +
      0.06 * continuity_resilience +
      0.05 * ethical_memory +
      0.03 * ai_governance,
      4
    ) AS memory_strength,
    ROUND(
      0.09 * (1 - capture_quality) +
      0.11 * (1 - metadata_completeness) +
      0.11 * (1 - context_preservation) +
      0.13 * (1 - decision_memory) +
      0.12 * (1 - learning_integration) +
      0.12 * (1 - retrieval_readiness) +
      0.09 * (1 - reuse_potential) +
      0.08 * (1 - stewardship_quality) +
      0.07 * (1 - continuity_resilience) +
      0.05 * (1 - ethical_memory) +
      0.03 * (1 - ai_governance),
      4
    ) AS memory_failure_risk
FROM memory_systems;

CREATE VIEW idea_lifecycle_scores AS
SELECT
    idea_id,
    idea_title,
    lifecycle_stage,
    ROUND(
      0.11 * source_quality +
      0.13 * problem_clarity +
      0.12 * mechanism_clarity +
      0.13 * evidence_level +
      0.12 * assumption_quality +
      0.13 * decision_status_quality +
      0.13 * learning_update_quality +
      0.13 * reuse_condition_quality,
      4
    ) AS lifecycle_quality_score
FROM idea_lifecycle;

CREATE VIEW decision_memory_scores AS
SELECT
    decision_id,
    idea_id,
    decision_type,
    ROUND(
      0.13 * rationale_quality +
      0.13 * evidence_quality +
      0.12 * assumption_visibility +
      0.11 * alternative_visibility +
      0.12 * tradeoff_visibility +
      0.12 * dissent_preservation +
      0.10 * owner_clarity +
      0.13 * revision_trigger_quality +
      0.14 * traceability_quality,
      4
    ) AS decision_memory_score
FROM decision_memory;

CREATE VIEW retrieval_reuse_scores AS
SELECT
    test_id,
    query_type,
    expected_record,
    ROUND(
      0.15 * relevance +
      0.15 * context_completeness +
      0.15 * trustworthiness +
      0.13 * timing_usefulness +
      0.13 * searchability +
      0.15 * reuse_potential +
      0.14 * transfer_caution_quality,
      4
    ) AS retrieval_reuse_score
FROM retrieval_tests;

CREATE VIEW learning_update_scores AS
SELECT
    learning_id,
    idea_id,
    learning_source,
    ROUND(
      0.15 * evidence_quality +
      0.14 * interpretation_quality +
      0.14 * assumption_update_quality +
      0.14 * decision_update_quality +
      0.14 * stakeholder_update_quality +
      0.14 * reuse_tag_quality +
      0.15 * followup_quality,
      4
    ) AS learning_update_score
FROM learning_updates;

CREATE VIEW stewardship_ethics_scores AS
SELECT
    stewardship_id,
    system_id,
    ROUND(
      0.12 * ownership_clarity +
      0.12 * lifecycle_governance +
      0.13 * metadata_stewardship +
      0.12 * repository_curation +
      0.10 * access_governance +
      0.12 * continuity_planning +
      0.10 * stakeholder_memory +
      0.10 * dissent_preservation -
      0.04 * privacy_sensitivity -
      0.05 * ethical_risk +
      0.08,
      4
    ) AS stewardship_score,
    ROUND(
      0.20 * ethical_risk +
      0.14 * privacy_sensitivity +
      0.14 * (1 - stakeholder_memory) +
      0.14 * (1 - dissent_preservation) +
      0.12 * (1 - access_governance) +
      0.10 * (1 - metadata_stewardship) +
      0.08 * (1 - continuity_planning) +
      0.08 * (1 - repository_curation),
      4
    ) AS ethical_memory_risk
FROM stewardship_ethics;
