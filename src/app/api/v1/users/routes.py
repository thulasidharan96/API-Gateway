from __future__ import annotations

from fastapi import APIRouter, Depends

from app.db.models.user import User
from app.dependencies.auth import get_current_user
from app.schemas.auth import UserProfile

router = APIRouter()


@router.get("/me", response_model=UserProfile)
async def get_current_profile(current_user: User = Depends(get_current_user)) -> UserProfile:
    return UserProfile(
        id=str(current_user.id),
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
    )
