from datetime import datetime, timedelta, timezone

from app.models.offer import Offer
from app.models.user import User


def test_complete_user_flow_register_login_browse_book_book_and_pay(client, db_session):
    register = client.post(
        "/api/v1/auth/register",
        json={
            "phone": "0999888777",
            "full_name": "Integration User",
            "email": "integration@example.com",
            "role": "customer",
        },
    )
    assert register.status_code == 200

    # Activate user so login succeeds
    user = db_session.query(User).filter(User.phone == "0999888777").first()
    assert user is not None
    user.is_active = True
    db_session.commit()

    login = client.post("/api/v1/auth/login", json={"phone": "0999888777"})
    assert login.status_code == 200
    assert login.json()["access_token"]

    category = client.post(
        "/api/v1/categories/",
        json={"name_ar": "مطاعم", "name_en": "Restaurants", "sort_order": 1},
    ).json()

    now = datetime.now(timezone.utc)
    created_offer = client.post(
        "/api/v1/offers/",
        json={
            "title_ar": "عرض تكاملي",
            "title_en": "Integration Offer",
            "description_ar": "وصف",
            "description_en": "Description",
            "original_price": 100.0,
            "offer_price": 70.0,
            "start_date": (now - timedelta(days=1)).isoformat(),
            "end_date": (now + timedelta(days=3)).isoformat(),
            "image_urls": None,
            "category_id": category["id"],
            "is_flash": False,
            "flash_discount_percent": 0,
            "latitude": 33.5,
            "longitude": 36.3,
            "location_name_ar": "دمشق",
            "location_name_en": "Damascus",
        },
    )
    assert created_offer.status_code == 201
    offer_id = created_offer.json()["id"]

    offer = db_session.query(Offer).filter(Offer.id == offer_id).first()
    offer.approved = True
    db_session.commit()

    offers = client.get("/api/v1/offers/")
    assert offers.status_code == 200
    assert any(item["id"] == offer_id for item in offers.json())

    booking = client.post(
        "/api/v1/bookings/",
        json={
            "user_name": "Integration User",
            "user_phone": "0999888777",
            "offer_id": offer_id,
            "booked_at": (now + timedelta(days=1)).isoformat(),
            "quantity": 2,
            "total_price": 140.0,
        },
    )
    assert booking.status_code == 201
    booking_id = booking.json()["id"]

    payment = client.post(
        "/api/v1/payments/pay",
        params={
            "booking_id": booking_id,
            "amount": 140.0,
            "phone": "0999888777",
            "method": "sham_cash",
        },
    )
    assert payment.status_code == 200
    assert payment.json()["success"] is True
