-- Advanced SQL schema for strategic ideation systems.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS idea_weighted_scores;
DROP VIEW IF EXISTS assumption_risk_register;
DROP VIEW IF EXISTS option_architecture_scores;
DROP VIEW IF EXISTS implementation_pathway_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS implementation_pathways;
DROP TABLE IF EXISTS prototype_plan;
DROP TABLE IF EXISTS evidence_register;
DROP TABLE IF EXISTS assumptions;
DROP TABLE IF EXISTS option_architecture;
DROP TABLE IF EXISTS idea_evaluations;
DROP TABLE IF EXISTS criteria;
DROP TABLE IF EXISTS ideas;

CREATE TABLE ideas (
    idea_id TEXT PRIMARY KEY,
    idea_name TEXT NOT NULL,
    idea_type TEXT NOT NULL,
    problem_frame TEXT NOT NULL,
    strategic_fit REAL CHECK (strategic_fit BETWEEN 0 AND 1),
    feasibility REAL CHECK (feasibility BETWEEN 0 AND 1),
    systems_leverage REAL CHECK (systems_leverage BETWEEN 0 AND 1),
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    ethical_legitimacy REAL CHECK (ethical_legitimacy BETWEEN 0 AND 1),
    knowledge_reusability REAL CHECK (knowledge_reusability BETWEEN 0 AND 1),
    uncertainty REAL CHECK (uncertainty BETWEEN 0 AND 1),
    estimated_cost REAL,
    implementation_months INTEGER
);

CREATE TABLE criteria (
    criterion_id TEXT PRIMARY KEY,
    criterion_name TEXT NOT NULL,
    weight REAL NOT NULL CHECK (weight >= 0),
    description TEXT
);

CREATE TABLE idea_evaluations (
    evaluation_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    criterion_id TEXT NOT NULL,
    score REAL NOT NULL CHECK (score BETWEEN 0 AND 1),
    evaluator_role TEXT,
    evidence_note TEXT,
    evaluated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (idea_id) REFERENCES ideas(idea_id),
    FOREIGN KEY (criterion_id) REFERENCES criteria(criterion_id)
);

CREATE TABLE option_architecture (
    option_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    option_role TEXT NOT NULL,
    time_horizon TEXT CHECK (time_horizon IN ('short', 'medium', 'long')),
    commitment_level TEXT CHECK (commitment_level IN ('low', 'medium', 'high')),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    dependency_complexity REAL CHECK (dependency_complexity BETWEEN 0 AND 1),
    portfolio_fit REAL CHECK (portfolio_fit BETWEEN 0 AND 1),
    scenario_robustness REAL CHECK (scenario_robustness BETWEEN 0 AND 1),
    sequencing_value REAL CHECK (sequencing_value BETWEEN 0 AND 1),
    description TEXT,
    FOREIGN KEY (idea_id) REFERENCES ideas(idea_id)
);

CREATE TABLE assumptions (
    assumption_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    assumption_text TEXT NOT NULL,
    layer TEXT NOT NULL,
    confidence REAL CHECK (confidence BETWEEN 0 AND 1),
    criticality REAL CHECK (criticality BETWEEN 0 AND 1),
    test_method TEXT,
    evidence_status TEXT CHECK (evidence_status IN ('untested', 'partial', 'strong', 'contested')),
    FOREIGN KEY (idea_id) REFERENCES ideas(idea_id)
);

CREATE TABLE evidence_register (
    evidence_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    evidence_type TEXT NOT NULL,
    evidence_summary TEXT NOT NULL,
    evidence_quality REAL CHECK (evidence_quality BETWEEN 0 AND 1),
    relevance REAL CHECK (relevance BETWEEN 0 AND 1),
    recency REAL CHECK (recency BETWEEN 0 AND 1),
    contestation REAL CHECK (contestation BETWEEN 0 AND 1),
    source_type TEXT,
    FOREIGN KEY (idea_id) REFERENCES ideas(idea_id)
);

CREATE TABLE prototype_plan (
    prototype_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    prototype_name TEXT NOT NULL,
    learning_goal TEXT,
    minimum_test TEXT,
    success_signal TEXT,
    review_layer TEXT,
    estimated_weeks INTEGER,
    resource_intensity TEXT CHECK (resource_intensity IN ('low', 'medium', 'high')),
    FOREIGN KEY (idea_id) REFERENCES ideas(idea_id)
);

CREATE TABLE implementation_pathways (
    pathway_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    pathway_name TEXT NOT NULL,
    phase_1 TEXT,
    phase_2 TEXT,
    phase_3 TEXT,
    dependency_count INTEGER,
    owner_clarity REAL CHECK (owner_clarity BETWEEN 0 AND 1),
    feedback_strength REAL CHECK (feedback_strength BETWEEN 0 AND 1),
    governance_fit REAL CHECK (governance_fit BETWEEN 0 AND 1),
    scaling_risk REAL CHECK (scaling_risk BETWEEN 0 AND 1),
    FOREIGN KEY (idea_id) REFERENCES ideas(idea_id)
);

CREATE TABLE decision_memory (
    decision_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    decision_date TEXT,
    decision_summary TEXT NOT NULL,
    chosen_option TEXT,
    rejected_options TEXT,
    rationale TEXT,
    assumptions_to_revisit TEXT,
    next_review_trigger TEXT,
    FOREIGN KEY (idea_id) REFERENCES ideas(idea_id)
);

CREATE VIEW idea_weighted_scores AS
SELECT
    idea_id,
    idea_name,
    idea_type,
    ROUND(
      0.20 * strategic_fit +
      0.12 * feasibility +
      0.18 * systems_leverage +
      0.13 * learning_value +
      0.16 * ethical_legitimacy +
      0.09 * knowledge_reusability -
      0.07 * uncertainty,
      4
    ) AS weighted_score
FROM ideas;

CREATE VIEW assumption_risk_register AS
SELECT
    assumption_id,
    idea_id,
    layer,
    assumption_text,
    confidence,
    criticality,
    ROUND((1.0 - confidence) * criticality, 4) AS assumption_risk,
    test_method,
    evidence_status
FROM assumptions
ORDER BY assumption_risk DESC;

CREATE VIEW option_architecture_scores AS
SELECT
    option_id,
    idea_id,
    option_role,
    time_horizon,
    commitment_level,
    ROUND(
      0.16 * reversibility -
      0.10 * dependency_complexity +
      0.24 * portfolio_fit +
      0.24 * scenario_robustness +
      0.22 * sequencing_value,
      4
    ) AS architecture_score
FROM option_architecture;

CREATE VIEW implementation_pathway_scores AS
SELECT
    pathway_id,
    idea_id,
    pathway_name,
    ROUND(
      0.20 * owner_clarity +
      0.24 * feedback_strength +
      0.22 * governance_fit -
      0.10 * scaling_risk -
      0.03 * dependency_count,
      4
    ) AS pathway_score
FROM implementation_pathways;
