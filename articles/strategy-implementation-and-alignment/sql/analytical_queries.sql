-- Advanced analytical queries for Strategy Implementation and Alignment.

SELECT * FROM implementation_profile_scores ORDER BY implementation_profile_score DESC;
SELECT * FROM implementation_profile_scores ORDER BY alignment_drift_risk DESC;
SELECT * FROM alignment_dimension_scores ORDER BY alignment_system_score DESC;
SELECT * FROM ethics_power_scores ORDER BY power_risk DESC;
