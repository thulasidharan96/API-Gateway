from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.client import Client, ClientKey


class ClientRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_client(
        self,
        *,
        name: str,
        environment: str,
        scopes: list[str],
        allowed_apis: list[str],
        allowed_rate_limit: int,
        created_by: str,
    ) -> Client:
        client = Client(
            name=name,
            environment=environment,
            scopes=scopes,
            allowed_apis=allowed_apis,
            allowed_rate_limit=allowed_rate_limit,
            created_by=created_by,
        )
        self._session.add(client)
        await self._session.flush()
        await self._session.refresh(client)
        return client

    async def create_key(self, *, client: Client, key_id: str, secret_hash: str) -> ClientKey:
        key = ClientKey(client_id=client.id, key_id=key_id, secret_hash=secret_hash)
        self._session.add(key)
        await self._session.flush()
        await self._session.refresh(key)
        return key

    async def list_clients(self) -> list[Client]:
        statement = select(Client).order_by(Client.created_at.desc())
        return list((await self._session.execute(statement)).scalars().all())
