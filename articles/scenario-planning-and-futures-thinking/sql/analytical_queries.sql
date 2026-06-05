-- Advanced analytical queries for Scenario Planning and Futures Thinking.

SELECT * FROM scenario_set_scores ORDER BY scenario_quality_score DESC;
SELECT * FROM scenario_set_scores ORDER BY workshop_theater_risk DESC;
SELECT * FROM driver_uncertainty_scores ORDER BY critical_uncertainty_score DESC;
SELECT * FROM driver_uncertainty_scores ORDER BY watch_priority DESC;
SELECT * FROM strategy_stress_test_scores ORDER BY worst_case DESC;
SELECT * FROM strategy_stress_test_scores ORDER BY worst_case ASC;
SELECT * FROM signal_monitoring_scores ORDER BY response_priority DESC;
SELECT * FROM adaptive_pathway_scores ORDER BY adaptive_pathway_score DESC;
SELECT ethics_id, scenario_set_id, ethical_issue, futures_ethics_score, ROUND(1 - futures_ethics_score, 4) AS futures_ethics_risk
FROM futures_ethics_scores
ORDER BY futures_ethics_risk DESC;
SELECT * FROM scenario_governance_scores ORDER BY scenario_governance_score DESC;
SELECT * FROM scenario_governance_scores ORDER BY scenario_governance_score ASC;
SELECT * FROM scenario_learning_memory_scores ORDER BY scenario_learning_memory_score DESC;
SELECT * FROM scenario_learning_memory_scores ORDER BY scenario_learning_memory_score ASC;
