from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.exceptions import AuthenticationError
from app.core.security import decode_token
from app.db.session import get_db_session
from app.schemas.auth import (
    LoginRequest,
    MessageResponse,
    RefreshRequest,
    RegisterRequest,
    TokenPair,
)
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: RegisterRequest,
    session: AsyncSession = Depends(get_db_session),
    settings: Settings = Depends(get_settings),
) -> MessageResponse:
    service = AuthService(session=session, settings=settings)
    try:
        await service.register(
            email=payload.email,
            credential=payload.credential,
            full_name=payload.full_name,
        )
    except AuthenticationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return MessageResponse(message="User registered")


@router.post("/login", response_model=TokenPair)
async def login_user(
    payload: LoginRequest,
    session: AsyncSession = Depends(get_db_session),
    settings: Settings = Depends(get_settings),
) -> TokenPair:
    service = AuthService(session=session, settings=settings)
    try:
        access_token, refresh_token = await service.login(
            email=payload.email,
            credential=payload.credential,
        )
    except AuthenticationError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    return TokenPair(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenPair)
async def refresh_tokens(
    payload: RefreshRequest,
    session: AsyncSession = Depends(get_db_session),
    settings: Settings = Depends(get_settings),
) -> TokenPair:
    service = AuthService(session=session, settings=settings)
    decoded = decode_token(payload.refresh_token, settings)
    if decoded.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id = UUID(str(decoded["sub"]))
    token_family = str(decoded["fam"])
    access_token, refresh_token = await service.rotate_refresh_token(
        user_id=user_id,
        token_family=token_family,
        current_refresh=payload.refresh_token,
    )
    return TokenPair(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout", response_model=MessageResponse)
async def logout_user() -> MessageResponse:
    return MessageResponse(message="Logout accepted")
