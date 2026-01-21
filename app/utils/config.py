"""
Configuration management for the application.
Loads environment variables and provides centralized config access.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4-turbo-preview"
    openai_embedding_model: str = "text-embedding-3-small"
    
    # Generation Parameters
    max_tokens: int = 1500
    temperature: float = 0.7
    
    # RAG Configuration
    top_k_results: int = 5
    
    # FAISS Configuration
    faiss_index_path: str = "data/faiss_index.bin"
    faiss_metadata_path: str = "data/faiss_metadata.json"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
