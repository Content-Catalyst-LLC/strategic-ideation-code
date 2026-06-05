-- Advanced analytical queries for Risk, Tradeoffs, and Strategic Choices.

SELECT * FROM strategic_tradeoff_scores ORDER BY strategic_tradeoff_score DESC;
SELECT * FROM strategic_tradeoff_scores ORDER BY fragility_warning DESC;
SELECT * FROM risk_exposure_scores ORDER BY gross_exposure DESC;
SELECT * FROM opportunity_cost_scores ORDER BY opportunity_cost_score DESC;
SELECT * FROM temporal_tradeoff_scores ORDER BY temporal_risk DESC;
SELECT * FROM scenario_stress_test_scores ORDER BY worst_case ASC;
SELECT * FROM scenario_stress_test_scores ORDER BY mean_performance DESC;
SELECT * FROM lock_in_reversibility_scores ORDER BY lock_in_score DESC;
SELECT * FROM resource_allocation_scores ORDER BY resource_coherence DESC;
SELECT * FROM resource_allocation_scores ORDER BY resource_coherence ASC;
SELECT * FROM value_conflict_scores ORDER BY value_conflict_score DESC;
SELECT * FROM ethical_burden_scores ORDER BY ethical_burden_risk DESC;
SELECT * FROM decision_memory_scores ORDER BY decision_memory_score DESC;
SELECT * FROM decision_memory_scores ORDER BY decision_memory_score ASC;
