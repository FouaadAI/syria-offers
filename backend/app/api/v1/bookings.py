from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import random

from app.core.database import get_db
from app.models.booking import Booking, BookingStatus
from app.schemas.booking import BookingCreate, BookingResponse

router = APIRouter(prefix="/bookings", tags=["الحجوزات"])

def generate_booking_code() -> str:
    """ينشئ رمز حجز فريد مثال: BOOK-250429-7A3F"""
    now = datetime.now()
    date_part = now.strftime("%y%m%d")
    random_part = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=4))
    return f"BOOK-{date_part}-{random_part}"

@router.post("/", response_model=BookingResponse, status_code=201)
async def create_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    """إنشاء حجز جديد وتخزينه في قاعدة البيانات"""
    
    # التأكد من وجود العرض (اختياري، يمكن إضافته لاحقاً)
    # offer = db.query(Offer).filter(Offer.id == payload.offer_id).first()
    # if not offer:
    #     raise HTTPException(status_code=404, detail="العرض غير موجود")

    booking = Booking(
        user_id=1,  # حالياً مستخدم افتراضي (سنضيف نظام مستخدمين لاحقاً)
        offer_id=payload.offer_id,
        booked_at=payload.booked_at,
        quantity=payload.quantity,
        total_price=payload.total_price,
        status=BookingStatus.CONFIRMED,
        payment_id=f"WALLET-{random.randint(1000000, 9999999)}",
        payment_method="محفظة إليكترونية",
    )
    
    db.add(booking)
    db.commit()
    db.refresh(booking)
    
    # بناء الاستجابة مع رمز الحجز
    return {
        "id": booking.id,
        "booking_code": generate_booking_code(),
        "user_name": payload.user_name,
        "user_phone": payload.user_phone,
        "offer_id": payload.offer_id,
        "booked_at": payload.booked_at,
        "quantity": payload.quantity,
        "total_price": payload.total_price,
        "status": booking.status.value,
        "created_at": booking.created_at,
    }