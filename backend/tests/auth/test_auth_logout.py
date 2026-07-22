def test_logout_clears_session(auth_client):
    logout = auth_client.post("/auth/logout")

    assert logout.status_code == 204

    me = auth_client.get("/auth/me")

    assert me.status_code == 401


def test_logout_without_cookie(client):
    resp = client.post("/auth/logout")

    assert resp.status_code == 204
