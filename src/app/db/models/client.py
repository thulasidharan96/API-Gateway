from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDAuditMixin


class Client(UUIDAuditMixin, Base):
    __tablename__ = "clients"
    __table_args__ = (UniqueConstraint("name", "environment", name="uq_clients_name_environment"),)

    name: Mapped[str] = mapped_column(String(120), nullable=False)
    environment: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="enabled", nullable=False)
    allowed_apis: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)
    scopes: Mapped[list[str]] = mapped_column(JSONB, default=list, nullable=False)
    allowed_rate_limit: Mapped[int] = mapped_column(Integer, default=1000, nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by: Mapped[str] = mapped_column(String(320), nullable=False)

    keys: Mapped[list[ClientKey]] = relationship(
        "ClientKey",
        back_populates="client",
        cascade="all, delete-orphan",
    )


class ClientKey(UUIDAuditMixin, Base):
    __tablename__ = "client_keys"

    client_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    key_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    secret_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    client: Mapped[Client] = relationship("Client", back_populates="keys")
