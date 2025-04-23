from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

db = Database()

async def get_database():
    if db.db is None:
        db.db = db.client[settings.DATABASE_NAME]
    return db.db

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    
async def close_mongo_connection():
    if db.client:
        db.client.close() 