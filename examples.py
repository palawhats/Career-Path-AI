"""Reproduce three illustrative input profiles through the actual API (not student data)."""
import json
from fastapi.testclient import TestClient
from app.main import app
from app.services.data import ROOT,validate_dataset

def run():
    _,skills,_=validate_dataset()
    technical={'Programming','Technology_Design','Troubleshooting','Systems_Analysis','Systems_Evaluation','Operations_Analysis','Operations_Monitoring','Operation_and_Control','Equipment_Selection','Equipment_Maintenance','Installation','Repairing','Quality_Control_Analysis','Mathematics','Science','Complex_Problem_Solving','Critical_Thinking'}
    social={'Active_Listening','Speaking','Writing','Social_Perceptiveness','Service_Orientation','Persuasion','Negotiation','Instructing','Coordination','Reading_Comprehension'}
    management={'Management_of_Financial_Resources','Management_of_Material_Resources','Management_of_Personnel_Resources','Time_Management','Monitoring','Judgment_and_Decision_Making','Coordination','Negotiation','Persuasion','Speaking','Critical_Thinking','Complex_Problem_Solving'}
    examples=[]
    with TestClient(app) as client:
        for label,high in [('A — Technical-oriented',technical),('B — Social/service-oriented',social),('C — Management-oriented',management)]:
            ratings={s:4 if s in high else 2 for s in skills}
            r=client.post('/api/match-careers',json={'skills':ratings});r.raise_for_status();recommendations=r.json()['recommendations']
            code=recommendations[0]['onet_code']
            career=client.get('/api/career/'+code).json()
            gaps=client.post('/api/career/'+code+'/skill-gap',json={'skills':ratings}).json()
            examples.append({'example':label,'note':'Constructed illustrative input, not measured student data; outputs executed through actual API.','35_answers':ratings,'top10':recommendations,'selected_career':career,'important_skills':career['important_skills'],'skills_to_develop':gaps['development']})
    (ROOT/'reports/examples.json').write_text(json.dumps(examples,ensure_ascii=False,indent=2),encoding='utf8')
    text='# Three reproducible examples\n\nIllustrative input profiles constructed for testing, not real student observations. All outputs below come from executed FastAPI endpoints and the saved model. Rerun `python examples.py`.\n'
    for e in examples:
        text+='\n## '+e['example']+'\n\n### All 35 answers\n\n| Skill | Self-rating |\n|---|---:|\n'
        text+=''.join('| '+s.replace('_',' ')+' | '+str(v)+' |\n' for s,v in e['35_answers'].items())
        text+='\n### Top 10 actual results\n\n| Rank | O*NET-SOC | Occupation | Distance | Match Score |\n|---:|---|---|---:|---:|\n'
        text+=''.join(f"| {c['rank']} | {c['onet_code']} | {c['career_en']} | {c['distance']:.6f} | {c['match_score']:.4f} |\n" for c in e['top10'])
        c=e['selected_career'];text+=f"\nSelected: **{c['career_en']}** ({c['onet_code']}).\n\n### Important skills\n\n| Skill | Level (0–7) | Importance (1–5) |\n|---|---:|---:|\n"
        text+=''.join(f"| {r['skill'].replace('_',' ')} | {r['level']} | {r['importance']} |\n" for r in e['important_skills'])
        text+='\n### Skills to develop\n\n| Skill | Self-rating | Occupational Level | Importance | Gap | Priority |\n|---|---:|---:|---:|---:|---:|\n'
        text+=''.join(f"| {r['skill'].replace('_',' ')} | {r['self_rating']} | {r['occupational_level']} | {r['importance']} | {r['gap']:.6f} | {r['priority']:.6f} |\n" for r in e['skills_to_develop']) or '| No positive gaps | | | | | |\n'
    (ROOT/'reports/examples.md').write_text(text,encoding='utf8')
    print([(e['example'],e['top10'][0]['career_en']) for e in examples])
if __name__=='__main__':run()
