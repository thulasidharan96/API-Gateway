from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.db.session import get_db_session
from app.dependencies.auth import get_current_user
from app.schemas.gateway import RouteCreateRequest, RouteResponse
from app.services.gateway_service import GatewayService

router = APIRouter()


@router.post("/routes", response_model=RouteResponse, status_code=status.HTTP_201_CREATED)
async def create_gateway_route(
    payload: RouteCreateRequest,
    session: AsyncSession = Depends(get_db_session),
    _: User = Depends(get_current_user),
) -> RouteResponse:
    route = await GatewayService(session).create_route(
        route_name=payload.route_name,
        upstream_url=str(payload.upstream_url),
        path_prefix=payload.path_prefix,
        methods=payload.methods,
    )
    return RouteResponse(
        id=str(route.id),
        route_name=route.route_name,
        upstream_url=route.upstream_url,
        path_prefix=route.path_prefix,
        methods=route.methods,
        enabled=route.enabled,
    )


@router.get("/routes", response_model=list[RouteResponse])
async def list_gateway_routes(
    session: AsyncSession = Depends(get_db_session),
    _: User = Depends(get_current_user),
) -> list[RouteResponse]:
    routes = await GatewayService(session).list_routes()
    return [
        RouteResponse(
            id=str(route.id),
            route_name=route.route_name,
            upstream_url=route.upstream_url,
            path_prefix=route.path_prefix,
            methods=route.methods,
            enabled=route.enabled,
        )
        for route in routes
    ]
