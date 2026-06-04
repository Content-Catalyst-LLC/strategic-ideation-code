-- Advanced analytical queries for analogical thinking and idea transfer.

-- 1. Strongest analogical strategy profiles
SELECT *
FROM analogical_strategy_profiles
ORDER BY analogy_profile_score DESC;

-- 2. Highest surface-distraction risks
SELECT *
FROM surface_distraction_risks
ORDER BY surface_distraction_risk DESC;

-- 3. Strongest source-domain candidates
SELECT *
FROM source_domain_quality_scores
ORDER BY source_quality_score DESC;

-- 4. Strongest source-target mappings
SELECT *
FROM source_target_mapping_scores
ORDER BY mapping_score DESC;

-- 5. Strongest adaptation candidates
SELECT *
FROM adaptation_readiness_scores
ORDER BY adaptation_score DESC;

-- 6. Strongest rival analogies by target
SELECT *
FROM rival_analogy_scores
ORDER BY rival_analogy_score DESC;

-- 7. Weakest stakeholder legitimacy reviews
SELECT *
FROM stakeholder_legitimacy_scores
ORDER BY stakeholder_legitimacy_score ASC;

-- 8. Transfer hypotheses ready for evidence testing
SELECT *
FROM transfer_hypothesis_scores
ORDER BY transfer_hypothesis_score DESC;
