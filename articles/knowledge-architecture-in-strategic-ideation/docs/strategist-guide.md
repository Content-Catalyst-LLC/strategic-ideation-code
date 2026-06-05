# Strategist Guide

This scaffold supports strategic knowledge architecture analysis through ten recurring questions:

1. What strategic work should this knowledge system support?
2. How are ideas classified?
3. What metadata is required for an idea to remain useful?
4. Are key terms semantically clear across teams?
5. What evidence and assumptions are linked to each idea?
6. How do ideas relate to other ideas, decisions, risks, stakeholders, and lessons?
7. Can teams retrieve the right knowledge when decisions arise?
8. Does decision memory preserve rationale, alternatives, dissent, and revision triggers?
9. Who stewards the taxonomy, metadata, repository, and evidence standards?
10. Whose knowledge is included, searchable, protected, or omitted?

Recommended workflow:

- Run `python3 python/knowledge_architecture_diagnostics.py`
- Review `outputs/tables/idea_architecture_scores.csv`
- Review `outputs/tables/evidence_assumption_scores.csv`
- Review `outputs/tables/relationship_mapping_scores.csv`
- Review `outputs/tables/retrieval_reuse_scores.csv`
- Review `outputs/tables/stewardship_ethics_scores.csv`
- Use the generated markdown report for workshop discussion.
