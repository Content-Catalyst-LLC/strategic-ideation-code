-- Advanced analytical queries for boundary setting in strategic ideation.

-- 1. Strongest boundary frames
SELECT *
FROM boundary_quality_scores
ORDER BY boundary_quality_score DESC;

-- 2. Stakeholder exclusion risks
SELECT *
FROM stakeholder_boundary_scores
ORDER BY stakeholder_exclusion_risk DESC;

-- 3. Strongest causal frames
SELECT *
FROM causal_boundary_scores
ORDER BY causal_quality_score DESC;

-- 4. Temporal compression risks
SELECT *
FROM temporal_boundary_scores
ORDER BY temporal_compression_risk DESC;

-- 5. Institutional authority-consequence gaps
SELECT *
FROM institutional_boundary_scores
ORDER BY authority_consequence_gap DESC;

-- 6. Evidence boundaries needing expansion
SELECT *
FROM evidence_boundary_scores
ORDER BY evidence_diversity_score ASC;

-- 7. Ethical boundary risks
SELECT *
FROM ethical_boundary_scores
ORDER BY ethical_risk_score DESC;

-- 8. Boundary drift risks
SELECT *
FROM boundary_drift_scores
ORDER BY boundary_drift_risk DESC;

-- 9. Strong revision triggers
SELECT *
FROM revision_trigger_scores
ORDER BY trigger_quality_score DESC;

-- 10. Boundary-sensitive option scores
SELECT
    option_id,
    option_name,
    ROUND(
      0.38 * internal_efficiency +
      0.10 * stakeholder_value +
      0.10 * system_leverage +
      0.10 * long_term_resilience +
      0.08 * ethical_responsibility +
      0.16 * implementation_feasibility +
      0.04 * learning_value +
      0.04 * strategic_reversibility,
      4
    ) AS internal_boundary_score,
    ROUND(
      0.08 * internal_efficiency +
      0.34 * stakeholder_value +
      0.12 * system_leverage +
      0.10 * long_term_resilience +
      0.20 * ethical_responsibility +
      0.08 * implementation_feasibility +
      0.05 * learning_value +
      0.03 * strategic_reversibility,
      4
    ) AS stakeholder_boundary_score,
    ROUND(
      0.08 * internal_efficiency +
      0.12 * stakeholder_value +
      0.34 * system_leverage +
      0.18 * long_term_resilience +
      0.10 * ethical_responsibility +
      0.06 * implementation_feasibility +
      0.08 * learning_value +
      0.04 * strategic_reversibility,
      4
    ) AS system_boundary_score
FROM options;
