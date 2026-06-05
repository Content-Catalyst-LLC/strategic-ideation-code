-- Advanced analytical queries for Empathy and User-Centered Ideation.

SELECT * FROM empathy_profile_scores ORDER BY empathy_profile_score DESC;
SELECT * FROM empathy_profile_scores ORDER BY superficiality_risk DESC;
SELECT * FROM stakeholder_field_scores ORDER BY inclusion_priority_score DESC;
SELECT * FROM observation_quality_scores ORDER BY observation_quality_score DESC;
SELECT * FROM journey_friction_scores ORDER BY accumulated_burden_score DESC;
SELECT * FROM unmet_need_scores ORDER BY unmet_need_priority DESC;
SELECT * FROM preference_behavior_gap_scores ORDER BY preference_behavior_gap_score DESC;
SELECT * FROM reframing_quality_scores ORDER BY reframing_quality_score DESC;
SELECT ethics_id, context_id, ethical_issue, ethical_empathy_score, ROUND(1 - ethical_empathy_score, 4) AS ethical_empathy_risk
FROM ethical_empathy_scores
ORDER BY ethical_empathy_risk DESC;
SELECT * FROM systems_empathy_scores ORDER BY systems_empathy_risk DESC;
SELECT * FROM decision_linkage_scores ORDER BY decision_linkage_score DESC;
