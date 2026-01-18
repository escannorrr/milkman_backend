from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from models.schemas.customer import CustomerModel
from db.database import get_database

class CustomerRepository:
    def __init__(self):
        self.collection_name = "customers"

    async def get_collection(self):
        db = await get_database()
        return db[self.collection_name]

    async def create_customer(self, customer_data: dict):
        collection = await self.get_collection()
        result = await collection.insert_one(customer_data)
        customer_data["_id"] = str(result.inserted_id)
        return customer_data

    async def find_by_dairy(self, dairy_id: str):
        collection = await self.get_collection()
        cursor = collection.find({"dairyId": dairy_id})
        customers = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            customers.append(CustomerModel(**doc))
        return customers

    async def find_by_id(self, customer_id: str):
        collection = await self.get_collection()
        try:
            return await collection.find_one({"_id": ObjectId(customer_id)})
        except:
             return None

    async def update_customer(self, customer_id: str, update_data: dict):
        collection = await self.get_collection()
        await collection.update_one(
            {"_id": ObjectId(customer_id)},
            {"$set": update_data}
        )

customer_repository = CustomerRepository()
