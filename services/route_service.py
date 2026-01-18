from fastapi import HTTPException
from datetime import datetime
from models.schemas.routes import RoutesModel, RoutesRequest, RouteUpdateModel
from repositories.routes_repository import routes_repository
from repositories.counter_repository import counter_repository
from repositories.milkman_repository import milkman_repository

class RoutesService:
    def __init__(self):
        self.repository = routes_repository
        self.counter_repository = counter_repository
        self.milkman_repository = milkman_repository

    async def create_route(self, route: RoutesRequest):
         # Create route logic
         route_data = RoutesModel(
             routeName=route.routeName,
             dairyId=route.dairyId,
             clients=route.clients,
             createdDate=datetime.utcnow().isoformat(),
             updatedDate=datetime.utcnow().isoformat()
         )
         result = await self.repository.create_route(route_data.dict())
         return result

    async def get_all_routes(self, dairy_id: str):
        return await self.repository.find_by_dairy(dairy_id)

    async def update_route(self, route_id: str, update_data: RouteUpdateModel):
        existing = await self.repository.find_by_id(route_id)
        if not existing:
             raise HTTPException(status_code=404, detail="Route not found")
        
        data = update_data.dict(exclude_unset=True)
        if not data:
             return existing
             
        data["updatedDate"] = datetime.utcnow().isoformat()
        await self.repository.update_route(route_id, data)
        return await self.repository.find_by_id(route_id)
        
    async def delete_route(self, route_id: str):
        result = await self.repository.delete_route(route_id)
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Route not found")
        return {"message": "Route deleted successfully"}

    async def assign_milkman(self, route_id: str, milkman_id: str):
        route = await self.repository.find_by_id(route_id)
        if not route:
            raise HTTPException(status_code=404, detail="Route not found")
            
        # Update milkman
        await self.milkman_repository.add_route_to_milkman(milkman_id, route_id)
        return {"message": "Milkman assigned to route successfully"}

    async def add_customers(self, route_id: str, client_ids: list):
        route = await self.repository.find_by_id(route_id)
        if not route:
            raise HTTPException(status_code=404, detail="Route not found")
            
        await self.repository.add_clients(route_id, client_ids)
        return {"message": "Customers added to route successfully"}

routes_service = RoutesService()