# Public deployment smoke checklist

Status: **NOT EXECUTED**. No public Render URL has been created or tested. Complete this checklist on the deployed HTTPS origin. Record URL, commit/ZIP version, date, browser and evidence for each check.

| # | Check | Expected outcome | Status |
|---:|---|---|---|
| 1 | Public URL opens | HTTPS, no server/console failure | Pending |
| 2 | Homepage loads | Hero, 3 steps, assessment CTA, static CSS/JS | Pending |
| 3 | Thai default | Fresh language storage gives Thai; document lang=th | Pending |
| 4 | English switch | ไทย / EN translate navigation and content | Pending |
| 5 | Assessment all35 | Five categories together contain exactly 35 original IDs | Pending |
| 6 | Manual answers | Required choices 1–5 visible/selected; progress updates | Pending |
| 7 | Paste Test Values | Valid35 fills answers; invalid34/36/0/6/text rejects atomically; labelled test helper | Pending |
| 8 | Analyze Results | Explicit manual click submits normal matching request | Pending |
| 9 | Exactly Top10 | 10 distinct codes ordered by distance/score; doctor29-1215.00 first | Pending |
| 10 | Career detail opens | Thai/English name, original code, matching score | Pending |
| 11 | Importance | ความสำคัญต่ออาชีพ; 1–5; describes importance, not ability | Pending |
| 12 | Level | ระดับทักษะที่ต้องใช้; 0–7; distinct from Importance | Pending |
| 13 | Skills to Develop | Cautious text; normalized comparison, gap and priority correct | Pending |
| 14 | Back/navigation | Return to Top10/assessment without losing ratings; language preserves route/results | Pending |
| 15 | Refresh/deep link | Session answers restored; /career/code and /results serve shell; no critical error | Pending |
| 16 | Mobile/keyboard | Check375/768/1440px, Thai wrap, >=44px choices, safe table scroll, focus/skip link, native dialog Escape/focus | Pending |
| 17 | Health | GET /health: ok, occupations910, skills35, metric euclidean | Pending |

Doctor paste vector (canonical skills.json order):

```text
3,4,3,3,4,1,1,1,3,4,3,2,2,3,3,3,3,1,3,2,3,1,2,4,1,3,3,3,4,3,3,1,3,1,3
```

Also verify malformed JSON, missing/extra identifiers, booleans/strings and NaN/Infinity return 422 rather than 500 on both matching and skill-gap endpoints. Inspect a direct career URL in a fresh session: all source skills accessible; personalized score/gaps should require assessment.

Public request example:

```sh
curl -f "$PUBLIC_URL/health"
```

Set PUBLIC_URL to the actual deployed HTTPS origin. Do not substitute localhost evidence for public deployment evidence. Browser saved permission currently blocks local automated visual verification; no workaround browser was used.
