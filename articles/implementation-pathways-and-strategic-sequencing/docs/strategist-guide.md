# Strategist Guide

This scaffold supports implementation pathway and sequencing analysis through ten recurring questions:

1. What is the strategic purpose of the pathway?
2. What are the major stages?
3. What must come before what?
4. What readiness conditions should govern stage advancement?
5. What capabilities must be built before scaling?
6. Can the organization absorb the proposed sequence?
7. Which steps are reversible and which create lock-in?
8. What external timing windows matter?
9. What feedback should trigger resequencing?
10. Who gets voice before commitment and who bears burden after it?

Recommended workflow:

- Run `python3 python/sequencing_readiness_diagnostics.py`
- Review `outputs/tables/pathway_readiness_scores.csv`
- Review `outputs/tables/dependency_risk_scores.csv`
- Review `outputs/tables/capacity_load_scores.csv`
- Review `outputs/tables/timing_window_scores.csv`
- Review `outputs/tables/reversibility_lockin_scores.csv`
- Review `outputs/tables/ethics_power_scores.csv`
- Use the generated markdown report for workshop discussion.
