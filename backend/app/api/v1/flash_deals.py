from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.models.offer import Offer
from app.schemas.offer import OfferResponse
from typing import List

router = APIRouter(prefix="/flash-deals", tags=["العروض الفلاشية"])

@router.get("/", response_model=List[OfferResponse])
async def get_flash_deals(db: Session = Depends(get_db)):
    """جلب العروض الفلاشية النشطة حالياً"""
    now = datetime.utcnow()
    deals = db.query(Offer).filter(
        Offer.is_flash == True,
        Offer.is_active == True,
        Offer.start_date <= now,
        Offer.end_date > now
    ).order_by(Offer.end_date).all()
    return deals