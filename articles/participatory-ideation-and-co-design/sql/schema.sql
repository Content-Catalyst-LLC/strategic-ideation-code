-- Advanced SQL schema for Participatory Ideation and Co-Design.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS participation_system_profile_scores;
DROP VIEW IF EXISTS stakeholder_representation_scores;
DROP VIEW IF EXISTS influence_boundary_scores;
DROP VIEW IF EXISTS accessibility_support_scores;
DROP VIEW IF EXISTS reciprocity_scores;
DROP VIEW IF EXISTS power_risk_scores;
DROP VIEW IF EXISTS knowledge_integration_scores;
DROP VIEW IF EXISTS conflict_tradeoff_scores;
DROP VIEW IF EXISTS decision_traceability_scores;
DROP VIEW IF EXISTS accountability_scores;

DROP TABLE IF EXISTS accountability;
DROP TABLE IF EXISTS decision_traceability;
DROP TABLE IF EXISTS conflict_tradeoffs;
DROP TABLE IF EXISTS knowledge_integration;
DROP TABLE IF EXISTS power_risks;
DROP TABLE IF EXISTS reciprocity;
DROP TABLE IF EXISTS accessibility_supports;
DROP TABLE IF EXISTS influence_boundaries;
DROP TABLE IF EXISTS stakeholders;
DROP TABLE IF EXISTS participation_systems;

CREATE TABLE participation_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    organization_type TEXT NOT NULL,
    domain TEXT NOT NULL,
    representation REAL CHECK (representation BETWEEN 0 AND 1),
    influence REAL CHECK (influence BETWEEN 0 AND 1),
    accessibility REAL CHECK (accessibility BETWEEN 0 AND 1),
    reciprocity REAL CHECK (reciprocity BETWEEN 0 AND 1),
    power_awareness REAL CHECK (power_awareness BETWEEN 0 AND 1),
    knowledge_integration REAL CHECK (knowledge_integration BETWEEN 0 AND 1),
    decision_linkage REAL CHECK (decision_linkage BETWEEN 0 AND 1),
    accountability REAL CHECK (accountability BETWEEN 0 AND 1),
    learning_memory REAL CHECK (learning_memory BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE stakeholders (
    stakeholder_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    stakeholder_group TEXT NOT NULL,
    stakeholder_type TEXT NOT NULL,
    affectedness REAL CHECK (affectedness BETWEEN 0 AND 1),
    decision_power REAL CHECK (decision_power BETWEEN 0 AND 1),
    implementation_role REAL CHECK (implementation_role BETWEEN 0 AND 1),
    knowledge_value REAL CHECK (knowledge_value BETWEEN 0 AND 1),
    usual_exclusion_risk REAL CHECK (usual_exclusion_risk BETWEEN 0 AND 1),
    participation_depth REAL CHECK (participation_depth BETWEEN 0 AND 1),
    representation_quality REAL CHECK (representation_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES participation_systems(system_id)
);

CREATE TABLE influence_boundaries (
    boundary_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    participation_purpose TEXT NOT NULL,
    problem_frame_open REAL CHECK (problem_frame_open BETWEEN 0 AND 1),
    idea_generation_open REAL CHECK (idea_generation_open BETWEEN 0 AND 1),
    prototype_open REAL CHECK (prototype_open BETWEEN 0 AND 1),
    evaluation_criteria_open REAL CHECK (evaluation_criteria_open BETWEEN 0 AND 1),
    implementation_open REAL CHECK (implementation_open BETWEEN 0 AND 1),
    governance_open REAL CHECK (governance_open BETWEEN 0 AND 1),
    constraint_transparency REAL CHECK (constraint_transparency BETWEEN 0 AND 1),
    decision_authority_clarity REAL CHECK (decision_authority_clarity BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES participation_systems(system_id)
);

CREATE TABLE accessibility_supports (
    access_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    access_design TEXT NOT NULL,
    language_access REAL CHECK (language_access BETWEEN 0 AND 1),
    disability_access REAL CHECK (disability_access BETWEEN 0 AND 1),
    schedule_flexibility REAL CHECK (schedule_flexibility BETWEEN 0 AND 1),
    technology_access REAL CHECK (technology_access BETWEEN 0 AND 1),
    compensation_support REAL CHECK (compensation_support BETWEEN 0 AND 1),
    care_transport_support REAL CHECK (care_transport_support BETWEEN 0 AND 1),
    psychological_safety REAL CHECK (psychological_safety BETWEEN 0 AND 1),
    cultural_fit REAL CHECK (cultural_fit BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES participation_systems(system_id)
);

CREATE TABLE reciprocity (
    reciprocity_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    participant_labor REAL CHECK (participant_labor BETWEEN 0 AND 1),
    compensation_quality REAL CHECK (compensation_quality BETWEEN 0 AND 1),
    credit_quality REAL CHECK (credit_quality BETWEEN 0 AND 1),
    feedback_return_quality REAL CHECK (feedback_return_quality BETWEEN 0 AND 1),
    capacity_building REAL CHECK (capacity_building BETWEEN 0 AND 1),
    benefit_to_participants REAL CHECK (benefit_to_participants BETWEEN 0 AND 1),
    ongoing_relationship REAL CHECK (ongoing_relationship BETWEEN 0 AND 1),
    extraction_risk_context REAL CHECK (extraction_risk_context BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES participation_systems(system_id)
);

CREATE TABLE power_risks (
    power_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    power_issue TEXT NOT NULL,
    invitation_bias REAL CHECK (invitation_bias BETWEEN 0 AND 1),
    framing_control REAL CHECK (framing_control BETWEEN 0 AND 1),
    language_barrier REAL CHECK (language_barrier BETWEEN 0 AND 1),
    dominant_voice_risk REAL CHECK (dominant_voice_risk BETWEEN 0 AND 1),
    interpretive_capture REAL CHECK (interpretive_capture BETWEEN 0 AND 1),
    decision_capture REAL CHECK (decision_capture BETWEEN 0 AND 1),
    participant_risk REAL CHECK (participant_risk BETWEEN 0 AND 1),
    mitigation_quality REAL CHECK (mitigation_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES participation_systems(system_id)
);

CREATE TABLE knowledge_integration (
    knowledge_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    integration_practice TEXT NOT NULL,
    lived_experience_integration REAL CHECK (lived_experience_integration BETWEEN 0 AND 1),
    technical_expertise_integration REAL CHECK (technical_expertise_integration BETWEEN 0 AND 1),
    operational_knowledge_integration REAL CHECK (operational_knowledge_integration BETWEEN 0 AND 1),
    systems_analysis_integration REAL CHECK (systems_analysis_integration BETWEEN 0 AND 1),
    evidence_quality REAL CHECK (evidence_quality BETWEEN 0 AND 1),
    conflict_visibility REAL CHECK (conflict_visibility BETWEEN 0 AND 1),
    synthesis_traceability REAL CHECK (synthesis_traceability BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES participation_systems(system_id)
);

CREATE TABLE conflict_tradeoffs (
    conflict_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    conflict_type TEXT NOT NULL,
    conflict_visibility REAL CHECK (conflict_visibility BETWEEN 0 AND 1),
    tradeoff_clarity REAL CHECK (tradeoff_clarity BETWEEN 0 AND 1),
    dissent_documentation REAL CHECK (dissent_documentation BETWEEN 0 AND 1),
    burden_shift_review REAL CHECK (burden_shift_review BETWEEN 0 AND 1),
    value_tension_review REAL CHECK (value_tension_review BETWEEN 0 AND 1),
    resolution_transparency REAL CHECK (resolution_transparency BETWEEN 0 AND 1),
    followup_quality REAL CHECK (followup_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES participation_systems(system_id)
);

CREATE TABLE decision_traceability (
    decision_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    decision_type TEXT NOT NULL,
    input_to_decision_clarity REAL CHECK (input_to_decision_clarity BETWEEN 0 AND 1),
    authority_connection REAL CHECK (authority_connection BETWEEN 0 AND 1),
    resource_connection REAL CHECK (resource_connection BETWEEN 0 AND 1),
    revision_trigger_quality REAL CHECK (revision_trigger_quality BETWEEN 0 AND 1),
    implementation_path_quality REAL CHECK (implementation_path_quality BETWEEN 0 AND 1),
    participant_review_quality REAL CHECK (participant_review_quality BETWEEN 0 AND 1),
    decision_rationale_quality REAL CHECK (decision_rationale_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES participation_systems(system_id)
);

CREATE TABLE accountability (
    accountability_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    accountability_practice TEXT NOT NULL,
    close_loop_quality REAL CHECK (close_loop_quality BETWEEN 0 AND 1),
    public_response_quality REAL CHECK (public_response_quality BETWEEN 0 AND 1),
    participant_challenge_path REAL CHECK (participant_challenge_path BETWEEN 0 AND 1),
    implementation_monitoring REAL CHECK (implementation_monitoring BETWEEN 0 AND 1),
    ongoing_governance REAL CHECK (ongoing_governance BETWEEN 0 AND 1),
    learning_memory_quality REAL CHECK (learning_memory_quality BETWEEN 0 AND 1),
    trust_repair_quality REAL CHECK (trust_repair_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (system_id) REFERENCES participation_systems(system_id)
);

CREATE VIEW participation_system_profile_scores AS
SELECT
    system_id,
    system_name,
    ROUND(
      0.13 * representation +
      0.15 * influence +
      0.11 * accessibility +
      0.11 * reciprocity +
      0.13 * power_awareness +
      0.12 * knowledge_integration +
      0.11 * decision_linkage +
      0.10 * accountability +
      0.04 * learning_memory,
      4
    ) AS participation_quality_score,
    ROUND(
      0.16 * (1 - influence) +
      0.14 * (1 - decision_linkage) +
      0.14 * (1 - accountability) +
      0.13 * (1 - reciprocity) +
      0.13 * (1 - power_awareness) +
      0.11 * (1 - representation) +
      0.10 * (1 - accessibility) +
      0.09 * (1 - learning_memory),
      4
    ) AS tokenism_extraction_risk
FROM participation_systems;

CREATE VIEW stakeholder_representation_scores AS
SELECT
    stakeholder_id,
    system_id,
    stakeholder_group,
    stakeholder_type,
    ROUND(
      0.20 * affectedness +
      0.11 * (1 - decision_power) +
      0.12 * implementation_role +
      0.18 * knowledge_value +
      0.16 * usual_exclusion_risk,
      4
    ) AS representation_need,
    ROUND(
      0.55 * participation_depth +
      0.45 * representation_quality,
      4
    ) AS representation_score
FROM stakeholders;

CREATE VIEW influence_boundary_scores AS
SELECT
    boundary_id,
    system_id,
    participation_purpose,
    ROUND(
      0.16 * problem_frame_open +
      0.14 * idea_generation_open +
      0.14 * prototype_open +
      0.13 * evaluation_criteria_open +
      0.11 * implementation_open +
      0.10 * governance_open +
      0.11 * constraint_transparency +
      0.11 * decision_authority_clarity,
      4
    ) AS influence_boundary_score
FROM influence_boundaries;

CREATE VIEW accessibility_support_scores AS
SELECT
    access_id,
    system_id,
    access_design,
    ROUND(
      0.13 * language_access +
      0.14 * disability_access +
      0.12 * schedule_flexibility +
      0.11 * technology_access +
      0.13 * compensation_support +
      0.12 * care_transport_support +
      0.13 * psychological_safety +
      0.12 * cultural_fit,
      4
    ) AS accessibility_support_score
FROM accessibility_supports;

CREATE VIEW reciprocity_scores AS
SELECT
    reciprocity_id,
    system_id,
    ROUND(
      0.16 * compensation_quality +
      0.12 * credit_quality +
      0.16 * feedback_return_quality +
      0.12 * capacity_building +
      0.15 * benefit_to_participants +
      0.14 * ongoing_relationship -
      0.15 * extraction_risk_context,
      4
    ) AS reciprocity_score,
    ROUND(
      0.25 * participant_labor +
      0.18 * extraction_risk_context +
      0.14 * (1 - compensation_quality) +
      0.13 * (1 - feedback_return_quality) +
      0.12 * (1 - benefit_to_participants) +
      0.10 * (1 - ongoing_relationship) +
      0.08 * (1 - credit_quality),
      4
    ) AS extraction_risk
FROM reciprocity;

CREATE VIEW power_risk_scores AS
SELECT
    power_id,
    system_id,
    power_issue,
    ROUND(
      0.13 * invitation_bias +
      0.15 * framing_control +
      0.11 * language_barrier +
      0.13 * dominant_voice_risk +
      0.16 * interpretive_capture +
      0.16 * decision_capture +
      0.10 * participant_risk -
      0.06 * mitigation_quality,
      4
    ) AS power_risk_score
FROM power_risks;

CREATE VIEW knowledge_integration_scores AS
SELECT
    knowledge_id,
    system_id,
    integration_practice,
    ROUND(
      0.15 * lived_experience_integration +
      0.12 * technical_expertise_integration +
      0.13 * operational_knowledge_integration +
      0.14 * systems_analysis_integration +
      0.13 * evidence_quality +
      0.14 * conflict_visibility +
      0.19 * synthesis_traceability,
      4
    ) AS knowledge_integration_score
FROM knowledge_integration;

CREATE VIEW conflict_tradeoff_scores AS
SELECT
    conflict_id,
    system_id,
    conflict_type,
    ROUND(
      0.16 * conflict_visibility +
      0.15 * tradeoff_clarity +
      0.15 * dissent_documentation +
      0.14 * burden_shift_review +
      0.14 * value_tension_review +
      0.13 * resolution_transparency +
      0.13 * followup_quality,
      4
    ) AS conflict_tradeoff_score
FROM conflict_tradeoffs;

CREATE VIEW decision_traceability_scores AS
SELECT
    decision_id,
    system_id,
    decision_type,
    ROUND(
      0.16 * input_to_decision_clarity +
      0.14 * authority_connection +
      0.11 * resource_connection +
      0.13 * revision_trigger_quality +
      0.13 * implementation_path_quality +
      0.15 * participant_review_quality +
      0.18 * decision_rationale_quality,
      4
    ) AS decision_traceability_score
FROM decision_traceability;

CREATE VIEW accountability_scores AS
SELECT
    accountability_id,
    system_id,
    accountability_practice,
    ROUND(
      0.16 * close_loop_quality +
      0.13 * public_response_quality +
      0.12 * participant_challenge_path +
      0.13 * implementation_monitoring +
      0.13 * ongoing_governance +
      0.16 * learning_memory_quality +
      0.17 * trust_repair_quality,
      4
    ) AS accountability_score
FROM accountability;
