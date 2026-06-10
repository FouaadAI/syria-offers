from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class TravelPlanRequest(BaseModel):
    preferences: Dict[str, Any]
    days: int

class Activity(BaseModel):
    time: str
    title: str
    location: str
    lat: float
    lng: float
    description: Optional[str] = None
    offer_id: Optional[int] = None

class DayPlan(BaseModel):
    day: int
    activities: List[Activity]

class TravelPlanResponse(BaseModel):
    id: int
    plan: List[DayPlan]