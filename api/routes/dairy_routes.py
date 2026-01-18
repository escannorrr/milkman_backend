from fastapi import APIRouter, Depends, Request,BackgroundTasks
from models.schemas.dairy import SignUpRequestModel, LoginModel, ChangePasswordModel
from services.dairy_service import dairy_service
from utils.jwt_token import verify_token

router = APIRouter() 

@router.post("/signup")
async def signup(dairy: SignUpRequestModel,background_tasks: BackgroundTasks):  
    return await dairy_service.create_dairy(dairy,background_tasks)

@router.post("/login")
async def login(details: LoginModel):
    return await dairy_service.login(details)

@router.post("/change-password")
async def change_password(passwords: ChangePasswordModel, request: Request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    return await dairy_service.change_password(passwords, token) 