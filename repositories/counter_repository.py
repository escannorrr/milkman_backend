from motor.motor_asyncio import AsyncIOMotorClient
from db.database import get_database
from enum import Enum

class CounterType(Enum):
    DAIRY = "dairy_id"
    MILKMAN = "milkman_id"
    ROUTE = "route_id"

class CounterRepository:
    def __init__(self):
        self.collection_name = "counters"
        self.INITIAL_IDS = {
            CounterType.DAIRY: 10000,
            CounterType.MILKMAN: 10000,
            CounterType.ROUTE: 10000
        }

    async def get_collection(self):
        db = await get_database()
        return db[self.collection_name]

    async def get_next_id(self, counter_type: CounterType):
        collection = await self.get_collection()
        initial_value = self.INITIAL_IDS[counter_type]
        
        # First, try to find the existing counter
        counter = await collection.find_one_and_update(
            {"_id": counter_type.value},
            {"$inc": {"sequence_value": 1}},
            upsert=True,
            return_document=True
        )

        # If this is the first entry or sequence_value is less than initial value
        if not counter or counter.get("sequence_value", 0) < initial_value:
            # Reset to initial value
            await collection.find_one_and_update(
                {"_id": counter_type.value},
                {"$set": {"sequence_value": initial_value}},
                upsert=True
            )
            return initial_value

        return counter["sequence_value"]

    async def get_next_dairy_id(self):
        return await self.get_next_id(CounterType.DAIRY)

    async def get_next_milkman_id(self):
        return await self.get_next_id(CounterType.MILKMAN)

    async def get_next_route_id(self):
        return await self.get_next_id(CounterType.ROUTE)

counter_repository = CounterRepository() 