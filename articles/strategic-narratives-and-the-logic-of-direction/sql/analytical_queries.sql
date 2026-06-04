-- Advanced analytical queries for strategic narrative systems.

-- 1. Weakest narrative coherence scores
SELECT *
FROM narrative_coherence_scores
ORDER BY coherence_score ASC;

-- 2. Weakest direction-logic links
SELECT *
FROM direction_logic_scores
ORDER BY direction_logic_score ASC;

-- 3. Highest narrative-performance gaps
SELECT *
FROM narrative_performance_gap_scores
ORDER BY narrative_performance_gap DESC;

-- 4. Weakest role alignment
SELECT *
FROM role_alignment_scores
ORDER BY role_alignment_score ASC;

-- 5. Highest narrative drift priorities
SELECT *
FROM narrative_drift_priorities
ORDER BY drift_priority DESC;

-- 6. Weakest governance scores
SELECT *
FROM narrative_governance_scores
ORDER BY governance_strength ASC;

-- 7. Stakeholder groups with low perceived truthfulness
SELECT
    interpretation_id,
    narrative_id,
    stakeholder_group,
    perceived_truthfulness,
    perceived_inclusion,
    perceived_burden_visibility,
    contestation_level
FROM stakeholder_interpretations
ORDER BY perceived_truthfulness ASC, contestation_level DESC;
