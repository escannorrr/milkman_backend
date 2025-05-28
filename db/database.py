from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings
import asyncio

class Database:
    client: AsyncIOMotorClient = None
    db = None

db = Database()

async def get_database():
    if db.db is None:
        db.db = db.client[settings.DATABASE_NAME]
    return db.db

async def connect_to_mongo():
    """Create database connection and test it"""
    try:
        db.client = AsyncIOMotorClient(settings.MONGODB_URL)
        # Test the connection
        await db.client.admin.command('ping')
        print(f"Connected to MongoDB at {settings.MONGODB_URL}")
        print(f"Using database: {settings.DATABASE_NAME}")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise e
    
async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        print("Disconnected from MongoDB")