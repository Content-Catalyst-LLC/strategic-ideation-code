-- Advanced SQL schema for creative constraints and innovation.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS constraint_context_profiles;
DROP VIEW IF EXISTS rigidity_and_diffusion_risks;
DROP VIEW IF EXISTS constraint_classification_scores;
DROP VIEW IF EXISTS constraint_function_scores;
DROP VIEW IF EXISTS innovation_option_scores;
DROP VIEW IF EXISTS stakeholder_constraint_scores;
DROP VIEW IF EXISTS dynamic_constraint_priorities;
DROP VIEW IF EXISTS capability_learning_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS capability_learning;
DROP TABLE IF EXISTS dynamic_constraints;
DROP TABLE IF EXISTS stakeholder_constraint_review;
DROP TABLE IF EXISTS innovation_options;
DROP TABLE IF EXISTS constraint_function_map;
DROP TABLE IF EXISTS constraint_register;
DROP TABLE IF EXISTS constraint_contexts;

CREATE TABLE constraint_contexts (
    context_id TEXT PRIMARY KEY,
    context_name TEXT NOT NULL,
    context_type TEXT NOT NULL,
    resource_pressure REAL CHECK (resource_pressure BETWEEN 0 AND 1),
    technical_rigidity REAL CHECK (technical_rigidity BETWEEN 0 AND 1),
    institutional_rigidity REAL CHECK (institutional_rigidity BETWEEN 0 AND 1),
    ecological_boundary_pressure REAL CHECK (ecological_boundary_pressure BETWEEN 0 AND 1),
    ethical_constraint_visibility REAL CHECK (ethical_constraint_visibility BETWEEN 0 AND 1),
    search_focus REAL CHECK (search_focus BETWEEN 0 AND 1),
    adaptive_opportunity REAL CHECK (adaptive_opportunity BETWEEN 0 AND 1),
    stakeholder_legitimacy REAL CHECK (stakeholder_legitimacy BETWEEN 0 AND 1),
    learning_capacity REAL CHECK (learning_capacity BETWEEN 0 AND 1),
    implementation_readiness REAL CHECK (implementation_readiness BETWEEN 0 AND 1)
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
    burden_visibility REAL CHECK (burden_visibility BETWEEN 0 AND 1),
    notes TEXT,
    FOREIGN KEY (context_id) REFERENCES constraint_contexts(context_id)
);

CREATE TABLE constraint_function_map (
    function_id TEXT PRIMARY KEY,
    constraint_id TEXT NOT NULL,
    context_id TEXT NOT NULL,
    focus_value REAL CHECK (focus_value BETWEEN 0 AND 1),
    tradeoff_visibility REAL CHECK (tradeoff_visibility BETWEEN 0 AND 1),
    recombination_pressure REAL CHECK (recombination_pressure BETWEEN 0 AND 1),
    legitimacy_protection REAL CHECK (legitimacy_protection BETWEEN 0 AND 1),
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    suppression_risk REAL CHECK (suppression_risk BETWEEN 0 AND 1),
    capability_requirement REAL CHECK (capability_requirement BETWEEN 0 AND 1),
    FOREIGN KEY (constraint_id) REFERENCES constraint_register(constraint_id),
    FOREIGN KEY (context_id) REFERENCES constraint_contexts(context_id)
);

CREATE TABLE innovation_options (
    option_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    option_name TEXT NOT NULL,
    novelty REAL CHECK (novelty BETWEEN 0 AND 1),
    strategic_fit REAL CHECK (strategic_fit BETWEEN 0 AND 1),
    constraint_fit REAL CHECK (constraint_fit BETWEEN 0 AND 1),
    adaptive_value REAL CHECK (adaptive_value BETWEEN 0 AND 1),
    stakeholder_value REAL CHECK (stakeholder_value BETWEEN 0 AND 1),
    ecological_responsibility REAL CHECK (ecological_responsibility BETWEEN 0 AND 1),
    ethical_legitimacy REAL CHECK (ethical_legitimacy BETWEEN 0 AND 1),
    implementation_readiness REAL CHECK (implementation_readiness BETWEEN 0 AND 1),
    assumption_burden REAL CHECK (assumption_burden BETWEEN 0 AND 1),
    FOREIGN KEY (context_id) REFERENCES constraint_contexts(context_id)
);

CREATE TABLE stakeholder_constraint_review (
    review_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    stakeholder_group TEXT NOT NULL,
    inclusion_level REAL CHECK (inclusion_level BETWEEN 0 AND 1),
    influence_on_constraint_definition REAL CHECK (influence_on_constraint_definition BETWEEN 0 AND 1),
    burden_visibility REAL CHECK (burden_visibility BETWEEN 0 AND 1),
    knowledge_recognition REAL CHECK (knowledge_recognition BETWEEN 0 AND 1),
    trust_signal REAL CHECK (trust_signal BETWEEN 0 AND 1),
    legitimacy_signal REAL CHECK (legitimacy_signal BETWEEN 0 AND 1),
    review_quality REAL CHECK (review_quality BETWEEN 0 AND 1),
    FOREIGN KEY (context_id) REFERENCES constraint_contexts(context_id)
);

CREATE TABLE dynamic_constraints (
    dynamic_id TEXT PRIMARY KEY,
    constraint_id TEXT NOT NULL,
    context_id TEXT NOT NULL,
    change_direction TEXT NOT NULL,
    change_likelihood REAL CHECK (change_likelihood BETWEEN 0 AND 1),
    strategic_exposure REAL CHECK (strategic_exposure BETWEEN 0 AND 1),
    detection_confidence REAL CHECK (detection_confidence BETWEEN 0 AND 1),
    adaptation_readiness REAL CHECK (adaptation_readiness BETWEEN 0 AND 1),
    recommended_response TEXT,
    FOREIGN KEY (constraint_id) REFERENCES constraint_register(constraint_id),
    FOREIGN KEY (context_id) REFERENCES constraint_contexts(context_id)
);

CREATE TABLE capability_learning (
    capability_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    capability_name TEXT NOT NULL,
    interpretive_flexibility REAL CHECK (interpretive_flexibility BETWEEN 0 AND 1),
    technical_capacity REAL CHECK (technical_capacity BETWEEN 0 AND 1),
    process_discipline REAL CHECK (process_discipline BETWEEN 0 AND 1),
    decision_memory REAL CHECK (decision_memory BETWEEN 0 AND 1),
    stakeholder_learning REAL CHECK (stakeholder_learning BETWEEN 0 AND 1),
    prototype_capacity REAL CHECK (prototype_capacity BETWEEN 0 AND 1),
    revision_capacity REAL CHECK (revision_capacity BETWEEN 0 AND 1),
    burnout_risk REAL CHECK (burnout_risk BETWEEN 0 AND 1),
    FOREIGN KEY (context_id) REFERENCES constraint_contexts(context_id)
);

CREATE TABLE decision_memory (
    decision_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    constraint_id TEXT,
    option_id TEXT,
    decision_date TEXT,
    constraint_classification TEXT,
    boundary_respected TEXT,
    boundary_challenged TEXT,
    evidence_considered TEXT,
    stakeholder_burden_review TEXT,
    revision_trigger TEXT,
    FOREIGN KEY (context_id) REFERENCES constraint_contexts(context_id),
    FOREIGN KEY (constraint_id) REFERENCES constraint_register(constraint_id),
    FOREIGN KEY (option_id) REFERENCES innovation_options(option_id)
);

CREATE VIEW constraint_context_profiles AS
SELECT
    context_id,
    context_name,
    context_type,
    ROUND(
      -0.10 * resource_pressure -
      0.10 * technical_rigidity -
      0.10 * institutional_rigidity +
      0.12 * ecological_boundary_pressure +
      0.16 * ethical_constraint_visibility +
      0.16 * search_focus +
      0.16 * adaptive_opportunity +
      0.14 * stakeholder_legitimacy +
      0.14 * learning_capacity +
      0.12 * implementation_readiness,
      4
    ) AS productive_constraint_profile
FROM constraint_contexts;

CREATE VIEW rigidity_and_diffusion_risks AS
SELECT
    context_id,
    context_name,
    ROUND(
      (0.24 * resource_pressure + 0.25 * technical_rigidity + 0.27 * institutional_rigidity + 0.24 * ecological_boundary_pressure) *
      (1.0 - learning_capacity),
      4
    ) AS rigidity_risk,
    ROUND((1.0 - search_focus) * adaptive_opportunity, 4) AS diffusion_risk,
    ROUND(MAX(0.0, 0.65 - stakeholder_legitimacy), 4) AS legitimacy_gap
FROM constraint_contexts;

CREATE VIEW constraint_classification_scores AS
SELECT
    constraint_id,
    context_id,
    constraint_name,
    constraint_type,
    is_real_constraint,
    ROUND(
      CASE
        WHEN is_real_constraint = 1 THEN certainty * strategic_importance * (1.0 - 0.35 * redesign_potential)
        ELSE strategic_importance * redesign_potential * (1.0 - evidence_quality + 0.25)
      END,
      4
    ) AS constraint_priority
FROM constraint_register;

CREATE VIEW constraint_function_scores AS
SELECT
    function_id,
    constraint_id,
    context_id,
    ROUND(
      0.18 * focus_value +
      0.16 * tradeoff_visibility +
      0.18 * recombination_pressure +
      0.16 * legitimacy_protection +
      0.16 * learning_value +
      0.10 * capability_requirement -
      0.16 * suppression_risk,
      4
    ) AS generative_constraint_value
FROM constraint_function_map;

CREATE VIEW innovation_option_scores AS
SELECT
    option_id,
    context_id,
    option_name,
    ROUND(
      0.12 * novelty +
      0.16 * strategic_fit +
      0.14 * constraint_fit +
      0.14 * adaptive_value +
      0.12 * stakeholder_value +
      0.12 * ecological_responsibility +
      0.12 * ethical_legitimacy +
      0.10 * implementation_readiness -
      0.08 * assumption_burden,
      4
    ) AS innovation_option_score
FROM innovation_options;

CREATE VIEW stakeholder_constraint_scores AS
SELECT
    review_id,
    context_id,
    stakeholder_group,
    ROUND(
      0.16 * inclusion_level +
      0.18 * influence_on_constraint_definition +
      0.16 * burden_visibility +
      0.16 * knowledge_recognition +
      0.12 * trust_signal +
      0.14 * legitimacy_signal +
      0.08 * review_quality,
      4
    ) AS stakeholder_constraint_score
FROM stakeholder_constraint_review;

CREATE VIEW dynamic_constraint_priorities AS
SELECT
    dynamic_id,
    constraint_id,
    context_id,
    change_direction,
    ROUND(
      0.26 * change_likelihood +
      0.30 * strategic_exposure +
      0.18 * detection_confidence +
      0.18 * (1.0 - adaptation_readiness),
      4
    ) AS dynamic_priority,
    recommended_response
FROM dynamic_constraints;

CREATE VIEW capability_learning_scores AS
SELECT
    capability_id,
    context_id,
    capability_name,
    ROUND(
      0.16 * interpretive_flexibility +
      0.14 * technical_capacity +
      0.16 * process_discipline +
      0.14 * decision_memory +
      0.14 * stakeholder_learning +
      0.12 * prototype_capacity +
      0.14 * revision_capacity -
      0.10 * burnout_risk,
      4
    ) AS constraint_learning_score
FROM capability_learning;
