# รายงานปรับ Positioning และ UX — 6 ตุลาคม 2026

สถานะ: **PASS สำหรับ automated regression / PENDING สำหรับ visual responsive acceptance**

## 1. ไฟล์ที่แก้ทั้งหมด

แก้ source ใน working tree เดิมที่ `outputs/career-path-ai-final/career-path-ai` โดยตรง: README.md, app/static/app.js, app/static/i18n.js, app/static/index.html, app/static/style.css, tests/i18n.test.cjs, tests/ui.test.cjs

เพิ่ม tests/test_exploration_regression.py และหลักฐาน reports/exploration_baseline.json, exploration_verification.json, exploration_python_before.txt, exploration_javascript_before.txt, exploration_python_after.txt, exploration_javascript_after.txt, exploration_changes.diff และ exploration_ux_report.md นี้

โฟลเดอร์ที่ผู้ใช้ระบุเป็น outer folder; .git เดิมอยู่ภายใน career-path-ai อีกชั้น ตรวจ Get-Location ที่ outer ก่อนเริ่ม และใช้ inner working directory สำหรับแก้ source และรัน Git ทั้งหมด ไม่ได้สร้างหรือ copy โปรเจกต์ใหม่

## 2. Positioning ที่เปลี่ยน

Career Exploration Tool สำหรับนักศึกษามหาวิทยาลัยที่สำรวจอาชีพ ลังเลกับสาขาปัจจุบัน สนใจเปลี่ยนสาย หรือพิจารณาเริ่มศึกษาสาขาใหม่ ผลใช้ประกอบการสำรวจและตัดสินใจ ไม่รับรองคุณสมบัติประกอบอาชีพและไม่ตัดสินอนาคต

About อธิบายการประเมิน35ทักษะ → Skill Profile → เปรียบเทียบ910โปรไฟล์ O*NET → สำรวจ10อาชีพ → ดูทักษะสำคัญและแนวทางพัฒนา มีข้อจำกัดครบตามคำขอทั้งไทยและอังกฤษ

## 3. Home

Headline: “สำรวจอาชีพใหม่ ๆ จากทักษะของคุณ” / “Explore New Career Paths Through Your Skills”

Subtitle ไทย: “ค้นพบอาชีพที่มีโปรไฟล์ทักษะใกล้เคียงกับคุณ เพื่อเป็นข้อมูลประกอบการสำรวจเส้นทางใหม่ สำหรับนักศึกษาที่กำลังทบทวนเส้นทางการเรียน สนใจเปลี่ยนสาย หรืออยากค้นหาโอกาสทางอาชีพเพิ่มเติม”

อังกฤษสื่อความหมายเดียวกัน CTA: “เริ่มสำรวจอาชีพ” / “Start Exploring Careers”

## 4. Results

“10 อาชีพที่มีโปรไฟล์ทักษะใกล้เคียงกับคุณ” / “10 Occupations with Similar Skill Profiles” คะแนนอธิบายความใกล้เคียงของ self-assessed profile กับ O*NET มี disclaimer ว่าบางอาชีพต้องมีการศึกษา การฝึกอบรม หรือใบอนุญาต ไม่ใช่การรับรองความพร้อม

## 5. Career Detail

ทักษะสำคัญ5รายการเดิมยังเรียงเดิม ตาราง35ทักษะเดิมยังอยู่ในส่วนเปิดดูได้ ชื่อ Level ไทยเปลี่ยนเป็น “ระดับทักษะของอาชีพ” มีคำอธิบาย metric/bands แบบ native details/summary ใช้ keyboard ได้และไม่ต้อง hover

## 6. Importance

ให้คำอธิบายเด่นกว่าตัวเลข เช่น “มาก” แล้วแสดง3.88 / 5 ด้านล่าง ค่าดิบและแถบเดิมยังใช้ค่าเดิม อธิบายว่าเป็นความสำคัญของทักษะต่อการทำงานในอาชีพ

## 7. O*NET Level

ให้คำอธิบาย เช่น “ปานกลาง” แล้วแสดง O*NET Level3.88 / 7 อธิบายว่าพบในโปรไฟล์อาชีพ ไม่ใช่คะแนนสอบผ่าน minimum qualification หรือข้อกำหนดทางกฎหมาย

## 8. Skill Gap

ระดับคุณแสดงคะแนน1–5พร้อม anchor เดิม ระดับอาชีพแสดง label และ O*NET Level แยกชัดเจน ช่องความแตกต่างแสดง “ควรพิจารณาพัฒนา” และ “ต่างประมาณ N จุดเปอร์เซ็นต์” จาก Gap×100 ปัดเพื่ออ่านค่า โดยไม่เปลี่ยน Gap ดิบ

แถบเปรียบเทียบแสดงโปรไฟล์คุณ/อาชีพเป็นเปอร์เซ็นต์พร้อมคำอธิบายสเกล0–1เพื่อเปรียบเทียบเท่านั้น ไม่ใช่เปอร์เซ็นต์ความสามารถจริง ตัวอย่าง2/5และ2.50/7ให้25%,36%,ต่างประมาณ11จุดเปอร์เซ็นต์; รายละเอียดแสดง0.250,0.357,0.107

## 9. Labels และ thresholds

helper ส่วนกลาง metricBand/metricLabel/metricValue อยู่ app/static/app.js ใช้ค่า unrounded จัดช่วงแล้วแปลผ่าน architecture เดิม i18n.js

| Metric | Threshold | TH | EN |
| --- | --- | --- | --- |
| Importance | 1 ≤ x < 2 | น้อย | Low |
| Importance | 2 ≤ x < 3 | ปานกลาง | Moderate |
| Importance | 3 ≤ x < 4 | มาก | High |
| Importance | 4 ≤ x ≤ 5 | มากที่สุด | Very High |
| Level | 0 ≤ x < 2.5 | ต่ำ | Low |
| Level | 2.5 ≤ x < 5 | ปานกลาง | Moderate |
| Level | 5 ≤ x ≤ 7 | สูง | High |

นี่เป็น UX interpretation ของระบบ ไม่ใช่ official O*NET categories มีข้อความและ thresholds ใน info disclosure รวมทั้ง README ใช้ข้อความ ไม่ใช้สีอย่างเดียว

## 10. Calculation Details

แต่ละ development card มี “ดูรายละเอียดการคำนวณ” / “View calculation details” ปิดโดย default แสดง self-rating, UserNorm, O*NET Level, CareerNorm, Skill Gap, Importance, ImportanceNorm, Priority Gap และสูตรเดิมครบ normalized/Gap/Priority แสดง3ทศนิยมตาม UX แต่ API เก็บค่าจริงเดิม

UserNorm=(UserRating−1)/4; CareerNorm=Level/7; Gap=max(0,CareerNorm−UserNorm); ImportanceNorm=(Importance−1)/4; PriorityGap=Gap×ImportanceNorm

## 11. สิ่งที่ไม่ได้เปลี่ยน

SHA256 ตรง baseline ทั้ง10ไฟล์: CSV, model.pkl, model_metadata.json, train_model.py, app/main.py, data.py, career_matcher.py, skill_gap.py, skills.json และ render.yaml

910อาชีพ,35ทักษะและลำดับ, locked questions, คำตอบ1–5, normalization, Nearest Neighbors Euclidean, ranking, Match Score, Gap, Priority Gap, API, paste mapping และ Render configuration ไม่เปลี่ยน ไม่มี retrain ไม่มี feature/LLM/filter/login/database เพิ่ม ไม่อ่านหรือแก้ secrets/environment variables

ทั้ง6 fixed vectors มี Top10และ gap response ตรงก่อนแก้ทุก field แบบ exact โดย verification drift ของ distance/score เป็น0 ทั้งสอง doctor vectors ยังได้29-1215.00อันดับ1 Python regression ยังตรวจ float tolerance1e−12แบบabsoluteและตรวจอันดับ/โครงสร้างexact

## 12. Python tests

ก่อนแก้136ผ่าน; หลังแก้152ผ่าน0fail รันครบทุก test รวม16 regressionใหม่ ไม่ข้าม tests มี Starlette/httpx deprecation warning เดิม1รายการ ไม่ใช่ application failure

ใช้ isolated test runtime เดิมใน work/final-audit-venv เพราะ .venv ของ repository ไม่มี pytest ไม่แก้ runtime production การลองครั้งแรกพบ test temp parent path ผิดทำให้ fixture setup error แก้คำสั่งใช้ absolute path แล้วรันครบผ่านก่อนเริ่ม implementation หลักฐาน baseline logบันทึก136ผ่าน

## 13. JavaScript tests

ก่อนแก้44ผ่าน; หลังแก้50ผ่าน0fail ใช้ npm ci จาก lockfileเดิมไม่เปลี่ยน dependencies มี boundary labels, bilingual calculation rendering, example11percentagepoints และ positioning/limitations tests ใหม่6รายการ Testsเดิมยังยืนยัน answers35, test-value helper, language state, progress, result/detail/doctor และการ submit

## 14. Dataset validation / model / routes

Dataset910×72,35Level/Importance pairs, missing0, duplicatecodes0, duplicatetitles0, Level0–6, Importance1–5 model loadสำเร็จ; FastAPI lifespanตรวจ dataset hashตรง model

/health200: statusok,occupations910,skills35,metriceuclidean,versionbilingual-v3 หน้า/,/assessment,/results,/about,/career/29-1215.00ตอบ200ผ่าน TestClient DOM testsตรวจ Home,Assessment,Results,CareerDetail,Development,AboutและTH/ENด้วยจริงทั้ง2ภาษา

## 15. ปัญหา/bug

ไม่พบ bug คำนวณ Importance/Level/normalization/Gap/Priority/Score จึงไม่แก้ backend ข้อความเดิมไทย “ระดับทักษะที่ต้องใช้” เปลี่ยนเพื่อไม่ให้ตีความเป็นคุณสมบัติขั้นต่ำ

Browser ปฏิเสธhttp://127.0.0.1:8010เพราะ saved user permission blocks action ไม่พยายามหลบด้วย alternate browser/CDP จึงไม่สามารถตรวจภาพจริงหรือ keyboardผ่านbrowserได้

## 16. สิ่งที่ยังไม่แน่ใจ / Git

Visual desktop1440/tablet768/mobile375และpixel overflowยังpending DOMและCSSตรวจได้แต่ไม่เท่ากับrendered acceptance CSSใช้minmax(0,1fr),min-width0,wrapและmobile metrics1column พร้อมsummary44pxและfocusoutline ส่วนตาราง35ทักษะยังscrollในcontainerเดิม

ก่อนแก้ working treeสะอาด branchmain remoteoriginhttps://github.com/Jessadaruk/career-path-ai.git ไม่เปลี่ยน.git,remote,Render,secretsหรือenvironment variables ไม่มีcommit/push/deploy รายการdiffรวมอยู่exploration_changes.diffและเปิดreviewในแอปให้ตรวจได้ ผู้ใช้ตรวจแล้วค่อยสั่งขั้นตอนถัดไป
