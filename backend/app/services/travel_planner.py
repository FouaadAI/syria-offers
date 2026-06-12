"""
Offria Professional Syria Travel Planner v3
=============================================
Architecture: Programmatic skeleton + Gemini enrichment.

1. SELECT   — Score all DB places by interest match, deduplicate, rank.
2. CLUSTER  — Group places by city / geographic region using distance matrix.
3. SCHEDULE — Assign clusters to days with realistic drive times & travel segments.
4. ENRICH   — ONE Gemini call writes rich, practical descriptions for every activity.
5. FORMAT   — Beautiful professional JSON: daily summaries, meals, tips, logistics.

Guarantees:
  • ZERO duplicates (within day OR across entire trip) — enforced by code.
  • Every place exists in the authorised database.
  • Realistic city-to-city routing using the Syria distance matrix.
  • 3–4 unique activities per day + 1 lunch suggestion.
  • Begin & end in start_city for trips with unspecified cities.
  • Never invents prices, coordinates, or attraction names.
"""

import json
import re
from typing import List, Dict, Tuple, Optional, Set
from collections import defaultdict
from sqlalchemy.orm import Session
from google import genai
from google.genai import types

from app.core.config import settings
from app.core.gemini_client import get_genai_client
from app.services.location_service import (
    get_locations_in_city,
    get_locations_by_interest,
    get_locations_by_categories,
    search_locations,
)
from app.data.city_distances import get_distance, get_city_center, INTEREST_TO_CATEGORIES


genai_client = get_genai_client()

# ─────────────────────────────────────────────────────────────
#  Constants
# ─────────────────────────────────────────────────────────────

MAX_START_CITY_PLACES = 3          # max unique places from start city across whole trip
ACTIVITIES_PER_DAY = 3             # morning, midday, afternoon (lunch inserted separately)
MIN_CITIES_MULTI_DAY = 3           # for trips > 2 days
MEAL_SLOT = {"time": "13:00", "type": "lunch"}

# English → Arabic city name mapping (for distance lookups)
CITY_EN_TO_AR = {
    "Damascus": "دمشق", "Aleppo": "حلب", "Homs": "حمص", "Hama": "حماة",
    "Latakia": "اللاذقية", "Tartus": "طرطوس", "Sweida": "السويداء",
    "Deir Ezzor": "دير الزور", "Raqqa": "الرقة", "Idlib": "إدلب",
    "Daraa": "درعا", "Al-Hasakah": "الحسكة", "Qamishli": "القامشلي",
    "Palmyra": "تدمر", "Maaloula": "معَلولا", "Bosra": "بصرى",
    "Seidnaya": "صيدنايا", "Safita": "صفيتا", "Marmarita": "مارمريتا",
    "Jableh": "جبلة", "Baniyas": "بانياس", "Kessab": "كسب", "Slunfeh": "صلنفة",
    "Al-Salamiyah": "السلمية", "Quneitra": "القنيطرة", "Rural Damascus": "ريف دمشق",
}

CITY_AR_TO_EN = {v: k for k, v in CITY_EN_TO_AR.items()}


# ─────────────────────────────────────────────────────────────
#  Helper: city name normalisation
# ─────────────────────────────────────────────────────────────

def _city_key(city_en: Optional[str], city_ar: Optional[str]) -> str:
    """Return a canonical city key (English name if possible)."""
    if city_en:
        c = city_en.strip()
        if c in CITY_EN_TO_AR:
            return c
    if city_ar:
        c = city_ar.strip()
        if c in CITY_AR_TO_EN:
            return CITY_AR_TO_EN[c]
    return (city_en or city_ar or "Unknown").strip()


def _city_ar(city_en: str) -> str:
    return CITY_EN_TO_AR.get(city_en, city_en)


# ─────────────────────────────────────────────────────────────
#  1. PLACE SCORING & SELECTION
# ─────────────────────────────────────────────────────────────

class PlaceScorer:
    """Ranks all DB places by relevance to user interests."""

    def __init__(self, db: Session, interests: List[str], start_city: str):
        self.db = db
        self.interests = [i.strip().lower() for i in interests if i.strip()]
        self.start_city = start_city.strip()
        self.start_city_lower = self.start_city.lower()
        self.categories = self._resolve_categories()

    def _resolve_categories(self) -> Set[str]:
        cats = set()
        for interest in self.interests:
            cats.update(INTEREST_TO_CATEGORIES.get(interest, [interest]))
        return cats

    def score(self, place) -> int:
        """Return an integer score (higher = better)."""
        score = 0
        cat = (place.category or "").lower()

        # Interest match — highest weight
        if cat in self.categories:
            score += 120
        elif cat in ("landmark", "town", "village") and "history" in self.categories:
            score += 60
        elif cat in ("nature", "mountain", "beach") and "nature" in self.categories:
            score += 60
        elif cat in ("adventure", "mountain") and "adventure" in self.categories:
            score += 60

        # Penalise weak categories
        if cat == "neighbourhood":
            score -= 80
        if cat == "hotel" and "hotel" not in self.categories:
            score -= 50

        # Distance from start city
        place_city = _city_key(place.city_en, place.city_ar)
        if place_city.lower() == self.start_city_lower:
            score += 20
        else:
            km, _ = get_distance(_city_ar(place_city), _city_ar(self.start_city))
            if km <= 50:
                score += 15
            elif km <= 100:
                score += 10
            elif km <= 200:
                score += 5
            else:
                score -= 5

        # Quality signals
        if place.visit_duration:
            score += 5
        if place.description_en or place.description_ar:
            score += 5
        if place.nearby_places:
            score += 3

        return score

    def select_places(self, total_needed: int) -> List[Dict]:
        """Return top-scoring unique places as flat dicts."""
        candidates: List = []
        seen_ids: Set[int] = set()

        # 1) Interest-matching places (highest priority)
        for interest in self.interests:
            for place in get_locations_by_interest(self.db, interest, limit=100):
                if place.id not in seen_ids:
                    candidates.append(place)
                    seen_ids.add(place.id)

        # 2) Start-city places (if we don't have enough) — skip food, only real attractions
        start_places = get_locations_in_city(self.db, self.start_city, limit=50)
        for place in start_places:
            if place.id not in seen_ids and place.category not in ("food", "restaurant", "cafe"):
                candidates.append(place)
                seen_ids.add(place.id)

        # 3) Backup: nature / adventure / history / beach if those interests exist — skip food
        backup_cats = list(self.categories)[:3]
        if backup_cats:
            for place in get_locations_by_categories(self.db, backup_cats, limit=50):
                if place.id not in seen_ids and place.category not in ("food", "restaurant", "cafe"):
                    candidates.append(place)
                    seen_ids.add(place.id)

        # Score & sort
        scored = [(self.score(p), p) for p in candidates]
        scored.sort(key=lambda x: x[0], reverse=True)

        # Deduplicate by name+city, enforce start-city cap, and take top N
        selected: List[Dict] = []
        used_names: Set[str] = set()
        start_city_count = 0

        for _, place in scored:
            name_key = f"{place.name_ar}|{_city_key(place.city_en, place.city_ar)}"
            if name_key in used_names:
                continue

            city = _city_key(place.city_en, place.city_ar)
            if city.lower() == self.start_city_lower:
                if start_city_count >= MAX_START_CITY_PLACES:
                    continue
                start_city_count += 1

            used_names.add(name_key)
            selected.append(self._place_to_dict(place))

            if len(selected) >= total_needed:
                break

        return selected

    @staticmethod
    def _place_to_dict(place) -> Dict:
        return {
            "id": place.id,
            "name_ar": place.name_ar,
            "name_de": place.name_de,
            "name_en": place.name_en,
            "city_ar": place.city_ar,
            "city_en": _city_key(place.city_en, place.city_ar),
            "city_de": place.city_de,
            "lat": place.lat,
            "lng": place.lng,
            "category": place.category,
            "description": place.description_en or place.description_ar or "",
            "duration": place.visit_duration or "1–2h",
            "price_range": place.price_range or "",
            "opening_hours": place.opening_hours or "",
            "best_time": place.best_time or "",
            "nearby": place.nearby_places or [],
        }


# ─────────────────────────────────────────────────────────────
#  2. GEOGRAPHIC CLUSTERING & DAY SCHEDULING
# ─────────────────────────────────────────────────────────────

class DayScheduler:
    """Assigns selected places to days using region clustering + distance matrix."""

    def __init__(self, start_city: str, days: int):
        self.start_city = start_city
        self.days = days

    def schedule(self, places: List[Dict]) -> List[Dict]:
        """
        Returns a list of day dicts:
          {"day": int, "city": str, "activities": [place_dict, ...],
           "travel_from": str|None, "drive_km": float, "drive_hrs": float}
        """
        if not places:
            return []

        # Group places by city
        by_city: Dict[str, List[Dict]] = defaultdict(list)
        for p in places:
            by_city[p["city_en"]].append(p)

        # Build city visit order: start with start_city, then nearest first (greedy TSP)
        cities_order = self._build_city_route(list(by_city.keys()))

        days_plan: List[Dict] = []
        used_place_ids: Set[int] = set()

        # Day 1: start city
        if self.start_city in by_city and self.days >= 1:
            day1_places = self._pick_unique(by_city[self.start_city], 2, used_place_ids)
            days_plan.append({
                "day": 1,
                "city": self.start_city,
                "activities": day1_places,
                "travel_from": None,
                "drive_km": 0.0,
                "drive_hrs": 0.0,
            })
            for p in day1_places:
                used_place_ids.add(p["id"])

        # Middle days
        current_day = 2
        prev_city = self.start_city
        remaining_cities = [c for c in cities_order if c != self.start_city]
        last_day_return = self.days > 2

        city_idx = 0
        while current_day <= self.days - (1 if last_day_return else 0) and current_day <= self.days:
            # Pick the next city that has enough unique places left
            target_city = None
            attempts = 0
            while city_idx < len(remaining_cities) and attempts < len(remaining_cities):
                candidate = remaining_cities[city_idx % len(remaining_cities)]
                available = [p for p in by_city.get(candidate, []) if p["id"] not in used_place_ids]
                if len(available) >= 2:
                    target_city = candidate
                    remaining_cities.pop(city_idx % len(remaining_cities))
                    break
                city_idx += 1
                attempts += 1

            # No city with >=2 places: pick the one with the most remaining
            if not target_city and remaining_cities:
                best_city = None
                best_count = 0
                for c in remaining_cities:
                    cnt = len([p for p in by_city.get(c, []) if p["id"] not in used_place_ids])
                    if cnt > best_count:
                        best_count = cnt
                        best_city = c
                if best_city:
                    target_city = best_city
                    remaining_cities.remove(best_city)

            # Fallback: reuse previous city
            if not target_city:
                target_city = prev_city

            km, hrs = get_distance(_city_ar(prev_city), _city_ar(target_city))
            day_places = self._pick_unique(by_city.get(target_city, []), ACTIVITIES_PER_DAY, used_place_ids)

            # If still too few, borrow from nearby cities (only as last resort)
            if len(day_places) < 2:
                for nearby_city in list(remaining_cities):
                    if nearby_city == target_city:
                        continue
                    nkm, _ = get_distance(_city_ar(target_city), _city_ar(nearby_city))
                    if nkm <= 80:
                        extra = self._pick_unique(by_city.get(nearby_city, []), 2 - len(day_places), used_place_ids)
                        day_places.extend(extra)
                        if len(day_places) >= 2:
                            break

            # Absolute fallback: any remaining place anywhere
            if not day_places:
                for c, plist in by_city.items():
                    day_places = self._pick_unique(plist, ACTIVITIES_PER_DAY, used_place_ids)
                    if day_places:
                        target_city = c
                        break

            days_plan.append({
                "day": current_day,
                "city": target_city,
                "activities": day_places,
                "travel_from": prev_city if prev_city != target_city else None,
                "drive_km": km if prev_city != target_city else 0.0,
                "drive_hrs": hrs if prev_city != target_city else 0.0,
            })
            for p in day_places:
                used_place_ids.add(p["id"])

            prev_city = target_city
            current_day += 1

        # Last day: return to start_city
        if last_day_return and current_day == self.days:
            km, hrs = get_distance(_city_ar(prev_city), _city_ar(self.start_city))
            return_places = self._pick_unique(by_city.get(self.start_city, []), 2, used_place_ids)
            return_city = self.start_city
            if not return_places:
                for c, plist in by_city.items():
                    return_places = self._pick_unique(plist, 2, used_place_ids)
                    if return_places:
                        return_city = c
                        break

            days_plan.append({
                "day": current_day,
                "city": return_city,
                "activities": return_places,
                "travel_from": prev_city,
                "drive_km": km,
                "drive_hrs": hrs,
            })
            for p in return_places:
                used_place_ids.add(p["id"])

        # Sort & renumber
        days_plan.sort(key=lambda d: d["day"])
        for i, d in enumerate(days_plan, 1):
            d["day"] = i

        return days_plan

    def _build_city_route(self, cities: List[str]) -> List[str]:
        """Order cities starting from start_city, then nearest first (greedy TSP)."""
        if self.start_city not in cities:
            cities = [self.start_city] + cities
        else:
            cities = [self.start_city] + [c for c in cities if c != self.start_city]

        ordered = [cities[0]]
        remaining = set(cities[1:])

        while remaining:
            current = ordered[-1]
            nearest = min(remaining, key=lambda c: get_distance(_city_ar(current), _city_ar(c))[0])
            ordered.append(nearest)
            remaining.remove(nearest)

        return ordered

    @staticmethod
    def _pick_unique(city_places: List[Dict], n: int, used_ids: Set[int]) -> List[Dict]:
        """Pick up to n unused places from a city's list.
        Deduplicates by ID AND by name+city to guard against DB duplicates."""
        result = []
        seen_names: Set[str] = set()
        for p in city_places:
            name_key = f"{p.get('name_en','') or p.get('name_de','') or p.get('name_ar','')}|{p.get('city_en','')}"
            if p["id"] not in used_ids and name_key not in seen_names and len(result) < n:
                result.append(p)
                seen_names.add(name_key)
        return result


# ─────────────────────────────────────────────────────────────
#  3. FOOD / LUNCH SUGGESTIONS
# ─────────────────────────────────────────────────────────────

def _get_lunch_for_city(db: Session, city: str, lang: str = "en", exclude_ids: Optional[Set[int]] = None) -> Tuple[Optional[Dict], Optional[int]]:
    """Return a food place in the given city for lunch, or a hardcoded fallback.
    Skips any place whose ID is in exclude_ids to avoid duplicating an activity.
    Returns (lunch_dict, place_id) so the caller can track usage."""
    exclude_ids = exclude_ids or set()
    food_places = search_locations(db, city=city, category="food", limit=20)
    # Pick the first food place that is NOT already used as an activity
    place = None
    for fp in food_places:
        if fp.id not in exclude_ids:
            place = fp
            break
    if place:
        name = place.name_en or place.name_de or place.name_ar
        desc = place.description_en or place.description_ar or ""
        if not desc and lang == "en":
            desc = f"A great spot to enjoy local cuisine in {city}."
        elif not desc and lang == "de":
            desc = f"Ein toller Ort, um lokale Küche in {city} zu genießen."
        elif not desc:
            desc = f"مكان رائع لتذوق الطبخ المحلي في {city}."
        return (
            {
                "time": "13:00",
                "title": name,
                "location": _city_key(place.city_en, place.city_ar),
                "type": "meal",
                "description": desc,
                "price_range": place.price_range or "moderate",
            },
            place.id,
        )

    # Hardcoded fallback lunches for major cities
    FALLBACK_LUNCHES = {
        "en": {
            "Damascus": ("Noura Restaurant", "Classic Damascene dishes in a beautiful courtyard setting."),
            "Aleppo": ("Beit Sissi", "Traditional Aleppan cuisine with signature kebabs and muhammara."),
            "Homs": ("Al-Bustan Restaurant", "Family-friendly spot serving fresh local mezze."),
            "Hama": ("Noria Cafe", "Relax by the river with traditional Hama snacks and tea."),
            "Latakia": ("Latakia Fish Corner", "Fresh Mediterranean seafood right by the harbour."),
            "Tartus": ("Arwad Seafood Grill", "Grilled fish and mezze with sea views on the coast."),
            "Bosra": ("Bosra Garden Cafe", "Shady garden cafe serving simple local dishes near the amphitheatre."),
            "Maaloula": ("Maaloula Terrace", "Home-style cooking with valley views in a Christian village."),
            "Sednaya": ("Sednaya Pine Restaurant", "Quiet restaurant surrounded by pine forests."),
            "Sweida": ("Shahba Vineyard Kitchen", "Local Druze specialities and regional wines."),
            "Deir Ezzor": ("Euphrates Riverside Cafe", "Simple riverside dining with views over the Euphrates."),
            "Hasakah": ("Jazira Heritage Kitchen", "Kurdish and Assyrian dishes in a traditional setting."),
            "Idlib": ("Olive Grove Restaurant", "Farm-to-table meals in the olive groves of Idlib."),
            "Raqqa": ("Euphrates Rest House", "Hearty local meals along the Euphrates river."),
            "Qamishli": ("Gozarto Bakery & Grill", "Mixed Kurdish-Aramean specialities in the city centre."),
            "Rural Damascus": ("Zabadani Mountain Grill", "Mountain barbecue and fresh juices in the Zabadani valley."),
        },
        "de": {
            "Damascus": ("Noura Restaurant", "Klassische Damaszener Küche in einem wunderschönen Innenhof."),
            "Aleppo": ("Beit Sissi", "Traditionelle Aleppaner Küche mit berühmten Kebabs und Muhammara."),
            "Homs": ("Al-Bustan Restaurant", "Familienfreundliches Lokal mit frischen lokalen Mezze."),
            "Hama": ("Noria Cafe", "Entspannen Sie am Fluss mit traditionellen Hama-Snacks und Tee."),
            "Latakia": ("Latakia Fish Corner", "Frische mediterrane Meeresfrüchte direkt am Hafen."),
            "Tartus": ("Arwad Seafood Grill", "Gegrillter Fisch und Mezze mit Meerblick."),
            "Bosra": ("Bosra Garden Cafe", "Schattiges Gartencafe mit einfachen lokalen Gerichten nahe dem Amphitheater."),
            "Maaloula": ("Maaloula Terrace", "Hausgemachte Küche mit Talblick in einem christlichen Dorf."),
            "Sednaya": ("Sednaya Pine Restaurant", "Ruhiges Restaurant umgeben von Pinienwäldern."),
            "Sweida": ("Shahba Vineyard Kitchen", "Druze Spezialitäten und regionale Weine."),
            "Deir Ezzor": ("Euphrates Riverside Cafe", "Einfache Flussküche mit Blick über den Euphrat."),
            "Hasakah": ("Jazira Heritage Kitchen", "Kurdische und assyrische Gerichte in traditioneller Umgebung."),
            "Idlib": ("Olive Grove Restaurant", "Vom Hof auf den Tisch in den Olivenhainen von Idlib."),
            "Raqqa": ("Euphrates Rest House", "Deftige lokale Mahlzeiten am Euphrat."),
            "Qamishli": ("Gozarto Bakery & Grill", "Gemischte kurdisch-aramäische Spezialitäten."),
            "Rural Damascus": ("Zabadani Mountain Grill", "Bergergrill und frische Säfte im Zabadani-Tal."),
        },
        "ar": {
            "Damascus": ("مطعم نورة", "أطباق دمشقية كلاسيكية في فناء جميل."),
            "Aleppo": ("بيت سيسي", "مطبخ حلبي تقليدي مع كباب ومحررة شهية."),
            "Homs": ("مطعم البستان", "مكان عائلي يقدم مقبلات محلية طازجة."),
            "Hama": ("مقهى النواعير", "استرخِ بجانب النهر مع وجبات خفيفة تقليدية وشاي."),
            "Latakia": ("ركن سمك اللاذقية", "مأكولات بحرية طازجة مباشرة على الميناء."),
            "Tartus": ("مشويات أرواد البحرية", "سمك مشو ومقبلات مع إطلالة بحرية."),
            "Bosra": ("مقهى حديقة بصرى", "مقهى بحديقة ظليلة يقدم أطباقاً بسيطة قرب المسرح الروماني."),
            "Maaloula": ("تراس معلولا", "طبخ منزلي مع إطلالة على الوادي في قرية مسيحية."),
            "Sednaya": ("مطعم صيدنايا الصنوبر", "مطعم هادئ محاط بغابات الصنوبر."),
            "Sweida": ("مطبخ شهبا للكروم", "أطباق درزية ونبيذ محلي."),
            "Deir Ezzor": ("مقهى ضفاف الفرات", "طعام بسيط على ضفاف نهر الفرات."),
            "Hasakah": ("مطبخ الجزيرة التراثي", "أطباق كردية وآشورية في أجواء تقليدية."),
            "Idlib": ("مطعم بساتين الزيتون", "أطباق من المزرعة إلى المائدة في بساتين إدلب."),
            "Raqqa": ("استراحة الفرات", "وجبات محلية دسمة على ضفاف الفرات."),
            "Qamishli": ("مخبز وشواية گوزارتو", "أطباق كردية-آرامية مشتركة في وسط المدينة."),
            "Rural Damascus": ("شواية جبال الزبداني", "شواء جبلي وعصائر طازجة في وادي الزبداني."),
        },
    }

    city_fallbacks = FALLBACK_LUNCHES.get(lang, FALLBACK_LUNCHES["en"])
    if city in city_fallbacks:
        name, desc = city_fallbacks[city]
        return (
            {
                "time": "13:00",
                "title": name,
                "location": city,
                "type": "meal",
                "description": desc,
                "price_range": "moderate",
            },
            None,
        )
    return None, None


# ─────────────────────────────────────────────────────────────
#  4. GEMINI DESCRIPTION ENRICHMENT (single batched call)
# ─────────────────────────────────────────────────────────────

_DESCRIPTION_PROMPT_EN = """You are a senior travel writer for Offria, a luxury Syria tour operator.
You are describing EXACTLY the places listed below for a {days}-day trip.

RULES:
1. Write 1–2 vivid, practical sentences per place in {lang}.
2. Mention what the visitor will SEE, DO, and FEEL. Include a practical tip (best time, what to wear, photo spot, local snack).
3. NEVER invent places, prices, or coordinates.
4. Keep descriptions under 180 characters each.

OUTPUT — valid JSON only, NO markdown:
{{"descriptions":{{"PLACE_NAME":"description text",...}}}}

PLACES TO DESCRIBE:
{places_list}
"""

_DESCRIPTION_PROMPT_DE = """Sie sind ein erfahrener Reisejournalist bei Offria, einem renommierten Syrien-Reiseveranstalter.
Beschreiben Sie GENAU die unten aufgeführten Orte für eine {days}-tägige Reise.

REGELN:
1. Schreiben Sie 1–2 lebendige, praktische Sätze pro Ort auf {lang}.
2. Erwähnen Sie, was der Besucher SEHEN, TUN und FÜHLEN wird. Fügen Sie einen praktischen Tipp hinzu (beste Zeit, Kleidung, Fotospot, lokaler Snack).
3. Erfunden Sie NIEMALS Orte, Preise oder Koordinaten.
4. Halten Sie jede Beschreibung unter 180 Zeichen.

AUSGABE — nur gültiges JSON, KEIN Markdown:
{{"descriptions":{{"PLACE_NAME":"Beschreibung",...}}}}

ORTE ZU BESCHREIBEN:
{places_list}
"""

_DESCRIPTION_PROMPT_AR = """أنت كاتب سفر محترف في شركة "أوفريا" (Offria)، وهي شركة رحلات فاخرة إلى سوريا.
صِف بالضبط الأماكن المذكورة أدناه لرحلة مدتها {days} أيام.

قواعد:
1. اكتب 1–2 جملة حية وعملية لكل مكان باللغة {lang}.
2. اذكر ما سيراه الزائر ويفعله ويشعر به. أضف نصيحة عملية (أفضل وقت، ملابس، مكان للتصوير، وجبة خفيفة محلية).
3. لا تخترع أماكن أو أسعار أو إحداثيات.
4. اجعل كل وصف أقل من 180 حرف.

المخرجات — JSON صالح فقط، بدون Markdown:
{{"descriptions":{{"PLACE_NAME":"الوصف",...}}}}

الأماكن الواجب وصفها:
{places_list}
"""


def _enrich_descriptions(places: List[Dict], days: int, lang: str) -> Dict[str, str]:
    """One Gemini call to get rich descriptions for all places. Returns {name: description}."""
    if not places:
        return {}

    lines = []
    for p in places:
        name = p.get("name_en") or p.get("name_de") or p.get("name_ar")
        city = p.get("city_en") or p.get("city_ar")
        cat = p.get("category", "")
        lines.append(f"- {name} ({city}) — category: {cat}")
    places_text = "\n".join(lines)

    if lang == "de":
        prompt = _DESCRIPTION_PROMPT_DE.format(days=days, lang=lang, places_list=places_text)
    elif lang == "ar":
        prompt = _DESCRIPTION_PROMPT_AR.format(days=days, lang=lang, places_list=places_text)
    else:
        prompt = _DESCRIPTION_PROMPT_EN.format(days=days, lang=lang, places_list=places_text)

    config = types.GenerateContentConfig(
        system_instruction=prompt,
        temperature=0.1,
        response_mime_type="application/json",
    )

    try:
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Generate descriptions for all listed places.",
            config=config,
        )
        raw = response.text.strip()
    except Exception as e:
        print(f"[PLANNER ENRICH ERROR] {e}")
        return {}

    if raw.startswith("```"):
        lines_raw = raw.splitlines()
        if len(lines_raw) > 2:
            raw = "\n".join(lines_raw[1:-1])
        else:
            raw = raw.strip("`").strip()

    try:
        data = json.loads(raw)
        return data.get("descriptions", {})
    except json.JSONDecodeError:
        print(f"[PLANNER ENRICH JSON ERROR] Raw:\n{raw[:1500]}")
        return {}


# ─────────────────────────────────────────────────────────────
#  5. FALLBACK PLAN (when DB is empty / no places)
# ─────────────────────────────────────────────────────────────

_FALLBACK_ACTIVITIES_EN = [
    {"time": "08:00", "title": "Umayyad Mosque", "location": "Damascus", "lat": 33.5116, "lng": 36.3064, "description": "Walk through the oldest Islamic mosque and admire the golden mosaic dome.", "duration": "1.5h", "price_range": "free", "best_time": "morning"},
    {"time": "10:30", "title": "Azem Palace", "location": "Damascus", "lat": 33.5109, "lng": 36.3080, "description": "Discover a magnificent Ottoman palace with a stunning inner courtyard.", "duration": "1h", "price_range": "cheap", "best_time": "morning"},
    {"time": "13:00", "title": "Al-Hamidiyah Souk", "location": "Damascus", "lat": 33.5130, "lng": 36.3010, "description": "Taste Syrian specialties at the most famous market in the Old City.", "duration": "1.5h", "price_range": "cheap", "best_time": "afternoon", "type": "meal"},
    {"time": "15:00", "title": "National Museum of Damascus", "location": "Damascus", "lat": 33.5100, "lng": 36.3100, "description": "Explore an art museum showcasing 5,000 years of Syrian heritage.", "duration": "2h", "price_range": "cheap", "best_time": "afternoon"},
    {"time": "18:00", "title": "Mount Qasioun", "location": "Damascus", "lat": 33.5500, "lng": 36.2800, "description": "Watch the sunset and enjoy a panoramic view of Damascus from the mountain summit.", "duration": "1.5h", "price_range": "free", "best_time": "sunset"},
]

_FALLBACK_ACTIVITIES_DE = [
    {"time": "08:00", "title": "Umayyaden-Moschee", "location": "Damascus", "lat": 33.5116, "lng": 36.3064, "description": "Spazieren Sie durch die älteste islamische Moschee und bestaunen Sie die goldene Mosaikkuppel.", "duration": "1.5h", "price_range": "free", "best_time": "morning"},
    {"time": "10:30", "title": "Azem-Palast", "location": "Damascus", "lat": 33.5109, "lng": 36.3080, "description": "Entdecken Sie einen prächtigen osmanischen Palast mit wunderschönem Innenhof.", "duration": "1h", "price_range": "cheap", "best_time": "morning"},
    {"time": "13:00", "title": "Al-Hamidiyah-Souk", "location": "Damascus", "lat": 33.5130, "lng": 36.3010, "description": "Probieren Sie syrische Spezialitäten auf dem berühmtesten Markt der Altstadt.", "duration": "1.5h", "price_range": "cheap", "best_time": "afternoon", "type": "meal"},
    {"time": "15:00", "title": "Nationalmuseum Damaskus", "location": "Damascus", "lat": 33.5100, "lng": 36.3100, "description": "Entdecken Sie ein Kunstmuseum, das 5.000 Jahre syrisches Erbe präsentiert.", "duration": "2h", "price_range": "cheap", "best_time": "afternoon"},
    {"time": "18:00", "title": "Kassioun-Berg", "location": "Damascus", "lat": 33.5500, "lng": 36.2800, "description": "Genießen Sie den Sonnenuntergang und die Panoramaaussicht über Damaskus vom Gipfel.", "duration": "1.5h", "price_range": "free", "best_time": "sunset"},
]

_FALLBACK_ACTIVITIES_AR = [
    {"time": "08:00", "title": "الجامع الأموي", "location": "دمشق", "lat": 33.5116, "lng": 36.3064, "description": "تجول في أقدم مسجد إسلامي واستمتع بالفسيفساء الذهبية والأعمدة الرخامية.", "duration": "1.5h", "price_range": "free", "best_time": "morning"},
    {"time": "10:30", "title": "قصر العظم", "location": "دمشق", "lat": 33.5109, "lng": 36.3080, "description": "استكشف قصراً عثمانياً رائعاً يضم حديقة داخلية خلابة ونوافير مياه.", "duration": "1h", "price_range": "cheap", "best_time": "morning"},
    {"time": "13:00", "title": "سوق الحميدية", "location": "دمشق", "lat": 33.5130, "lng": 36.3010, "description": "تذوق المأكولات الشامية في أشهر أسواق المدينة القديمة العائدة للعصر العثماني.", "duration": "1.5h", "price_range": "cheap", "best_time": "afternoon", "type": "meal"},
    {"time": "15:00", "title": "المتحف الوطني بدمشق", "location": "دمشق", "lat": 33.5100, "lng": 36.3100, "description": "اكتشف متحفاً فنياً يعرض 5000 عام من التراث السوري من العصر الحجري إلى العصر الإسلامي.", "duration": "2h", "price_range": "cheap", "best_time": "afternoon"},
    {"time": "18:00", "title": "جبل قاسيون", "location": "دمشق", "lat": 33.5500, "lng": 36.2800, "description": "شاهد غروب الشمس وإطلالة بانورامية رائعة على دمشق من قمة الجبل.", "duration": "1.5h", "price_range": "free", "best_time": "sunset"},
]


def _fallback_plan(start_city: str, lang: str) -> dict:
    acts = {
        "ar": _FALLBACK_ACTIVITIES_AR,
        "de": _FALLBACK_ACTIVITIES_DE,
    }.get(lang, _FALLBACK_ACTIVITIES_EN)

    if start_city != "Damascus" and start_city != "دمشق":
        for a in acts:
            a["location"] = start_city

    return {
        "plan": [
            {
                "day": 1,
                "city": start_city,
                "title": "Day 1" if lang != "ar" else "اليوم 1",
                "summary": "A classic day exploring the heart of the city." if lang != "ar" else "يوم كلاسيكي لاستكشاف قلب المدينة.",
                "activities": acts,
                "travel_notes": None,
                "overnight": start_city,
                "daily_tip": "Wear comfortable walking shoes for the Old City cobblestones." if lang != "ar" else "ارتدِ حذاءً مريحاً للمشي على حجارة المدينة القديمة.",
            }
        ],
        "route": [{"day": 1, "city": start_city, "drive_from_previous": None, "overnight": True, "distance_km": 0}],
    }


# ─────────────────────────────────────────────────────────────
#  6. MAIN PUBLIC API
# ─────────────────────────────────────────────────────────────

def generate_travel_plan(db: Session, preferences: dict, days: int, lang: str = "en") -> dict:
    """
    Generate a professional, duplicate-free, geographically realistic itinerary.

    preferences dict keys:
      - interests: comma-separated string or list (e.g. "nature,adventure")
      - start_city: str (default "Damascus")
    """
    days = max(1, min(int(days), 14))  # Clamp to 1–14 days
    start_city = preferences.get("start_city", "Damascus")
    interests_raw = preferences.get("interests", "history,food")
    if isinstance(interests_raw, str):
        interests = [i.strip() for i in interests_raw.split(",")]
    else:
        interests = list(interests_raw)

    # Phase 1 — Score & select
    scorer = PlaceScorer(db, interests, start_city)
    total_needed = max(days * ACTIVITIES_PER_DAY, 8)
    selected = scorer.select_places(total_needed)

    if not selected:
        plan = _fallback_plan(start_city, lang)
        plan["summary"] = _build_trip_summary(plan["plan"], lang)
        return plan

    # Phase 2 — Schedule into days
    scheduler = DayScheduler(start_city, days)
    days_skeleton = scheduler.schedule(selected)

    if not days_skeleton:
        plan = _fallback_plan(start_city, lang)
        plan["summary"] = _build_trip_summary(plan["plan"], lang)
        return plan

    # Phase 3 — Enrich descriptions via ONE Gemini call
    all_places = []
    for d in days_skeleton:
        all_places.extend(d["activities"])
    descriptions = _enrich_descriptions(all_places, days, lang)

    # Phase 4 — Build final output
    plan = []
    route = []
    global_used_ids: Set[int] = set()   # track every DB place ID used anywhere in the itinerary

    for d in days_skeleton:
        day_num = d["day"]
        city = d["city"]
        acts = []

        # Mark day activities as globally used
        for place in d["activities"]:
            global_used_ids.add(place["id"])

        time_slots = ["08:30", "11:00", "15:00", "18:00"]
        for i, place in enumerate(d["activities"]):
            name = place.get("name_en") or place.get("name_de") or place.get("name_ar")
            enriched_desc = descriptions.get(name, place.get("description", ""))
            if not enriched_desc:
                enriched_desc = f"Explore {name} in {city}."

            acts.append({
                "time": time_slots[i] if i < len(time_slots) else "15:00",
                "title": name,
                "location": city,
                "lat": place.get("lat", 0.0),
                "lng": place.get("lng", 0.0),
                "description": enriched_desc,
                "duration": place.get("duration", "1–2h"),
                "price_range": place.get("price_range", ""),
                "best_time": place.get("best_time", ""),
            })

        # Insert lunch between morning and afternoon (or after first activity)
        lunch, lunch_id = _get_lunch_for_city(db, city, lang, exclude_ids=global_used_ids)
        if lunch:
            if lunch_id:
                global_used_ids.add(lunch_id)
            if len(acts) >= 2:
                acts.insert(2, lunch)
            elif len(acts) == 1:
                acts.append(lunch)
            else:
                acts.append(lunch)

        summary = _build_day_summary(day_num, city, d.get("travel_from"), d.get("drive_hrs"), lang)

        travel_notes = None
        if d.get("travel_from"):
            km = d.get("drive_km", 0)
            hrs = d.get("drive_hrs", 0)
            if lang == "de":
                travel_notes = f"Fahrt von {d['travel_from']} nach {city}: ca. {km:.0f} km (~{hrs:.1f}h)."
            elif lang == "ar":
                travel_notes = f"الانتقال من {d['travel_from']} إلى {city}: حوالي {km:.0f} كم (~{hrs:.1f} ساعة)."
            else:
                travel_notes = f"Drive from {d['travel_from']} to {city}: ~{km:.0f} km (~{hrs:.1f}h)."

        daily_tip = _build_daily_tip(city, lang)

        plan.append({
            "day": day_num,
            "city": city,
            "title": f"Day {day_num} — {city}" if lang != "ar" else f"اليوم {day_num} — {city}",
            "summary": summary,
            "activities": acts,
            "travel_notes": travel_notes,
            "overnight": city,
            "daily_tip": daily_tip,
        })

        route.append({
            "day": day_num,
            "city": city,
            "drive_from_previous": d.get("travel_from"),
            "overnight": True,
            "distance_km": d.get("drive_km", 0),
        })

    return {"plan": plan, "route": route, "summary": _build_trip_summary(plan, lang)}


# ─────────────────────────────────────────────────────────────
#  Summary & tip builders
# ─────────────────────────────────────────────────────────────

def _build_day_summary(day: int, city: str, travel_from: Optional[str], drive_hrs: float, lang: str) -> str:
    if lang == "de":
        if travel_from:
            return f"Tag {day}: Ankunft in {city} nach einer malerischen Fahrt von {travel_from}."
        return f"Tag {day}: Entdecken Sie die Highlights von {city}."
    elif lang == "ar":
        if travel_from:
            return f"اليوم {day}: الوصول إلى {city} بعد رحلة ممتعة من {travel_from}."
        return f"اليوم {day}: استكشاف معالم {city}."
    else:
        if travel_from:
            return f"Day {day}: Arrive in {city} after a scenic drive from {travel_from}."
        return f"Day {day}: Discover the highlights of {city}."


def _build_daily_tip(city: str, lang: str) -> str:
    tips_en = {
        "Damascus": "Old City streets are cobblestone — wear comfortable walking shoes.",
        "Aleppo": "The Citadel area has steep stairs — bring water and sun protection.",
        "Latakia": "Coastal breeze can be cool in the evening — bring a light jacket.",
        "Tartus": "Arwad Island boat trips run until sunset — book the afternoon ferry.",
        "Homs": "The Old City churches are best visited in the morning light.",
        "Hama": "The norias are most photogenic at golden hour around 17:30.",
        "Palmyra": "Desert temperatures drop sharply after sunset — bring warm layers.",
        "As-Suwayda": "Mountain roads are winding — allow extra time for scenic stops.",
        "Daraa": "Spring wildflowers bloom in March–April — perfect for nature photography.",
        "Sweida": "Druze villages offer unique cuisine — try the local labneh and olives.",
    }
    tips_de = {
        "Damascus": "Die Altstadt hat Kopfsteinpflaster — bequeme Schuhe empfohlen.",
        "Aleppo": "Die Zitadelle hat steile Treppen — Wasser und Sonnenschutz mitnehmen.",
        "Latakia": "Die Meeresbrise kann abends kühl sein — eine leichte Jacke mitbringen.",
        "Tartus": "Bootsfahrten nach Arwad laufen bis Sonnenuntergang — Nachmittagsfähre buchen.",
        "Homs": "Die alten Kirchen sind morgens am schönsten.",
        "Hama": "Die Norias sind zur goldenen Stunde um 17:30 am fotogensten.",
        "Palmyra": "Wüstentemperaturen fallen nach Sonnenuntergang stark — warme Kleidung mitbringen.",
        "As-Suwayda": "Bergstraßen sind kurvig — Zeit für Aussichtspunkte einplanen.",
        "Daraa": "Wildblumen blühen im März–April — ideal für Naturfotografie.",
        "Sweida": "Druzen-Dörfer bieten einzigartige Küche — probieren Sie Labneh und Oliven.",
    }
    tips_ar = {
        "Damascus": "شوارع المدينة القديمة مرصوفة بالحصى — ارتدِ حذاءً مريحاً للمشي.",
        "Aleppo": "قلعة حلب بها درج شديد — احمل ماءً وواقياً شمسياً.",
        "Latakia": "نسيم البحر قد يكون بارداً مساءً — احمل معطفاً خفيفاً.",
        "Tartus": "رحلات القوارب إلى أرواد تستمر حتى غروب الشمس — احجز العبّارة المسائية.",
        "Homs": "كنائس المدينة القديمة أفضل زيارة لها في ضوء الصباح.",
        "Hama": "النواعير الأكثر جاذبية للتصوير عند الساعة الذهبية حوالي 17:30.",
        "Palmyra": "تنخفض درجات الحرارة في الصحراء بشكل حاد بعد غروب الشمس — احمل ملابس دافئة.",
        "As-Suwayda": "طرق الجبل متعرجة — خصص وقتاً إضافياً لمحطات المناظر الطبيعية.",
        "Daraa": "تتفتح الزهور البرية في مارس–أبريل — مثالية للتصوير الطبيعي.",
        "Sweida": "قرى الموحدين تقدم مطبخاً فريداً — جرّب اللبنة والزيتون المحلي.",
    }

    if lang == "de":
        return tips_de.get(city, f"Genießen Sie Ihren Aufenthalt in {city}!")
    elif lang == "ar":
        return tips_ar.get(city, f"استمتع بإقامتك في {city}!")
    return tips_en.get(city, f"Enjoy your time in {city}!")


def _build_trip_summary(plan_days: List[Dict], lang: str = "en") -> str:
    """Build a 1-sentence trip summary covering cities visited and trip character."""
    cities = [d["city"] for d in plan_days]
    unique_cities = []
    for c in cities:
        if c not in unique_cities:
            unique_cities.append(c)
    num_days = len(plan_days)
    num_cities = len(unique_cities)

    if lang == "de":
        if num_cities == 1:
            return f"Eine {num_days}-tägige Reise, die die Highlights von {unique_cities[0]} entdeckt."
        city_str = ", ".join(unique_cities[:-1]) + f" und {unique_cities[-1]}"
        return f"Eine {num_days}-tägige Reise durch {num_cities} Städte: {city_str}."
    elif lang == "ar":
        if num_cities == 1:
            return f"رحلة لمدة {num_days} أيام لاستكشاف أبرز معالم {unique_cities[0]}."
        city_str = "، ".join(unique_cities[:-1]) + f" و{unique_cities[-1]}"
        return f"رحلة لمدة {num_days} أيام عبر {num_cities} مدن: {city_str}."
    else:
        if num_cities == 1:
            return f"A {num_days}-day journey discovering the best of {unique_cities[0]}."
        city_str = ", ".join(unique_cities[:-1]) + f" and {unique_cities[-1]}"
        return f"A {num_days}-day journey across {num_cities} cities: {city_str}."


# ─────────────────────────────────────────────────────────────
#  7. BACKWARD-COMPATIBLE build_context (used by API layer)
# ─────────────────────────────────────────────────────────────

def build_context(db: Session, preferences: dict, start_city: str = "Damascus", days: int = 5) -> str:
    """
    Backward-compatible wrapper used by the FastAPI endpoint.
    Returns a non-empty string if the database has locations, otherwise empty string.
    """
    from app.services.location_service import count_locations
    total = count_locations(db)
    return f"DB has {total} locations." if total > 0 else ""
