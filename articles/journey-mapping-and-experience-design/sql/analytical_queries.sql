-- Advanced analytical queries for Journey Mapping and Experience Design.

SELECT * FROM journey_profile_scores ORDER BY journey_profile_score DESC;
SELECT * FROM journey_profile_scores ORDER BY redesign_need_score DESC;
SELECT * FROM stage_friction_scores ORDER BY accumulated_friction_score DESC;
SELECT * FROM touchpoint_quality_scores ORDER BY touchpoint_quality_score ASC;
SELECT * FROM transition_risk_scores ORDER BY transition_risk_score DESC;
SELECT access_id, journey_id, access_issue, accessibility_dignity_score, ROUND(1 - accessibility_dignity_score, 4) AS accessibility_dignity_risk
FROM accessibility_dignity_scores
ORDER BY accessibility_dignity_risk DESC;
SELECT * FROM trust_status_scores ORDER BY trust_status_score ASC;
SELECT decision_id, journey_id, stage_id, decision_point, decision_pathway_score, ROUND(1 - decision_pathway_score, 4) AS decision_pathway_risk
FROM decision_pathway_scores
ORDER BY decision_pathway_risk DESC;
SELECT blueprint_id, journey_id, visible_experience, backstage_dependency, service_blueprint_score, ROUND(1 - service_blueprint_score, 4) AS service_blueprint_risk
FROM service_blueprint_scores
ORDER BY service_blueprint_risk DESC;
SELECT * FROM redesign_priority_scores ORDER BY redesign_value_score DESC;
SELECT * FROM measurement_learning_scores ORDER BY measurement_learning_score DESC;
