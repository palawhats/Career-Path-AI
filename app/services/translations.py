"""Reuse existing project-authored Thai titles; missing entries safely fall back to English."""
from .data import ROOT

def load_career_titles(careers,path=None):
    path=path or ROOT/'data/career_titles_th.txt'
    allowed={c['ONET_SOC_Code'] for c in careers}
    if not path.exists(): return {}
    titles={}
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        if not line.strip():continue
        code,title=line.split('|',1)
        if code in titles or not title.strip():raise ValueError('Duplicate code or empty Thai title')
        if code in allowed:titles[code]=title.strip()
    return titles
