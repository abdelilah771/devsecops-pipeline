from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FixSuggester"
    API_V1_STR: str = "/api/v1"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # Postgres
    # Postgres
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "root"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_DB: str = "vulndetec"

    # RabbitMQ
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"

    # Gemini
    GEMINI_API_KEY: str = "AIzaSyC6xT_q8TI9q9M54xN4fd7K5yfuAeoDbdo"
    LLM_PROVIDER: str = "gemini"
    LLM_MODEL: str = "gemini-3-flash-preview"

    # App Config
    PORT: int = 8003
    LOG_LEVEL: str = "INFO"
    SERVICE_NAME: str = "FixSuggester"
    
    # Testing
    MOCK_DB: bool = False
    MOCK_REDIS: bool = True
    MOCK_AI: bool = False # Real Gemini API
    REDIS_ENABLED: bool = True
    POSTGRES_URI: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
