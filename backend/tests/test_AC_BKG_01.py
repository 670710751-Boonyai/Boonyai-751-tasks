# test ของ T-03: จองคิวสำเร็จ
# AC-BKG-01 (FR-BKG-04)
from tests.conftest import AUTH


def test_AC_BKG_01(client, make_slot):
    """AC-BKG-01: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง จองแล้วต้องสำเร็จ"""
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201
def test_TC_BKG_01_1_last_seat(client, make_slot):
    """TC-BKG-01-1: ยืนยันตัวตนแล้ว ช่วง 09.00 น. เหลือ 1 ที่ จองสำเร็จ"""
    slot = make_slot(start="09:00", remaining=1)
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)
    assert res.status_code == 201
    # Note: รอ Q-02 เรื่องหมายเลขคิว


def test_TC_BKG_01_2_no_seat(client, make_slot):
    """TC-BKG-01-2: ยืนยันตัวตนแล้ว ช่วง 09.00 น. เหลือ 0 ที่ ต้องตอบ 409"""
    slot = make_slot(start="09:00", remaining=0)
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)
    assert res.status_code == 409


def test_TC_BKG_01_3_not_verified(client, make_slot):
    """TC-BKG-01-3: ยังไม่ได้ยืนยันตัวตน ช่วง 09.00 น. เหลือ 1 ที่ ต้องตอบ 401"""
    slot = make_slot(start="09:00", remaining=1)
    res = client.post("/bookings", json={"slot_id": slot.id})  # ไม่ส่ง headers=AUTH
    assert res.status_code == 401