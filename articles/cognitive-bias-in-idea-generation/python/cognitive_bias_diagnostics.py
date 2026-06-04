#!/usr/bin/env python3
"""Advanced standard-library diagnostics for cognitive bias in idea generation."""
from __future__ import annotations
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
TABLES = ROOT / 'outputs' / 'tables'
REPORTS = ROOT / 'outputs' / 'reports'
PROCESSED = ROOT / 'data' / 'processed'
for p in (TABLES, REPORTS, PROCESSED): p.mkdir(parents=True, exist_ok=True)

def read_csv(path: Path):
    with path.open(newline='', encoding='utf-8') as f: return list(csv.DictReader(f))
def write_csv(path: Path, rows, fields):
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
def x(row, key): return float(row[key])

contexts = read_csv(RAW/'bias_contexts.csv')
ideas = read_csv(RAW/'idea_space_inventory.csv')
frames = read_csv(RAW/'frame_rotation.csv')
assumptions = read_csv(RAW/'assumption_register.csv')
stakeholders = read_csv(RAW/'stakeholder_visibility.csv')
interventions = read_csv(RAW/'intervention_library.csv')
context_names = {r['context_id']: r['context_name'] for r in contexts}

profiles=[]
for r in contexts:
    pressure=.15*x(r,'availability_pressure')+.15*x(r,'anchoring_intensity')+.15*x(r,'conformity_pressure')+.14*x(r,'framing_rigidity')+.12*x(r,'institutional_lock_in')+.10*x(r,'expert_enclosure')+.08*x(r,'ai_familiarity_pressure')-.06*x(r,'stakeholder_diversity')-.05*x(r,'evidence_discipline')
    profile=-.12*x(r,'availability_pressure')-.12*x(r,'anchoring_intensity')-.13*x(r,'conformity_pressure')-.12*x(r,'framing_rigidity')-.10*x(r,'institutional_lock_in')-.08*x(r,'expert_enclosure')-.07*x(r,'ai_familiarity_pressure')+.16*x(r,'stakeholder_diversity')+.18*x(r,'exploratory_variation')+.12*x(r,'evidence_discipline')+.08*x(r,'political_safety')+.08*x(r,'decision_memory_quality')
    convergence=x(r,'anchoring_intensity')*x(r,'conformity_pressure')*x(r,'framing_rigidity')
    institutional=x(r,'institutional_lock_in')*(1-x(r,'stakeholder_diversity'))
    ai_risk=x(r,'ai_familiarity_pressure')*(1-x(r,'exploratory_variation'))
    stakeholder_gap=max(0,.60-x(r,'stakeholder_diversity'))
    political_gap=max(0,.55-x(r,'political_safety'))
    diagnosis='premature_convergence_risk' if convergence>=.45 else 'institutional_bias_risk' if institutional>=.50 else 'stakeholder_visibility_gap' if stakeholder_gap>=.25 else 'ai_amplified_familiarity_risk' if ai_risk>=.45 else 'stronger_ideation_conditions' if profile>=.25 else 'requires_bias_review'
    profiles.append({**r,'bias_pressure':round(pressure,4),'bias_adjusted_ideation_profile':round(profile,4),'premature_convergence_risk':round(convergence,4),'institutional_bias_risk':round(institutional,4),'ai_familiarity_risk':round(ai_risk,4),'stakeholder_visibility_gap':round(stakeholder_gap,4),'political_safety_gap':round(political_gap,4),'diagnosis':diagnosis})
profiles.sort(key=lambda r:r['bias_adjusted_ideation_profile'], reverse=True)
profile_fields=['context_id','context_name','context_type','bias_pressure','bias_adjusted_ideation_profile','premature_convergence_risk','institutional_bias_risk','ai_familiarity_risk','stakeholder_visibility_gap','political_safety_gap','diagnosis','availability_pressure','anchoring_intensity','conformity_pressure','framing_rigidity','institutional_lock_in','expert_enclosure','ai_familiarity_pressure','stakeholder_diversity','exploratory_variation','evidence_discipline','political_safety','decision_memory_quality']
write_csv(TABLES/'bias_context_profiles.csv',profiles,profile_fields); write_csv(PROCESSED/'bias_context_profiles.csv',profiles,profile_fields)

risk_rows=sorted([{k:r[k] for k in ['context_id','context_name','premature_convergence_risk','institutional_bias_risk','ai_familiarity_risk','stakeholder_visibility_gap','political_safety_gap','diagnosis']} for r in profiles], key=lambda r:max(float(r['premature_convergence_risk']),float(r['institutional_bias_risk']),float(r['ai_familiarity_risk']),float(r['stakeholder_visibility_gap']),float(r['political_safety_gap'])), reverse=True)
write_csv(TABLES/'premature_convergence_risk.csv',risk_rows,['context_id','context_name','premature_convergence_risk','institutional_bias_risk','ai_familiarity_risk','stakeholder_visibility_gap','political_safety_gap','diagnosis'])

idea_rows=[]
for r in ideas:
    score=.14*x(r,'stakeholder_visibility')+.14*x(r,'novelty_level')+.14*x(r,'evidence_pathway')+.14*x(r,'strategic_relevance')+.10*x(r,'implementation_pathway')+.14*x(r,'source_diversity')-.10*x(r,'social_safety')-.10*x(r,'assumption_burden')
    action='check_for_safe_idea_conformity' if x(r,'social_safety')>=.80 and x(r,'novelty_level')<.35 else 'add_stakeholder_visibility_review' if x(r,'stakeholder_visibility')<.40 else 'expand_source_domain_search' if x(r,'source_diversity')<.40 else 'strong_idea_space_contributor' if score>=.50 else 'revise_or_defer'
    idea_rows.append({**r,'context_name':context_names.get(r['context_id'],r['context_id']),'idea_space_diversity_score':round(score,4),'recommended_action':action})
idea_rows.sort(key=lambda r:r['idea_space_diversity_score'], reverse=True)
write_csv(TABLES/'idea_space_diversity_scores.csv',idea_rows,['idea_id','context_id','context_name','idea_name','frame_family','mechanism_family','idea_space_diversity_score','recommended_action','stakeholder_visibility','novelty_level','evidence_pathway','strategic_relevance','implementation_pathway','system_level','source_diversity','social_safety','assumption_burden'])

frame_rows=[]
for r in frames:
    score=.10*min(1,float(r['idea_count'])/12)+.18*min(1,float(r['distinct_mechanisms'])/8)+.16*x(r,'stakeholder_inclusion')+.16*x(r,'system_level_coverage')+.14*x(r,'evidence_pathway_quality')-.08*x(r,'comfort_level')+.18*x(r,'frame_shift_value')
    action='comfort_frame_may_be_reinforcing_bias' if x(r,'comfort_level')>=.80 and x(r,'frame_shift_value')<.35 else 'increase_mechanism_diversity' if float(r['distinct_mechanisms'])<4 else 'add_stakeholder_frame' if x(r,'stakeholder_inclusion')<.40 else 'strong_frame_rotation_candidate' if score>=.60 else 'frame_requires_review'
    frame_rows.append({**r,'context_name':context_names.get(r['context_id'],r['context_id']),'frame_rotation_score':round(score,4),'recommended_action':action})
frame_rows.sort(key=lambda r:r['frame_rotation_score'], reverse=True)
write_csv(TABLES/'frame_rotation_review.csv',frame_rows,['frame_id','context_id','context_name','frame_name','frame_type','frame_rotation_score','recommended_action','idea_count','distinct_mechanisms','stakeholder_inclusion','system_level_coverage','evidence_pathway_quality','comfort_level','frame_shift_value'])

assumption_rows=[]
for r in assumptions:
    score=.22*x(r,'strategic_importance')+.22*x(r,'challenge_potential')+.18*(1-x(r,'evidence_strength'))+.16*x(r,'power_protection_risk')+.12*(1-x(r,'stakeholder_burden_visibility'))+.10*(1 if r['revision_priority']=='high' else .55)
    action='power_and_realism_review_required' if x(r,'power_protection_risk')>=.70 else 'test_or_challenge_assumption' if x(r,'evidence_strength')<.35 else 'add_burden_visibility_review' if x(r,'stakeholder_burden_visibility')<.35 else 'priority_bias_challenge' if score>=.70 else 'monitor_assumption'
    assumption_rows.append({**r,'context_name':context_names.get(r['context_id'],r['context_id']),'challenge_priority':round(score,4),'recommended_action':action})
assumption_rows.sort(key=lambda r:r['challenge_priority'], reverse=True)
write_csv(TABLES/'assumption_bias_review.csv',assumption_rows,['assumption_id','context_id','context_name','assumption_text','assumption_type','challenge_priority','recommended_action','evidence_strength','strategic_importance','challenge_potential','power_protection_risk','stakeholder_burden_visibility','revision_priority'])

stakeholder_rows=[]
for r in stakeholders:
    score=.16*x(r,'inclusion_level')+.18*x(r,'idea_influence')+.16*x(r,'burden_visibility')+.16*x(r,'knowledge_recognition')+.12*x(r,'interpretive_trust')-.12*x(r,'power_distance')+.14*x(r,'legitimacy_signal')
    action='include_stakeholders_before_idea_space_closes' if x(r,'idea_influence')<.30 else 'add_burden_visibility_review' if x(r,'burden_visibility')<.35 else 'power_distance_reduction_required' if x(r,'power_distance')>=.70 else 'stakeholder_visibility_gap' if score<.45 else 'stakeholder_visibility_manageable'
    stakeholder_rows.append({**r,'context_name':context_names.get(r['context_id'],r['context_id']),'stakeholder_visibility_score':round(score,4),'recommended_action':action})
stakeholder_rows.sort(key=lambda r:r['stakeholder_visibility_score'])
write_csv(TABLES/'stakeholder_visibility_review.csv',stakeholder_rows,['review_id','context_id','context_name','stakeholder_group','stakeholder_visibility_score','recommended_action','inclusion_level','idea_influence','burden_visibility','knowledge_recognition','interpretive_trust','power_distance','legitimacy_signal'])

intervention_rows=[]
for r in interventions:
    score=.20*x(r,'variation_gain')+.16*x(r,'legitimacy_gain')+.16*x(r,'evidence_gain')+.16*x(r,'decision_memory_gain')-.12*x(r,'process_cost')-.10*x(r,'implementation_complexity')-.10*x(r,'political_safety_need')
    action='requires_leadership_protection_for_dissent' if x(r,'political_safety_need')>=.60 else 'high_value_bias_intervention' if score>=.45 else 'use_as_supporting_intervention'
    intervention_rows.append({**r,'intervention_value_score':round(score,4),'recommended_action':action})
intervention_rows.sort(key=lambda r:r['intervention_value_score'], reverse=True)
write_csv(TABLES/'intervention_recommendations.csv',intervention_rows,['intervention_id','intervention_name','target_bias','intervention_value_score','recommended_action','process_cost','implementation_complexity','variation_gain','legitimacy_gain','evidence_gain','political_safety_need','decision_memory_gain'])

report=['# Cognitive Bias in Idea Generation Diagnostic Report\n','## Executive summary\n','This diagnostic separates bias pressure, bias-adjusted ideation quality, premature-convergence risk, institutional lock-in, AI-amplified familiarity, stakeholder visibility, idea-space diversity, frame rotation, assumption challenge priority, and intervention value.\n','## Contexts requiring the most bias review\n']
for r in sorted(profiles, key=lambda z:z['bias_adjusted_ideation_profile'])[:5]: report.append(f"- **{r['context_id']} — {r['context_name']}**: profile {r['bias_adjusted_ideation_profile']}; pressure {r['bias_pressure']}; diagnosis: {r['diagnosis']}.")
report.append('\n## Highest convergence or institutional risks\n')
for r in risk_rows[:5]: report.append(f"- **{r['context_id']} — {r['context_name']}**: premature convergence {r['premature_convergence_risk']}; institutional bias {r['institutional_bias_risk']}; AI familiarity {r['ai_familiarity_risk']}; stakeholder gap {r['stakeholder_visibility_gap']}.")
report.append('\n## Strongest idea-space diversity contributors\n')
for r in idea_rows[:6]: report.append(f"- **{r['idea_id']} — {r['idea_name']}**: score {r['idea_space_diversity_score']}; action: {r['recommended_action']}.")
report.append('\n## Highest-priority assumptions to challenge\n')
for r in assumption_rows[:6]: report.append(f"- **{r['assumption_id']} — {r['assumption_text']}**: priority {r['challenge_priority']}; action: {r['recommended_action']}.")
report.append('\n## Highest-value bias interventions\n')
for r in intervention_rows[:6]: report.append(f"- **{r['intervention_id']} — {r['intervention_name']}**: value {r['intervention_value_score']}; target bias: {r['target_bias']}.")
(REPORTS/'cognitive_bias_diagnostic_report.md').write_text('\n'.join(report), encoding='utf-8')
(REPORTS/'diagnostic_summary.json').write_text(json.dumps({'weakest_profiles': sorted(profiles, key=lambda z:z['bias_adjusted_ideation_profile'])[:5], 'highest_risks': risk_rows[:5], 'top_ideas': idea_rows[:6], 'top_assumptions': assumption_rows[:6], 'top_interventions': intervention_rows[:6]}, indent=2), encoding='utf-8')
print('Advanced cognitive bias diagnostics complete.')
print(f'Wrote: {TABLES / "bias_context_profiles.csv"}')
print(f'Wrote: {REPORTS / "cognitive_bias_diagnostic_report.md"}')
