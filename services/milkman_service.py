from fastapi import HTTPException
import random
import string
from datetime import datetime
from models.schemas.milkman import MilkmanModel
from repositories.milkman_repository import milkman_repository
from repositories.counter_repository import counter_repository
from utils.jwt_token import create_access_token, verify_token

class MilkmanService: 
    def __init__(self):
        self.repository = milkman_repository
        self.counter_repository = counter_repository

    async def create_milkman(self, milkman: MilkmanModel):
        # Check if milkman already exists
        existing_milkman = await self.repository.find_by_adhaar(milkman.adhaarNo)
        if existing_milkman:
            raise HTTPException(status_code=400, detail="Adhaar is already exists")

        # Generate temporary password
        temp_password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

        # Get next dairy ID
        next_id = await self.counter_repository.get_next_milkman_id()
        
        # Generate dairy ID with initials and sequential number
        milkman_initials = milkman.milkmanName[:2].upper() if milkman.milkmanName else "XX"
        adhaar_digits = (str(milkman.adhaarNo)[-4:] if milkman.adhaarNo else "XXXX")
        milkman_id = f"{milkman_initials}{adhaar_digits}{next_id}"

        # Create dairy object
        current_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        milkman_obj = MilkmanModel(
            milkmanName=milkman.milkmanName,
            dairyId=milkman.dairyId,
            phoneNumber=milkman.phoneNumber,
            password=temp_password,
            isNew=True,
            milkman_id=milkman_id,
            adhaarNo=milkman.adhaarNo,
            dl_number=milkman.dl_number,
            routeIdList=milkman.routeIdList,
            createdDate=current_time,
            updatedDate=current_time,
        )

        # Save dairy
        milkman_dict = milkman_obj.dict()
        result = await self.repository.create_milkman(milkman_dict)
        return {
            "message": milkman_id + ": Milkman created Successfully",
            "milkman": result
        }
    
    async def get_all_milkmens(self,dairy_id:str):
        result = await self.repository.get_all_milkmens(dairy_id=dairy_id)
        return {
            "milkMan": result
        }
    
    
    
milkman_service = MilkmanService()