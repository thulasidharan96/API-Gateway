from __future__ import annotations

from redis.asyncio import Redis

from app.core.config import Settings
from app.core.limiter import RateLimitStrategy


class RateLimitService:
    def __init__(
        self, *, redis_client: Redis, settings: Settings, strategy: RateLimitStrategy | None = None
    ) -> None:
        self._redis = redis_client
        self._settings = settings
        self._strategy = strategy or RateLimitStrategy()

    async def enforce(
        self, *, scope: str, subject: str, endpoint: str, limit: int, window_seconds: int
    ) -> bool:
        key = f"{self._settings.redis_rate_limit_prefix}:{scope}:{subject}:{endpoint}"
        return await self._strategy.allow(
            redis=self._redis,
            key=key,
            limit=limit,
            window_seconds=window_seconds,
        )
