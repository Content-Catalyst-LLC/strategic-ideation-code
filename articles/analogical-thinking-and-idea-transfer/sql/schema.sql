-- Advanced SQL schema for analogical thinking and idea transfer.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS analogical_strategy_profiles;
DROP VIEW IF EXISTS surface_distraction_risks;
DROP VIEW IF EXISTS source_domain_quality_scores;
DROP VIEW IF EXISTS source_target_mapping_scores;
DROP VIEW IF EXISTS adaptation_readiness_scores;
DROP VIEW IF EXISTS rival_analogy_scores;
DROP VIEW IF EXISTS stakeholder_legitimacy_scores;
DROP VIEW IF EXISTS transfer_hypothesis_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS transfer_hypotheses;
DROP TABLE IF EXISTS stakeholder_legitimacy;
DROP TABLE IF EXISTS rival_analogies;
DROP TABLE IF EXISTS adaptation_tests;
DROP TABLE IF EXISTS source_target_mappings;
DROP TABLE IF EXISTS target_problems;
DROP TABLE IF EXISTS source_domains;
DROP TABLE IF EXISTS analogical_strategies;

CREATE TABLE analogical_strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy_name TEXT NOT NULL,
    strategy_type TEXT NOT NULL,
    source_distance REAL CHECK (source_distance BETWEEN 0 AND 1),
    structural_fit REAL CHECK (structural_fit BETWEEN 0 AND 1),
    functional_fit REAL CHECK (functional_fit BETWEEN 0 AND 1),
    surface_distraction REAL CHECK (surface_distraction BETWEEN 0 AND 1),
    adaptation_quality REAL CHECK (adaptation_quality BETWEEN 0 AND 1),
    context_sensitivity REAL CHECK (context_sensitivity BETWEEN 0 AND 1),
    stakeholder_legitimacy REAL CHECK (stakeholder_legitimacy BETWEEN 0 AND 1),
    dynamic_compatibility REAL CHECK (dynamic_compatibility BETWEEN 0 AND 1),
    innovation_potential REAL CHECK (innovation_potential BETWEEN 0 AND 1),
    evidence_strength REAL CHECK (evidence_strength BETWEEN 0 AND 1)
);

CREATE TABLE source_domains (
    source_id TEXT PRIMARY KEY,
    source_name TEXT NOT NULL,
    source_domain_type TEXT NOT NULL,
    source_distance REAL CHECK (source_distance BETWEEN 0 AND 1),
    relational_clarity REAL CHECK (relational_clarity BETWEEN 0 AND 1),
    mechanism_visibility REAL CHECK (mechanism_visibility BETWEEN 0 AND 1),
    constraint_visibility REAL CHECK (constraint_visibility BETWEEN 0 AND 1),
    failure_mode_visibility REAL CHECK (failure_mode_visibility BETWEEN 0 AND 1),
    prestige_pressure REAL CHECK (prestige_pressure BETWEEN 0 AND 1),
    transfer_complexity REAL CHECK (transfer_complexity BETWEEN 0 AND 1)
);

CREATE TABLE target_problems (
    target_id TEXT PRIMARY KEY,
    target_name TEXT NOT NULL,
    target_domain TEXT NOT NULL,
    problem_clarity REAL CHECK (problem_clarity BETWEEN 0 AND 1),
    stakeholder_complexity REAL CHECK (stakeholder_complexity BETWEEN 0 AND 1),
    implementation_complexity REAL CHECK (implementation_complexity BETWEEN 0 AND 1),
    uncertainty_level REAL CHECK (uncertainty_level BETWEEN 0 AND 1),
    ethical_sensitivity REAL CHECK (ethical_sensitivity BETWEEN 0 AND 1),
    system_dynamism REAL CHECK (system_dynamism BETWEEN 0 AND 1),
    evidence_availability REAL CHECK (evidence_availability BETWEEN 0 AND 1)
);

CREATE TABLE source_target_mappings (
    mapping_id TEXT PRIMARY KEY,
    strategy_id TEXT NOT NULL,
    source_id TEXT NOT NULL,
    target_id TEXT NOT NULL,
    actor_correspondence REAL CHECK (actor_correspondence BETWEEN 0 AND 1),
    relation_correspondence REAL CHECK (relation_correspondence BETWEEN 0 AND 1),
    flow_correspondence REAL CHECK (flow_correspondence BETWEEN 0 AND 1),
    constraint_correspondence REAL CHECK (constraint_correspondence BETWEEN 0 AND 1),
    feedback_correspondence REAL CHECK (feedback_correspondence BETWEEN 0 AND 1),
    failure_mode_correspondence REAL CHECK (failure_mode_correspondence BETWEEN 0 AND 1),
    breakpoint_visibility REAL CHECK (breakpoint_visibility BETWEEN 0 AND 1),
    mapping_confidence REAL CHECK (mapping_confidence BETWEEN 0 AND 1),
    FOREIGN KEY (strategy_id) REFERENCES analogical_strategies(strategy_id),
    FOREIGN KEY (source_id) REFERENCES source_domains(source_id),
    FOREIGN KEY (target_id) REFERENCES target_problems(target_id)
);

CREATE TABLE adaptation_tests (
    adaptation_id TEXT PRIMARY KEY,
    mapping_id TEXT NOT NULL,
    strategy_id TEXT NOT NULL,
    target_id TEXT NOT NULL,
    constraint_fit REAL CHECK (constraint_fit BETWEEN 0 AND 1),
    stakeholder_fit REAL CHECK (stakeholder_fit BETWEEN 0 AND 1),
    mechanism_fit REAL CHECK (mechanism_fit BETWEEN 0 AND 1),
    governance_fit REAL CHECK (governance_fit BETWEEN 0 AND 1),
    implementation_fit REAL CHECK (implementation_fit BETWEEN 0 AND 1),
    evidence_fit REAL CHECK (evidence_fit BETWEEN 0 AND 1),
    ethical_fit REAL CHECK (ethical_fit BETWEEN 0 AND 1),
    adaptation_readiness REAL CHECK (adaptation_readiness BETWEEN 0 AND 1),
    FOREIGN KEY (mapping_id) REFERENCES source_target_mappings(mapping_id),
    FOREIGN KEY (strategy_id) REFERENCES analogical_strategies(strategy_id),
    FOREIGN KEY (target_id) REFERENCES target_problems(target_id)
);

CREATE TABLE rival_analogies (
    rival_id TEXT PRIMARY KEY,
    target_id TEXT NOT NULL,
    analogy_set TEXT NOT NULL,
    analogy_name TEXT NOT NULL,
    structural_fit REAL CHECK (structural_fit BETWEEN 0 AND 1),
    explanatory_power REAL CHECK (explanatory_power BETWEEN 0 AND 1),
    blind_spot_risk REAL CHECK (blind_spot_risk BETWEEN 0 AND 1),
    ethical_risk REAL CHECK (ethical_risk BETWEEN 0 AND 1),
    implementation_relevance REAL CHECK (implementation_relevance BETWEEN 0 AND 1),
    novelty_value REAL CHECK (novelty_value BETWEEN 0 AND 1),
    FOREIGN KEY (target_id) REFERENCES target_problems(target_id)
);

CREATE TABLE stakeholder_legitimacy (
    review_id TEXT PRIMARY KEY,
    strategy_id TEXT NOT NULL,
    target_id TEXT NOT NULL,
    stakeholder_group TEXT NOT NULL,
    inclusion_level REAL CHECK (inclusion_level BETWEEN 0 AND 1),
    burden_visibility REAL CHECK (burden_visibility BETWEEN 0 AND 1),
    knowledge_recognition REAL CHECK (knowledge_recognition BETWEEN 0 AND 1),
    interpretive_trust REAL CHECK (interpretive_trust BETWEEN 0 AND 1),
    legitimacy_signal REAL CHECK (legitimacy_signal BETWEEN 0 AND 1),
    power_blindness_risk REAL CHECK (power_blindness_risk BETWEEN 0 AND 1),
    review_quality REAL CHECK (review_quality BETWEEN 0 AND 1),
    FOREIGN KEY (strategy_id) REFERENCES analogical_strategies(strategy_id),
    FOREIGN KEY (target_id) REFERENCES target_problems(target_id)
);

CREATE TABLE transfer_hypotheses (
    hypothesis_id TEXT PRIMARY KEY,
    mapping_id TEXT NOT NULL,
    strategy_id TEXT NOT NULL,
    hypothesis_statement TEXT NOT NULL,
    hypothesis_clarity REAL CHECK (hypothesis_clarity BETWEEN 0 AND 1),
    evidence_strength REAL CHECK (evidence_strength BETWEEN 0 AND 1),
    testability REAL CHECK (testability BETWEEN 0 AND 1),
    implementation_risk REAL CHECK (implementation_risk BETWEEN 0 AND 1),
    unintended_consequence_risk REAL CHECK (unintended_consequence_risk BETWEEN 0 AND 1),
    revision_trigger_quality REAL CHECK (revision_trigger_quality BETWEEN 0 AND 1),
    recommended_next_step TEXT,
    FOREIGN KEY (mapping_id) REFERENCES source_target_mappings(mapping_id),
    FOREIGN KEY (strategy_id) REFERENCES analogical_strategies(strategy_id)
);

CREATE TABLE decision_memory (
    decision_id TEXT PRIMARY KEY,
    strategy_id TEXT NOT NULL,
    mapping_id TEXT,
    hypothesis_id TEXT,
    decision_date TEXT,
    source_domain_used TEXT,
    target_problem TEXT,
    structural_mapping_summary TEXT,
    breakpoints TEXT,
    adaptation_decision TEXT,
    stakeholder_review_summary TEXT,
    evidence_considered TEXT,
    revision_trigger TEXT,
    FOREIGN KEY (strategy_id) REFERENCES analogical_strategies(strategy_id),
    FOREIGN KEY (mapping_id) REFERENCES source_target_mappings(mapping_id),
    FOREIGN KEY (hypothesis_id) REFERENCES transfer_hypotheses(hypothesis_id)
);

CREATE VIEW analogical_strategy_profiles AS
SELECT
    strategy_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.20 * structural_fit +
      0.16 * functional_fit -
      0.16 * surface_distraction +
      0.16 * adaptation_quality +
      0.12 * context_sensitivity +
      0.08 * stakeholder_legitimacy +
      0.08 * dynamic_compatibility +
      0.12 * innovation_potential +
      0.08 * evidence_strength,
      4
    ) AS analogy_profile_score
FROM analogical_strategies;

CREATE VIEW surface_distraction_risks AS
SELECT
    strategy_id,
    strategy_name,
    ROUND(surface_distraction * (1.0 - structural_fit), 4) AS surface_distraction_risk
FROM analogical_strategies;

CREATE VIEW source_domain_quality_scores AS
SELECT
    source_id,
    source_name,
    source_domain_type,
    ROUND(
      0.22 * relational_clarity +
      0.20 * mechanism_visibility +
      0.18 * constraint_visibility +
      0.16 * failure_mode_visibility -
      0.12 * prestige_pressure -
      0.06 * transfer_complexity +
      0.12 * source_distance,
      4
    ) AS source_quality_score
FROM source_domains;

CREATE VIEW source_target_mapping_scores AS
SELECT
    mapping_id,
    strategy_id,
    source_id,
    target_id,
    ROUND(
      0.14 * actor_correspondence +
      0.20 * relation_correspondence +
      0.14 * flow_correspondence +
      0.14 * constraint_correspondence +
      0.14 * feedback_correspondence +
      0.12 * failure_mode_correspondence +
      0.08 * breakpoint_visibility +
      0.04 * mapping_confidence,
      4
    ) AS mapping_score
FROM source_target_mappings;

CREATE VIEW adaptation_readiness_scores AS
SELECT
    adaptation_id,
    mapping_id,
    strategy_id,
    target_id,
    ROUND(
      0.14 * constraint_fit +
      0.14 * stakeholder_fit +
      0.18 * mechanism_fit +
      0.14 * governance_fit +
      0.12 * implementation_fit +
      0.12 * evidence_fit +
      0.12 * ethical_fit +
      0.04 * adaptation_readiness,
      4
    ) AS adaptation_score
FROM adaptation_tests;

CREATE VIEW rival_analogy_scores AS
SELECT
    rival_id,
    target_id,
    analogy_set,
    analogy_name,
    ROUND(
      0.24 * structural_fit +
      0.20 * explanatory_power -
      0.16 * blind_spot_risk -
      0.12 * ethical_risk +
      0.14 * implementation_relevance +
      0.10 * novelty_value,
      4
    ) AS rival_analogy_score
FROM rival_analogies;

CREATE VIEW stakeholder_legitimacy_scores AS
SELECT
    review_id,
    strategy_id,
    target_id,
    stakeholder_group,
    ROUND(
      0.15 * inclusion_level +
      0.16 * burden_visibility +
      0.16 * knowledge_recognition +
      0.14 * interpretive_trust +
      0.16 * legitimacy_signal -
      0.15 * power_blindness_risk +
      0.08 * review_quality,
      4
    ) AS stakeholder_legitimacy_score
FROM stakeholder_legitimacy;

CREATE VIEW transfer_hypothesis_scores AS
SELECT
    hypothesis_id,
    mapping_id,
    strategy_id,
    hypothesis_statement,
    ROUND(
      0.18 * hypothesis_clarity +
      0.18 * evidence_strength +
      0.18 * testability -
      0.14 * implementation_risk -
      0.14 * unintended_consequence_risk +
      0.16 * revision_trigger_quality,
      4
    ) AS transfer_hypothesis_score,
    recommended_next_step
FROM transfer_hypotheses;
