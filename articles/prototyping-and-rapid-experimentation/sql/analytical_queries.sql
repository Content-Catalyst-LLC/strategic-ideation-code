-- Advanced analytical queries for Prototyping and Rapid Experimentation.

SELECT * FROM experimentation_profile_scores ORDER BY experimentation_profile_score DESC;
SELECT * FROM experimentation_profile_scores ORDER BY superficial_testing_risk DESC;
SELECT * FROM assumption_priority_scores ORDER BY assumption_priority_score DESC;
SELECT * FROM prototype_fit_scores ORDER BY prototype_fit_score DESC;
SELECT * FROM experiment_quality_scores ORDER BY experiment_quality_score DESC;
SELECT * FROM evidence_quality_scores ORDER BY evidence_quality_score DESC;
SELECT * FROM evidence_quality_scores ORDER BY evidence_quality_score ASC;
SELECT * FROM user_validation_scores ORDER BY user_validation_score DESC;
SELECT * FROM iteration_learning_scores ORDER BY iteration_learning_score DESC;
SELECT * FROM systems_impact_scores ORDER BY systems_impact_risk DESC;
SELECT ethics_id, experiment_id, ethical_issue, ethical_governance_score, ROUND(1 - ethical_governance_score, 4) AS ethical_governance_risk
FROM ethical_governance_scores
ORDER BY ethical_governance_risk DESC;
SELECT * FROM decision_linkage_scores ORDER BY decision_linkage_score DESC;
