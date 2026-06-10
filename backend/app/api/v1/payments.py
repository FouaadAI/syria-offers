from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.core.database import get_db
from app.models.booking import Booking, BookingStatus
from app.services.payment import PaymentGateway, PaymentRequest, PaymentMethod

router = APIRouter(prefix="/payments", tags=["الدفع"])

@router.post("/pay")
async def process_payment(
    booking_id: int,
    amount: float,
    phone: str,
    method: PaymentMethod,
    db: Session = Depends(get_db),
):
    # التحقق من الحجز
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="الحجز غير موجود")
    
    gateway = PaymentGateway()
    result = await gateway.process_payment(PaymentRequest(
        amount=amount,
        phone=phone,
        method=method,
        booking_id=booking_id,
    ))
    
    if result.success:
        booking.status = BookingStatus.CONFIRMED
        booking.payment_id = result.transaction_id
        booking.payment_method = method.value
        db.commit()
    
    return result


@router.post("/refund")
async def process_refund(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="الحجز غير موجود")

    if booking.status == BookingStatus.REFUNDED:
        raise HTTPException(status_code=400, detail="تم استرداد هذا الحجز مسبقاً")

    now = datetime.now(timezone.utc)
    booked_at = booking.booked_at
    if booked_at.tzinfo is None:
        booked_at = booked_at.replace(tzinfo=timezone.utc)

    if (booked_at - now).total_seconds() < 3600:
        raise HTTPException(
            status_code=400,
            detail="الإلغاء غير مسموح: يجب أن يكون قبل موعد الحجز بساعة على الأقل",
        )

    service_fee = round(booking.total_price * 0.10, 2)
    refund_amount = round(booking.total_price - service_fee, 2)

    booking.status = BookingStatus.REFUNDED
    db.commit()
    db.refresh(booking)

    return {
        "success": True,
        "booking_id": booking.id,
        "original_amount": booking.total_price,
        "service_fee": service_fee,
        "refund_amount": refund_amount,
        "status": booking.status.value,
    }
