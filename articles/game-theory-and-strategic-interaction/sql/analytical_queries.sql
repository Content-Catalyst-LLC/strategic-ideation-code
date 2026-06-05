-- Advanced analytical queries for Game Theory and Strategic Interaction.

SELECT * FROM strategic_interaction_scores ORDER BY mechanism_opportunity DESC;
SELECT * FROM strategic_interaction_scores ORDER BY cooperation_fragility DESC;
SELECT * FROM actor_payoff_scores ORDER BY power_dependency_risk DESC;
SELECT * FROM information_signal_scores ORDER BY response_risk DESC;
SELECT * FROM equilibrium_diagnosis_scores ORDER BY bad_equilibrium_risk DESC;
SELECT * FROM cooperation_fragility_scores ORDER BY cooperation_fragility_score DESC;
SELECT * FROM repeated_interaction_scores ORDER BY repeated_game_capacity DESC;
SELECT * FROM mechanism_design_scores ORDER BY mechanism_design_score DESC;
SELECT * FROM mechanism_design_scores ORDER BY mechanism_design_score ASC;
SELECT * FROM behavioral_game_theory_scores ORDER BY behavioral_failure_risk DESC;
SELECT * FROM ethics_power_scores ORDER BY ethics_power_risk DESC;
SELECT * FROM strategic_interaction_memory_scores ORDER BY strategic_interaction_memory_score DESC;
SELECT * FROM strategic_interaction_memory_scores ORDER BY strategic_interaction_memory_score ASC;
