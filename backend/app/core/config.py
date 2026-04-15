from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "F1 Telemetry Simulation System"
    api_prefix: str = "/api/v1"
    database_url: str = Field(
        default="postgresql+psycopg2://telemetry:telemetry@localhost:5432/telemetry",
        alias="DATABASE_URL",
    )
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"], alias="CORS_ORIGINS")
    live_stale_seconds: int = Field(default=3, alias="LIVE_STALE_SECONDS")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
