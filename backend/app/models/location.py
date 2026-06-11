from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, Index
from app.core.database import Base


class Location(Base):
    """
    Professional Syria tourism database — one row per point of interest.
    Populated from planner_data.json on first startup.
    """
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)

    # Multilingual names
    name_ar = Column(String(200), nullable=False)
    name_de = Column(String(200), nullable=True)
    name_en = Column(String(200), nullable=True)

    # City (multilingual)
    city_ar = Column(String(100), nullable=False)
    city_de = Column(String(100), nullable=True)
    city_en = Column(String(100), nullable=True)

    # Coordinates
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)

    # Classification
    category = Column(String(50), nullable=False, index=True)

    # Descriptions (description_de removed per project decision)
    description_ar = Column(String(2000), nullable=True)
    description_en = Column(String(2000), nullable=True)

    # Practical info
    visit_duration = Column(String(20), nullable=True)   # e.g. "1h", "half-day"
    price_range = Column(String(20), nullable=True)    # free | cheap | moderate | expensive
    opening_hours = Column(String(50), nullable=True)    # e.g. "08:00-18:00" or "N/A"
    best_time = Column(String(20), nullable=True)        # morning | afternoon | evening | sunset
    wheelchair = Column(String(20), nullable=True)       # yes | no | partial
    family_friendly = Column(Boolean, default=True)
    age_group = Column(String(20), nullable=True)        # all | kids | teens | adults | seniors

    # Relationships — stored as JSON array of Arabic place names
    nearby_places = Column(JSON, nullable=True)

    # Composite indexes for common planner queries
    __table_args__ = (
        Index("idx_loc_city_category", "city_en", "category"),
        Index("idx_loc_city_ar", "city_ar", "category"),
        Index("idx_loc_coords", "lat", "lng"),
    )
