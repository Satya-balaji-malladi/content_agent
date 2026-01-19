import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    APP_ENV: str = "development"
    PORT: int = 8080

    # Google Gemini
    # Google Gemini
    GOOGLE_API_KEY: str

    # Groq (Failover)
    GROQ_API_KEY: str | None = None

    # Instagram
    INSTAGRAM_ACCESS_TOKEN: str = "place_holder"
    INSTAGRAM_ACCOUNT_ID: str = "place_holder"
    IMGBB_API_KEY: str = "770edc9963563ed0800e734fc23daf61"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
