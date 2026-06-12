from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict
from datetime import datetime
from google import genai
from google.genai import types
import json, uuid

from app.core.database import get_db
from app.core.config import settings
from app.core.gemini_client import get_genai_client
from app.models.offer import Offer, Category
from app.models.location import Location
from app.schemas.offer import OfferResponse
from app.schemas.location import LocationOut
from pydantic import BaseModel

router = APIRouter(prefix="/chatbot", tags=["المساعد الذكي"])
genai_client = get_genai_client()


class ChatResponse(BaseModel):
    reply: str
    offers: List[OfferResponse] = []
    locations: List[LocationOut] = []
    plan_id: Optional[int] = None
    session_id: str = ""


# ---------------------------------------------------------------------------
#  Function declarations for Gemini
# ---------------------------------------------------------------------------

search_offers_function = {
    "name": "search_offers",
    "description": "Search for active offers by category, max price, and keywords in Syria.",
    "parameters": {
        "type": "object",
        "properties": {
            "category": {"type": "string", "description": "Category (Arabic or English)"},
            "max_price": {"type": "number", "description": "Max price in Syrian Pounds"},
            "keywords": {"type": "string", "description": "Search terms in any language"}
        },
        "required": []
    }
}

search_locations_function = {
    "name": "search_locations",
    "description": "Search the Syria tourism database for places, landmarks, restaurants, museums, neighbourhoods, etc. Use when the user asks about sightseeing, things to do, tourist attractions, or specific cities.",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name (Arabic or English). Examples: Damascus, دمشق, Aleppo, حلب"},
            "category": {"type": "string", "description": "Category like history, food, nature, shopping, museum, religious, beach, mountain, hotel, wellness"},
            "keywords": {"type": "string", "description": "Free-text keywords to match name or description"}
        },
        "required": []
    }
}

plan_trip_function = {
    "name": "plan_trip",
    "description": "Create a detailed multi-day travel itinerary for Syria using the official tourism database.",
    "parameters": {
        "type": "object",
        "properties": {
            "interests": {"type": "string", "description": "Comma-separated interests: history,food,nature,shopping,adventure,art,religious,beach,mountain,hotel,wellness"},
            "days": {"type": "integer", "description": "Number of days (1–14, default 5)"},
            "start_city": {"type": "string", "description": "Starting city, default Damascus"}
        },
        "required": ["interests", "days"]
    }
}

sessions: Dict[str, list] = {}


# ---------------------------------------------------------------------------
#  DB helpers
# ---------------------------------------------------------------------------

def search_offers_in_db(db: Session, category=None, max_price=None, keywords=None):
    filters = [Offer.is_active == True, Offer.end_date > datetime.utcnow()]
    if category:
        cat_obj = db.query(Category).filter((Category.name_ar == category) | (Category.name_en == category)).first()
        if cat_obj:
            filters.append(Offer.category_id == cat_obj.id)
    if max_price:
        filters.append(Offer.offer_price <= max_price)
    query = db.query(Offer).filter(*filters)
    if keywords:
        term = f"%{keywords}%"
        query = query.filter(Offer.title_ar.ilike(term) | Offer.title_en.ilike(term) | Offer.description_ar.ilike(term) | Offer.description_en.ilike(term))
    return query.order_by(Offer.offer_price).limit(5).all()


def search_locations_in_db(db: Session, city=None, category=None, keywords=None):
    q = db.query(Location)
    if city:
        from sqlalchemy import func
        c = city.strip().lower()
        q = q.filter((func.lower(Location.city_en) == c) | (func.lower(Location.city_ar) == c))
    if category:
        q = q.filter(Location.category == category.lower())
    if keywords:
        from sqlalchemy import func
        term = f"%{keywords}%"
        q = q.filter(
            Location.name_ar.ilike(term) |
            Location.name_en.ilike(term) |
            Location.description_ar.ilike(term) |
            Location.description_en.ilike(term)
        )
    return q.limit(8).all()


# ---------------------------------------------------------------------------
#  System prompt (multilingual, professional)
# ---------------------------------------------------------------------------

SYSTEM_PROMPT_TEMPLATE = """You are Offria — a multilingual, expert Syria travel assistant.

LANGUAGE RULE (strict):
• Detect the user's message language.
• If Arabic → reply ONLY in Modern Standard Arabic (الفصحى). Never use English or German.
• If German → reply ONLY in German. Never use English or Arabic.
• If English → reply ONLY in English. Never use Arabic or German.
• Never mix languages inside one reply.

CAPABILITIES:
1. Offers — restaurants, hotels, activities with discounts.
2. Locations — tourist sites, museums, neighbourhoods, nature spots from the official Syria database.
3. Trip Planning — multi-day itineraries with realistic routing.

TONE:
• Friendly, enthusiastic, concise.
• For locations: describe what the visitor will experience in 1–2 sentences.
• When listing places, mention city, category, and a highlight.

CRITICAL RULE — NO HALLUCINATION:
• You may ONLY mention places, museums, restaurants, hotels, or landmarks that were returned by the search_locations or search_offers database functions.
• NEVER use your own general knowledge about Syria, Damascus, Aleppo, or any other city.
• If the database returns zero results, be honest: say "I could not find matching places in our database right now" in the user's language.
• Do NOT invent museum names, historical sites, or attractions.

WHEN TO CALL FUNCTIONS:
• User asks about prices, discounts, deals → call search_offers.
• User asks about sightseeing, places to visit, neighbourhoods, landmarks → call search_locations.
• User asks for a full itinerary or travel plan → call plan_trip.
"""


# ---------------------------------------------------------------------------
#  Main endpoint
# ---------------------------------------------------------------------------

@router.get("/", response_model=ChatResponse)
async def chat(query: str, session_id: str = Query(""), db: Session = Depends(get_db)):
    sid = session_id.strip() or str(uuid.uuid4())
    history = sessions.get(sid, [])

    # Detect language
    has_arabic = any('\u0600' <= c <= '\u06ff' for c in query)
    has_german = any(c in 'äöüßÄÖÜ' for c in query)
    if has_arabic:
        lang = "ar"
    elif has_german:
        lang = "de"
    else:
        lang = "en"

    tools = types.Tool(function_declarations=[search_offers_function, search_locations_function, plan_trip_function])

    config = types.GenerateContentConfig(
        tools=[tools],
        system_instruction=SYSTEM_PROMPT_TEMPLATE,
        temperature=0.2,
    )

    contents = []
    for msg in history[-20:]:
        role = "user" if msg["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part(text=msg["text"])]))
    contents.append(types.Content(role="user", parts=[types.Part(text=query)]))

    try:
        response = genai_client.models.generate_content(model="gemini-2.5-flash-lite", contents=contents, config=config)
        fc = None
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    fc = part.function_call
                    break

        # ------------------------------------------------ search_offers -----
        if fc and fc.name == "search_offers":
            args = fc.args
            offers = search_offers_in_db(db, category=args.get("category"), max_price=args.get("max_price"), keywords=args.get("keywords"))
            offers_resp = [OfferResponse.model_validate(o) for o in offers]

            if not offers_resp:
                if lang == "ar":
                    reply = "❌ لا توجد عروض نشطة في قاعدة البيانات حالياً. يمكنني مساعدتك في التخطيط لرحلة بدلاً من ذلك!"
                elif lang == "de":
                    reply = "❌ Derzeit gibt es keine aktiven Angebote in unserer Datenbank. Ich kann dir stattdessen bei der Reiseplanung helfen!"
                else:
                    reply = "❌ There are no active offers in our database right now. I can help you plan a trip instead!"
            else:
                if lang == "ar":
                    reply = f"✅ وجدت لك {len(offers_resp)} عروض!"
                elif lang == "de":
                    reply = f"✅ Ich habe {len(offers_resp)} Angebote gefunden!"
                else:
                    reply = f"✅ Found {len(offers_resp)} offers!"

            history += [{"role":"user","text":query},{"role":"assistant","text":reply}]
            sessions[sid] = history
            return ChatResponse(reply=reply, offers=offers_resp, session_id=sid)

        # ------------------------------------------------ search_locations ---
        if fc and fc.name == "search_locations":
            args = fc.args
            locs = search_locations_in_db(db, city=args.get("city"), category=args.get("category"), keywords=args.get("keywords"))
            locs_resp = [LocationOut.model_validate(l) for l in locs]

            if not locs_resp:
                if lang == "ar":
                    reply = "❌ لم أجد أماكن مطابقة في قاعدة بياناتنا حالياً. جرّب كلمات بحث مختلفة أو مدينة أخرى."
                elif lang == "de":
                    reply = "❌ Ich habe leider keine passenden Orte in unserer Datenbank gefunden. Versuche andere Suchbegriffe oder eine andere Stadt."
                else:
                    reply = "❌ I could not find matching places in our database right now. Try different keywords or another city."
                history += [{"role":"user","text":query},{"role":"assistant","text":reply}]
                sessions[sid] = history
                return ChatResponse(reply=reply, locations=[], session_id=sid)

            # Build reply strictly from DB results — no external knowledge
            if lang == "ar":
                lines = [f"✅ وجدت {len(locs_resp)} أماكن في قاعدة البيانات:\n"]
            elif lang == "de":
                lines = [f"✅ Ich habe {len(locs_resp)} Orte in unserer Datenbank gefunden:\n"]
            else:
                lines = [f"✅ Found {len(locs_resp)} places in our database:\n"]

            for l in locs_resp[:8]:
                name = l.name_ar or l.name_en or ""
                city = l.city_ar or l.city_en or ""
                cat = l.category or ""
                desc = l.description_ar or l.description_en or ""
                lines.append(f"• {name} — {city} ({cat})")
                if desc:
                    short = desc.split(".")[0] + "." if "." in desc else desc[:120]
                    lines.append(f"  {short}")

            reply = "\n".join(lines)

            history += [{"role":"user","text":query},{"role":"assistant","text":reply}]
            sessions[sid] = history
            return ChatResponse(reply=reply, locations=locs_resp, session_id=sid)

        # ------------------------------------------------ plan_trip ---------
        if fc and fc.name == "plan_trip":
            args = fc.args
            from app.services.travel_planner import generate_travel_plan
            days = min(max(int(args.get("days", 5)), 1), 14)
            preferences = {
                "interests": args.get("interests", "history,food"),
                "start_city": args.get("start_city", "Damascus"),
                "lang": lang,
            }
            plan = generate_travel_plan(db, preferences=preferences, days=days, lang=lang)

            lines = []
            if lang == "ar":
                lines.append("🗺️ **خطة رحلتك إلى سوريا** 🌟\n")
            elif lang == "de":
                lines.append("🗺️ **Ihr Syrien-Reiseplan** 🌟\n")
            else:
                lines.append("🗺️ **Your Syria Travel Itinerary** 🌟\n")

            for day in plan["plan"]:
                lines.append(f"\n📅 **{'اليوم' if lang=='ar' else 'Tag' if lang=='de' else 'Day'} {day['day']}**")
                for a in day["activities"]:
                    lines.append(f"  ⏰ {a['time']} – {a['title']} ({a['location']})")

            lines.append("")
            if lang == "ar":
                lines.append("💡 يمكنك تصدير الخطة إلى تقويم هاتفك بالضغط على الزر أدناه.")
            elif lang == "de":
                lines.append("💡 Sie können den Plan über den Button unten in Ihren Kalender exportieren.")
            else:
                lines.append("💡 Export to your calendar using the button below.")

            reply_text = "\n".join(lines)

            from app.models.travel_plan import TravelPlan
            db_plan = TravelPlan(preferences=preferences, days=days, plan_data=plan)
            db.add(db_plan)
            db.commit()
            db.refresh(db_plan)

            history += [{"role":"user","text":query},{"role":"assistant","text":reply_text}]
            sessions[sid] = history
            return ChatResponse(reply=reply_text, plan_id=db_plan.id, session_id=sid)

        # ------------------------------------------------ plain text --------
        text = response.candidates[0].content.parts[0].text if response.candidates else (
            "لم أفهم طلبك." if lang == "ar" else "Ich habe das nicht verstanden." if lang == "de" else "I didn't understand."
        )
        history += [{"role":"user","text":query},{"role":"assistant","text":text}]
        sessions[sid] = history
        return ChatResponse(reply=text, session_id=sid)

    except Exception as e:
        err = f"⚠️ خطأ: {str(e)}" if lang == "ar" else f"⚠️ Fehler: {str(e)}" if lang == "de" else f"⚠️ Error: {str(e)}"
        return ChatResponse(reply=err, session_id=sid)
