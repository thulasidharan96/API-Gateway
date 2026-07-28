from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def developer_status() -> dict[str, str]:
    return {"status": "ok"}
