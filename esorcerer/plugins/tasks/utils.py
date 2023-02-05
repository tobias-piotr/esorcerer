from contextlib import asynccontextmanager
from typing import AsyncGenerator

from tortoise import Tortoise

from esorcerer.domain import services
from esorcerer.plugins.cache.repositories import RedisRepository
from esorcerer.plugins.database.repositories import EventDBRepository, HookDBRepository
from esorcerer.plugins.tasks.runner import CeleryTaskRunner
from esorcerer.settings import settings


@asynccontextmanager
async def get_event_service() -> AsyncGenerator[services.EventService, None]:
    """Initialize event service with database connection."""
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["esorcerer.plugins.database.models"]},
    )
    yield services.EventService(
        events=EventDBRepository(),
        cache=RedisRepository(),
        tasks_runner=CeleryTaskRunner,
    )
    await Tortoise.close_connections()


@asynccontextmanager
async def get_hook_service() -> AsyncGenerator[services.HookService, None]:
    """Initialize hook service with database connection."""
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={"models": ["esorcerer.plugins.database.models"]},
    )
    yield services.HookService(hooks=HookDBRepository())
    await Tortoise.close_connections()
