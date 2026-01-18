from fastapi import HTTPException, BackgroundTasks, APIRouter
import random
import string
from datetime import datetime
from models.schemas.routes import RoutesModel, RoutesRequest
from repositories.routes_repository import routes_repository
from repositories.counter_repository import counter_repository
from utils.jwt_token import verify_token
from services.route_service import routes_service

router = APIRouter() 

@router.post("/create_route")
async def create_milkman(route: RoutesRequest):
    return await routes_service.create_route(route)

