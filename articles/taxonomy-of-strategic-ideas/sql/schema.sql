-- Advanced SQL schema for Taxonomy of Strategic Ideas.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS taxonomy_record_scores;
DROP VIEW IF EXISTS classification_error_scores;
DROP VIEW IF EXISTS relationship_quality_scores;
DROP VIEW IF EXISTS retrieval_test_scores;
DROP VIEW IF EXISTS governance_ethics_scores;

DROP TABLE IF EXISTS governance_ethics;
DROP TABLE IF EXISTS retrieval_tests;
DROP TABLE IF EXISTS idea_relationships;
DROP TABLE IF EXISTS classification_errors;
DROP TABLE IF EXISTS taxonomy_records;

CREATE TABLE taxonomy_records (
    record_id TEXT PRIMARY KEY,
    idea_record TEXT NOT NULL,
    idea_type TEXT,
    strategic_level TEXT,
    maturity_state TEXT,
    evidence_status TEXT,
    strategic_function TEXT,
    category_clarity REAL,
    level_fit REAL,
    maturity_accuracy REAL,
    evidence_classification REAL,
    function_clarity REAL,
    relationship_mapping REAL,
    retrieval_value REAL,
    governance_strength REAL,
    ethical_visibility REAL,
    ai_classification_quality REAL,
    description TEXT
);

CREATE TABLE classification_errors (
    error_id TEXT PRIMARY KEY,
    record_id TEXT NOT NULL,
    error_type TEXT,
    error_description TEXT,
    severity REAL,
    likelihood REAL,
    detectability REAL,
    repair_quality REAL,
    governance_need REAL,
    review_action TEXT,
    FOREIGN KEY (record_id) REFERENCES taxonomy_records(record_id)
);

CREATE TABLE idea_relationships (
    relationship_id TEXT PRIMARY KEY,
    source_record TEXT NOT NULL,
    target_record TEXT NOT NULL,
    relationship_type TEXT,
    relationship_clarity REAL,
    strategic_importance REAL,
    evidence_support REAL,
    governance_visibility REAL,
    reuse_value REAL,
    review_action TEXT,
    FOREIGN KEY (source_record) REFERENCES taxonomy_records(record_id),
    FOREIGN KEY (target_record) REFERENCES taxonomy_records(record_id)
);

CREATE TABLE retrieval_tests (
    test_id TEXT PRIMARY KEY,
    query_type TEXT,
    query_text TEXT,
    expected_record TEXT NOT NULL,
    relevance REAL,
    context_completeness REAL,
    classification_accuracy REAL,
    searchability REAL,
    decision_usefulness REAL,
    transfer_caution REAL,
    ethical_visibility REAL,
    review_action TEXT,
    FOREIGN KEY (expected_record) REFERENCES taxonomy_records(record_id)
);

CREATE TABLE governance_ethics (
    governance_id TEXT PRIMARY KEY,
    taxonomy_area TEXT,
    category_ownership REAL,
    definition_quality REAL,
    change_control REAL,
    metadata_quality REAL,
    review_cadence REAL,
    user_guidance REAL,
    ai_review REAL,
    stakeholder_visibility REAL,
    dissent_preservation REAL,
    burden_visibility REAL,
    ethical_risk REAL,
    review_action TEXT
);

CREATE VIEW taxonomy_record_scores AS
SELECT
    record_id,
    idea_record,
    idea_type,
    strategic_level,
    maturity_state,
    evidence_status,
    strategic_function,
    ROUND(
      0.12 * category_clarity +
      0.10 * level_fit +
      0.10 * maturity_accuracy +
      0.12 * evidence_classification +
      0.12 * function_clarity +
      0.10 * relationship_mapping +
      0.12 * retrieval_value +
      0.09 * governance_strength +
      0.08 * ethical_visibility +
      0.05 * ai_classification_quality,
      4
    ) AS taxonomy_strength,
    ROUND(
      0.12 * (1 - category_clarity) +
      0.10 * (1 - level_fit) +
      0.10 * (1 - maturity_accuracy) +
      0.12 * (1 - evidence_classification) +
      0.12 * (1 - function_clarity) +
      0.10 * (1 - relationship_mapping) +
      0.12 * (1 - retrieval_value) +
      0.09 * (1 - governance_strength) +
      0.08 * (1 - ethical_visibility) +
      0.05 * (1 - ai_classification_quality),
      4
    ) AS taxonomy_risk
FROM taxonomy_records;

CREATE VIEW classification_error_scores AS
SELECT
    error_id,
    record_id,
    error_type,
    ROUND(
      0.30 * severity +
      0.25 * likelihood +
      0.20 * (1 - detectability) +
      0.15 * (1 - repair_quality) +
      0.10 * governance_need,
      4
    ) AS classification_error_risk
FROM classification_errors;

CREATE VIEW relationship_quality_scores AS
SELECT
    relationship_id,
    source_record,
    target_record,
    relationship_type,
    ROUND(
      0.22 * relationship_clarity +
      0.24 * strategic_importance +
      0.18 * evidence_support +
      0.16 * governance_visibility +
      0.20 * reuse_value,
      4
    ) AS relationship_quality_score
FROM idea_relationships;

CREATE VIEW retrieval_test_scores AS
SELECT
    test_id,
    query_type,
    expected_record,
    ROUND(
      0.14 * relevance +
      0.13 * context_completeness +
      0.14 * classification_accuracy +
      0.13 * searchability +
      0.15 * decision_usefulness +
      0.13 * transfer_caution +
      0.18 * ethical_visibility,
      4
    ) AS retrieval_test_score
FROM retrieval_tests;

CREATE VIEW governance_ethics_scores AS
SELECT
    governance_id,
    taxonomy_area,
    ROUND(
      0.11 * category_ownership +
      0.13 * definition_quality +
      0.11 * change_control +
      0.12 * metadata_quality +
      0.10 * review_cadence +
      0.10 * user_guidance +
      0.08 * ai_review +
      0.09 * stakeholder_visibility +
      0.08 * dissent_preservation +
      0.08 * burden_visibility -
      0.05 * ethical_risk +
      0.05,
      4
    ) AS taxonomy_stewardship_score,
    ROUND(
      0.20 * ethical_risk +
      0.13 * (1 - stakeholder_visibility) +
      0.13 * (1 - dissent_preservation) +
      0.13 * (1 - burden_visibility) +
      0.11 * (1 - definition_quality) +
      0.10 * (1 - metadata_quality) +
      0.10 * (1 - ai_review) +
      0.10 * (1 - change_control),
      4
    ) AS ethical_classification_risk
FROM governance_ethics;
