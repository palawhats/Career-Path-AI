> Historical skill-help implementation/copy review. Current locked behavioral wording, names and test counts are in [behavioral_report.md](behavioral_report.md) and [behavioral_questions_review.md](behavioral_questions_review.md).

# Skill explanations UX report

1. **Files changed:** app/static/skills.json, app/static/app.js, app/static/i18n.js, app/static/style.css, app/static/index.html (asset version), tests/ui.test.cjs, tests/ui_fixture.json, tests/test_redesign_regression.py, README.md. New: tests/test_skill_help.py, reports/skill_help_baseline.json, skill_explanations_review.md, skill_help_verification.json and this report. Test result logs updated. Earlier final audit is marked historical.

2. **Content location:** app/static/skills.json is the centralized ordered definition list, keyed by the existing stable id. Each record contains description_th, example_th, description_en, example_en. No second skill ordering or duplicated HTML content list was added.

3. **Thai coverage:** all35 have nonblank natural Thai explanations and practical examples. All existing Thai display names are unchanged. Copy reviewed for first-year students, using assignments, group projects, clubs, study, computers and lab equipment. Technical abilities remain technical; examples clarify rather than redefine them.

4. **English coverage:** all35 have nonblank English explanations/examples. Original English O*NET skill names are unchanged. All140 content fields are populated and tested. Complete copy is in skill_explanations_review.md.

5. **Accessibility:** every skill has a native type=button information control, translated skill-specific aria-label, aria-expanded and aria-controls linked to a unique hidden panel. Native buttons provide Enter/Space activation without custom key interception. The selected panel expands in normal document flow before the rating controls, preserving focus on its trigger. Opening another skill closes the previous one. Global focus-visible styling applies; information buttons are at least44px tall. Expanded/hidden state has semantic attributes, not color alone. Rating help uses native details/summary. DOM tests verify controls, states, focus retention and panel order; actual browser keyboard behavior is not claimed tested.

6. **Mobile verification:** CSS uses wrapping text, fluid block panels, a44px touch control and smaller-screen padding; no absolute positioning/overlay was introduced. Requested375/768/1440px rendered checks remain pending because saved Browser permission blocks local navigation. JSDOM does not verify layout or overflow. No screenshot or alternate-browser workaround is claimed.

7. **Python tests:** complete suite117 passed,0 failed. Existing non-failing Starlette/httpx deprecation warning.14 added cases verify all four content fields and exact current name/id/order/group and protected-file checksums. Historical regression test now treats English/Thai description/example fields as editable presentation while preserving canonical identity/order/group; a new pre-UX snapshot additionally protects the current Thai/English names.

8. **JavaScript tests:** complete npm test suite41 passed,0 failed. Six new cases cover all35 content records, all35 open/close controls and aria linkage, bilingual help/answer/progress state, exclusive open panel and category return, rating anchors, paste preservation and normal submission. Existing paste/doctor/refresh/bilingual tests all run.

9. **Doctor regression:** actual FastAPI production pipeline still returns Family Medicine Physicians, O*NET-SOC29-1215.00, rank1 for the supplied35-value vector. All five existing fixed vectors retain exact Top10 identities/order; measured distance/score changes are0 in this environment (accepted numerical tolerance1e-12). Evidence: skill_help_verification.json and existing regression suite.

10. **Canonical order:** unchanged. Current id, Thai name, English O*NET name and group compare exactly with the pre-UX snapshot. Paste still maps the same definitions array, keeps normal ratings/session state and never auto-submits or manipulates ranking.

11. **ML/data unchanged:** SHA256 checks pass for CSV, model.pkl, model metadata, train_model.py, app/main.py, normalization/data service, matching service, skill-gap service and Thai career mapping. No dependencies added. UI helper state is separate in-memory state; it does not enter the API payload. Explanation and rating-help state survive language switching; answer/session behavior is unchanged.

Run from project root:

```sh
python -m pip install -r requirements-dev.txt
python -m pytest -q
npm ci
npm test
```

On this audit host a fresh basetemp and disabled pytest cache provider avoid old directory-access issues; no tests are skipped. Public deployment and actual browser/mobile acceptance remain pending as documented in deployment_smoke_checklist.md.
