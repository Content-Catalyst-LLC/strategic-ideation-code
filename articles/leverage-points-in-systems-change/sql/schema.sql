-- Advanced SQL schema for leverage points in systems change.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS leverage_point_scores;
DROP VIEW IF EXISTS feedback_leverage_scores;
DROP VIEW IF EXISTS information_flow_scores;
DROP VIEW IF EXISTS rule_incentive_scores;
DROP VIEW IF EXISTS system_goal_scores;
DROP VIEW IF EXISTS paradigm_scores;
DROP VIEW IF EXISTS tipping_threshold_scores;
DROP VIEW IF EXISTS governance_need_scores;
DROP VIEW IF EXISTS early_warning_indicator_scores;
DROP VIEW IF EXISTS learning_loop_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS learning_loops;
DROP TABLE IF EXISTS early_warning_indicators;
DROP TABLE IF EXISTS governance_needs;
DROP TABLE IF EXISTS tipping_thresholds;
DROP TABLE IF EXISTS paradigms;
DROP TABLE IF EXISTS system_goals;
DROP TABLE IF EXISTS rules_incentives;
DROP TABLE IF EXISTS information_flows;
DROP TABLE IF EXISTS feedback_leverage;
DROP TABLE IF EXISTS leverage_points;

CREATE TABLE leverage_points (
    leverage_id TEXT PRIMARY KEY,
    intervention_name TEXT NOT NULL,
    leverage_level TEXT NOT NULL,
    domain TEXT NOT NULL,
    implementation_ease REAL CHECK (implementation_ease BETWEEN 0 AND 1),
    structural_depth REAL CHECK (structural_depth BETWEEN 0 AND 1),
    system_sensitivity REAL CHECK (system_sensitivity BETWEEN 0 AND 1),
    feedback_influence REAL CHECK (feedback_influence BETWEEN 0 AND 1),
    information_effect REAL CHECK (information_effect BETWEEN 0 AND 1),
    rule_power REAL CHECK (rule_power BETWEEN 0 AND 1),
    goal_alignment REAL CHECK (goal_alignment BETWEEN 0 AND 1),
    paradigm_relevance REAL CHECK (paradigm_relevance BETWEEN 0 AND 1),
    transformative_potential REAL CHECK (transformative_potential BETWEEN 0 AND 1),
    legitimacy_requirement REAL CHECK (legitimacy_requirement BETWEEN 0 AND 1),
    unintended_consequence_risk REAL CHECK (unintended_consequence_risk BETWEEN 0 AND 1),
    learning_capacity REAL CHECK (learning_capacity BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE feedback_leverage (
    feedback_id TEXT PRIMARY KEY,
    leverage_id TEXT NOT NULL,
    loop_name TEXT NOT NULL,
    loop_type TEXT NOT NULL,
    loop_strength REAL CHECK (loop_strength BETWEEN 0 AND 1),
    current_visibility REAL CHECK (current_visibility BETWEEN 0 AND 1),
    reinforcing_potential REAL CHECK (reinforcing_potential BETWEEN 0 AND 1),
    balancing_capacity REAL CHECK (balancing_capacity BETWEEN 0 AND 1),
    delay_risk REAL CHECK (delay_risk BETWEEN 0 AND 1),
    intervention_readiness REAL CHECK (intervention_readiness BETWEEN 0 AND 1),
    positive_cascade_potential REAL CHECK (positive_cascade_potential BETWEEN 0 AND 1),
    policy_resistance_risk REAL CHECK (policy_resistance_risk BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (leverage_id) REFERENCES leverage_points(leverage_id)
);

CREATE TABLE information_flows (
    flow_id TEXT PRIMARY KEY,
    leverage_id TEXT NOT NULL,
    flow_name TEXT NOT NULL,
    flow_type TEXT NOT NULL,
    visibility_gain REAL CHECK (visibility_gain BETWEEN 0 AND 1),
    signal_quality REAL CHECK (signal_quality BETWEEN 0 AND 1),
    decision_linkage REAL CHECK (decision_linkage BETWEEN 0 AND 1),
    stakeholder_access REAL CHECK (stakeholder_access BETWEEN 0 AND 1),
    delay_reduction REAL CHECK (delay_reduction BETWEEN 0 AND 1),
    context_quality REAL CHECK (context_quality BETWEEN 0 AND 1),
    gaming_risk REAL CHECK (gaming_risk BETWEEN 0 AND 1),
    data_burden REAL CHECK (data_burden BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (leverage_id) REFERENCES leverage_points(leverage_id)
);

CREATE TABLE rules_incentives (
    rule_id TEXT PRIMARY KEY,
    leverage_id TEXT NOT NULL,
    rule_name TEXT NOT NULL,
    rule_type TEXT NOT NULL,
    current_misalignment REAL CHECK (current_misalignment BETWEEN 0 AND 1),
    behavioral_power REAL CHECK (behavioral_power BETWEEN 0 AND 1),
    incentive_clarity REAL CHECK (incentive_clarity BETWEEN 0 AND 1),
    cross_boundary_effect REAL CHECK (cross_boundary_effect BETWEEN 0 AND 1),
    implementation_complexity REAL CHECK (implementation_complexity BETWEEN 0 AND 1),
    political_resistance REAL CHECK (political_resistance BETWEEN 0 AND 1),
    governance_readiness REAL CHECK (governance_readiness BETWEEN 0 AND 1),
    countermetric_quality REAL CHECK (countermetric_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (leverage_id) REFERENCES leverage_points(leverage_id)
);

CREATE TABLE system_goals (
    goal_id TEXT PRIMARY KEY,
    leverage_id TEXT NOT NULL,
    stated_goal TEXT NOT NULL,
    operating_goal TEXT NOT NULL,
    goal_misalignment REAL CHECK (goal_misalignment BETWEEN 0 AND 1),
    metric_alignment REAL CHECK (metric_alignment BETWEEN 0 AND 1),
    budget_alignment REAL CHECK (budget_alignment BETWEEN 0 AND 1),
    decision_right_alignment REAL CHECK (decision_right_alignment BETWEEN 0 AND 1),
    tradeoff_clarity REAL CHECK (tradeoff_clarity BETWEEN 0 AND 1),
    stakeholder_legitimacy REAL CHECK (stakeholder_legitimacy BETWEEN 0 AND 1),
    long_term_orientation REAL CHECK (long_term_orientation BETWEEN 0 AND 1),
    revision_readiness REAL CHECK (revision_readiness BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (leverage_id) REFERENCES leverage_points(leverage_id)
);

CREATE TABLE paradigms (
    paradigm_id TEXT PRIMARY KEY,
    leverage_id TEXT NOT NULL,
    paradigm_name TEXT NOT NULL,
    current_assumption TEXT NOT NULL,
    alternative_frame TEXT NOT NULL,
    assumption_visibility REAL CHECK (assumption_visibility BETWEEN 0 AND 1),
    paradigm_lock_in REAL CHECK (paradigm_lock_in BETWEEN 0 AND 1),
    conceptual_clarity REAL CHECK (conceptual_clarity BETWEEN 0 AND 1),
    coalition_strength REAL CHECK (coalition_strength BETWEEN 0 AND 1),
    evidence_base REAL CHECK (evidence_base BETWEEN 0 AND 1),
    transition_pathway_quality REAL CHECK (transition_pathway_quality BETWEEN 0 AND 1),
    practice_embedding REAL CHECK (practice_embedding BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (leverage_id) REFERENCES leverage_points(leverage_id)
);

CREATE TABLE tipping_thresholds (
    threshold_id TEXT PRIMARY KEY,
    leverage_id TEXT NOT NULL,
    threshold_name TEXT NOT NULL,
    threshold_type TEXT NOT NULL,
    current_progress REAL CHECK (current_progress BETWEEN 0 AND 1),
    threshold_level REAL CHECK (threshold_level BETWEEN 0 AND 1),
    diffusion_potential REAL CHECK (diffusion_potential BETWEEN 0 AND 1),
    self_reinforcement_strength REAL CHECK (self_reinforcement_strength BETWEEN 0 AND 1),
    complementary_condition_quality REAL CHECK (complementary_condition_quality BETWEEN 0 AND 1),
    legitimacy_support REAL CHECK (legitimacy_support BETWEEN 0 AND 1),
    infrastructure_support REAL CHECK (infrastructure_support BETWEEN 0 AND 1),
    monitoring_quality REAL CHECK (monitoring_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (leverage_id) REFERENCES leverage_points(leverage_id)
);

CREATE TABLE governance_needs (
    governance_id TEXT PRIMARY KEY,
    leverage_id TEXT NOT NULL,
    governance_focus TEXT NOT NULL,
    legitimacy_requirement REAL CHECK (legitimacy_requirement BETWEEN 0 AND 1),
    unintended_consequence_risk REAL CHECK (unintended_consequence_risk BETWEEN 0 AND 1),
    implementation_complexity REAL CHECK (implementation_complexity BETWEEN 0 AND 1),
    monitoring_need REAL CHECK (monitoring_need BETWEEN 0 AND 1),
    stakeholder_inclusion_need REAL CHECK (stakeholder_inclusion_need BETWEEN 0 AND 1),
    decision_memory_need REAL CHECK (decision_memory_need BETWEEN 0 AND 1),
    revision_trigger_clarity REAL CHECK (revision_trigger_clarity BETWEEN 0 AND 1),
    current_governance_capacity REAL CHECK (current_governance_capacity BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (leverage_id) REFERENCES leverage_points(leverage_id)
);

CREATE TABLE early_warning_indicators (
    indicator_id TEXT PRIMARY KEY,
    leverage_id TEXT NOT NULL,
    indicator_name TEXT NOT NULL,
    signal_type TEXT NOT NULL,
    leading_quality REAL CHECK (leading_quality BETWEEN 0 AND 1),
    visibility REAL CHECK (visibility BETWEEN 0 AND 1),
    reliability REAL CHECK (reliability BETWEEN 0 AND 1),
    timeliness REAL CHECK (timeliness BETWEEN 0 AND 1),
    sensitivity REAL CHECK (sensitivity BETWEEN 0 AND 1),
    false_positive_risk REAL CHECK (false_positive_risk BETWEEN 0 AND 1),
    decision_linkage REAL CHECK (decision_linkage BETWEEN 0 AND 1),
    monitoring_cost REAL CHECK (monitoring_cost BETWEEN 0 AND 1),
    trigger_threshold REAL CHECK (trigger_threshold BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (leverage_id) REFERENCES leverage_points(leverage_id)
);

CREATE TABLE learning_loops (
    learning_id TEXT PRIMARY KEY,
    leverage_id TEXT NOT NULL,
    learning_loop_name TEXT NOT NULL,
    feedback_quality REAL CHECK (feedback_quality BETWEEN 0 AND 1),
    revision_trigger_clarity REAL CHECK (revision_trigger_clarity BETWEEN 0 AND 1),
    decision_memory_quality REAL CHECK (decision_memory_quality BETWEEN 0 AND 1),
    stakeholder_learning_visibility REAL CHECK (stakeholder_learning_visibility BETWEEN 0 AND 1),
    scenario_update_quality REAL CHECK (scenario_update_quality BETWEEN 0 AND 1),
    governance_response_capacity REAL CHECK (governance_response_capacity BETWEEN 0 AND 1),
    cycle_time REAL CHECK (cycle_time BETWEEN 0 AND 1),
    learning_risk REAL CHECK (learning_risk BETWEEN 0 AND 1),
    action_if_triggered TEXT,
    FOREIGN KEY (leverage_id) REFERENCES leverage_points(leverage_id)
);

CREATE TABLE decision_memory (
    decision_id TEXT PRIMARY KEY,
    leverage_id TEXT NOT NULL,
    decision_date TEXT,
    recurring_pattern TEXT,
    leverage_hypothesis TEXT,
    intervention_level TEXT,
    feedback_loops_reviewed TEXT,
    information_flows_reviewed TEXT,
    rules_and_incentives_reviewed TEXT,
    operating_goal_reviewed TEXT,
    paradigm_assumptions TEXT,
    tipping_thresholds TEXT,
    early_warning_indicators TEXT,
    revision_triggers TEXT,
    archived_learning TEXT,
    FOREIGN KEY (leverage_id) REFERENCES leverage_points(leverage_id)
);

CREATE VIEW leverage_point_scores AS
SELECT
    leverage_id,
    intervention_name,
    leverage_level,
    domain,
    ROUND(
      0.06 * implementation_ease +
      0.16 * structural_depth +
      0.14 * system_sensitivity +
      0.13 * feedback_influence +
      0.11 * information_effect +
      0.13 * rule_power +
      0.13 * goal_alignment +
      0.08 * paradigm_relevance +
      0.14 * transformative_potential +
      0.08 * learning_capacity -
      0.06 * unintended_consequence_risk,
      4
    ) AS leverage_profile_score
FROM leverage_points;

CREATE VIEW governance_need_scores AS
SELECT
    leverage_id,
    intervention_name,
    ROUND(
      0.26 * legitimacy_requirement +
      0.24 * unintended_consequence_risk +
      0.22 * transformative_potential +
      0.14 * (1 - implementation_ease) +
      0.14 * paradigm_relevance,
      4
    ) AS governance_need_score
FROM leverage_points;

CREATE VIEW feedback_leverage_scores AS
SELECT
    feedback_id,
    leverage_id,
    loop_name,
    loop_type,
    ROUND(
      0.14 * loop_strength +
      0.12 * current_visibility +
      0.16 * reinforcing_potential +
      0.12 * balancing_capacity -
      0.10 * delay_risk +
      0.10 * intervention_readiness +
      0.18 * positive_cascade_potential -
      0.10 * policy_resistance_risk,
      4
    ) AS feedback_leverage_score
FROM feedback_leverage;

CREATE VIEW information_flow_scores AS
SELECT
    flow_id,
    leverage_id,
    flow_name,
    flow_type,
    ROUND(
      0.15 * visibility_gain +
      0.14 * signal_quality +
      0.15 * decision_linkage +
      0.12 * stakeholder_access +
      0.12 * delay_reduction +
      0.12 * context_quality -
      0.10 * gaming_risk -
      0.08 * data_burden,
      4
    ) AS information_value_score
FROM information_flows;

CREATE VIEW rule_incentive_scores AS
SELECT
    rule_id,
    leverage_id,
    rule_name,
    rule_type,
    ROUND(
      0.14 * current_misalignment +
      0.18 * behavioral_power +
      0.12 * incentive_clarity +
      0.12 * cross_boundary_effect -
      0.10 * implementation_complexity -
      0.10 * political_resistance +
      0.12 * governance_readiness +
      0.12 * countermetric_quality,
      4
    ) AS rule_leverage_score
FROM rules_incentives;

CREATE VIEW system_goal_scores AS
SELECT
    goal_id,
    leverage_id,
    stated_goal,
    operating_goal,
    ROUND(
      0.20 * goal_misalignment -
      0.10 * metric_alignment -
      0.10 * budget_alignment -
      0.10 * decision_right_alignment +
      0.12 * (1 - tradeoff_clarity) +
      0.12 * stakeholder_legitimacy +
      0.12 * (1 - long_term_orientation) +
      0.10 * revision_readiness,
      4
    ) AS goal_change_need_score
FROM system_goals;

CREATE VIEW paradigm_scores AS
SELECT
    paradigm_id,
    leverage_id,
    paradigm_name,
    ROUND(
      0.10 * assumption_visibility -
      0.12 * paradigm_lock_in +
      0.16 * conceptual_clarity +
      0.16 * coalition_strength +
      0.16 * evidence_base +
      0.18 * transition_pathway_quality +
      0.16 * practice_embedding,
      4
    ) AS paradigm_transition_readiness
FROM paradigms;

CREATE VIEW tipping_threshold_scores AS
SELECT
    threshold_id,
    leverage_id,
    threshold_name,
    threshold_type,
    ROUND(
      0.12 * (1 - MAX(0, threshold_level - current_progress)) +
      0.14 * diffusion_potential +
      0.16 * self_reinforcement_strength +
      0.14 * complementary_condition_quality +
      0.14 * legitimacy_support +
      0.14 * infrastructure_support +
      0.12 * monitoring_quality,
      4
    ) AS tipping_readiness_score
FROM tipping_thresholds;

CREATE VIEW early_warning_indicator_scores AS
SELECT
    indicator_id,
    leverage_id,
    indicator_name,
    signal_type,
    ROUND(
      0.15 * leading_quality +
      0.13 * visibility +
      0.13 * reliability +
      0.13 * timeliness +
      0.12 * sensitivity +
      0.14 * decision_linkage -
      0.08 * false_positive_risk -
      0.08 * monitoring_cost,
      4
    ) AS indicator_quality_score
FROM early_warning_indicators;

CREATE VIEW learning_loop_scores AS
SELECT
    learning_id,
    leverage_id,
    learning_loop_name,
    ROUND(
      0.14 * feedback_quality +
      0.14 * revision_trigger_clarity +
      0.14 * decision_memory_quality +
      0.14 * stakeholder_learning_visibility +
      0.12 * scenario_update_quality +
      0.12 * governance_response_capacity +
      0.08 * cycle_time -
      0.10 * learning_risk,
      4
    ) AS learning_quality_score
FROM learning_loops;
