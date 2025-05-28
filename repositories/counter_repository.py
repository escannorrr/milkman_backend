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

        counter = await collection.find_one({"_id": counter_type.value})

        if not counter:
            await collection.insert_one({
               "_id": counter_type.value,
              "sequence_value": initial_value
            })
            return initial_value

        updated_counter = await collection.find_one_and_update(
            {"_id": counter_type.value},
            {"$inc": {"sequence_value": 1}},
            return_document=True
        )
        return updated_counter["sequence_value"]

    async def get_next_dairy_id(self):
        return await self.get_next_id(CounterType.DAIRY)

    async def get_next_milkman_id(self):
        return await self.get_next_id(CounterType.MILKMAN)

    async def get_next_route_id(self):
        return await self.get_next_id(CounterType.ROUTE)

counter_repository = CounterRepository() 