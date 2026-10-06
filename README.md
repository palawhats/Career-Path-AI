# Career Path AI
## ระบบแนะนำเส้นทางอาชีพและทักษะที่ควรพัฒนาสำหรับนักศึกษา

Career Path AI เป็นเครื่องมือสำรวจอาชีพจาก Skill Profile สำหรับนักศึกษามหาวิทยาลัย เหมาะสำหรับผู้ที่กำลังสำรวจเส้นทางอาชีพ ลังเลกับสาขาปัจจุบัน สนใจเปลี่ยนสาย พิจารณาศึกษาสาขาใหม่ หรือต้องการค้นพบอาชีพและทักษะที่อาจพัฒนาเมื่อสนใจเส้นทางนั้น

Career Path AI is a Career Exploration Tool for university students exploring occupations, reconsidering their major, changing fields, or considering new studies. Skill Profile Match indicates similarity, not occupational qualification or a decision about a student's future.

ผลลัพธ์ใช้การประเมินตนเอง 35 ด้านเป็นหลัก ไม่ได้พิจารณาสาขาที่เรียน GPA ผลการเรียน ความสนใจทั้งหมด บุคลิกภาพ ประสบการณ์ทำงานทั้งหมด ค่าใช้จ่ายในการศึกษา เงื่อนไขเข้าศึกษา คุณวุฒิวิชาชีพ ใบอนุญาต หรือเงื่อนไขสมัครงานเฉพาะตำแหน่ง ใช้เพื่อสำรวจและประกอบการตัดสินใจร่วมกับการค้นคว้าและคำแนะนำจากอาจารย์

Results do not incorporate major, GPA, grades, all interests, personality, full work experience, education costs, admission conditions, professional qualifications, licenses, or position-specific hiring requirements. Some occupations need specific education, training, or licensing.

## Reading occupational metrics

Human-readable labels are presentation aids, not official O*NET categorical labels. Raw values remain visible; no model calculations change.

| Metric | UX bands (TH / EN) |
| --- | --- |
| Importance 1–5 | [1,2) น้อย / Low; [2,3) ปานกลาง / Moderate; [3,4) มาก / High; [4,5] มากที่สุด / Very High |
| O*NET Level 0–7 | [0,2.5) ต่ำ / Low; [2.5,5) ปานกลาง / Moderate; [5,7] สูง / High |

Occupational levels in the main skill and development cards display **CareerDisplay5 = 1 + 4 × (O*NET Level / 7)** on a 1–5 scale. Examples: 0 → 1.00; 2.50 → 2.43; 3.75 → 3.14; 7 → 5.00. The original 0–7 value remains in each important-skill disclosure, calculation details and the collapsed full-skill table. Labels still use unrounded original Level and the thresholds above. This display value never feeds CareerNorm, gaps, bars, distances, scores or ranking.

Level describes the occupational profile; it is not a passing score, minimum qualification, or legal requirement. User ratings keep the original assessment anchors. Development cards show a difference in **percentage points** (`Gap × 100`), not a percentage of missing ability. Comparison bars show normalized profiles as percentages for reading only. Native keyboard-accessible **View calculation details / ดูรายละเอียดการคำนวณ** disclosures preserve self-rating, raw Level, normalized values, Importance, Skill Gap, Priority Gap and formulas.

This change is in the existing Git working tree. No commit, push or deployment is performed. See [current UX report](reports/exploration_ux_report.md) for validation and remaining visual checks. Existing audit reports describe earlier revisions.

## Academic explanation: Features, Technique, Output

**FEATURES:** 35 O*NET **Skill Level** features. A student completes the same 35-skill self-assessment with integer ratings 1–5. There is no 70-dimensional student vector.

**TECHNIQUE:** Nearest Neighbors / kNN-style retrieval using **Euclidean Distance**, implemented with a fitted scikit-learn `NearestNeighbors` index. It is similarity retrieval, not supervised classification.

**OUTPUT:** Top 10 occupations with the nearest occupational skill profiles, followed by career details, important skills and skills to develop.

**IMPORTANCE:** The 35 occupational Importance values help interpret careers, resolve explanation ties and prioritize positive skill gaps. They are not extra user features and are not used in the matching distance.

Current flow: Home → five-category self-assessment → Top 10 → Career Detail → important skills and possible development priorities. About explains the method and limitations. The application does not assess interests or generate a Career Roadmap. No LLM, accounts, database or paid API is used.

## Dataset and canonical order

The supplied `data/career_training_data_v2_70_features.csv` is unchanged:

- 910 rows, 910 unique O*NET-SOC codes, 0 duplicate career titles and 0 missing values.
- 72 columns: `ONET_SOC_Code`, `Career`, 35 `_Level` columns and 35 `_Importance` columns.
- Observed Level range 0–6; Importance range 1–5.
- SHA256: `7777b391793189c942f4020cc53564e9062b700b519f42850b7851c775101f88`.

The canonical order is determined by existing CSV skill stems sorted by name in `validate_dataset()`. Model and metadata save that order; runtime constructs vectors by those identifiers rather than request dictionary order. `skills.json` preserves the same order for assessment and Paste Test Values. All eight pipeline surfaces are checked by tests. Categories change presentation only; concatenating categories is not the paste order. Career detail contains all 35 source records; gap records are sorted for priority while retaining their skill IDs.

The exact 35 English names, in order:

Active Learning; Active Listening; Complex Problem Solving; Coordination; Critical Thinking; Equipment Maintenance; Equipment Selection; Installation; Instructing; Judgment and Decision Making; Learning Strategies; Management of Financial Resources; Management of Material Resources; Management of Personnel Resources; Mathematics; Monitoring; Negotiation; Operation and Control; Operations Analysis; Operations Monitoring; Persuasion; Programming; Quality Control Analysis; Reading Comprehension; Repairing; Science; Service Orientation; Social Perceptiveness; Speaking; Systems Analysis; Systems Evaluation; Technology Design; Time Management; Troubleshooting; Writing.

API IDs preserve underscores (for example `Active_Learning`). Complete columns/order appear in `reports/dataset_validation.json` and `models/model_metadata.json`. Thai display names/descriptions are in `app/static/skills.json`; original English O*NET labels and codes remain available. Career translations in `data/career_titles_th.txt` are project-authored, not certified official translations; missing Thai names fall back to English.

The CSV was supplied as O*NET-derived. Its exact upstream release and preprocessing provenance are unavailable. [O*NET's scale documentation](https://www.onetonline.org/help/online/scales) supports Level 0–7 and Importance 1–5; the project assumes the CSV contains raw-scale values. The observed maximum of 6 does not change the Level scale maximum.

## Verified calculations

```text
User normalized             u_i = (rating_i - 1) / 4
Occupation Level normalized c_i = Level_i / 7
Importance normalized       w_i = (Importance_i - 1) / 4
Euclidean distance          d   = sqrt(sum((u_i - c_i)^2)), i = 1..35
Skill Profile Match             = clip(100 * (1 - d / sqrt(35)), 0, 100)
Skill gap                       = max(0, c_i - u_i)
Development priority            = gap_i * w_i
```

Training, saved metadata, runtime and tests use these same formulas. The ten lowest distances are returned, with O*NET-SOC code resolving distance ties. Match Score decreases monotonically as distance increases. Thai label: **ความสอดคล้องของทักษะ**; English: **Skill Profile Match**. It is not probability, AI confidence, aptitude or a guarantee of suitability or success. Display rounding may produce apparent score ties.

Level means the level of skill use associated with the occupation; Importance means how important it is to that occupation. Thai UI distinguishes **ระดับทักษะที่ต้องใช้** (0–7) and **ความสำคัญต่ออาชีพ** (1–5). User self-ratings are compared with normalized Level, never Importance. The ordinal self-assessment scale is uncalibrated; equal normalized scales do not establish objective ability equivalence.

The career API returns 10 important skills sorted by Importance, then Level and ID; the UI previews the first 5. All 35 raw skills are available in a collapsed table. Positive gaps are prioritized, then the top 5 are shown. Zero-gap skills are listed separately. Comparison bars use the same normalized 0–1 scale, with numerical labels. These are development suggestions based on self-assessment, not qualification requirements.

Direct career links work without answers: source skills remain visible and personalized results prompt the user to complete the assessment.

## Architecture, language and privacy

A single same-origin HTML/CSS/JavaScript shell calls FastAPI/Pydantic and the trusted saved model. Production paths use `Path(__file__)`; fetch URLs are relative. No Windows paths, external fonts or localhost dependencies exist in production application code. CSS uses local Thai fonts and responsive cards.

Thai is default; ไทย | EN switches the centralized `i18n.js` catalog. Language persists in localStorage. Answers/step persist in sessionStorage; switching language does not alter answers, ranking, scores, cached results or route. Refresh restores valid answers and recomputes results. The Clear Responses action clears manual and pasted answers. Closing a normal tab ends the session, though browser session restoration can vary. Application code does not write ratings to a database or log request bodies.

**Paste Test Values / วางค่าทดสอบ** is labelled **For system testing / สำหรับทดสอบระบบ**. It accepts exactly 35 integer values 1–5 separated by commas, spaces or newlines, validates atomically, uses the existing canonical definitions, updates all answers/progress/session state and closes the dialog. It never evaluates code, accepts a career target, forces ranking or submits automatically. The user navigates to the last category and presses Analyze Results.

## APIs and validation

| Method | Route | Purpose |
|---|---|---|
| GET | `/`, `/assessment`, `/results`, `/about`, `/career/{code}` | Shared frontend shell |
| GET | `/api/skills` | Canonical 35 skill IDs |
| POST | `/api/match-careers` | Top 10 matches |
| GET | `/api/career/{code}` | Source career/important/all skills |
| POST | `/api/career/{code}/skill-gap` | Personalized gaps/priorities |
| GET | `/health` | status, 910 occupations, 35 skills, Euclidean metric/version |

POST body: `{"skills": {"Active_Learning": 3, ...all 35 identifiers...}}`.

Only strict integers 1–5 are accepted. Missing, extra, unknown, boolean, decimal, string, null, HTML/JS, NaN and Infinity inputs are rejected with 422. Invalid JSON is rejected. Unknown careers return 404. Validation error responses retain `detail`, `type`, `loc`, and `msg` and omit raw inputs/context so non-finite values cannot break strict JSON serialization. Successful API response contracts are unchanged. `/docs` provides the schema.

## Local run and tests

Python 3.12; clean audit used 3.12.14. Production Python dependencies are in `requirements.txt`; development-only Python dependencies are in `requirements-dev.txt`. Frontend tests require a compatible Node version; tested Node **24.18.0** and npm **11.16.0**. jsdom 30.1.1 supports Node `^22.22.2 || ^24.15.0 || >=26.0.0`.

From the project root (a fresh ZIP checkout):

```sh
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux instead:
# source .venv/bin/activate
python -m pip install -r requirements.txt
# The supplied trusted model is ready; rebuild only if required:
# python train_model.py
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Development verification:

```sh
python -m pip install -r requirements-dev.txt
python -m pip check
python -m pytest -q
npm ci
npm test
```

`package-lock.json` pins jsdom and its transitive development dependencies. No external NODE_PATH or scratch dependency directory is needed. npm/jsdom are not required for production. If host-owned pytest cache/temp directories have access errors, use a fresh temp directory and `-p no:cacheprovider --basetemp <new-directory>`; this does not skip tests.

Earlier behavioral revision gates: **136 Python passed + 44 JavaScript passed = 180 passed, 0 failed**. Current exploration UX gates: **152 Python + 50 JavaScript = 202 passed, 0 failed**. One existing Starlette/httpx deprecation warning is non-failing. Coverage includes data/model/order, strict input rejection for both POST routes, all 35 answers, bilingual/paste behavior, exact Top 10 identities, numerical regression, physician demo, representative field retrieval and refresh. Float regression uses absolute tolerance `1e-12`, relative tolerance `0`; identities, rank and ordering stay exact. Changes larger than tolerance and reordered careers are explicitly tested to fail.

DOM tests use actual API fixtures and mock only native dialog lifecycle because JSDOM lacks `showModal`/`close`. They do not prove rendered layout or native keyboard/focus behavior. Actual browser/mobile verification is pending because saved Browser permission blocks local navigation.

Reproducible illustrative examples:

```sh
python examples.py
python tests/build_ui_fixture.py
```

These produce `reports/examples.md/json` and `tests/ui_fixture.json`. Inputs are constructed demonstrations, not real students. The fixed doctor vector appears in `tests/test_final_audit.py` and actual API responses in `tests/doctor_fixture.json`; it naturally retrieves **Family Medicine Physicians (29-1215.00), rank 1**.

## Controlled Retrieval Tests and limitations

Six representative occupations (healthcare, education, legal, software, civil engineering and robotics) were tested by quantizing their source profiles to integer self-assessment-like values. Each corresponding target appeared at rank 1 in the executed checks. These are **Controlled Retrieval Tests**, not evidence of real student career suitability.

`train_model.py` also records synthetic self/perturbation retrieval diagnostics with seed 2026 and Gaussian noise sigma 0.05. Reports are labelled synthetic/controlled. There is no verified student-profile → correct-career labeled dataset and no claimed student-career Accuracy, Precision, Recall or F1.

Self-assessment bias, ordinal calibration, unknown CSV release/transformation, uncertified Thai translation and missing interest/context/job-market information limit interpretation. Recommendations support exploration and advising. They do not replace counseling or determine the objectively correct career.

## Render deployment

`render.yaml` matches [Render's FastAPI instructions](https://render.com/docs/deploy-fastapi) and [Python version configuration](https://render.com/docs/python-version). It pins Python **3.12.10** (same CPython 3.12 ABI as the clean audit environment).

1. Put this project's contents at the repository root and push to your chosen GitHub repository.
2. Connect the repository to a Render Blueprint using `render.yaml`, or create a Python Web Service with these settings.
3. Build: `pip install -r requirements.txt && python train_model.py`.
4. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
5. Health check: `/health`; `PYTHON_VERSION=3.12.10`.
6. Verify the deployed public HTTPS URL using [the 17-item smoke checklist](reports/deployment_smoke_checklist.md).

Training was run twice in an isolated copy; artifacts were identical across the two builds and fitted profiles matched the unchanged submission model. All pinned production packages and resolved transitive packages have Python 3.12 Linux-compatible wheels. Local production-command smoke testing verified PORT, actual HTTP routes/static files, UTF-8, doctor matching and non-finite input rejection. There is no Linux runtime on this host; Linux/Render execution and the public smoke checklist remain unperformed. Do not interpret wheel resolution as successful public deployment.

## Skill explanations and rating guidance

All35 existing skill definitions in app/static/skills.json contain description_th, example_th, description_en and example_en. On Assessment, the accessible ⓘ Explanation button expands that skill’s explanation and example in normal flow above its rating options. Only the selected skill’s help is open. Language switching preserves the open skill, rating guide, current answers and progress. Help state stays in memory; a full reload can close it without affecting saved answers. “ให้คะแนนอย่างไร?” / “How should I rate my skills?” explains all five anchors and asks students to rate their current ability without comparing themselves with others. This is presentation only: same1–5 values, canonical ordering, paste mapping and ML pipeline.

Complete reviewed text: reports/skill_explanations_review.md. Current verification/report: reports/skill_help_verification.json and reports/skill_help_report.md. The final pre-deployment audit’s earlier counts are historical; that revision passed136 Python and44 JavaScript tests. Render/browser acceptance limitations remain unchanged.

## Locked behavioral questions — current assessment

Every one of the35 existing records now contains question_th and question_en. The Thai main questions and display names use the user-approved locked wording exactly. The behavioral question is always visible between the skill name and information button; additional meaning/examples stay in the expandable panel. Global instructions say to rate current ability without comparing with others, and that no experience can be rated1 without guessing. The same final1–5 scale is used across all questions: ยังทำไม่ได้ / แทบไม่มีประสบการณ์; ทำได้เล็กน้อย; ทำได้พอสมควร; ทำได้ดี; ทำได้ดีมาก. Buttons may shorten these labels; the full meanings are in the guide and radio accessible labels. Numeric values/formulas are unchanged.

Current report/evidence: reports/behavioral_report.md, behavioral_verification.json and complete copy review behavioral_questions_review.md. All6 before/after fixed profiles retain identical ranks, distances, scores and gap records; both doctor vectors return29-1215.00 first. That revision passed136 Python and44 JavaScript tests. Current suites pass152 Python and50 JavaScript tests. This local revision has not been redeployed to the user's public service.

Current display-scale change and verification: [1–5 display report](reports/display5_report.md). This change continues the existing uncommitted UX work; no commit/push/deployment occurs.
