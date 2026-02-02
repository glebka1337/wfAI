from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Waifu AI"
    DEBUG: bool = True
    DEFAULT_MODEL: str = "llama3"
    LLM_BASE_URL: str = "http://localhost:11434/v1"
    LLM_API_KEY: str = "ollama"
    LLM_TEMPERATURE: float = 0.7
    CONTEXT_CHAR_LIMIT: int = 12000 
    INITIAL_LOAD_SIZE: int = 30
    
    MONGO_URL: str = "mongodb://localhost:27017"
    DB_NAME: str = "waifu_db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()