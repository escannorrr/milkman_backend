from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class userModel(BaseModel):
    dairyId : str
    dairyName : str
    ownerName : str
    phoneNumber : int
    password : str
    isNew : bool
    createdDate : datetime
    updatedDate : datetime

class loginModel(BaseModel):
    phoneNumber : int
    password : str


class changePasswordModel(BaseModel):
    oldPassword : str
    newPassword : str