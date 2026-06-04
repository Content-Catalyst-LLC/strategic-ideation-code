-- Advanced analytical queries for complex systems and strategic uncertainty.

-- 1. Most complex environments
SELECT *
FROM complexity_profile_scores
ORDER BY complexity_profile_score DESC;

-- 2. Highest structural uncertainty drivers
SELECT *
FROM uncertainty_driver_scores
ORDER BY uncertainty_intensity_score DESC;

-- 3. Feedback loops requiring attention
SELECT *
FROM feedback_loop_scores
ORDER BY feedback_risk_score DESC;

-- 4. Adaptive actors most likely to change system behavior
SELECT *
FROM adaptive_actor_scores
ORDER BY adaptation_risk_score DESC;

-- 5. Highest path-dependence and lock-in risks
SELECT *
FROM path_dependence_scores
ORDER BY lock_in_risk_score DESC;

-- 6. Scenarios with the largest strategic risk
SELECT *
FROM scenario_risk_scores
ORDER BY scenario_risk_score DESC;

-- 7. Highest-value adaptive options
SELECT *
FROM adaptive_option_scores
ORDER BY adaptive_option_value_score DESC;

-- 8. Strongest early-warning indicators
SELECT *
FROM early_warning_indicator_scores
ORDER BY indicator_quality_score DESC;

-- 9. Learning loops needing repair
SELECT *
FROM learning_loop_scores
ORDER BY learning_quality_score ASC;

-- 10. Highest-value complexity strategy interventions
SELECT *
FROM intervention_value_scores
ORDER BY intervention_value_score DESC;

-- 11. Environments where linear planning is likely fragile
SELECT
    environment_id,
    environment_name,
    ROUND(
      0.20 * nonlinearity +
      0.20 * feedback_intensity +
      0.18 * adaptation_pressure +
      0.16 * deep_uncertainty +
      0.14 * boundary_ambiguity +
      0.12 * emergence_potential,
      4
    ) AS linear_planning_risk
FROM complexity_environments
ORDER BY linear_planning_risk DESC;
