from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime
from models.schemas.user import UserModel
from db.database import get_database

class UserRepository:
    def __init__(self):
        self.collection_name = "users"

    async def get_collection(self):
        db = await get_database()
        return db[self.collection_name]

    async def find_by_phone(self, phone_number: int):
        collection = await self.get_collection()
        return await collection.find_one({"phoneNumber": phone_number})

    async def find_by_dairy_name(self, dairy_name: str):
        collection = await self.get_collection()
        return await collection.find_one({"dairyName": dairy_name})

    async def create_user(self, user_data: dict):
        collection = await self.get_collection()
        result = await collection.insert_one(user_data)
        user_data["_id"] = str(result.inserted_id)
        return user_data

    async def update_user(self, user_id: str, update_data: dict):
        collection = await self.get_collection()
        await collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )

user_repository = UserRepository() 