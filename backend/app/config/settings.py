from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    NEON_DB_URL: str

    # Qdrant
    QDRANT_URL: str
    QDRANT_API_KEY: str

    # LLM
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    EMBED_MODEL: str = "all-MiniLM-L6-v2"  # Using a free sentence transformer model
    CHAT_MODEL: str = "llama-3.1-8b-instant"  # Using currently supported Groq model

    # Processing
    CHUNK_SIZE: int = 600
    CHUNK_OVERLAP: int = 50

    # Qdrant collection names
    DOCUMENT_COLLECTION_NAME: str = "documents"

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra variables in env file


settings = Settings()