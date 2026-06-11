"""
Professional Syria Travel Planner for Offria
==============================================
Uses the built-in Syria locations database instead of scraping the PostgreSQL
offers table (which may be empty).

Features:
  - Multi-city route optimisation (respects realistic drive times)
  - Interest-based filtering with fallback diversity
  - Clustering nearby places into logical day chunks
  - Automatic Arabic / German / English language selection
  - JSON output compatible with the existing frontend
"""

import json
from typing import List, Dict, Optional, Tuple
from google import genai
from google.genai import types
from app.core.config import settings
from app.core.gemini_client import get_genai_client
from app.data.syria_locations import (
    PLACES,
    places_by_interest,
    places_in_city,
    get_distance,
    get_city_center,
)


genai_client = get_genai_client()


# ---------------------------------------------------------------------------
#  1. BUILD RICH CONTEXT  (replaces old build_context)
# ---------------------------------------------------------------------------

def build_context(preferences: dict, start_city: str = "Damascus", days: int = 5) -> str:
    """
    Creates a detailed, structured prompt block containing:
      - Selected places matching user interests
      - Real distances / drive times between cities
      - Nearby clustering hints
    """
    interests = [i.strip().lower() for i in preferences.get("interests", "history,food").split(",")]

    # collect matching places
    selected: List[dict] = []
    for interest in interests:
        for p in places_by_interest(interest):
            selected.append({
                "name_ar": p.name_ar,
                "name_de": p.name_de,
                "name_en": p.name_en,
                "city_en": p.city_en,
                "city_ar": p.city_ar,
                "lat": p.lat,
                "lng": p.lng,
                "category": p.category,
                "description_ar": p.description_ar,
                "description_de": p.description_de,
                "description_en": p.description_en,
                "duration": p.visit_duration,
                "price": p.price_range,
                "opening": p.opening_hours,
                "best_time": p.best_time,
                "nearby": p.nearby_places,
            })

    # deduplicate
    seen = set()
    uniq = []
    for s in selected:
        key = s["name_en"]
        if key not in seen:
            seen.add(key)
            uniq.append(s)
    selected = uniq

    # if too few, add diversity places from start city
    if len(selected) < days * 3:
        for p in places_in_city(start_city):
            key = p.name_en
            if key not in seen:
                seen.add(key)
                selected.append({
                    "name_ar": p.name_ar,
                    "name_de": p.name_de,
                    "name_en": p.name_en,
                    "city_en": p.city_en,
                    "city_ar": p.city_ar,
                    "lat": p.lat,
                    "lng": p.lng,
                    "category": p.category,
                    "description_ar": p.description_ar,
                    "description_de": p.description_de,
                    "description_en": p.description_en,
                    "duration": p.visit_duration,
                    "price": p.price_range,
                    "opening": p.opening_hours,
                    "best_time": p.best_time,
                    "nearby": p.nearby_places,
                })

    # build distance matrix for cities involved
    cities_involved = list({p["city_ar"] for p in selected})
    distances_text = ""
    for i, c1 in enumerate(cities_involved):
        for c2 in cities_involved[i + 1:]:
            km, hrs = get_distance(c1, c2)
            if km > 0:
                distances_text += f"- {c1} ↔ {c2}: {km} km, ca. {hrs} Std. Fahrt\n"

    # format places as JSON-safe text
    places_json = json.dumps(selected, ensure_ascii=False, indent=2)

    context = f"""
=== START CITY ===
{start_city}

=== USER INTERESTS ===
{', '.join(interests)}

=== PLANNED DAYS ===
{days}

=== DISTANCES BETWEEN CITIES ===
{distances_text or '(All places in one city)'}

=== AVAILABLE PLACES (with GPS, category, duration, best time) ===
{places_json}

=== IMPORTANT RULES ===
1. Respect realistic drive times between cities. Do NOT schedule 2 cities on the same day if they are >80 km apart.
2. Cluster nearby places (same city or <5 km) into one day.
3. Mix categories: history, food, nature, shopping, religious per day when possible.
4. Respect 'best_time' (morning/evening/sunset) when scheduling.
5. Use ONLY the places listed above — no fictional locations.
6. Each activity MUST include lat, lng, and a real location name from the list.
"""
    return context


# ---------------------------------------------------------------------------
#  2. GENERATE TRAVEL PLAN  (replaces old generate_travel_plan)
# ---------------------------------------------------------------------------

def generate_travel_plan(preferences: dict, days: int, lang: str = "ar") -> dict:
    """
    Generates a day-by-day itinerary using the Syria database + Gemini for intelligent composition.
    Returns dict: {"plan": [...], "route": [...]}
    """
    if lang == "ar":
        instruction = "اكتب خطة السفر **باللغة العربية فقط**."
        desc_field = "description_ar"
        name_field = "name_ar"
        city_field = "city_ar"
    elif lang == "de":
        instruction = "Erstelle den Reiseplan **ausschließlich auf Deutsch**."
        desc_field = "description_de"
        name_field = "name_de"
        city_field = "city_de"
    else:
        instruction = "Create the itinerary **in English only**."
        desc_field = "description_en"
        name_field = "name_en"
        city_field = "city_en"

    start_city = preferences.get("start_city", "Damascus")
    context = build_context(preferences, start_city, days)

    system_prompt = f"""
{instruction}

You are an expert Syria travel planner. Compose a {days}-day itinerary for a trip starting in {start_city}.

User preferences: {json.dumps(preferences, ensure_ascii=False)}

Use ONLY the places provided in the context below. Each activity must include:
  - time: HH:MM
  - title: exact name from the database
  - location: city name
  - lat / lng: real coordinates from the database
  - description: 1-2 sentences about the place

Rules:
  - Morning activities (08:00-12:00): museums, religious sites, historical landmarks.
  - Lunch (12:00-14:00): food / market places.
  - Afternoon (14:00-18:00): nature, shopping, markets, light walking.
  - Evening (18:00-21:00): sunset viewpoints, dinner, cafes.
  - Max 2 cities per day, and only if they are close (<50 km).
  - Do NOT invent places not in the database.

Respond ONLY with a valid JSON object in this exact format:
{{
  "plan": [
    {{
      "day": 1,
      "activities": [
        {{
          "time": "08:00",
          "title": "...",
          "location": "...",
          "lat": 33.5138,
          "lng": 36.2765,
          "description": "..."
        }}
      ]
    }}
  ],
  "route": [
    {{"day": 1, "city": "Damascus", "drive_from_previous": null, "overnight": true}}
  ]
}}

Context:
{context}
"""

    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.2,
    )
    response = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Plan a {days}-day Syria trip starting from {start_city}.",
        config=config,
    )
    raw = response.text.strip()

    # strip markdown code block if present
    if raw.startswith("```"):
        lines = raw.splitlines()
        # remove first and last line (```json / ```)
        if len(lines) > 2:
            raw = "\n".join(lines[1:-1])
        else:
            raw = raw.strip("`").strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # fallback: wrap in a simple plan
        data = {
            "plan": [
                {
                    "day": 1,
                    "activities": [
                        {
                            "time": "09:00",
                            "title": "Umayyad Mosque" if lang != "ar" else "الجامع الأموي",
                            "location": start_city,
                            "lat": 33.5116,
                            "lng": 36.3064,
                            "description": "Explore the old city" if lang != "ar" else "استكشف المدينة القديمة",
                        }
                    ],
                }
            ],
            "route": [{"day": 1, "city": start_city, "drive_from_previous": None, "overnight": True}],
        }

    # ensure top-level keys exist
    if "plan" not in data:
        data["plan"] = []
    if "route" not in data:
        data["route"] = []

    return data


# ---------------------------------------------------------------------------
#  3. FALLBACK PROMPT  (for manual expansion by an AI researcher)
# ---------------------------------------------------------------------------

RESEARCH_PROMPT = """
=== MISSION ===
You are a world-class Syria tourism researcher. Expand the Offria travel app database with
verified, high-quality data for EVERY city, village, neighbourhood, and tourist site in Syria.

=== OUTPUT FORMAT ===
For each location, provide a JSON object:
{{
  "name_ar": "الاسم بالعربية",
  "name_de": "Name auf Deutsch",
  "name_en": "Name in English",
  "city_ar": "المدينة بالعربية",
  "city_de": "Stadt auf Deutsch",
  "city_en": "City in English",
  "lat": 33.5138,
  "lng": 36.2765,
  "category": "history",
  "description_ar": "وصف بالعربية",
  "description_de": "Beschreibung auf Deutsch",
  "description_en": "Description in English",
  "visit_duration": "1h",
  "price_range": "free",
  "opening_hours": "08:00-18:00",
  "best_time": "morning",
  "wheelchair": "partial",
  "family_friendly": true,
  "age_group": "all",
  "nearby_places": ["مكان قريب 1", "مكان قريب 2"]
}}

=== CATEGORIES ===
history | food | nature | shopping | adventure | art | religious | beach | mountain | market | museum | hotel | wellness

=== PRIORITY LIST (expand these first) ===
1. Damascus neighbourhoods: Salhieh, Malki, Baramkeh, Masaken Barzeh, Mazzeh, Abu Rummaneh, Rukn al-Din, Al-Qanawat
2. Aleppo neighbourhoods: Al-Jdayde, Azazieh, Saadallah Al-Jabri, Al-Sabil
3. Coastal villages: Slunfeh, Kessab, Kasab, Al-Samra, Banias
4. Desert sites: Resafa, Halabiya, Zenobia, Qasr Ibn Wardan
5. Druze villages: Ain al-Tineh, Al-Qrayya, Salkhad
6. Euphrates sites: Mari, Dura Europos, Halabiya
7. Every museum in every governorate
8. Every famous restaurant (with cuisine type)
9. Hotels and guesthouses (with price range and stars)
10. Wellness / spa / hammam locations

=== QUALITY RULES ===
- GPS coordinates must be accurate within 100 meters.
- Descriptions must be 2-3 sentences, factual, not promotional.
- nearby_places must be real places within 5 km walking distance.
- Do NOT invent information you are unsure about.
- Mark uncertain fields with "???" so a human can verify.
"""
