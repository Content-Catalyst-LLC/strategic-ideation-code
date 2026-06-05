-- Advanced analytical queries for Alignment Drift and Strategic Coherence.

SELECT * FROM coherence_scores ORDER BY strategic_coherence_score DESC;
SELECT * FROM coherence_scores ORDER BY alignment_drift_risk DESC;
SELECT * FROM drift_signal_scores ORDER BY drift_signal_risk DESC;
SELECT * FROM resource_alignment_scores ORDER BY resource_alignment_score ASC;
SELECT * FROM incentive_metric_scores ORDER BY metric_distortion_risk DESC;
SELECT * FROM governance_strength_scores ORDER BY governance_strength_score ASC;
SELECT * FROM ethics_power_scores ORDER BY power_risk DESC;
