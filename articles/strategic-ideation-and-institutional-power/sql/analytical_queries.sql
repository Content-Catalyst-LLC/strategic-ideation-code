-- Advanced analytical queries for Strategic Ideation and Institutional Power.

SELECT * FROM power_idea_scores ORDER BY power_distortion DESC;
SELECT * FROM power_idea_scores ORDER BY merit_score DESC;
SELECT * FROM agenda_power_scores ORDER BY power_filtered_attention DESC;
SELECT * FROM evidence_parity_scores ORDER BY evidence_parity_score ASC;
SELECT * FROM participation_voice_scores ORDER BY tokenism_risk_score DESC;
SELECT * FROM resource_memory_ai_scores ORDER BY ai_power_risk DESC;
