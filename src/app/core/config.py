from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__", extra="ignore")

    app_name: str = "API Gateway Platform"
    app_version: str = "0.1.0"
    environment: Literal["development", "testing", "production"] = "development"
    api_prefix: str = "/api"

    server_host: str = "0.0.0.0"
    server_port: int = 8000
    server_workers: int = 2

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/api_gateway"
    redis_url: str = "redis://redis:6379/0"

    jwt_secret_key: SecretStr = Field(default=SecretStr("change-me-in-production"))
    jwt_algorithm: str = "HS256"
    access_token_ttl_seconds: int = 900
    refresh_token_ttl_seconds: int = 1209600

    cors_allow_origins: list[str] = ["*"]
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]
    trusted_hosts: list[str] = ["*"]

    redis_rate_limit_prefix: str = "ratelimit"

    @property
    def is_development(self) -> bool:
        return self.environment == "development"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
