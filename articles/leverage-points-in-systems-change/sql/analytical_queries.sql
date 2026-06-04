-- Advanced analytical queries for leverage points in systems change.

-- 1. Highest leverage candidates
SELECT *
FROM leverage_point_scores
ORDER BY leverage_profile_score DESC;

-- 2. Highest governance needs
SELECT *
FROM governance_need_scores
ORDER BY governance_need_score DESC;

-- 3. Easy but shallow interventions
SELECT
    leverage_id,
    intervention_name,
    leverage_level,
    implementation_ease,
    structural_depth
FROM leverage_points
WHERE implementation_ease >= 0.70 AND structural_depth <= 0.45
ORDER BY implementation_ease DESC;

-- 4. Feedback leverage opportunities
SELECT *
FROM feedback_leverage_scores
ORDER BY feedback_leverage_score DESC;

-- 5. Information-flow leverage opportunities
SELECT *
FROM information_flow_scores
ORDER BY information_value_score DESC;

-- 6. Rule and incentive leverage opportunities
SELECT *
FROM rule_incentive_scores
ORDER BY rule_leverage_score DESC;

-- 7. Operating-goal misalignment priorities
SELECT *
FROM system_goal_scores
ORDER BY goal_change_need_score DESC;

-- 8. Paradigm transition readiness
SELECT *
FROM paradigm_scores
ORDER BY paradigm_transition_readiness DESC;

-- 9. Positive tipping threshold candidates
SELECT *
FROM tipping_threshold_scores
ORDER BY tipping_readiness_score DESC;

-- 10. Strong early-warning indicators
SELECT *
FROM early_warning_indicator_scores
ORDER BY indicator_quality_score DESC;

-- 11. Strongest learning loops
SELECT *
FROM learning_loop_scores
ORDER BY learning_quality_score DESC;
