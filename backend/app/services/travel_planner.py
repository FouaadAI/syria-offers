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
    Builds a compact, high-quality prompt context.
    Limits to ~15 places so Gemini answers quickly (< 10 s) even via proxy.
    """
    interests = [i.strip().lower() for i in preferences.get("interests", "history,food").split(",")]
    max_places = 15

    # --- 1. Collect places, prioritise start-city, then nearby cities ---
    scored: List[Tuple[int, dict]] = []
    seen = set()

    def _add_place(p, score: int):
        if p.name_en in seen:
            return
        seen.add(p.name_en)
        # truncate description to first sentence to keep prompt small
        for desc in (p.description_en, p.description_de, p.description_ar):
            if desc:
                short = desc.split(".")[0] + "."
                break
        else:
            short = ""
        scored.append((score, {
            "name_ar": p.name_ar,
            "name_de": p.name_de,
            "name_en": p.name_en,
            "city_ar": p.city_ar,
            "city_en": p.city_en,
            "lat": p.lat,
            "lng": p.lng,
            "category": p.category,
            "description": short,
            "duration": p.visit_duration,
            "best_time": p.best_time,
        }))

    # Start-city places get highest score
    for p in places_in_city(start_city):
        _add_place(p, score=100)

    # Interest-matching places (score by relevance)
    for interest in interests:
        for p in places_by_interest(interest):
            # bonus if in start city, otherwise base score by distance tier
            if p.city_en == start_city or p.city_ar == start_city:
                _add_place(p, score=90)
            else:
                km, _ = get_distance(start_city, p.city_ar)
                if km <= 0:
                    km = 999
                if km < 80:
                    _add_place(p, score=70)
                elif km < 150:
                    _add_place(p, score=50)
                else:
                    _add_place(p, score=30)

    # Sort by score descending, keep top N
    scored.sort(key=lambda x: x[0], reverse=True)
    selected = [item[1] for item in scored[:max_places]]

    # --- 2. Compact distance matrix (only <= 150 km) ---
    cities_involved = list({p["city_ar"] for p in selected})
    distances_text = ""
    for i, c1 in enumerate(cities_involved):
        for c2 in cities_involved[i + 1:]:
            km, hrs = get_distance(c1, c2)
            if 0 < km <= 150:
                distances_text += f"- {c1} ↔ {c2}: {km} km ({hrs}h)\n"

    places_json = json.dumps(selected, ensure_ascii=False, indent=2)

    context = f"""
Start city: {start_city}
Interests: {', '.join(interests)}
Days: {days}

Distances (only <=150 km shown):
{distances_text or 'All places in one city.'}

Places (use ONLY these — max {max_places}):
{places_json}

Rules:
1. Same-day cities must be <80 km apart.
2. Cluster nearby places into single days.
3. Mix categories per day.
4. Respect 'best_time' when scheduling.
5. NEVER invent places not in the list above.
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
