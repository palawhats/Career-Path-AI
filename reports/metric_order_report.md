# รายงาน Metric presentation order

สถานะ: PASS automated tests; actual rendered responsive checks pending

1. ไฟล์รอบนี้: app/static/app.js, app/static/i18n.js, app/static/style.css, app/static/index.html (metric-order-v10), tests/ui.test.cjs เพิ่ม reports/metric_order_changes.diff, metric_order_python_tests.txt, metric_order_javascript_tests.txt และรายงานนี้ รักษางานที่ยังไม่commitทุกรอบก่อนหน้า

2. Components: metricValueสำหรับImportance, developmentItemช่องGap CSSmetric-labelเป็น20pxboldและmetric-rawเป็น14pxsecondary ส่วนUserLevelกับCareerLevelใช้numeric-firstเดิมอยู่แล้ว Metricที่เหลือเช่นscore/bar/technicaltableเป็นชื่อ→ตัวเลขอยู่แล้ว จึงไม่สลับข้อมูลทางเทคนิค

3. Skills to Developก่อน→หลัง: ชื่อ→ควรพิจารณาพัฒนา→ต่างประมาณ11จุดเปอร์เซ็นต์ เปลี่ยนเป็นชื่อ→ประมาณ11จุดเปอร์เซ็นต์→ควรพิจารณาพัฒนา Userชื่อ→2/5→ทำได้เล็กน้อยและCareerชื่อ→2.43/5→ปานกลางคงเดิม EnglishGap: About11percentagepoints→Considerdeveloping ผ่านi18n

4. Top Important Skillsก่อน→หลัง: Importanceชื่อ→มาก→3.88/5เปลี่ยนเป็นชื่อ→3.88/5→มาก Careerชื่อ→3.22/5→ปานกลางคงเดิม ทุกช่องใช้dtแล้วddที่มีstrongตัวเลขก่อนsmallคำอธิบาย

5. คำนวณทั้งหมดเดิม: careerDisplay5,metricBand,calculationDetailssourceตรงก่อนรอบนี้ทุกตัวอักษร;10protectedfileshashตรงbaselineรวมdataset/backend/model/API/skills/Render ทั้ง6fixedvectorsมีrankings,distance,scores,rawlevels,CareerNorm,Gap,Priorityตรงทุกfieldแบบexact เทียบactualAPI แถบใช้UserNorm/CareerNormเดิม ไม่มีretrain/backendchanges

6. Python152passed0failed;warningStarlette/httpxเดิม1รายการ รันทุกtestไม่ข้าม

7. JavaScript57passed0failed (เพิ่ม3tests) ตรวจDOMจริงด้วยJSDOMทั้งTH/EN: dtชื่อมาก่อนdd,ddมีSTRONGnumericก่อนSMALLinterpretation ตัวอย่างUser2/5,career2.43/5,gap11percentagepoints,Importance3.88/5,career3.22/5 และสลับภาษาnumeric/state/scoreไม่เปลี่ยน

8. Regressionเดิมทุกชุดผ่าน รวม35answers,pastehelper,languageswitch,rawdisclosures,displayendpoints,examplesA/B,barsและ6fixedAPIvectors

9. Git diffเฉพาะรอบนี้ในmetric_order_changes.diff ส่วนgit diffปกติรวมuncommittedงานก่อนด้วย branchmain,originเดิม ไม่มีcommit/push/deploy/reset/env/secretschanges

Responsive CSSเดิมยังเรียงdevelopmentmetrics1columnที่≤768px ไม่มีCSSorderเพื่อสลับDOM ตัวเลข20pxboldและคำอธิบาย14pxมีoverflow-wrap:anywhere ลำดับจึงคงเดิมเมื่อstack แต่visual375/768/1440และpixeloverflowยังpendingเพราะsavedBrowserpermissionblock ไม่อ้างJSDOMเป็นrenderedacceptance
