from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BookingCreate(BaseModel):
    user_name: str
    user_phone: str
    offer_id: int
    booked_at: datetime
    quantity: int = 1
    total_price: float

class BookingResponse(BaseModel):
    id: int
    booking_code: str
    user_name: str
    user_phone: str
    offer_id: int
    booked_at: datetime
    quantity: int
    total_price: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True