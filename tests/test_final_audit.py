"""Final input/canonical/retrieval checks against actual HTTP routes and saved index."""
import json
import numpy as np
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.data import ROOT,validate_dataset
from app.services.career_matcher import CareerMatcher

@pytest.fixture(scope='module')
def final_client():
    with TestClient(app,raise_server_exceptions=False) as client:yield client

@pytest.mark.parametrize('route',['/api/match-careers','/api/career/29-1215.00/skill-gap'])
@pytest.mark.parametrize('bad',[float('nan'),float('inf'),float('-inf'),True,0,6,2.5,'3','<script>alert(1)</script>',None])
def test_invalid_ratings_rejected_as_json_not_server_error(final_client,route,bad):
    skills=final_client.get('/api/skills').json();values=dict.fromkeys(skills,3);values[skills[0]]=bad
    r=final_client.post(route,content=json.dumps({'skills':values}),headers={'Content-Type':'application/json'})
    assert r.status_code==422
    def disallow(value):raise AssertionError('Nonstandard JSON response '+value)
    assert 'detail' in json.loads(r.text,parse_constant=disallow)
    assert all(set(error)=={'type','loc','msg'} for error in r.json()['detail'])

@pytest.mark.parametrize('route',['/api/match-careers','/api/career/29-1215.00/skill-gap'])
@pytest.mark.parametrize('body',['{bad json','null','[]','{"skills":{},"extra":3}','{"skills":{"Active_Learning":1e309}}'])
def test_malformed_requests_rejected(final_client,route,body):
    assert final_client.post(route,content=body,headers={'Content-Type':'application/json'}).status_code==422

@pytest.mark.parametrize('route',['/api/match-careers','/api/career/29-1215.00/skill-gap'])
@pytest.mark.parametrize('defect',['missing','extra','unknown','outer_extra'])
def test_exact_assessment_contract(final_client,route,defect):
    skills=final_client.get('/api/skills').json();values=dict.fromkeys(skills,3);body={'skills':values}
    if defect=='missing':values.pop(skills[0])
    if defect=='extra':values['ExtraSkill']=3
    if defect=='unknown':values['UnknownSkill']=values.pop(skills[0])
    if defect=='outer_extra':body['occupation']='29-1215.00'
    assert final_client.post(route,json=body).status_code==422

def test_entire_canonical_pipeline(final_client):
    _,csv_order,_=validate_dataset();m=CareerMatcher()
    ui=json.loads((ROOT/'app/static/skills.json').read_text(encoding='utf8'))
    metadata=json.loads((ROOT/'models/model_metadata.json').read_text(encoding='utf8'))
    assert [s['id'] for s in ui]==final_client.get('/api/skills').json()==csv_order==m.artifact['skills']==metadata['feature_names']
    assert [s['skill'] for s in final_client.get('/api/career/29-1215.00').json()['skills']]==csv_order
    gaps=final_client.post('/api/career/29-1215.00/skill-gap',json={'skills':dict.fromkeys(csv_order,3)}).json()
    assert len(gaps['all_skills'])==35 and {s['skill'] for s in gaps['all_skills']}==set(csv_order)
    for index,skill in enumerate(csv_order):
        vector=m.vector({s:5 if s==skill else 1 for s in csv_order})
        assert vector.shape==(35,) and vector[index]==1 and vector.sum()==1

@pytest.mark.parametrize('title',[
    'Family Medicine Physicians',
    'Elementary School Teachers, Except Special Education',
    'Lawyers','Software Developers','Civil Engineers','Robotics Technicians'])
def test_controlled_integer_retrieval_across_fields(final_client,title):
    # Quantized source occupational profiles, not measured student outcomes.
    m=CareerMatcher();index=next(i for i,c in enumerate(m.artifact['careers']) if c['Career']==title)
    values=np.rint(1+4*m.artifact['neighbors']._fit_X[index]).astype(int).tolist()
    r=final_client.post('/api/match-careers',json={'skills':dict(zip(m.artifact['skills'],values))})
    assert r.status_code==200
    records=r.json()['recommendations'];assert len(records)==10
    assert m.artifact['careers'][index]['ONET_SOC_Code'] in [c['onet_code'] for c in records]

def test_supplied_doctor_vector_production_pipeline(final_client):
    values=[3,4,3,3,4,1,1,1,3,4,3,2,2,3,3,3,3,1,3,2,3,1,2,4,1,3,3,3,4,3,3,1,3,1,3]
    r=final_client.post('/api/match-careers',json={'skills':dict(zip(final_client.get('/api/skills').json(),values))})
    assert r.status_code==200
    first=r.json()['recommendations'][0]
    assert first['onet_code']=='29-1215.00' and first['career_en']=='Family Medicine Physicians'
