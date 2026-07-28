from __future__ import annotations

import hashlib
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.core.exceptions import AuthenticationError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.db.models.token import RefreshToken
from app.db.models.user import User
from app.db.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, *, session: AsyncSession, settings: Settings) -> None:
        self._session = session
        self._settings = settings
        self._users = UserRepository(session)

    async def register(self, *, email: str, credential: str, full_name: str) -> User:
        existing = await self._users.get_by_email(email)
        if existing is not None:
            raise AuthenticationError("Email is already registered")

        user = await self._users.create(
            email=email, password_hash=hash_password(credential), full_name=full_name
        )
        await self._session.commit()
        return user

    async def login(self, *, email: str, credential: str) -> tuple[str, str]:
        user = await self._users.get_by_email(email)
        if user is None or not verify_password(credential, user.password_hash):
            raise AuthenticationError("Invalid credentials")

        token_family = uuid4()
        access_token = create_access_token(user.id, self._settings, scopes=["user"])
        refresh_token = create_refresh_token(user.id, token_family, self._settings)

        hashed = hashlib.sha256(refresh_token.encode()).hexdigest()
        self._session.add(
            RefreshToken(
                user_id=user.id,
                token_family=str(token_family),
                token_hash=hashed,
                expires_at=datetime.now(UTC)
                + timedelta(seconds=self._settings.refresh_token_ttl_seconds),
            ),
        )
        await self._session.commit()
        return access_token, refresh_token

    async def rotate_refresh_token(
        self, *, user_id: UUID, token_family: str, current_refresh: str
    ) -> tuple[str, str]:
        token_hash = hashlib.sha256(current_refresh.encode()).hexdigest()
        existing_statement = select(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.token_family == token_family,
            RefreshToken.token_hash == token_hash,
            RefreshToken.is_revoked.is_(False),
        )
        active_token = (await self._session.execute(existing_statement)).scalar_one_or_none()
        if active_token is None:
            raise AuthenticationError("Refresh token invalid or revoked")
        active_token.is_revoked = True

        new_access = create_access_token(user_id, self._settings, scopes=["user"])
        new_refresh = create_refresh_token(user_id, UUID(token_family), self._settings)
        self._session.add(
            RefreshToken(
                user_id=user_id,
                token_family=token_family,
                token_hash=hashlib.sha256(new_refresh.encode()).hexdigest(),
                expires_at=datetime.now(UTC)
                + timedelta(seconds=self._settings.refresh_token_ttl_seconds),
            ),
        )
        await self._session.commit()
        return new_access, new_refresh
