"""
Professional Syria Travel Planner for Offria
==============================================
DB-backed itinerary generation using the locations table + Gemini for
intelligent composition.

Features:
  • Multi-city route optimisation with realistic drive times
  • Interest-based filtering with fallback diversity
  • Clustering nearby places into logical day chunks
  • Automatic Arabic / German / English language selection
  • JSON output compatible with the existing frontend
"""

import json
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from google import genai
from google.genai import types

from app.core.config import settings
from app.core.gemini_client import get_genai_client
from app.services.location_service import (
    get_locations_in_city,
    get_locations_by_interest,
)
from app.data.city_distances import get_distance


genai_client = get_genai_client()


# ---------------------------------------------------------------------------
#  1. BUILD RICH CONTEXT
# ---------------------------------------------------------------------------

def build_context(db: Session, preferences: dict, start_city: str = "Damascus", days: int = 5) -> str:
    """
    Query the locations DB and build a compact, high-quality prompt context.
    Limits to ~20 places so Gemini answers quickly (<10 s) even via proxy.
    """
    interests = [i.strip().lower() for i in preferences.get("interests", "history,food").split(",")]
    max_places = 20

    scored: List[Tuple[int, Dict]] = []
    seen = set()

    def _add(place, score: int):
        key = f"{place.name_ar}|{place.city_ar}"
        if key in seen:
            return
        seen.add(key)

        # Truncate description to first sentence for compactness
        desc = place.description_ar or place.description_en or ""
        if desc:
            short = desc.split(".")[0] + "." if "." in desc else desc[:120]
        else:
            short = ""

        scored.append((score, {
            "name_ar": place.name_ar,
            "name_de": place.name_de,
            "name_en": place.name_en,
            "city_ar": place.city_ar,
            "city_en": place.city_en,
            "lat": place.lat,
            "lng": place.lng,
            "category": place.category,
            "description": short,
            "duration": place.visit_duration,
            "best_time": place.best_time,
        }))

    # 1) Start-city places get highest score
    for place in get_locations_in_city(db, start_city):
        _add(place, score=100)

    # 2) Interest-matching places
    for interest in interests:
        for place in get_locations_by_interest(db, interest):
            if place.city_en and place.city_en.lower() == start_city.lower():
                _add(place, score=90)
            else:
                km, _ = get_distance(start_city, place.city_ar or place.city_en or "")
                if km <= 0:
                    km = 999
                if km < 80:
                    _add(place, score=70)
                elif km < 150:
                    _add(place, score=50)
                else:
                    _add(place, score=30)

    # Sort by score descending, keep top N
    scored.sort(key=lambda x: x[0], reverse=True)
    selected = [item[1] for item in scored[:max_places]]

    if not selected:
        return ""

    # Compact distance matrix (only <=150 km)
    cities_involved = list({p["city_ar"] for p in selected})
    distances_text = ""
    for i, c1 in enumerate(cities_involved):
        for c2 in cities_involved[i + 1:]:
            km, hrs = get_distance(c1, c2)
            if 0 < km <= 150:
                distances_text += f"- {c1} ↔ {c2}: {km} km ({hrs}h drive)\n"

    places_json = json.dumps(selected, ensure_ascii=False, indent=2)

    context = f"""START CITY: {start_city}
TRIP DURATION: {days} days
INTERESTS: {', '.join(interests)}

REALISTIC DISTANCES (≤150 km):
{distances_text or 'All selected places are within one city region.'}

AUTHORISED PLACES (use ONLY these — do not invent):
{places_json}

ROUTING RULES:
1. Same-day cities must be <80 km apart (see distance table).
2. Cluster nearby places into single logical days.
3. Mix categories per day for a balanced experience.
4. Respect 'best_time' when scheduling (morning = museums/history, afternoon = nature/shopping, evening = dining/views).
5. NEVER invent places, prices, or coordinates not listed above.
6. If a place lacks coordinates, skip it — do not guess.
"""
    return context


# ---------------------------------------------------------------------------
#  2. GENERATE TRAVEL PLAN
# ---------------------------------------------------------------------------

def generate_travel_plan(db: Session, preferences: dict, days: int, lang: str = "ar") -> dict:
    """
    Generates a day-by-day itinerary using the Syria DB + Gemini.
    Returns dict: {"plan": [...], "route": [...]}
    """
    start_city = preferences.get("start_city", "Damascus")
    context = build_context(db, preferences, start_city, days)

    if not context:
        # Graceful fallback if DB is empty
        return {
            "plan": [{
                "day": 1,
                "activities": [{
                    "time": "09:00",
                    "title": "الجامع الأموي" if lang == "ar" else "Umayyad Mosque",
                    "location": start_city,
                    "lat": 33.5116,
                    "lng": 36.3064,
                    "description": "استكشف المدينة القديمة" if lang == "ar" else "Explore the Old City",
                }]
            }],
            "route": [{"day": 1, "city": start_city, "drive_from_previous": None, "overnight": True}],
        }

    # Language-specific instructions
    if lang == "ar":
        system_instruction = (
            "أنت مخطط سفر خبير متخصص في سوريا. "
            "اكتب خطة السفر **باللغة العربية الفصحى فقط**. "
            "لا تخلط بين العربية والإنجليزية أبداً."
        )
    elif lang == "de":
        system_instruction = (
            "Du bist ein erfahrener Syrien-Reiseplaner. "
            "Erstelle den Reiseplan **ausschließlich auf Deutsch**. "
            "Mische niemals Sprachen."
        )
    else:
        system_instruction = (
            "You are an expert Syria travel planner. "
            "Create the itinerary **in English only**. "
            "Never mix languages."
        )

    prompt = f"""{system_instruction}

You must plan a {days}-day trip starting in {start_city}.
User preferences: {json.dumps(preferences, ensure_ascii=False)}

---

{context}

---

OUTPUT FORMAT — respond ONLY with a valid JSON object matching this exact schema:
{{
  "plan": [
    {{
      "day": 1,
      "activities": [
        {{
          "time": "08:00",
          "title": "exact place name from database",
          "location": "city name",
          "lat": 33.5138,
          "lng": 36.2765,
          "description": "1–2 factual sentences about the place"
        }}
      ]
    }}
  ],
  "route": [
    {{"day": 1, "city": "Damascus", "drive_from_previous": null, "overnight": true}}
  ]
}}

SCHEDULING GUIDELINES:
• 08:00–12:00 → historical sites, museums, religious landmarks.
• 12:00–14:00 → lunch / food markets / local cuisine.
• 14:00–18:00 → nature, shopping districts, light walking.
• 18:00–21:00 → sunset viewpoints, dinner, cafés.
• Max 2 cities per day and ONLY if they are ≤50 km apart.
• Do NOT invent places, prices, or GPS coordinates.
• Every activity must use a place from the AUTHORISED PLACES list above.
"""

    config = types.GenerateContentConfig(
        system_instruction=prompt,
        temperature=0.15,
        response_mime_type="application/json",
    )

    response = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Plan a professional {days}-day Syria itinerary starting from {start_city}.",
        config=config,
    )
    raw = response.text.strip()

    # Strip markdown code fences
    if raw.startswith("```"):
        lines = raw.splitlines()
        if len(lines) > 2:
            raw = "\n".join(lines[1:-1])
        else:
            raw = raw.strip("`").strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {
            "plan": [{
                "day": 1,
                "activities": [{
                    "time": "09:00",
                    "title": "Umayyad Mosque" if lang != "ar" else "الجامع الأموي",
                    "location": start_city,
                    "lat": 33.5116,
                    "lng": 36.3064,
                    "description": "Explore the old city" if lang != "ar" else "استكشف المدينة القديمة",
                }]
            }],
            "route": [{"day": 1, "city": start_city, "drive_from_previous": None, "overnight": True}],
        }

    if "plan" not in data:
        data["plan"] = []
    if "route" not in data:
        data["route"] = []

    return data
