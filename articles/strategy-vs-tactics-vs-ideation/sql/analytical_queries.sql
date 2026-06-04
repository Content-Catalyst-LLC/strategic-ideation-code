-- Advanced analytical queries for strategy, tactics, and ideation.

-- 1. Highest-scoring initiatives
SELECT *
FROM initiative_weighted_scores
ORDER BY weighted_score DESC;

-- 2. Lowest tactical translation scores
SELECT *
FROM tactical_translation_scores
ORDER BY translation_score ASC;

-- 3. Highest-priority feedback events
SELECT *
FROM feedback_priority_queue
ORDER BY priority_score DESC;

-- 4. High-criticality, low-confidence assumptions
SELECT
    assumption_id,
    initiative_id,
    layer,
    assumption_text,
    confidence,
    criticality,
    ROUND((1.0 - confidence) * criticality, 4) AS assumption_risk,
    test_method,
    evidence_status
FROM assumptions
ORDER BY assumption_risk DESC;

-- 5. Initiatives with tactical alignment problems
SELECT
    s.initiative_id,
    s.initiative_name,
    s.primary_layer,
    AVG(t.alignment_to_strategy) AS avg_tactical_alignment,
    AVG(t.learning_routing) AS avg_learning_routing
FROM strategic_initiatives s
JOIN tactical_actions t ON s.initiative_id = t.initiative_id
GROUP BY s.initiative_id, s.initiative_name, s.primary_layer
HAVING avg_tactical_alignment < 0.75 OR avg_learning_routing < 0.70
ORDER BY avg_tactical_alignment ASC;
