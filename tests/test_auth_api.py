from app.models.user import User


def test_register_and_login_success(client, db_session):
    register_payload = {
        "phone": "0999000111",
        "full_name": "Test User",
        "email": "test@example.com",
        "role": "customer",
    }
    register_response = client.post("/api/v1/auth/register", json=register_payload)
    assert register_response.status_code == 200
    register_data = register_response.json()
    assert register_data["message"]

    # User is inactive after registration; activate directly for login test
    user = db_session.query(User).filter(User.phone == register_payload["phone"]).first()
    assert user is not None
    user.is_active = True
    db_session.commit()

    login_response = client.post(
        "/api/v1/auth/login", json={"phone": register_payload["phone"]}
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert login_data["token_type"] == "bearer"
    assert isinstance(login_data["access_token"], str) and login_data["access_token"]
    assert login_data["role"] == "customer"


def test_register_duplicate_phone_returns_200_with_message(client):
    payload = {
        "phone": "0999000222",
        "full_name": "Dup User",
        "email": "dup@example.com",
        "role": "customer",
    }
    first = client.post("/api/v1/auth/register", json=payload)
    assert first.status_code == 200

    duplicate = client.post("/api/v1/auth/register", json=payload)
    assert duplicate.status_code == 200
    assert "مسجل مسبقاً" in duplicate.json()["message"]


def test_login_unknown_user_returns_401(client):
    response = client.post("/api/v1/auth/login", json={"phone": "0000000999"})
    assert response.status_code == 401
