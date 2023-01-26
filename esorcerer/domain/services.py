import uuid

import structlog

from esorcerer.domain import models, repositories

logger = structlog.get_logger(__name__)


class EventService:
    """Orchestrator for event processes."""

    def __init__(self, *, repository: repositories.EventRepository) -> None:
        self.repository = repository

    async def create(self, data: models.EventCreateModel) -> models.EventModel:
        """Create a new event."""
        logger.info("Creating an event", data=data)
        event = await self.repository.create(data.dict())
        logger.info("Event created", created_event=event)
        return event

    async def get(self, uid: uuid.UUID) -> models.EventModel:
        """Get event by id."""
        return await self.repository.get(uid)

    async def collect(self) -> list[models.EventModel]:
        """Get events based on parameters."""
        # TODO: Add filters
        return await self.repository.collect()
