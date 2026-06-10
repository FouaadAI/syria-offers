from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.booking import Booking, BookingStatus
from app.models.offer import Offer

router = APIRouter(prefix="/reports", tags=["التقارير"])

@router.get("/daily")
async def daily_report(db: Session = Depends(get_db)):
    today = datetime.utcnow().date()
    start = datetime.combine(today, datetime.min.time())
    end = start + timedelta(days=1)
    
    bookings = db.query(Booking).filter(
        Booking.created_at >= start,
        Booking.created_at < end,
        Booking.status == BookingStatus.CONFIRMED,
    ).all()
    
    revenue = sum(b.total_price for b in bookings)
    
    return {
        "date": str(today),
        "total_bookings": len(bookings),
        "total_revenue": revenue,
    }

@router.get("/top-offers")
async def top_offers(db: Session = Depends(get_db), limit: int = 10):
    offers = db.query(Offer).filter(
        Offer.is_active == True,
        Offer.approved == True,
    ).order_by(Offer.view_count.desc()).limit(limit).all()
    
    return [{
        "id": o.id,
        "title": o.title_ar,
        "views": o.view_count,
        "bookings": db.query(Booking).filter(
            Booking.offer_id == o.id,
            Booking.status == BookingStatus.CONFIRMED,
        ).count(),
    } for o in offers]