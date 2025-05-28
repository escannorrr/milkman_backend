from pydantic_settings import BaseSettings
from typing import Optional

# Time constants
DAYS_2 = 2
HOURS_PER_DAY = 24
MINUTES_PER_HOUR = 60
TWO_DAYS_IN_MINUTES = DAYS_2 * HOURS_PER_DAY * MINUTES_PER_HOUR

class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "milkman"
    SECRET_KEY: str = "a-string-secret-at-least-256-bits-long"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = TWO_DAYS_IN_MINUTES

    class Config:
        env_file = ".env"

settings = Settings() 