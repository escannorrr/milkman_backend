from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    BILLING = "BILLING"
    SALARY = "SALARY"
    SYSTEM = "SYSTEM"

class NotificationModel(BaseModel):
    notification_id: Optional[str] = None
    dairyId: str
    title: str
    message: str
    type: NotificationType
    isRead: bool = False
    createdDate: str

class DashboardStats(BaseModel):
    totalCustomers: int
    totalMilkmen: int
    totalRoutes: int
    totalDailyMilk: float
    projectedMonthlyRevenue: float
    activeNotifications: int
