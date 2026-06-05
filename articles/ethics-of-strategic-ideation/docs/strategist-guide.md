# Strategist Guide

This scaffold supports ethical strategic ideation analysis through ten recurring questions:

1. Who defined the problem, and what did the frame exclude?
2. Which affected stakeholders have meaningful influence before decisions harden?
3. Do claims match evidence, uncertainty, and counterevidence?
4. Who benefits, who pays, who adapts, and who bears risk?
5. Which constraints are genuine, and which reflect institutional power?
6. What knowledge, categories, futures, or stakeholders are missing?
7. What if the idea is wrong, and can it be reversed or stopped?
8. What obligations exist to future people, ecosystems, and institutional capacity?
9. How did AI shape the idea, and how were outputs verified?
10. Who owns monitoring, correction, accountability, and redress?

Recommended workflow:

- Run `python3 python/ethical_ideation_diagnostics.py`
- Review `outputs/tables/ethical_idea_scores.csv`
- Review `outputs/tables/stakeholder_impact_scores.csv`
- Review `outputs/tables/claim_evidence_ethics_scores.csv`
- Review `outputs/tables/ai_ethics_scores.csv`
- Review `outputs/tables/accountability_redress_scores.csv`
- Use the generated markdown report for workshop discussion.
