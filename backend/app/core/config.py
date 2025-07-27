"""
Configuration settings for Fashioning.ai backend
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Fashioning.ai"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000", 
        "http://127.0.0.1:3000", 
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        # Add your Vercel domain here when deployed
        "https://fashioning-ai.vercel.app",
        "https://fashioning-ai-git-main-fa-anony-mous.vercel.app",
        "https://fashioning-ai-fa-anony-mous.vercel.app"
    ]
    
    
    # Algolia
    ALGOLIA_APP_ID: str = ""
    ALGOLIA_API_KEY: str = ""  # For backward compatibility
    ALGOLIA_SEARCH_API_KEY: str = ""
    ALGOLIA_WRITE_API_KEY: str = ""
    ALGOLIA_ADMIN_API_KEY: str = ""
    
    # AI/ML APIs
    GEMINI_API_KEY: str = ""
    HUGGINGFACE_API_KEY: str = ""
    
    # External APIs
    WEATHER_API_KEY: str = ""
    INSTAGRAM_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"

# Create settings instance
settings = Settings()