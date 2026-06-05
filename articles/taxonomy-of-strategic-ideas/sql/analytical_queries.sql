-- Advanced analytical queries for Taxonomy of Strategic Ideas.

SELECT * FROM taxonomy_record_scores ORDER BY taxonomy_strength DESC;
SELECT * FROM taxonomy_record_scores ORDER BY taxonomy_risk DESC;
SELECT * FROM classification_error_scores ORDER BY classification_error_risk DESC;
SELECT * FROM relationship_quality_scores ORDER BY relationship_quality_score ASC;
SELECT * FROM retrieval_test_scores ORDER BY retrieval_test_score ASC;
SELECT * FROM governance_ethics_scores ORDER BY taxonomy_stewardship_score ASC;
SELECT * FROM governance_ethics_scores ORDER BY ethical_classification_risk DESC;
