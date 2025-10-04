from pydantic_settings import BaseSettings

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

    class Config:
        env_file = ".env"

settings = Settings()
