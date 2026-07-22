from core.auth_deps import SESSION_COOKIE_NAME


def test_login_success(client, user):
    resp = client.post(
        "/auth/login", json={"email": user.email, "password": "testtest"}
    )

    assert resp.status_code == 200
    assert resp.json()["email"] == user.email
    assert SESSION_COOKIE_NAME in resp.cookies


def test_login_sets_working_cookie(client, user):
    login = client.post(
        "/auth/login", json={"email": user.email, "password": "testtest"}
    )

    assert login.status_code == 200

    me = client.get("/auth/me")

    assert me.status_code == 200
    assert me.json()["email"] == user.email


def test_login_wrong_password(client, user):
    resp = client.post("/auth/login", json={"email": user.email, "password": "wrong"})

    assert resp.status_code == 401


def test_login_unknown_email(client):
    resp = client.post(
        "/auth/login", json={"email": "unknown@test.com", "password": "testtest"}
    )

    assert resp.status_code == 401


def test_login_normalizes_email(client, user):
    resp = client.post(
        "/auth/login", json={"email": " Test@example.Com ", "password": "testtest"}
    )

    assert resp.json()["email"] == "test@example.com"
