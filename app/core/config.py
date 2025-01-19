from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "LGTM Image Service"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str
    
    # Google Cloud
    GCP_PROJECT_ID: str
    GCP_BUCKET_NAME: str
    
    # Image settings
    MAX_IMAGE_SIZE: int = 5_242_880  # 5MB
    ALLOWED_IMAGE_TYPES: set = {"image/jpeg", "image/png", "image/gif"}
    
    # Cache
    REDIS_URL: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()