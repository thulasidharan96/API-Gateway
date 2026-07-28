from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.gateway import GatewayRoute


class RouteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_route(
        self,
        *,
        route_name: str,
        upstream_url: str,
        path_prefix: str,
        methods: list[str],
    ) -> GatewayRoute:
        route = GatewayRoute(
            route_name=route_name,
            upstream_url=upstream_url,
            path_prefix=path_prefix,
            methods=methods,
        )
        self._session.add(route)
        await self._session.flush()
        await self._session.refresh(route)
        return route

    async def list_routes(self) -> list[GatewayRoute]:
        statement = select(GatewayRoute).where(GatewayRoute.enabled.is_(True))
        return list((await self._session.execute(statement)).scalars().all())
