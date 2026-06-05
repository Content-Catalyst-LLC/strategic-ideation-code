-- Advanced analytical queries for Prototype Evidence and Strategic Learning.

SELECT * FROM prototype_system_profile_scores ORDER BY prototype_learning_quality DESC;
SELECT * FROM prototype_system_profile_scores ORDER BY validation_theater_risk DESC;

SELECT *,
       ROUND(criticality * (1 - test_design_score), 4) AS strategic_priority_gap
FROM assumption_evidence_scores
ORDER BY strategic_priority_gap DESC;

SELECT * FROM evidence_quality_scores ORDER BY evidence_quality_score DESC;
SELECT * FROM evidence_quality_scores ORDER BY evidence_quality_score ASC;
SELECT * FROM behavioral_observation_scores ORDER BY behavioral_concern_score DESC;
SELECT * FROM context_realism_scores ORDER BY context_realism_score DESC;
SELECT * FROM systems_impact_scores ORDER BY systems_impact_risk DESC;

SELECT ethics_id, system_id, ethical_issue, ethical_governance_score, ROUND(1 - ethical_governance_score, 4) AS ethical_governance_risk
FROM ethical_prototype_governance_scores
ORDER BY ethical_governance_risk DESC;

SELECT * FROM decision_rule_scores ORDER BY decision_rule_score DESC;
SELECT * FROM decision_rule_scores ORDER BY decision_rule_score ASC;
SELECT * FROM learning_memory_scores ORDER BY learning_memory_score DESC;
SELECT * FROM learning_memory_scores ORDER BY learning_memory_score ASC;
