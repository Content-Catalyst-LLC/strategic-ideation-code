-- Advanced analytical queries for Implementation Pathways and Strategic Sequencing.

SELECT * FROM pathway_readiness_scores ORDER BY sequencing_readiness_score DESC;
SELECT * FROM pathway_readiness_scores ORDER BY premature_commitment_risk DESC;
SELECT * FROM dependency_risk_scores ORDER BY dependency_risk_score DESC;
SELECT * FROM capacity_load_scores ORDER BY capacity_load_score DESC;
SELECT * FROM timing_window_scores ORDER BY timing_window_score DESC;
SELECT * FROM reversibility_lockin_scores ORDER BY lockin_risk_score DESC;
SELECT * FROM ethics_power_scores ORDER BY power_risk DESC;
