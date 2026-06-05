-- Advanced analytical queries for Institutional Memory and Idea Systems.

SELECT * FROM memory_system_scores ORDER BY memory_strength DESC;
SELECT * FROM memory_system_scores ORDER BY memory_failure_risk DESC;
SELECT * FROM idea_lifecycle_scores ORDER BY lifecycle_quality_score ASC;
SELECT * FROM decision_memory_scores ORDER BY decision_memory_score ASC;
SELECT * FROM retrieval_reuse_scores ORDER BY retrieval_reuse_score ASC;
SELECT * FROM learning_update_scores ORDER BY learning_update_score ASC;
SELECT * FROM stewardship_ethics_scores ORDER BY stewardship_score ASC;
SELECT * FROM stewardship_ethics_scores ORDER BY ethical_memory_risk DESC;
