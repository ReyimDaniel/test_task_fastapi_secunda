from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    database_url: str | None = None
    db_echo: bool = False

    api_v1_prefix: str = '/api/v1'
    alembic_prefix: str = '/alembic'

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
