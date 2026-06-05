-- Advanced SQL schema for Game Theory and Strategic Interaction.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS strategic_interaction_scores;
DROP VIEW IF EXISTS actor_payoff_scores;
DROP VIEW IF EXISTS information_signal_scores;
DROP VIEW IF EXISTS equilibrium_diagnosis_scores;
DROP VIEW IF EXISTS cooperation_fragility_scores;
DROP VIEW IF EXISTS repeated_interaction_scores;
DROP VIEW IF EXISTS mechanism_design_scores;
DROP VIEW IF EXISTS behavioral_game_theory_scores;
DROP VIEW IF EXISTS ethics_power_scores;
DROP VIEW IF EXISTS strategic_interaction_memory_scores;

DROP TABLE IF EXISTS strategic_interaction_memory;
DROP TABLE IF EXISTS ethics_power;
DROP TABLE IF EXISTS behavioral_game_theory;
DROP TABLE IF EXISTS mechanism_design;
DROP TABLE IF EXISTS repeated_interactions;
DROP TABLE IF EXISTS cooperation_fragility;
DROP TABLE IF EXISTS equilibrium_diagnoses;
DROP TABLE IF EXISTS information_signals;
DROP TABLE IF EXISTS actor_payoffs;
DROP TABLE IF EXISTS strategic_interaction_profiles;

CREATE TABLE strategic_interaction_profiles (
    setting_id TEXT PRIMARY KEY,
    setting_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    rivalry REAL CHECK (rivalry BETWEEN 0 AND 1),
    coordination_potential REAL CHECK (coordination_potential BETWEEN 0 AND 1),
    information_asymmetry REAL CHECK (information_asymmetry BETWEEN 0 AND 1),
    retaliation_risk REAL CHECK (retaliation_risk BETWEEN 0 AND 1),
    institutional_support REAL CHECK (institutional_support BETWEEN 0 AND 1),
    behavioral_realism REAL CHECK (behavioral_realism BETWEEN 0 AND 1),
    mechanism_design_potential REAL CHECK (mechanism_design_potential BETWEEN 0 AND 1),
    ethical_complexity REAL CHECK (ethical_complexity BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE actor_payoffs (
    actor_id TEXT PRIMARY KEY,
    setting_id TEXT NOT NULL,
    actor_name TEXT NOT NULL,
    actor_role TEXT NOT NULL,
    material_payoff REAL CHECK (material_payoff BETWEEN 0 AND 1),
    reputation_payoff REAL CHECK (reputation_payoff BETWEEN 0 AND 1),
    legitimacy_payoff REAL CHECK (legitimacy_payoff BETWEEN 0 AND 1),
    risk_avoidance REAL CHECK (risk_avoidance BETWEEN 0 AND 1),
    control_preference REAL CHECK (control_preference BETWEEN 0 AND 1),
    cooperation_dependency REAL CHECK (cooperation_dependency BETWEEN 0 AND 1),
    exit_option_quality REAL CHECK (exit_option_quality BETWEEN 0 AND 1),
    power_level REAL CHECK (power_level BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (setting_id) REFERENCES strategic_interaction_profiles(setting_id)
);

CREATE TABLE information_signals (
    signal_id TEXT PRIMARY KEY,
    setting_id TEXT NOT NULL,
    signal_name TEXT NOT NULL,
    signal_type TEXT NOT NULL,
    credibility REAL CHECK (credibility BETWEEN 0 AND 1),
    observability REAL CHECK (observability BETWEEN 0 AND 1),
    costliness REAL CHECK (costliness BETWEEN 0 AND 1),
    ambiguity REAL CHECK (ambiguity BETWEEN 0 AND 1),
    response_sensitivity REAL CHECK (response_sensitivity BETWEEN 0 AND 1),
    misinterpretation_risk REAL CHECK (misinterpretation_risk BETWEEN 0 AND 1),
    coordination_value REAL CHECK (coordination_value BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (setting_id) REFERENCES strategic_interaction_profiles(setting_id)
);

CREATE TABLE equilibrium_diagnoses (
    equilibrium_id TEXT PRIMARY KEY,
    setting_id TEXT NOT NULL,
    equilibrium_name TEXT NOT NULL,
    desirability REAL CHECK (desirability BETWEEN 0 AND 1),
    stability REAL CHECK (stability BETWEEN 0 AND 1),
    efficiency REAL CHECK (efficiency BETWEEN 0 AND 1),
    fairness REAL CHECK (fairness BETWEEN 0 AND 1),
    exit_pressure REAL CHECK (exit_pressure BETWEEN 0 AND 1),
    coordination_barrier REAL CHECK (coordination_barrier BETWEEN 0 AND 1),
    incentive_misalignment REAL CHECK (incentive_misalignment BETWEEN 0 AND 1),
    rule_change_need REAL CHECK (rule_change_need BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (setting_id) REFERENCES strategic_interaction_profiles(setting_id)
);

CREATE TABLE cooperation_fragility (
    cooperation_id TEXT PRIMARY KEY,
    setting_id TEXT NOT NULL,
    cooperation_need TEXT NOT NULL,
    trust_level REAL CHECK (trust_level BETWEEN 0 AND 1),
    monitoring_quality REAL CHECK (monitoring_quality BETWEEN 0 AND 1),
    defection_temptation REAL CHECK (defection_temptation BETWEEN 0 AND 1),
    retaliation_feasibility REAL CHECK (retaliation_feasibility BETWEEN 0 AND 1),
    reputation_value REAL CHECK (reputation_value BETWEEN 0 AND 1),
    reciprocity_quality REAL CHECK (reciprocity_quality BETWEEN 0 AND 1),
    enforcement_quality REAL CHECK (enforcement_quality BETWEEN 0 AND 1),
    shared_upside REAL CHECK (shared_upside BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (setting_id) REFERENCES strategic_interaction_profiles(setting_id)
);

CREATE TABLE repeated_interactions (
    repeat_id TEXT PRIMARY KEY,
    setting_id TEXT NOT NULL,
    relationship_name TEXT NOT NULL,
    interaction_frequency REAL CHECK (interaction_frequency BETWEEN 0 AND 1),
    future_shadow REAL CHECK (future_shadow BETWEEN 0 AND 1),
    reputation_visibility REAL CHECK (reputation_visibility BETWEEN 0 AND 1),
    memory_quality REAL CHECK (memory_quality BETWEEN 0 AND 1),
    retaliation_proportionality REAL CHECK (retaliation_proportionality BETWEEN 0 AND 1),
    forgiveness_capacity REAL CHECK (forgiveness_capacity BETWEEN 0 AND 1),
    trust_repair_quality REAL CHECK (trust_repair_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (setting_id) REFERENCES strategic_interaction_profiles(setting_id)
);

CREATE TABLE mechanism_design (
    mechanism_id TEXT PRIMARY KEY,
    setting_id TEXT NOT NULL,
    mechanism_name TEXT NOT NULL,
    incentive_alignment REAL CHECK (incentive_alignment BETWEEN 0 AND 1),
    information_transparency REAL CHECK (information_transparency BETWEEN 0 AND 1),
    verification_quality REAL CHECK (verification_quality BETWEEN 0 AND 1),
    enforcement_quality REAL CHECK (enforcement_quality BETWEEN 0 AND 1),
    participation_quality REAL CHECK (participation_quality BETWEEN 0 AND 1),
    burden_distribution_quality REAL CHECK (burden_distribution_quality BETWEEN 0 AND 1),
    adaptability REAL CHECK (adaptability BETWEEN 0 AND 1),
    implementation_feasibility REAL CHECK (implementation_feasibility BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (setting_id) REFERENCES strategic_interaction_profiles(setting_id)
);

CREATE TABLE behavioral_game_theory (
    behavior_id TEXT PRIMARY KEY,
    setting_id TEXT NOT NULL,
    behavioral_factor TEXT NOT NULL,
    fairness_salience REAL CHECK (fairness_salience BETWEEN 0 AND 1),
    trust_salience REAL CHECK (trust_salience BETWEEN 0 AND 1),
    identity_salience REAL CHECK (identity_salience BETWEEN 0 AND 1),
    bounded_reasoning_risk REAL CHECK (bounded_reasoning_risk BETWEEN 0 AND 1),
    loss_aversion_risk REAL CHECK (loss_aversion_risk BETWEEN 0 AND 1),
    norm_strength REAL CHECK (norm_strength BETWEEN 0 AND 1),
    legitimacy_sensitivity REAL CHECK (legitimacy_sensitivity BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (setting_id) REFERENCES strategic_interaction_profiles(setting_id)
);

CREATE TABLE ethics_power (
    ethics_id TEXT PRIMARY KEY,
    setting_id TEXT NOT NULL,
    ethical_issue TEXT NOT NULL,
    power_asymmetry REAL CHECK (power_asymmetry BETWEEN 0 AND 1),
    voice_quality REAL CHECK (voice_quality BETWEEN 0 AND 1),
    exit_option_quality REAL CHECK (exit_option_quality BETWEEN 0 AND 1),
    transparency REAL CHECK (transparency BETWEEN 0 AND 1),
    burden_shift_risk REAL CHECK (burden_shift_risk BETWEEN 0 AND 1),
    manipulation_risk REAL CHECK (manipulation_risk BETWEEN 0 AND 1),
    legitimacy_quality REAL CHECK (legitimacy_quality BETWEEN 0 AND 1),
    redress_quality REAL CHECK (redress_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (setting_id) REFERENCES strategic_interaction_profiles(setting_id)
);

CREATE TABLE strategic_interaction_memory (
    memory_id TEXT PRIMARY KEY,
    setting_id TEXT NOT NULL,
    memory_practice TEXT NOT NULL,
    player_record_quality REAL CHECK (player_record_quality BETWEEN 0 AND 1),
    payoff_record_quality REAL CHECK (payoff_record_quality BETWEEN 0 AND 1),
    information_record_quality REAL CHECK (information_record_quality BETWEEN 0 AND 1),
    equilibrium_record_quality REAL CHECK (equilibrium_record_quality BETWEEN 0 AND 1),
    signal_record_quality REAL CHECK (signal_record_quality BETWEEN 0 AND 1),
    mechanism_record_quality REAL CHECK (mechanism_record_quality BETWEEN 0 AND 1),
    ethics_record_quality REAL CHECK (ethics_record_quality BETWEEN 0 AND 1),
    revision_record_quality REAL CHECK (revision_record_quality BETWEEN 0 AND 1),
    reuse_quality REAL CHECK (reuse_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (setting_id) REFERENCES strategic_interaction_profiles(setting_id)
);

CREATE VIEW strategic_interaction_scores AS
SELECT
    setting_id,
    setting_name,
    domain,
    ROUND(
      0.12 * rivalry +
      0.18 * coordination_potential +
      0.12 * information_asymmetry +
      0.10 * retaliation_risk +
      0.15 * institutional_support +
      0.12 * behavioral_realism +
      0.15 * mechanism_design_potential +
      0.06 * ethical_complexity,
      4
    ) AS strategic_interaction_score,
    ROUND(
      0.22 * rivalry +
      0.20 * retaliation_risk +
      0.16 * information_asymmetry +
      0.12 * ethical_complexity -
      0.15 * institutional_support -
      0.15 * coordination_potential,
      4
    ) AS cooperation_fragility,
    ROUND(
      0.30 * mechanism_design_potential +
      0.18 * coordination_potential +
      0.16 * information_asymmetry +
      0.14 * ethical_complexity +
      0.12 * institutional_support +
      0.10 * behavioral_realism,
      4
    ) AS mechanism_opportunity
FROM strategic_interaction_profiles;

CREATE VIEW actor_payoff_scores AS
SELECT
    actor_id,
    setting_id,
    actor_name,
    actor_role,
    ROUND(
      0.24 * power_level +
      0.18 * (1 - exit_option_quality) +
      0.18 * control_preference +
      0.14 * risk_avoidance +
      0.14 * (1 - cooperation_dependency) +
      0.12 * material_payoff,
      4
    ) AS power_dependency_risk
FROM actor_payoffs;

CREATE VIEW information_signal_scores AS
SELECT
    signal_id,
    setting_id,
    signal_name,
    signal_type,
    ROUND(
      0.24 * response_sensitivity +
      0.22 * misinterpretation_risk +
      0.18 * ambiguity +
      0.14 * (1 - credibility) +
      0.12 * observability +
      0.10 * costliness,
      4
    ) AS response_risk
FROM information_signals;

CREATE VIEW equilibrium_diagnosis_scores AS
SELECT
    equilibrium_id,
    setting_id,
    equilibrium_name,
    ROUND(
      0.18 * (1 - desirability) +
      0.15 * stability +
      0.15 * (1 - efficiency) +
      0.13 * (1 - fairness) +
      0.10 * exit_pressure +
      0.12 * coordination_barrier +
      0.12 * incentive_misalignment +
      0.05 * rule_change_need,
      4
    ) AS bad_equilibrium_risk
FROM equilibrium_diagnoses;

CREATE VIEW cooperation_fragility_scores AS
SELECT
    cooperation_id,
    setting_id,
    cooperation_need,
    ROUND(
      0.16 * (1 - trust_level) +
      0.12 * (1 - monitoring_quality) +
      0.18 * defection_temptation +
      0.10 * (1 - retaliation_feasibility) +
      0.10 * (1 - reputation_value) +
      0.12 * (1 - reciprocity_quality) +
      0.12 * (1 - enforcement_quality) +
      0.10 * (1 - shared_upside),
      4
    ) AS cooperation_fragility_score
FROM cooperation_fragility;

CREATE VIEW repeated_interaction_scores AS
SELECT
    repeat_id,
    setting_id,
    relationship_name,
    ROUND(
      0.14 * interaction_frequency +
      0.17 * future_shadow +
      0.14 * reputation_visibility +
      0.14 * memory_quality +
      0.10 * retaliation_proportionality +
      0.14 * forgiveness_capacity +
      0.17 * trust_repair_quality,
      4
    ) AS repeated_game_capacity
FROM repeated_interactions;

CREATE VIEW mechanism_design_scores AS
SELECT
    mechanism_id,
    setting_id,
    mechanism_name,
    ROUND(
      0.15 * incentive_alignment +
      0.13 * information_transparency +
      0.13 * verification_quality +
      0.13 * enforcement_quality +
      0.12 * participation_quality +
      0.13 * burden_distribution_quality +
      0.11 * adaptability +
      0.10 * implementation_feasibility,
      4
    ) AS mechanism_design_score
FROM mechanism_design;

CREATE VIEW behavioral_game_theory_scores AS
SELECT
    behavior_id,
    setting_id,
    behavioral_factor,
    ROUND(
      0.18 * bounded_reasoning_risk +
      0.18 * loss_aversion_risk +
      0.16 * legitimacy_sensitivity +
      0.14 * identity_salience +
      0.12 * fairness_salience +
      0.12 * (1 - trust_salience) +
      0.10 * (1 - norm_strength),
      4
    ) AS behavioral_failure_risk
FROM behavioral_game_theory;

CREATE VIEW ethics_power_scores AS
SELECT
    ethics_id,
    setting_id,
    ethical_issue,
    ROUND(
      0.16 * power_asymmetry +
      0.13 * (1 - voice_quality) +
      0.13 * (1 - exit_option_quality) +
      0.12 * (1 - transparency) +
      0.16 * burden_shift_risk +
      0.14 * manipulation_risk +
      0.10 * (1 - legitimacy_quality) +
      0.06 * (1 - redress_quality),
      4
    ) AS ethics_power_risk
FROM ethics_power;

CREATE VIEW strategic_interaction_memory_scores AS
SELECT
    memory_id,
    setting_id,
    memory_practice,
    ROUND(
      0.11 * player_record_quality +
      0.11 * payoff_record_quality +
      0.11 * information_record_quality +
      0.12 * equilibrium_record_quality +
      0.11 * signal_record_quality +
      0.12 * mechanism_record_quality +
      0.11 * ethics_record_quality +
      0.10 * revision_record_quality +
      0.11 * reuse_quality,
      4
    ) AS strategic_interaction_memory_score
FROM strategic_interaction_memory;
