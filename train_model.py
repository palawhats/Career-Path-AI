"""Build a reusable 35-dimensional Euclidean retrieval artifact and honest diagnostics."""
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from threadpoolctl import threadpool_limits
from app.services.data import ROOT, validate_dataset, normalize_onet_levels

NORMALIZATION = {'user':'(rating - 1) / 4','level':'Level / 7','importance':'(Importance - 1) / 4','level_scale':[0,7],'importance_scale':[1,5],'source':'https://www.onetonline.org/help/online/scales'}
def build():
    d,skills,report=validate_dataset()
    levels=normalize_onet_levels(d[[s+'_Level' for s in skills]])
    assert np.all((levels>=0)&(levels<=1))
    rng=np.random.default_rng(2026)
    noisy=np.clip(levels+rng.normal(0,.05,levels.shape),0,1)
    rows=[]
    with threadpool_limits(limits=1):
        for metric in ['euclidean','manhattan','cosine']:
            model=NearestNeighbors(n_neighbors=10,metric=metric,algorithm='brute',n_jobs=1).fit(levels)
            exact=model.kneighbors(levels,return_distance=False)
            perturbed=model.kneighbors(noisy,return_distance=False)
            row={'metric':metric}
            for label,idx in [('self',exact),('perturb',perturbed)]:
                for k in [1,3,10]:row[f'{label}_top{k}']=float(np.mean([i in r[:k] for i,r in enumerate(idx)]))
            rows.append(row)
        model=NearestNeighbors(n_neighbors=10,metric='euclidean',algorithm='brute',n_jobs=1).fit(levels)
    artifact={'neighbors':model,'skills':skills,'careers':d[['ONET_SOC_Code','Career']].to_dict('records'),'raw_levels':d[[s+'_Level' for s in skills]].to_numpy(),'raw_importance':d[[s+'_Importance' for s in skills]].to_numpy(),'metric':'euclidean','sha256':report['sha256'],'normalization':NORMALIZATION,'version':'bilingual-v3'}
    (ROOT/'models').mkdir(exist_ok=True); (ROOT/'reports').mkdir(exist_ok=True)
    joblib.dump(artifact,ROOT/'models/model.pkl')
    metadata={'version':artifact['version'],'career_count':len(d),'skill_count':len(skills),'metric':'euclidean','feature_names':skills,'normalization':NORMALIZATION,'match_score':'clip(100 * (1 - distance / sqrt(35)), 0, 100)','dataset_sha256':report['sha256'],'validation':report,'evaluation_seed':2026,'noise_sigma':.05}
    (ROOT/'models/model_metadata.json').write_text(json.dumps(metadata,indent=2),encoding='utf8')
    (ROOT/'reports/dataset_validation.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    pd.DataFrame(rows).to_csv(ROOT/'reports/model_evaluation.csv',index=False)
    text='# Retrieval evaluation\n\nActual execution; synthetic / controlled perturbation evaluation. Not student career outcome accuracy.\n\n'+pd.DataFrame(rows).to_string(index=False)+'\n\nSeed 2026, independent Gaussian noise sigma 0.05 per normalized dimension, clipped to [0,1]. All 910 occupations remain in the reference index. Top-K counts retrieval of the originating occupation code. Self-retrieval is a sanity check. Tied profiles can obscure identity. Continuous noise does not emulate discrete student ratings. No student ground truth, holdout classification accuracy or career success prediction is claimed.\n\nEuclidean is used by specification because it preserves absolute level differences. The alternative metrics are diagnostics, not a claim of superiority. Normalization uses Level / 7 based on the documented O*NET scale, replacing the old observed-maximum /6 calibration. Prior evaluation numbers therefore do not describe this model.\n'
    (ROOT/'reports/model_evaluation.md').write_text(text,encoding='utf8')
    print(json.dumps(report,indent=2));print(text)
if __name__=='__main__':build()
