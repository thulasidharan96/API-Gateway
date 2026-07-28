from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class RouteCreateRequest(BaseModel):
    route_name: str = Field(min_length=3, max_length=120)
    upstream_url: HttpUrl
    path_prefix: str = Field(min_length=1, max_length=255)
    methods: list[str] = Field(default_factory=lambda: ["GET"])


class RouteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    route_name: str
    upstream_url: str
    path_prefix: str
    methods: list[str]
    enabled: bool
