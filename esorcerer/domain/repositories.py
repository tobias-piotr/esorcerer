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

    async def collect(self) -> list[models.EventModel]:
        """Get events based on parameters."""
        ...
