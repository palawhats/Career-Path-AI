from pathlib import Path
import hashlib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'data/career_training_data_v2_70_features.csv'

def validate_dataset(path=DATA):
    d = pd.read_csv(path, dtype={'ONET_SOC_Code': str})
    skills = sorted(c[:-6] for c in d if c.endswith('_Level'))
    if len(skills) != 35 or set(d.columns) != {'ONET_SOC_Code','Career'} | {s+t for s in skills for t in ('_Level','_Importance')}:
        raise ValueError('Expected identifiers and 35 paired skills')
    if d.isna().any().any() or d.ONET_SOC_Code.duplicated().any() or d.empty:
        raise ValueError('Missing values or duplicate occupation codes')
    for suffix, lo, hi in [('_Level',0,7),('_Importance',1,5)]:
        a = d[[s+suffix for s in skills]].to_numpy(dtype=float)
        if not np.isfinite(a).all() or (a < lo).any() or (a > hi).any():
            raise ValueError('Unexpected numeric range; inspect data before changing normalization')
    report = {'shape':list(d.shape),'skills':skills,'columns':list(d.columns),'level_range':[float(d.filter(regex='_Level$').min().min()),float(d.filter(regex='_Level$').max().max())],'importance_range':[float(d.filter(regex='_Importance$').min().min()),float(d.filter(regex='_Importance$').max().max())],'missing':0,'duplicate_codes':0,'duplicate_titles':int(d.Career.duplicated().sum()),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'examples':d.Career.head(8).tolist()}
    return d, skills, report

def normalize_user_skills(values):
    # User 1..5 -> 0..1. Ordinal self-assessment is only an approximate calibration.
    a=np.asarray(values,dtype=float)
    if not np.isfinite(a).all() or (a<1).any() or (a>5).any(): raise ValueError('Ratings must be finite and between 1 and 5')
    return (a-1)/4

def normalize_onet_levels(values):
    # O*NET's documented LV scale is 0..7. Observed maximum 6 is not the scale maximum.
    a = np.asarray(values,dtype=float)
    if not np.isfinite(a).all() or (a < 0).any() or (a > 7).any():
        raise ValueError('O*NET Level must be finite and within 0..7')
    return a/7

def normalize_importance(values):
    # Observed 1..5 -> 0..1 for interpretable gap prioritization.
    return (np.asarray(values,dtype=float)-1)/4
