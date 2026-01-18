from pydantic import BaseModel
from typing import Optional
from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"

class SalaryRecord(BaseModel):
    salary_id: Optional[str] = None
    milkmanId: str
    dairyId: str
    month: str # YYYY-MM
    amount: float
    status: PaymentStatus = PaymentStatus.PENDING
    generatedDate: str
    paidDate: Optional[str] = None

class SalaryPreviewRequest(BaseModel):
    milkmanId: str
    month: str # YYYY-MM

class SalaryPayRequest(BaseModel):
    salaryId: str
