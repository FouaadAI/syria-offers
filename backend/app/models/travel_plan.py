from sqlalchemy import Column, Integer, String, DateTime, JSON, func
from app.core.database import Base

class TravelPlan(Base):
    __tablename__ = "travel_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)            # Gast oder registriert
    preferences = Column(JSON, nullable=False)          # {"interests":["history","food"], "start_city":"Damaskus"}
    days = Column(Integer, nullable=False)
    plan_data = Column(JSON, nullable=False)            # generiertes JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())