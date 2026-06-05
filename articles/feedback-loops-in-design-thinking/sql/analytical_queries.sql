-- Advanced analytical queries for Feedback Loops in Design Thinking.

SELECT * FROM feedback_system_profile_scores ORDER BY feedback_profile_score DESC;
SELECT * FROM feedback_system_profile_scores ORDER BY noisy_churn_risk DESC;
SELECT * FROM signal_quality_scores ORDER BY signal_quality_score DESC;
SELECT * FROM signal_quality_scores ORDER BY signal_quality_score ASC;
SELECT * FROM interpretation_capacity_scores ORDER BY interpretation_capacity_score DESC;
SELECT * FROM adjustment_pathway_scores ORDER BY adjustment_pathway_score DESC;
SELECT * FROM user_feedback_scores ORDER BY user_feedback_score DESC;
SELECT * FROM temporal_learning_scores ORDER BY temporal_learning_score DESC;
SELECT * FROM systems_impact_scores ORDER BY systems_impact_risk DESC;
SELECT ethics_id, system_id, ethical_issue, ethical_governance_score, ROUND(1 - ethical_governance_score, 4) AS ethical_governance_risk
FROM ethical_feedback_governance_scores
ORDER BY ethical_governance_risk DESC;
SELECT * FROM decision_linkage_scores ORDER BY decision_linkage_score DESC;
SELECT * FROM feedback_memory_scores ORDER BY feedback_memory_score DESC;
