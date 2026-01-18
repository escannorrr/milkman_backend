from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from models.schemas.salary import SalaryRecord, PaymentStatus
from db.database import get_database

class SalaryRepository:
    def __init__(self):
        self.collection_name = "salaries"

    async def get_collection(self):
        db = await get_database()
        return db[self.collection_name]

    async def create_salary(self, salary_data: dict):
        collection = await self.get_collection()
        result = await collection.insert_one(salary_data)
        salary_data["_id"] = str(result.inserted_id)
        return salary_data

    async def get_by_milkman(self, milkman_id: str):
        collection = await self.get_collection()
        cursor = collection.find({"milkmanId": milkman_id}).sort("month", -1)
        salaries = []
        async for doc in cursor:
            doc["salary_id"] = str(doc["_id"])
            salaries.append(SalaryRecord(**doc))
        return salaries

    async def get_by_id(self, salary_id: str):
        collection = await self.get_collection()
        try:
             return await collection.find_one({"_id": ObjectId(salary_id)})
        except:
             return None

    async def update_status(self, salary_id: str, status: str, paid_date: str):
        collection = await self.get_collection()
        await collection.update_one(
            {"_id": ObjectId(salary_id)},
            {"$set": {"status": status, "paidDate": paid_date}}
        )

salary_repository = SalaryRepository()
