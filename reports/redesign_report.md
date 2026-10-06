> Historical implementation report. The current submission and test gates are documented in [final_audit_report.md](final_audit_report.md) and [README](../README.md). Earlier counts and design descriptions below are historical evidence, not current claims.

# Student Career Exploration redesign report

Thai-first display redesign of the current single-page bilingual application. No model retraining.

## Files changed

- app/static/index.html: shared shell, cache version and skip link.
- app/static/app.js: page presentation and accessible focus behavior; same rating/session handlers, canonical definitions and paste parser.
- app/static/style.css: clean light blue visual system, local Thai font stack, 16px body, generous spacing, responsive grids and touch targets.
- app/static/i18n.js: centralized Thai/English wording; plain-language primary screens, technical details in disclosure/About.
- app/static/skills.json: Thai display names and descriptions reviewed for all 35 skills. IDs, order, English labels, English descriptions and groups preserved.
- data/career_titles_th.txt: 80 familiar occupations prioritized, 29 titles revised. All 910 code keys preserved. English titles remain sourced from unchanged CSV/model.
- tests/ui.test.cjs and tests/ui_fixture.json: current UI expectations and real API fixture updated; 5 new UI cases.
- tests/test_redesign_regression.py: 12 new protected-file/order/fixed-vector regression cases.
- README.md and reports: documentation and before/after evidence.

## UI/UX changes

- Light home hero with 3 steps and a single primary assessment CTA; no decorative background image or methodology overload.
- Assessment progress at the top, 5 existing categories, Thai skill name with English below, descriptive 1–5 choices, explicit selected state. Existing manual flow and test paste behavior retained.
- Ten result cards: Thai/English career names and code, unchanged score, first 3 matching skill tags; distance removed from primary subtitle.
- Detail: large match card, first 5 API important skills, comparison bars and skill gaps, then expandable all-35 table. Raw scales are labelled; gap comparison bars explicitly share the normalized 0–1 scale.
- About: readable data/how/limitations cards, optional technical explanation and clear exploration disclaimer.
- Mobile rules use stacked cards, wrapped navigation, full labels, scrollable table and tappable rating targets. Font uses Leelawadee UI, Tahoma, system-ui; no external font downloads.
- Skip link, native radio/fieldset controls, visible keyboard focus, text labels and numeric values supplement color.

## Verification

- Python: 57 passed (one pre-existing Starlette/httpx deprecation warning). JavaScript: 33 passed. Total: 90 passed.
- 5 fixed vectors (all 1, all 3, all 5, alternating 1–5, supplied doctor vector) were captured BEFORE edits and compared AFTER through the actual API. Top10, ranks, original English titles, distances, exact scores, matching skill records and gap records match exactly.
- Doctor vector: Family Medicine Physicians remains rank 1.
- All 910 careers and 35 canonical skill definitions remain available. Dataset/model/backend files have identical SHA256 hashes. No change to normalization, retrieval, ranking or gap calculations.
- Paste parser text is byte-for-byte unchanged; original paste tests pass, including mapping, progress, no auto-submit, language persistence, clear and normal submission.
- Language switching preserves assessment step/ratings, current route and cached results; English title fallback and both catalogs tested.
- Browser visual checks at 375/768/1440px are pending: saved user permission rejected local browser navigation. No screenshots or actual responsive-render verification are claimed. JSDOM tests check DOM/state; native dialog lifecycle is mocked, not visually rendered.

## Thai changes

All 35 names/descriptions were rewritten in everyday Thai, with original English O*NET labels kept underneath. Examples: การเรียนรู้และนำความรู้ใหม่ไปใช้; การคิดวิเคราะห์อย่างมีเหตุผล; การบริหารงบประมาณและการเงิน; การบริหารวัสดุและทรัพยากร. Student-facing score is ความสอดคล้องของทักษะ and difference is ช่องว่างทักษะ. These labels do not imply career success probability.

Revised occupation names (remaining titles retained):

- 13-1071.00 Human Resources Specialists: ผู้เชี่ยวชาญด้านทรัพยากรบุคคล → เจ้าหน้าที่ทรัพยากรบุคคล
- 13-1081.00 Logisticians: นักโลจิสติกส์ → นักวางแผนโลจิสติกส์
- 13-1151.00 Training and Development Specialists: ผู้เชี่ยวชาญด้านการฝึกอบรมและพัฒนา → เจ้าหน้าที่ฝึกอบรมและพัฒนาบุคลากร
- 13-1161.00 Market Research Analysts and Marketing Specialists: นักวิเคราะห์วิจัยตลาดและผู้เชี่ยวชาญด้านการตลาด → นักวิจัยตลาดและผู้เชี่ยวชาญด้านการตลาด
- 13-2011.00 Accountants and Auditors: นักบัญชีและผู้สอบบัญชี → นักบัญชีและผู้ตรวจสอบบัญชี
- 15-1212.00 Information Security Analysts: นักวิเคราะห์ความมั่นคงปลอดภัยสารสนเทศ → นักวิเคราะห์ความมั่นคงปลอดภัยไซเบอร์
- 15-1231.00 Computer Network Support Specialists: ผู้เชี่ยวชาญสนับสนุนเครือข่ายคอมพิวเตอร์ → เจ้าหน้าที่ดูแลและแก้ปัญหาเครือข่ายคอมพิวเตอร์
- 15-1232.00 Computer User Support Specialists: ผู้เชี่ยวชาญช่วยเหลือผู้ใช้คอมพิวเตอร์ → เจ้าหน้าที่สนับสนุนการใช้งานคอมพิวเตอร์
- 15-1241.00 Computer Network Architects: สถาปนิกเครือข่ายคอมพิวเตอร์ → นักออกแบบเครือข่ายคอมพิวเตอร์
- 15-1243.00 Database Architects: สถาปนิกฐานข้อมูล → นักออกแบบระบบฐานข้อมูล
- 15-1251.00 Computer Programmers: นักเขียนโปรแกรมคอมพิวเตอร์ → โปรแกรมเมอร์
- 15-1253.00 Software Quality Assurance Analysts and Testers: นักวิเคราะห์การประกันคุณภาพและผู้ทดสอบซอฟต์แวร์ → นักวิเคราะห์และทดสอบคุณภาพซอฟต์แวร์
- 15-1255.00 Web and Digital Interface Designers: นักออกแบบเว็บไซต์และส่วนติดต่อผู้ใช้ดิจิทัล → นักออกแบบเว็บไซต์และส่วนติดต่อผู้ใช้
- 15-2031.00 Operations Research Analysts: นักวิเคราะห์วิจัยการดำเนินงาน → นักวิเคราะห์วิจัยดำเนินงาน
- 17-1011.00 Architects, Except Landscape and Naval: สถาปนิก ยกเว้นภูมิสถาปัตยกรรมและสถาปัตยกรรมเรือ → สถาปนิก
- 17-2072.00 Electronics Engineers, Except Computer: วิศวกรอิเล็กทรอนิกส์ ยกเว้นด้านคอมพิวเตอร์ → วิศวกรอิเล็กทรอนิกส์
- 25-2011.00 Preschool Teachers, Except Special Education: ครูปฐมวัย ยกเว้นการศึกษาพิเศษ → ครูปฐมวัย
- 25-2012.00 Kindergarten Teachers, Except Special Education: ครูอนุบาล ยกเว้นการศึกษาพิเศษ → ครูอนุบาล
- 25-2021.00 Elementary School Teachers, Except Special Education: ครูประถมศึกษา ยกเว้นการศึกษาพิเศษ → ครูระดับประถมศึกษา
- 25-2022.00 Middle School Teachers, Except Special and Career/Technical Education: ครูมัธยมศึกษาตอนต้น ยกเว้นการศึกษาพิเศษและอาชีวศึกษา → ครูระดับมัธยมศึกษาตอนต้น
- 25-2031.00 Secondary School Teachers, Except Special and Career/Technical Education: ครูมัธยมศึกษาตอนปลาย ยกเว้นการศึกษาพิเศษและอาชีวศึกษา → ครูระดับมัธยมศึกษา
- 25-4022.00 Librarians and Media Collections Specialists: บรรณารักษ์และผู้เชี่ยวชาญจัดการคลังสื่อ → บรรณารักษ์และผู้ดูแลสื่อการเรียนรู้
- 27-1014.00 Special Effects Artists and Animators: ศิลปินเทคนิคพิเศษและนักสร้างภาพเคลื่อนไหว → นักสร้างเทคนิคพิเศษและแอนิเมชัน
- 27-2012.00 Producers and Directors: ผู้อำนวยการสร้างและผู้กำกับ → โปรดิวเซอร์และผู้กำกับ
- 27-3031.00 Public Relations Specialists: ผู้เชี่ยวชาญด้านประชาสัมพันธ์ → เจ้าหน้าที่ประชาสัมพันธ์
- 27-3042.00 Technical Writers: นักเขียนเอกสารทางเทคนิค → นักเขียนเอกสารเทคนิค
- 27-3043.00 Writers and Authors: นักเขียนและนักประพันธ์ → นักเขียน
- 35-1011.00 Chefs and Head Cooks: เชฟและหัวหน้าพ่อครัว → เชฟและหัวหน้าครัว
- 39-7011.00 Tour Guides and Escorts: มัคคุเทศก์และผู้นำชม → มัคคุเทศก์และผู้นำเที่ยว
