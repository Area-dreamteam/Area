import os
from pydantic_settings import BaseSettings


def get_env_file() -> str:
    env = os.getenv("ENV")
    if env is None:
        raise "No env file found"
    elif env == "dev":
        return ".env"
    elif env == "prod":
        return ".env.prod"
    elif env == "tests":
        return ".env.tests"


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_HOURS: int
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str
    TODOIST_CLIENT_ID: str
    TODOIST_CLIENT_SECRET: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    MICROSOFT_CLIENT_ID: str
    MICROSOFT_CLIENT_SECRET: str
    MICROSOFT_DIR_TENANT: str
    REDDIT_CLIENT_ID: str
    REDDIT_CLIENT_SECRET: str
    FRONT_URL: str
    CRON_USER: str = "root"

    class Config:
        env_file = get_env_file()


settings = Settings()
