-- Advanced SQL schema for boundary setting in strategic ideation.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS boundary_quality_scores;
DROP VIEW IF EXISTS stakeholder_boundary_scores;
DROP VIEW IF EXISTS causal_boundary_scores;
DROP VIEW IF EXISTS temporal_boundary_scores;
DROP VIEW IF EXISTS institutional_boundary_scores;
DROP VIEW IF EXISTS evidence_boundary_scores;
DROP VIEW IF EXISTS ethical_boundary_scores;
DROP VIEW IF EXISTS boundary_drift_scores;
DROP VIEW IF EXISTS revision_trigger_scores;

DROP TABLE IF EXISTS decision_memory;
DROP TABLE IF EXISTS revision_triggers;
DROP TABLE IF EXISTS boundary_drift;
DROP TABLE IF EXISTS options;
DROP TABLE IF EXISTS ethical_boundaries;
DROP TABLE IF EXISTS evidence_boundaries;
DROP TABLE IF EXISTS institutional_boundaries;
DROP TABLE IF EXISTS temporal_boundaries;
DROP TABLE IF EXISTS causal_boundaries;
DROP TABLE IF EXISTS stakeholder_boundaries;
DROP TABLE IF EXISTS boundary_frames;

CREATE TABLE boundary_frames (
    boundary_id TEXT PRIMARY KEY,
    boundary_name TEXT NOT NULL,
    frame_type TEXT NOT NULL,
    domain TEXT NOT NULL,
    problem_clarity REAL CHECK (problem_clarity BETWEEN 0 AND 1),
    system_context REAL CHECK (system_context BETWEEN 0 AND 1),
    stakeholder_inclusion REAL CHECK (stakeholder_inclusion BETWEEN 0 AND 1),
    causal_adequacy REAL CHECK (causal_adequacy BETWEEN 0 AND 1),
    temporal_adequacy REAL CHECK (temporal_adequacy BETWEEN 0 AND 1),
    institutional_responsibility REAL CHECK (institutional_responsibility BETWEEN 0 AND 1),
    evidence_diversity REAL CHECK (evidence_diversity BETWEEN 0 AND 1),
    ethical_review REAL CHECK (ethical_review BETWEEN 0 AND 1),
    revision_readiness REAL CHECK (revision_readiness BETWEEN 0 AND 1),
    actionability REAL CHECK (actionability BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE stakeholder_boundaries (
    stakeholder_id TEXT PRIMARY KEY,
    boundary_id TEXT NOT NULL,
    stakeholder_group TEXT NOT NULL,
    role_type TEXT NOT NULL,
    inclusion_quality REAL CHECK (inclusion_quality BETWEEN 0 AND 1),
    affectedness REAL CHECK (affectedness BETWEEN 0 AND 1),
    decision_power REAL CHECK (decision_power BETWEEN 0 AND 1),
    implementation_role REAL CHECK (implementation_role BETWEEN 0 AND 1),
    knowledge_value REAL CHECK (knowledge_value BETWEEN 0 AND 1),
    burden_risk REAL CHECK (burden_risk BETWEEN 0 AND 1),
    trust_sensitivity REAL CHECK (trust_sensitivity BETWEEN 0 AND 1),
    representation_quality REAL CHECK (representation_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (boundary_id) REFERENCES boundary_frames(boundary_id)
);

CREATE TABLE causal_boundaries (
    cause_id TEXT PRIMARY KEY,
    boundary_id TEXT NOT NULL,
    causal_frame TEXT NOT NULL,
    causal_level TEXT NOT NULL,
    causal_plausibility REAL CHECK (causal_plausibility BETWEEN 0 AND 1),
    evidence_strength REAL CHECK (evidence_strength BETWEEN 0 AND 1),
    structural_depth REAL CHECK (structural_depth BETWEEN 0 AND 1),
    actor_adaptation_considered REAL CHECK (actor_adaptation_considered BETWEEN 0 AND 1),
    feedback_considered REAL CHECK (feedback_considered BETWEEN 0 AND 1),
    incentive_considered REAL CHECK (incentive_considered BETWEEN 0 AND 1),
    historical_context_considered REAL CHECK (historical_context_considered BETWEEN 0 AND 1),
    implementation_relevance REAL CHECK (implementation_relevance BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (boundary_id) REFERENCES boundary_frames(boundary_id)
);

CREATE TABLE temporal_boundaries (
    time_id TEXT PRIMARY KEY,
    boundary_id TEXT NOT NULL,
    time_horizon TEXT NOT NULL,
    review_stage TEXT NOT NULL,
    immediate_signal_quality REAL CHECK (immediate_signal_quality BETWEEN 0 AND 1),
    short_term_signal_quality REAL CHECK (short_term_signal_quality BETWEEN 0 AND 1),
    medium_term_signal_quality REAL CHECK (medium_term_signal_quality BETWEEN 0 AND 1),
    long_term_signal_quality REAL CHECK (long_term_signal_quality BETWEEN 0 AND 1),
    delayed_effect_risk REAL CHECK (delayed_effect_risk BETWEEN 0 AND 1),
    resilience_relevance REAL CHECK (resilience_relevance BETWEEN 0 AND 1),
    ownership_continuity REAL CHECK (ownership_continuity BETWEEN 0 AND 1),
    revision_cadence_quality REAL CHECK (revision_cadence_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (boundary_id) REFERENCES boundary_frames(boundary_id)
);

CREATE TABLE institutional_boundaries (
    institution_id TEXT PRIMARY KEY,
    boundary_id TEXT NOT NULL,
    institutional_frame TEXT NOT NULL,
    authority_clarity REAL CHECK (authority_clarity BETWEEN 0 AND 1),
    influence_capacity REAL CHECK (influence_capacity BETWEEN 0 AND 1),
    consequence_visibility REAL CHECK (consequence_visibility BETWEEN 0 AND 1),
    accountability_clarity REAL CHECK (accountability_clarity BETWEEN 0 AND 1),
    cross_boundary_coordination REAL CHECK (cross_boundary_coordination BETWEEN 0 AND 1),
    externality_risk REAL CHECK (externality_risk BETWEEN 0 AND 1),
    escalation_path_quality REAL CHECK (escalation_path_quality BETWEEN 0 AND 1),
    learning_flow_quality REAL CHECK (learning_flow_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (boundary_id) REFERENCES boundary_frames(boundary_id)
);

CREATE TABLE evidence_boundaries (
    evidence_id TEXT PRIMARY KEY,
    boundary_id TEXT NOT NULL,
    evidence_frame TEXT NOT NULL,
    quantitative_quality REAL CHECK (quantitative_quality BETWEEN 0 AND 1),
    qualitative_quality REAL CHECK (qualitative_quality BETWEEN 0 AND 1),
    stakeholder_testimony_quality REAL CHECK (stakeholder_testimony_quality BETWEEN 0 AND 1),
    prototype_evidence_quality REAL CHECK (prototype_evidence_quality BETWEEN 0 AND 1),
    scenario_evidence_quality REAL CHECK (scenario_evidence_quality BETWEEN 0 AND 1),
    expert_judgment_quality REAL CHECK (expert_judgment_quality BETWEEN 0 AND 1),
    ethical_reasoning_quality REAL CHECK (ethical_reasoning_quality BETWEEN 0 AND 1),
    interpretation_discipline REAL CHECK (interpretation_discipline BETWEEN 0 AND 1),
    blind_spot_risk REAL CHECK (blind_spot_risk BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (boundary_id) REFERENCES boundary_frames(boundary_id)
);

CREATE TABLE ethical_boundaries (
    ethics_id TEXT PRIMARY KEY,
    boundary_id TEXT NOT NULL,
    ethical_issue TEXT NOT NULL,
    exclusion_risk REAL CHECK (exclusion_risk BETWEEN 0 AND 1),
    burden_shift_risk REAL CHECK (burden_shift_risk BETWEEN 0 AND 1),
    harm_visibility REAL CHECK (harm_visibility BETWEEN 0 AND 1),
    future_consequence_risk REAL CHECK (future_consequence_risk BETWEEN 0 AND 1),
    power_asymmetry REAL CHECK (power_asymmetry BETWEEN 0 AND 1),
    redress_path_quality REAL CHECK (redress_path_quality BETWEEN 0 AND 1),
    participation_quality REAL CHECK (participation_quality BETWEEN 0 AND 1),
    accountability_quality REAL CHECK (accountability_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (boundary_id) REFERENCES boundary_frames(boundary_id)
);

CREATE TABLE options (
    option_id TEXT PRIMARY KEY,
    option_name TEXT NOT NULL,
    internal_efficiency REAL CHECK (internal_efficiency BETWEEN 0 AND 1),
    stakeholder_value REAL CHECK (stakeholder_value BETWEEN 0 AND 1),
    system_leverage REAL CHECK (system_leverage BETWEEN 0 AND 1),
    long_term_resilience REAL CHECK (long_term_resilience BETWEEN 0 AND 1),
    ethical_responsibility REAL CHECK (ethical_responsibility BETWEEN 0 AND 1),
    implementation_feasibility REAL CHECK (implementation_feasibility BETWEEN 0 AND 1),
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    strategic_reversibility REAL CHECK (strategic_reversibility BETWEEN 0 AND 1)
);

CREATE TABLE boundary_drift (
    drift_id TEXT PRIMARY KEY,
    boundary_id TEXT NOT NULL,
    drift_type TEXT NOT NULL,
    original_boundary TEXT NOT NULL,
    new_boundary TEXT NOT NULL,
    scope_change REAL CHECK (scope_change BETWEEN 0 AND 1),
    stakeholder_change REAL CHECK (stakeholder_change BETWEEN 0 AND 1),
    metric_change REAL CHECK (metric_change BETWEEN 0 AND 1),
    responsibility_change REAL CHECK (responsibility_change BETWEEN 0 AND 1),
    evidence_change REAL CHECK (evidence_change BETWEEN 0 AND 1),
    explicitness REAL CHECK (explicitness BETWEEN 0 AND 1),
    evidence_basis REAL CHECK (evidence_basis BETWEEN 0 AND 1),
    coherence_risk REAL CHECK (coherence_risk BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (boundary_id) REFERENCES boundary_frames(boundary_id)
);

CREATE TABLE revision_triggers (
    trigger_id TEXT PRIMARY KEY,
    boundary_id TEXT NOT NULL,
    trigger_name TEXT NOT NULL,
    trigger_type TEXT NOT NULL,
    signal_quality REAL CHECK (signal_quality BETWEEN 0 AND 1),
    threshold_clarity REAL CHECK (threshold_clarity BETWEEN 0 AND 1),
    decision_linkage REAL CHECK (decision_linkage BETWEEN 0 AND 1),
    timeliness REAL CHECK (timeliness BETWEEN 0 AND 1),
    stakeholder_visibility REAL CHECK (stakeholder_visibility BETWEEN 0 AND 1),
    governance_owner_clarity REAL CHECK (governance_owner_clarity BETWEEN 0 AND 1),
    response_options_quality REAL CHECK (response_options_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (boundary_id) REFERENCES boundary_frames(boundary_id)
);

CREATE TABLE decision_memory (
    decision_id TEXT PRIMARY KEY,
    boundary_id TEXT NOT NULL,
    decision_date TEXT,
    problem_boundary TEXT,
    system_boundary TEXT,
    stakeholder_boundary TEXT,
    causal_boundary TEXT,
    temporal_boundary TEXT,
    institutional_boundary TEXT,
    evidence_boundary TEXT,
    ethical_boundary TEXT,
    excluded_scope TEXT,
    revision_triggers TEXT,
    archived_learning TEXT,
    FOREIGN KEY (boundary_id) REFERENCES boundary_frames(boundary_id)
);

CREATE VIEW boundary_quality_scores AS
SELECT
    boundary_id,
    boundary_name,
    frame_type,
    domain,
    ROUND(
      0.12 * problem_clarity +
      0.13 * system_context +
      0.14 * stakeholder_inclusion +
      0.14 * causal_adequacy +
      0.12 * temporal_adequacy +
      0.11 * institutional_responsibility +
      0.11 * evidence_diversity +
      0.10 * ethical_review +
      0.09 * revision_readiness +
      0.04 * actionability,
      4
    ) AS boundary_quality_score
FROM boundary_frames;

CREATE VIEW stakeholder_boundary_scores AS
SELECT
    stakeholder_id,
    boundary_id,
    stakeholder_group,
    role_type,
    ROUND(
      0.18 * affectedness +
      0.15 * knowledge_value +
      0.15 * burden_risk +
      0.14 * trust_sensitivity +
      0.12 * implementation_role -
      0.15 * inclusion_quality -
      0.11 * representation_quality,
      4
    ) AS stakeholder_exclusion_risk
FROM stakeholder_boundaries;

CREATE VIEW causal_boundary_scores AS
SELECT
    cause_id,
    boundary_id,
    causal_frame,
    causal_level,
    ROUND(
      0.13 * causal_plausibility +
      0.12 * evidence_strength +
      0.16 * structural_depth +
      0.11 * actor_adaptation_considered +
      0.14 * feedback_considered +
      0.13 * incentive_considered +
      0.10 * historical_context_considered +
      0.11 * implementation_relevance,
      4
    ) AS causal_quality_score
FROM causal_boundaries;

CREATE VIEW temporal_boundary_scores AS
SELECT
    time_id,
    boundary_id,
    time_horizon,
    review_stage,
    ROUND(
      0.28 * delayed_effect_risk +
      0.22 * (1 - medium_term_signal_quality) +
      0.24 * (1 - long_term_signal_quality) +
      0.14 * (1 - ownership_continuity) +
      0.12 * (1 - revision_cadence_quality),
      4
    ) AS temporal_compression_risk
FROM temporal_boundaries;

CREATE VIEW institutional_boundary_scores AS
SELECT
    institution_id,
    boundary_id,
    institutional_frame,
    ROUND(MAX(0, authority_clarity - consequence_visibility), 4) AS authority_consequence_gap
FROM institutional_boundaries;

CREATE VIEW evidence_boundary_scores AS
SELECT
    evidence_id,
    boundary_id,
    evidence_frame,
    ROUND(
      0.12 * quantitative_quality +
      0.13 * qualitative_quality +
      0.14 * stakeholder_testimony_quality +
      0.12 * prototype_evidence_quality +
      0.12 * scenario_evidence_quality +
      0.11 * expert_judgment_quality +
      0.13 * ethical_reasoning_quality +
      0.13 * interpretation_discipline -
      0.12 * blind_spot_risk,
      4
    ) AS evidence_diversity_score
FROM evidence_boundaries;

CREATE VIEW ethical_boundary_scores AS
SELECT
    ethics_id,
    boundary_id,
    ethical_issue,
    ROUND(
      0.14 * exclusion_risk +
      0.15 * burden_shift_risk -
      0.12 * harm_visibility +
      0.13 * future_consequence_risk +
      0.13 * power_asymmetry -
      0.11 * redress_path_quality -
      0.11 * participation_quality -
      0.11 * accountability_quality,
      4
    ) AS ethical_risk_score
FROM ethical_boundaries;

CREATE VIEW boundary_drift_scores AS
SELECT
    drift_id,
    boundary_id,
    drift_type,
    original_boundary,
    new_boundary,
    ROUND(
      0.12 * scope_change +
      0.12 * stakeholder_change +
      0.14 * metric_change +
      0.13 * responsibility_change +
      0.13 * evidence_change -
      0.14 * explicitness -
      0.10 * evidence_basis +
      0.12 * coherence_risk,
      4
    ) AS boundary_drift_risk
FROM boundary_drift;

CREATE VIEW revision_trigger_scores AS
SELECT
    trigger_id,
    boundary_id,
    trigger_name,
    trigger_type,
    ROUND(
      0.15 * signal_quality +
      0.15 * threshold_clarity +
      0.15 * decision_linkage +
      0.12 * timeliness +
      0.12 * stakeholder_visibility +
      0.13 * governance_owner_clarity +
      0.18 * response_options_quality,
      4
    ) AS trigger_quality_score
FROM revision_triggers;
