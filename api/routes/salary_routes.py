from fastapi import APIRouter
from models.schemas.salary import SalaryPreviewRequest, SalaryPayRequest
from services.salary_service import salary_service

router = APIRouter()

@router.post("/calculate")
async def calculate_salary(req: SalaryPreviewRequest):
    return await salary_service.generate_salary_record(req.milkmanId, req.month)

@router.get("/history/{milkman_id}")
async def get_history(milkman_id: str):
    return await salary_service.get_history(milkman_id)

@router.put("/pay/{id}")
async def pay_salary(id: str):
    return await salary_service.pay_salary(id)

@router.get("/slip/{id}")
async def download_slip(id: str):
    return await salary_service.download_slip(id)
