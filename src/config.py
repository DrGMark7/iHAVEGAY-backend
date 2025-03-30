import yaml
import logging
from pathlib import Path
from typing import Dict, Any, List
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # MongoDB Settings
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "computer_parts_db")
    MONGO_MAX_CONNECTIONS: int = int(os.getenv("MONGO_MAX_CONNECTIONS", "10"))
    MONGO_MIN_CONNECTIONS: int = int(os.getenv("MONGO_MIN_CONNECTIONS", "1"))
    
    # JWT Settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "secret_key_for_development_only")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    
    # API Settings
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    
    # Server Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    RELOAD: bool = os.getenv("RELOAD", "True").lower() in ("true", "1", "t")
    WORKERS: int = int(os.getenv("WORKERS", "1"))
    
    # CORS Settings
    CORS_ORIGINS: List[str] = ["*"]
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore",  # Allow extra fields to be provided
    }

# Create global settings object
settings = Settings()

# Environment-specific configurations
if settings.ENVIRONMENT == "production":
    # Override settings for production
    settings.DEBUG = False
    settings.CORS_ORIGINS = [
        "https://app.example.com",
        "https://admin.example.com"
    ]
elif settings.ENVIRONMENT == "testing":
    # Override settings for testing
    settings.MONGO_DB_NAME = f"{settings.MONGO_DB_NAME}_test"
    settings.DEBUG = True

def get_settings() -> Settings:
    """
    Get application settings
    """
    return settings

def loadConfig() -> Dict:
    try:
        with open('config.yaml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data
    except FileNotFoundError:
        logging.error("Config file not found")
        return None

class BaseConfig:
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
        self.config = loadConfig()

    """
    __getitem__ method is used to access the item using the key.
    Returns the value of the key Any String
    """
    def __getitem__(self, key) -> Any:
        try:
            return self.config[key]
        except KeyError:
            logging.error(f"Key {key} not found in config") 
            return None
    
    def __setitem__(self, key, value):
        self.config[key] = value

    def __delitem__(self, key):
        del self.config[key]

    def show(self) -> None:
        for key, value in self.config.items():
            print(f"[Base Config] {key}")
            for k, v in value.items():
                print(f'\t{k}: {v}')
    

