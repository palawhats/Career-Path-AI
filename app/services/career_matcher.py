import math
import joblib
import numpy as np
from threadpoolctl import threadpool_limits
from .data import ROOT, normalize_user_skills
from .translations import load_career_titles
from .skill_gap import analyze

def score_from_distance(distance,number_of_skills=35):
    if not math.isfinite(distance) or distance<0 or number_of_skills<1:raise ValueError('Invalid distance')
    return float(np.clip(100*(1-distance/math.sqrt(number_of_skills)),0,100))

class CareerMatcher:
    def __init__(self):
        self.artifact=joblib.load(ROOT/'models/model.pkl')
        if self.artifact.get('version')!='bilingual-v3' or self.artifact['metric']!='euclidean':
            raise RuntimeError('Rebuild the matching artifact with python train_model.py')
        a=self.artifact
        if a['neighbors']._fit_X.shape!=(len(a['careers']),35) or not np.all((a['neighbors']._fit_X>=0)&(a['neighbors']._fit_X<=1)):
            raise RuntimeError('Invalid normalized occupational index')
        self.titles_th=load_career_titles(a['careers'])
        self.indices={c['ONET_SOC_Code']:i for i,c in enumerate(a['careers'])}
    def vector(self,ratings):
        if set(ratings)!=set(self.artifact['skills']):raise ValueError('Provide exactly the 35 required skill identifiers')
        if any(isinstance(v,bool) or not isinstance(v,int) for v in ratings.values()):raise ValueError('Self-ratings must be integers from 1 to 5')
        return normalize_user_skills([ratings[s] for s in self.artifact['skills']])
    def index(self,code):return self.indices[code]
    def identity(self,i):
        c=self.artifact['careers'][i]
        return {'onet_code':c['ONET_SOC_Code'],'career_en':c['Career'],'career_th':self.titles_th.get(c['ONET_SOC_Code'])}
    def career(self,code):
        i=self.index(code);a=self.artifact
        rows=[{'skill':s,'level':float(a['raw_levels'][i,j]),'importance':float(a['raw_importance'][i,j])} for j,s in enumerate(a['skills'])]
        important=sorted(rows,key=lambda r:(-r['importance'],-r['level'],r['skill']))[:10]
        return {**self.identity(i),'skills':rows,'important_skills':important,'source':'O*NET-derived supplied CSV','level_scale':[0,7],'importance_scale':[1,5]}
    def gaps(self,ratings,code):
        user=self.vector(ratings);i=self.index(code);a=self.artifact
        return analyze(a['skills'],user,a['raw_levels'][i],a['raw_importance'][i],ratings)
    def match(self,ratings):
        u=self.vector(ratings);a=self.artifact
        # Retrieve all to make distance ties deterministic by original occupation code.
        with threadpool_limits(limits=1):
            distances,indices=a['neighbors'].kneighbors([u],n_neighbors=len(a['careers']))
        nearest=sorted(zip(distances[0],indices[0]),key=lambda pair:(pair[0],a['careers'][pair[1]]['ONET_SOC_Code']))[:10]
        results=[]
        for rank,(dist,i) in enumerate(nearest,1):
            delta=np.abs(a['neighbors']._fit_X[i]-u)
            aligned=sorted(range(35),key=lambda j:(float(delta[j]),-float(a['raw_importance'][i,j]),a['skills'][j]))[:5]
            results.append({**self.identity(i),'rank':rank,'distance':float(dist),'match_score':score_from_distance(float(dist)),'matching_skills':[{'skill':a['skills'][j],'difference':float(delta[j]),'importance':float(a['raw_importance'][i,j])} for j in aligned]})
        return results
