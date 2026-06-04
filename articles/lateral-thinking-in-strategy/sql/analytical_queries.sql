-- Advanced analytical queries for lateral thinking in strategy.

-- 1. Strongest lateral context profiles
SELECT *
FROM lateral_context_profiles
ORDER BY lateral_profile_score DESC;

-- 2. Highest frame rigidity, drift, legitimacy, and political-safety risks
SELECT *
FROM frame_rigidity_risks
ORDER BY MAX(frame_rigidity_risk, drift_risk, legitimacy_gap, political_safety_gap) DESC;

-- 3. Weakest dominant frames
SELECT *
FROM dominant_frame_scores
ORDER BY frame_quality_score ASC;

-- 4. Highest-priority assumptions to challenge
SELECT *
FROM assumption_challenge_priorities
ORDER BY challenge_priority DESC;

-- 5. Strongest lateral moves
SELECT *
FROM lateral_move_scores
ORDER BY lateral_move_score DESC;

-- 6. Strongest reframed problems
SELECT *
FROM reframed_problem_scores
ORDER BY reframe_quality_score DESC;

-- 7. Strongest convergence integration scores
SELECT *
FROM convergence_integration_scores
ORDER BY convergence_integration_score DESC;

-- 8. Weakest stakeholder legitimacy scores
SELECT *
FROM stakeholder_legitimacy_scores
ORDER BY stakeholder_legitimacy_score ASC;
