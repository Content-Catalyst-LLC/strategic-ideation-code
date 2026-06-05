-- Advanced analytical queries for Knowledge Architecture in Strategic Ideation.

SELECT * FROM idea_architecture_scores ORDER BY architecture_strength DESC;
SELECT * FROM idea_architecture_scores ORDER BY architecture_risk DESC;
SELECT * FROM evidence_assumption_scores ORDER BY evidence_assumption_score ASC;
SELECT * FROM relationship_mapping_scores ORDER BY relationship_mapping_score DESC;
SELECT * FROM retrieval_reuse_scores ORDER BY retrieval_reuse_score ASC;
SELECT * FROM stewardship_ethics_scores ORDER BY stewardship_score ASC;
SELECT * FROM stewardship_ethics_scores ORDER BY ethical_knowledge_risk DESC;
