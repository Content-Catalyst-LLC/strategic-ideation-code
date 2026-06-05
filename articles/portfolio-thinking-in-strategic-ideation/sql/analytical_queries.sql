-- Advanced analytical queries for Portfolio Thinking in Strategic Ideation.

SELECT * FROM portfolio_idea_scores ORDER BY portfolio_contribution DESC;
SELECT * FROM portfolio_idea_scores ORDER BY overload_warning DESC;
SELECT role, COUNT(*) AS current_count, ROUND(COUNT(*) * 1.0 / (SELECT COUNT(*) FROM strategic_ideas), 4) AS current_share
FROM strategic_ideas
GROUP BY role
ORDER BY current_share DESC;
SELECT * FROM risk_learning_scores ORDER BY exposure_score DESC;
SELECT * FROM risk_learning_scores ORDER BY learning_strength DESC;
SELECT * FROM capacity_load_scores ORDER BY capacity_load DESC;
SELECT * FROM dependency_sequence_scores ORDER BY sequence_priority DESC;
SELECT * FROM time_horizon_scores ORDER BY future_value DESC;
SELECT * FROM time_horizon_scores ORDER BY present_bias_warning DESC;
SELECT * FROM ethics_power_scores ORDER BY power_risk DESC;
SELECT * FROM governance_review_scores ORDER BY governance_score DESC;
SELECT * FROM governance_review_scores ORDER BY governance_score ASC;
SELECT * FROM decision_memory_scores ORDER BY decision_memory_score DESC;
SELECT * FROM decision_memory_scores ORDER BY decision_memory_score ASC;
