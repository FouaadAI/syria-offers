import os
os.environ.setdefault("DATABASE_URL", "postgresql://syriaoffers:syriaoffers@localhost:5432/syriaoffers")

from app.services.travel_planner import generate_travel_plan
from app.core.database import SessionLocal

db = SessionLocal()
try:
    for lang, days in [("de", 3), ("ar", 4)]:
        plan = generate_travel_plan(db, {"interests": "history,food", "start_city": "Damascus"}, days=days, lang=lang)
        print(f"--- {lang.upper()} {days}-day plan ---")
        for day in plan["plan"]:
            print(f"Day {day['day']} - {day['city']}")
            for a in day["activities"]:
                print(f"  {a['time']} | {a['title']} ({a['type']})")
            if "lunch" in day:
                l = day["lunch"]
                print(f"  LUNCH: {l['name']} ({l['cuisine']})")
        print()
        print("Route:", plan["route"])
        print()
        seen = set()
        dups = []
        for day in plan["plan"]:
            for a in day["activities"]:
                k = (day["city"], a["title"])
                if k in seen:
                    dups.append(k)
                seen.add(k)
        print("Duplicates:", dups if dups else "None")
        print()
        print()
finally:
    db.close()
