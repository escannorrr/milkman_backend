from typing import List, Optional
from pydantic import BaseModel

class signUpRequestModel(BaseModel):
    dairyName : str
    ownerName : str
    phoneNumber : int
    