from fastapi import APIRouter
from models.schemas.customer import CustomerRequest, BillRequest
from services.customer_service import customer_service

router = APIRouter()

@router.post("/create")
async def create_customer(customer: CustomerRequest):
    return await customer_service.create_customer(customer)

@router.get("/all/{dairy_id}")
async def get_all_customers(dairy_id: str):
    return await customer_service.get_by_dairy(dairy_id)

@router.post("/generate-bill")
async def generate_bill(request: BillRequest):
    return await customer_service.generate_bill_pdf(request)
