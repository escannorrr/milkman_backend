from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi import BackgroundTasks
from core.config import settings

class SendEmail:
    
    async def send_temp_password_email(background_tasks: BackgroundTasks, email: str, owner_name: str, temp_password: str):
        
        # Email configuration
        email_conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
            MAIL_STARTTLS=settings.MAIL_STARTTLS,
            USE_CREDENTIALS=settings.USE_CREDENTIALS
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