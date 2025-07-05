from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime
from models.schemas.routes import RoutesModel
from db.database import get_database

class DairyRepository:
    def __init__(self):
        self.collection_name = "routes"

    async def get_collection(self):
        db = await get_database()
        return db[self.collection_name]

    async def create_route(self, route_data: dict):
        collection = await self.get_collection()
        result = await collection.insert_one(route_data)
        route_data["_id"] = str(result.inserted_id)
        return route_data

    async def update_route(self, route_id: str, update_data: dict):
        collection = await self.get_collection()
        await collection.update_one(
            {"_id": ObjectId(route_id)},
            {"$set": update_data}
        )