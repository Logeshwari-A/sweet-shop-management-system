import pytest

async def get_token(client, email="user@example.com", password="pw", admin_secret=None):
    await client.post('/api/auth/register', json={"username": "user", "email": email, "password": password, "admin_secret": admin_secret})
    r = await client.post('/api/auth/login', json={"username": "x", "email": email, "password": password})
    return r.json()['access_token']

async def test_add_get_sweets_requires_auth(client):
    r = await client.post('/api/sweets', json={"name": "Toffee", "category": "Candy", "price": 1.5, "quantity": 10})
    assert r.status_code == 401

async def test_add_and_list_sweets(client):
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    r = await client.post('/api/sweets', headers=headers, json={"name": "Toffee", "category": "Candy", "price": 1.5, "quantity": 10})
    assert r.status_code == 200
    sweet = r.json()
    assert sweet['name'] == 'Toffee'

    r2 = await client.get('/api/sweets', headers=headers)
    assert r2.status_code == 200
    assert len(r2.json()) == 1

async def test_search_and_purchase_and_restock(client):
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    # add two sweets
    await client.post('/api/sweets', headers=headers, json={"name": "Toffee", "category": "Candy", "price": 1.5, "quantity": 10})
    await client.post('/api/sweets', headers=headers, json={"name": "Caramel", "category": "Candy", "price": 2.0, "quantity": 5})

    # search by name
    r = await client.get('/api/sweets/search?name=Toff', headers=headers)
    assert r.status_code == 200
    assert len(r.json()) == 1

    # purchase
    sweets = (await client.get('/api/sweets', headers=headers)).json()
    sid = sweets[0]['id']
    r2 = await client.post(f'/api/sweets/{sid}/purchase', headers=headers, json={"amount": 2})
    assert r2.status_code == 200
    assert r2.json()['quantity'] == sweets[0]['quantity'] - 2

    # restock as non-admin should fail
    r3 = await client.post(f'/api/sweets/{sid}/restock', headers=headers, json={"amount": 5})
    assert r3.status_code == 403

    # create admin and restock
    from app.core import settings
    admin_token = await get_token(client, email='admin@example.com', password='pw', admin_secret=settings.ADMIN_SECRET)
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    r4 = await client.post(f'/api/sweets/{sid}/restock', headers=admin_headers, json={"amount": 5})
    assert r4.status_code == 200
    # now quantity increased
    assert r4.json()['quantity'] == sweets[0]['quantity'] - 2 + 5

async def test_delete_requires_admin(client):
    token = await get_token(client)
    headers = {"Authorization": f"Bearer {token}"}
    r = await client.post('/api/sweets', headers=headers, json={"name": "Gum", "category": "Gum", "price": 0.5, "quantity": 3})
    sid = r.json()['id']
    r2 = await client.delete(f'/api/sweets/{sid}', headers=headers)
    assert r2.status_code == 403
    # admin delete
    from app.core import settings
    admin_token = await get_token(client, email='root@example.com', password='pw', admin_secret=settings.ADMIN_SECRET)
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    r3 = await client.delete(f'/api/sweets/{sid}', headers=admin_headers)
    assert r3.status_code == 200
    assert r3.json()['deleted'] is True
