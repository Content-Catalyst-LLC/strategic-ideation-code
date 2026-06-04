-- Advanced analytical queries for heuristics in strategic ideation.

-- 1. Strongest heuristic ecologies
SELECT *
FROM heuristic_context_profiles
ORDER BY heuristic_profile_score DESC;

-- 2. Highest premature closure, recognition trap, institutional autopilot, and social proof risks
SELECT *
FROM premature_closure_risks
ORDER BY MAX(closure_pressure, recognition_trap_risk, institutional_autopilot_risk, social_proof_risk) DESC;

-- 3. Strongest deliberate heuristic uses
SELECT *
FROM heuristic_use_scores
ORDER BY heuristic_value_score DESC;

-- 4. Weakest heuristic uses
SELECT *
FROM heuristic_use_scores
ORDER BY heuristic_value_score ASC;

-- 5. Strongest search-breadth contributors
SELECT *
FROM search_breadth_scores
ORDER BY search_breadth_score DESC;

-- 6. Highest institutional shortcut risks
SELECT *
FROM institutional_shortcut_risks
ORDER BY institutional_shortcut_risk DESC;

-- 7. Weakest complexity fit
SELECT *
FROM complexity_fit_scores
ORDER BY complexity_fit_score ASC;

-- 8. Weakest stopping-rule governance
SELECT *
FROM stopping_rule_scores
ORDER BY stopping_rule_quality_score ASC;

-- 9. Highest-value heuristic interventions
SELECT *
FROM intervention_value_scores
ORDER BY intervention_value_score DESC;
