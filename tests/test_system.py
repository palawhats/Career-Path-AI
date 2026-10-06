import hashlib,json,math
import numpy as np
import pandas as pd
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.data import ROOT,validate_dataset,normalize_user_skills,normalize_onet_levels,normalize_importance
from app.services.career_matcher import CareerMatcher,score_from_distance
from app.services.translations import load_career_titles
from app.services.skill_gap import analyze

@pytest.fixture(scope='module')
def matcher():return CareerMatcher()
@pytest.fixture
def ratings(matcher):return {s:3 for s in matcher.artifact['skills']}
@pytest.fixture(scope='module')
def client():
    with TestClient(app) as client:yield client

def test_dataset():
    d,s,r=validate_dataset()
    assert d.shape==(910,72) and len(s)==35
    assert r['level_range']==[0,6] and r['importance_range']==[1,5]
    assert r['missing']==r['duplicate_codes']==0
    assert all(k+'_Importance' in d and k+'_Level' in d for k in s)
    assert r['sha256']=='7777b391793189c942f4020cc53564e9062b700b519f42850b7851c775101f88'
@pytest.mark.parametrize('kind',['duplicate','missing_pair','missing_value','invalid_level','invalid_importance'])
def test_bad_dataset(tmp_path,kind):
    d,s,_=validate_dataset()
    if kind=='duplicate':d=pd.concat([d,d.iloc[:1]])
    if kind=='missing_pair':d=d.drop(columns=s[0]+'_Importance')
    if kind=='missing_value':d.loc[0,s[0]+'_Level']=np.nan
    if kind=='invalid_level':d.loc[0,s[0]+'_Level']=8
    if kind=='invalid_importance':d.loc[0,s[0]+'_Importance']=6
    p=tmp_path/'bad.csv';d.to_csv(p,index=False)
    with pytest.raises(ValueError):validate_dataset(p)
def test_reordered_columns(tmp_path):
    d,s,_=validate_dataset();p=tmp_path/'order.csv';d[list(reversed(d.columns))].to_csv(p,index=False)
    d2,s2,_=validate_dataset(p)
    assert s==s2 and np.allclose(d[[k+'_Level' for k in s]],d2[[k+'_Level' for k in s]])
def test_normalization():
    assert np.allclose(normalize_user_skills([1,3,5]),[0,.5,1])
    assert np.allclose(normalize_onet_levels([0,3.5,7]),[0,.5,1])
    assert normalize_onet_levels([6])[0]==pytest.approx(6/7)
    assert np.allclose(normalize_importance([1,3,5]),[0,.5,1])
@pytest.mark.parametrize('v',[0,6,float('nan'),float('inf')])
def test_bad_user_normalization(v):
    with pytest.raises(ValueError):normalize_user_skills([v])
@pytest.mark.parametrize('v',[-1,8,float('nan')])
def test_bad_level_normalization(v):
    with pytest.raises(ValueError):normalize_onet_levels([v])
def test_model_metadata(matcher):
    metadata=json.loads((ROOT/'models/model_metadata.json').read_text())
    assert metadata['career_count']==910 and metadata['skill_count']==35
    assert metadata['normalization']['level']=='Level / 7'
    assert metadata['feature_names']==matcher.artifact['skills']
    x=matcher.artifact['neighbors']._fit_X
    assert x.shape==(910,35) and np.all((x>=0)&(x<=1))
def test_ten_deterministic_sorted_matches(matcher,ratings):
    r=matcher.match(ratings)
    assert r==matcher.match(ratings) and len(r)==10
    assert [c['rank'] for c in r]==list(range(1,11))
    assert len({c['onet_code'] for c in r})==10
    distances=[c['distance'] for c in r];scores=[c['match_score'] for c in r]
    assert distances==sorted(distances) and scores==sorted(scores,reverse=True)
    assert all(0<=s<=100 for s in scores)
    # Independent reference calculation verifies actual fitted retrieval.
    x=matcher.artifact['neighbors']._fit_X;u=matcher.vector(ratings)
    expected=sorted(zip(np.linalg.norm(x-u,axis=1),matcher.artifact['careers']),key=lambda x:(x[0],x[1]['ONET_SOC_Code']))[:10]
    assert [c['onet_code'] for c in r]==[c['ONET_SOC_Code'] for _,c in expected]
    assert all(c['matching_skills'] for c in r)
@pytest.mark.parametrize('rating',[1,5])
def test_extreme_profiles(matcher,rating):
    r=matcher.match({s:rating for s in matcher.artifact['skills']})
    assert len(r)==10 and all(math.isfinite(c['distance']) for c in r)
def test_score_monotonic():
    assert score_from_distance(0)==100
    assert score_from_distance(math.sqrt(35))==pytest.approx(0)
    assert score_from_distance(.2)>score_from_distance(.3)
    assert score_from_distance(10)==0
    with pytest.raises(ValueError):score_from_distance(-1)
def test_career_raw_values_and_important_order(matcher):
    d,skills,_=validate_dataset();code='15-1252.00';c=matcher.career(code);row=d[d.ONET_SOC_Code==code].iloc[0]
    assert c['career_en']==row.Career and c['onet_code']==code
    assert c['career_th']=='นักพัฒนาซอฟต์แวร์'
    assert len(c['skills'])==35 and len(c['important_skills'])==10
    for r in c['skills']:
        assert r['level']==row[r['skill']+'_Level'] and r['importance']==row[r['skill']+'_Importance']
    assert c['important_skills']==sorted(c['skills'],key=lambda r:(-r['importance'],-r['level'],r['skill']))[:10]
def test_translation_missing_file_and_partial(matcher,tmp_path):
    path=tmp_path/'missing.txt';assert load_career_titles(matcher.artifact['careers'],path)=={}
    path.write_text('15-1252.00|นักพัฒนาซอฟต์แวร์',encoding='utf8')
    titles=load_career_titles(matcher.artifact['careers'],path)
    assert len(titles)==1
    matcher2=CareerMatcher();matcher2.titles_th={}
    c=matcher2.career('15-1252.00');assert c['career_th'] is None and c['career_en']=='Software Developers'
def test_gap_math(matcher,ratings):
    g=matcher.gaps(ratings,'11-1011.00');assert len(g['all_skills'])==35 and len(g['development'])<=5
    for r in g['all_skills']:
        assert r['gap']==pytest.approx(max(0,r['occupational_level']/7-.5))
        assert r['priority']==pytest.approx(r['gap']*(r['importance']-1)/4)
    assert [r['priority'] for r in g['all_skills']]==sorted([r['priority'] for r in g['all_skills']],reverse=True)
    assert all(r['gap']>0 for r in g['development']) and all(r['gap']==0 for r in g['aligned'])
def test_importance_priority_and_no_gap():
    g=analyze(['A','B'],np.array([.25,.25]),np.array([3.5,3.5]),np.array([2.,5.]),{'A':2,'B':2})
    assert [r['skill'] for r in g['development']]==['B','A']
    no=analyze(['A'],np.array([1.]),np.array([3.5]),np.array([5.]),{'A':5})
    assert no['development']==[] and no['aligned'][0]['gap']==0
@pytest.mark.parametrize('kind',['missing','extra','zero','six','bool','fraction','string'])
def test_invalid_api_input(client,ratings,kind):
    p=dict(ratings);key=next(iter(p))
    if kind=='missing':p.pop(key)
    elif kind=='extra':p['unknown']=3
    else:p[key]={'zero':0,'six':6,'bool':True,'fraction':2.5,'string':'3'}[kind]
    assert client.post('/api/match-careers',json={'skills':p}).status_code==422
    assert client.post('/api/career/15-1252.00/skill-gap',json={'skills':p}).status_code==422
def test_apis(client,ratings):
    assert client.get('/health').json()['occupations']==910
    assert client.get('/health').json()['metric']=='euclidean'
    r=client.post('/api/match-careers',json={'skills':ratings})
    assert r.status_code==200 and len(r.json()['recommendations'])==10
    c=client.get('/api/career/15-1252.00').json();assert len(c['skills'])==35
    assert 'match_score' not in c and 'development' not in c
    assert client.post('/api/career/15-1252.00/skill-gap',json={'skills':ratings}).status_code==200
    assert client.get('/api/career/unknown').status_code==404
    assert client.post('/api/career/unknown/skill-gap',json={'skills':ratings}).status_code==404
@pytest.mark.parametrize('url',['/','/assessment','/about','/career/15-1252.00','/static/i18n.js','/static/skills.json','/static/style.css'])
def test_pages(client,url):assert client.get(url).status_code==200
@pytest.mark.parametrize('url',['/roadmap','/api/roadmap','/api/career/15-1252.00/knowledge','/api/career/15-1252.00/software','/api/career/15-1252.00/tasks'])
def test_removed_routes(client,url):assert client.get(url).status_code==404

def test_bilingual_skill_catalog(matcher):
    defs=json.loads((ROOT/'app/static/skills.json').read_text(encoding='utf8'))
    assert len(defs)==35 and {s['id'] for s in defs}==set(matcher.artifact['skills'])
    assert len({s['id'] for s in defs})==35
    assert {s['group'] for s in defs}=={0,1,2,3,4}
    assert all(s['th'] and s['en']==s['id'].replace('_',' ') and s['description_th'] and s['description_en'] for s in defs)
    js=(ROOT/'app/static/app.js').read_text(encoding='utf8')
    assert 'roadmap' not in js.lower() and 'softwareView' not in js
