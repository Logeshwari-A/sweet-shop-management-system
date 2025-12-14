import pytest
import sys
import pathlib
from httpx import AsyncClient
import asyncio
import os

# Ensure backend package is importable when tests run from workspace root
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.main import app
from app.core import settings


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac


@pytest.fixture(autouse=True)
async def clear_db():
    # Ensure tests run against test DB; requires docker-compose mongo running
    from app.db import users_collection, sweets_collection
    await users_collection.delete_many({})
    await sweets_collection.delete_many({})
    yield
    await users_collection.delete_many({})
    await sweets_collection.delete_many({})
