from fastapi import BackgroundTasks, HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import random
import string
from datetime import datetime
from models.schemas.dairy import DairyModel, SignUpRequestModel, LoginModel, ChangePasswordModel
from repositories.dairy_repository import dairy_repository
from repositories.counter_repository import counter_repository
from utils.jwt_token import create_access_token, verify_token
import logging

class DairyService: 
    def __init__(self):
        self.repository = dairy_repository
        self.counter_repository = counter_repository

    logging.basicConfig(level=logging.INFO)

    async def create_dairy(self, dairy: SignUpRequestModel, background_tasks: BackgroundTasks):
        logging.info("Received request to create dairy: %s", dairy.dict())
        # Check if dairy already exists
        existing_dairy = await self.repository.find_by_phone(dairy.phoneNumber)
        if existing_dairy:
            raise HTTPException(status_code=400, detail="Dairy with this phone number already exists")

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
            email=dairy.email,  # Make sure email is included in the model
        )

        # Save dairy
        dairy_dict = dairy_obj.dict()
        result = await self.repository.create_dairy(dairy_dict)
        
        # Send email with temporary password
        await self.send_temp_password_email(
            background_tasks=background_tasks,
            email=dairy.email,
            owner_name=dairy.ownerName,
            temp_password=temp_password
        )
        
        return {
            "message": "Dairy created Successfully",
            "dairy": result,
            "emailSent": True
        }

    async def send_temp_password_email(self, background_tasks: BackgroundTasks, email: str, owner_name: str, temp_password: str):
        
        # Email configuration (should be moved to a config file or environment variables)
        email_conf = ConnectionConfig(
            MAIL_USERNAME="nishadkhadilkar81@gmail.com",
            MAIL_PASSWORD="bzjk ibqn koef wehz",
            MAIL_FROM="nishadkhadilkar81@gmail.com",
            MAIL_PORT=587,
            MAIL_SERVER="smtp.gmail.com",
            MAIL_SSL_TLS=True,
            MAIL_STARTTLS=False,
            USE_CREDENTIALS=True
        )
        
        # Create email content
        subject = "Your Milkman Account"
        body = f"""
        <html>
        <body>
            <h2>Welcome to Milkman</h2>
            <p>Hello {owner_name},</p>
            <p>Your account has been created successfully.</p>
            <p>Here is your temporary password: <strong>{temp_password}</strong></p>
            <p>Please login to your account and change your password as soon as possible.</p>
            <p>Thank you!</p>
        </body>
        </html>
        """
        
        # Create message schema
        message = MessageSchema(
            subject=subject,
            recipients=[email],
            body=body,
            subtype="html"
        )
        
        # Initialize FastMail
        fm = FastMail(email_conf)
        
        # Send email in the background
        background_tasks.add_task(fm.send_message, message)
        logging.info(f"Temporary password email sent to {email}")

    async def login(self, details: LoginModel):
        dairy = await self.repository.find_by_phone(details.phoneNumber)
        if not dairy:
            raise HTTPException(status_code=401, detail="Phone number does not exist")

        dairy_data = DairyModel(**dairy)
        if details.password != dairy_data.password:
            raise HTTPException(status_code=401, detail="Invalid password/phone number")

        access_token = create_access_token({"sub": str(dairy_data.phoneNumber),"auth_roles":["admin","user"]})
        return {
            "message": "Dairy logged in Successfully",
            "accessToken": access_token,
            "dairy_details": dairy_data
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

dairy_service = DairyService()