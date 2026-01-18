from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime
from models.schemas.milkman import MilkmanModel
from db.database import get_database
from fastapi.encoders import jsonable_encoder
import logging

class MilkmanRepository:
    def __init__(self):
        self.collection_name = "milkman"

    logging.basicConfig(level=logging.INFO)

    async def get_collection(self):
        db = await get_database()
        return db[self.collection_name]

    async def find_by_adhaar(self, adhaar_number: int):
        collection = await self.get_collection()
        return await collection.find_one({"adhaarNo": adhaar_number})

    async def find_by_milkman_name(self, milkman_name: str):
        collection = await self.get_collection()
        return await collection.find_one({"milkmanName": milkman_name})

    async def create_milkman(self, milkman_data: dict):
        collection = await self.get_collection()
        result = await collection.insert_one(milkman_data)
        milkman_data["_id"] = str(result.inserted_id)
        return milkman_data

    async def find_by_phone(self, phone_number: int):
        collection = await self.get_collection()
        milkman = await collection.find_one({"phoneNumber": phone_number})
        logging.info("found Milkman: %s", phone_number)
        return await collection.find_one({"phoneNumber": phone_number})

    async def update_milkman(self, milkman_id: str, update_data: dict):
        collection = await self.get_collection()
        await collection.update_one(
            {"_id": ObjectId(milkman_id)},
            {"$set": update_data}
        )
        
    async def add_route_to_milkman(self, milkman_id: str, route_id: str):
        collection = await self.get_collection()
        await collection.update_one(
            {"_id": ObjectId(milkman_id)},
            {"$addToSet": {"routeIdList": route_id}}
        )
    
    async def get_all_milkmens(self, dairy_id: str):
        collection = await self.get_collection()
        cursor = collection.find({"dairyId": dairy_id})
        milkmen = []
        async for document in cursor:
            document["_id"] = str(document["_id"])
            document.pop("password", None)
            document.pop("isNew", None)
            milkman = MilkmanModel(**document)
            milkmen.append(milkman)
        
        return milkmen

milkman_repository = MilkmanRepository()