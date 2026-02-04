from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # --- App ---
    PROJECT_NAME: str = "Waifu AI"
    DEBUG: bool = True
    
    # --- LLM (Generation) ---
    DEFAULT_MODEL: str = "llama3"
    LLM_BASE_URL: str = "http://localhost:11434/v1" 
    LLM_API_KEY: str = "ollama" 
    LLM_TEMPERATURE: float = 0.7
    CONTEXT_CHAR_LIMIT: int = 12000 
    
    # --- Embeddings (Vectors) ---
    EMBEDDING_MODEL: str = "nomic-embed-text" 

    # --- Qdrant (Memory) ---
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "waifu_memory_v1"

    MONGO_URL: str = "mongodb://localhost:27017"
    DB_NAME: str = "waifu_db"
    INITIAL_LOAD_SIZE: int = 30

    # --- S3 (MinIO) ---
    S3_ENDPOINT_URL: str = "http://localhost:9000"
    S3_PUBLIC_URL: str = "http://localhost:9000"  # URL accessible from browser
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET_NAME: str = "waifu-icons"
    S3_REGION_NAME: str = "us-east-1" # MinIO default

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()