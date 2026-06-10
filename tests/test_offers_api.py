from datetime import datetime, timedelta, timezone

from app.models.offer import Offer

def _create_category(client):
    response = client.post(
        "/api/v1/categories/",
        json={"name_ar": "حدائق", "name_en": "Parks", "sort_order": 1},
    )
    assert response.status_code == 201
    return response.json()["id"]


def _offer_payload(category_id, title_en="Park Offer"):
    now = datetime.now(timezone.utc)
    return {
        "title_ar": "عرض حديقة",
        "title_en": title_en,
        "description_ar": "وصف",
        "description_en": "Description",
        "original_price": 100.0,
        "offer_price": 75.0,
        "start_date": (now - timedelta(days=1)).isoformat(),
        "end_date": (now + timedelta(days=5)).isoformat(),
        "image_urls": None,
        "category_id": category_id,
        "is_flash": False,
        "flash_discount_percent": 0,
        "latitude": 33.5138,
        "longitude": 36.2765,
        "location_name_ar": "دمشق",
        "location_name_en": "Damascus",
    }


def test_create_offer_and_list_active_offers(client, db_session):
    category_id = _create_category(client)
    payload = _offer_payload(category_id=category_id)

    create_response = client.post("/api/v1/offers/", json=payload)
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["id"] > 0
    assert created["title_en"] == "Park Offer"

    offer = db_session.query(Offer).filter(Offer.id == created["id"]).first()
    offer.approved = True
    db_session.commit()

    list_response = client.get("/api/v1/offers/")
    assert list_response.status_code == 200
    offers = list_response.json()
    assert len(offers) == 1
    assert offers[0]["id"] == created["id"]


def test_list_offers_filters_by_category_and_query(client, db_session):
    category_id = _create_category(client)
    payload = _offer_payload(category_id=category_id, title_en="Special Cinema Offer")

    created = client.post("/api/v1/offers/", json=payload).json()
    offer = db_session.query(Offer).filter(Offer.id == created["id"]).first()
    offer.approved = True
    db_session.commit()

    filter_by_category = client.get(f"/api/v1/offers/?category_id={category_id}")
    assert filter_by_category.status_code == 200
    assert len(filter_by_category.json()) == 1

    filter_by_query = client.get("/api/v1/offers/?q=Cinema")
    assert filter_by_query.status_code == 200
    assert len(filter_by_query.json()) == 1


def test_list_offers_sorted_by_distance_with_lat_lon(client, db_session):
    category_id = _create_category(client)
    nearby_payload = _offer_payload(category_id=category_id, title_en="Nearby")
    nearby_payload["latitude"] = 33.5138
    nearby_payload["longitude"] = 36.2765

    farther_payload = _offer_payload(category_id=category_id, title_en="Farther")
    farther_payload["latitude"] = 34.0
    farther_payload["longitude"] = 37.0

    nearby = client.post("/api/v1/offers/", json=nearby_payload).json()
    farther = client.post("/api/v1/offers/", json=farther_payload).json()

    offer1 = db_session.query(Offer).filter(Offer.id == nearby["id"]).first()
    offer2 = db_session.query(Offer).filter(Offer.id == farther["id"]).first()
    offer1.approved = True
    offer2.approved = True
    db_session.commit()

    response = client.get("/api/v1/offers/?lat=33.51&lon=36.28")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title_en"] == "Nearby"
    assert data[1]["title_en"] == "Farther"
