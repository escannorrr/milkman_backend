from datetime import datetime
from models.schemas.dashboard import DashboardStats, NotificationModel, NotificationType
from repositories.milkman_repository import milkman_repository
from repositories.routes_repository import routes_repository
from repositories.customer_repository import customer_repository
from repositories.notification_repository import notification_repository

class DashboardService:
    def __init__(self):
        self.milkman_repo = milkman_repository
        self.routes_repo = routes_repository
        self.customer_repo = customer_repository
        self.notification_repo = notification_repository

    async def get_stats(self, dairy_id: str) -> DashboardStats:
        # 1. Check Alerts first
        await self.check_monthly_alerts(dairy_id)

        # 2. Aggregate Data
        # Note: Repositories currently implement "find" logic which returns lists. 
        # Ideally, we should add "count" methods to repositories for performance.
        # For now, I'll fetch lists and count.
        
        milkmens = await self.milkman_repo.get_all_milkmens(dairy_id)
        routes = await self.routes_repo.find_by_dairy(dairy_id)
        customers = await self.customer_repo.find_by_dairy(dairy_id)
        
        total_milk = sum(c.dailyQuantity for c in customers)
        # Revenue projection: Daily Total * 30
        daily_revenue = sum(c.dailyQuantity * c.pricePerLiter for c in customers)
        projected_revenue = daily_revenue * 30
        
        notifications = await self.notification_repo.get_by_dairy(dairy_id, unread_only=True)

        return DashboardStats(
            totalCustomers=len(customers),
            totalMilkmen=len(milkmens),
            totalRoutes=len(routes),
            totalDailyMilk=total_milk,
            projectedMonthlyRevenue=projected_revenue,
            activeNotifications=len(notifications)
        )

    async def check_monthly_alerts(self, dairy_id: str):
        # Alert if date is between 1st and 5th of the month
        today = datetime.now()
        if 1 <= today.day <= 5:
            start_of_month = datetime(today.year, today.month, 1).isoformat()
            
            # Check Salary Alert
            exists = await self.notification_repo.check_exists(dairy_id, "Monthly Salary Calculation", start_of_month)
            if not exists:
                await self.notification_repo.create_notification({
                    "dairyId": dairy_id,
                    "title": "Monthly Salary Calculation",
                    "message": "It's the start of the month. Please calculate salaries for your milkmen.",
                    "type": NotificationType.SALARY,
                    "isRead": False,
                    "createdDate": datetime.utcnow().isoformat()
                })

            # Check Bill Alert
            exists_bill = await self.notification_repo.check_exists(dairy_id, "Generate Monthly Bills", start_of_month)
            if not exists_bill:
                await self.notification_repo.create_notification({
                    "dairyId": dairy_id,
                    "title": "Generate Monthly Bills",
                    "message": "New month started. Time to generate bills for customers.",
                    "type": NotificationType.BILLING,
                    "isRead": False,
                    "createdDate": datetime.utcnow().isoformat()
                })

    async def get_notifications(self, dairy_id: str):
        return await self.notification_repo.get_by_dairy(dairy_id)

    async def mark_notification_read(self, n_id: str):
        await self.notification_repo.mark_as_read(n_id)
        return {"message": "Marked as read"}

dashboard_service = DashboardService()
