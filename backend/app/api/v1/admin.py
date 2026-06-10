from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy import func, text

from app.core.database import get_db
from app.core.config import settings
from app.models.offer import Offer, Category
from app.models.booking import Booking, BookingStatus
from app.models.user import User
from app.schemas.offer import OfferCreate, OfferResponse
from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/admin", tags=["لوحة التحكم"])

# ========== نماذج المصادقة ==========
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ========== إعدادات الأمان ==========
security = HTTPBearer()
import os
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "change-me-in-production")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=24))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="رمز غير صالح")

# ========== نقطة النهاية: تسجيل الدخول ==========
@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    if request.username == ADMIN_USERNAME and request.password == ADMIN_PASSWORD:
        access_token = create_access_token(data={"sub": request.username})
        return TokenResponse(access_token=access_token)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="اسم المستخدم أو كلمة المرور غير صحيحة")

# ========== لوحة المعلومات ==========
@router.get("/dashboard")
async def dashboard(db: Session = Depends(get_db), admin: str = Depends(verify_token)):
    active_offers = db.query(Offer).filter(
        Offer.is_active == True,
        Offer.approved == True,
        Offer.end_date > datetime.utcnow()
    ).count()

    total_bookings = db.query(Booking).count()
    pending_approval = db.query(Offer).filter(
        Offer.approved == False,
        Offer.is_active == True,
        Offer.end_date > datetime.utcnow()
    ).count()
    # استخراج مجموع المبيعات باستخدام func.sum
    total_revenue = db.query(func.sum(Booking.total_price)).filter(
        Booking.status == BookingStatus.CONFIRMED
    ).scalar() or 0

    flash_deals = db.query(Offer).filter(
        Offer.is_flash == True,
        Offer.is_active == True
    ).count()

    return {
        "active_offers": active_offers,
        "total_bookings": total_bookings,
        "total_revenue": total_revenue,
        "flash_deals": flash_deals,
        "pending_approval": pending_approval,
    }

# ========== إدارة الأقسام ==========
@router.get("/categories", response_model=List[CategoryResponse])
async def list_categories(db: Session = Depends(get_db), admin: str = Depends(verify_token)):
    return db.query(Category).all()

@router.post("/categories", response_model=CategoryResponse, status_code=201)
async def create_category(payload: CategoryCreate, db: Session = Depends(get_db), admin: str = Depends(verify_token)):
    category = Category(**payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, payload: CategoryCreate, db: Session = Depends(get_db), admin: str = Depends(verify_token)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="القسم غير موجود")
    for key, value in payload.model_dump().items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category

@router.delete("/categories/{category_id}")
async def delete_category(category_id: int, db: Session = Depends(get_db), admin: str = Depends(verify_token)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="القسم غير موجود")
    db.delete(category)
    db.commit()
    return {"message": "تم الحذف بنجاح"}

# ========== إدارة العروض ==========
@router.get("/offers", response_model=List[OfferResponse])
async def list_offers(db: Session = Depends(get_db), admin: str = Depends(verify_token)):
    db.expire_all()  # ⬅️ يمسح كل الكاش الداخلي للجلسة قبل الاستعلام
    return db.query(Offer).all()

@router.post("/offers", response_model=OfferResponse, status_code=201)
async def create_offer(payload: OfferCreate, db: Session = Depends(get_db), admin: str = Depends(verify_token)):
    data = payload.model_dump()
    offer = Offer(**data, is_active=True, approved=True)

    # ---------- Bildvalidierung (NEU) ----------
    if offer.image_urls:
        from app.services.image_validation import validate_image
        from app.models.offer import Category
        import requests as http_requests  # falls Bilder als HTTP-URLs vorliegen

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

@router.put("/offers/{offer_id}", response_model=OfferResponse)
async def update_offer(offer_id: int, payload: OfferCreate, db: Session = Depends(get_db), admin: str = Depends(verify_token)):
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="العرض غير موجود")
    for key, value in payload.model_dump().items():
        setattr(offer, key, value)
    db.commit()
    db.refresh(offer)
    return offer

@router.delete("/offers/{offer_id}")
async def delete_offer(offer_id: int, db: Session = Depends(get_db), admin: str = Depends(verify_token)):
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="العرض غير موجود")
    db.delete(offer)
    db.commit()
    return {"message": "تم حذف العرض"}

# ========== إدارة الحجوزات ==========
@router.get("/bookings")
async def list_bookings(db: Session = Depends(get_db), admin: str = Depends(verify_token)):
    bookings = db.query(Booking).all()
    return [{
        "id": b.id,
        "user_id": b.user_id,
        "offer_id": b.offer_id,
        "booked_at": b.booked_at,
        "quantity": b.quantity,
        "total_price": b.total_price,
        "status": b.status.value,
        "payment_method": b.payment_method,
        "created_at": b.created_at,
    } for b in bookings]

@router.put("/bookings/{booking_id}/status")
async def update_booking_status(booking_id: int, status: BookingStatus, db: Session = Depends(get_db), admin: str = Depends(verify_token)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="الحجز غير موجود")
    booking.status = status
    db.commit()
    return {"message": f"تم تغيير الحالة إلى {status.value}"}

# في admin.py، أضف بعد المسارات الحالية

@router.get("/offers/pending", response_model=List[OfferResponse])
async def list_pending_offers(db: Session = Depends(get_db), admin: str = Depends(verify_token)):
    """العروض التي لم تتم الموافقة عليها بعد"""
    offers = db.query(Offer).filter(Offer.approved == False).all()
    return offers

from sqlalchemy import text

@router.put("/offers/{offer_id}/approve", response_model=OfferResponse)
async def approve_offer(offer_id: int, db: Session = Depends(get_db), admin: str = Depends(verify_token)):
    # تنفيذ التحديث مباشرة دون الاعتماد على كائن ORM للتزامن
    db.execute(
        text("UPDATE offers SET approved = TRUE, updated_at = now() WHERE id = :oid"),
        {"oid": offer_id}
    )
    db.commit()
    
    # استرجاع الكائن المحدّث من قاعدة البيانات بقوة
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="العرض غير موجود")
    db.refresh(offer)
    return offer

@router.delete("/offers/{offer_id}/reject")
async def reject_offer(offer_id: int, db: Session = Depends(get_db), admin: str = Depends(verify_token)):
    offer = db.query(Offer).filter(Offer.id == offer_id, Offer.approved == False).first()
    if not offer:
        raise HTTPException(status_code=404, detail="العرض غير موجود أو معتمد بالفعل")
    db.delete(offer)
    db.commit()
    return {"message": "تم رفض العرض وحذفه"}