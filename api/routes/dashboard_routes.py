from fastapi import APIRouter
from services.dashboard_service import dashboard_service

router = APIRouter()

@router.get("/stats/{dairy_id}")
async def get_stats(dairy_id: str):
    return await dashboard_service.get_stats(dairy_id)

@router.get("/notifications/{dairy_id}")
async def get_notifications(dairy_id: str):
    return await dashboard_service.get_notifications(dairy_id)

@router.put("/notifications/{id}/read")
async def mark_read(id: str):
    return await dashboard_service.mark_notification_read(id)
