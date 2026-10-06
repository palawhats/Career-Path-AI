import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from app.main import app
from app.services.data import ROOT
with TestClient(app) as c:
    source=json.loads((ROOT/'reports/examples.json').read_text(encoding='utf8'))[0]
    code=source['top10'][0]['onet_code']
    fixture={'skills':json.loads((ROOT/'app/static/skills.json').read_text(encoding='utf8')),'match':{'recommendations':source['top10']},'career':c.get('/api/career/'+code).json(),'gap':c.post('/api/career/'+code+'/skill-gap',json={'skills':source['35_answers']}).json(),'answers':source['35_answers']}
(ROOT/'tests/ui_fixture.json').write_text(json.dumps(fixture,ensure_ascii=False,indent=2),encoding='utf8')
