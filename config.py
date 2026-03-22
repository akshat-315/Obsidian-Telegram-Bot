from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TELEGRAM_API_KEY: str
    GITHUB_APP_ID: str
    GITHUB_APP_PRIVATE_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()