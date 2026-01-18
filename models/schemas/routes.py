from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime

class RoutesModel(BaseModel): 
    route_id:Optional[str]=None
    routeName: str
    dairyId: str
    clients:Optional[List[str]]=[]
    createdDate: Optional[str]=None
    updatedDate: Optional[str]=None

class RoutesRequest(BaseModel):
    routeName: str
    dairyId: str
    clients:Optional[List[str]]=[]