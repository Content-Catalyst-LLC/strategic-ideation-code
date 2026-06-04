-- Advanced analytical queries for systems thinking in ideation.

-- 1. Highest systems-ideation capacity
SELECT *
FROM systems_ideation_scores
ORDER BY systems_ideation_score DESC;

-- 2. Strongest feedback loops for intervention
SELECT *
FROM feedback_loop_scores
ORDER BY feedback_loop_quality_score DESC;

-- 3. Highest-value leverage points
SELECT *
FROM leverage_point_scores
ORDER BY leverage_value_score DESC;

-- 4. Weakest boundaries
SELECT *
FROM boundary_quality_scores
ORDER BY boundary_quality_score ASC;

-- 5. Highest unintended-consequence risks
SELECT *
FROM consequence_risk_scores
ORDER BY consequence_risk_score DESC;

-- 6. Highest-value intervention portfolio items
SELECT *
FROM intervention_portfolio_scores
ORDER BY portfolio_value_score DESC;

-- 7. Strongest learning loops
SELECT *
FROM learning_loop_scores
ORDER BY learning_quality_score DESC;

-- 8. Highest-value systems-ideation interventions
SELECT *
FROM intervention_value_scores
ORDER BY intervention_value_score DESC;

-- 9. Systems where ideation is probably too symptom-focused
SELECT
    system_id,
    system_name,
    ROUND(
      (1.0 - root_cause_depth) * 0.30 +
      (1.0 - leverage_sensitivity) * 0.25 +
      local_optimization_risk * 0.25 +
      unintended_consequence_risk * 0.20,
      4
    ) AS symptom_focus_risk
FROM systems_profiles
ORDER BY symptom_focus_risk DESC;
