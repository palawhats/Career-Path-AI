import hashlib,json
import pytest
from app.services.data import ROOT
BASELINE=json.loads((ROOT/'reports/skill_help_baseline.json').read_text(encoding='utf8'))
def test_skill_help_preserves_current_names_order_and_groups():
    current=json.loads((ROOT/'app/static/skills.json').read_text(encoding='utf8'))
    fields=('id','en','group')  # Thai display names follow the later locked wording.
    assert [{k:s[k] for k in fields} for s in current]==[{k:s[k] for k in fields} for s in BASELINE['skills']]
    assert len(current)==35
@pytest.mark.parametrize('field',['description_th','example_th','description_en','example_en'])
def test_all_35_skill_explanations_nonempty(field):
    current=json.loads((ROOT/'app/static/skills.json').read_text(encoding='utf8'))
    assert all(isinstance(s[field],str) and s[field].strip() for s in current)
@pytest.mark.parametrize('filename',list(BASELINE['protected_sha256']))
def test_skill_help_does_not_modify_pipeline_or_mapping(filename):
    assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==BASELINE['protected_sha256'][filename]
