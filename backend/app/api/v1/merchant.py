# backend/app/api/v1/merchant.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from app.models.merchant import Merchant
from app.models.offer import Offer
from app.models.booking import Booking, BookingStatus
from app.schemas.offer import OfferCreate, OfferResponse
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List

router = APIRouter(prefix="/merchant", tags=["التاجر"])

security = HTTPBearer()

def get_current_merchant(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Merchant:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = int(payload.get("sub"))
        role = payload.get("role")
        if role != "merchant":
            raise HTTPException(status_code=403, detail="يجب أن تكون تاجراً")
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="رمز غير صالح")
    
    merchant = db.query(Merchant).filter(Merchant.user_id == user_id).first()
    if not merchant:
        raise HTTPException(status_code=404, detail="ملف التاجر غير موجود")
    return merchant

@router.get("/dashboard")
async def dashboard(merchant: Merchant = Depends(get_current_merchant), db: Session = Depends(get_db)):
    offers = db.query(Offer).filter(Offer.merchant_id == merchant.id).all()
    total_offers = len(offers)
    active_offers = sum(1 for o in offers if o.is_active and o.approved)
    pending_offers = sum(1 for o in offers if not o.approved)
    
    bookings = db.query(Booking).filter(Booking.offer_id.in_([o.id for o in offers])).all()
    total_bookings = len(bookings)
    total_views = sum(o.view_count for o in offers)
    
    return {
        "total_offers": total_offers,
        "active_offers": active_offers,
        "pending_offers": pending_offers,
        "total_bookings": total_bookings,
        "total_views": total_views,
    }

@router.get("/offers", response_model=List[OfferResponse])
async def my_offers(merchant: Merchant = Depends(get_current_merchant), db: Session = Depends(get_db)):
    db.expire_all()  # ⬅️ يمسح الكاش قبل جلب عروض التاجر
    return db.query(Offer).filter(Offer.merchant_id == merchant.id).all()
@router.post("/offers", response_model=OfferResponse, status_code=201)
async def create_my_offer(
    payload: OfferCreate,
    merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    data = payload.model_dump()
    offer = Offer(**data, merchant_id=merchant.id, is_active=True, approved=False)

    # ---------- Bildvalidierung (wie oben) ----------
    if offer.image_urls:
        from app.services.image_validation import validate_image
        from app.models.offer import Category
        import requests as http_requests

        cat = db.query(Category).filter(Category.id == payload.category_id).first()
        cat_name = cat.name_ar if cat else "Allgemein"

        scores = []
        matches = []
        messages = []
        for url in offer.image_urls:
            try:
                resp = http_requests.get(url, timeout=10)
                if resp.status_code == 200:
                    content_type = resp.headers.get("Content-Type", "image/jpeg")
                    img_bytes = resp.content
                    result = validate_image(img_bytes, cat_name, content_type)
                    scores.append(result["score"])
                    matches.append(result["match"])
                    messages.append(result["message"])
            except Exception:
                messages.append("Konnte Bild nicht laden")
                scores.append(0)
                matches.append(False)

        if scores:
            offer.image_quality_score = sum(scores) // len(scores)
            offer.image_category_match = all(matches)
            offer.image_validation_message = "; ".join(messages)
    # ---------- Ende Bildvalidierung ----------

    db.add(offer)
    db.commit()
    db.refresh(offer)
    return offer

@router.delete("/offers/{offer_id}")
async def delete_my_offer(
    offer_id: int,
    merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    offer = db.query(Offer).filter(Offer.id == offer_id, Offer.merchant_id == merchant.id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="العرض غير موجود")
    db.delete(offer)
    db.commit()
    return {"message": "تم حذف العرض"}

@router.get("/bookings")
async def my_bookings(merchant: Merchant = Depends(get_current_merchant), db: Session = Depends(get_db)):
    offers = db.query(Offer).filter(Offer.merchant_id == merchant.id).all()
    offer_ids = [o.id for o in offers]
    return db.query(Booking).filter(Booking.offer_id.in_(offer_ids)).all()