from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime
from models.schemas.routes import RoutesModel
from db.database import get_database

class RoutesRepository:
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
        
    async def find_by_id(self, route_id: str):
        collection = await self.get_collection()
        # Handle string vs ObjectId conversion if needed, assuming service passes valid ID
        try:
             return await collection.find_one({"_id": ObjectId(route_id)})
        except:
             return None

    async def find_by_dairy(self, dairy_id: str):
        collection = await self.get_collection()
        cursor = collection.find({"dairyId": dairy_id})
        routes = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            routes.append(RoutesModel(**doc))
        return routes

    async def delete_route(self, route_id: str):
        collection = await self.get_collection()
        return await collection.delete_one({"_id": ObjectId(route_id)})

    async def add_clients(self, route_id: str, client_ids: list):
        collection = await self.get_collection()
        await collection.update_one(
            {"_id": ObjectId(route_id)},
            {"$addToSet": {"clients": {"$each": client_ids}}}
        )


routes_repository = RoutesRepository()