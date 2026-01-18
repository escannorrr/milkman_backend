from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi import BackgroundTasks

class SendEmail:
    
    async def send_temp_password_email(background_tasks: BackgroundTasks, email: str, owner_name: str, temp_password: str):
        
        # Email configuration (should be moved to a config file or environment variables)
        email_conf = ConnectionConfig(
            MAIL_USERNAME="nishadkhadilkar81@gmail.com",
            MAIL_PASSWORD="bzjk ibqn koef wehz",
            MAIL_FROM="nishadkhadilkar81@gmail.com",
            MAIL_PORT=587,
            MAIL_SERVER="smtp.gmail.com",
            MAIL_SSL_TLS=False,
            MAIL_STARTTLS=True,
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