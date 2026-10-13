# บันทึกการจองและตัดที่นั่ง (T-03)
# รองรับ FR-BKG-04
from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from app.db.models import Booking, Slot


class SlotFullError(Exception):
    """ช่วงเวลาที่เลือกไม่มีที่นั่งเหลือแล้ว"""


# รองรับ FR-BKG-02
class ExistingBookingError(Exception):
    """ผู้รับบริการมีคิวที่ยังไม่ได้ใช้ในวันเดียวกัน"""

    def __init__(self, booking: Booking):
        self.booking = booking


def next_queue_no(db: Session, slot_date) -> str:
    """ออกหมายเลขคิวรูปแบบ A001 เริ่มนับใหม่ทุกวัน (FR-BKG-04)"""
    count = db.scalar(
        select(func.count()).select_from(Booking).where(Booking.booking_date == slot_date)
    )
    return f"A{count + 1:03d}"


def create_booking(db: Session, hn: str, slot_id: int) -> Booking:
    """ยืนยันการจองและกันคิวซ้ำวันเดียวกัน (FR-BKG-02, FR-BKG-04)"""
    slot = db.get(Slot, slot_id)
    if slot is None:
        raise ValueError("ไม่พบช่วงเวลา")

    existing_booking = db.scalar(
        select(Booking)
        .where(
            Booking.hn == hn,
            Booking.booking_date == slot.slot_date,
            Booking.status == "BOOKED",
        )
        .order_by(Booking.id)
    )
    if existing_booking is not None:
        raise ExistingBookingError(existing_booking)

    result = db.execute(
        update(Slot)
        .where(Slot.id == slot_id, Slot.remaining > 0)
        .values(remaining=Slot.remaining - 1)
    )
    if result.rowcount != 1:
        raise SlotFullError(slot_id)

    db.refresh(slot)
    booking = Booking(
        hn=hn,
        slot_id=slot.id,
        booking_date=slot.slot_date,
        queue_no=next_queue_no(db, slot.slot_date),
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

