# API จองคิว POST /bookings (T-03)
# รองรับ FR-BKG-04, IF-IDP-01
import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.idp import get_verified_hn
from app.booking import service
from app.db.session import get_db

logger = logging.getLogger("booking")
router = APIRouter()


class BookingRequest(BaseModel):
    slot_id: int
    national_id: str | None = None  # เผื่อใช้ค้น HN จาก HIS


@router.post("/bookings", status_code=201)
def create_booking(req: BookingRequest, hn: str = Depends(get_verified_hn), db: Session = Depends(get_db)):
    """ยืนยันการจองและปฏิเสธคิวซ้ำในวันเดียวกัน (FR-BKG-02, FR-BKG-04)"""
    logger.info("booking request slot=%s hn=%s national_id=%s", req.slot_id, hn, req.national_id)
    try:
        booking = service.create_booking(db, hn=hn, slot_id=req.slot_id)
    except service.ExistingBookingError as e:
        return JSONResponse(status_code=409, content={"queue_no": e.booking.queue_no})
    except service.SlotFullError:
        raise HTTPException(status_code=409, detail="ช่วงเวลาเต็ม")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"booking_id": booking.id, "slot_id": booking.slot_id, "queue_no": booking.queue_no}
