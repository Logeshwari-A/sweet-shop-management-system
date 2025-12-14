from motor.motor_asyncio import AsyncIOMotorClient
from .core import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client.get_default_database()

# collections
users_collection = db.get_collection("users")
sweets_collection = db.get_collection("sweets")
