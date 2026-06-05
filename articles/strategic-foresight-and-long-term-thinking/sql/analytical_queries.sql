-- Advanced analytical queries for Strategic Foresight and Long-Term Thinking.

SELECT * FROM foresight_profile_scores ORDER BY future_viability_score DESC;
SELECT * FROM foresight_profile_scores ORDER BY short_term_bias DESC;
SELECT * FROM horizon_signal_scores ORDER BY response_priority DESC;
SELECT * FROM driver_uncertainty_scores ORDER BY critical_uncertainty_score DESC;
SELECT * FROM strategy_stress_test_scores ORDER BY worst_case DESC;
SELECT * FROM strategy_stress_test_scores ORDER BY worst_case ASC;
SELECT * FROM path_dependence_scores ORDER BY lock_in_risk DESC;
SELECT * FROM adaptive_pathway_scores ORDER BY adaptive_pathway_score DESC;
SELECT * FROM adaptive_pathway_scores ORDER BY adaptive_pathway_score ASC;
SELECT * FROM anticipatory_governance_scores ORDER BY anticipatory_governance_score DESC;
SELECT * FROM anticipatory_governance_scores ORDER BY anticipatory_governance_score ASC;
SELECT ethics_id, profile_id, ethical_issue, futures_ethics_score, ROUND(1 - futures_ethics_score, 4) AS futures_ethics_risk
FROM futures_ethics_scores
ORDER BY futures_ethics_risk DESC;
SELECT * FROM foresight_learning_memory_scores ORDER BY foresight_learning_memory_score DESC;
SELECT * FROM foresight_learning_memory_scores ORDER BY foresight_learning_memory_score ASC;
