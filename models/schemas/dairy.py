from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SignUpRequestModel(BaseModel):
    dairyName: str
    ownerName: str
    phoneNumber: int
    email:str

class LoginModel(BaseModel):
    phoneNumber: int
    password: str

class ChangePasswordModel(BaseModel):
    oldPassword: str
    newPassword: str

class DairyModel(BaseModel): 
    dairyName: str
    ownerName: str
    phoneNumber: int
    password: str
    isNew: bool
    dairyId: str
    createdDate: str
    updatedDate: str 