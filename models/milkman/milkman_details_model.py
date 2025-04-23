from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class milkmanDetailsModel(BaseModel):
    milkmanId:str
    milkmanName:str
    phoneNumber:int
    address:str
    adhaarNumber:int
    dlNumber:str
    createdDate : datetime
    updatedDate : datetime