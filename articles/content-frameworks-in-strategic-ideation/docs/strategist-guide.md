# Strategist Guide

This scaffold supports strategic content framework analysis through ten recurring questions:

1. What strategic work should this framework support?
2. What content type does this framework produce?
3. Does the framework distinguish purpose, principles, themes, problems, opportunities, options, decisions, and actions?
4. What fields are required for strategic judgment?
5. Are evidence, assumptions, uncertainty, counterevidence, and revision triggers visible?
6. Does the framework preserve narrative coherence?
7. Can content components be reused and recombined?
8. What decision, communication need, or implementation step does the framework support?
9. Who owns, reviews, trains, and updates the framework?
10. Whose knowledge, burden, dissent, and ethical concerns remain visible?

Recommended workflow:

- Run `python3 python/content_framework_diagnostics.py`
- Review `outputs/tables/framework_scores.csv`
- Review `outputs/tables/component_reuse_scores.csv`
- Review `outputs/tables/framework_component_scores.csv`
- Review `outputs/tables/decision_support_scores.csv`
- Review `outputs/tables/narrative_coherence_scores.csv`
- Review `outputs/tables/governance_ethics_scores.csv`
- Use the generated markdown report for workshop discussion.
