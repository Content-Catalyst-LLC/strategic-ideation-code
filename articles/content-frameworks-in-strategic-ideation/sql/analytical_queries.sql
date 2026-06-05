-- Advanced analytical queries for Content Frameworks in Strategic Ideation.

SELECT * FROM framework_scores ORDER BY framework_strength DESC;
SELECT * FROM framework_scores ORDER BY framework_risk DESC;
SELECT * FROM component_reuse_scores ORDER BY component_reuse_score DESC;
SELECT * FROM framework_component_scores ORDER BY framework_component_score ASC;
SELECT * FROM decision_support_scores ORDER BY decision_support_score ASC;
SELECT * FROM narrative_coherence_scores ORDER BY narrative_coherence_score ASC;
SELECT * FROM governance_ethics_scores ORDER BY framework_stewardship_score ASC;
SELECT * FROM governance_ethics_scores ORDER BY ethical_framework_risk DESC;
