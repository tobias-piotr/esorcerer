import json
import uuid
from functools import reduce

import structlog

from esorcerer.domain import exceptions, models, repositories, tasks

logger = structlog.get_logger(__name__)


class EventService:
    """Orchestrator for event processes."""

    def __init__(
        self,
        *,
        events: repositories.EventRepository,
        cache: repositories.CacheRepository,
        tasks_runner: type[tasks.TaskRunner]
    ) -> None:
        self.events = events
        self.cache = cache
        self.tasks = tasks_runner

    async def create(self, data: models.EventCreateModel) -> models.EventModel:
        """Create a new event."""
        logger.info("Creating an event", data=data)
        event = await self.events.create(data.dict())
        logger.info("Event created", created_event=event)
        self.tasks.run(tasks.TaskName.RUN_ACTIVE_HOOKS, event_id=event.id)
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
            raise exceptions.NotFoundError(detail="No events found for this entity")

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


class HookService:
    """Orchestrator for hook processes."""

    def __init__(self, *, hooks: repositories.HookRepository) -> None:
        self.hooks = hooks

    async def create(self, data: models.HookCreateModel) -> models.HookModel:
        """Create a new hook."""
        logger.info("Creating a new hook", data=data)
        hook = await self.hooks.create(data.dict())
        logger.info("New hook created", hook=hook)
        return hook

    async def get(self, uid: uuid.UUID) -> models.HookModel:
        """Get hook by id."""
        return await self.hooks.get(uid)

    async def collect(
        self,
        filters: dict | None = None,
        ordering: list[str] | None = None,
        pagination: dict | None = None,
    ) -> list[models.HookModel]:
        """Get hooks based on parameters."""
        return await self.hooks.collect(filters, ordering, pagination)

    async def update(
        self,
        uid: uuid.UUID,
        data: models.HookUpdateModel,
    ) -> models.HookModel:
        """Update hook with given data."""
        return await self.hooks.update(
            uid,
            data.dict(
                exclude_unset=True,
                exclude_defaults=True,
            ),
        )

    async def delete(self, uid: uuid.UUID) -> None:
        """Delete hook."""
        return await self.hooks.delete(uid)
