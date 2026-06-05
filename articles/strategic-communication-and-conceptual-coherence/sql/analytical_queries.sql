-- Advanced analytical queries for Strategic Communication and Conceptual Coherence.

SELECT * FROM communication_profile_scores ORDER BY coherence_strength DESC;
SELECT * FROM communication_profile_scores ORDER BY meaning_loss_risk DESC;
SELECT * FROM concept_definition_scores ORDER BY concept_definition_score ASC;
SELECT * FROM concept_definition_scores ORDER BY drift_risk DESC;
SELECT * FROM claim_evidence_scores ORDER BY claim_evidence_integrity_score ASC;
SELECT * FROM audience_adaptation_scores ORDER BY audience_adaptation_score ASC;
SELECT * FROM decision_alignment_scores ORDER BY decision_alignment_score ASC;
SELECT * FROM governance_ethics_scores ORDER BY communication_stewardship_score ASC;
SELECT * FROM governance_ethics_scores ORDER BY ethical_communication_risk DESC;
