from fastapi import APIRouter, Depends, Request, Query, BackgroundTasks
from models.schemas.milkman import MilkmanModel, MilkmanResponse, MilkmanRequest
from services.milkman_service import milkman_service
from models.schemas.user import LoginModel
from api.dependencies import get_current_milkman

router = APIRouter() 

@router.post("/create_milkman",response_model=MilkmanResponse)
async def create_milkman(milkMan: MilkmanRequest,background_tasks: BackgroundTasks):  
    return await milkman_service.create_milkman(milkMan,background_tasks)

@router.get("/get_all_milkman")
async def get_all_milkman(current_user: MilkmanModel = Depends(get_current_milkman)):
    return await milkman_service.get_all_milkmens(current_user.dairyId)

@router.post("/login",response_model=MilkmanResponse)
async def login(details: LoginModel):
    return await milkman_service.milkmanLogin(details)