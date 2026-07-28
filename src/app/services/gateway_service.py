from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.gateway import GatewayRoute
from app.db.repositories.route_repository import RouteRepository


class GatewayService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repository = RouteRepository(session)

    async def create_route(
        self,
        *,
        route_name: str,
        upstream_url: str,
        path_prefix: str,
        methods: list[str],
    ) -> GatewayRoute:
        route = await self._repository.create_route(
            route_name=route_name,
            upstream_url=upstream_url,
            path_prefix=path_prefix,
            methods=methods,
        )
        await self._session.commit()
        return route

    async def list_routes(self) -> list[GatewayRoute]:
        return await self._repository.list_routes()
