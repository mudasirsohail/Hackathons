from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # LLM
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    CHAT_MODEL: str = "gpt-3.5-turbo"  # Default model

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra variables in env file


settings = Settings()