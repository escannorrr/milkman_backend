from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from models.schemas.dashboard import NotificationModel
from db.database import get_database

class NotificationRepository:
    def __init__(self):
        self.collection_name = "notifications"

    async def get_collection(self):
        db = await get_database()
        return db[self.collection_name]

    async def create_notification(self, notification_data: dict):
        collection = await self.get_collection()
        result = await collection.insert_one(notification_data)
        notification_data["_id"] = str(result.inserted_id)
        return notification_data

    async def get_by_dairy(self, dairy_id: str, unread_only: bool = False):
        collection = await self.get_collection()
        query = {"dairyId": dairy_id}
        if unread_only:
            query["isRead"] = False
            
        cursor = collection.find(query).sort("createdDate", -1)
        notifications = []
        async for doc in cursor:
            doc["notification_id"] = str(doc["_id"])
            notifications.append(NotificationModel(**doc))
        return notifications

    async def mark_as_read(self, notification_id: str):
        collection = await self.get_collection()
        await collection.update_one(
            {"_id": ObjectId(notification_id)},
            {"$set": {"isRead": True}}
        )

    async def check_exists(self, dairy_id: str, title: str, start_date_str: str):
        # Check if similar notification exists roughly overlapping this period/month
        collection = await self.get_collection()
        # Simple check: same title and dairy within last 10 days
        # A robust way: store "month" field. stick to date string filter for now.
        return await collection.find_one({
            "dairyId": dairy_id,
            "title": title,
            "createdDate": {"$gte": start_date_str}
        })

notification_repository = NotificationRepository()
