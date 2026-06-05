-- Advanced analytical queries for theory of change and strategic logic.

-- 1. Strongest strategic logic
SELECT *
FROM strategic_logic_scores
ORDER BY strategic_logic_score DESC;

-- 2. Highest-risk theory-of-change links
SELECT *
FROM theory_link_risk_scores
ORDER BY link_risk_score DESC;

-- 3. Load-bearing assumption risks
SELECT *
FROM assumption_link_scores
ORDER BY assumption_risk_score DESC;

-- 4. Weak evidence matches
SELECT *
FROM evidence_match_scores
ORDER BY evidence_match_score ASC;

-- 5. Actor response risks
SELECT *
FROM actor_response_scores
ORDER BY actor_response_risk DESC;

-- 6. System feedback risks
SELECT *
FROM system_feedback_scores
ORDER BY feedback_risk_score DESC;

-- 7. Weak outcome sequence areas
SELECT *
FROM outcome_sequence_scores
ORDER BY outcome_sequence_quality ASC;

-- 8. Strongest prototype tests
SELECT *
FROM prototype_test_scores
ORDER BY prototype_test_score DESC;

-- 9. Strongest implementation learning loops
SELECT *
FROM implementation_learning_scores
ORDER BY learning_loop_quality DESC;

-- 10. Strongest revision triggers
SELECT *
FROM revision_trigger_scores
ORDER BY trigger_quality_score DESC;
