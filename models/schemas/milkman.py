from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime

class MilkmanModel(BaseModel): 
    milkman_id:Optional[str]=None
    milkmanName: str
    dairyId: str
    routeIdList: Optional[List[str]]=[] 
    password: Optional[str]=None
    isNew: Optional[bool]=None
    phoneNumber:int
    adhaarNo:int
    dl_number:str
    createdDate: Optional[str]=None
    updatedDate: Optional[str]=None 