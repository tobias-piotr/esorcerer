import uuid
from typing import Protocol

from esorcerer.domain import models


class EventRepository(Protocol):
    """Event repository interface."""

    async def create(self, data: dict) -> models.EventModel:
        """Create a new event."""
        ...

    async def get(self, uid: uuid.UUID) -> models.EventModel:
        """Get event by id."""
        ...

    async def collect(
        self,
        filters: dict | None = None,
        ordering: list[str] | None = None,
        pagination: dict | None = None,
    ) -> list[models.EventModel]:
        """Get events based on parameters."""
        ...


class CacheRepository(Protocol):
    """Cache repository."""

    def set(self, key: str, data: str) -> None:
        """Cache data by the key."""

    def get(self, key: str) -> bytes | None:
        """Get cache by the key."""
