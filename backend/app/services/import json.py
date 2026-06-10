import json
from sqlalchemy.orm import Session
from google import genai
from google.genai import types
from app.core.config import settings
from app.models.offer import Offer

genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)

def build_context(db: Session) -> str:
    """
    Sammelt alle aktiven Angebote mit Koordinaten und formatiert sie als Auflistung.
    Ergänzend könnten CulturalSites aus einer separaten Liste einfließen.
    """
    offers = db.query(Offer).filter(
        Offer.is_active == True,
        Offer.approved == True,
        Offer.latitude.isnot(None),
        Offer.longitude.isnot(None)
    ).all()
    lines = []
    for offer in offers:
        lines.append(
            f"- {offer.title_ar} (Kategorie: {offer.category.name_ar if offer.category else 'Allgemein'}): "
            f"{offer.description_ar or ''} "
            f"Preis: {offer.offer_price} SP, "
            f"Ort: {offer.location_name_ar or 'kein Name'}, "
            f"Koordinaten: {offer.latitude},{offer.longitude}"
        )
    return "\n".join(lines)

def generate_travel_plan(preferences: dict, days: int, context: str) -> dict:
    system_prompt = f"""
Du bist ein Reiseplaner für Syrien. Erstelle einen {days}-Tages-Reiseplan basierend auf:
- Nutzerpräferenzen: {json.dumps(preferences, ensure_ascii=False)}
- Nur folgende reale Orte verwenden (jeder Ort hat Koordinaten):

{context}

Die Antwort muss ausschließlich ein gültiges JSON-Objekt sein (kein zusätzlicher Text). 
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
    # Bereinigung, falls Markdown-Codeblock
    if raw.startswith("```"):
        lines = raw.splitlines()
        lines = lines[1:-1]
        raw = "\n".join(lines)
    return json.loads(raw)