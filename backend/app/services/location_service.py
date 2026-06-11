"""
Location Service — DB-backed queries for the Syria tourism dataset.
Replaces the old in-memory syria_locations module.
"""
import json
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.location import Location
from app.data.city_distances import get_distance, INTEREST_TO_CATEGORIES


# ---------------------------------------------------------------------------
#  Bulk import (called once on startup if table is empty)
# ---------------------------------------------------------------------------

def import_locations_from_json(db: Session, json_path: str) -> int:
    """Import all locations from planner_data.json into the database."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    count = 0
    for item in data:
        # Skip duplicates — composite unique on name_ar + city_ar
        exists = db.query(Location).filter(
            Location.name_ar == item.get("name_ar"),
            Location.city_ar == item.get("city_ar"),
        ).first()
        if exists:
            continue

        loc = Location(
            name_ar=item.get("name_ar", ""),
            name_de=item.get("name_de"),
            name_en=item.get("name_en"),
            city_ar=item.get("city_ar", ""),
            city_de=item.get("city_de"),
            city_en=item.get("city_en"),
            lat=item.get("lat", 0.0),
            lng=item.get("lng", 0.0),
            category=item.get("category", "other"),
            description_ar=item.get("description_ar"),
            description_en=item.get("description_en"),
            visit_duration=item.get("visit_duration"),
            price_range=item.get("price_range"),
            opening_hours=item.get("opening_hours"),
            best_time=item.get("best_time"),
            wheelchair=item.get("wheelchair"),
            family_friendly=item.get("family_friendly", True),
            age_group=item.get("age_group"),
            nearby_places=item.get("nearby_places", []),
        )
        db.add(loc)
        count += 1

    db.commit()
    return count


# ---------------------------------------------------------------------------
#  Query helpers
# ---------------------------------------------------------------------------

def get_locations_in_city(db: Session, city: str, limit: int = 200) -> List[Location]:
    """All places inside a city (matches city_en or city_ar, case-insensitive)."""
    city_clean = city.strip().lower()
    return db.query(Location).filter(
        func.lower(Location.city_en) == city_clean
    ).limit(limit).all()


def get_locations_by_categories(db: Session, categories: List[str], limit: int = 200) -> List[Location]:
    """Places matching any of the given categories (case-insensitive)."""
    cats_lower = [c.lower() for c in categories]
    return db.query(Location).filter(
        func.lower(Location.category).in_(cats_lower)
    ).limit(limit).all()


def get_locations_by_interest(db: Session, interest: str, limit: int = 200) -> List[Location]:
    """Fuzzy-match an interest string to categories."""
    cats = INTEREST_TO_CATEGORIES.get(interest.lower(), [interest.lower()])
    return get_locations_by_categories(db, cats, limit)


def get_location_by_name(db: Session, name_ar: str) -> Optional[Location]:
    return db.query(Location).filter(Location.name_ar == name_ar).first()


def get_all_cities(db: Session) -> List[Tuple[str, str, str]]:
    """Return distinct (city_ar, city_de, city_en) tuples."""
    rows = db.query(Location.city_ar, Location.city_de, Location.city_en).distinct().all()
    return [(r[0], r[1], r[2]) for r in rows]


def search_locations(
    db: Session,
    city: Optional[str] = None,
    category: Optional[str] = None,
    interests: Optional[List[str]] = None,
    limit: int = 50,
) -> List[Location]:
    """
    Flexible search used by the planner and chatbot.
    Priority scoring happens in the planner layer.
    """
    q = db.query(Location)

    if city:
        city_clean = city.strip().lower()
        q = q.filter(
            (func.lower(Location.city_en) == city_clean) |
            (func.lower(Location.city_ar) == city_clean)
        )

    if category:
        q = q.filter(func.lower(Location.category) == category.lower())

    if interests:
        cats = set()
        for interest in interests:
            cats.update(INTEREST_TO_CATEGORIES.get(interest.lower(), [interest.lower()]))
        if cats:
            q = q.filter(func.lower(Location.category).in_(list(cats)))

    return q.limit(limit).all()


def count_locations(db: Session) -> int:
    return db.query(Location).count()
