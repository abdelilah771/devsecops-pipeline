from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # Service
    SERVICE_NAME: str = "LogParser"
    PORT: int = 8001
    
    # MongoDB
    MONGODB_URI: str = Field(alias="MONGODB_URI")
    MONGODB_DB: str = Field(alias="MONGODB_DB")
    
    # RabbitMQ
    RABBITMQ_HOST: str = Field(default="localhost", alias="RABBITMQ_HOST")
    RABBITMQ_PORT: int = Field(default=5672, alias="RABBITMQ_PORT")
    RABBITMQ_USER: str = Field(default="guest", alias="RABBITMQ_USER")
    RABBITMQ_PASS: str = Field(default="guest", alias="RABBITMQ_PASS")
    
    # Queues
    # Queues & Exchange
    QUEUE_RAW_LOGS: str = "raw_logs"
    QUEUE_PARSED_EVENTS: str = "logparser.vulndetector.queue" # Destination queue for VulnDetector
    
    RABBITMQ_EXCHANGE: str = "logpipeline.exchange"
    RABBITMQ_ROUTING_KEY: str = "logparsed.vuln.detect"

    @property
    def rabbitmq_url(self) -> str:
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_pass}@{self.rabbitmq_host}:{self.rabbitmq_port}/"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
