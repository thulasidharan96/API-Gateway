from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.db.session import get_db_session
from app.dependencies.auth import get_current_user
from app.schemas.client import ClientCreateRequest, ClientResponse, ClientSecretResponse
from app.services.client_service import ClientService

router = APIRouter()


@router.post("", response_model=ClientSecretResponse, status_code=status.HTTP_201_CREATED)
async def create_client(
    payload: ClientCreateRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
) -> ClientSecretResponse:
    service = ClientService(session)
    _, key_id, client_secret = await service.create_client(
        name=payload.name,
        environment=payload.environment,
        scopes=payload.scopes,
        allowed_apis=payload.allowed_apis,
        allowed_rate_limit=payload.allowed_rate_limit,
        created_by=current_user.email,
    )
    return ClientSecretResponse(key_id=key_id, client_secret=client_secret)


@router.get("", response_model=list[ClientResponse])
async def list_clients(
    session: AsyncSession = Depends(get_db_session),
    _: User = Depends(get_current_user),
) -> list[ClientResponse]:
    clients = await ClientService(session).list_clients()
    return [
        ClientResponse(
            id=str(client.id),
            name=client.name,
            environment=client.environment,
            status=client.status,
            scopes=client.scopes,
            allowed_apis=client.allowed_apis,
            allowed_rate_limit=client.allowed_rate_limit,
            expires_at=client.expires_at,
        )
        for client in clients
    ]
