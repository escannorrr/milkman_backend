from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CustomerModel(BaseModel):
    customer_id: Optional[str] = None
    customerName: str
    dairyId: str
    routeId: Optional[str] = None
    address: Optional[str] = None
    phoneNumber: int
    dailyQuantity: float # Liters
    pricePerLiter: float
    createdDate: Optional[str] = None
    updatedDate: Optional[str] = None

class CustomerRequest(BaseModel):
    customerName: str
    dairyId: str
    routeId: Optional[str] = None
    address: Optional[str] = None
    phoneNumber: int
    dailyQuantity: float
    pricePerLiter: float

class BillRequest(BaseModel):
    customerId: str
    startDate: str # YYYY-MM-DD
    endDate: str # YYYY-MM-DD
