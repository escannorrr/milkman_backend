from fastapi import APIRouter, Depends, Request,Query
from models.schemas.milkman import MilkmanModel
from services.milkman_service import milkman_service
from utils.jwt_token import verify_token

router = APIRouter() 

@router.post("/create_milkman")
async def create_milkman(milkMan: MilkmanModel):  
    return await milkman_service.create_milkman(milkMan)

@router.get("/get_all_milkman")
async def get_all_milkman(dairyId: str = Query(...)):
    return await milkman_service.get_all_milkmens(dairyId)