-- Advanced analytical queries for Participatory Ideation and Co-Design.

SELECT * FROM participation_system_profile_scores ORDER BY participation_quality_score DESC;
SELECT * FROM participation_system_profile_scores ORDER BY tokenism_extraction_risk DESC;
SELECT *, ROUND(representation_need - representation_score, 4) AS representation_gap
FROM stakeholder_representation_scores
ORDER BY representation_gap DESC;
SELECT * FROM influence_boundary_scores ORDER BY influence_boundary_score DESC;
SELECT * FROM influence_boundary_scores ORDER BY influence_boundary_score ASC;
SELECT * FROM accessibility_support_scores ORDER BY accessibility_support_score DESC;
SELECT * FROM reciprocity_scores ORDER BY extraction_risk DESC;
SELECT * FROM power_risk_scores ORDER BY power_risk_score DESC;
SELECT * FROM knowledge_integration_scores ORDER BY knowledge_integration_score DESC;
SELECT * FROM conflict_tradeoff_scores ORDER BY conflict_tradeoff_score DESC;
SELECT * FROM decision_traceability_scores ORDER BY decision_traceability_score DESC;
SELECT * FROM accountability_scores ORDER BY accountability_score DESC;
SELECT * FROM accountability_scores ORDER BY accountability_score ASC;
