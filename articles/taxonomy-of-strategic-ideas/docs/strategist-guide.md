# Strategist Guide

This scaffold supports strategic idea taxonomy analysis through ten recurring questions:

1. What kind of strategic object is this idea?
2. At what level of strategy does it operate?
3. How mature is the idea?
4. What evidence status and confidence level does it have?
5. What strategic function does it perform?
6. What mechanism is expected to produce effects?
7. How does it relate to other ideas?
8. Can it be retrieved later using meaningful strategic questions?
9. Who governs categories, definitions, changes, metadata quality, and AI classification?
10. Whose categories, voice, burden, dissent, and affected experience remain visible?

Recommended workflow:

- Run `python3 python/taxonomy_diagnostics.py`
- Review `outputs/tables/taxonomy_record_scores.csv`
- Review `outputs/tables/classification_error_scores.csv`
- Review `outputs/tables/relationship_quality_scores.csv`
- Review `outputs/tables/retrieval_test_scores.csv`
- Review `outputs/tables/governance_ethics_scores.csv`
- Use the generated markdown report for workshop discussion.
