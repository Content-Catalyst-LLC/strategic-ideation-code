-- Advanced analytical queries for Learning Loops in Strategic Execution.

SELECT * FROM learning_loop_scores ORDER BY learning_loop_strength DESC;
SELECT * FROM learning_loop_scores ORDER BY learning_failure_risk DESC;
SELECT * FROM feedback_quality_scores ORDER BY feedback_quality_score DESC;
SELECT * FROM assumption_review_scores ORDER BY assumption_review_score ASC;
SELECT * FROM governance_learning_scores ORDER BY governance_learning_score ASC;
SELECT * FROM knowledge_scaling_scores ORDER BY knowledge_scaling_score ASC;
SELECT * FROM ethics_power_scores ORDER BY learning_power_risk DESC;
