from pydantic import BaseModel
from typing import Optional


class CategoryBase(BaseModel):
    name_ar: str
    name_en: str
    icon_url: Optional[str] = None
    sort_order: int = 0


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True  # للتوافق مع كائنات SQLAlchemy مباشرة