from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

    DATABASE_URL: str
    UPLOAD_FOLDER: str = "uploads"

settings = Settings()

# Ensure upload directory exists on startup
os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)