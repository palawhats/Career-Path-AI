# Behavioral assessment final UX report

**FINAL STATUS: PASS** — all automated critical content/mapping/ML regressions pass. Actual rendered mobile/browser checks remain pending and are not claimed passed.

## 1. Files changed

app/static/skills.json, app/static/app.js, app/static/i18n.js, app/static/style.css, app/static/index.html, tests/test_skill_help.py, tests/ui.test.cjs, tests/ui_fixture.json, README.md, test-result logs. Added tests/locked_questions.json (approved Thai text keyed by ID), tests/test_behavioral_questions.py, reports/behavioral_baseline.json, behavioral_verification.json, behavioral_questions_review.md and this report. Earlier skill-help reports are marked historical.

No dependencies or deployment architecture changed. No redesign of results or career-detail pages.

## 2. Content location

app/static/skills.json remains the sole ordered frontend skill definition list. Each existing record now adds question_th and question_en, alongside original English O*NET name, approved Thai display name, descriptions/examples and group. Thai questions were extracted directly from the supplied locked text and matched by original English name/ID, not rewritten. tests/locked_questions.json independently preserves approved names/questions for exact-copy checks; it is a keyed test fixture, not another production order.

## 3. Exactly35 skills

Confirmed35 unique original IDs and the same five categories. Existing radio names/values and session-state structure remain. No question was added or removed.

## 4. Exactly35 Thai behavioral questions

Confirmed all35 nonblank, unique, and byte-for-byte equal to the locked Thai question strings. Supplied Thai display names are used exactly. Main questions remain visible outside the information panel even while it is collapsed. The panel provides หมายถึงอะไร and ตัวอย่าง, not a duplicate main question.

## 5. Exactly35 English behavioral questions

Confirmed35 nonblank, unique, natural behavioral equivalents attached to the same IDs. Original English O*NET names are unchanged. All descriptions/examples remain populated. Technical examples use coursework, personal projects and relevant equipment experience rather than requiring industrial employment.

## 6. Canonical order unchanged

CSV/model/metadata/API/UI order remains unchanged. Tests protect exact IDs, English names and category/order. The earlier test preserving Thai display names now follows this later explicitly approved locked copy; it still protects all immutable feature mappings, and new tests require exact approved Thai names/questions. No tests were removed.

## 7. Paste Test Values unchanged

Still exactly35 integers1–5 mapped through the original definitions array; all original invalid-input/separator/paste tests run. State/progress, language switching, no auto-submit and normal Analyze submission remain. API receives exactly the same35 keyed scores; no career target or new field is sent.

## 8. Dataset unchanged

CSV SHA256 matches the pre-edit snapshot:7777b391793189c942f4020cc53564e9062b700b519f42850b7851c775101f88. Still910 occupations,35 Level features and35 Importance features. Source values and career mapping were not edited.

## 9. Model behavior unchanged

SHA256 matches for model.pkl, metadata, train_model.py, app/main.py, data/normalization, matcher, gap service and career_titles_th.txt. The35-dimensional vector, Nearest Neighbors/Euclidean, score formula, Top10 and gap/priority logic are unchanged. No retraining performed.

## 10. Python tests

Complete suite:136 passed,0 failed. One existing non-failing Starlette/httpx deprecation warning. Added19 cases for locked copy, TH/EN coverage, canonical mapping, all6 before/after profile comparisons and unchanged protected files. All prior tests continue to run.

## 11. JavaScript tests

Complete npm test suite:44 passed,0 failed. Updated assertions only for explicitly requested new display/scale wording. Added3 cases covering every always-visible question across both languages/all categories, common five-value scale and no-experience instruction, and unchanged paste/language/submission payload. Existing info accessibility, paste, bilingual, doctor, refresh and Top10 tests pass.

## 12. Doctor regression

Both existing35-value doctor vector and the newly supplied35-value vector naturally return Family Medicine Physicians,29-1215.00, rank1 through actual production FastAPI matching routes. The new vector differs only at Persuasion (canonical position21:4 instead of3). It was mapped to the existing order without reordering or truncation. Their Top10 can differ because their input values differ; comparisons use the same input before and after this task.

## 13. Before/after recommendations

Captured BEFORE changing content: all1, all3, all5, cycle1–5, existingdoctor and newpromptdoctor. AFTER: exact career identities/ranking; observed Euclidean distance change0 and score change0 in this environment; all gap records identical. Existing accepted absolute floating tolerance1e-12 remains for cross-platform tests. Complete actual outputs are in behavioral_baseline.json and behavioral_verification.json.

## 14. Mobile verification

Requested375/768/1440px rendered checks are pending because saved Browser permission blocks local access. No alternate browser/raw-CDP workaround or fabricated screenshot used. Added normal-flow16px question text with line-height1.85 and word wrapping; unchanged tappable rating controls and44px info buttons. No absolute-positioned explanation overlay. JSDOM checks that questions are visible block elements and precede info/rating controls; this does not prove rendered width/overflow behavior.

## 15. Accessibility verification

Native type=button info controls preserve aria-expanded, aria-controls, translated skill-specific aria-label and keyboard focus style. Mouse/touch and native Enter/Space activation are supported by the HTML control; no hover dependency. Each radio adds aria-describedby pointing to its unique always-visible question and an aria-label with the full scale meaning. The guide explains1 as not yet able/almost no experience; visible instructions say choosing1 is valid without guessing. One consistent scale is used for all35, with shortened button labels and full guide/accessible labels. Language switching preserves answers, progress, current step and expanded help.

## 16. Remaining issues

Actual mobile layout and real-browser/native keyboard acceptance remain pending under the saved Browser restriction. The user reports an existing successful public deployment; this task modifies the current workspace and downloadable project only, and has not redeployed or checked the updated assets at a public URL. No critical automated regression failed. Self-assessment remains ordinal and uncalibrated: wording improvements do not establish objective aptitude or career-success accuracy.

Run from a fresh project root:

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
npm ci
npm test
```

Audit host used a fresh basetemp and -p no:cacheprovider because of old directory-access issues; no tests were skipped.
