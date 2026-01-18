from pydantic import BaseModel
from typing import Optional, List, Any

class MilkmanModel(BaseModel): 
    milkman_id:Optional[str]=None
    milkmanName: str
    dairyId: str
    email: str
    routeIdList: Optional[List[str]]=[] 
    password: Optional[str]=None
    isNew: Optional[bool]=None
    phoneNumber:int
    adhaarNo:int
    dl_number:str
    baseSalary: float = 0.0 # New field
    createdDate: Optional[str]=None
    updatedDate: Optional[str]=None 

class MilkmanResponse(BaseModel):
    milkman_id:Optional[str]=None
    milkmanName: str
    dairyId: str
    email: str
    routeIdList: Optional[List[str]]=[]
    isNew: Optional[bool]=None
    phoneNumber:int
    adhaarNo:int
    dl_number:str
    baseSalary: float = 0.0
    message: Optional[str] = None
    accessToken: Optional[str] = None

class MilkmanRequest(BaseModel):
    milkmanName: str
    dairyId: str
    email: str
    routeIdList: Optional[List[str]]=[]
    phoneNumber:int
    adhaarNo:int
    dl_number:str
    baseSalary: float = 0.0 # New field