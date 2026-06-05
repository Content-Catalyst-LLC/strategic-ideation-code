-- Advanced SQL schema for Design Thinking Foundations.
-- SQLite-compatible.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS design_capability_scores;
DROP VIEW IF EXISTS stakeholder_inquiry_scores;
DROP VIEW IF EXISTS problem_reframing_scores;
DROP VIEW IF EXISTS idea_portfolio_scores;
DROP VIEW IF EXISTS prototype_learning_scores;
DROP VIEW IF EXISTS test_evidence_scores;
DROP VIEW IF EXISTS systems_design_scores;
DROP VIEW IF EXISTS ethical_design_scores;
DROP VIEW IF EXISTS decision_linkage_scores;
DROP VIEW IF EXISTS institutional_learning_scores;

DROP TABLE IF EXISTS institutional_learning;
DROP TABLE IF EXISTS decision_linkage;
DROP TABLE IF EXISTS ethical_design;
DROP TABLE IF EXISTS systems_design;
DROP TABLE IF EXISTS test_evidence;
DROP TABLE IF EXISTS prototypes;
DROP TABLE IF EXISTS idea_portfolios;
DROP TABLE IF EXISTS problem_frames;
DROP TABLE IF EXISTS stakeholder_inquiry;
DROP TABLE IF EXISTS design_contexts;

CREATE TABLE design_contexts (
    context_id TEXT PRIMARY KEY,
    context_name TEXT NOT NULL,
    organization_type TEXT NOT NULL,
    domain TEXT NOT NULL,
    empathy_depth REAL CHECK (empathy_depth BETWEEN 0 AND 1),
    reframing_capacity REAL CHECK (reframing_capacity BETWEEN 0 AND 1),
    divergence_quality REAL CHECK (divergence_quality BETWEEN 0 AND 1),
    convergence_quality REAL CHECK (convergence_quality BETWEEN 0 AND 1),
    prototyping_strength REAL CHECK (prototyping_strength BETWEEN 0 AND 1),
    testing_quality REAL CHECK (testing_quality BETWEEN 0 AND 1),
    systems_awareness REAL CHECK (systems_awareness BETWEEN 0 AND 1),
    ethical_review REAL CHECK (ethical_review BETWEEN 0 AND 1),
    decision_linkage REAL CHECK (decision_linkage BETWEEN 0 AND 1),
    adaptability REAL CHECK (adaptability BETWEEN 0 AND 1),
    institutional_memory REAL CHECK (institutional_memory BETWEEN 0 AND 1),
    description TEXT
);

CREATE TABLE stakeholder_inquiry (
    inquiry_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    stakeholder_group TEXT NOT NULL,
    inquiry_method TEXT NOT NULL,
    sample_quality REAL CHECK (sample_quality BETWEEN 0 AND 1),
    contextual_depth REAL CHECK (contextual_depth BETWEEN 0 AND 1),
    behavioral_observation REAL CHECK (behavioral_observation BETWEEN 0 AND 1),
    trust_sensitivity REAL CHECK (trust_sensitivity BETWEEN 0 AND 1),
    burden_visibility REAL CHECK (burden_visibility BETWEEN 0 AND 1),
    representation_quality REAL CHECK (representation_quality BETWEEN 0 AND 1),
    interpretation_quality REAL CHECK (interpretation_quality BETWEEN 0 AND 1),
    decision_relevance REAL CHECK (decision_relevance BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES design_contexts(context_id)
);

CREATE TABLE problem_frames (
    frame_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    initial_frame TEXT NOT NULL,
    reframed_problem TEXT NOT NULL,
    frame_source TEXT NOT NULL,
    inquiry_influence REAL CHECK (inquiry_influence BETWEEN 0 AND 1),
    boundary_quality REAL CHECK (boundary_quality BETWEEN 0 AND 1),
    stakeholder_evidence REAL CHECK (stakeholder_evidence BETWEEN 0 AND 1),
    causal_depth REAL CHECK (causal_depth BETWEEN 0 AND 1),
    systems_context REAL CHECK (systems_context BETWEEN 0 AND 1),
    ethical_awareness REAL CHECK (ethical_awareness BETWEEN 0 AND 1),
    decision_usefulness REAL CHECK (decision_usefulness BETWEEN 0 AND 1),
    reframing_maturity REAL CHECK (reframing_maturity BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES design_contexts(context_id)
);

CREATE TABLE idea_portfolios (
    idea_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    idea_name TEXT NOT NULL,
    idea_type TEXT NOT NULL,
    novelty REAL CHECK (novelty BETWEEN 0 AND 1),
    strategic_fit REAL CHECK (strategic_fit BETWEEN 0 AND 1),
    human_centered_fit REAL CHECK (human_centered_fit BETWEEN 0 AND 1),
    feasibility REAL CHECK (feasibility BETWEEN 0 AND 1),
    evidence_strength REAL CHECK (evidence_strength BETWEEN 0 AND 1),
    system_awareness REAL CHECK (system_awareness BETWEEN 0 AND 1),
    ethical_quality REAL CHECK (ethical_quality BETWEEN 0 AND 1),
    learning_value REAL CHECK (learning_value BETWEEN 0 AND 1),
    reversibility REAL CHECK (reversibility BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES design_contexts(context_id)
);

CREATE TABLE prototypes (
    prototype_id TEXT PRIMARY KEY,
    idea_id TEXT NOT NULL,
    context_id TEXT NOT NULL,
    prototype_name TEXT NOT NULL,
    prototype_type TEXT NOT NULL,
    assumption_tested TEXT NOT NULL,
    prototype_fidelity REAL CHECK (prototype_fidelity BETWEEN 0 AND 1),
    learning_potential REAL CHECK (learning_potential BETWEEN 0 AND 1),
    test_speed REAL CHECK (test_speed BETWEEN 0 AND 1),
    stakeholder_inclusion REAL CHECK (stakeholder_inclusion BETWEEN 0 AND 1),
    realism REAL CHECK (realism BETWEEN 0 AND 1),
    system_signal_quality REAL CHECK (system_signal_quality BETWEEN 0 AND 1),
    ethical_safety REAL CHECK (ethical_safety BETWEEN 0 AND 1),
    cost_efficiency REAL CHECK (cost_efficiency BETWEEN 0 AND 1),
    decision_usefulness REAL CHECK (decision_usefulness BETWEEN 0 AND 1),
    success_threshold REAL CHECK (success_threshold BETWEEN 0 AND 1),
    decision_if_failed TEXT,
    FOREIGN KEY (idea_id) REFERENCES idea_portfolios(idea_id),
    FOREIGN KEY (context_id) REFERENCES design_contexts(context_id)
);

CREATE TABLE test_evidence (
    test_id TEXT PRIMARY KEY,
    prototype_id TEXT NOT NULL,
    context_id TEXT NOT NULL,
    test_method TEXT NOT NULL,
    evidence_type TEXT NOT NULL,
    reliability REAL CHECK (reliability BETWEEN 0 AND 1),
    relevance REAL CHECK (relevance BETWEEN 0 AND 1),
    transferability REAL CHECK (transferability BETWEEN 0 AND 1),
    behavioral_signal REAL CHECK (behavioral_signal BETWEEN 0 AND 1),
    stakeholder_signal REAL CHECK (stakeholder_signal BETWEEN 0 AND 1),
    implementation_signal REAL CHECK (implementation_signal BETWEEN 0 AND 1),
    system_signal REAL CHECK (system_signal BETWEEN 0 AND 1),
    bias_risk REAL CHECK (bias_risk BETWEEN 0 AND 1),
    interpretation_quality REAL CHECK (interpretation_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (prototype_id) REFERENCES prototypes(prototype_id),
    FOREIGN KEY (context_id) REFERENCES design_contexts(context_id)
);

CREATE TABLE systems_design (
    system_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    design_issue TEXT NOT NULL,
    feedback_risk REAL CHECK (feedback_risk BETWEEN 0 AND 1),
    delay_risk REAL CHECK (delay_risk BETWEEN 0 AND 1),
    burden_shift_risk REAL CHECK (burden_shift_risk BETWEEN 0 AND 1),
    incentive_misalignment REAL CHECK (incentive_misalignment BETWEEN 0 AND 1),
    metric_gaming_risk REAL CHECK (metric_gaming_risk BETWEEN 0 AND 1),
    context_dependency REAL CHECK (context_dependency BETWEEN 0 AND 1),
    leverage_relevance REAL CHECK (leverage_relevance BETWEEN 0 AND 1),
    monitoring_quality REAL CHECK (monitoring_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES design_contexts(context_id)
);

CREATE TABLE ethical_design (
    ethics_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    ethical_issue TEXT NOT NULL,
    participation_quality REAL CHECK (participation_quality BETWEEN 0 AND 1),
    power_awareness REAL CHECK (power_awareness BETWEEN 0 AND 1),
    burden_visibility REAL CHECK (burden_visibility BETWEEN 0 AND 1),
    consent_quality REAL CHECK (consent_quality BETWEEN 0 AND 1),
    representation_quality REAL CHECK (representation_quality BETWEEN 0 AND 1),
    redress_quality REAL CHECK (redress_quality BETWEEN 0 AND 1),
    decision_traceability REAL CHECK (decision_traceability BETWEEN 0 AND 1),
    harm_monitoring REAL CHECK (harm_monitoring BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES design_contexts(context_id)
);

CREATE TABLE decision_linkage (
    decision_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    design_artifact TEXT NOT NULL,
    decision_type TEXT NOT NULL,
    artifact_quality REAL CHECK (artifact_quality BETWEEN 0 AND 1),
    evidence_quality REAL CHECK (evidence_quality BETWEEN 0 AND 1),
    decision_relevance REAL CHECK (decision_relevance BETWEEN 0 AND 1),
    authority_connection REAL CHECK (authority_connection BETWEEN 0 AND 1),
    resource_connection REAL CHECK (resource_connection BETWEEN 0 AND 1),
    revision_trigger_quality REAL CHECK (revision_trigger_quality BETWEEN 0 AND 1),
    learning_memory_quality REAL CHECK (learning_memory_quality BETWEEN 0 AND 1),
    implementation_path_quality REAL CHECK (implementation_path_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES design_contexts(context_id)
);

CREATE TABLE institutional_learning (
    learning_id TEXT PRIMARY KEY,
    context_id TEXT NOT NULL,
    learning_system TEXT NOT NULL,
    observation_quality REAL CHECK (observation_quality BETWEEN 0 AND 1),
    frame_revision_quality REAL CHECK (frame_revision_quality BETWEEN 0 AND 1),
    prototype_record_quality REAL CHECK (prototype_record_quality BETWEEN 0 AND 1),
    test_record_quality REAL CHECK (test_record_quality BETWEEN 0 AND 1),
    decision_memory_quality REAL CHECK (decision_memory_quality BETWEEN 0 AND 1),
    reuse_quality REAL CHECK (reuse_quality BETWEEN 0 AND 1),
    governance_review_quality REAL CHECK (governance_review_quality BETWEEN 0 AND 1),
    adaptation_quality REAL CHECK (adaptation_quality BETWEEN 0 AND 1),
    review_action TEXT,
    FOREIGN KEY (context_id) REFERENCES design_contexts(context_id)
);

CREATE VIEW design_capability_scores AS
SELECT
    context_id,
    context_name,
    organization_type,
    domain,
    ROUND(
      0.12 * empathy_depth +
      0.13 * reframing_capacity +
      0.10 * divergence_quality +
      0.10 * convergence_quality +
      0.12 * prototyping_strength +
      0.12 * testing_quality +
      0.11 * systems_awareness +
      0.10 * ethical_review +
      0.10 * decision_linkage +
      0.06 * adaptability +
      0.04 * institutional_memory,
      4
    ) AS design_capability_score,
    ROUND(
      0.18 * (1 - empathy_depth) +
      0.14 * (1 - reframing_capacity) +
      0.12 * (1 - testing_quality) +
      0.12 * (1 - systems_awareness) +
      0.12 * (1 - ethical_review) +
      0.16 * (1 - decision_linkage) +
      0.10 * (1 - institutional_memory) +
      0.06 * (1 - adaptability),
      4
    ) AS superficiality_risk
FROM design_contexts;

CREATE VIEW stakeholder_inquiry_scores AS
SELECT
    inquiry_id,
    context_id,
    stakeholder_group,
    inquiry_method,
    ROUND(
      0.13 * sample_quality +
      0.16 * contextual_depth +
      0.14 * behavioral_observation +
      0.11 * trust_sensitivity +
      0.12 * burden_visibility +
      0.12 * representation_quality +
      0.12 * interpretation_quality +
      0.10 * decision_relevance,
      4
    ) AS inquiry_quality_score
FROM stakeholder_inquiry;

CREATE VIEW problem_reframing_scores AS
SELECT
    frame_id,
    context_id,
    initial_frame,
    reframed_problem,
    ROUND(
      0.14 * inquiry_influence +
      0.12 * boundary_quality +
      0.13 * stakeholder_evidence +
      0.14 * causal_depth +
      0.13 * systems_context +
      0.12 * ethical_awareness +
      0.10 * decision_usefulness +
      0.12 * reframing_maturity,
      4
    ) AS reframing_quality_score
FROM problem_frames;

CREATE VIEW idea_portfolio_scores AS
SELECT
    idea_id,
    context_id,
    idea_name,
    idea_type,
    ROUND(
      0.10 * novelty +
      0.14 * strategic_fit +
      0.14 * human_centered_fit +
      0.10 * feasibility +
      0.12 * evidence_strength +
      0.12 * system_awareness +
      0.12 * ethical_quality +
      0.10 * learning_value +
      0.06 * reversibility,
      4
    ) AS idea_quality_score
FROM idea_portfolios;

CREATE VIEW prototype_learning_scores AS
SELECT
    prototype_id,
    idea_id,
    context_id,
    prototype_name,
    prototype_type,
    ROUND(
      0.08 * prototype_fidelity +
      0.16 * learning_potential +
      0.10 * test_speed +
      0.12 * stakeholder_inclusion +
      0.12 * realism +
      0.12 * system_signal_quality +
      0.11 * ethical_safety +
      0.08 * cost_efficiency +
      0.11 * decision_usefulness,
      4
    ) AS prototype_learning_score
FROM prototypes;

CREATE VIEW test_evidence_scores AS
SELECT
    test_id,
    prototype_id,
    context_id,
    test_method,
    evidence_type,
    ROUND(
      0.13 * reliability +
      0.17 * relevance +
      0.11 * transferability +
      0.13 * behavioral_signal +
      0.12 * stakeholder_signal +
      0.10 * implementation_signal +
      0.10 * system_signal -
      0.08 * bias_risk +
      0.12 * interpretation_quality,
      4
    ) AS evidence_quality_score
FROM test_evidence;

CREATE VIEW systems_design_scores AS
SELECT
    system_id,
    context_id,
    design_issue,
    ROUND(
      0.14 * feedback_risk +
      0.11 * delay_risk +
      0.16 * burden_shift_risk +
      0.14 * incentive_misalignment +
      0.12 * metric_gaming_risk +
      0.12 * context_dependency +
      0.11 * leverage_relevance -
      0.10 * monitoring_quality,
      4
    ) AS systems_design_risk
FROM systems_design;

CREATE VIEW ethical_design_scores AS
SELECT
    ethics_id,
    context_id,
    ethical_issue,
    ROUND(
      0.13 * participation_quality +
      0.14 * power_awareness +
      0.13 * burden_visibility +
      0.11 * consent_quality +
      0.12 * representation_quality +
      0.12 * redress_quality +
      0.13 * decision_traceability +
      0.12 * harm_monitoring,
      4
    ) AS ethical_design_score
FROM ethical_design;

CREATE VIEW decision_linkage_scores AS
SELECT
    decision_id,
    context_id,
    design_artifact,
    decision_type,
    ROUND(
      0.12 * artifact_quality +
      0.14 * evidence_quality +
      0.15 * decision_relevance +
      0.15 * authority_connection +
      0.11 * resource_connection +
      0.12 * revision_trigger_quality +
      0.10 * learning_memory_quality +
      0.11 * implementation_path_quality,
      4
    ) AS decision_linkage_score
FROM decision_linkage;

CREATE VIEW institutional_learning_scores AS
SELECT
    learning_id,
    context_id,
    learning_system,
    ROUND(
      0.12 * observation_quality +
      0.13 * frame_revision_quality +
      0.12 * prototype_record_quality +
      0.12 * test_record_quality +
      0.13 * decision_memory_quality +
      0.12 * reuse_quality +
      0.13 * governance_review_quality +
      0.13 * adaptation_quality,
      4
    ) AS institutional_learning_score
FROM institutional_learning;
