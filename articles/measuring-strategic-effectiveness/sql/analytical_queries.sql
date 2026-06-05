-- Advanced analytical queries for Measuring Strategic Effectiveness.

SELECT * FROM strategic_effectiveness_scores ORDER BY strategic_effectiveness_score DESC;
SELECT * FROM strategic_effectiveness_scores ORDER BY confidence_adjusted_effectiveness DESC;
SELECT * FROM indicator_quality_scores ORDER BY indicator_quality_score DESC;
SELECT * FROM evidence_confidence_scores ORDER BY evidence_confidence_score DESC;
SELECT * FROM feedback_learning_scores ORDER BY feedback_learning_score DESC;
SELECT * FROM ethics_power_scores ORDER BY power_risk DESC;
