import os
os.environ['GEMINI_API_KEY'] = 'dummy-key-for-test'

import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models.location import Location

engine = create_engine('sqlite:///:memory:')
Location.__table__.create(bind=engine)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

locs = [
    Location(name_ar='جبل قاسيون', name_en='Mount Qasioun', city_ar='دمشق', city_en='Damascus', lat=33.55, lng=36.28, category='nature', description_en='Panoramic mountain view over Damascus', visit_duration='2h'),
    Location(name_ar='عين الفيجة', name_en='Ain al-Fijah Bridge', city_ar='ريف دمشق', city_en='Rural Damascus', lat=33.6, lng=36.3, category='nature', description_en='Fresh water springs and stone bridge', visit_duration='1.5h'),
    Location(name_ar='تل شهاب', name_en='Tel Shahab Waterfall', city_ar='درعا', city_en='Daraa', lat=32.7, lng=36.1, category='nature', description_en='Beautiful waterfall in Daraa', visit_duration='2h'),
    Location(name_ar='جزيرة أرواد', name_en='Arwad Island', city_ar='طرطوس', city_en='Tartus', lat=34.85, lng=35.85, category='beach', description_en='Historic island fortress off Tartus', visit_duration='3h'),
    Location(name_ar='دهر الجبل', name_en='Dahr al-Jabal Tourist Area', city_ar='السويداء', city_en='As-Suwayda', lat=32.7, lng=36.6, category='mountain', description_en='Mountain tourist area with great views', visit_duration='half-day'),
    Location(name_ar='القدموس', name_en='Al-Qadmus', city_ar='طرطوس', city_en='Tartus', lat=34.98, lng=36.15, category='history', description_en='Crusader castle in Tartus mountains', visit_duration='2h'),
    Location(name_ar='شميميس', name_en='Shmemis Castle', city_ar='السلمية', city_en='Al-Salamiyah', lat=35.0, lng=37.0, category='history', description_en='Ancient castle ruins on a hill', visit_duration='1.5h'),
    Location(name_ar='صلنفة', name_en='Slunfeh', city_ar='اللاذقية', city_en='Latakia', lat=35.6, lng=36.0, category='nature', description_en='Mountain resort with forest walks', visit_duration='half-day'),
    Location(name_ar='كركدوان', name_en='Karadouran', city_ar='اللاذقية', city_en='Latakia', lat=35.7, lng=36.0, category='beach', description_en='Secluded beach near Kessab', visit_duration='2h'),
    Location(name_ar='بصرى', name_en='Bosra Amphitheatre', city_ar='درعا', city_en='Daraa', lat=32.5, lng=36.5, category='history', description_en='Roman amphitheatre in Bosra', visit_duration='2h'),
    Location(name_ar='معلولا', name_en='Maaloula', city_ar='ريف دمشق', city_en='Rural Damascus', lat=33.8, lng=36.5, category='religious', description_en='Christian village with Aramaic speakers', visit_duration='half-day'),
    Location(name_ar='قلعة حلب', name_en='Aleppo Citadel', city_ar='حلب', city_en='Aleppo', lat=36.2, lng=37.1, category='history', description_en='Massive medieval fortress in Aleppo', visit_duration='2h'),
    Location(name_ar='نواعير حماة', name_en='Hama Norias', city_ar='حماة', city_en='Hama', lat=35.1, lng=36.7, category='history', description_en='Ancient water wheels on the Orontes River', visit_duration='1h'),
    Location(name_ar='تدمر', name_en='Palmyra', city_ar='تدمر', city_en='Palmyra', lat=34.5, lng=38.3, category='history', description_en='Spectacular Roman ruins in the desert', visit_duration='half-day'),
    # Food places for lunch testing
    Location(name_ar='مطعم نارنج', name_en='Naranj Restaurant', city_ar='دمشق', city_en='Damascus', lat=33.51, lng=36.30, category='food', description_en='Fine dining in the Old City with traditional Syrian dishes', visit_duration='1.5h'),
    Location(name_ar='مطعم الصياد', name_en='Al-Sayyad Seafood', city_ar='طرطوس', city_en='Tartus', lat=34.89, lng=35.88, category='food', description_en='Fresh fish and seafood by the harbour', visit_duration='1.5h'),
]
for l in locs:
    db.add(l)
db.commit()

from app.services.travel_planner import PlaceScorer, DayScheduler

print('=== Test PlaceScorer ===')
scorer = PlaceScorer(db, ['nature', 'adventure'], 'Damascus')
selected = scorer.select_places(20)
print(f'Selected {len(selected)} places:')
for p in selected:
    print(f'  - {p["name_en"]} ({p["city_en"]}) cat={p["category"]}')

print()
print('=== Test DayScheduler ===')
scheduler = DayScheduler('Damascus', 5)
days = scheduler.schedule(selected)
print(f'Scheduled {len(days)} days:')
for d in days:
    print(f'  Day {d["day"]}: {d["city"]} — travel_from={d.get("travel_from")} drive={d.get("drive_km"):.0f}km')
    for a in d['activities']:
        print(f'    - {a["name_en"]}')

# Check for duplicates
all_ids = []
for d in days:
    for a in d['activities']:
        all_ids.append(a['id'])

if len(all_ids) != len(set(all_ids)):
    print('ERROR: Duplicate places found!')
    from collections import Counter
    c = Counter(all_ids)
    for k, v in c.items():
        if v > 1:
            print(f'  Duplicate ID {k}: {v} times')
else:
    print()
    print('OK: No duplicate places across entire itinerary')

# Check city diversity
all_cities = set()
for d in days:
    all_cities.add(d['city'])
print(f'Cities visited: {all_cities}')

if len(all_cities) >= 3:
    print('OK: Visited >= 3 cities')
else:
    print('WARNING: Only visited', len(all_cities), 'cities')

# Full end-to-end test with mocked Gemini
print()
print('=== Test generate_travel_plan (with mocked Gemini) ===')

from unittest.mock import MagicMock, patch
from app.services import travel_planner as tp_module

# Mock Gemini response: return descriptions as JSON
mock_response = MagicMock()
mock_response.text = json.dumps({
    "descriptions": {
        "Mount Qasioun": "A stunning viewpoint overlooking Damascus, best visited at sunset for panoramic city views.",
        "Ain al-Fijah Bridge": "Historic stone bridge surrounded by fresh springs and lush greenery, perfect for a short nature walk.",
        "Tel Shahab Waterfall": "A hidden gem waterfall in southern Syria, ideal for nature lovers seeking a refreshing escape.",
        "Dahr al-Jabal Tourist Area": "Mountain resort area offering spectacular hiking trails and panoramic views over the Syrian countryside.",
        "Arwad Island": "Tiny inhabited island with a historic fortress, reachable by boat from Tartus harbour.",
        "Slunfeh": "Beautiful mountain village surrounded by pine forests, famous for cool summer retreats and scenic walks.",
        "Karadouran": "Secluded pebble beach near Kessab with crystal clear water, perfect for a quiet swim.",
        "Bosra Amphitheatre": "Well-preserved Roman amphitheatre in a black-basalt city, a UNESCO World Heritage highlight.",
        "Maaloula": "Ancient Christian village where Aramaic is still spoken, nestled in dramatic cliff-side scenery.",
        "Aleppo Citadel": "One of the oldest and largest castles in the world, dominating the skyline of Aleppo.",
        "Hama Norias": "Iconic wooden water wheels on the Orontes River, a unique engineering feat still functioning today.",
        "Palmyra": "Magnificent Roman ruins rising from the desert, including the grand colonnade and Temple of Bel.",
        "Al-Qadmus": "Crusader castle perched on a mountain ridge, offering commanding views over the Tartus countryside.",
        "Shmemis Castle": "Ruined fortress on a volcanic hilltop, once guarding the ancient trade routes of central Syria.",
    }
})

with patch.object(tp_module.genai_client.models, 'generate_content', return_value=mock_response):
    from app.services.travel_planner import generate_travel_plan, build_context

    plan = generate_travel_plan(db, {'interests': 'nature,adventure', 'start_city': 'Damascus'}, 5, 'en')
    import json
    print(json.dumps(plan, ensure_ascii=False, indent=2)[:2000])
    print('...')

    # Verify structure
    assert 'plan' in plan, 'Missing plan'
    assert 'route' in plan, 'Missing route'
    for day in plan['plan']:
        assert 'activities' in day
        for act in day['activities']:
            assert 'title' in act
            assert 'description' in act
            assert act['description'], f"Empty description for {act['title']}"

    # Verify at least one lunch suggestion exists across all days
    lunch_count = sum(1 for d in plan['plan'] if any(a.get('type') == 'meal' or a.get('time') == '13:00' for a in d['activities']))
    assert lunch_count >= 1, 'Expected at least one lunch suggestion in the itinerary'

    print()
    print('OK: generate_travel_plan structure valid')

    # Test build_context compatibility
    ctx = build_context(db, {'interests': 'nature,adventure', 'start_city': 'Damascus'}, 5)
    assert isinstance(ctx, str)
    assert len(ctx) > 0
    print('OK: build_context backward compatible')

db.close()
print()
print('ALL TESTS PASSED')
