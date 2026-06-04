-- Advanced SQL schema for divergent vs convergent thinking.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS divergence_convergence_profiles;
DROP VIEW IF EXISTS premature_convergence_risks;
DROP VIEW IF EXISTS unbounded_divergence_risks;
DROP VIEW IF EXISTS idea_portfolio_scores;
DROP VIEW IF EXISTS criteria_quality_scores;
DROP VIEW IF EXISTS selection_integrity_scores;
DROP VIEW IF EXISTS stakeholder_inclusion_scores;
DROP VIEW IF EXISTS iteration_learning_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS stakeholder_review;
DROP TABLE IF EXISTS learning_cycles;
DROP TABLE IF EXISTS evaluation_rounds;
DROP TABLE IF EXISTS constraint_register;
DROP TABLE IF EXISTS evaluation_criteria;
DROP TABLE IF EXISTS idea_portfolio;
DROP TABLE IF EXISTS ideation_contexts;

CREATE TABLE ideation_contexts (
    context_id TEXT PRIMARY KEY,
    context_name TEXT NOT NULL,
    context_type TEXT NOT NULL,
    exploratory_breadth REAL CHECK (exploratory_breadth BETWEEN 0 AND 1),
    evaluative_discipline REAL CHECK (evaluative_discipline BETWEEN 0 AND 1),
    iteration_quality REAL CHECK (iteration_quality BETWEEN 0 AND 1),
    constraint_clarity REAL CHECK (constraint_clarity BETWEEN 0 AND 1),
    stakeholder_inclusion REAL CHECK (stakeholder_inclusion BETWEEN 0 AND 1),
    evidence_contact REAL CHECK (evidence_contact BETWEEN 0 AND 1),
    action_readiness REAL CHECK (action_readiness BETWEEN 0 AND 1),
    decision_memory_quality REAL CHECK (decision_memory_quality BETWEEN 0 AND 1),
    closure_pressure REAL CHECK (closure_pressure BETWEEN 0 AND 1)
);

CREATE TABLE idea_portfolio (
    idea_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    idea_name TEXT NOT NULL,
    novelty REAL CHECK (novelty BETWEEN 0 AND 1),
    strategic_fit REAL CHECK (strategic_fit BETWEEN 0 AND 1),
    evidence_strength REAL CHECK (evidence_strength BETWEEN 0 AND 1),
    feasibility REAL CHECK (feasibility BETWEEN 0 AND 1),
    stakeholder_value REAL CHECK (stakeholder_value BETWEEN 0 AND 1),
    risk_visibility REAL CHECK (risk_visibility BETWEEN 0 AND 1),
    ethical_legitimacy REAL CHECK (ethical_legitimacy BETWEEN 0 AND 1),
    implementation_readiness REAL CHECK (implementation_readiness BETWEEN 0 AND 1),
    assumption_burden REAL CHECK (assumption_burden BETWEEN 0 AND 1),
    FOREIGN KEY (context_id) REFERENCES ideation_contexts(context_id)
);

CREATE TABLE evaluation_criteria (
    criteria_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    criterion_name TEXT NOT NULL,
    definition_clarity REAL CHECK (definition_clarity BETWEEN 0 AND 1),
    weight_justification REAL CHECK (weight_justification BETWEEN 0 AND 1),
    measurement_validity REAL CHECK (measurement_validity BETWEEN 0 AND 1),
    bias_risk REAL CHECK (bias_risk BETWEEN 0 AND 1),
    stakeholder_relevance REAL CHECK (stakeholder_relevance BETWEEN 0 AND 1),
    strategic_importance REAL CHECK (strategic_importance BETWEEN 0 AND 1),
    review_priority TEXT,
    FOREIGN KEY (context_id) REFERENCES ideation_contexts(context_id)
);

CREATE TABLE constraint_register (
    constraint_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    constraint_name TEXT NOT NULL,
    constraint_type TEXT NOT NULL,
    is_real_constraint INTEGER CHECK (is_real_constraint IN (0, 1)),
    certainty REAL CHECK (certainty BETWEEN 0 AND 1),
    strategic_importance REAL CHECK (strategic_importance BETWEEN 0 AND 1),
    redesign_potential REAL CHECK (redesign_potential BETWEEN 0 AND 1),
    evidence_quality REAL CHECK (evidence_quality BETWEEN 0 AND 1),
    notes TEXT,
    FOREIGN KEY (context_id) REFERENCES ideation_contexts(context_id)
);

CREATE TABLE evaluation_rounds (
    round_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    round_name TEXT NOT NULL,
    mode TEXT NOT NULL,
    mode_clarity REAL CHECK (mode_clarity BETWEEN 0 AND 1),
    participation_quality REAL CHECK (participation_quality BETWEEN 0 AND 1),
    criteria_transparency REAL CHECK (criteria_transparency BETWEEN 0 AND 1),
    evidence_use REAL CHECK (evidence_use BETWEEN 0 AND 1),
    stakeholder_voice REAL CHECK (stakeholder_voice BETWEEN 0 AND 1),
    decision_documentation REAL CHECK (decision_documentation BETWEEN 0 AND 1),
    iteration_trigger_quality REAL CHECK (iteration_trigger_quality BETWEEN 0 AND 1),
    FOREIGN KEY (context_id) REFERENCES ideation_contexts(context_id)
);

CREATE TABLE learning_cycles (
    cycle_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    cycle_name TEXT NOT NULL,
    divergence_quality REAL CHECK (divergence_quality BETWEEN 0 AND 1),
    convergence_quality REAL CHECK (convergence_quality BETWEEN 0 AND 1),
    evidence_learning REAL CHECK (evidence_learning BETWEEN 0 AND 1),
    frame_revision REAL CHECK (frame_revision BETWEEN 0 AND 1),
    assumption_revision REAL CHECK (assumption_revision BETWEEN 0 AND 1),
    decision_memory REAL CHECK (decision_memory BETWEEN 0 AND 1),
    implementation_feedback REAL CHECK (implementation_feedback BETWEEN 0 AND 1),
    next_cycle_readiness REAL CHECK (next_cycle_readiness BETWEEN 0 AND 1),
    FOREIGN KEY (context_id) REFERENCES ideation_contexts(context_id)
);

CREATE TABLE stakeholder_review (
    review_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    stakeholder_group TEXT NOT NULL,
    inclusion_level REAL CHECK (inclusion_level BETWEEN 0 AND 1),
    influence_on_criteria REAL CHECK (influence_on_criteria BETWEEN 0 AND 1),
    influence_on_selection REAL CHECK (influence_on_selection BETWEEN 0 AND 1),
    burden_visibility REAL CHECK (burden_visibility BETWEEN 0 AND 1),
    knowledge_recognition REAL CHECK (knowledge_recognition BETWEEN 0 AND 1),
    legitimacy_signal REAL CHECK (legitimacy_signal BETWEEN 0 AND 1),
    review_quality REAL CHECK (review_quality BETWEEN 0 AND 1),
    FOREIGN KEY (context_id) REFERENCES ideation_contexts(context_id)
);

CREATE TABLE decision_memory (
    decision_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    idea_id TEXT,
    decision_date TEXT,
    current_mode TEXT,
    criteria_used TEXT,
    constraints_applied TEXT,
    stakeholders_consulted TEXT,
    ideas_rejected TEXT,
    ideas_deferred TEXT,
    evidence_considered TEXT,
    revision_trigger TEXT,
    FOREIGN KEY (context_id) REFERENCES ideation_contexts(context_id),
    FOREIGN KEY (idea_id) REFERENCES idea_portfolio(idea_id)
);

CREATE VIEW divergence_convergence_profiles AS
SELECT
    context_id,
    context_name,
    context_type,
    ROUND(
      0.16 * exploratory_breadth +
      0.16 * evaluative_discipline +
      0.18 * iteration_quality +
      0.14 * constraint_clarity +
      0.12 * stakeholder_inclusion +
      0.12 * evidence_contact +
      0.08 * action_readiness +
      0.04 * decision_memory_quality,
      4
    ) AS profile_score
FROM ideation_contexts;

CREATE VIEW premature_convergence_risks AS
SELECT
    context_id,
    context_name,
    ROUND((1.0 - exploratory_breadth) * closure_pressure, 4) AS premature_convergence_risk
FROM ideation_contexts;

CREATE VIEW unbounded_divergence_risks AS
SELECT
    context_id,
    context_name,
    ROUND(exploratory_breadth * (1.0 - evaluative_discipline), 4) AS unbounded_divergence_risk
FROM ideation_contexts;

CREATE VIEW idea_portfolio_scores AS
SELECT
    idea_id,
    context_id,
    idea_name,
    ROUND(
      0.12 * novelty +
      0.18 * strategic_fit +
      0.14 * evidence_strength +
      0.12 * feasibility +
      0.14 * stakeholder_value +
      0.10 * risk_visibility +
      0.12 * ethical_legitimacy +
      0.10 * implementation_readiness -
      0.08 * assumption_burden,
      4
    ) AS idea_score
FROM idea_portfolio;

CREATE VIEW criteria_quality_scores AS
SELECT
    criteria_id,
    context_id,
    criterion_name,
    ROUND(
      0.24 * definition_clarity +
      0.18 * weight_justification +
      0.20 * measurement_validity -
      0.18 * bias_risk +
      0.16 * stakeholder_relevance +
      0.12 * strategic_importance,
      4
    ) AS criteria_quality_score
FROM evaluation_criteria;

CREATE VIEW selection_integrity_scores AS
SELECT
    round_id,
    context_id,
    round_name,
    mode,
    ROUND(
      0.16 * mode_clarity +
      0.14 * participation_quality +
      0.18 * criteria_transparency +
      0.18 * evidence_use +
      0.14 * stakeholder_voice +
      0.10 * decision_documentation +
      0.10 * iteration_trigger_quality,
      4
    ) AS selection_integrity_score
FROM evaluation_rounds;

CREATE VIEW stakeholder_inclusion_scores AS
SELECT
    review_id,
    context_id,
    stakeholder_group,
    ROUND(
      0.18 * inclusion_level +
      0.18 * influence_on_criteria +
      0.18 * influence_on_selection +
      0.14 * burden_visibility +
      0.14 * knowledge_recognition +
      0.10 * legitimacy_signal +
      0.08 * review_quality,
      4
    ) AS stakeholder_inclusion_score
FROM stakeholder_review;

CREATE VIEW iteration_learning_scores AS
SELECT
    cycle_id,
    context_id,
    cycle_name,
    ROUND(
      0.14 * divergence_quality +
      0.14 * convergence_quality +
      0.16 * evidence_learning +
      0.14 * frame_revision +
      0.12 * assumption_revision +
      0.12 * decision_memory +
      0.10 * implementation_feedback +
      0.08 * next_cycle_readiness,
      4
    ) AS iteration_learning_score
FROM learning_cycles;
