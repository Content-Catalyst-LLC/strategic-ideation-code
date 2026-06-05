-- Advanced analytical queries for Opportunity Recognition and Evaluation.

SELECT * FROM opportunity_profile_scores ORDER BY profile_score DESC;
SELECT * FROM opportunity_profile_scores ORDER BY confidence_adjusted_score DESC;
SELECT * FROM signal_quality_scores ORDER BY signal_quality_score DESC;
SELECT * FROM capability_alignment_scores ORDER BY capability_score DESC;
SELECT * FROM timing_window_scores ORDER BY timing_strength DESC;
SELECT * FROM risk_and_error_scores ORDER BY false_positive_risk DESC;
SELECT * FROM risk_and_error_scores ORDER BY missed_opportunity_risk DESC;
SELECT * FROM ethics_power_scores ORDER BY power_risk DESC;
SELECT * FROM learning_pathway_scores ORDER BY learning_pathway_score DESC;
SELECT * FROM governance_review_scores ORDER BY governance_score DESC;
SELECT * FROM governance_review_scores ORDER BY governance_score ASC;
SELECT * FROM decision_memory_scores ORDER BY decision_memory_score DESC;
SELECT * FROM decision_memory_scores ORDER BY decision_memory_score ASC;
