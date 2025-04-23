from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Library Management System"
    VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    API_V1_STR: str = "/api"

    DATABASE_URL: str = "sqlite:///./library.db"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # ✅ Ajoute ces lignes :
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "library_db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()