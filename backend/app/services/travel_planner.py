import json
from sqlalchemy.orm import Session
from google import genai
from google.genai import types
from app.core.config import settings
from app.models.offer import Offer

genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)

def build_context(db: Session) -> str:
    offers = db.query(Offer).filter(
        Offer.is_active == True,
        Offer.approved == True,
        Offer.latitude.isnot(None),
        Offer.longitude.isnot(None)
    ).all()

    lines = []
    for offer in offers:
        cat_name = offer.category.name_ar if offer.category else "Allgemein"
        lines.append(
            f"- {offer.title_ar} (Kategorie: {cat_name}): "
            f"{offer.description_ar or ''} "
            f"Preis: {offer.offer_price} SP, "
            f"Ort: {offer.location_name_ar or 'kein Name'}, "
            f"Koordinaten: {offer.latitude},{offer.longitude}"
        )
    return "\n".join(lines)

def generate_travel_plan(preferences: dict, days: int, context: str, lang: str = "ar") -> dict:
    if lang == "ar":
        instruction = "Erstelle den Reiseplan **ausschließlich auf Arabisch**."
    elif lang == "de":
        instruction = "Erstelle den Reiseplan **ausschließlich auf Deutsch**."
    else:
        instruction = "Erstelle den Reiseplan **ausschließlich auf Englisch**."

    system_prompt = f"""
Du bist ein Reiseplaner für Syrien. {instruction}

Erstelle einen {days}-Tages-Reiseplan basierend auf:
- Nutzerpräferenzen: {json.dumps(preferences, ensure_ascii=False)}
- Nur folgende reale Orte verwenden (jeder Ort hat Koordinaten):

{context}

Antworte NUR mit einem gültigen JSON-Objekt (kein zusätzlicher Text). 
Das JSON-Format:
{{
  "plan": [
    {{
      "day": 1,
      "activities": [
        {{
          "time": "09:00",
          "title": "...",
          "location": "...",
          "lat": 33.5138,
          "lng": 36.2765,
          "description": "..."
        }}
      ]
    }}
  ]
}}
"""
    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.2,
    )
    response = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Erstelle den Reiseplan gemäß den Vorgaben.",
        config=config,
    )
    raw = response.text.strip()
    if raw.startswith("```"):
        lines = raw.splitlines()
        lines = lines[1:-1]
        raw = "\n".join(lines)
    return json.loads(raw)