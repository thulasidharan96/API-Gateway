"""initial schema

Revision ID: 20260727_0001
Revises:
Create Date: 2026-07-27 20:00:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20260727_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "roles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False, unique=True),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "permissions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False, unique=True),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "clients",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("environment", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("allowed_apis", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("scopes", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("allowed_rate_limit", sa.Integer(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", sa.String(length=320), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("name", "environment", name="uq_clients_name_environment"),
    )

    op.create_table(
        "client_keys",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "client_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("clients.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("key_id", sa.String(length=64), nullable=False, unique=True),
        sa.Column("secret_hash", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_client_keys_client_id", "client_keys", ["client_id"], unique=False)

    op.create_table(
        "refresh_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("token_family", sa.String(length=64), nullable=False),
        sa.Column("token_hash", sa.String(length=255), nullable=False, unique=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_revoked", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_refresh_tokens_user_id", "refresh_tokens", ["user_id"], unique=False)
    op.create_index(
        "ix_refresh_tokens_token_family", "refresh_tokens", ["token_family"], unique=False
    )

    op.create_table(
        "gateway_routes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("route_name", sa.String(length=120), nullable=False, unique=True),
        sa.Column("upstream_url", sa.String(length=500), nullable=False),
        sa.Column("path_prefix", sa.String(length=255), nullable=False),
        sa.Column("methods", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("strip_prefix", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("timeout_ms", sa.Integer(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "service_registry",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("service_name", sa.String(length=120), nullable=False, unique=True),
        sa.Column("base_url", sa.String(length=500), nullable=False),
        sa.Column("health_path", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("actor_id", sa.String(length=320), nullable=False),
        sa.Column("action", sa.String(length=120), nullable=False),
        sa.Column("entity", sa.String(length=120), nullable=False),
        sa.Column("entity_id", sa.String(length=64), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "rate_limits",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("scope", sa.String(length=32), nullable=False),
        sa.Column("subject", sa.String(length=128), nullable=False),
        sa.Column("limit", sa.Integer(), nullable=False),
        sa.Column("window_seconds", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_rate_limits_subject", "rate_limits", ["subject"], unique=False)

    op.create_table(
        "api_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("request_id", sa.String(length=64), nullable=False),
        sa.Column("route", sa.String(length=255), nullable=False),
        sa.Column("method", sa.String(length=16), nullable=False),
        sa.Column("status_code", sa.Integer(), nullable=False),
        sa.Column("duration_ms", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_api_logs_request_id", "api_logs", ["request_id"], unique=False)

    op.create_table(
        "request_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("request_id", sa.String(length=64), nullable=False),
        sa.Column("correlation_id", sa.String(length=64), nullable=False),
        sa.Column(
            "client_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("clients.id"), nullable=True
        ),
        sa.Column(
            "user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True
        ),
        sa.Column("path", sa.String(length=255), nullable=False),
        sa.Column("response_code", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_request_logs_request_id", "request_logs", ["request_id"], unique=False)
    op.create_index(
        "ix_request_logs_correlation_id", "request_logs", ["correlation_id"], unique=False
    )

    op.create_table(
        "user_roles",
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "role_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("roles.id", ondelete="CASCADE"),
            primary_key=True,
        ),
    )

    op.create_table(
        "role_permissions",
        sa.Column(
            "role_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("roles.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "permission_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("permissions.id", ondelete="CASCADE"),
            primary_key=True,
        ),
    )


def downgrade() -> None:
    op.drop_table("role_permissions")
    op.drop_table("user_roles")
    op.drop_index("ix_request_logs_correlation_id", table_name="request_logs")
    op.drop_index("ix_request_logs_request_id", table_name="request_logs")
    op.drop_table("request_logs")
    op.drop_index("ix_api_logs_request_id", table_name="api_logs")
    op.drop_table("api_logs")
    op.drop_index("ix_rate_limits_subject", table_name="rate_limits")
    op.drop_table("rate_limits")
    op.drop_table("audit_logs")
    op.drop_table("service_registry")
    op.drop_table("gateway_routes")
    op.drop_index("ix_refresh_tokens_token_family", table_name="refresh_tokens")
    op.drop_index("ix_refresh_tokens_user_id", table_name="refresh_tokens")
    op.drop_table("refresh_tokens")
    op.drop_index("ix_client_keys_client_id", table_name="client_keys")
    op.drop_table("client_keys")
    op.drop_table("clients")
    op.drop_table("permissions")
    op.drop_table("roles")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
