from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    mongo_uri: str = Field(alias="MONGODB_URI")
    mongo_db: str = Field(alias="MONGODB_DB")

    rabbitmq_host: str = Field(default="localhost", alias="RABBITMQ_HOST")
    rabbitmq_port: int = Field(default=5672, alias="RABBITMQ_PORT")
    rabbitmq_user: str = Field(default="guest", alias="RABBITMQ_USER")
    rabbitmq_pass: str = Field(default="guest", alias="RABBITMQ_PASS")

    @property
    def rabbitmq_url(self) -> str:
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_pass}@{self.rabbitmq_host}:{self.rabbitmq_port}/"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
