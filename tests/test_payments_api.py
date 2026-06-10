from datetime import datetime, timedelta, timezone

from app.models.booking import Booking


def _seed_booking(client):
    client.post(
        "/api/v1/auth/register",
        json={"phone": "0944000111", "full_name": "Pay User", "role": "customer"},
    )
    category = client.post(
        "/api/v1/categories/",
        json={"name_ar": "ترفيه", "name_en": "Entertainment", "sort_order": 1},
    ).json()

    now = datetime.now(timezone.utc)
    offer = client.post(
        "/api/v1/offers/",
        json={
            "title_ar": "عرض ترفيه",
            "title_en": "Entertainment Offer",
            "description_ar": "وصف",
            "description_en": "Description",
            "original_price": 80.0,
            "offer_price": 55.0,
            "start_date": (now - timedelta(days=1)).isoformat(),
            "end_date": (now + timedelta(days=4)).isoformat(),
            "image_urls": None,
            "category_id": category["id"],
            "is_flash": False,
            "flash_discount_percent": 0,
            "latitude": 33.5,
            "longitude": 36.3,
            "location_name_ar": "دمشق",
            "location_name_en": "Damascus",
        },
    ).json()

    booking = client.post(
        "/api/v1/bookings/",
        json={
            "user_name": "Pay User",
            "user_phone": "0944000111",
            "offer_id": offer["id"],
            "booked_at": (now + timedelta(hours=2)).isoformat(),
            "quantity": 1,
            "total_price": 55.0,
        },
    ).json()
    return booking["id"]


def test_process_payment_success_updates_booking(client, db_session):
    booking_id = _seed_booking(client)
    response = client.post(
        "/api/v1/payments/pay",
        params={
            "booking_id": booking_id,
            "amount": 55.0,
            "phone": "0944000111",
            "method": "sham_cash",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["transaction_id"].startswith("SHAM-")

    booking = db_session.query(Booking).filter(Booking.id == booking_id).first()
    assert booking.status.value == "confirmed"
    assert booking.payment_id == payload["transaction_id"]
    assert booking.payment_method == "sham_cash"


def test_process_payment_nonexistent_booking_returns_404(client):
    response = client.post(
        "/api/v1/payments/pay",
        params={
            "booking_id": 9999,
            "amount": 10.0,
            "phone": "0944000999",
            "method": "mtn_cash",
        },
    )
    assert response.status_code == 404


def test_process_refund_success_when_more_than_one_hour_before_booking(client):
    booking_id = _seed_booking(client)
    response = client.post("/api/v1/payments/refund", params={"booking_id": booking_id})
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["booking_id"] == booking_id
    assert payload["status"] == "refunded"
    assert payload["service_fee"] == 5.5
    assert payload["refund_amount"] == 49.5


def test_process_refund_fails_within_one_hour_of_booking(client):
    client.post(
        "/api/v1/auth/register",
        json={"phone": "0944000222", "full_name": "Soon User", "role": "customer"},
    )
    category = client.post(
        "/api/v1/categories/",
        json={"name_ar": "ترفيه", "name_en": "Entertainment", "sort_order": 1},
    ).json()

    now = datetime.now(timezone.utc)
    offer = client.post(
        "/api/v1/offers/",
        json={
            "title_ar": "عرض قريب",
            "title_en": "Soon Offer",
            "description_ar": "وصف",
            "description_en": "Description",
            "original_price": 80.0,
            "offer_price": 55.0,
            "start_date": (now - timedelta(days=1)).isoformat(),
            "end_date": (now + timedelta(days=4)).isoformat(),
            "image_urls": None,
            "category_id": category["id"],
            "is_flash": False,
            "flash_discount_percent": 0,
            "latitude": 33.5,
            "longitude": 36.3,
            "location_name_ar": "دمشق",
            "location_name_en": "Damascus",
        },
    ).json()

    booking = client.post(
        "/api/v1/bookings/",
        json={
            "user_name": "Soon User",
            "user_phone": "0944000222",
            "offer_id": offer["id"],
            "booked_at": (now + timedelta(minutes=30)).isoformat(),
            "quantity": 1,
            "total_price": 55.0,
        },
    ).json()

    response = client.post("/api/v1/payments/refund", params={"booking_id": booking["id"]})
    assert response.status_code == 400
