import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "MedCare E-Prescription Auth System"
    API_V1_STR: str = "/api/v1"
    MEDCARE_SECRET_KEY: str = os.getenv("MEDCARE_SECRET_KEY", "default_medcare_secret_key_2026")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "20"))

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()