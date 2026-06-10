import json
from google import genai
from google.genai import types
from app.core.config import settings
from PIL import Image, UnidentifiedImageError
import io

genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)

def validate_image(image_bytes: bytes, category_name: str, mime_type: str = "image/jpeg") -> dict:
    """
    Führt eine KI-gestützte Analyse durch und prüft, ob das Bild zur angegebenen Kategorie passt.
    Gibt einen Dict mit 'score' (0-100), 'match' (bool) und 'message' (str) zurück.
    """
    try:
        # Qualitätscheck: Mindestauflösung
        img = Image.open(io.BytesIO(image_bytes))
        w, h = img.size
        if w < 800 or h < 600:
            return {"score": 0, "match": False, "message": "Auflösung zu gering (<800x600)"}
    except UnidentifiedImageError:
        return {"score": 0, "match": False, "message": "Kein gültiges Bildformat"}

    prompt = f"""
Du prüfst Bilder für eine Reise‑ und Angebotsplattform.
Das Bild muss thematisch zur Kategorie '{category_name}' passen.
Antworte ausschließlich mit JSON:
{{
  "match": true/false,
  "reason": "kurze Begründung (max. 200 Zeichen)"
}}
"""
    config = types.GenerateContentConfig(
        system_instruction="Du bist ein Bildanalyse‑Spezialist.",
        temperature=0,
    )
    response = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[types.Part.from_bytes(data=image_bytes, mime_type=mime_type)],
        config=config,
    )
    raw = response.text.strip()
    if raw.startswith("```"):
        lines = raw.splitlines()
        lines = lines[1:-1]
        raw = "\n".join(lines)
    result = json.loads(raw)
    return {
        "score": 90 if result.get("match") else 50,
        "match": result.get("match", True),
        "message": result.get("reason", "")
    }