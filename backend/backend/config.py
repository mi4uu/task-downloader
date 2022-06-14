from enum import Enum
from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    dask_scheduler_host: str = Field(
        env="DASK_SCHEDULER_HOST", default="scheduler:8786"
    )
    app_port: int = Field(env="APP_PORT", default=8080)
    app_host: str = Field(env="APP_HOST", default="0.0.0.0")
    database_url: str = Field(
        env="DATABASE_URL", default="postgresql+asyncpg://user:password@database/db"
    )
    shared_storage_url: str = Field(env="STORAGE", default="/storage")
    redis_host: str = Field(env="REDIS_HOST", default="redis")
    redis_port: str = Field(env="REDIS_PORT", default="6379")
    redis_celery_db_index: str = Field(env="REDIS_CELERY_DB_INDEX", default="0")
    redis_store_db_index: str = Field(env="REDIS_STORE_DB_INDEX", default="1")
    rabbitmq_host: str = Field(env="RABBITMQ_HOST", default="rabbitmq")
    rabbit_username: str = Field(env="RABBITMQ_USERNAME", default="guest")
    rabbit_password: str = Field(env="RABBITMQ_PASSWORD", default="guest")
    rabbit_port: str = Field(env="RABBITMQ_PORT", default="5672")

    @property
    def broker_uri(self):
        return f"amqp://{self.rabbit_username}:{self.rabbit_password}@{self.rabbitmq_host}:{self.rabbit_port}//"

    @property
    def backend_uri(self):
        return (
            f"redis://{self.redis_host}:{self.redis_port}/{self.redis_celery_db_index}"
        )

    @property
    def redis_store_uri(self):
        return (
            f"redis://{self.redis_host}:{self.redis_port}/{self.redis_store_db_index}"
        )





def get_settings() -> AppSettings:
    return AppSettings()
