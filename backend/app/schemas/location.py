from pydantic import BaseModel
from typing import List, Optional


class LocationBase(BaseModel):
    name_ar: str
    name_de: Optional[str] = None
    name_en: Optional[str] = None
    city_ar: str
    city_de: Optional[str] = None
    city_en: Optional[str] = None
    lat: float
    lng: float
    category: str
    description_ar: Optional[str] = None
    description_en: Optional[str] = None
    visit_duration: Optional[str] = None
    price_range: Optional[str] = None
    opening_hours: Optional[str] = None
    best_time: Optional[str] = None
    wheelchair: Optional[str] = None
    family_friendly: bool = True
    age_group: Optional[str] = None
    nearby_places: Optional[List[str]] = []


class LocationCreate(LocationBase):
    pass


class LocationOut(LocationBase):
    id: int

    class Config:
        from_attributes = True
