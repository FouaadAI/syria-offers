from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2

from app.core.database import get_db
from app.models.offer import Offer
from app.schemas.offer import OfferCreate, OfferResponse

router = APIRouter(prefix="/offers", tags=["العروض"])


@router.get("/", response_model=List[OfferResponse])
async def list_active_offers(
    category_id: Optional[int] = Query(None),
    q: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
    lng: Optional[float] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Offer).filter(
        Offer.is_active == True,
        Offer.end_date > datetime.utcnow(),
        Offer.approved == True,  # فقط العروض المعتمدة
    )
    if category_id:
        query = query.filter(Offer.category_id == category_id)

    # multilingual search (title and location in Arabic/English)
    if q and q.strip():
        term = f"%{q.strip()}%"
        query = query.filter(
            or_(
                Offer.title_ar.ilike(term),
                Offer.title_en.ilike(term),
                Offer.location_name_ar.ilike(term),
                Offer.location_name_en.ilike(term),
            )
        )

    # fetch baseline ordered list (priority, recency)
    offers = query.order_by(Offer.priority.desc(), Offer.created_at.desc()).all()

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    user_lon = lon if lon is not None else lng

    if lat is not None and user_lon is not None:
        # compute distance; offers with missing coords placed at end
        def dist_key(o):
            if o.latitude is None or o.longitude is None:
                return float('inf')
            return haversine(lat, user_lon, o.latitude, o.longitude)
        offers.sort(key=dist_key)

    return offers

@router.post("/", response_model=OfferResponse, status_code=201)
async def create_offer(payload: OfferCreate, db: Session = Depends(get_db)):
    """إضافة عرض جديد (يدوياً حالياً)"""
    offer = Offer(**payload.model_dump(), is_active=True)
    db.add(offer)
    db.commit()
    db.refresh(offer)
    return offer
