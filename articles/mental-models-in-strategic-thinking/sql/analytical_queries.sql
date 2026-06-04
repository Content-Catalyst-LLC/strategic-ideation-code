-- Advanced analytical queries for mental-model strategy analysis.

-- 1. Highest adaptive model scores
SELECT *
FROM mental_model_profile_scores
ORDER BY adaptive_model_score DESC;

-- 2. Weakest causal frames
SELECT *
FROM causal_frame_scores
ORDER BY causal_adequacy_score ASC;

-- 3. Institutional artifacts with highest model lock-in
SELECT *
FROM artifact_lock_in_scores
ORDER BY lock_in_risk DESC;

-- 4. Evidence events requiring revision
SELECT *
FROM evidence_revision_priorities
ORDER BY revision_priority DESC;

-- 5. Scenario stress-test results
SELECT *
FROM scenario_stress_scores
ORDER BY stress_score ASC;

-- 6. Highest-priority audit gaps
SELECT
    audit_id,
    model_id,
    audit_dimension,
    audit_question,
    current_score,
    desired_score,
    ROUND(desired_score - current_score, 4) AS revision_gap,
    priority,
    review_method
FROM model_audit_items
ORDER BY revision_gap DESC;
