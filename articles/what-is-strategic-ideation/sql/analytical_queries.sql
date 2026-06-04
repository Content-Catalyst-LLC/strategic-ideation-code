-- Advanced analytical queries for strategic ideation systems.

-- 1. Highest-scoring ideas
SELECT *
FROM idea_weighted_scores
ORDER BY weighted_score DESC;

-- 2. Highest-risk assumptions
SELECT *
FROM assumption_risk_register
ORDER BY assumption_risk DESC;

-- 3. Strongest option architecture
SELECT *
FROM option_architecture_scores
ORDER BY architecture_score DESC;

-- 4. Implementation pathways needing review
SELECT *
FROM implementation_pathway_scores
WHERE pathway_score < 0.55
ORDER BY pathway_score ASC;

-- 5. Evidence strength review
SELECT
    evidence_id,
    idea_id,
    evidence_type,
    ROUND(
      0.34 * evidence_quality +
      0.30 * relevance +
      0.20 * recency -
      0.16 * contestation,
      4
    ) AS evidence_strength,
    source_type,
    evidence_summary
FROM evidence_register
ORDER BY evidence_strength DESC;

-- 6. Prototype plan by review layer
SELECT
    review_layer,
    COUNT(*) AS prototype_count,
    AVG(estimated_weeks) AS avg_weeks
FROM prototype_plan
GROUP BY review_layer
ORDER BY prototype_count DESC;
