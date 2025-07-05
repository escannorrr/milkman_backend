from fastapi import HTTPException, BackgroundTasks
import random
import string
from datetime import datetime
from models.schemas.milkman import MilkmanModel, MilkmanRequest, MilkmanResponse
from repositories.milkman_repository import milkman_repository
from repositories.counter_repository import counter_repository
from utils.jwt_token import create_access_token, verify_token
from utils.send_email import SendEmail
from utils.jwt_token import verify_token
from models.schemas.user import LoginModel
from utils.encryption import Encrypt

class MilkmanService: 
    def __init__(self):
        self.repository = milkman_repository
        self.counter_repository = counter_repository

    async def create_milkman(self, milkman: MilkmanRequest,background_tasks: BackgroundTasks):
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
        encryptedPassword = Encrypt.encrypt(temp_password)
        current_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        milkman_obj = MilkmanModel(
            milkmanName=milkman.milkmanName,
            dairyId=milkman.dairyId,
            phoneNumber=milkman.phoneNumber,
            password=encryptedPassword,
            isNew=True,
            milkman_id=milkman_id,
            email=milkman.email,
            adhaarNo=milkman.adhaarNo,
            dl_number=milkman.dl_number,
            routeIdList=milkman.routeIdList,
            createdDate=current_time,
            updatedDate=current_time,
        )

        await SendEmail.send_temp_password_email(
            background_tasks=background_tasks,
            email=milkman_obj.email,
            owner_name=milkman_obj.milkmanName,
            temp_password=temp_password
        )

        # Save dairy
        milkman_dict = milkman_obj.dict()
        result = await self.repository.create_milkman(milkman_dict)
        return result
    
    async def get_all_milkmens(self, token:str):
        phone_number = verify_token(token)
        dairy = await self.repository.find_by_phone(int(phone_number))
        result = await self.repository.get_all_milkmens(dairy_id=dairy.dairy_id)
        return {
            "milkMan": result
        }

    async def milkmanLogin(self, details:LoginModel):
        milkman = await self.repository.find_by_phone(details.phoneNumber)
        if not milkman:
            raise HTTPException(status_code=401, detail="Phone number does not exist")

        milkman_data = MilkmanModel(**milkman)
        if details.password != milkman_data.password:
            raise HTTPException(status_code=401, detail="Invalid password/phone number")

        access_token = create_access_token({"sub": str(milkman_data.phoneNumber),"auth_roles":["milkman"]})
        milkmanRes = MilkmanResponse(**milkman_data.dict())
        milkmanRes.message = 'Milkman logged in Successfully'
        milkmanRes.accessToken = access_token
        return milkmanRes
    
    
    
milkman_service = MilkmanService()