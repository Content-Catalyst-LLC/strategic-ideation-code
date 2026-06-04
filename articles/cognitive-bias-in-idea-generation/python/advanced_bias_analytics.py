#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'data'/'raw'; TABLES=ROOT/'outputs'/'tables'; FIGURES=ROOT/'outputs'/'figures'
TABLES.mkdir(parents=True, exist_ok=True); FIGURES.mkdir(parents=True, exist_ok=True)
try:
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError as exc:
    print('Missing optional analytics dependencies. Run: pip install -r python/requirements-advanced.txt')
    raise SystemExit(1) from exc
contexts=pd.read_csv(RAW/'bias_contexts.csv'); ideas=pd.read_csv(RAW/'idea_space_inventory.csv'); interventions=pd.read_csv(RAW/'intervention_library.csv')
contexts['bias_adjusted_ideation_profile']=(-.12*contexts.availability_pressure-.12*contexts.anchoring_intensity-.13*contexts.conformity_pressure-.12*contexts.framing_rigidity-.10*contexts.institutional_lock_in-.08*contexts.expert_enclosure-.07*contexts.ai_familiarity_pressure+.16*contexts.stakeholder_diversity+.18*contexts.exploratory_variation+.12*contexts.evidence_discipline+.08*contexts.political_safety+.08*contexts.decision_memory_quality)
contexts['premature_convergence_risk']=contexts.anchoring_intensity*contexts.conformity_pressure*contexts.framing_rigidity
ideas['idea_space_diversity_score']=(.14*ideas.stakeholder_visibility+.14*ideas.novelty_level+.14*ideas.evidence_pathway+.14*ideas.strategic_relevance+.10*ideas.implementation_pathway+.14*ideas.source_diversity-.10*ideas.social_safety-.10*ideas.assumption_burden)
interventions['intervention_value_score']=(.20*interventions.variation_gain+.16*interventions.legitimacy_gain+.16*interventions.evidence_gain+.16*interventions.decision_memory_gain-.12*interventions.process_cost-.10*interventions.implementation_complexity-.10*interventions.political_safety_need)
for df,xcol,ycol,title,filename in [(contexts,'context_name','bias_adjusted_ideation_profile','Bias-Adjusted Ideation Profile Scores','bias_adjusted_ideation_profiles.png'),(contexts,'context_name','premature_convergence_risk','Premature Convergence Risk','premature_convergence_risk.png'),(ideas,'idea_name','idea_space_diversity_score','Idea-Space Diversity Scores','idea_space_diversity_scores.png'),(interventions,'intervention_name','intervention_value_score','Bias Intervention Value Scores','intervention_value_scores.png')]:
    df.sort_values(ycol).plot(kind='barh',x=xcol,y=ycol,legend=False,figsize=(11,8)); plt.title(title); plt.xlabel(ycol.replace('_',' ')); plt.ylabel(''); plt.tight_layout(); plt.savefig(FIGURES/filename,dpi=160); plt.close()
contexts.to_csv(TABLES/'advanced_bias_context_profiles.csv', index=False); ideas.to_csv(TABLES/'advanced_idea_space_diversity_scores.csv', index=False); interventions.to_csv(TABLES/'advanced_intervention_value_scores.csv', index=False)
print('Advanced cognitive bias analytics complete.')
