from fastapi import HTTPException
import random
import string
from datetime import datetime
from models.schemas.user import UserModel, SignUpRequestModel, LoginModel, ChangePasswordModel
from repositories.user_repository import user_repository
from utils.jwt_token import create_access_token, verify_token

class UserService:
    def __init__(self):
        self.repository = user_repository

    async def create_user(self, user: SignUpRequestModel):
        # Check if dairy already exists
        existing_user = await self.repository.find_by_dairy_name(user.dairyName)
        if existing_user:
            raise HTTPException(status_code=400, detail="Dairy with this name already exists")

        # Generate temporary password
        temp_password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

        # Generate dairy ID
        dairy_initials = user.dairyName[:2].upper() if user.dairyName else "XX"
        owner_initials = user.ownerName[:2].upper() if user.ownerName else "XX"
        dairy_id = f"{dairy_initials}{owner_initials}{random.randint(100000, 999999)}"

        # Create user object
        current_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        user_obj = UserModel(
            dairyName=user.dairyName,
            ownerName=user.ownerName,
            phoneNumber=user.phoneNumber,
            password=temp_password,
            isNew=True,
            dairyId=dairy_id,
            createdDate=current_time,
            updatedDate=current_time,
        )

        # Save user
        user_dict = user_obj.dict()
        result = await self.repository.create_user(user_dict)
        return {
            "message": "Dairy created Successfully",
            "dairy": result
        }

    async def login(self, details: LoginModel):
        user = await self.repository.find_by_phone(details.phoneNumber)
        if not user:
            raise HTTPException(status_code=401, detail="Phone number does not exist")

        user_data = UserModel(**user)
        if details.password != user_data.password:
            raise HTTPException(status_code=401, detail="Invalid password/phone number")

        access_token = create_access_token({"sub": str(user_data.phoneNumber)})
        return {
            "message": "User logged in Successfully",
            "accessToken": access_token,
            "isNew": user_data.isNew
        }

    async def change_password(self, passwords: ChangePasswordModel, token: str):
        # Verify token and get user
        phone_number = verify_token(token)
        user = await self.repository.find_by_phone(int(phone_number))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user_data = UserModel(**user)
        if passwords.oldPassword != user_data.password:
            return {"message": "Invalid old password"}

        # Update password
        current_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        update_data = {
            "password": passwords.newPassword,
            "isNew": False,
            "updatedDate": current_time
        }
        await self.repository.update_user(str(user["_id"]), update_data)
        return {"message": "Password updated successfully"}

user_service = UserService() 