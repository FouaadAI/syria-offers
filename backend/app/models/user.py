from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, Text
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=False)
    verification_code = Column(String(6), nullable=True)
    role = Column(String(20), default='customer')  # customer, merchant, admin
    # إعدادات الإشعارات يخزنها المستخدم بنفسه
    notification_settings = Column(JSON, default=lambda: {
        "promotions": True,
        "reminders": True,
        "quiet_hours_start": None,  # مثال "22:00"
        "quiet_hours_end": None     # مثال "08:00"
    })

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # Neue Felder für Bildqualität
