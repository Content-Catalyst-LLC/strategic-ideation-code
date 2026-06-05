-- Advanced analytical queries for assumption mapping.

-- 1. Highest evidence-adjusted assumption risks
SELECT *
FROM assumption_risk_scores
ORDER BY evidence_adjusted_risk DESC;

-- 2. Weakest evidence
SELECT *
FROM evidence_review_scores
ORDER BY evidence_quality_score ASC;

-- 3. Highest-value tests
SELECT *
FROM test_prioritization_scores
ORDER BY test_value_score DESC;

-- 4. Strongest prototypes for learning
SELECT *
FROM prototype_learning_scores
ORDER BY prototype_learning_score DESC;

-- 5. Highest-risk theory-of-change links
SELECT *
FROM theory_of_change_assumption_scores
ORDER BY theory_link_risk_score DESC;

-- 6. Strongest option confidence
SELECT *
FROM option_confidence_scores
ORDER BY option_confidence_score DESC;

-- 7. Stakeholder assumption risks
SELECT *
FROM stakeholder_assumption_scores
ORDER BY stakeholder_assumption_risk DESC;

-- 8. System response risks
SELECT *
FROM system_response_assumption_scores
ORDER BY system_response_risk DESC;

-- 9. Future assumption risks
SELECT *
FROM future_assumption_scores
ORDER BY future_assumption_risk DESC;

-- 10. Strongest revision triggers
SELECT *
FROM revision_trigger_scores
ORDER BY trigger_quality_score DESC;
