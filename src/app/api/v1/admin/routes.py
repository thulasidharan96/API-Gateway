from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def admin_status() -> dict[str, str]:
    return {"status": "ok"}
