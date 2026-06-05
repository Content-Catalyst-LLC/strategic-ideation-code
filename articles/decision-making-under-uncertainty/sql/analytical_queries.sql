-- Advanced analytical queries for Decision-Making Under Uncertainty.

SELECT * FROM decision_option_scores ORDER BY decision_profile_score DESC;
SELECT * FROM decision_option_scores ORDER BY fragility_risk DESC;
SELECT * FROM uncertainty_classification_scores ORDER BY classification_difficulty DESC;
SELECT * FROM assumption_risk_scores ORDER BY assumption_risk DESC;
SELECT * FROM scenario_stress_test_scores ORDER BY worst_case DESC;
SELECT * FROM scenario_stress_test_scores ORDER BY worst_case ASC;
SELECT * FROM option_value_scores ORDER BY option_value_score DESC;
SELECT * FROM experiment_design_scores ORDER BY experiment_quality DESC;
SELECT * FROM heuristic_bias_scores ORDER BY bias_risk DESC;
SELECT ethics_id, option_id, ethical_issue, ethical_uncertainty_score, ROUND(1 - ethical_uncertainty_score, 4) AS ethical_uncertainty_risk
FROM ethical_uncertainty_scores
ORDER BY ethical_uncertainty_risk DESC;
SELECT * FROM decision_governance_scores ORDER BY decision_governance_score DESC;
SELECT * FROM decision_governance_scores ORDER BY decision_governance_score ASC;
SELECT * FROM decision_learning_memory_scores ORDER BY decision_learning_memory_score DESC;
SELECT * FROM decision_learning_memory_scores ORDER BY decision_learning_memory_score ASC;
