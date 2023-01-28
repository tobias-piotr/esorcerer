import json
import uuid
from functools import reduce

import structlog
from fastapi import status

from esorcerer.domain import exceptions, models, repositories

logger = structlog.get_logger(__name__)


class EventService:
    """Orchestrator for event processes."""

    def __init__(
        self,
        *,
        events: repositories.EventRepository,
        cache: repositories.CacheRepository,
    ) -> None:
        self.events = events
        self.cache = cache

    async def create(self, data: models.EventCreateModel) -> models.EventModel:
        """Create a new event."""
        logger.info("Creating an event", data=data)
        event = await self.events.create(data.dict())
        logger.info("Event created", created_event=event)
        return event

    async def get(self, uid: uuid.UUID) -> models.EventModel:
        """Get event by id."""
        return await self.events.get(uid)

    async def collect(
        self,
        filters: dict | None = None,
        ordering: list[str] | None = None,
        pagination: dict | None = None,
    ) -> list[models.EventModel]:
        """Get events based on parameters."""
        return await self.events.collect(filters, ordering, pagination)

    async def project(
        self,
        entity_id: uuid.UUID,
        use_cache: bool = True,
    ) -> models.ProjectionModel:
        """Create projection for given entity."""
        logger.info("Starting projection", entity_id=entity_id)

        projection_cache = self.cache.get(str(entity_id))
        if projection_cache and use_cache:
            projection = models.ProjectionModel(**json.loads(projection_cache))
            logger.info("Existing projection found", projection=projection)
            return projection

        logger.info("Building a new projection", entity_id=entity_id)

        events = await self.collect({"entity_id": entity_id}, ["created_at"])
        if not events:
            raise exceptions.NotFoundException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No events found for this entity",
            )

        body: dict = reduce(lambda acc, event: acc | event.payload, events, {})
        projection = models.ProjectionModel(
            started_at=events[0].created_at,
            last_update_at=events[-1].created_at,
            entries=len(events),
            entity_id=entity_id,
            body=body,
        )
        logger.info("Projection created", projection=projection)

        self.cache.set(str(entity_id), projection.json())
        return projection
