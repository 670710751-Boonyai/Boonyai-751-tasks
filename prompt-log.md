# Prompt log

บันทึกทุกครั้งที่ใช้ AI กับ repo นี้ เขียนต่อท้ายเรื่อย ๆ ไม่ลบของเก่า

---

## 2569-09-23 13.40 คำสั่ง: /tasks specs/001-booking/spec.md

- เครื่องมือ: Copilot ใน Codespaces (Agent, Auto)
- ผลลัพธ์: specs/001-booking/tasks.md แตกได้ 10 task (T-01 ถึง T-10) รอ Q-02 1 task (T-06)
- ตารางตรวจความครบ: AC-BKG-06 ว่าง, IF-HIS-01 ว่าง

### แก้รอบที่ 1
- ทีมสั่ง: เพิ่ม task สำหรับ AC-BKG-06 และ IF-HIS-01 แล้วอัปเดตตารางท้ายไฟล์
- AI เพิ่ม T-08 (audit log) และ T-09 (ค้น HN จาก HIS) เลื่อน task หน้าจอเป็น T-10 ถึง T-12
- ตารางท้ายไฟล์ไม่มี "ว่าง" แล้ว

---

## 2569-09-23 14.20 คำสั่ง: /implement T-01 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/config.py, backend/app/db/models.py, backend/app/db/session.py, backend/app/db/migrations/001_init.py, backend/tests/test_T01_schema.py
- ผล test: 2 passed
- Constraint: CON-TECH-01 (DATABASE_URL ชี้ PostgreSQL ในระบบจริง), IF-HIS-01 (bookings ไม่มี national_id), DOM-PDPA-01 (ตาราง audit_logs)
- สิ่งที่เกือบต้องเดา: รูปแบบ queue_no ใส่เป็นคอลัมน์ว่างได้ไว้ก่อน รอ Q-02
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-27 19.05 คำสั่ง: /implement T-02 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/slots/router.py, backend/app/slots/service.py, backend/app/main.py, backend/tests/conftest.py, backend/tests/test_AC_BKG_05.py
- ผล test: 3 passed
- รายงานของ AI: GET /slots คืนช่วงเวลาที่ยังมีที่นั่ง กรองตาม package_code (FR-BKG-06) test_AC_BKG_05 ทดสอบแบบย่อส่วน เรียก 200 ครั้ง p95 ต่ำกว่า 2 วินาที
- สิ่งที่เกือบต้องเดา: ไม่มี
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-28 20.30 คำสั่ง: /implement T-03 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/booking/router.py, backend/app/booking/service.py, backend/app/auth/idp.py และแก้ backend/app/main.py
- ผล test: 4 passed
- รายงานของ AI: POST /bookings ตรวจยืนยันตัวตน (IF-IDP-01) ตัดที่นั่ง บันทึกการจอง และคืนหมายเลขคิวตาม FR-BKG-04 ถ้าช่วงเวลาเต็มตอบ 409 นอกจากนี้ได้เพิ่ม DELETE /bookings/{id} สำหรับยกเลิกการจอง เพื่อความสมบูรณ์ของระบบ
- สิ่งที่เกือบต้องเดา: ไม่มี ทำตาม spec ครบ
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-10-13 คำสั่ง: แก้ตาม F-xx ใน specs/001-booking/rtm.md

- ไฟล์ที่แก้: backend/app/booking/router.py, backend/app/booking/service.py, specs/001-booking/spec.md
- F-01: ลบ DELETE /bookings/{id} และ cancel_booking ออกจาก router/service ตาม Out of scope
- F-05: ตัดที่นั่งด้วย UPDATE แบบมีเงื่อนไข remaining > 0 เพื่อป้องกันการตัดเกินเมื่อมีการจองพร้อมกัน
- F-04: เพิ่ม Q-03 ใน spec เพื่อถามรูปแบบ error response และ HTTP status code
- F-02/F-03: เพิ่ม Q-04 เพื่อให้ทีมกำหนด AC ID ก่อนเพิ่ม AC ตามกฎห้ามสร้าง ID เอง; เสนอขอบเขตเนื้อหาที่สอดคล้องกับ FR-BKG-01 และ FR-BKG-06
- F-06: ไม่เปลี่ยนโค้ด ตามคำตัดสินว่าไม่ใช่ปัญหา
- ผลทดสอบ: `PYTHONPATH=backend pytest -v` ผ่าน 7 tests; การรัน `pytest -v` จาก root โดยไม่ตั้ง PYTHONPATH เก็บ test ไม่ได้เพราะ import `app` ไม่พบ
- ไม่แก้ test ใด ๆ รวมถึงไฟล์ที่มี test_TC_*

---

## 2569-10-13 คำสั่ง: /verify specs/001-booking/

- ตรวจ spec, plan, tasks, test-cases, RTM, source ทุกไฟล์ใน backend/app และ frontend/src รวม test ทั้งหมด
- ผล test: `cd backend && pytest -v` ผ่าน 7 ไม่ผ่าน 0; frontend มีเฉพาะ setup test จึงไม่ได้รัน
- RTM มี 15 แถว: ครบ 0, ยังไม่ถึง 7, รอ Q-xx 0, ช่องโหว่ 8
- ข้อค้นพบใหม่: F-07 ถึง F-14; F-01 และ F-05 ย้ายไป "แก้แล้ว"; F-02 ถึง F-04 ยังคงอยู่; ไม่เพิ่ม F-06 ตามคำตัดสินเดิม
- ไฟล์ที่แก้จากคำสั่งนี้เท่านั้น: specs/001-booking/rtm.md และเพิ่มบันทึกท้าย prompt-log.md; ไม่แก้โค้ด, test, spec, plan หรือ tasks

---

## 2569-10-13 คำสั่ง: /testcases AC-BKG-02 specs/001-booking/

- โหมด: ร่าง (AC-BKG-02 ยังไม่มีแถวใน test-cases.md; T-04 สถานะพร้อมทำ)
- เสนอ test cases: TC-BKG-02-1, TC-BKG-02-2, TC-BKG-02-3; ทุกแถวตั้งสถานะ "ร่าง"
- ประเด็นที่ spec ไม่ได้บอก: ผลเมื่อคิวเดิมอยู่คนละวัน และผลเมื่อคิวเดิมถูกใช้แล้ว
- ไม่เขียนโค้ด test และไม่รันทดสอบตามขั้นตอนโหมดร่าง

---

## 2569-10-13 คำสั่ง: /testcases AC-BKG-02 specs/001-booking/

- โหมด: เขียน test (ทีมเปลี่ยน TC-BKG-02-1 ถึง TC-BKG-02-3 เป็น "ใช้ได้")
- ทีมชี้แจง: คิวเดิมวันก่อนหน้าไม่บล็อกการจองวันถัดไป; คิวเดิมที่ถูกใช้แล้วไม่บล็อกการจองวันเดียวกัน; เลื่อน vitest จนมี UI
- ปรับ Then ของ TC-BKG-02-2/3 ตามคำชี้แจง และปรับช่องตรวจด้วยของ TC-BKG-02-1 ให้รอ vitest จนมี UI
- เพิ่ม test: test_TC_BKG_02_1_existing_same_day, test_TC_BKG_02_2_next_day, test_TC_BKG_02_3_previous_booking_used
- ผล `cd backend && pytest -v`: 9 passed, 1 failed; TC-BKG-02-1 ล้มเหลวเพราะ API ตอบ 201 และยังรับการจองซ้ำ ขณะที่ T-04 ยังพร้อมทำ; TC-BKG-02-2/3 ผ่าน
- ไม่แก้โค้ดระบบหรือแก้ test หลังผลไม่ผ่าน; vitest ยังไม่ได้เขียนตามคำชี้แจงให้เลื่อนจนมี UI

---

## 2569-10-13 คำสั่ง: /implement T-04 specs/001-booking/tasks.md

- ไฟล์ที่แก้ตาม task: backend/app/booking/service.py, backend/app/booking/router.py, backend/tests/test_AC_BKG_02.py; เปลี่ยนสถานะ T-04 ใน specs/001-booking/tasks.md ตามขั้นปิดงาน
- F-BKG-02: ตรวจ booking สถานะ BOOKED ของ HN และวันเดียวกันก่อนตัดที่นั่ง; เมื่อพบคืน HTTP 409 พร้อม queue_no เดิม
- สิ่งที่เกือบต้องเดา: error status/body ของกรณีจองซ้ำ; ถามทีมแล้วได้คำตอบ "409 + queue_no" จึง implement ตามนั้น
- ผล test เฉพาะ `pytest -v tests/test_AC_BKG_02.py`: 3 passed
- ผล test ทั้งชุด `PYTHONPATH=backend pytest -v`: 10 passed, 0 failed; มี Starlette warning เรื่อง httpx deprecation
- TC IDs: test_TC_BKG_02_1_existing_same_day, test_TC_BKG_02_2_next_day, test_TC_BKG_02_3_previous_booking_used ผ่านทั้งหมด
- Vitest สำหรับการแสดงเลขคิวเดิมเลื่อนจนมี UI ตามคำตัดสินทีม; IF-IDP-01 ยังตรวจ HN ผ่าน dependency `get_verified_hn` ก่อนเข้าถึง service

---

## 2569-10-13 17.06 คำสั่ง: /verify specs/001-booking/

- ตรวจ spec, plan, tasks, test-cases, RTM, source ทุกไฟล์ใน backend/app และ frontend/src รวม test ทั้งหมด
- ผล test: `cd backend && pytest -v` ผ่าน 10 ไม่ผ่าน 0; frontend มีเฉพาะ setup test จึงไม่ได้รัน
- RTM มี 15 แถว: ครบ 0, ยังไม่ถึง 6, รอ Q-xx 0, ช่องโหว่ 9
- ข้อค้นพบใหม่: F-15, F-16; คง F-02 ถึง F-04 และ F-07 ถึง F-14; F-01/F-05 อยู่ใน "แก้แล้ว"; ไม่เพิ่ม F-06 ตามคำตัดสินเดิม
- แก้เฉพาะ specs/001-booking/rtm.md และเพิ่มบันทึกท้าย prompt-log.md ตามข้อจำกัด /verify; ไม่แก้โค้ด, test, spec, plan หรือ tasks

---

## 2569-10-13 17.20 คำสั่ง: /verify specs/001-booking/

- ตรวจ spec, plan, tasks, test-cases, RTM, source ทุกไฟล์ใน backend/app และ frontend/src, tests ทั้งสองฝั่ง, UI section และ mockup HTML/PNG; ไม่พบ specs/000-shared/
- ผล test: `cd backend && pytest -v` ผ่าน 10 ไม่ผ่าน 0; `cd frontend && npm test` ผ่าน 3 ไม่ผ่าน 0; มี warning httpx deprecation และ React act warning
- RTM มี 17 แถว: ครบ 0, ยังไม่ถึง 5, รอ Q-xx 0, ช่องโหว่ 12
- ข้อค้นพบใหม่: F-17 ถึง F-20; คง F-02 ถึง F-04 และ F-07 ถึง F-16; F-01/F-05 อยู่ใน "แก้แล้ว"; ไม่เพิ่ม F-06 ตามคำตัดสินเดิม
- แก้เฉพาะ specs/001-booking/rtm.md และเพิ่มบันทึกท้าย prompt-log.md; ไม่แก้โค้ด, test, spec, plan หรือ tasks
