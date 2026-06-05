-- Advanced SQL schema for Portfolio Thinking in Strategic Ideation.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS portfolio_idea_scores;
DROP VIEW IF EXISTS risk_learning_scores;
DROP VIEW IF EXISTS capacity_load_scores;
DROP VIEW IF EXISTS dependency_sequence_scores;
DROP VIEW IF EXISTS time_horizon_scores;
DROP VIEW IF EXISTS ethics_power_scores;
DROP VIEW IF EXISTS governance_review_scores;
DROP VIEW IF EXISTS decision_memory_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS governance_review;
DROP TABLE IF EXISTS ethics_power;
DROP TABLE IF EXISTS time_horizons;
DROP TABLE IF EXISTS dependencies;
DROP TABLE IF EXISTS capacity_load;
DROP TABLE IF EXISTS risk_learning_profiles;
DROP TABLE IF EXISTS portfolio_targets;
DROP TABLE IF EXISTS strategic_ideas;

CREATE TABLE strategic_ideas (
    idea_id TEXT PRIMARY KEY,
    idea_name TEXT NOT NULL,
    role TEXT NOT NULL,
    time_horizon TEXT NOT NULL,
    impact REAL CHECK (impact BETWEEN 0 AND 1),
    risk REAL CHECK (risk BETWEEN 0 AND 1),
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    option_value REAL CHECK (option_value BETWEEN 0 AND 1),
    strategic_fit REAL CHECK (strategic_fit BETWEEN 0 AND 1),
    capacity_demand REAL CHECK (capacity_demand BETWEEN 0 AND 1),
    ethical_resilience REAL CHECK (ethical_resilience BETWEEN 0 AND 1),
    evidence_strength REAL CHECK (evidence_strength BETWEEN 0 AND 1),
    dependency_count INTEGER,
    governance_readiness REAL CHECK (governance_readiness BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE portfolio_targets (
    role TEXT PRIMARY KEY,
    target_share REAL CHECK (target_share BETWEEN 0 AND 1),
    minimum_share REAL CHECK (minimum_share BETWEEN 0 AND 1),
    maximum_share REAL CHECK (maximum_share BETWEEN 0 AND 1),
    strategic_rationale TEXT
);

CREATE TABLE risk_learning_profiles (
    profile_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    implementation_risk REAL CHECK (implementation_risk BETWEEN 0 AND 1),
    strategic_risk REAL CHECK (strategic_risk BETWEEN 0 AND 1),
    ethical_risk REAL CHECK (ethical_risk BETWEEN 0 AND 1),
    systemic_risk REAL CHECK (systemic_risk BETWEEN 0 AND 1),
    opportunity_cost REAL CHECK (opportunity_cost BETWEEN 0 AND 1),
    learning_quality REAL CHECK (learning_quality BETWEEN 0 AND 1),
    assumption_clarity REAL CHECK (assumption_clarity BETWEEN 0 AND 1),
    evidence_gap REAL CHECK (evidence_gap BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id)
);

CREATE TABLE capacity_load (
    capacity_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    budget_demand REAL CHECK (budget_demand BETWEEN 0 AND 1),
    staff_demand REAL CHECK (staff_demand BETWEEN 0 AND 1),
    leadership_attention REAL CHECK (leadership_attention BETWEEN 0 AND 1),
    technical_capacity_demand REAL CHECK (technical_capacity_demand BETWEEN 0 AND 1),
    governance_bandwidth REAL CHECK (governance_bandwidth BETWEEN 0 AND 1),
    stakeholder_absorption REAL CHECK (stakeholder_absorption BETWEEN 0 AND 1),
    communication_load REAL CHECK (communication_load BETWEEN 0 AND 1),
    available_capacity REAL CHECK (available_capacity BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id)
);

CREATE TABLE dependencies (
    dependency_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    depends_on TEXT NOT NULL,
    dependency_type TEXT NOT NULL,
    dependency_strength REAL CHECK (dependency_strength BETWEEN 0 AND 1),
    sequencing_urgency REAL CHECK (sequencing_urgency BETWEEN 0 AND 1),
    readiness_gap REAL CHECK (readiness_gap BETWEEN 0 AND 1),
    criticality REAL CHECK (criticality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id),
    FOREIGN KEY (depends_on) REFERENCES strategic_ideas(idea_id)
);

CREATE TABLE time_horizons (
    horizon_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    immediate_value REAL CHECK (immediate_value BETWEEN 0 AND 1),
    short_term_value REAL CHECK (short_term_value BETWEEN 0 AND 1),
    medium_term_value REAL CHECK (medium_term_value BETWEEN 0 AND 1),
    long_term_value REAL CHECK (long_term_value BETWEEN 0 AND 1),
    intergenerational_value REAL CHECK (intergenerational_value BETWEEN 0 AND 1),
    near_term_pressure REAL CHECK (near_term_pressure BETWEEN 0 AND 1),
    deferred_value REAL CHECK (deferred_value BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id)
);

CREATE TABLE ethics_power (
    ethics_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    ethical_issue TEXT NOT NULL,
    sponsor_power REAL CHECK (sponsor_power BETWEEN 0 AND 1),
    affected_stakeholder_voice REAL CHECK (affected_stakeholder_voice BETWEEN 0 AND 1),
    benefit_concentration REAL CHECK (benefit_concentration BETWEEN 0 AND 1),
    burden_concentration REAL CHECK (burden_concentration BETWEEN 0 AND 1),
    long_term_responsibility REAL CHECK (long_term_responsibility BETWEEN 0 AND 1),
    transparency REAL CHECK (transparency BETWEEN 0 AND 1),
    redress_quality REAL CHECK (redress_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id)
);

CREATE TABLE governance_review (
    governance_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    entry_rule_quality REAL CHECK (entry_rule_quality BETWEEN 0 AND 1),
    review_cadence_quality REAL CHECK (review_cadence_quality BETWEEN 0 AND 1),
    pruning_rule_quality REAL CHECK (pruning_rule_quality BETWEEN 0 AND 1),
    evidence_standard_quality REAL CHECK (evidence_standard_quality BETWEEN 0 AND 1),
    decision_rights_clarity REAL CHECK (decision_rights_clarity BETWEEN 0 AND 1),
    escalation_path_quality REAL CHECK (escalation_path_quality BETWEEN 0 AND 1),
    decision_memory_quality REAL CHECK (decision_memory_quality BETWEEN 0 AND 1),
    portfolio_visibility REAL CHECK (portfolio_visibility BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id)
);

CREATE TABLE decision_memory (
    memory_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    memory_practice TEXT NOT NULL,
    role_record_quality REAL CHECK (role_record_quality BETWEEN 0 AND 1),
    evidence_record_quality REAL CHECK (evidence_record_quality BETWEEN 0 AND 1),
    risk_record_quality REAL CHECK (risk_record_quality BETWEEN 0 AND 1),
    dependency_record_quality REAL CHECK (dependency_record_quality BETWEEN 0 AND 1),
    capacity_record_quality REAL CHECK (capacity_record_quality BETWEEN 0 AND 1),
    ethics_record_quality REAL CHECK (ethics_record_quality BETWEEN 0 AND 1),
    decision_gate_record_quality REAL CHECK (decision_gate_record_quality BETWEEN 0 AND 1),
    revision_history_quality REAL CHECK (revision_history_quality BETWEEN 0 AND 1),
    reuse_quality REAL CHECK (reuse_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (idea_id) REFERENCES strategic_ideas(idea_id)
);

CREATE VIEW portfolio_idea_scores AS
SELECT
    idea_id,
    idea_name,
    role,
    time_horizon,
    ROUND(
      0.17 * impact +
      0.16 * strategic_fit +
      0.15 * learning_value +
      0.15 * option_value +
      0.12 * ethical_resilience +
      0.10 * evidence_strength +
      0.08 * governance_readiness -
      0.10 * risk -
      0.08 * capacity_demand -
      0.04 * MIN(dependency_count / 6.0, 1.0),
      4
    ) AS portfolio_contribution,
    ROUND(
      0.30 * capacity_demand +
      0.24 * risk +
      0.14 * (1 - strategic_fit) +
      0.12 * (1 - ethical_resilience) +
      0.10 * (1 - option_value) +
      0.10 * MIN(dependency_count / 6.0, 1.0),
      4
    ) AS overload_warning
FROM strategic_ideas;

CREATE VIEW risk_learning_scores AS
SELECT
    profile_id,
    idea_id,
    ROUND(
      0.20 * implementation_risk +
      0.22 * strategic_risk +
      0.18 * ethical_risk +
      0.18 * systemic_risk +
      0.22 * opportunity_cost,
      4
    ) AS exposure_score,
    ROUND(
      0.36 * learning_quality +
      0.24 * assumption_clarity +
      0.22 * (1 - evidence_gap),
      4
    ) AS learning_strength
FROM risk_learning_profiles;

CREATE VIEW capacity_load_scores AS
SELECT
    capacity_id,
    idea_id,
    ROUND(
      0.16 * budget_demand +
      0.16 * staff_demand +
      0.14 * leadership_attention +
      0.14 * technical_capacity_demand +
      0.14 * governance_bandwidth +
      0.12 * stakeholder_absorption +
      0.10 * communication_load,
      4
    ) AS gross_demand,
    available_capacity,
    ROUND(
      (
        0.16 * budget_demand +
        0.16 * staff_demand +
        0.14 * leadership_attention +
        0.14 * technical_capacity_demand +
        0.14 * governance_bandwidth +
        0.12 * stakeholder_absorption +
        0.10 * communication_load
      ) / available_capacity,
      4
    ) AS capacity_load
FROM capacity_load;

CREATE VIEW dependency_sequence_scores AS
SELECT
    dependency_id,
    idea_id,
    depends_on,
    dependency_type,
    ROUND(
      0.30 * dependency_strength +
      0.26 * sequencing_urgency +
      0.24 * readiness_gap +
      0.20 * criticality,
      4
    ) AS sequence_priority
FROM dependencies;

CREATE VIEW time_horizon_scores AS
SELECT
    horizon_id,
    idea_id,
    ROUND(
      0.20 * medium_term_value +
      0.30 * long_term_value +
      0.24 * intergenerational_value +
      0.16 * deferred_value +
      0.10 * short_term_value,
      4
    ) AS future_value,
    ROUND(
      0.40 * near_term_pressure +
      0.26 * immediate_value +
      0.18 * (1 - long_term_value) +
      0.16 * (1 - intergenerational_value),
      4
    ) AS present_bias_warning
FROM time_horizons;

CREATE VIEW ethics_power_scores AS
SELECT
    ethics_id,
    idea_id,
    ethical_issue,
    ROUND(
      0.18 * sponsor_power +
      0.18 * (1 - affected_stakeholder_voice) +
      0.16 * benefit_concentration +
      0.18 * burden_concentration +
      0.12 * (1 - transparency) +
      0.10 * (1 - redress_quality) +
      0.08 * (1 - long_term_responsibility),
      4
    ) AS power_risk
FROM ethics_power;

CREATE VIEW governance_review_scores AS
SELECT
    governance_id,
    idea_id,
    ROUND(
      0.12 * entry_rule_quality +
      0.12 * review_cadence_quality +
      0.13 * pruning_rule_quality +
      0.14 * evidence_standard_quality +
      0.13 * decision_rights_clarity +
      0.12 * escalation_path_quality +
      0.12 * decision_memory_quality +
      0.12 * portfolio_visibility,
      4
    ) AS governance_score
FROM governance_review;

CREATE VIEW decision_memory_scores AS
SELECT
    memory_id,
    idea_id,
    memory_practice,
    ROUND(
      0.11 * role_record_quality +
      0.12 * evidence_record_quality +
      0.12 * risk_record_quality +
      0.12 * dependency_record_quality +
      0.11 * capacity_record_quality +
      0.12 * ethics_record_quality +
      0.11 * decision_gate_record_quality +
      0.10 * revision_history_quality +
      0.09 * reuse_quality,
      4
    ) AS decision_memory_score
FROM decision_memory;
