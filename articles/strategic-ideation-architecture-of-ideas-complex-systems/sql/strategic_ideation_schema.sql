-- Strategic Ideation SQL schema
-- Educational schema for ideas, criteria, assumptions, evaluations, prototypes, and implementation pathways.

CREATE TABLE IF NOT EXISTS strategic_projects (
    project_id INTEGER PRIMARY KEY,
    project_name TEXT NOT NULL,
    description TEXT NOT NULL,
    problem_frame TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS strategic_ideas (
    idea_id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL,
    idea_name TEXT NOT NULL,
    idea_description TEXT NOT NULL,
    idea_type TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES strategic_projects(project_id)
);

CREATE TABLE IF NOT EXISTS evaluation_criteria (
    criterion_id INTEGER PRIMARY KEY,
    criterion_name TEXT NOT NULL,
    description TEXT NOT NULL,
    weight REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS idea_evaluations (
    evaluation_id INTEGER PRIMARY KEY,
    idea_id INTEGER NOT NULL,
    criterion_id INTEGER NOT NULL,
    score_value REAL NOT NULL,
    evidence_note TEXT,
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id),
    FOREIGN KEY (criterion_id) REFERENCES evaluation_criteria(criterion_id)
);

CREATE TABLE IF NOT EXISTS assumptions (
    assumption_id INTEGER PRIMARY KEY,
    idea_id INTEGER NOT NULL,
    assumption_text TEXT NOT NULL,
    confidence REAL NOT NULL,
    impact_if_wrong REAL NOT NULL,
    testing_method TEXT NOT NULL,
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id)
);

CREATE TABLE IF NOT EXISTS prototypes (
    prototype_id INTEGER PRIMARY KEY,
    idea_id INTEGER NOT NULL,
    prototype_name TEXT NOT NULL,
    prototype_type TEXT NOT NULL,
    learning_goal TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id)
);

CREATE TABLE IF NOT EXISTS implementation_pathways (
    pathway_id INTEGER PRIMARY KEY,
    idea_id INTEGER NOT NULL,
    milestone_name TEXT NOT NULL,
    sequence_order INTEGER NOT NULL,
    dependency_note TEXT,
    measurement_note TEXT,
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id)
);

INSERT INTO strategic_projects
(project_id, project_name, description, problem_frame)
VALUES
(1, 'Strategic Ideation Portfolio', 'Synthetic educational project for modeling strategic ideas.', 'How can institutions structure, compare, and revise strategic ideas under uncertainty?');

INSERT INTO evaluation_criteria
(criterion_id, criterion_name, description, weight)
VALUES
(1, 'Novelty', 'Degree to which the idea creates a new pathway or reframes the problem.', 0.16),
(2, 'Relevance', 'Degree to which the idea addresses the problem frame.', 0.20),
(3, 'Feasibility', 'Degree to which the idea can be explored or implemented with available capacity.', 0.16),
(4, 'Strategic Fit', 'Degree of alignment with strategic goals.', 0.20),
(5, 'Learning Potential', 'Degree to which the idea can generate useful feedback.', 0.14),
(6, 'Risk', 'Degree of uncertainty, downside, or implementation risk.', -0.08),
(7, 'Implementation Readiness', 'Degree to which the idea can move toward action.', 0.14);
