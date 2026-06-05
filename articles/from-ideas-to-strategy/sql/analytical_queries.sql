-- Advanced analytical queries for From Ideas to Strategy.

SELECT * FROM strategy_conversion_scores ORDER BY strategy_conversion_score DESC;
SELECT * FROM strategic_fit_scores ORDER BY strategic_fit_score DESC;
SELECT * FROM integration_readiness_scores ORDER BY integration_readiness_score DESC;
SELECT * FROM resource_commitment_scores ORDER BY resource_commitment_score DESC;
SELECT * FROM alignment_coordination_scores ORDER BY alignment_coordination_score DESC;
SELECT * FROM feedback_learning_scores ORDER BY feedback_learning_score DESC;
SELECT * FROM ethics_power_scores ORDER BY power_risk DESC;
SELECT * FROM governance_review_scores ORDER BY governance_score DESC;
SELECT * FROM governance_review_scores ORDER BY governance_score ASC;
SELECT * FROM decision_memory_scores ORDER BY decision_memory_score DESC;
SELECT * FROM decision_memory_scores ORDER BY decision_memory_score ASC;
