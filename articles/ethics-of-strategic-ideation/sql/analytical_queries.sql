-- Advanced analytical queries for Ethics of Strategic Ideation.

SELECT * FROM ethical_idea_scores ORDER BY ethical_legitimacy DESC;
SELECT * FROM ethical_idea_scores ORDER BY ethical_risk DESC;
SELECT * FROM stakeholder_impact_scores ORDER BY burden_risk DESC;
SELECT * FROM claim_evidence_ethics_scores ORDER BY claim_evidence_ethics_score ASC;
SELECT * FROM ai_ethics_scores ORDER BY ai_ethics_governance_score ASC;
SELECT * FROM accountability_redress_scores ORDER BY accountability_redress_score ASC;
