from fastapi import HTTPException
import random
import string
from datetime import datetime
from models.schemas.dairy import DairyModel, SignUpRequestModel, LoginModel, ChangePasswordModel
from repositories.dairy_repository import dairy_repository
from repositories.counter_repository import counter_repository
from utils.jwt_token import create_access_token, verify_token

class DairyService:  # Changed from UserService to DairyService
    def __init__(self):
        self.repository = dairy_repository
        self.counter_repository = counter_repository

    async def create_dairy(self, dairy: SignUpRequestModel):  # Changed from create_user to create_dairy
        # Check if dairy already exists
        existing_dairy = await self.repository.find_by_dairy_name(dairy.dairyName)
        if existing_dairy:
            raise HTTPException(status_code=400, detail="Dairy with this name already exists")

        # Generate temporary password
        temp_password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

        # Get next dairy ID
        next_id = await self.counter_repository.get_next_dairy_id()
        
        # Generate dairy ID with initials and sequential number
        dairy_initials = dairy.dairyName[:2].upper() if dairy.dairyName else "XX"
        owner_initials = dairy.ownerName[:2].upper() if dairy.ownerName else "XX"
        dairy_id = f"{dairy_initials}{owner_initials}{next_id}"

        # Create dairy object
        current_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        dairy_obj = DairyModel(
            dairyName=dairy.dairyName,
            ownerName=dairy.ownerName,
            phoneNumber=dairy.phoneNumber,
            password=temp_password,
            isNew=True,
            dairyId=dairy_id,
            createdDate=current_time,
            updatedDate=current_time,
        )

        # Save dairy
        dairy_dict = dairy_obj.dict()
        result = await self.repository.create_dairy(dairy_dict)
        return {
            "message": "Dairy created Successfully",
            "dairy": result
        }

    async def login(self, details: LoginModel):
        dairy = await self.repository.find_by_phone(details.phoneNumber)
        if not dairy:
            raise HTTPException(status_code=401, detail="Phone number does not exist")

        dairy_data = DairyModel(**dairy)
        if details.password != dairy_data.password:
            raise HTTPException(status_code=401, detail="Invalid password/phone number")

        access_token = create_access_token({"sub": str(dairy_data.phoneNumber)})
        return {
            "message": "Dairy logged in Successfully",
            "accessToken": access_token,
            "isNew": dairy_data.isNew
        }

    async def change_password(self, passwords: ChangePasswordModel, token: str):
        # Verify token and get dairy
        phone_number = verify_token(token)
        dairy = await self.repository.find_by_phone(int(phone_number))
        if not dairy:
            raise HTTPException(status_code=404, detail="Dairy not found")

        dairy_data = DairyModel(**dairy)
        if passwords.oldPassword != dairy_data.password:
            return {"message": "Invalid old password"}

        # Update password
        current_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        update_data = {
            "password": passwords.newPassword,
            "isNew": False,
            "updatedDate": current_time
        }
        await self.repository.update_dairy(str(dairy["_id"]), update_data)
        return {"message": "Password updated successfully"}

dairy_service = DairyService()  # Changed from user_service to dairy_service 