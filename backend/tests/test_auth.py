from app.domain.enums.auth import ShiftType


def test_login_success_returns_token_and_user(client, admin_user):
    response = client.post(
        "/api/v1/auth/login",
        json={"userId": "admin", "password": "admin"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token"]
    assert body["user"]["userId"] == "admin"
    assert body["user"]["name"] == "System Admin"
    assert body["user"]["role"] == "ADMIN"


def test_login_rejects_bad_password(client, admin_user):
    response = client.post(
        "/api/v1/auth/login",
        json={"userId": "admin", "password": "wrong"},
    )

    assert response.status_code == 401


def test_current_user_requires_bearer_token(client):
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


def test_current_user_returns_authenticated_user(client, auth_headers):
    response = client.get("/api/v1/auth/me", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["userId"] == "admin"


def test_update_shift_updates_current_user(client, auth_headers):
    response = client.put(
        "/api/v1/auth/me/shift",
        headers=auth_headers,
        json={"shift": ShiftType.NIGHT.value, "unitId": "99"},
    )

    assert response.status_code == 200
    assert response.json() == {"shift": "NIGHT", "unitId": "99"}

    me_response = client.get("/api/v1/auth/me", headers=auth_headers)
    assert me_response.status_code == 200
    assert me_response.json()["shift"] == "NIGHT"
    assert me_response.json()["unitId"] == "99"
