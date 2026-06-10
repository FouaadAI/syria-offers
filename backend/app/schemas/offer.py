from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class OfferBase(BaseModel):
    title_ar: str
    title_en: str
    description_ar: Optional[str] = None
    description_en: Optional[str] = None
    original_price: float
    offer_price: float
    start_date: datetime
    end_date: datetime
    image_urls: Optional[List[str]] = None
    category_id: int
    is_flash: bool = False
    flash_discount_percent: int = 0
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_name_ar: Optional[str] = None
    location_name_en: Optional[str] = None

class OfferCreate(OfferBase):
    pass

class OfferResponse(OfferBase):
    id: int
    is_active: bool
    created_at: datetime
    image_quality_score: Optional[int] = None
    image_category_match: Optional[bool] = None
    image_validation_message: Optional[str] = None
    class Config:
        from_attributes = True