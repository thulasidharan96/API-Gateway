from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any, cast
from uuid import UUID

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from jose import JWTError, jwt

from app.core.config import Settings

password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return password_hasher.verify(password_hash, password)
    except VerifyMismatchError:
        return False


def create_access_token(subject: UUID, settings: Settings, scopes: list[str] | None = None) -> str:
    expires_at = datetime.now(UTC) + timedelta(seconds=settings.access_token_ttl_seconds)
    payload: dict[str, Any] = {
        "sub": str(subject),
        "type": "access",
        "scopes": scopes or [],
        "exp": expires_at,
        "iat": datetime.now(UTC),
    }
    return cast(
        str,
        jwt.encode(
            payload, settings.jwt_secret_key.get_secret_value(), algorithm=settings.jwt_algorithm
        ),
    )


def create_refresh_token(subject: UUID, token_family: UUID, settings: Settings) -> str:
    expires_at = datetime.now(UTC) + timedelta(seconds=settings.refresh_token_ttl_seconds)
    payload: dict[str, Any] = {
        "sub": str(subject),
        "type": "refresh",
        "fam": str(token_family),
        "exp": expires_at,
        "iat": datetime.now(UTC),
    }
    return cast(
        str,
        jwt.encode(
            payload, settings.jwt_secret_key.get_secret_value(), algorithm=settings.jwt_algorithm
        ),
    )


def decode_token(token: str, settings: Settings) -> dict[str, Any]:
    try:
        return cast(
            dict[str, Any],
            jwt.decode(
                token,
                settings.jwt_secret_key.get_secret_value(),
                algorithms=[settings.jwt_algorithm],
            ),
        )
    except JWTError as exc:
        raise ValueError("Invalid token") from exc
