"""Locked behavioral copy and pre-change pipeline regression."""
import hashlib,json
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.data import ROOT
from app.services.career_matcher import CareerMatcher
from test_redesign_regression import assert_equivalent
BASELINE=json.loads((ROOT/'reports/behavioral_baseline.json').read_text(encoding='utf8'))
LOCKED=json.loads((ROOT/'tests/locked_questions.json').read_text(encoding='utf8'))

def test_exact_35_locked_thai_questions_and_names():
    skills=json.loads((ROOT/'app/static/skills.json').read_text(encoding='utf8'))
    assert len(skills)==len(LOCKED)==35
    assert set(LOCKED)=={s['id'] for s in skills}
    for s in skills:
        assert s['th']==LOCKED[s['id']]['th']
        assert s['question_th']==LOCKED[s['id']]['question_th']

@pytest.mark.parametrize('field',['question_th','question_en'])
def test_35_nonempty_behavioral_questions(field):
    skills=json.loads((ROOT/'app/static/skills.json').read_text(encoding='utf8'))
    assert len(skills)==35
    assert all(isinstance(s[field],str) and s[field].strip() for s in skills)
    assert len({s[field] for s in skills})==35

def test_behavioral_content_order_and_english_names_unchanged():
    skills=json.loads((ROOT/'app/static/skills.json').read_text(encoding='utf8'))
    immutable=lambda items:[{k:s[k] for k in ('id','en','group')} for s in items]
    assert immutable(skills)==immutable(BASELINE['skills'])
    assert [s['id'] for s in skills]==CareerMatcher().artifact['skills']
    assert all(s['question_th']!=s['description_th'] and s['question_en']!=s['description_en'] for s in skills)

@pytest.mark.parametrize('profile',list(BASELINE['outputs']))
def test_behavioral_api_recommendations_and_gaps_unchanged(profile):
    old=BASELINE['outputs'][profile];m=CareerMatcher()
    assert len(old['values'])==35
    with TestClient(app) as c:
        values=dict(zip(m.artifact['skills'],old['values']))
        response=c.post('/api/match-careers',json={'skills':values});assert response.status_code==200
        actual=response.json()['recommendations']
        assert [r['onet_code'] for r in actual]==[r['onet_code'] for r in old['top10']]
        assert_equivalent(actual,old['top10'])
        assert_equivalent(c.post('/api/career/'+actual[0]['onet_code']+'/skill-gap',json={'skills':values}).json(),old['gaps'])
        if profile in ('doctor','new_prompt_doctor'):
            assert actual[0]['onet_code']=='29-1215.00' and actual[0]['career_en']=='Family Medicine Physicians'

@pytest.mark.parametrize('filename',list(BASELINE['protected_sha256']))
def test_behavioral_data_model_pipeline_files_unchanged(filename):
    assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==BASELINE['protected_sha256'][filename]
