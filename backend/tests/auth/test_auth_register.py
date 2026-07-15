from sqlalchemy import select

from db.models import User
from services.auth.passwords import verify_password


def test_register_success(client):
    email = 'test@test.com'
    resp = client.post('/auth/register', json={'email': email, 'password': 'testtest'})

    assert resp.status_code == 201
    assert resp.json()['email'] == email

def test_register_does_not_leak_password(client):
    email = 'test@test.com'
    resp = client.post('/auth/register', json={'email': email, 'password': 'testtest'})
    body = resp.json()

    assert "password" not in body
    assert "hashed_password" not in body

def test_register_hashes_password(client, db):
    email = 'test@test.com'
    client.post('/auth/register', json={'email': email, 'password': 'testtest'})
    user = db.execute(select(User).where(User.email == email)).scalar_one()

    assert user.hashed_password != "testtest"
    assert verify_password("testtest", user.hashed_password) is True

def test_register_duplicate_email(client, user):
    resp = client.post('/auth/register', json={'email': user.email, 'password': 'testtest'})

    assert resp.status_code == 409

def test_register_normalizes_email(client):
    email = ' Test@Test.Com '
    resp = client.post('/auth/register', json={'email': email, 'password': 'testtest'})

    assert resp.json()['email'] == 'test@test.com'

def test_register_password_too_long(client):
    resp = client.post('/auth/register', json={'email': 'test@test.com', 'password': "x" * 73})

    assert resp.status_code == 422

def test_register_password_too_short(client):
    resp = client.post('/auth/register', json={'email': 'test@test.com', 'password': "x" * 7})

    assert resp.status_code == 422

def test_register_invalid_email(client):
    resp = client.post('/auth/register', json={'email': 'testtest.com', 'password': "x" * 8})

    assert resp.status_code == 422


