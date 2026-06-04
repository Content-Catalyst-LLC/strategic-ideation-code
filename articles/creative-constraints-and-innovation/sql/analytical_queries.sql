-- Advanced analytical queries for creative constraints and innovation.

-- 1. Strongest productive constraint profiles
SELECT *
FROM constraint_context_profiles
ORDER BY productive_constraint_profile DESC;

-- 2. Highest rigidity and diffusion risks
SELECT *
FROM rigidity_and_diffusion_risks
ORDER BY MAX(rigidity_risk, diffusion_risk, legitimacy_gap) DESC;

-- 3. Highest-priority constraint classifications
SELECT *
FROM constraint_classification_scores
ORDER BY constraint_priority DESC;

-- 4. Most generative constraints
SELECT *
FROM constraint_function_scores
ORDER BY generative_constraint_value DESC;

-- 5. Highest-scoring innovation options
SELECT *
FROM innovation_option_scores
ORDER BY innovation_option_score DESC;

-- 6. Weakest stakeholder constraint scores
SELECT *
FROM stakeholder_constraint_scores
ORDER BY stakeholder_constraint_score ASC;

-- 7. Highest dynamic constraint priorities
SELECT *
FROM dynamic_constraint_priorities
ORDER BY dynamic_priority DESC;

-- 8. Strongest capability-learning scores
SELECT *
FROM capability_learning_scores
ORDER BY constraint_learning_score DESC;
