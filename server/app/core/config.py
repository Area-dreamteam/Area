import os
from pydantic_settings import BaseSettings


def get_env_file() -> str:
    env = os.getenv("ENV")
    if env is None:
        return "No env file found"
    elif env == "dev":
        return ".env"
    elif env == "prod":
        return ".env"
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
    STRAVA_CLIENT_ID: str
    STRAVA_CLIENT_SECRET: str
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str
    TWITCH_CLIENT_ID: str
    TWITCH_CLIENT_SECRET: str
    CLASHROYALE_API_KEY: str
    GITHUB_LINK_CLIENT_ID: str
    GITHUB_LINK_CLIENT_SECRET: str
    DISCORD_BOT_TOKEN: str
    DISCORD_CLIENT_ID: str
    DISCORD_CLIENT_SECRET: str
    TRAKT_CLIENT_ID: str
    TRAKT_CLIENT_SECRET: str
    DROPBOX_CLIENT_ID: str
    DROPBOX_CLIENT_SECRET: str
    NOTION_CLIENT_ID: str
    NOTION_CLIENT_SECRET: str
    LINKEDIN_CLIENT_ID: str
    LINKEDIN_CLIENT_SECRET: str
    FIGMA_CLIENT_ID: str
    FIGMA_CLIENT_SECRET: str
    FRONT_URL: str
    CRON_USER: str = "root"
    EMAIL: str
    EMAIL_PASSWORD: str

    class Config:
        env_file = get_env_file()


settings = Settings()
