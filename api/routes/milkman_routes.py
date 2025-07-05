from fastapi import APIRouter, Depends, Request,Query,BackgroundTasks
from models.schemas.milkman import MilkmanModel, MilkmanResponse, MilkmanRequest
from services.milkman_service import milkman_service
from utils.jwt_token import verify_token
from models.schemas.user import LoginModel

router = APIRouter() 

@router.post("/create_milkman",response_model=MilkmanResponse)
async def create_milkman(milkMan: MilkmanRequest,background_tasks: BackgroundTasks):  
    return await milkman_service.create_milkman(milkMan,background_tasks)

@router.get("/get_all_milkman")
async def get_all_milkman(request: Request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    return await milkman_service.get_all_milkmens(token)

@router.post("/login",response_model=MilkmanResponse)
async def login(details: LoginModel):
    return await milkman_service.milkmanLogin(details)