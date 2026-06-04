-- Advanced analytical queries for conceptual clarity systems.

-- 1. Weakest conceptual clarity scores
SELECT *
FROM conceptual_clarity_scores
ORDER BY clarity_score ASC;

-- 2. Highest metric proxy-failure risk
SELECT *
FROM metric_proxy_risk_scores
ORDER BY proxy_failure_risk DESC;

-- 3. Highest conceptual drift priorities
SELECT *
FROM conceptual_drift_priorities
ORDER BY drift_priority DESC;

-- 4. Weakest governance scores
SELECT *
FROM concept_governance_scores
ORDER BY governance_strength ASC;

-- 5. Highest distinction risks
SELECT *
FROM distinction_risk_scores
ORDER BY distinction_risk DESC;

-- 6. Concepts with high decision relevance
SELECT
    concept_id,
    decision_context,
    ROUND(
      0.26 * decision_relevance +
      0.20 * resource_allocation_effect +
      0.18 * role_clarity_effect +
      0.20 * tradeoff_visibility +
      0.16 * escalation_need,
      4
    ) AS decision_power
FROM decision_implications
ORDER BY decision_power DESC;
