from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.travel_plan import TravelPlanRequest, TravelPlanResponse
from app.models.travel_plan import TravelPlan
from app.services.travel_planner import build_context, generate_travel_plan
from ics import Calendar, Event
from datetime import datetime, timedelta, timezone
import uuid

router = APIRouter(prefix="/travel-planner", tags=["Travel Planner"])

@router.post("/generate", response_model=TravelPlanResponse)
def create_travel_plan(req: TravelPlanRequest, db: Session = Depends(get_db)):
    start_city = req.preferences.get("start_city", "Damascus")
    ctx = build_context(db, req.preferences, start_city, req.days)
    if not ctx:
        raise HTTPException(400, "No locations available in database.")

    lang = req.preferences.get("lang", "ar")
    plan_data = generate_travel_plan(db, req.preferences, req.days, lang=lang)

    db_plan = TravelPlan(
        preferences=req.preferences,
        days=req.days,
        plan_data=plan_data,
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)

    return {"id": db_plan.id, "plan": plan_data["plan"]}

@router.get("/{plan_id}/export-ics")
def export_ics(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(TravelPlan).filter(TravelPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(404, "Plan not found")

    tz_syria = timezone(timedelta(hours=3))
    cal = Calendar()

    for day in plan.plan_data["plan"]:
        d = day["day"]
        for act in day["activities"]:
            e = Event()
            e.name = act["title"]
            e.location = f"geo:{act['lat']},{act['lng']}"
            e.description = act.get("description", "")
            e.uid = str(uuid.uuid4())

            try:
                h, m = map(int, act["time"].split(":"))
                start = datetime(2026, 5, d, h, m, tzinfo=tz_syria)
                e.begin = start
                e.end = start + timedelta(hours=1)
                e.dtstamp = datetime.now(tz_syria)
            except:
                start = datetime(2026, 5, d, tzinfo=tz_syria)
                e.begin = start.date()
                e.end = start.date() + timedelta(days=1)
                e.dtstamp = datetime.now(tz_syria)
                e.make_all_day()

            cal.events.add(e)

    ics_str = cal.serialize()
    return Response(content=ics_str, media_type="text/calendar",
                    headers={"Content-Disposition": f"attachment; filename=travel_plan_{plan_id}.ics"})