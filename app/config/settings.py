import os
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Set, Dict, List, Any, Optional, Tuple, Literal
from decouple import config

class Settings(BaseSettings):

    # Environment Settings
    ENV: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # API Documentation Setup
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "TransactShield Crowdfunding"
    PROJECT_DESCRIPTION: str = "API Documentation for this year's crowdfunding"
    VERSION: str = "1.0.0"
    
    # Base paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent


    RATE_LIMIT_PER_MINUTE: int = 60

    # CORS Settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]

    # Authentication
    SECRET_KEY: str = config("SECRET_KEY")
    ALGORITHM: str = config("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
