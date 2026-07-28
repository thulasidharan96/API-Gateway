from __future__ import annotations

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, UUIDAuditMixin


class GatewayRoute(UUIDAuditMixin, Base):
    __tablename__ = "gateway_routes"

    route_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    upstream_url: Mapped[str] = mapped_column(String(500), nullable=False)
    path_prefix: Mapped[str] = mapped_column(String(255), nullable=False)
    methods: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)
    strip_prefix: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    timeout_ms: Mapped[int] = mapped_column(Integer, default=3000, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    extra_metadata: Mapped[dict[str, str]] = mapped_column(
        "metadata", JSONB, default=dict, nullable=False
    )


class ServiceRegistry(UUIDAuditMixin, Base):
    __tablename__ = "service_registry"

    service_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    base_url: Mapped[str] = mapped_column(String(500), nullable=False)
    health_path: Mapped[str] = mapped_column(String(255), default="/health", nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="healthy", nullable=False)
    extra_metadata: Mapped[dict[str, str]] = mapped_column(
        "metadata", JSONB, default=dict, nullable=False
    )
