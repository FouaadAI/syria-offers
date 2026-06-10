from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.offer import Category
from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["التصنيفات"])


@router.get("/", response_model=List[CategoryResponse])
async def list_categories(db: Session = Depends(get_db)):
    """جلب جميع الأقسام النشطة مرتبة حسب ترتيب الظهور"""
    return db.query(Category).order_by(Category.sort_order).all()


@router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    """إضافة قسم جديد (يُستخدم يدوياً من قبلك حالياً)"""
    category = Category(**payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category