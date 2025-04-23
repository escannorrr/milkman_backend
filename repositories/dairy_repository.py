from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime
from models.schemas.dairy import DairyModel
from db.database import get_database

class DairyRepository:
    def __init__(self):
        self.collection_name = "dairies"

    async def get_collection(self):
        db = await get_database()
        return db[self.collection_name]

    async def find_by_phone(self, phone_number: int):
        collection = await self.get_collection()
        return await collection.find_one({"phoneNumber": phone_number})

    async def find_by_dairy_name(self, dairy_name: str):
        collection = await self.get_collection()
        return await collection.find_one({"dairyName": dairy_name})

    async def create_dairy(self, dairy_data: dict):
        collection = await self.get_collection()
        result = await collection.insert_one(dairy_data)
        dairy_data["_id"] = str(result.inserted_id)
        return dairy_data

    async def update_dairy(self, dairy_id: str, update_data: dict):
        collection = await self.get_collection()
        await collection.update_one(
            {"_id": ObjectId(dairy_id)},
            {"$set": update_data}
        )

dairy_repository = DairyRepository()