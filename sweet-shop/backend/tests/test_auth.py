import pytest

async def test_register_and_login(client):
    # Register
    r = await client.post('/api/auth/register', json={"username": "alice", "email": "alice@example.com", "password": "secret"})
    assert r.status_code == 200
    data = r.json()
    assert data['email'] == 'alice@example.com'

    # Duplicate
    r2 = await client.post('/api/auth/register', json={"username": "alice2", "email": "alice@example.com", "password": "secret"})
    assert r2.status_code == 400

    # Login
    r3 = await client.post('/api/auth/login', json={"username": "ignored", "email": "alice@example.com", "password": "secret"})
    assert r3.status_code == 200
    token = r3.json()
    assert 'access_token' in token

async def test_admin_registration(client):
    # register with wrong admin_secret -> not admin
    r = await client.post('/api/auth/register', json={"username": "bob", "email": "bob@example.com", "password": "pw", "admin_secret": "wrong"})
    assert r.status_code == 200
    assert r.json()['is_admin'] is False

    # register with correct admin secret
    from app.core import settings
    r2 = await client.post('/api/auth/register', json={"username": "admin", "email": "admin@example.com", "password": "pw", "admin_secret": settings.ADMIN_SECRET})
    assert r2.status_code == 200
    assert r2.json()['is_admin'] is True
