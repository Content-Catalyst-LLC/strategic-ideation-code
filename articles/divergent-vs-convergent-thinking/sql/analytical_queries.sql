-- Advanced analytical queries for divergence-convergence strategy systems.

-- 1. Strongest process profiles
SELECT *
FROM divergence_convergence_profiles
ORDER BY profile_score DESC;

-- 2. Highest premature convergence risk
SELECT *
FROM premature_convergence_risks
ORDER BY premature_convergence_risk DESC;

-- 3. Highest unbounded divergence risk
SELECT *
FROM unbounded_divergence_risks
ORDER BY unbounded_divergence_risk DESC;

-- 4. Highest-scoring idea portfolio candidates
SELECT *
FROM idea_portfolio_scores
ORDER BY idea_score DESC;

-- 5. Weakest criteria quality
SELECT *
FROM criteria_quality_scores
ORDER BY criteria_quality_score ASC;

-- 6. Weakest selection integrity
SELECT *
FROM selection_integrity_scores
ORDER BY selection_integrity_score ASC;

-- 7. Weakest stakeholder inclusion
SELECT *
FROM stakeholder_inclusion_scores
ORDER BY stakeholder_inclusion_score ASC;

-- 8. Strongest learning cycles
SELECT *
FROM iteration_learning_scores
ORDER BY iteration_learning_score DESC;
