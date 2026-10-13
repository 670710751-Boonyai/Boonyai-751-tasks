# Tests for AC-BKG-02 (FR-BKG-02)
from sqlalchemy import func, select

from app.db.models import Booking
from tests.conftest import AUTH


def test_TC_BKG_02_1_existing_same_day(client, db, make_slot):
    # Given: verified patient has an unused booking on the same day
    previous_slot = make_slot(start="09:00", days_from_today=1)
    target_slot = make_slot(start="10:00", days_from_today=1)
    previous_booking = Booking(
        hn="0001234",
        slot_id=previous_slot.id,
        booking_date=previous_slot.slot_date,
        queue_no="existing-queue",
    )
    db.add(previous_booking)
    db.commit()

    # When: the patient tries to book another slot on that day
    response = client.post("/bookings", json={"slot_id": target_slot.id}, headers=AUTH)

    # Then: reject the new booking and return the original queue number
    assert response.status_code != 201
    assert response.json().get("queue_no") == previous_booking.queue_no
    booking_count = db.scalar(
        select(func.count()).select_from(Booking).where(Booking.hn == "0001234")
    )
    assert booking_count == 1


def test_TC_BKG_02_2_next_day(client, db, make_slot):
    # Given: verified patient has an unused booking on one day
    previous_slot = make_slot(start="09:00", days_from_today=1)
    target_slot = make_slot(start="09:00", days_from_today=2)
    db.add(
        Booking(
            hn="0001234",
            slot_id=previous_slot.id,
            booking_date=previous_slot.slot_date,
            queue_no="existing-queue",
        )
    )
    db.commit()

    # When: the patient books a slot on the following day
    response = client.post("/bookings", json={"slot_id": target_slot.id}, headers=AUTH)

    # Then: allow and save the booking for the following day
    assert response.status_code == 201
    assert response.json()["slot_id"] == target_slot.id
    booking_count = db.scalar(
        select(func.count())
        .select_from(Booking)
        .where(Booking.hn == "0001234", Booking.booking_date == target_slot.slot_date)
    )
    assert booking_count == 1


def test_TC_BKG_02_3_previous_booking_used(client, db, make_slot):
    # Given: verified patient has a used booking on the same day
    previous_slot = make_slot(start="09:00", days_from_today=1)
    target_slot = make_slot(start="10:00", days_from_today=1)
    db.add(
        Booking(
            hn="0001234",
            slot_id=previous_slot.id,
            booking_date=previous_slot.slot_date,
            queue_no="existing-queue",
            status="USED",
        )
    )
    db.commit()

    # When: the patient books another slot on that day
    response = client.post("/bookings", json={"slot_id": target_slot.id}, headers=AUTH)

    # Then: allow and save the new booking on the same day
    assert response.status_code == 201
    assert response.json()["slot_id"] == target_slot.id
    booking_count = db.scalar(
        select(func.count())
        .select_from(Booking)
        .where(Booking.hn == "0001234", Booking.booking_date == target_slot.slot_date)
    )
    assert booking_count == 2