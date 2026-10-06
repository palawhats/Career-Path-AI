from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI,HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel,Field,ConfigDict
from app.services.data import ROOT,validate_dataset
from app.services.career_matcher import CareerMatcher

@asynccontextmanager
async def lifespan(app):
    _,_,report=validate_dataset()
    app.state.matcher=CareerMatcher()
    if app.state.matcher.artifact['sha256']!=report['sha256']:raise RuntimeError('Dataset changed; rebuild model')
    yield
app=FastAPI(title='Career Path Recommendation and Skill Development System for Students',lifespan=lifespan)

@app.exception_handler(RequestValidationError)
async def invalid_assessment(request,exc):
    # Pydantic rejects non-finite ratings. Do not echo them into strict JSON:
    # NaN/Infinity in the default error payload would otherwise cause a 500.
    errors=[{key:error[key] for key in ('type','loc','msg')} for error in exc.errors()]
    return JSONResponse(status_code=422,content={'detail':errors})

app.mount('/static',StaticFiles(directory=ROOT/'app/static'),name='static')
class Assessment(BaseModel):
    model_config=ConfigDict(extra='forbid')
    skills:dict[str,Annotated[int,Field(strict=True,ge=1,le=5)]]
def guarded(fn):
    try:return fn()
    except ValueError as e:raise HTTPException(422,str(e)) from None
    except KeyError:raise HTTPException(404,'Occupation not found') from None
@app.get('/health')
def health():return {'status':'ok','occupations':len(app.state.matcher.indices),'skills':35,'metric':'euclidean','version':'bilingual-v3'}
@app.get('/api/skills')
def skills():return app.state.matcher.artifact['skills']
@app.post('/api/match-careers')
def match(p:Assessment):return guarded(lambda:{'recommendations':app.state.matcher.match(p.skills)})
@app.get('/api/career/{onet_code}')
def career(onet_code:str):return guarded(lambda:app.state.matcher.career(onet_code))
@app.post('/api/career/{onet_code}/skill-gap')
def gap(onet_code:str,p:Assessment):return guarded(lambda:app.state.matcher.gaps(p.skills,onet_code))
@app.get('/')
@app.get('/assessment')
@app.get('/about')
@app.get('/results')
@app.get('/career/{onet_code}')
def page(onet_code:str|None=None):return FileResponse(ROOT/'app/static/index.html')
