def test_me_returns_logged_in_user(auth_client, user):
    resp = auth_client.get('/auth/me')

    assert resp.status_code == 200
    assert resp.json()["email"] == user.email

def test_me_without_session_is_unauthorized(client):
    resp = client.get('/auth/me')

    assert resp.status_code == 401