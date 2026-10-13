# RTM: จองคิวตรวจสุขภาพ (Booking)
อ้างอิง: spec.md Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2569-10-13 17:20 | test backend: 10 ผ่าน 0 ไม่ผ่าน; frontend: 3 ผ่าน 0 ไม่ผ่าน
สถานะตามรอย: ครบ 0, ยังไม่ถึง 5, รอ Q-xx 0, ช่องโหว่ 12 (รวม UI-BKG-01/02)

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | AC-BKG-05 ตรวจเฉพาะ p95 ไม่ได้ตรวจช่วง 30 วัน/จำนวนที่นั่ง | T-02 เสร็จ; T-10 เสร็จ รอทีมตรวจ | `backend/app/slots/service.py`: `list_available_slots` ใช้ `DAYS_AHEAD = 14`; `frontend/src/pages/SlotPicker.jsx`: แสดงเวลาและจำนวน | `test_AC_BKG_05` ผ่านแต่ตรวจเฉพาะ p95; `SlotPicker.test.jsx` ผ่านแต่ตรวจเฉพาะการเปลี่ยนแพ็กเกจ | ช่องโหว่ (F-03, F-07, F-17) |
| FR-BKG-02 | AC-BKG-02 | T-04 เสร็จ รอทีมตรวจ | `backend/app/booking/service.py`: `create_booking` ตรวจ BOOKED ตาม HN/วัน; `backend/app/booking/router.py`: 409 พร้อม queue_no; `frontend/src/pages/ConfirmBooking.jsx`: ทุก 409 ถูกแสดงเป็นกรณี slot เต็ม | test_TC_BKG_02_1/2/3 ผ่าน backend; ไม่มี vitest สำหรับการแสดงคิวเดิม | ช่องโหว่ (F-15, F-16) |
| FR-BKG-03 | AC-BKG-03 | T-05 พร้อมทำ; T-11 เสร็จ รอทีมตรวจ; T-12 พร้อมทำ | `frontend/src/pages/ConfirmBooking.jsx`: แสดงข้อความและสูงสุด 3 options; ยังไม่มี logic backend หา options | `AC-BKG-03.test.jsx` ผ่าน แต่ assert เฉพาะข้อความและจำนวนปุ่ม ไม่ตรวจวัน/เวลาใกล้ที่สุดหรือไม่มี booking ซ้อน | ช่องโหว่ (F-19) |
| FR-BKG-04 | AC-BKG-01 | T-03 เสร็จ; T-06 รอ Q-02; T-11 เสร็จ รอทีมตรวจ | `backend/app/booking/router.py`: `create_booking`; `backend/app/booking/service.py`: `create_booking`, `next_queue_no`; `frontend/src/pages/ConfirmBooking.jsx`: success view | `test_AC_BKG_01` และ TC-BKG-01 tests ผ่านแต่ assert เฉพาะ status; ไม่มี UI test success view | ช่องโหว่ (F-08, F-09, F-20) |
| FR-BKG-05 | AC-BKG-04 | T-07 พร้อมทำ | ยังไม่มี notification queue หรือการอ่านผลเพื่อแสดงคิวหลังแจ้งเตือนล้มเหลว | ไม่มี | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC | T-02 เสร็จ; T-10 เสร็จ รอทีมตรวจ | `backend/app/slots/service.py`: filter package; `frontend/src/pages/SlotPicker.jsx`: เปลี่ยน package แล้วโหลด slots ใหม่ | `SlotPicker.test.jsx` ผ่าน ตรวจเวลาเปลี่ยนหลังเปลี่ยนแพ็กเกจ แต่ไม่มี AC | ช่องโหว่ (F-02) |
| NFR-PERF-01 | AC-BKG-05 | T-02 เสร็จ | `backend/app/slots/service.py`: `list_available_slots` | `test_AC_BKG_05` ผ่านแต่เรียก 200 ครั้งต่อเนื่อง ไม่ได้จำลอง concurrent users | ช่องโหว่ (F-10) |
| NFR-SEC-01 | ไม่มี AC | ไม่มี task เฉพาะ | ไม่พบการตั้งค่า/บังคับ TLS 1.2+ ใน `backend/app/` หรือ `frontend/src/` | ไม่มี | ช่องโหว่ (F-14) |
| NFR-REL-02 | AC-BKG-04 | T-07 พร้อมทำ | ยังไม่มีคิวส่งซ้ำ | ไม่มี | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC | T-10/T-11 เสร็จ รอทีมตรวจ; T-12 พร้อมทำ | UI บางขั้นมีแล้ว แต่ยังไม่ต่อ workflow กับ API จริงและไม่มี usability session | setup test ผ่านแต่ไม่วัด 8/10 คนภายใน 3 นาที | ยังไม่ถึง |
| CON-TECH-01 | ไม่มี AC | T-01 เสร็จ | `backend/app/config.py`: default `DATABASE_URL` เป็น SQLite; `backend/app/db/session.py`: สร้าง engine จากค่านั้น | `test_T01_tables_created` ผ่านบน SQLite เท่านั้น | ช่องโหว่ (F-11) |
| DOM-PDPA-01 | AC-BKG-06 | T-01 เสร็จ; T-08 พร้อมทำ | `backend/app/db/models.py`: `AuditLog`; ไม่พบการเขียน audit log ใน endpoint/middleware | `test_T01_tables_created` ตรวจแค่ตาราง; ไม่มี test access logging | ยังไม่ถึง |
| IF-IDP-01 | AC-BKG-01 มีกรณีไม่ยืนยันตัวตนใน test-cases | T-03 เสร็จ | `backend/app/auth/idp.py`: `get_verified_hn` ตรวจ prefix เท่านั้น; `frontend/src/api/client.js`: ไม่ส่ง Authorization header | `test_TC_BKG_01_3_not_verified` ผ่าน; ไม่ตรวจ token ปลอมหรือ UI integration | ช่องโหว่ (F-12) |
| IF-HIS-01 | ไม่มี AC ตรง ๆ | T-01 เสร็จ; T-09 พร้อมทำ | ไม่มี HIS lookup; `BookingRequest` รับ `national_id` และ log ค่า | `test_T01_no_national_id` ผ่านเฉพาะการไม่มีคอลัมน์ใน bookings | ช่องโหว่ (F-13) |
| IF-NOT-01 | AC-BKG-04 | T-07 พร้อมทำ | ยังไม่มีการส่งงาน asynchronous | ไม่มี | ยังไม่ถึง |
| UI-BKG-01 | UI-BKG-01 | T-10 เสร็จ รอทีมตรวจ | `frontend/src/pages/SlotPicker.jsx`: package select, 3-step bar, list slot | `SlotPicker.test.jsx` ผ่าน แต่ไม่ตรวจ label/date/availability presentation | ช่องโหว่ (F-17) |
| UI-BKG-02 | UI-BKG-02 | T-11 เสร็จ รอทีมตรวจ | `frontend/src/pages/ConfirmBooking.jsx`: confirm/full state; duplicate state ไม่รองรับ | `AC-BKG-03.test.jsx` ผ่านแต่ไม่ตรวจ nearest options/no overlap; ไม่มี duplicate-state vitest | ช่องโหว่ (F-15, F-19, F-20) |

ผล test backend: 10 ผ่าน 0 ไม่ผ่าน (Starlette เตือน httpx deprecation). Frontend: 3 ผ่าน 0 ไม่ผ่าน (setup test เตือน React update ไม่ wrapped in act); ไม่มี `specs/000-shared/` จึงไม่มี shared constraints เพิ่ม

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| `backend/app/main.py`: `lifespan`, `app.include_router` | FR-BKG-01, FR-BKG-04 | บางส่วน | สร้าง tables และลงทะเบียน GET `/slots`, POST `/bookings`; ยังไม่มี endpoints HIS/audit/notification |
| `backend/app/slots/router.py`: GET `/slots`, `get_slots` | FR-BKG-01, FR-BKG-06 | บางส่วน | รับ `package_code`, `date_from`; ส่ง slot id/date/time/remaining; backend ส่ง date แต่ UI ไม่ render date |
| `backend/app/slots/service.py`: `list_available_slots` | FR-BKG-01, FR-BKG-06 | ไม่ตรง | filter package และ remaining ถูกต้อง แต่ `DAYS_AHEAD = 14` แทน 30 วัน |
| `backend/app/booking/router.py`: `BookingRequest`, POST `/bookings`, `create_booking` | FR-BKG-02, FR-BKG-04, IF-IDP-01, IF-HIS-01 | บางส่วน | request รับ `national_id`, log เขียน HN/national_id; duplicate เป็น 409 พร้อม queue_no ตามคำตอบทีม; response ปกติ booking_id/slot_id/queue_no; error อื่นยังไม่สรุป Q-03 |
| `backend/app/auth/idp.py`: `get_verified_hn` | IF-IDP-01 | ไม่ตรง | ตรวจ prefix `Bearer verified:` ไม่ได้ตรวจผลยืนยันตัวตนจาก IDP จริง |
| `backend/app/booking/service.py`: `ExistingBookingError`, `create_booking` | FR-BKG-02, FR-BKG-04 | ตรงบางส่วน | ตรวจ BOOKED ตาม HN/วันและคืนคิวเดิม; check กับ insert ไม่ atomic สำหรับ request พร้อมกัน (F-16); ลด remaining ด้วย conditional UPDATE |
| `backend/app/booking/service.py`: `SlotFullError` | FR-BKG-04 | ตรงบางส่วน | ช่วงเต็มถูกแปลงเป็น 409/detail; Q-03 ยังไม่กำหนด error contract โดยรวม |
| `backend/app/booking/service.py`: `next_queue_no` | FR-BKG-04, Q-02 | ไม่ตรง | เลือก `A{count + 1:03d}` และเริ่มนับใหม่รายวัน ทั้งที่รูปแบบและวิธีนับยังรอ Q-02 |
| `backend/app/db/models.py`: `Slot`, `Booking`, `AuditLog` | FR-BKG-01, FR-BKG-02, FR-BKG-04, DOM-PDPA-01, IF-HIS-01 | บางส่วน | schema มีข้อมูล slot/booking/audit และไม่มีคอลัมน์ national_id; ไม่มี audit writer; queue format ยังไม่ยืนยัน |
| `backend/app/config.py`: `DATABASE_URL`; `backend/app/db/session.py`: `engine`, `get_db` | CON-TECH-01 | ไม่ตรงเมื่อไม่กำหนด environment | default เป็น `sqlite:///./dev.db`; production ต้องตั้ง PostgreSQL เอง ไม่มี guard ใน code |
| `backend/app/db/migrations/001_init.py`: `upgrade` | CON-TECH-01, DOM-PDPA-01, IF-HIS-01 | บางส่วน | สร้าง schema; tests ใช้ SQLite จึงยังไม่ยืนยัน PostgreSQL |
| `frontend/src/App.jsx`: `App` | UI-BKG-01, UI-BKG-02, FR-BKG-01, FR-BKG-04 | ไม่ตรงทั้งหมด | ต่อหน้า SlotPicker/ConfirmBooking แต่ส่งเฉพาะ slot id แล้วกำหนดวันเป็น today และเวลา `09:00` คงที่แทน slot ที่เลือก (F-20) |
| `frontend/src/pages/SlotPicker.jsx`: `SlotPicker` | UI-BKG-01, FR-BKG-01, FR-BKG-06 | ไม่ตรง | มี package select และ 3 steps; แสดงเวลาและ “ว่าง N” แต่ไม่มีวันที่และไม่ใช้ข้อความ “เหลือ N ที่”; `onNext` ส่งเพียง id |
| `frontend/src/pages/ConfirmBooking.jsx`: `ConfirmBooking`, `confirm` | UI-BKG-02, FR-BKG-02, FR-BKG-03, FR-BKG-04 | ไม่ตรงบาง state | มีปุ่มยืนยัน, full text และไม่เกิน 3 ตัวเลือกพร้อมวันเวลา; ทุก 409 ถูกมองเป็นช่วงเต็ม จึงไม่แสดง duplicate message/queue number; success แสดง queue ที่ยังผูกกับ Q-02 |
| `frontend/src/api/client.js`: `getSlots`, `createBooking`, `cancelBooking` | FR-BKG-01, FR-BKG-03, FR-BKG-04, IF-IDP-01 | ไม่ตรงทั้งหมด | `createBooking` ไม่ส่ง Authorization; มี `cancelBooking` ทำ DELETE `/bookings/{id}` ทั้งที่ endpoint ไม่มีใน plan และยกเลิกอยู่ Out of scope (F-18) |

## 3. ข้อค้นพบ
ชนิดที่ใช้: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง / ไม่ตรง mockup / ของแถม

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-02 | FR ไม่มี AC | spec.md: FR-BKG-06 | FR-BKG-06 | `FR-BKG-06` ไม่มี Acceptance Criteria; Q-04 ที่เพิ่มไว้ยังรอทีมกำหนด AC ID | **แก้ spec:** เพิ่ม AC สำหรับ FR-BKG-06 ให้ชัดเจน |
| F-03 | FR ไม่มี AC | spec.md: FR-BKG-01 | FR-BKG-01 | มีเพียง AC-BKG-05 ด้านความเร็ว ไม่มี AC ตรวจช่วงว่างและจำนวนที่นั่งตาม FR-BKG-01; Q-04 ยังรอทีมกำหนด AC ID | **แก้ spec:** เพิ่ม AC การทำงานของ FR-BKG-01 |
| F-04 | อ้าง ID ผิดเรื่อง | `backend/app/booking/router.py`: `create_booking` | spec ยังไม่ระบุ error response/status code | สำหรับ duplicate ทีมเลือก 409 พร้อม `queue_no` แล้ว แต่ Q-03 ใน spec ยังไม่ตอบสำหรับ error อื่น เช่น 404 และช่วงเวลาเต็ม | **เพิ่ม Q-xx:** สอบถามทีมเกี่ยวกับรูปแบบ Error response และ status code |
| F-07 | ตัวเลขไม่ตรง spec | `backend/app/slots/service.py`: `DAYS_AHEAD` | FR-BKG-01 ระบุ 30 วัน | โค้ดค้นถึง `date_from + 14 วัน` จึงไม่แสดงช่วงเวลาตลอด 30 วันตาม requirement | |
| F-08 | test อ่อน | `backend/tests/test_AC_BKG_01.py`; TC-BKG-01-1/2 | AC-BKG-01 Then | test assert เพียง status 201/409 ไม่ตรวจ booking, remaining, หมายเลขคิว หรือผลที่นั่งเต็มให้ครบ; ส่วนแสดงคิวรอ Q-02 | |
| F-09 | เดา Q-xx | `backend/app/booking/service.py`: `next_queue_no`; `frontend/src/pages/ConfirmBooking.jsx` | Q-02 | กำหนด `A{count + 1:03d}`/เริ่มใหม่รายวัน และแสดงเลขดังกล่าวทั้งที่ Q-02 ยังไม่ตอบ; `A001` เป็นเพียงตัวอย่าง | |
| F-10 | test อ่อน | `backend/tests/test_AC_BKG_05.py`: `test_AC_BKG_05` | NFR-PERF-01, AC-BKG-05 | วนเรียก 200 requests ทีละรายการ ไม่ได้จำลองผู้ใช้พร้อมกัน 200 คน | |
| F-11 | ละเมิด Constraint | `backend/app/config.py`: `DATABASE_URL` | CON-TECH-01 | เมื่อไม่มี `DATABASE_URL` ระบบเลือก SQLite; ยังไม่มี guard ป้องกันการเปิดใช้งานโดยไม่ใช้ PostgreSQL ในระบบจริง | |
| F-12 | ละเมิด Constraint | `backend/app/auth/idp.py`: `get_verified_hn` | IF-IDP-01 | ตรวจเพียง prefix ของ bearer string ไม่ได้ยืนยันผลจากระบบ IDP; ผู้เรียกกำหนด HN เองได้ | |
| F-13 | ละเมิด Constraint | `backend/app/booking/router.py`: `BookingRequest`, logger | IF-HIS-01 | รับ `national_id` ใน request และบันทึกลง application log ทั้งที่ไม่ใช้ค้น HIS; ไม่มี HIS lookup และอาจเปิดเผยเลขบัตรใน log | |
| F-14 | ละเมิด Constraint | `backend/app/`, `frontend/src/` | NFR-SEC-01 | ไม่พบการตั้งค่าหรือหลักฐานบังคับ TLS 1.2+ ใน source; ยังยืนยันการเข้ารหัสระหว่างรับส่งไม่ได้ | |
| F-15 | test อ่อน | `frontend/src/pages/ConfirmBooking.jsx`; ไม่มี duplicate-state vitest | FR-BKG-02: “แสดงหมายเลขคิวเดิม” | frontend มีแล้วแต่ส่งทุก 409 ไป state “ช่วงเวลาเต็ม” และไม่แสดง `queue_no` เดิม; UI-BKG-02 mockup มี state “จองเพิ่มไม่ได้” พร้อมหมายเลขคิวเดิม; test backend ตรวจเพียง API response | |
| F-16 | test อ่อน | `backend/app/booking/service.py`: `create_booking`; `backend/tests/test_AC_BKG_02.py` | FR-BKG-02 | SELECT คิวเดิมกับ INSERT คิวใหม่ไม่ atomic และไม่มี constraint/lock กัน request พร้อมกัน; concurrent requests ของ HN/วันเดียวกันอาจผ่านทั้งคู่ แต่ test ทดสอบตามลำดับ | |
| F-17 | ไม่ตรง mockup | `frontend/src/pages/SlotPicker.jsx`: `SlotPicker` | UI-BKG-01, FR-BKG-01 | รายการเวลาไม่แสดงวันที่ของแต่ละ slot และแสดง “ว่าง N” แทนข้อความที่ spec กำหนด “เหลือ N ที่”; ทำให้ตรวจวันและจำนวนที่นั่งตาม UI ไม่ได้ครบ | |
| F-18 | ของแถม | `frontend/src/api/client.js`: `cancelBooking` | Out of scope: ยกเลิกคิว (UC-02) | ยังมี helper เรียก DELETE `/bookings/{id}` แม้ไม่มี route รองรับและการยกเลิกอยู่ใน Out of scope | |
| F-19 | test อ่อน | `frontend/src/__tests__/AC-BKG-03.test.jsx` | AC-BKG-03 Then; T-11 เสร็จ รอทีมตรวจ | test ตรวจข้อความ “ช่วงเวลาเต็ม” และจำนวน 3 ปุ่ม แต่ไม่ตรวจว่าตัวเลือกใกล้ 09.00 น. ที่สุด อยู่ในวันเดียวกัน/วันถัดไป หรือไม่มี booking ซ้อน | |
| F-20 | ไม่ตรง mockup | `frontend/src/App.jsx`: `onNext` | UI-BKG-02, FR-BKG-04 | เมื่อเลือก slot ส่งต่อเพียง id แล้วกำหนดวันเป็น `today` และเวลา `09:00` คงที่ ทำให้หน้าจอยืนยันอาจแสดงวัน/เวลาที่ไม่ใช่ slot ที่เลือก | |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
| F-01 | ลบ DELETE `/bookings/{id}` และ `cancel_booking` ออกจาก router/service | ตรวจ backend source ปัจจุบันไม่พบ endpoint/service ยกเลิก; แต่พบ frontend helper คงเหลือใน F-18 |
| F-05 | ใช้ conditional UPDATE ที่ลดที่นั่งเฉพาะเมื่อ `remaining > 0` | ตรวจ `create_booking` พบ predicate ใน UPDATE; backend tests 10 ผ่าน (ยังไม่มี test concurrent โดยเฉพาะ) |