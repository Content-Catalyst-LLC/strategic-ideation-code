-- Strategic Ideation SQL schema
-- SQLite-compatible schema for ideas, criteria, assumptions, evaluations, prototypes, and implementation records.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS implementation_records;
DROP TABLE IF EXISTS prototypes;
DROP TABLE IF EXISTS evaluations;
DROP TABLE IF EXISTS assumptions;
DROP TABLE IF EXISTS criteria;
DROP TABLE IF EXISTS ideas;

CREATE TABLE ideas (
    idea_id TEXT PRIMARY KEY,
    idea_name TEXT NOT NULL,
    category TEXT NOT NULL,
    summary TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE criteria (
    criterion_id TEXT PRIMARY KEY,
    criterion_name TEXT NOT NULL,
    weight REAL NOT NULL CHECK (weight >= 0),
    description TEXT
);

CREATE TABLE assumptions (
    assumption_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    assumption_text TEXT NOT NULL,
    confidence REAL CHECK (confidence BETWEEN 0 AND 1),
    criticality REAL CHECK (criticality BETWEEN 0 AND 1),
    test_method TEXT,
    FOREIGN KEY (idea_id) REFERENCES ideas(idea_id)
);

CREATE TABLE evaluations (
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

CREATE TABLE prototypes (
    prototype_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    prototype_name TEXT NOT NULL,
    learning_goal TEXT,
    status TEXT CHECK (status IN ('planned', 'active', 'completed', 'paused', 'stopped')),
    FOREIGN KEY (idea_id) REFERENCES ideas(idea_id)
);

CREATE TABLE implementation_records (
    record_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    decision_status TEXT CHECK (decision_status IN ('hold', 'prototype', 'advance', 'revise', 'retire')),
    decision_rationale TEXT,
    next_review_date TEXT,
    FOREIGN KEY (idea_id) REFERENCES ideas(idea_id)
);

INSERT INTO ideas (idea_id, idea_name, category, summary) VALUES
('I001', 'Strategic idea repository', 'knowledge_architecture', 'Create reusable structure for idea capture, comparison, and learning.'),
('I002', 'Assumption mapping workshop', 'decision_process', 'Expose critical assumptions before selecting strategic options.'),
('I003', 'Scenario-based option review', 'foresight', 'Compare ideas across plausible future conditions.');

INSERT INTO criteria (criterion_id, criterion_name, weight, description) VALUES
('C001', 'Strategic Fit', 0.24, 'Alignment with mission, problem frame, and long-term direction.'),
('C002', 'Feasibility', 0.16, 'Capacity to implement with realistic resources.'),
('C003', 'Systems Leverage', 0.20, 'Potential to influence deeper structures, feedbacks, or incentives.'),
('C004', 'Learning Value', 0.14, 'Ability to generate useful evidence.'),
('C005', 'Ethical Legitimacy', 0.18, 'Attention to voice, burdens, accountability, and distributional effects.'),
('C006', 'Uncertainty Penalty', 0.08, 'Penalty for fragile assumptions or weak evidence.');

CREATE VIEW weighted_evaluation_scores AS
SELECT
    e.idea_id,
    i.idea_name,
    SUM(e.score * c.weight) AS weighted_score
FROM evaluations e
JOIN criteria c ON e.criterion_id = c.criterion_id
JOIN ideas i ON e.idea_id = i.idea_id
GROUP BY e.idea_id, i.idea_name;
