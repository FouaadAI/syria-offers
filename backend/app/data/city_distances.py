"""
Static city-to-city distance matrix for Syria.
Used by the travel planner for realistic multi-city routing.
"""
from typing import List, Tuple, Dict

# Format: ((city_a_ar, city_b_ar), distance_km, drive_time_hours)
DISTANCES: List[Tuple[Tuple[str, str], float, float]] = [
    # Damascus hub
    (("دمشق", "معَلولا"), 55, 1.0),
    (("دمشق", "صيدنايا"), 30, 0.5),
    (("دمشق", "بصرى"), 140, 2.0),
    (("دمشق", "تدمر"), 215, 2.5),
    (("دمشق", "حلب"), 355, 4.0),
    (("دمشق", "حماة"), 210, 2.5),
    (("دمشق", "حمص"), 165, 2.0),
    (("دمشق", "اللاذقية"), 330, 3.5),
    (("دمشق", "طرطوس"), 290, 3.0),
    (("دمشق", "السويداء"), 110, 1.5),
    (("دمشق", "درعا"), 100, 1.5),
    (("دمشق", "دير الزور"), 450, 5.0),
    (("دمشق", "الرقة"), 380, 4.5),
    (("دمشق", "إدلب"), 320, 3.5),
    (("دمشق", "القامشلي"), 680, 7.0),
    (("دمشق", "الحسكة"), 650, 7.0),
    # Aleppo hub
    (("حلب", "حماة"), 150, 1.5),
    (("حلب", "حمص"), 190, 2.0),
    (("حلب", "إدلب"), 65, 1.0),
    (("حلب", "اللاذقية"), 185, 2.0),
    (("حلب", "طرطوس"), 220, 2.5),
    (("حلب", "الرقة"), 160, 2.0),
    (("حلب", "القامشلي"), 340, 4.0),
    # Homs hub
    (("حمص", "حماة"), 45, 0.5),
    (("حمص", "طرطوس"), 125, 1.5),
    (("حمص", "اللاذقية"), 165, 2.0),
    (("حمص", "السويداء"), 90, 1.0),
    (("حمص", "بصرى"), 110, 1.5),
    # Hama hub
    (("حماة", "إدلب"), 90, 1.0),
    (("حماة", "اللاذقية"), 135, 1.5),
    (("حماة", "طرطوس"), 155, 1.5),
    # Latakia hub
    (("اللاذقية", "طرطوس"), 85, 1.0),
    (("اللاذقية", "إدلب"), 145, 1.5),
    # Sweida hub
    (("السويداء", "بصرى"), 80, 1.0),
    (("السويداء", "درعا"), 65, 1.0),
    # Deir Ezzor hub
    (("دير الزور", "الرقة"), 200, 2.0),
    (("دير الزور", "الحسكة"), 240, 2.5),
    (("دير الزور", "القامشلي"), 270, 3.0),
    # Qamishli / Hasakah
    (("القامشلي", "الحسكة"), 80, 1.0),
]


def get_distance(city_a: str, city_b: str) -> Tuple[float, float]:
    """Return (km, drive_hours) between two cities. Falls back to rough estimate if unknown."""
    if city_a == city_b:
        return 0.0, 0.0
    for (a, b), km, hrs in DISTANCES:
        if (a == city_a and b == city_b) or (a == city_b and b == city_a):
            return km, hrs
    # fallback estimate: ~70 km/h average on Syrian roads
    return 100.0, 1.5


def get_city_center(city_en: str) -> Tuple[float, float]:
    """Approximate GPS centre of each major city."""
    centers = {
        "Damascus": (33.5138, 36.2765),
        "Aleppo": (36.2021, 37.1343),
        "Homs": (34.7308, 36.7094),
        "Hama": (35.1333, 36.7500),
        "Latakia": (35.5317, 35.7881),
        "Tartus": (34.8920, 35.8868),
        "Sweida": (32.7089, 36.5667),
        "Deir Ezzor": (35.3359, 40.1408),
        "Raqqa": (35.9606, 39.0089),
        "Idlib": (35.9306, 36.6339),
        "Daraa": (32.6257, 36.1060),
        "Al-Hasakah": (36.5024, 40.7477),
        "Qamishli": (37.0590, 41.2280),
        "Palmyra": (34.5614, 38.2842),
        "Maaloula": (33.8443, 36.5456),
        "Bosra": (32.5175, 36.4810),
        "Al-Husn": (34.7560, 36.2950),
        "Seidnaya": (33.6960, 36.3770),
        "Safita": (34.8170, 36.1170),
        "Marmarita": (34.7670, 36.2330),
    }
    return centers.get(city_en, (33.5138, 36.2765))


# ---------------------------------------------------------------------------
# Interest → category mapping (used by the planner for fuzzy matching)
# ---------------------------------------------------------------------------
INTEREST_TO_CATEGORIES: Dict[str, List[str]] = {
    "history": ["history", "museum", "religious"],
    "food": ["food", "market"],
    "nature": ["nature", "mountain", "beach"],
    "shopping": ["shopping", "market"],
    "adventure": ["adventure", "mountain"],
    "art": ["art", "museum", "history"],
    "religious": ["religious", "history"],
    "beach": ["beach", "nature"],
    "mountain": ["mountain", "nature"],
    "market": ["market", "shopping", "food"],
    "museum": ["museum", "history", "art"],
    "hotel": ["hotel"],
    "wellness": ["wellness"],
    "neighbourhood": ["neighbourhood"],
}
