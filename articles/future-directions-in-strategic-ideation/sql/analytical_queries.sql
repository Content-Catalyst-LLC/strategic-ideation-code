-- Advanced analytical queries for Future Directions in Strategic Ideation.

SELECT * FROM future_ready_idea_scores ORDER BY future_ready_score DESC;
SELECT * FROM future_ready_idea_scores ORDER BY future_risk DESC;
SELECT * FROM scenario_option_scores ORDER BY scenario_option_score DESC;
SELECT * FROM scenario_option_scores ORDER BY scenario_risk DESC;
SELECT * FROM ai_governance_scores ORDER BY ai_risk DESC;
SELECT * FROM collective_intelligence_scores ORDER BY collective_intelligence_score DESC;
SELECT * FROM learning_memory_scores ORDER BY learning_memory_score DESC;
