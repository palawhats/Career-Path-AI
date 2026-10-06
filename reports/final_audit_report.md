> Historical pre-deployment audit. Current presentation additions and complete test counts are documented in [skill_help_report.md](skill_help_report.md). Model, backend, deployment settings and data remain as audited below.

# FINAL AUDIT REPORT — Career Path AI

**FINAL STATUS: READY TO DEPLOY**

Scope: all automated pre-deployment gates passed. This is readiness to deploy, not evidence of public deployment or rendered desktop/mobile acceptance. Public smoke tests and browser visual checks remain unperformed and are explicitly listed below.

## 1. Files changed

Application: `app/main.py`, `app/static/app.js`, `app/static/i18n.js`, `app/static/index.html`.

Tests/dependency reproducibility: `tests/test_redesign_regression.py`, `tests/test_final_audit.py` (new), `tests/ui.test.cjs`, `tests/ui_fixture.json` (regenerated), `tests/doctor_fixture.json` (new), `package-lock.json` (new).

Documentation/evidence: README.md rewritten; final_audit_report.md, final_audit_before.json, final_audit_results.json, final_build_verification.json/log, final_environment_verification.json, final_production_smoke_log.txt, deployment_smoke_checklist.md, complete Python/JavaScript result logs; examples regenerated with current translations. Earlier implementation reports are labelled historical.

Unchanged: CSV, 910 occupations, canonical skills.json ordering/IDs/English names, model.pkl, model metadata, train_model.py, matching/data/gap services, Thai career mapping, CSS design, requirements files, package.json and Render configuration.

## 2. Bugs found

- Reproduced genuine API bug: request ratings NaN, Infinity and -Infinity were rejected by strict Pydantic validation, but the default validation-error response echoed non-finite inputs. Strict JSON serialization then failed, returning HTTP500 instead of422. Evidence: final_audit_before.json.
- Existing regression assertions compared nested floating values exactly. Four failures reported by the external audit did not reproduce here: the initial full57 tests passed and the original protected source/model hashes matched. An independent direct Euclidean norm calculation produced the same ordering but differences up to 2.775557561562891e-15; this is consistent with floating accumulation roundoff, not a changed algorithm. No external failure log was available to identify its exact platform-specific path.
- Standard JavaScript tests depended on declared jsdom but no lock/project-local installation had been delivered previously; earlier local testing used an external dependency directory. npm install/ci now resolve dependencies inside this project.
- README contained obsolete counts, old background-illustration language, and conflicting appended version summaries. Some Level/Importance wording lacked the instructor's explicit distinction.

## 3. Bugs fixed

- Added a RequestValidationError handler returning422 with type/loc/msg without echoing raw input/context. Success-response contracts and input validators are unchanged. Both POST APIs now reject non-finite/malformed values safely.
- Regression comparison requires exact nested structure, identities, ranks and list order; only floating values use pytest.approx with abs=1e-12 and rel=0. Tests prove roundoff is accepted, a2e-12 deviation is rejected and swapping career codes fails. The original stored baseline was not rewritten.
- Historical hash assertion intentionally excludes app/main.py after this reviewed error-handler change; all calculation/data/model hashes remain required unchanged, and new API tests cover the application change.
- Installed declared JS dev dependencies with npm install and then npm ci. Added package-lock.json. No production Node dependency was added.
- Clarified Level/Importance labels and their separate explanations in both languages, updated the asset cache version, and consolidated current documentation. Paste parser/functionality and design were preserved.

## 4. Dataset validation — PASS

Programmatic validation:910 rows,910 unique O*NET-SOC codes,0 duplicate codes,0 duplicate titles,0 missing values,72 columns,35 Level and35 Importance columns. Numeric values are finite; observed Level0–6 and Importance1–5. No verified source defect was found and the CSV was not edited.

SHA256: `7777b391793189c942f4020cc53564e9062b700b519f42850b7851c775101f88`.

## 5. Model validation — PASS

Trusted joblib model loads in a fresh isolated venv (`include-system-site-packages=false`). Fitted index has910x35 dimensions; metadata, raw CSV values, raw levels/importance and canonical feature order agree. Euclidean/brute/n_jobs=1 configuration remains intact.

Train_model.py was executed twice in an isolated project copy, leaving the submitted model untouched. Both build files had SHA256 `fdd0a50265bc776045d1ae08025667f45a864757b597104b35530f904ba6333e`. Rebuilt vectors, raw arrays, identities, normalization and fitted index exactly equal the current model. Fixed-vector ranks/scores remain equivalent. The clean environment used Python3.12.14 on Windows; no Linux execution is claimed.

## 6. Features used — PASS

Exactly35 O*NET Skill Level dimensions and35 integer1–5 student ratings. Importance is retained for interpretation/explanation and development priority; it is not an extra user feature. CSV-sorted canonical IDs agree with UI definitions, paste mapping, API IDs, preprocessing, model/metadata, matching, career detail and gap identities. Category display order and priority-sorted gap output do not reindex the vector.

## 7. Technique used — PASS

Nearest Neighbors/kNN-style retrieval using Euclidean Distance over35 normalized Level features. Top10 use ascending distance and O*NET-SOC tie ordering. No classifier, clustering, LLM, random score, hard-coded occupation insertion or ranking manipulation was introduced.

## 8. Normalization verified — PASS

User=(rating-1)/4; occupational Level=Level/7; normalized Importance=(Importance-1)/4. Score=clip(100*(1-distance/sqrt(35)),0,100). Gap=max(0,Level/7-user); priority=gap*normalizedImportance. Training, saved metadata, runtime and tests agree. Score is monotonic and means Skill Profile Match/ความสอดคล้องของทักษะ, not probability or success certainty.

[O*NET documents the raw scales](https://www.onetonline.org/help/online/scales). The CSV's exact upstream release/transformation remains unknown; raw-scale semantics are an explicit assumption. Current normalization was not changed.

## 9. Python test result — PASS

**103 passed,0 failed**, complete suite in a clean venv with pinned requirements-dev.txt. One existing non-failing Starlette/httpx deprecation warning. Includes full original suites, stricter float regression and46 new input/canonical/controlled-retrieval cases. Old cache/temp directories had host access issues, so the audit used a new basetemp and disabled only pytest's cache provider. No tests were excluded.

Exact audit command from project root:

```powershell
..\..\work\final-audit-venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --basetemp ../../work/final-after-temp
```

This command names the audit host's fresh environment. Portable checkout instructions are in section17/README.

## 10. JavaScript test result — PASS

**35 passed,0 failed**, using project-local npm dependencies with Node24.18.0/npm11.16.0. Commands: npm install --ignore-scripts --no-audit --no-fund; npm ci --ignore-scripts --no-audit --no-fund; npm test. jsdom is declared in package.json and all lockfile packages are development-only. NODE_PATH is unnecessary. Two new tests cover the actual recorded doctor API fixture through paste/normal analysis/detail/bilingual flow and refresh/session restoration.

## 11. Doctor retrieval result — PASS

The exact supplied35-value vector was passed through the actual API and live production-command HTTP server. Rank1: **Family Medicine Physicians (29-1215.00)**, distance 0.409775946745, Skill Profile Match 93.073522302464%. Returned naturally by the unchanged saved index. No career name/target is an API matching input.

## 12. Other retrieval sanity checks — PASS

Source occupation profiles were quantized with round(1+4*normalizedLevel) into integers1–5, then passed through the actual matching API. The following are Controlled Retrieval Tests, not real-world prediction accuracy:

| Field | Target | Code | Observed target rank |
|---|---|---|---:|
| Healthcare | Family Medicine Physicians | 29-1215.00 | 1 |
| Education | Elementary School Teachers, Except Special Education | 25-2021.00 | 1 |
| Legal | Lawyers | 23-1011.00 | 1 |
| Computer/IT | Software Developers | 15-1252.00 | 1 |
| Engineering | Civil Engineers | 17-2051.00 | 1 |
| Technical | Robotics Technicians | 17-3024.01 | 1 |

Five fixed vectors (ones, threes, fives, cycle and supplied doctor) retained identical Top10 ordering before/after this final fix. Measured distance/score drift in this environment was0. Tolerance exists for legitimate cross-platform roundoff, not to conceal output changes. Actual inputs/results are saved in final_audit_results.json.

## 13. Thai/English verification — PASS for automated behavior

Thai defaults; centralized catalogs have equal nonempty keys; language switching preserves ratings/step, current route, rankings/scores and cached results. Fallback to original English career names works. All35 original English skill labels and910 O*NET codes remain unchanged. Skill labels/descriptions were reviewed during the prior redesign and retained in this final fix. Current Level label is ระดับทักษะที่ต้องใช้ with อาชีพนี้ต้องใช้ทักษะนี้ในระดับใด; Importance is ความสำคัญต่ออาชีพ with ทักษะนี้สำคัญต่ออาชีพมากน้อยเพียงใด. Cautious skills-to-develop explanation remains.

## 14. Input validation verification — PASS

Both matching and skill-gap endpoints reject missing/extra/unknown IDs, outer extra fields, bool, strings, null,0,6, decimals, HTML/JS, NaN/Infinity and malformed JSON with422. Actual live HTTP confirms non-finite rejection no longer returns500. Paste accepts exactly35 valid integers atomically and preserves canonical order, controls, progress, session state, language and normal explicit Analyze flow. It does not execute pasted text or accept a target occupation. Tests retain all existing invalid count/separator/range cases.

## 15. Render deployment verification — PASS for configuration/preflight

Existing render.yaml uses Python3.12.10, correct application module app.main:app, production install/train build, 0.0.0.0:$PORT startup and /health. Verified against [Render's FastAPI deployment documentation](https://render.com/docs/deploy-fastapi) and [Python version settings](https://render.com/docs/python-version). No Windows paths or localhost dependencies are present in production source. All actual third-party production imports are declared; pip check reports no broken requirements.

Pip resolved and downloaded all pinned production packages/transitive dependencies as Python3.12-compatible Linux wheels (including manylinux x86_64 numerical packages). This verifies dependency availability, not a Linux runtime execution.

A clean-environment subprocess was started using the actual uvicorn module with host0.0.0.0 and PORT environment value8012. Real HTTP verified /health, all page routes, all static files, Thai UTF-8, Top10 doctor matching and422 rejection. Server stopped after testing. Build retraining was verified twice separately.

No public Render service or URL was deployed/tested. All17 public smoke checklist items are pending in deployment_smoke_checklist.md.

## 16. Remaining limitations

- Actual375/768/1440px rendering, native dialog/focus and mobile usability checks are pending. Saved Browser permission blocks local navigation; no alternate browser/raw-CDP workaround was used. JSDOM DOM/state tests are not layout verification.
- There is no Linux runtime/distro on this host. Linux wheels and portable paths pass preflight; actual Linux/Render execution must be confirmed during deployment.
- Public HTTPS deployment smoke checklist is not executed. READY TO DEPLOY does not mean already deployed or instructor visual acceptance completed.
- Self-assessment is ordinal, biased and uncalibrated; no labeled student-to-correct-career ground truth exists. No real student suitability Accuracy/Precision/Recall/F1 is claimed. Controlled/synthetic retrieval is not success prediction.
- Original CSV upstream release/transformation and professional certification of Thai translations are unavailable. Interests, personality, geography, opportunity and qualifications are not assessed.
- Existing Starlette/httpx test-client deprecation warning remains; all tests pass without changing production dependencies just to suppress it.

## 17. Exact commands to deploy/run

From a fresh project root:

```sh
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux/macOS instead:
# source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip check
python -m pytest -q
npm ci
npm test
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Node/npm are needed for development tests only. To reproduce a model build: python train_model.py. For production install only requirements.txt.

Render Blueprint: connect a repository whose root contains this project and select render.yaml. Manual Python Web Service settings:

```sh
# Build
pip install -r requirements.txt && python train_model.py
# Start (Render's shell expands PORT)
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

PYTHON_VERSION=3.12.10; healthCheckPath=/health. After deployment, use the actual public HTTPS URL and complete deployment_smoke_checklist.md. No repository push, hosting payment or publication was performed by this audit.
