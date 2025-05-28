from pydantic_settings import BaseSettings
from typing import Optional

# Time constants
DAYS_2 = 2
HOURS_PER_DAY = 24
MINUTES_PER_HOUR = 60
TWO_DAYS_IN_MINUTES = DAYS_2 * HOURS_PER_DAY * MINUTES_PER_HOUR

class Settings(BaseSettings):
    # Database settings
    # MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_URL: str = "mongodb+srv://nishadkhadilkar81:NjKDTwwQYVsyjaG3@milkman-cluster.ybzyezr.mongodb.net/"
    DATABASE_NAME: str = "milkman"
    
    # JWT settings  
    SECRET_KEY: str = "a-string-secret-at-least-256-bits-long"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = TWO_DAYS_IN_MINUTES
    
    # Email settings
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM: Optional[str] = None
    MAIL_PORT: int = 587
    MAIL_SERVER: Optional[str] = None
    MAIL_SSL_TLS: bool = False
    MAIL_STARTTLS: bool = True
    USE_CREDENTIALS: bool = True

    class Config:
        env_file = ".env"
        # Allow extra fields (optional approach)
        # extra = "allow"

settings = Settings()