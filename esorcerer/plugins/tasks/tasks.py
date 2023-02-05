import asyncio
import uuid

import structlog

from esorcerer.domain import exceptions, tasks
from esorcerer.plugins.tasks.utils import get_event_service, get_hook_service
from esorcerer.plugins.tasks.worker import celery_app

logger = structlog.get_logger(__name__)


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
        async with get_event_service() as service:
            entity_ids = await service.events.group_by("entity_id", 5)
            for eid in entity_ids:
                await service.project(eid["entity_id"], use_cache=False)

        return len(entity_ids)

    logger.info("Looking for expensive projections")
    entities_count = asyncio.run(func())
    logger.info("Done processing big projections", count=entities_count)
    return entities_count


@celery_app.task(name=tasks.TaskName.RUN_ACTIVE_HOOKS.value)
def run_active_hooks(event_id: str) -> int:
    """Run all active hooks on created event."""

    async def func() -> int:
        async with get_event_service() as service:
            try:
                await service.get(uuid.UUID(event_id))
            except exceptions.NotFoundError:
                logger.error("Event not found", event_id=event_id)
                return 0

        async with get_hook_service() as service:
            hooks = await service.collect({"is_active": True})
            logger.info("Retrieved hooks to run", hooks=hooks)

        # TODO: Run hooks
        return len(hooks)

    logger.info("Running hooks", event_id=event_id)
    hooks_count = asyncio.run(func())
    logger.info("Done running hooks")
    return hooks_count
