from fastapi import HTTPException
from datetime import datetime
from models.schemas.routes import RoutesModel, RoutesRequest
from repositories.routes_repository import routes_repository
from repositories.counter_repository import counter_repository
from utils.jwt_token import verify_token

class MilkmanService: 
    def __init__(self):
        self.repository = routes_repository
        self.counter_repository = counter_repository

    async def create_route(self, milkman: MilkmanRequest):
         next_id = await self.counter_repository.get_next_route_id()
         
