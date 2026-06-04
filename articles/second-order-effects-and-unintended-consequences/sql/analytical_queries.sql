-- Advanced analytical queries for second-order effects and unintended consequences.

-- 1. Highest second-order risk interventions
SELECT *
FROM second_order_effect_scores
ORDER BY second_order_risk_score DESC;

-- 2. Highest propagation pathway risks
SELECT *
FROM propagation_pathway_scores
ORDER BY pathway_risk_score DESC;

-- 3. Feedback loops and policy resistance
SELECT *
FROM feedback_loop_scores
ORDER BY feedback_risk_score DESC;

-- 4. Adaptive actors likely to change outcomes
SELECT *
FROM adaptive_actor_scores
ORDER BY adaptation_risk_score DESC;

-- 5. Burden shifts requiring review
SELECT *
FROM burden_shift_scores
ORDER BY burden_risk_score DESC;

-- 6. Fragility risks requiring mitigation
SELECT *
FROM fragility_scores
ORDER BY fragility_score DESC;

-- 7. Scenario stress tests with the highest risk
SELECT *
FROM scenario_stress_scores
ORDER BY scenario_risk_score DESC;

-- 8. Strongest early-warning indicators
SELECT *
FROM early_warning_indicator_scores
ORDER BY indicator_quality_score DESC;

-- 9. Learning loops needing repair
SELECT *
FROM learning_loop_scores
ORDER BY learning_quality_score ASC;

-- 10. Highest-value second-order interventions
SELECT *
FROM intervention_value_scores
ORDER BY intervention_value_score DESC;

-- 11. False first-order success risks
SELECT
    intervention_id,
    intervention_name,
    ROUND(
      0.26 * first_order_gain +
      0.20 * long_term_fragility +
      0.16 * delay_risk +
      0.14 * gaming_risk +
      0.12 * burden_shift_risk -
      0.16 * learning_capacity,
      4
    ) AS false_success_risk
FROM interventions
ORDER BY false_success_risk DESC;
