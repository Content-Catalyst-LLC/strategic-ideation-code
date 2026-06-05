#!/usr/bin/env python3
from __future__ import annotations
import csv, json, math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
TABLES = ROOT / "outputs" / "tables"
REPORTS = ROOT / "outputs" / "reports"
PROCESSED = ROOT / "data" / "processed"
for d in (TABLES, REPORTS, PROCESSED): d.mkdir(parents=True, exist_ok=True)

def read_csv(path):
    with path.open(newline='', encoding='utf-8') as h: return list(csv.DictReader(h))
def write_csv(path, rows):
    if not rows: return
    with path.open('w', newline='', encoding='utf-8') as h:
        w=csv.DictWriter(h, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
def f(row, key): return float(row[key])

options=read_csv(RAW/'options.csv')
criteria=read_csv(RAW/'criteria.csv')
scores=read_csv(RAW/'scores.csv')
weights=read_csv(RAW/'weight_sets.csv')
scenarios=read_csv(RAW/'scenario_scores.csv')
criteria_audit=read_csv(RAW/'criteria_audit.csv')
governance=read_csv(RAW/'governance_review.csv')
memory=read_csv(RAW/'decision_memory.csv')
option_names={r['option_id']:r['option_name'] for r in options}
cn=[r['criterion_name'] for r in criteria]
base=next(r for r in weights if r['weight_set']=='base')

def weighted(row, w): return sum(f(row,c)*f(w,c) for c in cn)

def threshold_flags(row):
    flags=[]
    for c in criteria:
        t=c['ethical_threshold'].strip()
        if t and c['non_compensatory'].lower()=='true' and f(row,c['criterion_name']) < float(t):
            flags.append(f"{c['criterion_name']}={f(row,c['criterion_name']):.2f}<threshold {float(t):.2f}")
    return flags

weighted_rows=[]
for r in scores:
    score=weighted(r,base); flags=threshold_flags(r)
    warn='threshold_review_required' if flags else ('low_evidence_confidence' if f(r,'evidence_confidence')<.55 else ('strong_matrix_candidate' if score>=.70 else 'deliberation_required'))
    weighted_rows.append({'option_id':r['option_id'],'option_name':option_names[r['option_id']],'base_score':round(score,4),'confidence_adjusted_score':round(score*f(r,'evidence_confidence'),4),'evidence_confidence':r['evidence_confidence'],'threshold_flags':'; '.join(flags),'decision_warning':warn,'score_notes':r['score_notes']})
weighted_rows.sort(key=lambda x:x['base_score'], reverse=True)
for i,r in enumerate(weighted_rows,1): r['base_rank']=i
write_csv(TABLES/'weighted_matrix_scores.csv', weighted_rows); write_csv(PROCESSED/'weighted_matrix_scores.csv', weighted_rows)
conf=sorted(weighted_rows, key=lambda x:x['confidence_adjusted_score'], reverse=True)
for i,r in enumerate(conf,1): r['confidence_adjusted_rank']=i
write_csv(TABLES/'confidence_adjusted_scores.csv', conf)

sens=[]
for w in weights:
    subset=[]
    for r in scores:
        s=weighted(r,w)
        subset.append({'weight_set':w['weight_set'],'option_id':r['option_id'],'option_name':option_names[r['option_id']],'score':round(s,4),'confidence_adjusted_score':round(s*f(r,'evidence_confidence'),4),'description':w['description']})
    subset.sort(key=lambda x:x['score'], reverse=True)
    for rank,row in enumerate(subset,1): row['rank']=rank
    sens.extend(subset)
write_csv(TABLES/'weight_sensitivity_scores.csv', sens)

groups=defaultdict(list)
for r in sens: groups[r['option_id']].append(r)
stability=[]
for oid, rows in groups.items():
    ranks=[int(r['rank']) for r in rows]; vals=[float(r['score']) for r in rows]
    rr=max(ranks)-min(ranks); sr=max(vals)-min(vals)
    warning='high_rank_instability' if rr>=3 else ('moderate_rank_instability' if rr>=2 else ('near_tie_false_precision_zone' if sr<.035 else 'stable_enough_for_deliberation'))
    stability.append({'option_id':oid,'option_name':option_names[oid],'best_rank':min(ranks),'worst_rank':max(ranks),'rank_range':rr,'score_range':round(sr,4),'average_score':round(sum(vals)/len(vals),4),'stability_warning':warning})
stability.sort(key=lambda x:(x['rank_range'],x['score_range']), reverse=True)
write_csv(TABLES/'rank_stability_scores.csv', stability)

crit_rows=[]
for r in criteria_audit:
    q=.18*f(r,'relevance')+.15*f(r,'clarity')+.12*f(r,'measurability')+.13*f(r,'evidence_availability')+.14*f(r,'stakeholder_legitimacy')+.15*f(r,'ethical_importance')+.13*f(r,'uncertainty_sensitivity')
    fp=.28*(1-f(r,'measurability'))+.24*(1-f(r,'evidence_availability'))+.18*f(r,'uncertainty_sensitivity')+.16*(1-f(r,'clarity'))+.14*f(r,'ethical_importance')
    action='avoid_false_precision_and_use_qualitative_review' if fp>=.62 else ('strong_criterion' if q>=.72 else r['review_action'])
    crit_rows.append({'criterion_id':r['criterion_id'],'criterion_name':r['criterion_name'],'criteria_quality':round(q,4),'false_precision_risk':round(fp,4),'recommended_action':action,'source_review_action':r['review_action']})
crit_rows.sort(key=lambda x:x['false_precision_risk'], reverse=True)
write_csv(TABLES/'criteria_audit_scores.csv', crit_rows)

scenario_rows=[]
for r in scenarios:
    s=weighted(r,base)
    scenario_rows.append({'scenario_id':r['scenario_id'],'scenario_name':r['scenario_name'],'option_id':r['option_id'],'option_name':option_names[r['option_id']],'scenario_score':round(s,4),'confidence_adjusted_score':round(s*f(r,'evidence_confidence'),4)})
for scen in sorted({r['scenario_name'] for r in scenario_rows}):
    sub=[r for r in scenario_rows if r['scenario_name']==scen]; sub.sort(key=lambda x:x['scenario_score'], reverse=True)
    for rank,row in enumerate(sub,1): row['scenario_rank']=rank
write_csv(TABLES/'scenario_matrix_scores.csv', scenario_rows)
sg=defaultdict(list)
for r in scenario_rows: sg[r['option_id']].append(r)
rob=[]
for oid, rows in sg.items():
    vals=[float(r['scenario_score']) for r in rows]; ranks=[int(r['scenario_rank']) for r in rows]
    mean=sum(vals)/len(vals); vol=(sum((v-mean)**2 for v in vals)/len(vals))**0.5
    score=.42*min(vals)+.34*mean+.12*max(vals)-.12*vol
    rob.append({'option_id':oid,'option_name':option_names[oid],'mean_scenario_score':round(mean,4),'worst_case_score':round(min(vals),4),'best_case_score':round(max(vals),4),'scenario_volatility':round(vol,4),'best_scenario_rank':min(ranks),'worst_scenario_rank':max(ranks),'scenario_rank_range':max(ranks)-min(ranks),'scenario_robustness_score':round(score,4)})
rob.sort(key=lambda x:x['scenario_robustness_score'], reverse=True)
write_csv(TABLES/'scenario_robustness_scores.csv', rob)

threshold=[]
for r in scores:
    flags=threshold_flags(r)
    threshold.append({'option_id':r['option_id'],'option_name':option_names[r['option_id']],'threshold_status':'threshold_review_required' if flags else 'passes_defined_thresholds','threshold_flags':'; '.join(flags),'risk_control':r['risk_control'],'ethical_resilience':r['ethical_resilience'],'recommended_action':'redesign_or_veto_review' if flags else 'continue_deliberation'})
write_csv(TABLES/'ethical_threshold_review.csv', threshold)

fp_rows=[]
for r in weighted_rows:
    gaps=[abs(float(r['base_score'])-float(o['base_score'])) for o in weighted_rows if o['option_id']!=r['option_id']]
    nearest=min(gaps) if gaps else 0
    flags=[]
    if nearest<.035: flags.append('near_tie')
    if float(r['evidence_confidence'])<.55: flags.append('low_evidence_confidence')
    if r['threshold_flags']: flags.append('non_compensatory_threshold_flag')
    if any(s['option_id']==r['option_id'] and s['rank_range']>=2 for s in stability): flags.append('rank_sensitive_to_weights')
    fp_rows.append({'option_id':r['option_id'],'option_name':r['option_name'],'base_score':r['base_score'],'nearest_score_gap':round(nearest,4),'warning_flags':';'.join(flags),'recommended_action':'treat_ranking_as_deliberation_zone' if flags else 'stable_enough_for_discussion'})
write_csv(TABLES/'false_precision_warnings.csv', sorted(fp_rows,key=lambda x:x['nearest_score_gap']))

gov_rows=[]
for r in governance:
    g=.12*f(r,'process_quality')+.12*f(r,'transparency')+.13*f(r,'stakeholder_voice')+.12*f(r,'dissent_capture')+.14*f(r,'sensitivity_testing')+.13*f(r,'evidence_traceability')+.13*f(r,'ethical_threshold_quality')+.11*f(r,'decision_memory_quality')
    action='strong_matrix_governance' if g>=.68 else ('run_sensitivity_testing' if f(r,'sensitivity_testing')<.50 else ('increase_stakeholder_voice' if f(r,'stakeholder_voice')<.52 else r['review_action']))
    gov_rows.append({'governance_id':r['governance_id'],'practice':r['practice'],'governance_score':round(g,4),'governance_gap':round(1-g,4),'recommended_action':action,'source_review_action':r['review_action']})
gov_rows.sort(key=lambda x:x['governance_score'], reverse=True)
write_csv(TABLES/'governance_review_scores.csv', gov_rows)

mem_rows=[]
for r in memory:
    m=.12*f(r,'criteria_rationale')+.12*f(r,'weight_rationale')+.12*f(r,'evidence_notes')+.13*f(r,'sensitivity_results')+.12*f(r,'dissent_record')+.13*f(r,'ethical_threshold_record')+.12*f(r,'uncertainty_record')+.12*f(r,'revision_trigger_quality')+.12*f(r,'reuse_quality')
    action='strong_decision_memory' if m>=.68 else ('preserve_dissent_record' if f(r,'dissent_record')<.50 else ('record_sensitivity_results' if f(r,'sensitivity_results')<.58 else r['review_action']))
    mem_rows.append({'memory_id':r['memory_id'],'decision_record':r['decision_record'],'decision_memory_score':round(m,4),'recommended_action':action,'source_review_action':r['review_action']})
mem_rows.sort(key=lambda x:x['decision_memory_score'], reverse=True)
write_csv(TABLES/'decision_memory_scores.csv', mem_rows)

report=['# Decision Matrices and Their Limits Diagnostic Report','', '## Executive summary','', 'This diagnostic evaluates a strategic decision matrix across weighted scores, confidence-adjusted rankings, weight sensitivity, rank stability, criteria quality, scenario robustness, ethical thresholds, false precision warnings, governance, and decision memory.', '', '## Base weighted ranking']
for r in weighted_rows: report.append(f"- **{r['base_rank']}. {r['option_name']}** — score {r['base_score']}; confidence-adjusted {r['confidence_adjusted_score']}; warning: {r['decision_warning']}.")
report += ['', '## Rank stability warnings']
for r in stability: report.append(f"- **{r['option_name']}** — best rank {r['best_rank']}; worst rank {r['worst_rank']}; rank range {r['rank_range']}; warning: {r['stability_warning']}.")
report += ['', '## Scenario robustness']
for r in rob: report.append(f"- **{r['option_name']}** — robustness {r['scenario_robustness_score']}; worst case {r['worst_case_score']}; rank range {r['scenario_rank_range']}.")
report += ['', '## Ethical threshold review']
for r in threshold: report.append(f"- **{r['option_name']}** — {r['threshold_status']}; action: {r['recommended_action']}; flags: {r['threshold_flags'] or 'none'}.")
report += ['', '## False precision warnings']
for r in fp_rows: report.append(f"- **{r['option_name']}** — nearest score gap {r['nearest_score_gap']}; flags: {r['warning_flags'] or 'none'}; action: {r['recommended_action']}.")
report += ['', '## Professional interpretation','', 'Decision matrices are most useful when they make judgment inspectable. Treat close rankings, low-confidence scores, threshold flags, and weight-sensitive outcomes as deliberation zones rather than automatic decisions.']
(REPORTS/'decision_matrix_diagnostic_report.md').write_text('\n'.join(report), encoding='utf-8')
(REPORTS/'diagnostic_summary.json').write_text(json.dumps({'weighted':weighted_rows,'stability':stability,'scenario_robustness':rob,'thresholds':threshold,'false_precision':fp_rows}, indent=2), encoding='utf-8')
print('Advanced decision matrix diagnostics complete.')
print(f'Wrote: {TABLES}')
print(f'Wrote: {REPORTS / "decision_matrix_diagnostic_report.md"}')
