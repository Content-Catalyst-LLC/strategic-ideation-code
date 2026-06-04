-- Advanced SQL schema for heuristics in strategic ideation.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS heuristic_context_profiles;
DROP VIEW IF EXISTS premature_closure_risks;
DROP VIEW IF EXISTS heuristic_use_scores;
DROP VIEW IF EXISTS search_breadth_scores;
DROP VIEW IF EXISTS institutional_shortcut_risks;
DROP VIEW IF EXISTS complexity_fit_scores;
DROP VIEW IF EXISTS stopping_rule_scores;
DROP VIEW IF EXISTS intervention_value_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS intervention_library;
DROP TABLE IF EXISTS stopping_rules;
DROP TABLE IF EXISTS complexity_fit;
DROP TABLE IF EXISTS institutional_shortcuts;
DROP TABLE IF EXISTS idea_search_inventory;
DROP TABLE IF EXISTS heuristic_use_cases;
DROP TABLE IF EXISTS heuristic_contexts;

CREATE TABLE heuristic_contexts (
    context_id TEXT PRIMARY KEY,
    context_name TEXT NOT NULL,
    context_type TEXT NOT NULL,
    availability_dependence REAL CHECK (availability_dependence BETWEEN 0 AND 1),
    anchoring_intensity REAL CHECK (anchoring_intensity BETWEEN 0 AND 1),
    recognition_comfort REAL CHECK (recognition_comfort BETWEEN 0 AND 1),
    satisficing_tendency REAL CHECK (satisficing_tendency BETWEEN 0 AND 1),
    affect_pressure REAL CHECK (affect_pressure BETWEEN 0 AND 1),
    default_gravity REAL CHECK (default_gravity BETWEEN 0 AND 1),
    social_proof_pressure REAL CHECK (social_proof_pressure BETWEEN 0 AND 1),
    exploratory_diversity REAL CHECK (exploratory_diversity BETWEEN 0 AND 1),
    stakeholder_variation REAL CHECK (stakeholder_variation BETWEEN 0 AND 1),
    source_domain_diversity REAL CHECK (source_domain_diversity BETWEEN 0 AND 1),
    systems_check_quality REAL CHECK (systems_check_quality BETWEEN 0 AND 1),
    political_safety REAL CHECK (political_safety BETWEEN 0 AND 1),
    decision_memory_quality REAL CHECK (decision_memory_quality BETWEEN 0 AND 1)
);

CREATE TABLE heuristic_use_cases (
    heuristic_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    heuristic_name TEXT NOT NULL,
    heuristic_family TEXT NOT NULL,
    use_phase TEXT NOT NULL,
    search_speed_gain REAL CHECK (search_speed_gain BETWEEN 0 AND 1),
    search_depth_loss REAL CHECK (search_depth_loss BETWEEN 0 AND 1),
    strategic_relevance REAL CHECK (strategic_relevance BETWEEN 0 AND 1),
    fit_to_context REAL CHECK (fit_to_context BETWEEN 0 AND 1),
    misuse_risk REAL CHECK (misuse_risk BETWEEN 0 AND 1),
    stakeholder_visibility REAL CHECK (stakeholder_visibility BETWEEN 0 AND 1),
    systems_fit REAL CHECK (systems_fit BETWEEN 0 AND 1),
    evidence_pathway REAL CHECK (evidence_pathway BETWEEN 0 AND 1),
    FOREIGN KEY (context_id) REFERENCES heuristic_contexts(context_id)
);

CREATE TABLE idea_search_inventory (
    idea_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    idea_name TEXT NOT NULL,
    dominant_heuristic TEXT NOT NULL,
    frame_family TEXT NOT NULL,
    source_domain TEXT NOT NULL,
    stakeholder_visibility REAL CHECK (stakeholder_visibility BETWEEN 0 AND 1),
    novelty_level REAL CHECK (novelty_level BETWEEN 0 AND 1),
    evidence_pathway REAL CHECK (evidence_pathway BETWEEN 0 AND 1),
    strategic_relevance REAL CHECK (strategic_relevance BETWEEN 0 AND 1),
    implementation_pathway REAL CHECK (implementation_pathway BETWEEN 0 AND 1),
    system_level TEXT NOT NULL,
    search_breadth REAL CHECK (search_breadth BETWEEN 0 AND 1),
    closure_pressure REAL CHECK (closure_pressure BETWEEN 0 AND 1),
    assumption_burden REAL CHECK (assumption_burden BETWEEN 0 AND 1),
    FOREIGN KEY (context_id) REFERENCES heuristic_contexts(context_id)
);

CREATE TABLE institutional_shortcuts (
    shortcut_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    shortcut_name TEXT NOT NULL,
    shortcut_type TEXT NOT NULL,
    coordination_benefit REAL CHECK (coordination_benefit BETWEEN 0 AND 1),
    search_narrowing_risk REAL CHECK (search_narrowing_risk BETWEEN 0 AND 1),
    metric_lock_in REAL CHECK (metric_lock_in BETWEEN 0 AND 1),
    template_dependency REAL CHECK (template_dependency BETWEEN 0 AND 1),
    leadership_preference_pressure REAL CHECK (leadership_preference_pressure BETWEEN 0 AND 1),
    stakeholder_exclusion REAL CHECK (stakeholder_exclusion BETWEEN 0 AND 1),
    revision_difficulty REAL CHECK (revision_difficulty BETWEEN 0 AND 1),
    strategic_obsolescence_risk REAL CHECK (strategic_obsolescence_risk BETWEEN 0 AND 1),
    FOREIGN KEY (context_id) REFERENCES heuristic_contexts(context_id)
);

CREATE TABLE complexity_fit (
    fit_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    heuristic_name TEXT NOT NULL,
    assumed_environment TEXT NOT NULL,
    actual_environment TEXT NOT NULL,
    feedback_awareness REAL CHECK (feedback_awareness BETWEEN 0 AND 1),
    delay_awareness REAL CHECK (delay_awareness BETWEEN 0 AND 1),
    second_order_review REAL CHECK (second_order_review BETWEEN 0 AND 1),
    adaptation_review REAL CHECK (adaptation_review BETWEEN 0 AND 1),
    boundary_quality REAL CHECK (boundary_quality BETWEEN 0 AND 1),
    robustness_across_scenarios REAL CHECK (robustness_across_scenarios BETWEEN 0 AND 1),
    complexity_mismatch_risk REAL CHECK (complexity_mismatch_risk BETWEEN 0 AND 1),
    FOREIGN KEY (context_id) REFERENCES heuristic_contexts(context_id)
);

CREATE TABLE stopping_rules (
    rule_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    rule_name TEXT NOT NULL,
    closure_trigger TEXT NOT NULL,
    option_diversity_requirement REAL CHECK (option_diversity_requirement BETWEEN 0 AND 1),
    stakeholder_coverage_requirement REAL CHECK (stakeholder_coverage_requirement BETWEEN 0 AND 1),
    source_domain_requirement REAL CHECK (source_domain_requirement BETWEEN 0 AND 1),
    systems_review_requirement REAL CHECK (systems_review_requirement BETWEEN 0 AND 1),
    evidence_threshold REAL CHECK (evidence_threshold BETWEEN 0 AND 1),
    political_pressure REAL CHECK (political_pressure BETWEEN 0 AND 1),
    closure_quality REAL CHECK (closure_quality BETWEEN 0 AND 1),
    reopen_trigger_quality REAL CHECK (reopen_trigger_quality BETWEEN 0 AND 1),
    FOREIGN KEY (context_id) REFERENCES heuristic_contexts(context_id)
);

CREATE TABLE intervention_library (
    intervention_id TEXT PRIMARY KEY,
    intervention_name TEXT NOT NULL,
    target_heuristic_risk TEXT NOT NULL,
    process_cost REAL CHECK (process_cost BETWEEN 0 AND 1),
    implementation_complexity REAL CHECK (implementation_complexity BETWEEN 0 AND 1),
    search_breadth_gain REAL CHECK (search_breadth_gain BETWEEN 0 AND 1),
    stakeholder_gain REAL CHECK (stakeholder_gain BETWEEN 0 AND 1),
    systems_fit_gain REAL CHECK (systems_fit_gain BETWEEN 0 AND 1),
    closure_quality_gain REAL CHECK (closure_quality_gain BETWEEN 0 AND 1),
    decision_memory_gain REAL CHECK (decision_memory_gain BETWEEN 0 AND 1),
    political_safety_need REAL CHECK (political_safety_need BETWEEN 0 AND 1)
);

CREATE TABLE decision_memory (
    decision_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    idea_id TEXT,
    heuristic_id TEXT,
    shortcut_id TEXT,
    rule_id TEXT,
    decision_date TEXT,
    search_logic_summary TEXT,
    heuristics_used TEXT,
    risks_identified TEXT,
    alternatives_excluded TEXT,
    stopping_rule_used TEXT,
    decision_outcome TEXT,
    rejected_or_deferred_reason TEXT,
    reopen_trigger TEXT,
    FOREIGN KEY (context_id) REFERENCES heuristic_contexts(context_id),
    FOREIGN KEY (idea_id) REFERENCES idea_search_inventory(idea_id),
    FOREIGN KEY (heuristic_id) REFERENCES heuristic_use_cases(heuristic_id),
    FOREIGN KEY (shortcut_id) REFERENCES institutional_shortcuts(shortcut_id),
    FOREIGN KEY (rule_id) REFERENCES stopping_rules(rule_id)
);

CREATE VIEW heuristic_context_profiles AS
SELECT
    context_id,
    context_name,
    context_type,
    ROUND(
      -0.11 * availability_dependence -
      0.11 * anchoring_intensity -
      0.10 * recognition_comfort -
      0.11 * satisficing_tendency -
      0.07 * affect_pressure -
      0.08 * default_gravity -
      0.06 * social_proof_pressure +
      0.17 * exploratory_diversity +
      0.13 * stakeholder_variation +
      0.13 * source_domain_diversity +
      0.14 * systems_check_quality +
      0.07 * political_safety +
      0.08 * decision_memory_quality,
      4
    ) AS heuristic_profile_score
FROM heuristic_contexts;

CREATE VIEW premature_closure_risks AS
SELECT
    context_id,
    context_name,
    ROUND(anchoring_intensity * satisficing_tendency, 4) AS closure_pressure,
    ROUND(recognition_comfort * (1.0 - exploratory_diversity), 4) AS recognition_trap_risk,
    ROUND(default_gravity * (1.0 - decision_memory_quality), 4) AS institutional_autopilot_risk,
    ROUND(social_proof_pressure * (1.0 - source_domain_diversity), 4) AS social_proof_risk
FROM heuristic_contexts;

CREATE VIEW heuristic_use_scores AS
SELECT
    heuristic_id,
    context_id,
    heuristic_name,
    heuristic_family,
    use_phase,
    ROUND(
      0.12 * search_speed_gain -
      0.12 * search_depth_loss +
      0.16 * strategic_relevance +
      0.16 * fit_to_context -
      0.14 * misuse_risk +
      0.12 * stakeholder_visibility +
      0.14 * systems_fit +
      0.14 * evidence_pathway,
      4
    ) AS heuristic_value_score
FROM heuristic_use_cases;

CREATE VIEW search_breadth_scores AS
SELECT
    idea_id,
    context_id,
    idea_name,
    dominant_heuristic,
    frame_family,
    source_domain,
    ROUND(
      0.12 * stakeholder_visibility +
      0.12 * novelty_level +
      0.12 * evidence_pathway +
      0.14 * strategic_relevance +
      0.10 * implementation_pathway +
      0.16 * search_breadth -
      0.12 * closure_pressure -
      0.08 * assumption_burden,
      4
    ) AS search_breadth_score
FROM idea_search_inventory;

CREATE VIEW institutional_shortcut_risks AS
SELECT
    shortcut_id,
    context_id,
    shortcut_name,
    shortcut_type,
    ROUND(
      0.16 * search_narrowing_risk +
      0.14 * metric_lock_in +
      0.14 * template_dependency +
      0.14 * leadership_preference_pressure +
      0.14 * stakeholder_exclusion +
      0.14 * revision_difficulty +
      0.14 * strategic_obsolescence_risk -
      0.08 * coordination_benefit,
      4
    ) AS institutional_shortcut_risk
FROM institutional_shortcuts;

CREATE VIEW complexity_fit_scores AS
SELECT
    fit_id,
    context_id,
    heuristic_name,
    assumed_environment,
    actual_environment,
    ROUND(
      0.16 * feedback_awareness +
      0.14 * delay_awareness +
      0.16 * second_order_review +
      0.14 * adaptation_review +
      0.14 * boundary_quality +
      0.16 * robustness_across_scenarios -
      0.10 * complexity_mismatch_risk,
      4
    ) AS complexity_fit_score
FROM complexity_fit;

CREATE VIEW stopping_rule_scores AS
SELECT
    rule_id,
    context_id,
    rule_name,
    closure_trigger,
    ROUND(
      0.14 * option_diversity_requirement +
      0.14 * stakeholder_coverage_requirement +
      0.14 * source_domain_requirement +
      0.16 * systems_review_requirement +
      0.14 * evidence_threshold -
      0.10 * political_pressure +
      0.14 * closure_quality +
      0.14 * reopen_trigger_quality,
      4
    ) AS stopping_rule_quality_score
FROM stopping_rules;

CREATE VIEW intervention_value_scores AS
SELECT
    intervention_id,
    intervention_name,
    target_heuristic_risk,
    ROUND(
      0.18 * search_breadth_gain +
      0.14 * stakeholder_gain +
      0.16 * systems_fit_gain +
      0.16 * closure_quality_gain +
      0.16 * decision_memory_gain -
      0.10 * process_cost -
      0.08 * implementation_complexity -
      0.08 * political_safety_need,
      4
    ) AS intervention_value_score
FROM intervention_library;
