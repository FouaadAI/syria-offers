from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Category(Base):
    """
    نموذج الأقسام: مطاعم، منتزهات، متاحف، سينما، مراكز طبية، الخ.
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name_ar = Column(String(255), nullable=False)        # مثل: "مطاعم"
    name_en = Column(String(255), nullable=False)        # مثل: "Restaurants"
    icon_url = Column(String(500), nullable=True)        # رابط أيقونة القسم
    sort_order = Column(Integer, default=0)              # ترتيب الظهور

    # العلاقة مع العروض
    offers = relationship("Offer", back_populates="category")


class Offer(Base):
    """
    نموذج العروض الأساسي. العرض مرتبط بقسم ونشاط محدد.
    """
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    title_ar = Column(String(500), nullable=False)
    title_en = Column(String(500), nullable=False)
    description_ar = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)

    # السعر
    original_price = Column(Float, nullable=False)
    offer_price = Column(Float, nullable=False)

    # التحكم بوقت الظهور
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)

    # الصور
    image_urls = Column(ARRAY(String), nullable=True)    # روابط صور العرض

    # الموقع الجغرافي (خطة مستقبلية للبحث بالقرب مني)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    # Separate multilingual location names
    location_name_ar = Column(String(500), nullable=True)   # اسم الحي أو المنطقة (عربي)
    location_name_en = Column(String(500), nullable=True)   # اسم الحي أو المنطقة (English)

    # الكمية المتاحة (للحجوزات المحدودة)
    max_bookings = Column(Integer, nullable=True)
    current_bookings = Column(Integer, default=0)

    # مفاتيح خارجية
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    category = relationship("Category", back_populates="offers")

    # الطوابع الزمنية
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # خصائص العروض الفلاشية
    is_flash = Column(Boolean, default=False)
    flash_discount_percent = Column(Integer, default=0)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=True)
    approved = Column(Boolean, default=False)  # يتطلب موافقة الأدمن
    priority = Column(Integer, default=0)       # 0-10، الأعلى يظهر أولاً
    view_count = Column(Integer, default=0)     # عدد المشاهدات
        # Bildqualität (NEU)
    image_quality_score = Column(Integer, nullable=True)
    image_category_match = Column(Boolean, nullable=True)
    image_validation_message = Column(Text, nullable=True)