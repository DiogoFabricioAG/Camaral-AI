import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    STRIPE_API_KEY: str
    DATABASE_URL: str = "sqlite:///./test.db"
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
