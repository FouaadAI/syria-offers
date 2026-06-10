from datetime import datetime, timedelta, timezone


def _create_category(client):
    res = client.post(
        "/api/v1/categories/",
        json={"name_ar": "نشاطات", "name_en": "Activities", "sort_order": 1},
    )
    return res.json()["id"]


def _create_offer(client, category_id):
    now = datetime.now(timezone.utc)
    payload = {
        "title_ar": "عرض نشاط",
        "title_en": "Activity Offer",
        "description_ar": "وصف",
        "description_en": "Description",
        "original_price": 50.0,
        "offer_price": 30.0,
        "start_date": (now - timedelta(days=1)).isoformat(),
        "end_date": (now + timedelta(days=7)).isoformat(),
        "image_urls": None,
        "category_id": category_id,
        "is_flash": False,
        "flash_discount_percent": 0,
        "latitude": 33.5,
        "longitude": 36.3,
        "location_name_ar": "دمشق",
        "location_name_en": "Damascus",
    }
    res = client.post("/api/v1/offers/", json=payload)
    return res.json()["id"]


def test_create_booking(client):
    client.post(
        "/api/v1/auth/register",
        json={"phone": "0933000111", "full_name": "Book User", "role": "customer"},
    )
    category_id = _create_category(client)
    offer_id = _create_offer(client, category_id)

    booking_payload = {
        "user_name": "Book User",
        "user_phone": "0933000111",
        "offer_id": offer_id,
        "booked_at": datetime.now(timezone.utc).isoformat(),
        "quantity": 2,
        "total_price": 60.0,
    }
    response = client.post("/api/v1/bookings/", json=booking_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] > 0
    assert data["offer_id"] == offer_id
    assert data["quantity"] == 2
    assert data["status"] == "confirmed"
    assert data["booking_code"].startswith("BOOK-")


def test_create_booking_validation_error(client):
    response = client.post(
        "/api/v1/bookings/",
        json={
            "user_name": "Incomplete",
            "user_phone": "0933000222",
            "quantity": 1,
            "total_price": 10.0,
        },
    )
    assert response.status_code == 422
