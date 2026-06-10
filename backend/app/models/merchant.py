from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class BusinessType(str, enum.Enum):
    RESTAURANT = "restaurant"
    PARK = "park"
    MUSEUM = "museum"
    CINEMA = "cinema"
    ACTIVITY = "activity"
    MEDICAL = "medical"
    OTHER = "other"

class SubscriptionPlan(str, enum.Enum):
    FREE = "free"
    PREMIUM = "premium"

class Merchant(Base):
    __tablename__ = "merchants"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    business_name = Column(String(255), nullable=False)
    business_type = Column(SQLEnum(BusinessType), default=BusinessType.OTHER)
    is_verified = Column(Boolean, default=False)
    subscription_plan = Column(SQLEnum(SubscriptionPlan), default=SubscriptionPlan.FREE)
    
    user = relationship("User")