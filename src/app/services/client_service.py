from __future__ import annotations

import secrets

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.db.models.client import Client
from app.db.repositories.client_repository import ClientRepository


class ClientService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repository = ClientRepository(session)

    async def create_client(
        self,
        *,
        name: str,
        environment: str,
        scopes: list[str],
        allowed_apis: list[str],
        allowed_rate_limit: int,
        created_by: str,
    ) -> tuple[Client, str, str]:
        client = await self._repository.create_client(
            name=name,
            environment=environment,
            scopes=scopes,
            allowed_apis=allowed_apis,
            allowed_rate_limit=allowed_rate_limit,
            created_by=created_by,
        )
        key_id = f"ck_{secrets.token_urlsafe(16)}"
        client_secret = secrets.token_urlsafe(48)
        await self._repository.create_key(
            client=client, key_id=key_id, secret_hash=hash_password(client_secret)
        )
        await self._session.commit()
        return client, key_id, client_secret

    async def list_clients(self) -> list[Client]:
        return await self._repository.list_clients()
