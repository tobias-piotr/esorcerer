from pydantic import BaseSettings


class Settings(BaseSettings):
    """App settings."""

    PROJECT_NAME: str = "esorcerer"
    DEBUG: bool = False
    ENVIRONMENT: str = "local"

    # API
    DOMAIN: str = "127.0.0.1"
    RATE_LIMIT: int = 10
    CORS_ALLOW_ORIGINS: list[str] = []
    API_PREFIX: str = "/eso"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
