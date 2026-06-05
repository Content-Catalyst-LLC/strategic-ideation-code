-- Advanced analytical queries for Adaptive Strategy and Iteration.

SELECT * FROM adaptive_strategy_profile_scores ORDER BY adaptive_strategy_score DESC;
SELECT * FROM adaptive_strategy_profile_scores ORDER BY over_adaptation_risk DESC;
SELECT * FROM feedback_signal_scores ORDER BY response_priority DESC;
SELECT * FROM assumption_revision_scores ORDER BY revision_need DESC;
SELECT * FROM trigger_condition_scores ORDER BY trigger_condition_score DESC;
SELECT * FROM trigger_condition_scores ORDER BY trigger_condition_score ASC;
SELECT * FROM experiment_portfolio_scores ORDER BY experiment_score DESC;
SELECT * FROM experiment_portfolio_scores ORDER BY experiment_score ASC;
SELECT * FROM timing_responsiveness_scores ORDER BY timing_discipline_score DESC;
SELECT * FROM timing_responsiveness_scores ORDER BY whiplash_risk DESC;
SELECT * FROM exploration_exploitation_scores ORDER BY portfolio_balance_score DESC;
SELECT * FROM systems_impact_scores ORDER BY systems_impact_risk DESC;
SELECT * FROM adaptive_governance_scores ORDER BY adaptive_governance_score DESC;
SELECT * FROM adaptive_governance_scores ORDER BY adaptive_governance_score ASC;
SELECT * FROM learning_memory_scores ORDER BY learning_memory_score DESC;
SELECT * FROM learning_memory_scores ORDER BY learning_memory_score ASC;
