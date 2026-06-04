-- Advanced analytical queries for imagination, discipline, and strategic creativity.

-- 1. Highest strategic creativity scores
SELECT *
FROM strategic_creativity_scores
ORDER BY strategic_creativity_score DESC;

-- 2. Highest novelty-theater risks
SELECT *
FROM novelty_depth_scores
ORDER BY novelty_theater_risk DESC;

-- 3. Highest dead-constraint risks
SELECT *
FROM constraint_scores
ORDER BY dead_constraint_risk DESC;

-- 4. Strongest stakeholder grounding
SELECT *
FROM stakeholder_grounding_scores
ORDER BY stakeholder_grounding_score DESC;

-- 5. Weakest stakeholder grounding
SELECT *
FROM stakeholder_grounding_scores
ORDER BY stakeholder_grounding_score ASC;

-- 6. Strongest systems fit
SELECT *
FROM systems_fit_scores
ORDER BY systems_fit_score DESC;

-- 7. Weakest systems fit
SELECT *
FROM systems_fit_scores
ORDER BY systems_fit_score ASC;

-- 8. Strongest evidence pathways
SELECT *
FROM evidence_pathway_scores
ORDER BY evidence_value_score DESC;

-- 9. Ideas most ready for maturation
SELECT *
FROM idea_maturation_scores
ORDER BY maturation_score DESC;

-- 10. Highest-value creative portfolio items
SELECT *
FROM creative_portfolio_scores
ORDER BY portfolio_value_score DESC;

-- 11. Highest-value interventions
SELECT *
FROM intervention_value_scores
ORDER BY intervention_value_score DESC;
