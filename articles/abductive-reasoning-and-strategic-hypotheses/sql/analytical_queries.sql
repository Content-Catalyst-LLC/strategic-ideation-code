-- Advanced analytical queries for abductive reasoning and strategic hypotheses.

-- 1. Highest-value strategic hypotheses
SELECT *
FROM hypothesis_value_scores
ORDER BY hypothesis_value_score DESC;

-- 2. Highest-value evidence pathways
SELECT *
FROM evidence_pathway_scores
ORDER BY evidence_value_score DESC;

-- 3. Strongest disconfirmation tests
SELECT *
FROM disconfirmation_scores
ORDER BY disconfirmation_quality_score DESC;

-- 4. Strongest commitment readiness
SELECT *
FROM commitment_readiness_scores
ORDER BY commitment_readiness_score DESC;

-- 5. Strongest revision triggers
SELECT *
FROM revision_trigger_scores
ORDER BY revision_quality_score DESC;

-- 6. Highest-value portfolio hypotheses
SELECT *
FROM hypothesis_portfolio_scores
ORDER BY portfolio_value_score DESC;

-- 7. Highest-value abductive reasoning interventions
SELECT *
FROM intervention_value_scores
ORDER BY intervention_value_score DESC;

-- 8. Observations with too few rival hypotheses
SELECT
    o.observation_id,
    o.observation_name,
    COUNT(h.hypothesis_id) AS hypothesis_count
FROM observations o
LEFT JOIN hypotheses h ON o.observation_id = h.observation_id
GROUP BY o.observation_id, o.observation_name
HAVING COUNT(h.hypothesis_id) < 2;
