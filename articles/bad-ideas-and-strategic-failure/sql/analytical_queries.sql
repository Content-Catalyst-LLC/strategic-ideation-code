-- Advanced analytical queries for Bad Ideas and Strategic Failure.

SELECT * FROM bad_idea_risk_scores ORDER BY failure_risk DESC;
SELECT * FROM bad_idea_risk_scores ORDER BY idea_quality DESC;
SELECT * FROM bad_idea_risk_scores ORDER BY power_distortion DESC;
SELECT * FROM failure_pathway_scores ORDER BY failure_pathway_risk DESC;
SELECT * FROM evidence_overclaim_scores ORDER BY overclaim_exposure DESC;
SELECT * FROM implementation_incentive_scores ORDER BY implementation_incentive_risk DESC;
SELECT * FROM power_narrative_learning_scores ORDER BY power_narrative_risk DESC;
