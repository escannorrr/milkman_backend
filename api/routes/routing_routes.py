from fastapi import HTTPException, BackgroundTasks
import random
import string
from datetime import datetime
from models.schemas.routes import RoutesModel, MilkmanRequest
from repositories.routes_repository import routes_repository
from repositories.counter_repository import counter_repository
from utils.jwt_token import verify_token
from services.routes_service import routes_service

router = APIRouter() 

@router.post("/create_route")
async def create_milkman(route: MilkmanRequest):  
    return await routes_service.create_route(route)

