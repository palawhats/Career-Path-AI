"""Regression evidence captured from the current project before any redesign edit."""
import hashlib,json
import pytest
from app.services.data import ROOT
from app.services.career_matcher import CareerMatcher

BASELINE=json.loads((ROOT/'reports/redesign_baseline.json').read_text(encoding='utf8'))

ABS_TOL=1e-12
def assert_equivalent(actual,expected):
    """Exact structure/order/identities; absolute-only tolerance for float values."""
    if isinstance(expected,float):
        assert isinstance(actual,(int,float)) and not isinstance(actual,bool)
        assert actual==pytest.approx(expected,rel=0,abs=ABS_TOL)
    elif isinstance(expected,dict):
        assert isinstance(actual,dict) and actual.keys()==expected.keys()
        for key in expected:assert_equivalent(actual[key],expected[key])
    elif isinstance(expected,list):
        assert isinstance(actual,list) and len(actual)==len(expected)
        for left,right in zip(actual,expected):assert_equivalent(left,right)
    else:
        assert actual==expected


# app/main.py now has a reviewed validation-error fix; calculation/data/model
# files remain protected. The original recorded baseline is not rewritten.
@pytest.mark.parametrize('filename',[p for p in BASELINE['protected_sha256'] if p!='app/main.py'])
def test_redesign_protected_files_unchanged(filename):
    assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==BASELINE['protected_sha256'][filename]

def test_redesign_skill_order_and_mapping_unchanged():
    current=json.loads((ROOT/'app/static/skills.json').read_text(encoding='utf8'))
    # UX content is editable; canonical identities, English names and groups are not.
    immutable=lambda entries:[{k:s[k] for k in ('id','en','group')} for s in entries]
    assert immutable(current)==immutable(BASELINE['skills'])
    matcher=CareerMatcher()
    assert [s['id'] for s in current]==matcher.artifact['skills']
    assert len(matcher.artifact['careers'])==BASELINE['occupation_count']==910

@pytest.mark.parametrize('profile',list(BASELINE['outputs']))
def test_redesign_fixed_vector_outputs_unchanged(profile):
    matcher=CareerMatcher();before=BASELINE['outputs'][profile]
    ratings=dict(zip(matcher.artifact['skills'],before['values']))
    after=[{k:v for k,v in c.items() if k!='career_th'} for c in matcher.match(ratings)]
    assert [r['onet_code'] for r in after]==[r['onet_code'] for r in before['recommendations']]
    assert_equivalent(after,before['recommendations'])
    assert_equivalent(matcher.gaps(ratings,after[0]['onet_code']),before['gaps'])
    assert len(after)==10
    if profile=='doctor':assert after[0]['career_en']=='Family Medicine Physicians'


def test_numeric_tolerance_accepts_only_roundoff():
    assert_equivalent({'distance':1.0+5e-13},{'distance':1.0})
    with pytest.raises(AssertionError):assert_equivalent({'distance':1.0+2e-12},{'distance':1.0})
    with pytest.raises(AssertionError):assert_equivalent([{'code':'A'},{'code':'B'}],[{'code':'B'},{'code':'A'}])
    with pytest.raises(AssertionError):assert_equivalent({'distance':float('nan')},{'distance':1.0})
