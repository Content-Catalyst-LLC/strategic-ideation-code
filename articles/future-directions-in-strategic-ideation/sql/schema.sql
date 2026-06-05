-- Advanced SQL schema for Future Directions in Strategic Ideation.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS future_ready_idea_scores;
DROP VIEW IF EXISTS scenario_option_scores;
DROP VIEW IF EXISTS ai_governance_scores;
DROP VIEW IF EXISTS collective_intelligence_scores;
DROP VIEW IF EXISTS learning_memory_scores;

DROP TABLE IF EXISTS learning_memory;
DROP TABLE IF EXISTS collective_intelligence;
DROP TABLE IF EXISTS ai_governance;
DROP TABLE IF EXISTS scenario_options;
DROP TABLE IF EXISTS future_ideas;

CREATE TABLE future_ideas (
    idea_id TEXT PRIMARY KEY,
    idea TEXT NOT NULL,
    idea_type TEXT,
    problem_frame_quality REAL,
    evidence_quality REAL,
    adaptability REAL,
    scenario_robustness REAL,
    stakeholder_legitimacy REAL,
    implementation_readiness REAL,
    ethical_visibility REAL,
    learning_design REAL,
    option_value REAL,
    ai_governance REAL,
    systems_responsibility REAL,
    description TEXT
);

CREATE TABLE scenario_options (
    scenario_option_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    scenario TEXT,
    scenario_performance REAL,
    adaptation_capacity REAL,
    option_preservation REAL,
    lock_in_risk REAL,
    learning_value REAL,
    resilience_contribution REAL,
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES future_ideas(idea_id)
);

CREATE TABLE ai_governance (
    ai_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    ai_use_case TEXT,
    disclosure_quality REAL,
    source_traceability REAL,
    human_review REAL,
    bias_review REAL,
    stakeholder_review REAL,
    uncertainty_preservation REAL,
    accountability_clarity REAL,
    fluency_risk REAL,
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES future_ideas(idea_id)
);

CREATE TABLE collective_intelligence (
    ci_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    knowledge_source TEXT,
    executive_alignment REAL,
    frontline_voice REAL,
    stakeholder_voice REAL,
    technical_expertise REAL,
    analytical_support REAL,
    dissent_protection REAL,
    synthesis_quality REAL,
    participation_influence REAL,
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES future_ideas(idea_id)
);

CREATE TABLE learning_memory (
    lm_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    idea_metadata_quality REAL,
    decision_memory_quality REAL,
    retrieval_quality REAL,
    experiment_design REAL,
    stop_rule_quality REAL,
    revision_trigger_quality REAL,
    outcome_learning REAL,
    knowledge_reuse_value REAL,
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES future_ideas(idea_id)
);

CREATE VIEW future_ready_idea_scores AS
SELECT
    idea_id,
    idea,
    idea_type,
    ROUND(
      0.10 * problem_frame_quality +
      0.10 * evidence_quality +
      0.10 * adaptability +
      0.11 * scenario_robustness +
      0.10 * stakeholder_legitimacy +
      0.09 * implementation_readiness +
      0.10 * ethical_visibility +
      0.11 * learning_design +
      0.08 * option_value +
      0.06 * ai_governance +
      0.05 * systems_responsibility,
      4
    ) AS future_ready_score,
    ROUND(
      1 -
      (0.10 * problem_frame_quality +
       0.10 * evidence_quality +
       0.10 * adaptability +
       0.11 * scenario_robustness +
       0.10 * stakeholder_legitimacy +
       0.09 * implementation_readiness +
       0.10 * ethical_visibility +
       0.11 * learning_design +
       0.08 * option_value +
       0.06 * ai_governance +
       0.05 * systems_responsibility),
      4
    ) AS future_risk
FROM future_ideas;

CREATE VIEW scenario_option_scores AS
SELECT
    scenario_option_id,
    idea_id,
    scenario,
    ROUND(
      0.20 * scenario_performance +
      0.18 * adaptation_capacity +
      0.18 * option_preservation +
      0.14 * (1 - lock_in_risk) +
      0.15 * learning_value +
      0.15 * resilience_contribution,
      4
    ) AS scenario_option_score,
    ROUND(
      0.20 * (1 - scenario_performance) +
      0.18 * (1 - adaptation_capacity) +
      0.16 * (1 - option_preservation) +
      0.18 * lock_in_risk +
      0.14 * (1 - learning_value) +
      0.14 * (1 - resilience_contribution),
      4
    ) AS scenario_risk
FROM scenario_options;

CREATE VIEW ai_governance_scores AS
SELECT
    ai_id,
    idea_id,
    ai_use_case,
    ROUND(
      0.13 * disclosure_quality +
      0.14 * source_traceability +
      0.14 * human_review +
      0.13 * bias_review +
      0.13 * stakeholder_review +
      0.13 * uncertainty_preservation +
      0.12 * accountability_clarity +
      0.08 * (1 - fluency_risk),
      4
    ) AS ai_governance_score,
    ROUND(
      0.22 * fluency_risk +
      0.12 * (1 - disclosure_quality) +
      0.14 * (1 - source_traceability) +
      0.12 * (1 - human_review) +
      0.12 * (1 - bias_review) +
      0.10 * (1 - stakeholder_review) +
      0.10 * (1 - uncertainty_preservation) +
      0.08 * (1 - accountability_clarity),
      4
    ) AS ai_risk
FROM ai_governance;

CREATE VIEW collective_intelligence_scores AS
SELECT
    ci_id,
    idea_id,
    knowledge_source,
    ROUND(
      0.10 * executive_alignment +
      0.13 * frontline_voice +
      0.15 * stakeholder_voice +
      0.12 * technical_expertise +
      0.12 * analytical_support +
      0.14 * dissent_protection +
      0.12 * synthesis_quality +
      0.12 * participation_influence,
      4
    ) AS collective_intelligence_score,
    ROUND(MAX(0, stakeholder_voice - participation_influence), 4) AS participation_gap
FROM collective_intelligence;

CREATE VIEW learning_memory_scores AS
SELECT
    lm_id,
    idea_id,
    ROUND(
      0.13 * idea_metadata_quality +
      0.14 * decision_memory_quality +
      0.13 * retrieval_quality +
      0.12 * experiment_design +
      0.12 * stop_rule_quality +
      0.12 * revision_trigger_quality +
      0.12 * outcome_learning +
      0.12 * knowledge_reuse_value,
      4
    ) AS learning_memory_score,
    ROUND(
      0.13 * (1 - idea_metadata_quality) +
      0.14 * (1 - decision_memory_quality) +
      0.13 * (1 - retrieval_quality) +
      0.12 * (1 - experiment_design) +
      0.12 * (1 - stop_rule_quality) +
      0.12 * (1 - revision_trigger_quality) +
      0.12 * (1 - outcome_learning) +
      0.12 * (1 - knowledge_reuse_value),
      4
    ) AS learning_memory_risk
FROM learning_memory;
