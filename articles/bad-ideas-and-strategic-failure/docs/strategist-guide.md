# Strategist Guide

This scaffold supports bad-idea and strategic failure analysis through ten recurring questions:

1. Is the idea solving the right problem?
2. Is the causal mechanism clear enough to test?
3. Does confidence match evidence?
4. Does external evidence actually fit this context?
5. Can the organization implement the idea responsibly?
6. What incentives and unintended behaviors will the idea create?
7. Who bears burden, harm, risk, or hidden labor?
8. Is the idea advancing because of merit or because power protects it?
9. Is the narrative more honest or more persuasive?
10. What would cause the idea to pause, pivot, shrink, retire, or return to problem framing?

Recommended workflow:

- Run `python3 python/bad_idea_diagnostics.py`
- Review `outputs/tables/bad_idea_risk_scores.csv`
- Review `outputs/tables/failure_pathway_scores.csv`
- Review `outputs/tables/evidence_overclaim_scores.csv`
- Review `outputs/tables/implementation_incentive_scores.csv`
- Review `outputs/tables/power_narrative_learning_scores.csv`
- Use the generated markdown report for workshop discussion.
