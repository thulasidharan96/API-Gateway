from __future__ import annotations

from redis.asyncio import Redis


class RateLimitStrategy:
    async def allow(self, *, redis: Redis, key: str, limit: int, window_seconds: int) -> bool:
        current = await redis.incr(key)
        if current == 1:
            await redis.expire(key, window_seconds)
        return current <= limit
