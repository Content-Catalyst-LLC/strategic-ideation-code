-- Advanced analytical queries for Design Thinking Foundations.

-- 1. Strongest design thinking capability profiles
SELECT *
FROM design_capability_scores
ORDER BY design_capability_score DESC;

-- 2. Highest superficiality risks
SELECT *
FROM design_capability_scores
ORDER BY superficiality_risk DESC;

-- 3. Strongest stakeholder inquiry
SELECT *
FROM stakeholder_inquiry_scores
ORDER BY inquiry_quality_score DESC;

-- 4. Strongest problem reframing
SELECT *
FROM problem_reframing_scores
ORDER BY reframing_quality_score DESC;

-- 5. Strongest idea candidates
SELECT *
FROM idea_portfolio_scores
ORDER BY idea_quality_score DESC;

-- 6. Strongest prototype learning candidates
SELECT *
FROM prototype_learning_scores
ORDER BY prototype_learning_score DESC;

-- 7. Strongest test evidence
SELECT *
FROM test_evidence_scores
ORDER BY evidence_quality_score DESC;

-- 8. Highest systems design risks
SELECT *
FROM systems_design_scores
ORDER BY systems_design_risk DESC;

-- 9. Strongest ethical design scores
SELECT *
FROM ethical_design_scores
ORDER BY ethical_design_score DESC;

-- 10. Strongest decision linkage
SELECT *
FROM decision_linkage_scores
ORDER BY decision_linkage_score DESC;

-- 11. Strongest institutional learning systems
SELECT *
FROM institutional_learning_scores
ORDER BY institutional_learning_score DESC;
