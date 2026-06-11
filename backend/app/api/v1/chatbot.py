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
from app.schemas.offer import OfferResponse
from pydantic import BaseModel

router = APIRouter(prefix="/chatbot", tags=["المساعد الذكي"])
genai_client = get_genai_client()

class ChatResponse(BaseModel):
    reply: str
    offers: List[OfferResponse] = []
    plan_id: Optional[int] = None
    session_id: str = ""

search_offers_function = {
    "name": "search_offers",
    "description": "Search for offers by category, max price, and keywords in Syria.",
    "parameters": {
        "type": "object",
        "properties": {
            "category": {"type": "string", "description": "Category (Arabic/English)"},
            "max_price": {"type": "number", "description": "Max price in SP"},
            "keywords": {"type": "string", "description": "Search terms"}
        },
        "required": []
    }
}

plan_trip_function = {
    "name": "plan_trip",
    "description": "Create a detailed multi-day travel itinerary for Syria.",
    "parameters": {
        "type": "object",
        "properties": {
            "interests": {"type": "string", "description": "Interests: history,food,nature,shopping,adventure,art"},
            "days": {"type": "integer", "description": "Number of days (3-7, default 5)"},
            "start_city": {"type": "string", "description": "Starting city, default Damascus"}
        },
        "required": ["interests", "days"]
    }
}

sessions: Dict[str, list] = {}

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

@router.get("/", response_model=ChatResponse)
async def chat(query: str, session_id: str = Query(""), db: Session = Depends(get_db)):
    sid = session_id.strip() or str(uuid.uuid4())
    history = sessions.get(sid, [])

    has_arabic = any('\u0600' <= c <= '\u06ff' for c in query)
    has_german = any(c in 'äöüßÄÖÜ' for c in query)
    if has_arabic:
        lang = "ar"
    elif has_german:
        lang = "de"
    else:
        lang = "en"

    tools = types.Tool(function_declarations=[search_offers_function, plan_trip_function])

    system_prompt = (
        "You are a multilingual Syria travel assistant for the Offria app. "
        "**CRITICAL LANGUAGE RULE:** Detect the language of the user's message. "
        "If the message is in Arabic, answer ONLY in Arabic. "
        "If the message is in English, answer ONLY in English. "
        "If the message is in German, answer ONLY in German. "
        "Never mix languages. "
        "**Trip planning:** When the user requests a trip, call plan_trip IMMEDIATELY. "
        "**Offers:** When the user asks about restaurants, parks, museums, etc., call search_offers. "
        "Be friendly and enthusiastic."
    )

    config = types.GenerateContentConfig(
        tools=[tools],
        system_instruction=system_prompt,
        temperature=0.1,
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

        if fc:
            if fc.name == "search_offers":
                args = fc.args
                offers = search_offers_in_db(db, category=args.get("category"), max_price=args.get("max_price"), keywords=args.get("keywords"))
                offers_resp = [OfferResponse.model_validate(o) for o in offers]
                reply = (f"✅ وجدت لك {len(offers_resp)} عروض!" if has_arabic and offers_resp
                         else f"✅ Found {len(offers_resp)} offers!" if offers_resp
                         else ("❌ لم أجد عروضاً." if has_arabic else "❌ No offers found."))
                history += [{"role":"user","text":query},{"role":"assistant","text":reply}]
                sessions[sid] = history
                return ChatResponse(reply=reply, offers=offers_resp, session_id=sid)

            elif fc.name == "plan_trip":
                args = fc.args
                from app.services.travel_planner import generate_travel_plan
                days = min(max(int(args.get("days", 5)), 1), 7)
                preferences = {
                    "interests": args.get("interests", "history,food"),
                    "start_city": args.get("start_city", "Damascus"),
                }
                plan = generate_travel_plan(
                    preferences=preferences,
                    days=days,
                    lang=lang,
                )
                lines = []
                if has_arabic:
                    lines.append("🗺️ **خطة رحلتك إلى سوريا** 🌟\n")
                else:
                    lines.append("🗺️ **Your Syria Travel Itinerary** 🌟\n")
                for day in plan["plan"]:
                    lines.append(f"\n📅 **{'اليوم' if has_arabic else 'Day'} {day['day']}**")
                    for a in day["activities"]:
                        lines.append(f"  ⏰ {a['time']} – {a['title']} ({a['location']})")
                lines.append("")
                lines.append("💡 يمكنك تصدير الخطة إلى تقويم هاتفك بالضغط على الزر أدناه." if has_arabic else "💡 Export to your calendar using the button below.")
                reply_text = "\n".join(lines)

                from app.models.travel_plan import TravelPlan
                db_plan = TravelPlan(preferences=args, days=args.get("days", 5), plan_data=plan)
                db.add(db_plan)
                db.commit()
                db.refresh(db_plan)

                history += [{"role":"user","text":query},{"role":"assistant","text":reply_text}]
                sessions[sid] = history
                return ChatResponse(reply=reply_text, plan_id=db_plan.id, session_id=sid)

        text = response.candidates[0].content.parts[0].text if response.candidates else ("لم أفهم" if has_arabic else "I didn't understand")
        history += [{"role":"user","text":query},{"role":"assistant","text":text}]
        sessions[sid] = history
        return ChatResponse(reply=text, session_id=sid)

    except Exception as e:
        err = f"⚠️ خطأ: {str(e)}" if has_arabic else f"⚠️ Error: {str(e)}"
        return ChatResponse(reply=err, session_id=sid)