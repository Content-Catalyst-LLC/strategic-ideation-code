-- Advanced analytical queries for problem framing and problem definition.

-- 1. Strongest problem frames
SELECT *
FROM problem_framing_scores
ORDER BY problem_framing_score DESC;

-- 2. Highest frame-origin lock-in risks
SELECT *
FROM frame_origin_scores
ORDER BY lock_in_risk DESC;

-- 3. Weakest boundary definitions
SELECT *
FROM boundary_quality_scores
ORDER BY boundary_quality_score ASC;

-- 4. Strongest stakeholder frame quality
SELECT *
FROM stakeholder_frame_scores
ORDER BY stakeholder_frame_quality_score DESC;

-- 5. Weakest stakeholder frame quality
SELECT *
FROM stakeholder_frame_scores
ORDER BY stakeholder_frame_quality_score ASC;

-- 6. Weakest causal models
SELECT *
FROM causal_quality_scores
ORDER BY causal_quality_score ASC;

-- 7. Priority assumptions to test
SELECT *
FROM assumption_priority_scores
ORDER BY assumption_priority_score DESC;

-- 8. Highest-value alternative frames
SELECT *
FROM alternative_frame_scores
ORDER BY comparison_value_score DESC;

-- 9. Strongest reframing triggers
SELECT *
FROM reframing_trigger_scores
ORDER BY trigger_strength_score DESC;

-- 10. Highest-value framing interventions
SELECT *
FROM intervention_value_scores
ORDER BY intervention_value_score DESC;

-- 11. Frames likely to be symptom-focused or institutionally convenient
SELECT
    frame_id,
    frame_name,
    ROUND(
      (1.0 - causal_depth) * 0.30 +
      (1.0 - systems_awareness) * 0.25 +
      CASE WHEN 0.70 - boundary_breadth > 0 THEN (0.70 - boundary_breadth) * 0.20 ELSE 0 END +
      institutional_lock_in_risk * 0.15 +
      political_convenience_risk * 0.10,
      4
    ) AS symptom_framing_risk
FROM problem_frames
ORDER BY symptom_framing_risk DESC;
