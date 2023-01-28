import asyncio

import structlog
from tortoise import Tortoise

from esorcerer.domain import services
from esorcerer.plugins.cache.repositories import RedisRepository
from esorcerer.plugins.database.repositories import EventDBRepository
from esorcerer.plugins.tasks.worker import celery_app
from esorcerer.settings import settings

logger = structlog.get_logger(__name__)


async def get_event_service() -> services.EventService:  # pragma: no cover
    """Initialize event service with database connection."""
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["esorcerer.plugins.database.models"]},
    )
    return services.EventService(
        events=EventDBRepository(),
        cache=RedisRepository(),
    )


@celery_app.task()
def health_check() -> dict:
    """Check health of the worker."""
    return {"detail": "Ok"}


@celery_app.task()
def create_expensive_projections() -> int:
    """Cache the biggest projections.

    Look for entities that have many events associated to them
    and create their projections.
    """

    async def func() -> int:
        service = await get_event_service()
        entity_ids = await service.events.group_by("entity_id", 5)
        for eid in entity_ids:
            await service.project(eid["entity_id"], use_cache=False)

        await Tortoise.close_connections()
        return len(entity_ids)

    logger.info("Looking for expensive projections")
    entities_count = asyncio.run(func())
    logger.info("Done processing big projections", count=entities_count)
    return entities_count
