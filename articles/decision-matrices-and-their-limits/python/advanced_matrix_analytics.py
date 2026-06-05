#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'data'/'raw'; TABLES=ROOT/'outputs'/'tables'; FIGURES=ROOT/'outputs'/'figures'
TABLES.mkdir(parents=True,exist_ok=True); FIGURES.mkdir(parents=True,exist_ok=True)
try:
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError as exc:
    print('Missing optional dependencies. Run: pip install -r python/requirements-advanced.txt')
    raise SystemExit(1) from exc
opts=pd.read_csv(RAW/'options.csv')
scores=pd.read_csv(RAW/'scores.csv').merge(opts[['option_id','option_name']], on='option_id')
weights=pd.read_csv(RAW/'weight_sets.csv')
criteria=pd.read_csv(RAW/'criteria.csv')['criterion_name'].tolist()
rows=[]
for _,w in weights.iterrows():
    temp=scores[['option_id','option_name','evidence_confidence']].copy(); temp['weight_set']=w['weight_set']
    temp['score']=scores[criteria].to_numpy() @ w[criteria].to_numpy(dtype=float)
    temp['confidence_adjusted_score']=temp['score']*temp['evidence_confidence']
    temp['rank']=temp['score'].rank(ascending=False,method='min').astype(int)
    rows.append(temp)
res=pd.concat(rows); res.to_csv(TABLES/'advanced_weight_sensitivity_scores.csv', index=False)
rank=res.groupby(['option_id','option_name']).agg(best_rank=('rank','min'),worst_rank=('rank','max'),average_score=('score','mean'),score_range=('score',lambda x:x.max()-x.min())).reset_index()
rank['rank_range']=rank['worst_rank']-rank['best_rank']; rank.to_csv(TABLES/'advanced_rank_stability_scores.csv', index=False)
res.pivot(index='option_name',columns='weight_set',values='score').plot(kind='barh',figsize=(11,7))
plt.title('Decision Matrix Scores Across Weight Sets'); plt.xlabel('Score'); plt.ylabel('Option'); plt.tight_layout(); plt.savefig(FIGURES/'scores_across_weight_sets.png',dpi=160); plt.close()
rank.sort_values('rank_range').plot(kind='barh',x='option_name',y='rank_range',legend=False,figsize=(11,7))
plt.title('Rank Instability Across Weight Sets'); plt.xlabel('Rank range'); plt.ylabel('Option'); plt.tight_layout(); plt.savefig(FIGURES/'rank_instability.png',dpi=160); plt.close()
print('Advanced matrix analytics complete.')
