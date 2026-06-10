from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class BookingStatus(str, enum.Enum):
    PENDING = "pending"          # بانتظار تأكيد الدفع
    CONFIRMED = "confirmed"      # تم الدفع والتأكيد
    CANCELLED = "cancelled"      # ملغي
    REFUNDED = "refunded"        # تم الاسترجاع


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    offer_id = Column(Integer, ForeignKey("offers.id"), nullable=False)

    # تفاصيل الحجز
    booked_at = Column(DateTime(timezone=True), nullable=False)        # التاريخ الذي اختاره المستخدم
    quantity = Column(Integer, default=1)                              # عدد التذاكر/الأشخاص
    total_price = Column(Float, nullable=False)                        # السعر الإجمالي بعد الضرب

    # حالة الحجز والدفع
    status = Column(SQLEnum(BookingStatus), default=BookingStatus.PENDING)
    payment_id = Column(String(500), nullable=True)                    # معرف العملية من بوابة الدفع
    payment_method = Column(String(100), nullable=True)                # اسم المحفظة المستخدمة

    # طوابع زمنية
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # العلاقات
    user = relationship("User")
    offer = relationship("Offer")