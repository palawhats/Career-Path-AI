"""Transparent deficit calculation; Importance is relevance, not user ability."""
import numpy as np
from .data import normalize_importance

def analyze(skills,user,levels,importance,ratings):
    normalized=levels/7
    gaps=np.maximum(0,normalized-user)
    priority=gaps*normalize_importance(importance)
    rows=[{'skill':s,'self_rating':ratings[s],'user_normalized':float(user[j]),'occupational_level':float(levels[j]),'career_normalized':float(normalized[j]),'importance':float(importance[j]),'gap':float(gaps[j]),'priority':float(priority[j])} for j,s in enumerate(skills)]
    ordered=sorted(rows,key=lambda r:(-r['priority'],-r['importance'],r['skill']))
    return {'development': [r for r in ordered if r['gap']>0][:5],'aligned':[r for r in ordered if r['gap']==0],'all_skills':ordered}
