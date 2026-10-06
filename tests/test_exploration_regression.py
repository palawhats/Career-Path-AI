"""Same-input API rankings and raw calculations captured before this UX change."""
import json,hashlib
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.data import ROOT
from test_redesign_regression import assert_equivalent
BASE=json.loads((ROOT/'reports/exploration_baseline.json').read_text(encoding='utf8'))
@pytest.mark.parametrize('name',list(BASE['outputs']))
def test_exploration_rankings_and_raw_gaps_unchanged(name):
    old=BASE['outputs'][name]
    with TestClient(app) as c:
        skills=c.get('/api/skills').json()
        ratings=dict(zip(skills,old['values']))
        rows=c.post('/api/match-careers',json={'skills':ratings}).json()['recommendations']
        assert_equivalent(rows,old['top10'])
        gaps=c.post('/api/career/'+rows[0]['onet_code']+'/skill-gap',json={'skills':ratings}).json()
        assert_equivalent(gaps,old['gaps'])
@pytest.mark.parametrize('file',list(BASE['protected_sha256']))
def test_exploration_protected_files(file):
    assert hashlib.sha256((ROOT/file).read_bytes()).hexdigest()==BASE['protected_sha256'][file]
