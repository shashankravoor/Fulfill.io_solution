import os
from pydantic import BaseSettings, PostgresDsn

class Settings(BaseSettings):
    APP_NAME: str = "Product Importer"
    DATABASE_URL: PostgresDsn = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/products")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    CELERY_BROKER_URL: str = REDIS_URL
    CELERY_RESULT_BACKEND: str = REDIS_URL
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "/tmp/uploads")
    CHUNK_SIZE: int = 10 * 1024 * 1024  # 10MB

settings = Settings()
