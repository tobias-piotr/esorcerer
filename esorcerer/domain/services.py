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
        # TODO: 404
        return await self.repository.get(uid)

    async def collect(
        self,
        filters: dict | None = None,
        ordering: list[str] | None = None,
        pagination: dict | None = None,
    ) -> list[models.EventModel]:
        """Get events based on parameters."""
        return await self.repository.collect(filters, ordering, pagination)

    # TODO: Cache
    async def project(self, entity_id: uuid.UUID) -> models.ProjectionModel:
        """Create projection for given entity."""
        logger.info("Starting projection", entity_id=entity_id)
        events = await self.collect({"entity_id": entity_id}, ["created_at"])

        # TODO: If not events
        body = {}
        for event in events:
            body.update(event.payload)

        projection = models.ProjectionModel(
            created_at=events[0].created_at,
            last_update_at=events[-1].created_at,
            entries=len(events),
            entity_id=entity_id,
            body=body,
        )
        logger.info("Projection created", projection=projection)
        return projection
