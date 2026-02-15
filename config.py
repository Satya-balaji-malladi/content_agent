import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # App
    APP_ENV: str = "development"
    PORT: int = 8080

    # Google Gemini
    GOOGLE_API_KEY: str

    # Groq (Failover)
    GROQ_API_KEY: str | None = None

    # Instagram
    INSTAGRAM_ACCESS_TOKEN: str = "place_holder"
    INSTAGRAM_ACCOUNT_ID: str = "place_holder"
    
    # ImgBB API Key (Loaded from environment)
    IMGBB_API_KEY: str = os.getenv('IMGBB_API_KEY')

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
