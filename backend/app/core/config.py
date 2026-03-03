from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    database_url: str = "sqlite:///./earnings.db"
    debug: bool = True
    class Config:
        env_file = ".env"

settings = Settings()
