from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings
import asyncio
import certifi

class Database:
    client: AsyncIOMotorClient = None
    db = None

db = Database()

async def get_database():
    if db.db is None:
        db.db = db.client[settings.DATABASE_NAME]
    return db.db

async def connect_to_mongo():
    try:
        db.client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            tls=True,
            tlsCAFile=certifi.where()
        )
        await db.client.admin.command('ping')
        print("✅ MongoDB connected.")
    except Exception as e:
        print("❌ MongoDB connection error:", e)
        raise e
    
async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        print("Disconnected from MongoDB")