from motor.motor_asyncio import AsyncIOMotorClient

from .settings import settings

# Initialize MongoDB client and database
client = AsyncIOMotorClient(settings.DATABASE_URI)
db = client["survey_app"]


def get_collection(collection_name: str):
    return db[collection_name]
