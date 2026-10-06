# รายงานแสดงระดับอาชีพบนสเกล1–5

สถานะ: PASS automated tests / visual browser acceptance ยังpendingจากsavedpermissionเดิม

## 1. ไฟล์ที่แก้

แก้ต่อใน working tree เดิม: app/static/app.js, app/static/i18n.js, app/static/index.html (cacheversiondisplay5-v9), README.md, tests/ui.test.cjs

เพิ่มหลักฐาน reports/display5_python_before.txt, display5_javascript_before.txt, display5_python_after.txt, display5_javascript_after.txt, display5_verification.json, display5_changes.diff และรายงานนี้ รักษา uncommitted changesจากUXรอบก่อนทั้งหมด ไม่แตะ backend/model/data/CSSของรอบก่อน

## 2. Helper

careerDisplay5(rawLevel) = 1 + 4 × (rawLevel / 7) ใน app/static/app.js คืนค่าเต็มไม่ปัดเศษ ปัด2ทศนิยมเฉพาะตอนrender ไม่ใช้Level×5/7 ไม่มีการส่ง display value ไป API หรือใช้คำนวณ matching/gap/bar

metricValue('level',rawLevel) แสดงค่า/5เป็นหลัก และคำต่ำ/ปานกลาง/สูงเป็นข้อความรอง โดย metricLabelยังใช้rawLevelก่อนปัดเศษตาม thresholdsเดิม

## 3. จุดในUIที่เปลี่ยน

Skills to Developแสดงระดับคุณ1–5กับระดับอาชีพ1–5ที่แปลงแล้ว ทั้งTH/EN

Top Important Skillsใช้helperเดียวกันเพื่อให้ระดับอาชีพอ่านสม่ำเสมอ เพิ่มsourceLevelDetailsแบบnative details/summaryที่เข้าถึงด้วยkeyboardเพื่อดูO*NETต้นฉบับและสูตรแสดงผล

Calculation Detailsเพิ่ม“ระดับที่แสดงบนหน้าเว็บ / Level displayed on this page”และแยก“ O*NET Level ต้นฉบับ / Original O*NET Level” คง normalized,Gap,Importance,Priorityและสูตรเดิมไว้ครบ

ตาราง35ทักษะที่อยู่ในinformation disclosureยังแสดงraw0–7 เปลี่ยนหัวคอลัมน์ให้ระบุว่าเป็นO*NET Levelต้นฉบับ คำอธิบายTH/ENอธิบายสเกลแสดงผลใหม่และค่าดิบให้สอดคล้องกัน

## 4. Example A

User2/5,rawLevel2.50/7 → careerDisplay5=2.428571… → UI2.43/5

UserNorm0.250;CareerNorm0.357142…;Gap0.107142… แสดงต่างประมาณ11จุดเปอร์เซ็นต์ แถบ25%และ36%ไม่เปลี่ยน

## 5. Example B

User3/5,rawLevel3.75/7 → careerDisplay5=3.142857… → UI3.14/5

UserNorm0.500;CareerNorm0.535714…;Gap0.035714… แสดงต่างประมาณ4จุดเปอร์เซ็นต์ แถบ50%และ54%ไม่เปลี่ยน

Endpoints: raw0→1.00/5;raw7→5.00/5

## 6. Raw O*NET Level

ยังอยู่ในdatasetและAPIเดิม และดูได้จากCalculation Details,แต่ละimportant skill disclosureและตาราง35ทักษะ ไม่มีค่าดิบถูกเขียนทับ Testsตรวจrawแยกจากprimarydisplayทั้งTH/EN

## 7. ค่าคำนวณและranking

CareerNorm,Gap,PriorityGap,MatchScore,distancesและrankingตรงbaselineทุกfieldแบบexactทั้ง6fixedvectors รวมdoctorทั้ง2ชุด การตรวจhash10protectedfilesผ่านทั้งหมด รวมCSV,model.pkl,modelmetadata,train_model.py,backendservices,app/main.py,skills.jsonและrender.yaml /healthok910อาชีพ35ทักษะ

Comparison barยังใช้UserNormและCareerNorm ค่าความกว้างไม่เปลี่ยน labelsยังแบ่งrawLevel[0,2.5),[2.5,5),[5,7] การปัด2ตำแหน่งไม่เปลี่ยนlabelและcalculations Testsตรวจใกล้boundary2.499/2.5และ4.999/5ด้วย

## 8. Python tests

ก่อน152ผ่าน;หลัง152ผ่าน0fail รันครบด้วยisolatedtestenvเดิม มีStarlette/httpx deprecationwarningเดิม1รายการ ไม่มีbackend/model/calculationเปลี่ยน

## 9. JavaScript tests

ก่อน50ผ่าน;หลัง54ผ่าน0fail เพิ่ม4testsสำหรับhelperendpoints/examples/unrounded,labelboundaries,TH/ENrawdisclosures,unchangedbarwidths,examplesA/Bและไม่mutateAPIrecords Testsเดิมassessment/paste35answers/result/languageswitchยังผ่านครบ

## 10. Git diffและข้อจำกัด

ก่อนเริ่มพบuncommittedchangesจากUXรอบก่อนและเก็บทั้งหมดไว้ branchmainและoriginhttps://github.com/Jessadaruk/career-path-ai.gitไม่เปลี่ยน .gitเดิมยังอยู่ ไม่มีcommit/push/deploy/reset ไม่มีconfiguration/env/secretsเปลี่ยน

reports/display5_changes.diffแสดงdiffเฉพาะรอบนี้เทียบworkingtreeก่อนแก้ git diffปกติรวมUXรอบก่อนด้วย git diff --checkผ่าน

ไม่มีความจำเป็นต้องแก้backend/model/calculationและไม่พบbugใหม่ Actualrendered375/768/1440ยังไม่ได้ยืนยันเพราะsavedBrowserpermissionblockเดิม DOMtestsไม่ใช่visualacceptance
