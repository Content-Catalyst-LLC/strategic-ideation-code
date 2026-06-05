-- Advanced SQL schema for Knowledge Architecture in Strategic Ideation.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS idea_architecture_scores;
DROP VIEW IF EXISTS evidence_assumption_scores;
DROP VIEW IF EXISTS relationship_mapping_scores;
DROP VIEW IF EXISTS retrieval_reuse_scores;
DROP VIEW IF EXISTS stewardship_ethics_scores;

DROP TABLE IF EXISTS stewardship_ethics;
DROP TABLE IF EXISTS retrieval_tests;
DROP TABLE IF EXISTS evidence_assumptions;
DROP TABLE IF EXISTS relationships;
DROP TABLE IF EXISTS idea_records;

CREATE TABLE idea_records (
    idea_id TEXT PRIMARY KEY,
    idea_title TEXT NOT NULL,
    domain TEXT NOT NULL,
    strategic_function TEXT,
    maturity TEXT,
    evidence_level TEXT,
    decision_status TEXT,
    taxonomy_quality REAL CHECK (taxonomy_quality BETWEEN 0 AND 1),
    metadata_completeness REAL CHECK (metadata_completeness BETWEEN 0 AND 1),
    semantic_clarity REAL CHECK (semantic_clarity BETWEEN 0 AND 1),
    evidence_linkage REAL CHECK (evidence_linkage BETWEEN 0 AND 1),
    assumption_clarity REAL CHECK (assumption_clarity BETWEEN 0 AND 1),
    relationship_mapping REAL CHECK (relationship_mapping BETWEEN 0 AND 1),
    retrieval_readiness REAL CHECK (retrieval_readiness BETWEEN 0 AND 1),
    decision_memory REAL CHECK (decision_memory BETWEEN 0 AND 1),
    stewardship_quality REAL CHECK (stewardship_quality BETWEEN 0 AND 1),
    ethical_representation REAL CHECK (ethical_representation BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE relationships (
    relationship_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    target_id TEXT NOT NULL,
    relationship_type TEXT,
    relationship_strength REAL,
    relationship_confidence REAL,
    strategic_value REAL,
    maintenance_need REAL,
    review_action TEXT,
    FOREIGN KEY (source_id) REFERENCES idea_records(idea_id),
    FOREIGN KEY (target_id) REFERENCES idea_records(idea_id)
);

CREATE TABLE evidence_assumptions (
    record_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    knowledge_type TEXT,
    item_name TEXT,
    source_quality REAL,
    confidence_level REAL,
    review_frequency REAL,
    uncertainty_level REAL,
    counterevidence_visibility REAL,
    owner_clarity REAL,
    revision_trigger_quality REAL,
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES idea_records(idea_id)
);

CREATE TABLE retrieval_tests (
    test_id TEXT PRIMARY KEY,
    query_type TEXT,
    query_text TEXT,
    expected_idea_id TEXT NOT NULL,
    relevance REAL,
    context_completeness REAL,
    trustworthiness REAL,
    usability REAL,
    searchability REAL,
    reuse_potential REAL,
    review_action TEXT,
    FOREIGN KEY (expected_idea_id) REFERENCES idea_records(idea_id)
);

CREATE TABLE stewardship_ethics (
    stewardship_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    taxonomy_stewardship REAL,
    metadata_stewardship REAL,
    evidence_standard_quality REAL,
    repository_curation REAL,
    access_governance REAL,
    privacy_sensitivity REAL,
    stakeholder_representation REAL,
    dissent_preservation REAL,
    ethical_risk REAL,
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES idea_records(idea_id)
);

CREATE VIEW idea_architecture_scores AS
SELECT
    idea_id,
    idea_title,
    domain,
    maturity,
    evidence_level,
    decision_status,
    ROUND(
      0.11 * taxonomy_quality +
      0.12 * metadata_completeness +
      0.11 * semantic_clarity +
      0.12 * evidence_linkage +
      0.11 * assumption_clarity +
      0.11 * relationship_mapping +
      0.12 * retrieval_readiness +
      0.09 * decision_memory +
      0.07 * stewardship_quality +
      0.04 * ethical_representation,
      4
    ) AS architecture_strength,
    ROUND(
      0.11 * (1 - taxonomy_quality) +
      0.12 * (1 - metadata_completeness) +
      0.12 * (1 - semantic_clarity) +
      0.13 * (1 - evidence_linkage) +
      0.12 * (1 - assumption_clarity) +
      0.10 * (1 - relationship_mapping) +
      0.12 * (1 - retrieval_readiness) +
      0.09 * (1 - decision_memory) +
      0.06 * (1 - stewardship_quality) +
      0.03 * (1 - ethical_representation),
      4
    ) AS architecture_risk
FROM idea_records;

CREATE VIEW evidence_assumption_scores AS
SELECT
    record_id,
    idea_id,
    knowledge_type,
    item_name,
    ROUND(
      0.17 * source_quality +
      0.18 * confidence_level +
      0.13 * review_frequency -
      0.12 * uncertainty_level +
      0.12 * counterevidence_visibility +
      0.14 * owner_clarity +
      0.16 * revision_trigger_quality +
      0.12,
      4
    ) AS evidence_assumption_score
FROM evidence_assumptions;

CREATE VIEW relationship_mapping_scores AS
SELECT
    relationship_id,
    source_id,
    target_id,
    relationship_type,
    ROUND(
      0.26 * relationship_strength +
      0.24 * relationship_confidence +
      0.28 * strategic_value -
      0.12 * maintenance_need +
      0.10,
      4
    ) AS relationship_mapping_score
FROM relationships;

CREATE VIEW retrieval_reuse_scores AS
SELECT
    test_id,
    query_type,
    expected_idea_id,
    ROUND(
      0.16 * relevance +
      0.15 * context_completeness +
      0.16 * trustworthiness +
      0.14 * usability +
      0.14 * searchability +
      0.15 * reuse_potential +
      0.10,
      4
    ) AS retrieval_reuse_score
FROM retrieval_tests;

CREATE VIEW stewardship_ethics_scores AS
SELECT
    stewardship_id,
    idea_id,
    ROUND(
      0.13 * taxonomy_stewardship +
      0.13 * metadata_stewardship +
      0.13 * evidence_standard_quality +
      0.13 * repository_curation +
      0.11 * access_governance -
      0.07 * privacy_sensitivity +
      0.13 * stakeholder_representation +
      0.12 * dissent_preservation -
      0.05 * ethical_risk +
      0.04,
      4
    ) AS stewardship_score,
    ROUND(
      0.22 * ethical_risk +
      0.14 * privacy_sensitivity +
      0.16 * (1 - stakeholder_representation) +
      0.14 * (1 - dissent_preservation) +
      0.12 * (1 - access_governance) +
      0.10 * (1 - evidence_standard_quality) +
      0.12 * (1 - repository_curation),
      4
    ) AS ethical_knowledge_risk
FROM stewardship_ethics;
