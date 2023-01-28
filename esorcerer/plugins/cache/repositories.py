import redis

from esorcerer.settings import settings


class RedisRepository:
    """Redis cache repository."""

    def __init__(self, expiry_time: int = 600) -> None:
        self.r = redis.Redis.from_url(settings.REDIS_URL)
        self.expiry_time = expiry_time

    def set(self, key: str, data: str) -> None:
        """Cache data by the key."""
        self.r.set(key, data, self.expiry_time)

    def get(self, key: str) -> bytes | None:
        """Get cache by the key."""
        return self.r.get(key)
