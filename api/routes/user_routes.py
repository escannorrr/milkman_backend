from fastapi import APIRouter, Depends, Request
from models.schemas.user import SignUpRequestModel, LoginModel, ChangePasswordModel
from services.user_service import user_service
from utils.jwt_token import verify_token

router = APIRouter(tags=["users"])

@router.post("/signup")
async def signup(user: SignUpRequestModel):
    return await user_service.create_user(user)

@router.post("/login")
async def login(details: LoginModel):
    return await user_service.login(details)

@router.post("/change-password")
async def change_password(passwords: ChangePasswordModel, request: Request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    return await user_service.change_password(passwords, token) 