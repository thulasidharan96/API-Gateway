from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ClientCreateRequest(BaseModel):
    name: str = Field(min_length=3, max_length=120)
    environment: str = Field(pattern="^(development|testing|production)$")
    scopes: list[str] = Field(default_factory=list)
    allowed_apis: list[str] = Field(default_factory=list)
    allowed_rate_limit: int = Field(default=1000, ge=1)


class ClientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    environment: str
    status: str
    scopes: list[str]
    allowed_apis: list[str]
    allowed_rate_limit: int
    expires_at: datetime | None


class ClientSecretResponse(BaseModel):
    key_id: str
    client_secret: str
